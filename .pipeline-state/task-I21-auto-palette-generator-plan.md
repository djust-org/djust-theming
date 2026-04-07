# I21: Brand Color Auto-Palette Generator - Implementation Plan

## Overview

`PaletteGenerator` derives a complete `ThemePreset` (light + dark modes, 31 color fields each) from 1-3 brand colors. Uses HSL color math from `colors.py` and WCAG validation from `accessibility.py`.

## ThemeTokens: All 31 ColorScale Fields

### Core surfaces (6)
1. `background` - Page background
2. `foreground` - Default text on background
3. `card` - Card surface
4. `card_foreground` - Text on card
5. `popover` - Popover surface
6. `popover_foreground` - Text on popover

### Brand colors (6)
7. `primary` - Primary action/brand color
8. `primary_foreground` - Text on primary
9. `secondary` - Secondary action
10. `secondary_foreground` - Text on secondary
11. `accent` - Highlight/accent
12. `accent_foreground` - Text on accent

### Muted (2)
13. `muted` - Muted backgrounds
14. `muted_foreground` - Text on muted

### Semantic states (8)
15. `destructive` - Error/destructive
16. `destructive_foreground` - Text on destructive
17. `success` - Success state
18. `success_foreground` - Text on success
19. `warning` - Warning state
20. `warning_foreground` - Text on warning
21. `info` - Info state
22. `info_foreground` - Text on info

### Extensions (6)
23. `link` - Link color
24. `link_hover` - Link hover color
25. `code` - Code block background
26. `code_foreground` - Code block text
27. `selection` - Text selection background
28. `selection_foreground` - Text on selection

### UI chrome (3)
29. `border` - Border color
30. `input` - Input border color
31. `ring` - Focus ring color

## ThemePreset Structure

```python
ThemePreset(
    name: str,
    display_name: str,
    light: ThemeTokens,    # 31 ColorScale fields
    dark: ThemeTokens,     # 31 ColorScale fields
    description: str = "",
    radius: float = 0.5,   # rem
)
```

## Available Utilities

### colors.py
- `hex_to_hsl(hex_str) -> (h, s, l)` — h:0-360, s:0-100, l:0-100
- `hsl_to_hex(h, s, l) -> str` — "#rrggbb"
- `hex_to_rgb(hex_str) -> (r, g, b)`
- `rgb_to_hex(r, g, b) -> str`
- `hsl_to_rgb(h, s, l) -> (r, g, b)`
- `rgb_to_hsl(r, g, b) -> (h, s, l)`

### presets.py — ColorScale
- `ColorScale(h, s, lightness)` — dataclass
- `ColorScale.from_hex(hex_str)` — factory
- `ColorScale.with_lightness(new_l)` — returns new instance
- `ColorScale.with_saturation(new_s)` — returns new instance

### accessibility.py — AccessibilityValidator
- `calculate_contrast_ratio(color1: ColorScale, color2: ColorScale) -> float`
- `evaluate_contrast(ratio, is_large_text) -> ContrastResult`
- Uses WCAG luminance formula with gamma correction

## API Design

### File: `djust_theming/palette.py` (new)

```python
class PaletteGenerator:
    """Derives complete ThemePreset from 1-3 brand colors."""

    MODES = ("professional", "playful", "muted", "vibrant")

    @classmethod
    def from_brand_colors(
        cls,
        primary: str,             # hex color, required
        secondary: str = None,    # hex color, optional
        accent: str = None,       # hex color, optional
        mode: str = "professional",
    ) -> ThemePreset:
        """Generate a complete ThemePreset from brand colors.

        Args:
            primary: Primary brand color as hex (#RRGGBB or #RGB).
            secondary: Secondary color. If None, derived as complementary (180 deg).
            accent: Accent color. If None, derived as analogous (30 deg offset).
            mode: Generation style — professional, playful, muted, vibrant.

        Returns:
            Complete ThemePreset with light and dark modes.

        Raises:
            ValueError: If mode is invalid or colors are not valid hex.
        """
```

## Color Derivation Algorithm

### Mode Parameters

| Parameter          | professional | playful | muted | vibrant |
|--------------------|-------------|---------|-------|---------|
| sat_scale          | 0.85        | 1.15    | 0.55  | 1.30    |
| lightness_range    | narrow      | wide    | narrow| wide    |
| secondary_hue_offset | 180       | 150     | 180   | 120     |
| accent_hue_offset  | 30          | 60      | 20    | 45      |
| bg_saturation      | 0-2%        | 2-5%    | 2-4%  | 0-3%    |
| radius             | 0.5         | 0.75    | 0.375 | 0.5     |

### Step-by-step Derivation

#### 1. Parse inputs
- `primary_hsl = hex_to_hsl(primary)` -> (h, s, l)
- If no secondary: rotate hue by mode's `secondary_hue_offset`
- If no accent: rotate hue by mode's `accent_hue_offset`
- Apply mode's `sat_scale` to derived (not user-provided) colors

#### 2. Light mode surfaces
- `background`: ColorScale(0, 0, 100) — pure white (or near-white with slight primary hue tint)
- `foreground`: ColorScale(primary_h, 10, 4) — near-black with slight brand warmth
- `card`: ColorScale(0, 0, 100) — same as background
- `card_foreground`: same as foreground
- `popover`: same as card
- `popover_foreground`: same as foreground

#### 3. Light mode brand colors
- `primary`: ColorScale(primary_h, primary_s * sat_scale, clamp(primary_l, 35, 55))
  - Ensure lightness in usable range for text-on-primary contrast
- `primary_foreground`: white (0, 0, 98) or black (0, 0, 4), whichever gives >= 4.5:1
- `secondary`: ColorScale(secondary_h, low_sat(15-25), 96) — subtle tinted background
- `secondary_foreground`: ColorScale(secondary_h, secondary_s, 10) — dark text
- `accent`: ColorScale(accent_h, low_sat(15-25), 96)
- `accent_foreground`: ColorScale(accent_h, accent_s, 10)

#### 4. Light mode muted
- `muted`: ColorScale(primary_h, 5-8, 96) — very desaturated primary
- `muted_foreground`: ColorScale(primary_h, 5-8, 40) — readable gray

#### 5. Light mode semantic states
- `destructive`: ColorScale(0, 84, 60) — red (fixed hue, adjust sat by mode)
- `destructive_foreground`: white
- `success`: ColorScale(142, 76, 36) — green
- `success_foreground`: white
- `warning`: ColorScale(38, 92, 50) — amber
- `warning_foreground`: white (or dark if contrast fails)
- `info`: ColorScale(199, 89, 48) — blue
- `info_foreground`: white

#### 6. Light mode extensions
- `link`: ColorScale(primary_h, primary_s, 53) — brand-colored link
- `link_hover`: ColorScale(primary_h, primary_s, 45) — darker on hover
- `code`: ColorScale(primary_h, 5, 94) — subtle background
- `code_foreground`: ColorScale(primary_h, 10, 20)
- `selection`: ColorScale(primary_h, 100, 80) — light brand highlight
- `selection_foreground`: foreground

#### 7. Light mode UI chrome
- `border`: ColorScale(primary_h, 6, 90)
- `input`: ColorScale(primary_h, 6, 90) — same as border
- `ring`: primary color (used for focus)

#### 8. Dark mode — invert lightness scale
- Key principle: swap light/dark, keep hue and saturation similar
- `background`: ColorScale(primary_h, 10, 4)
- `foreground`: ColorScale(0, 0, 98)
- `card`: same as dark background (or slight offset)
- `primary`: ColorScale(primary_h, primary_s * 0.9, clamp(85 - primary_l_light, 50, 75))
  - Lighter in dark mode
- `primary_foreground`: near-black or near-white based on contrast
- `secondary`: ColorScale(secondary_h, 10-15, 15)
- `secondary_foreground`: ColorScale(secondary_h, 5, 90)
- `muted`: ColorScale(primary_h, 8, 15)
- `muted_foreground`: ColorScale(primary_h, 5, 65)
- Semantic colors: slightly desaturate, adjust lightness for dark bg contrast
- `border`: ColorScale(primary_h, 6, 18)
- `input`: ColorScale(primary_h, 6, 18)
- `ring`: primary (dark mode version)

#### 9. WCAG AA Contrast Validation (4.5:1 minimum)
For every fg/bg pair, after generation:
1. Calculate contrast ratio using `AccessibilityValidator.calculate_contrast_ratio()`
2. If ratio < 4.5:
   - For foreground-on-background: adjust foreground lightness (darken on light bg, lighten on dark bg)
   - Binary search lightness in range [0, 100] until ratio >= 4.5:1
3. Pairs to validate:
   - foreground / background
   - card_foreground / card
   - popover_foreground / popover
   - primary_foreground / primary
   - secondary_foreground / secondary
   - muted_foreground / muted
   - accent_foreground / accent
   - destructive_foreground / destructive
   - success_foreground / success
   - warning_foreground / warning
   - info_foreground / info
   - code_foreground / code
   - selection_foreground / selection
   - link / background (links must be readable)
   - border / background (minimum 3:1 for UI components)

### Contrast Auto-Fix Algorithm
```
def ensure_contrast(fg: ColorScale, bg: ColorScale, min_ratio=4.5) -> ColorScale:
    """Adjust fg lightness to meet minimum contrast against bg."""
    validator = AccessibilityValidator()
    ratio = validator.calculate_contrast_ratio(fg, bg)
    if ratio >= min_ratio:
        return fg

    # Determine direction: if bg is light, darken fg; if dark, lighten fg
    bg_lightness = bg.lightness
    direction = -1 if bg_lightness > 50 else 1

    # Binary search for optimal lightness
    low, high = (0, fg.lightness) if direction == -1 else (fg.lightness, 100)
    best = fg
    for _ in range(20):  # 20 iterations = precision < 0.01%
        mid = (low + high) // 2
        candidate = ColorScale(fg.h, fg.s, mid)
        r = validator.calculate_contrast_ratio(candidate, bg)
        if r >= min_ratio:
            best = candidate
            if direction == -1:
                low = mid + 1  # try less extreme
            else:
                high = mid - 1
        else:
            if direction == -1:
                high = mid - 1  # go more extreme
            else:
                low = mid + 1
    return best
```

## File Changes

### New files
1. `djust_theming/palette.py` — `PaletteGenerator` class + `ensure_contrast` helper
2. `tests/test_palette.py` — comprehensive test suite

### Modified files
3. `djust_theming/__init__.py` — export `PaletteGenerator`

## Test Strategy

### `tests/test_palette.py`

#### Basic generation tests
- `test_from_single_brand_color` — provide only primary, get valid ThemePreset
- `test_from_two_brand_colors` — primary + secondary
- `test_from_three_brand_colors` — primary + secondary + accent
- `test_all_modes` — professional, playful, muted, vibrant each produce valid output
- `test_invalid_mode_raises` — ValueError for unknown mode
- `test_invalid_hex_raises` — ValueError for bad color input

#### Output validation tests
- `test_output_is_theme_preset` — isinstance check
- `test_has_light_and_dark` — both modes present
- `test_all_31_fields_present` — every ThemeTokens field is a ColorScale
- `test_preset_name_generated` — name/display_name are non-empty strings
- `test_radius_varies_by_mode` — different modes produce different radii

#### Color derivation tests
- `test_primary_hue_preserved` — output primary hue matches input (within rounding)
- `test_secondary_derived_complementary` — when not provided, ~180 deg from primary
- `test_accent_derived_analogous` — when not provided, ~30 deg from primary
- `test_user_provided_secondary_used` — if secondary provided, its hue is used
- `test_user_provided_accent_used` — if accent provided, its hue is used

#### WCAG contrast validation tests
- `test_all_fg_bg_pairs_pass_aa` — every foreground/background pair >= 4.5:1
- `test_all_fg_bg_pairs_pass_aa_dark_mode` — same for dark mode
- `test_border_contrast_minimum` — border/background >= 3:1
- `test_contrast_autofix_works` — deliberately bad input still produces passing output
- `test_known_brand_colors` — test with known brands:
  - Spotify green (#1DB954) -> valid palette
  - Coca-Cola red (#F40009) -> valid palette
  - Facebook blue (#1877F2) -> valid palette

#### Mode differentiation tests
- `test_muted_mode_lower_saturation` — muted primary has lower saturation
- `test_vibrant_mode_higher_saturation` — vibrant primary has higher saturation
- `test_playful_wider_hue_range` — playful accent further from primary

#### Round-trip / integration tests
- `test_preset_works_with_css_generator` — generated preset can be fed to ThemeCSSGenerator
- `test_preset_works_with_accessibility_validator` — generated preset passes validation

## Implementation Order

1. Create `djust_theming/palette.py` with `PaletteGenerator` class
2. Implement `_mode_params()` returning per-mode configuration dict
3. Implement `_derive_light_tokens()` — light mode ThemeTokens
4. Implement `_derive_dark_tokens()` — dark mode ThemeTokens
5. Implement `_ensure_contrast()` — WCAG auto-fix
6. Implement `from_brand_colors()` — main public API
7. Update `__init__.py` exports
8. Write `tests/test_palette.py`
9. Run full test suite, fix any failures
