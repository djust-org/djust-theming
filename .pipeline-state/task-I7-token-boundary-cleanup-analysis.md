# I7: Token Boundary Cleanup — Analysis

## Summary

`ThemeTokens` (presets.py) currently owns 5 non-color fields that violate the intended boundary: ThemeTokens should own **color only**, while `design_tokens.py` and the `Theme` system (themes.py) own everything structural.

## Non-Color Fields in ThemeTokens

| Field | Type | Default | Purpose |
|---|---|---|---|
| `radius` | `float` | `0.5` | Border radius multiplier (output as `--radius: {val}rem`) |
| `card_lift_distance` | `float` | `1.0` | Pixels cards lift on hover (`--card-lift-distance`) |
| `card_glow_opacity` | `float` | `0.3` | Border glow effect strength (`--card-glow-opacity`) |
| `transition_speed` | `int` | `150` | Base transition duration in ms (`--transition-speed`) |
| `animation_intensity` | `str` | `"subtle"` | Animation level: subtle/moderate/dramatic (`--animation-intensity`) |

## Where Structural Tokens Already Exist

### design_tokens.py (theme-agnostic structural tokens)
- **`get_radius_extensions()`** — Defines `--radius-sm` through `--radius-full`, all derived from `var(--radius)`. This system already depends on `--radius` being set, but currently that value comes from `ThemeTokens.radius`.
- **`get_transition_tokens()`** — Defines `--duration-fast/normal/slow/slower` and `--ease-*` curves. This **overlaps** with `ThemeTokens.transition_speed` which outputs `--transition-speed`.
- **`get_shadow_tokens()`** — Theme-aware shadows, fully structural.

### themes.py (Theme system — complete structural tokens)
- **`BorderRadius` dataclass** — Full radius scale: `radius_sm`, `radius`, `radius_md`, `radius_lg`, `radius_xl`, `radius_2xl`, `radius_3xl`, `radius_full`.
- **`Animations` dataclass** — `duration_fast/normal/slow`, `ease_in/out/in_out`, optional `ease_bounce`.
- **`Theme` dataclass** — Composes `Typography`, `Spacing`, `BorderRadius`, `Shadows`, `Animations`, `ComponentStyles`.
- **`CompleteThemeCSSGenerator`** (theme_css_generator.py) — Generates all structural CSS vars from `Theme` objects, including full border-radius and animation scales.

The `Theme` system is the **proper home** for all structural tokens. The duplication in `ThemeTokens` is legacy.

## Consumers of ThemeTokens Non-Color Fields

### 1. `css_generator.py` — `ThemeCSSGenerator._tokens_to_css_vars()` (lines 104-111)
**The primary consumer.** Outputs these CSS vars into `:root`, `.dark`, and `prefers-color-scheme` blocks:
```python
lines.append(f"{indent}--radius: {tokens.radius}rem;")
lines.append(f"{indent}--card-lift-distance: {tokens.card_lift_distance}px;")
lines.append(f"{indent}--card-glow-opacity: {tokens.card_glow_opacity};")
lines.append(f"{indent}--transition-speed: {tokens.transition_speed}ms;")
lines.append(f"{indent}--animation-intensity: {tokens.animation_intensity};")
```

### 2. `high_contrast.py` — `HighContrastPresets.create_high_contrast_tokens()` (lines 67, 110)
Forwards `radius=base_tokens.radius` when creating high-contrast variants. Does **not** forward animation fields (they fall to defaults).

### 3. `high_contrast.py` — `HIGH_CONTRAST_PRESETS` dict (lines 181, 207, 240, 266)
Hard-coded `radius=8` or `radius=0` in pre-defined high-contrast presets. No animation fields set.

### 4. `shadcn.py` — `import_from_shadcn()` (line 134, 160)
Parses `radius` from shadcn JSON and passes it to `ThemeTokens(radius=radius)`. Does **not** import animation fields.

### 5. `shadcn.py` — `export_to_shadcn_format()` (lines 216, 238)
Exports `"radius": f"{light.radius}rem"` to shadcn JSON format.

### 6. `design_tokens.py` — `get_radius_extensions()` (line 82)
Uses `var(--radius)` in CSS calc expressions. Depends on `--radius` being set **somewhere** — currently that is `ThemeTokens`.

## Presets with Custom (Non-Default) Values

### Radius
- **16 presets** use `radius=0.5` (default)
- **12 presets** use `radius=0.75` (pastel_*, neon_*, earth_*, monochrome_*)
- **High-contrast presets** use `radius=8` or `radius=0`

### Animation Fields (only set explicitly in 10 of 20 dark-mode ThemeTokens)

| Preset | card_lift | glow_opacity | speed | intensity |
|---|---|---|---|---|
| pastel_blue (dark) | 1.0 | 0.2 | 150 | subtle |
| pastel_green (dark) | 1.0 | 0.2 | 150 | subtle |
| neon_pink (dark) | 2.0 | 0.35 | 175 | moderate |
| neon_green (dark) | 1.0 | 0.2 | 150 | subtle |
| neon_blue (dark) | 3.0 | 0.5 | 200 | dramatic |
| neon_purple (dark) | 3.0 | 0.5 | 200 | dramatic |
| neon_orange (dark) | 3.0 | 0.5 | 200 | dramatic |
| earth_forest (dark) | 1.0 | 0.2 | 150 | subtle |
| earth_desert (dark) | 1.0 | 0.25 | 150 | subtle |
| earth_ocean (dark) | 1.0 | 0.15 | 150 | subtle |
| monochrome (dark) | 2.0 | 0.3 | 175 | moderate |

Note: The first 10 presets (default through rose) **never** set animation fields — they rely on dataclass defaults.

## Proposed Migration

### What to Remove from ThemeTokens
All 5 non-color fields:
- `radius`
- `card_lift_distance`
- `card_glow_opacity`
- `transition_speed`
- `animation_intensity`

### Where They Should Live

**Option A (Recommended): Move `radius` to `ThemePreset`, remove animation fields entirely**

1. **`radius`** — Add a `radius: float = 0.5` field to `ThemePreset` (not `ThemeTokens`). Radius is per-theme, not per-light/dark-mode. The CSS generator reads it from `ThemePreset` and outputs `--radius` once in `:root`.
   - Avoids the current oddity where light and dark modes can have different radii (they never do in practice).

2. **`card_lift_distance`, `card_glow_opacity`, `transition_speed`, `animation_intensity`** — These are better served by the existing `design_tokens.py` transition tokens (`--duration-fast/normal/slow`) and the `Theme.animations` system. Remove them entirely.
   - The `--card-lift-distance` and `--card-glow-opacity` CSS vars are not consumed by any CSS in the codebase — they are set but never read. They were meant for user-space CSS.
   - `--transition-speed` duplicates `--duration-normal` from design_tokens.
   - `--animation-intensity` is a string token with no CSS consumer.

**Option B: Move all to design_tokens.py**
Less clean — design_tokens is meant for static, theme-agnostic values. Animation intensity varies per preset.

### Files Requiring Changes

| File | Change |
|---|---|
| `presets.py` | Remove 5 fields from `ThemeTokens`; add `radius` to `ThemePreset`; update all 20+ preset definitions |
| `css_generator.py` | Read radius from preset (not tokens); remove animation lines from `_tokens_to_css_vars()` |
| `high_contrast.py` | Move `radius` to `ThemePreset` level; remove from `ThemeTokens` constructors |
| `shadcn.py` | Import/export radius at preset level instead of token level |
| `types.d.ts` | Remove `radius` from ThemeTokens type; update ThemePreset type |

### Backward Compatibility

**Breaking changes:**
1. **`--radius` CSS var** — Will still be output, just sourced differently. **No CSS breakage.**
2. **`--card-lift-distance`, `--card-glow-opacity`, `--transition-speed`, `--animation-intensity` CSS vars** — Will no longer be emitted. Any user CSS referencing these will break.
   - Mitigation: These vars are never consumed internally. Users referencing them are unlikely but possible.
   - Recommendation: Emit them with hardcoded defaults in `design_tokens.py` for one release cycle, with a deprecation comment.
3. **Python API** — `ThemeTokens.radius`, `.card_lift_distance`, etc. will no longer exist. Any code accessing these fields breaks.
   - Mitigation: `ThemePreset.radius` replaces `ThemeTokens.radius`. Animation fields have no replacement.
4. **shadcn import/export** — Radius handling moves to preset level but the JSON format stays the same.

## Risk Assessment

| Risk | Level | Notes |
|---|---|---|
| CSS output for `--radius` breaks | **Low** | Same var, different source. Output identical. |
| Animation CSS vars disappear | **Medium** | 4 vars removed. No internal consumers, but external users might reference them. |
| Python API breaks | **Medium** | `ThemeTokens.radius` access moves to `ThemePreset.radius`. |
| High-contrast presets break | **Low** | Straightforward: move radius to ThemePreset constructor. |
| shadcn import/export breaks | **Low** | Radius moves one level up; JSON format unchanged. |
| Tests break | **Low** | No tests directly reference these fields (confirmed by grep). |
| design_tokens.py radius extensions break | **None** | They use `var(--radius)` in CSS, which will still be set. |

## Recommended Implementation Order

1. Add `radius: float = 0.5` to `ThemePreset` dataclass
2. Update `css_generator.py` to read radius from preset, not tokens
3. Update all preset definitions to move radius from ThemeTokens to ThemePreset
4. Update `high_contrast.py` to set radius on ThemePreset
5. Update `shadcn.py` import/export
6. Remove radius + animation fields from `ThemeTokens`
7. Remove animation CSS var lines from `css_generator.py`
8. Add deprecated animation vars to `design_tokens.py` with defaults (optional, for backward compat)
9. Update `types.d.ts`
10. Run full test suite
