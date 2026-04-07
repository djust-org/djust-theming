# Plan: I16 — Color Format Interoperability

## Current State

### ColorScale (presets.py, line 11-33)
- Dataclass with fields: `h: int`, `s: int`, `lightness: int`
- Instance methods: `to_hsl()` -> `"H S% L%"`, `to_hsl_func()` -> `"hsl(H, S%, L%)"`
- Factory methods: `with_lightness()`, `with_saturation()` return new ColorScale

### Existing color math (scattered)
- `accessibility.py` line 52-57: `AccessibilityValidator.hsl_to_rgb()` — uses `colorsys.hls_to_rgb`, instance method on validator class, takes ColorScale, returns `(float, float, float)` in 0-1 range
- `accessibility.py` line 59-71: `rgb_to_luminance()` — WCAG gamma-corrected luminance, also on validator
- `shadcn.py` line 79-95: `parse_hsl()` — local function inside `_parse_shadcn_vars`, parses `"H S% L%"` strings to ColorScale
- `high_contrast.py`: Uses ColorScale constructor directly with HSL ints, no color math

### No existing hex/RGB support anywhere in the codebase.

## Design

### 1. New module: `djust_theming/colors.py`

Consolidate all color math into a single module. Pure functions, no class dependencies.

```python
"""
Color conversion utilities for djust-theming.

Consolidates HSL, RGB, and hex color math in one place.
All functions are pure — no side effects or class dependencies.
"""
import colorsys
from typing import Tuple

def hsl_to_rgb(h: int, s: int, l: int) -> Tuple[int, int, int]:
    """Convert HSL (h: 0-360, s: 0-100, l: 0-100) to RGB (0-255 each)."""
    # Normalize to colorsys ranges: h 0-1, l 0-1, s 0-1
    # colorsys uses HLS order (not HSL)
    r, g, b = colorsys.hls_to_rgb(h / 360.0, l / 100.0, s / 100.0)
    return (round(r * 255), round(g * 255), round(b * 255))

def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """Convert RGB (0-255 each) to HSL (h: 0-360, s: 0-100, l: 0-100)."""
    h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    return (round(h * 360), round(s * 100), round(l * 100))

def hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
    """Convert hex string (#RRGGBB or RRGGBB, 3 or 6 digit) to RGB (0-255)."""
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 3:
        hex_str = ''.join(c * 2 for c in hex_str)
    if len(hex_str) != 6:
        raise ValueError(f"Invalid hex color: #{hex_str}")
    return (int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))

def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB (0-255 each) to hex string (#rrggbb, lowercase)."""
    return f"#{r:02x}{g:02x}{b:02x}"

def hex_to_hsl(hex_str: str) -> Tuple[int, int, int]:
    """Convert hex string to HSL tuple."""
    return rgb_to_hsl(*hex_to_rgb(hex_str))

def hsl_to_hex(h: int, s: int, l: int) -> str:
    """Convert HSL to hex string."""
    return rgb_to_hex(*hsl_to_rgb(h, s, l))
```

### 2. New instance methods on ColorScale (presets.py)

Add three instance methods and two class methods:

```python
# Instance methods — output formats
def to_hex(self) -> str:
    """Return hex color string, e.g. '#3b82f6'."""
    from .colors import hsl_to_hex
    return hsl_to_hex(self.h, self.s, self.lightness)

def to_rgb(self) -> Tuple[int, int, int]:
    """Return RGB tuple (0-255 each)."""
    from .colors import hsl_to_rgb
    return hsl_to_rgb(self.h, self.s, self.lightness)

def to_rgb_func(self) -> str:
    """Return complete rgb() CSS function string, e.g. 'rgb(59, 130, 246)'."""
    r, g, b = self.to_rgb()
    return f"rgb({r}, {g}, {b})"

# Class methods — constructors from other formats
@classmethod
def from_hex(cls, hex_str: str) -> "ColorScale":
    """Create ColorScale from hex string (#RRGGBB or #RGB)."""
    from .colors import hex_to_hsl
    h, s, l = hex_to_hsl(hex_str)
    return cls(h, s, l)

@classmethod
def from_rgb(cls, r: int, g: int, b: int) -> "ColorScale":
    """Create ColorScale from RGB values (0-255 each)."""
    from .colors import rgb_to_hsl
    h, s, l = rgb_to_hsl(r, g, b)
    return cls(h, s, l)
```

Import uses lazy `from .colors import ...` inside methods to avoid circular imports (colors.py is pure functions, so no risk, but keeps presets.py import-clean).

### 3. Refactor accessibility.py

Replace `AccessibilityValidator.hsl_to_rgb()` to delegate to `colors.hsl_to_rgb`:

```python
def hsl_to_rgb(self, color_scale: ColorScale) -> Tuple[float, float, float]:
    """Convert HSL ColorScale to RGB (0-1 range)."""
    from .colors import hsl_to_rgb
    r, g, b = hsl_to_rgb(color_scale.h, color_scale.s, color_scale.lightness)
    return (r / 255.0, g / 255.0, b / 255.0)
```

This preserves the existing 0-1 range return type so `rgb_to_luminance` needs no changes. The method signature stays the same for backward compatibility.

### 4. Exports from `__init__.py`

Add color utility exports:

```python
from .colors import hsl_to_rgb, rgb_to_hsl, hex_to_rgb, rgb_to_hex, hex_to_hsl, hsl_to_hex
```

Add to `__all__`:
```python
# Color utilities
"hsl_to_rgb",
"rgb_to_hsl",
"hex_to_rgb",
"rgb_to_hex",
"hex_to_hsl",
"hsl_to_hex",
```

ColorScale is already exported; its new methods are automatically available.

## Files Changed

| File | Change |
|------|--------|
| `djust_theming/colors.py` | **NEW** — Pure color conversion functions |
| `djust_theming/presets.py` | Add `to_hex`, `to_rgb`, `to_rgb_func`, `from_hex`, `from_rgb` to ColorScale |
| `djust_theming/accessibility.py` | Refactor `hsl_to_rgb` to delegate to `colors` module |
| `djust_theming/__init__.py` | Export color utility functions |
| `tests/test_colors.py` | **NEW** — Color conversion and round-trip tests |

## Test Strategy

New file: `tests/test_colors.py`

### Unit tests for `colors.py` functions

1. **Known color values** (exact expected outputs):
   - `hsl_to_rgb(0, 100, 50)` == `(255, 0, 0)` (pure red)
   - `hsl_to_rgb(120, 100, 50)` == `(0, 255, 0)` (pure green)
   - `hsl_to_rgb(240, 100, 50)` == `(0, 0, 255)` (pure blue)
   - `hsl_to_rgb(0, 0, 0)` == `(0, 0, 0)` (black)
   - `hsl_to_rgb(0, 0, 100)` == `(255, 255, 255)` (white)
   - `hsl_to_rgb(0, 0, 50)` == `(128, 128, 128)` (gray, approximately)
   - `hex_to_rgb("#ff0000")` == `(255, 0, 0)`
   - `rgb_to_hex(255, 0, 0)` == `"#ff0000"`
   - `hex_to_rgb("#fff")` == `(255, 255, 255)` (3-digit shorthand)

2. **Round-trip tests** (lossless or near-lossless):
   - `hex -> RGB -> hex`: `rgb_to_hex(*hex_to_rgb("#3b82f6"))` == `"#3b82f6"` (exact)
   - `RGB -> hex -> RGB`: `hex_to_rgb(rgb_to_hex(59, 130, 246))` == `(59, 130, 246)` (exact)
   - `hex -> HSL -> hex`: May have rounding; test with tolerance of +/-1 per channel
   - `HSL -> RGB -> HSL`: May have rounding; test known round-trip-safe values

3. **Edge cases**:
   - `hex_to_rgb("")` raises ValueError
   - `hex_to_rgb("#GGG")` raises ValueError
   - `hex_to_rgb("#12345")` raises ValueError (5-digit)
   - RGB boundary values: `(0, 0, 0)`, `(255, 255, 255)`
   - HSL boundary values: hue=0 vs hue=360 (should both map to red-ish)

### Unit tests for ColorScale methods

4. **Instance method tests**:
   - `ColorScale(0, 100, 50).to_hex()` == `"#ff0000"`
   - `ColorScale(0, 100, 50).to_rgb()` == `(255, 0, 0)`
   - `ColorScale(0, 100, 50).to_rgb_func()` == `"rgb(255, 0, 0)"`
   - Existing methods still work: `to_hsl()`, `to_hsl_func()`

5. **Class method tests**:
   - `ColorScale.from_hex("#ff0000")` == `ColorScale(0, 100, 50)`
   - `ColorScale.from_rgb(255, 0, 0)` == `ColorScale(0, 100, 50)`
   - `ColorScale.from_hex("#000000")` == `ColorScale(0, 0, 0)`
   - `ColorScale.from_hex("#ffffff")` == `ColorScale(0, 0, 100)`

6. **Round-trip on ColorScale**:
   - `ColorScale.from_hex(ColorScale(221, 83, 53).to_hex())` — h, s, l should be close to original (within +/-1)

### Integration: accessibility.py still works

7. **Regression test**: Run existing accessibility validation to confirm refactored `hsl_to_rgb` produces identical contrast ratios. Compare a known preset's contrast result before/after.

## Risks and Mitigations

- **Integer rounding**: HSL uses ints in ColorScale. Converting hex->HSL->hex may not be perfectly lossless because colorsys works in floats. Mitigation: document that ColorScale rounds to nearest int, and test round-trips with tolerance.
- **colorsys uses HLS order** (not HSL): Already handled correctly in accessibility.py. The new `colors.py` must maintain the same `hls_to_rgb(h, l, s)` argument order.
- **No breaking changes**: All new methods are additive. The accessibility refactor preserves the method signature and return type.
