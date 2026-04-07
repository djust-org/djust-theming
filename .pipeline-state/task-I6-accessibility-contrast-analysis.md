# Task I6: Accessibility Contrast Validation at Preset Level -- Analysis

## Objective

Add a Django system check that validates all registered presets in `THEME_PRESETS` meet WCAG AA contrast ratios at startup. Report warnings (not errors) so projects are informed but not blocked.

## Existing Code Review

### accessibility.py (already exists)

`/djust_theming/accessibility.py` contains a full `AccessibilityValidator` class with:

- `hsl_to_rgb()` -- converts `ColorScale` HSL to RGB
- `rgb_to_luminance()` -- WCAG relative luminance formula
- `calculate_contrast_ratio()` -- WCAG contrast ratio between two `ColorScale` objects
- `evaluate_contrast()` -- classifies ratio as AA/AAA/FAIL
- `validate_theme_accessibility()` -- validates a single preset across light+dark modes
- `validate_all_combinations()` -- iterates all design system x preset combos
- `ContrastResult` / `AccessibilityReport` dataclasses

**Critical bug found:** Line 56 references `color_scale.l` but the `ColorScale` dataclass field is named `lightness` (not `l`). This means `hsl_to_rgb()` will raise `AttributeError` at runtime. This must be fixed before or alongside this task.

The critical foreground/background pairs already defined (lines 137-148):
- foreground / background
- card_foreground / card
- primary_foreground / primary
- secondary_foreground / secondary
- muted_foreground / muted
- destructive_foreground / destructive
- success_foreground / success
- warning_foreground / warning
- border / background (non-text, uses AA_LARGE threshold potentially)
- input / background

Missing pairs worth adding:
- popover_foreground / popover
- accent_foreground / accent
- info_foreground / info
- code_foreground / code
- selection_foreground / selection

### presets.py

- `ColorScale` dataclass: fields `h`, `s`, `lightness` (int values, HSL)
- `ThemeTokens` dataclass: complete token set with all foreground/background pairs
- `ThemePreset` dataclass: `name`, `display_name`, `light: ThemeTokens`, `dark: ThemeTokens`
- `THEME_PRESETS`: dict of 19 registered presets (default, shadcn, blue, green, purple, orange, rose, natural20, catppuccin, rose_pine, tokyo_night, nord, synthwave, cyberpunk, outrun, forest, amber, slate, nebula)
- `get_preset(name)` returns preset with fallback to default

### apps.py

Minimal `DjustThemingConfig` -- no `ready()` method, no check registration currently.

### checks.py

Does not exist yet. Needs to be created.

## Proposed Implementation

### New file: `djust_theming/checks.py`

```python
"""Django system checks for djust-theming accessibility validation."""

from django.core.checks import Warning, register, Tags

from .presets import THEME_PRESETS, ColorScale
from .accessibility import AccessibilityValidator


@register(Tags.compatibility)
def check_preset_contrast(app_configs, **kwargs):
    """Validate all registered theme presets meet WCAG AA contrast ratios."""
    warnings = []
    validator = AccessibilityValidator()

    # Foreground/background pairs to check (attr_fg, attr_bg, label)
    CONTRAST_PAIRS = [
        ("foreground", "background", "text on background"),
        ("card_foreground", "card", "text on card"),
        ("primary_foreground", "primary", "text on primary"),
        ("secondary_foreground", "secondary", "text on secondary"),
        ("muted_foreground", "muted", "text on muted"),
        ("accent_foreground", "accent", "text on accent"),
        ("destructive_foreground", "destructive", "text on destructive"),
        ("success_foreground", "success", "text on success"),
        ("warning_foreground", "warning", "text on warning"),
        ("info_foreground", "info", "text on info"),
        ("popover_foreground", "popover", "text on popover"),
        ("code_foreground", "code", "text on code"),
    ]

    for preset_name, preset in THEME_PRESETS.items():
        for mode_name in ("light", "dark"):
            tokens = getattr(preset, mode_name)
            for fg_attr, bg_attr, label in CONTRAST_PAIRS:
                fg = getattr(tokens, fg_attr)
                bg = getattr(tokens, bg_attr)
                ratio = validator.calculate_contrast_ratio(fg, bg)
                if ratio < validator.AA_NORMAL:
                    warnings.append(
                        Warning(
                            f'Preset "{preset_name}" {mode_name} mode: {label} '
                            f'contrast ratio {ratio:.2f}:1 < {validator.AA_NORMAL}:1 (WCAG AA)',
                            hint=f"Adjust {fg_attr} or {bg_attr} to achieve at least {validator.AA_NORMAL}:1 contrast.",
                            id="djust_theming.W001",
                        )
                    )

    return warnings
```

### Modify: `djust_theming/apps.py`

Add a `ready()` method that imports checks to trigger registration:

```python
class DjustThemingConfig(AppConfig):
    name = "djust_theming"
    verbose_name = "Djust Theming"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from . import checks  # noqa: F401 -- triggers @register
```

### Fix: `djust_theming/accessibility.py` line 56

Change `color_scale.l` to `color_scale.lightness`.

## Token Pairs to Validate

Primary (text readability -- WCAG AA 4.5:1 for normal text):
1. foreground / background
2. card_foreground / card
3. popover_foreground / popover
4. primary_foreground / primary
5. secondary_foreground / secondary
6. muted_foreground / muted
7. accent_foreground / accent
8. destructive_foreground / destructive
9. success_foreground / success
10. warning_foreground / warning
11. info_foreground / info
12. code_foreground / code

Excluded from text checks (non-text or decorative):
- border / background -- UI element, could use 3:1 threshold (AA large/non-text) but not critical for system check
- input / background -- same reasoning
- selection_foreground / selection -- transient state
- link / background -- important but link styling varies

## Risk Assessment

### HSL Format Parsing
- **Low risk.** `ColorScale` stores raw integer H/S/L values; no string parsing needed. The `hsl_to_rgb` conversion uses `colorsys.hls_to_rgb` (note: Python's colorsys uses HLS order, not HSL). The existing code handles this correctly.
- **Bug:** `color_scale.l` must become `color_scale.lightness` -- this is a blocking issue.

### Performance at Startup
- **Negligible.** 19 presets x 2 modes x 12 pairs = 456 contrast calculations. Each is pure arithmetic (HSL->RGB->luminance->ratio). Sub-millisecond total.
- No I/O, no database queries, no file reads.

### False Positives
- Some presets may intentionally have low-contrast decorative pairs (e.g., muted text). Using W-level warnings (not errors) means these are informational, not blocking.
- The `id="djust_theming.W001"` allows silencing via `SILENCED_SYSTEM_CHECKS`.

### Backward Compatibility
- Adding a system check is purely additive. Existing projects will see new warnings but no breakage.
- The `ready()` import pattern is standard Django.

## Testing Plan

New test file: `tests/test_checks.py`
1. Test that all built-in presets produce no warnings (or document expected ones)
2. Test that a deliberately bad preset triggers W001
3. Test that the check function runs without error when THEME_PRESETS is empty
4. Test the bug fix -- `hsl_to_rgb` works with `ColorScale.lightness`

## Files to Create/Modify

| File | Action | Description |
|------|--------|-------------|
| `djust_theming/checks.py` | CREATE | Django system check with `@register` |
| `djust_theming/apps.py` | MODIFY | Add `ready()` to import checks |
| `djust_theming/accessibility.py` | MODIFY | Fix `color_scale.l` -> `color_scale.lightness` (line 56) |
| `tests/test_checks.py` | CREATE | Tests for the system check |

## Open Questions

1. Should we also warn for pairs that pass AA but fail AAA? (Recommendation: no -- keep it focused on AA, add AAA as a separate optional check later)
2. Should link/background contrast be included? (Recommendation: not in v1 -- link color is context-dependent)
3. Should the check be gated behind a setting like `DJUST_THEMING_CHECK_CONTRAST = True`? (Recommendation: no -- always-on W-level warnings are the Django convention; users can silence with `SILENCED_SYSTEM_CHECKS`)
