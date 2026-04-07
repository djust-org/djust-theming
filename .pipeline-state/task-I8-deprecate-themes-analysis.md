# I8: Deprecate themes.py - Analysis

## Status
- **ENV_OK** - Branch `task/I8-deprecate-themes` created from main, venv installed, 19 tests pass.
- **MERGE_CLEAN** - No conflict markers found.

---

## Current State

### themes.py (OLD system)
- **Location**: `djust_theming/themes.py`
- **Already marked deprecated** (line 2): `DEPRECATED: This module is deprecated in favor of theme_packs.py`
- Contains 7 dataclasses: `Typography`, `Spacing`, `BorderRadius`, `Shadows`, `Animations`, `ComponentStyles`, `Theme`
- Contains 11 predefined Theme instances: material, ios, fluent, minimalist, playful, corporate, retro, elegant, neo_brutalist, organic, dense
- Exposes **`THEMES: Dict[str, Theme]`** registry (line 690) with all 11 themes
- Exposes `get_theme(name)` and `list_themes()` helper functions

### theme_packs.py (NEW system)
- **Location**: `djust_theming/theme_packs.py`
- Contains new dataclasses: `TypographyStyle`, `LayoutStyle`, `SurfaceStyle`, `IconStyle`, `AnimationStyle`, `InteractionStyle`, `DesignSystem`
- Contains **`DESIGN_SYSTEMS: Dict[str, DesignSystem]`** registry (line 1140) with the same 11 keys: material, ios, fluent, playful, corporate, dense, minimalist, neo_brutalist, elegant, retro, organic
- Also contains `ThemePack` (bundles a `design_theme` string + `color_preset` string + style dimensions)
- `THEME_PACKS` registry with 11 packs
- `get_design_system()`, `get_all_design_systems()`, `get_theme_pack()`, `get_all_theme_packs()`

### design_tokens.py
- **Location**: `djust_theming/design_tokens.py`
- Provides CSS custom property generation functions (spacing, typography, radius, transitions, shadows, etc.)
- Theme-agnostic -- generates static CSS token values (not parameterized by design system)
- **No registry or dict of design systems** -- purely a CSS generation utility
- Not directly relevant to the THEMES deprecation; it complements both systems

---

## All imports/references to themes.py

| File | Import/Usage | Lines |
|------|-------------|-------|
| **`djust_theming/manager.py`** | `from .themes import THEMES` (inside `get_state()` and `set_theme()`) | 121, 158, 190, 192 |
| **`djust_theming/theme_css_generator.py`** | `from .themes import Theme, get_theme` | 15 |
| **`example_project/theme_demo/views.py`** | `from djust_theming.themes import THEMES` | 6, 56 |
| **`djust_theming/__init__.py`** | Does NOT import from themes.py | -- |
| **tests/** | No direct themes.py imports | -- |

### How manager.py uses THEMES

1. **`get_state()` (line 121, 158)**: Imports `THEMES` at function level. After resolving theme name from cookies/session/config, validates with `if theme not in THEMES:` and falls back to `"material"`. This is the primary validation gate.

2. **`set_theme()` (line 190, 192)**: Imports `THEMES` at function level. Validates `if theme_name not in THEMES:` before persisting to session.

Both uses are purely **key-existence checks** against the `THEMES` dict -- they only need the set of valid theme names, not the Theme objects themselves.

### How theme_css_generator.py uses themes.py

- Imports `Theme` (type) and `get_theme()` (lookup function)
- `CompleteThemeCSSGenerator.__init__()` calls `get_theme(theme_name)` to get a `Theme` object
- Uses the full `Theme` object to generate CSS custom properties (typography, spacing, radius, shadows, animations, component styles)
- This is the only consumer that actually reads Theme object data

---

## Key Observation: DESIGN_SYSTEMS mirrors THEMES

The `DESIGN_SYSTEMS` dict in `theme_packs.py` has **exactly the same 11 keys** as `THEMES` in `themes.py`:

```
THEMES keys:        material, ios, fluent, minimalist, playful, corporate, retro, elegant, neo_brutalist, organic, dense
DESIGN_SYSTEMS keys: material, ios, fluent, minimalist, playful, corporate, retro, elegant, neo_brutalist, organic, dense
```

This confirms `DESIGN_SYSTEMS` is the intended replacement registry.

---

## Proposed Plan

### 1. Update manager.py to validate against DESIGN_SYSTEMS directly

**manager.py `get_state()`** (line 121):
- Change `from .themes import THEMES` to `from .theme_packs import DESIGN_SYSTEMS`
- Change `if theme not in THEMES:` to `if theme not in DESIGN_SYSTEMS:`

**manager.py `set_theme()`** (line 190):
- Same change: validate against `DESIGN_SYSTEMS` instead of `THEMES`

### 2. Make themes.py a deprecation shim

Replace the entire themes.py module body with:
- Import `DESIGN_SYSTEMS` from `theme_packs`
- Create `THEMES` as a proxy/alias that emits `DeprecationWarning` on access
- Keep `get_theme()` and `list_themes()` as shims that warn and delegate
- Keep the `Theme`, `Typography`, etc. dataclasses available for type compatibility (theme_css_generator.py uses `Theme`)

**Approach**: Use a lazy dict wrapper class that emits `DeprecationWarning` on any access:

```python
import warnings
from .theme_packs import DESIGN_SYSTEMS

class _DeprecatedThemesDict(dict):
    """Wrapper that emits deprecation warnings when accessed."""
    def __getitem__(self, key):
        warnings.warn(
            "THEMES is deprecated. Use DESIGN_SYSTEMS from djust_theming.theme_packs instead.",
            DeprecationWarning, stacklevel=2
        )
        return super().__getitem__(key)
    # ... similar for __contains__, get, etc.
```

**Problem**: The `Theme` objects in `THEMES` and `DesignSystem` objects in `DESIGN_SYSTEMS` are **different types** with different attributes. `THEMES["material"]` returns a `Theme` (with typography, spacing, border_radius, shadows, animations, component_styles), while `DESIGN_SYSTEMS["material"]` returns a `DesignSystem` (with typography, layout, surface, icons, animation, interaction -- all different sub-types).

### 3. Handle theme_css_generator.py

`theme_css_generator.py` is the only file that uses `Theme` objects' **actual data** (not just key existence). It reads:
- `theme.typography.*` (font_sans, font_mono, text sizes, weights, line heights)
- `theme.spacing.*` (base, space multipliers)
- `theme.border_radius.*` (radius values)
- `theme.shadows.*` (shadow definitions)
- `theme.animations.*` (durations, easing curves)
- `theme.component_styles.*` (button_style, card_style, input_style)

Options:
- **Option A**: Keep themes.py `Theme` objects intact for theme_css_generator.py, but mark them as deprecated. The shim would still contain the real Theme data for backward compat.
- **Option B**: Create a new `design_system_css.py` generator that works with `DesignSystem` objects, and deprecate `theme_css_generator.py` along with themes.py.

**Recommended: Option A** (smaller scope, cleaner deprecation path):
- Keep the Theme dataclasses and instances in themes.py
- Add `DeprecationWarning` to `THEMES` dict access, `get_theme()`, and `list_themes()`
- Update manager.py to use `DESIGN_SYSTEMS` directly (since it only checks key existence)
- theme_css_generator.py continues to work unchanged (it will trigger deprecation warnings, which is correct -- it should be migrated later)

### 4. Update example_project

- `example_project/theme_demo/views.py` imports `THEMES` -- update to use `DESIGN_SYSTEMS` or leave as-is (will get deprecation warning)

---

## Files to modify

| File | Change |
|------|--------|
| `djust_theming/themes.py` | Wrap `THEMES` dict, `get_theme()`, `list_themes()` with `DeprecationWarning` |
| `djust_theming/manager.py` | Replace `from .themes import THEMES` with `from .theme_packs import DESIGN_SYSTEMS`; validate against `DESIGN_SYSTEMS` |
| `example_project/theme_demo/views.py` | Update import from `themes.THEMES` to `theme_packs.DESIGN_SYSTEMS` |
| `tests/` | Add tests for deprecation warnings on themes.py access |

### Files that need NO changes (yet)
| File | Reason |
|------|--------|
| `djust_theming/theme_css_generator.py` | Uses Theme objects for CSS generation; will trigger deprecation warning (correct behavior, migration is separate task) |
| `djust_theming/__init__.py` | Does not import from themes.py |
| `djust_theming/design_tokens.py` | Independent CSS utility, no themes.py dependency |

---

## Risk Assessment

- **Low risk**: manager.py change is a 1:1 key-set swap (same 11 keys in both dicts)
- **Low risk**: DeprecationWarning in themes.py is additive, no breaking change
- **Medium risk**: Any downstream consumers (outside this repo) importing `THEMES` will get warnings but will still work
- **Test coverage**: 19 existing tests pass; need new tests for warning emission
