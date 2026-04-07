# I5: CSS Generation Caching — Analysis

## 1. How CSS Generation Works Today

### Generator Hierarchy

There are **four** CSS generator classes, forming a layered hierarchy:

1. **`ThemeCSSGenerator`** (`css_generator.py`) — Base color CSS generator. Takes a `preset_name` and generates CSS custom properties for light/dark modes, base styles, and utility classes.

2. **`CompleteThemeCSSGenerator`** (`theme_css_generator.py`) — Wraps `ThemeCSSGenerator` and adds typography, spacing, border-radius, shadows, animations, and component styles from a `Theme` object. Constructor takes `(theme_name, color_preset)`.

3. **`ThemePackCSSGenerator`** (`pack_css_generator.py`) — Wraps `CompleteThemeCSSGenerator` and adds icon, animation, pattern, interaction, and illustration CSS from a `ThemePack`. Constructor takes `pack_name`.

4. **`DesignSystemCSSGenerator`** (`design_system_css.py`) — Separate path combining a `DesignSystem` with a color preset. Constructor takes `(design_system_name, color_preset_name)`.

### Current Cost per `generate_css()` Call

Each call to `CompleteThemeCSSGenerator.generate_css()`:
- Looks up the Theme from a module-level dict (`THEMES`)
- Looks up the color preset from a module-level dict (`THEME_PRESETS`)
- Builds a large CSS string via string concatenation/join across ~6 helper methods
- No caching — every call reconstructs the entire string from scratch

The output is **deterministic**: same `(theme_name, color_preset)` always produces identical CSS. The underlying data sources are module-level dicts of frozen dataclass-like objects that never change at runtime.

### Call Sites (where `generate_css()` is invoked)

| Call Site | File | Generator Used | Frequency |
|-----------|------|---------------|-----------|
| `theme_css_view` | `views.py:46` | CompleteThemeCSSGenerator or ThemePackCSSGenerator | Every CSS HTTP request (mitigated by HTTP ETag/Cache-Control) |
| `theme_context` | `context_processors.py:32-39` | CompleteThemeCSSGenerator or ThemePackCSSGenerator | **Every page render** via context processor |
| `{% theme_head %}` | `theme_tags.py:82-89` | CompleteThemeCSSGenerator or ThemePackCSSGenerator | **Every page render** via template tag |
| `{% theme_css %}` | `theme_tags.py:120-126` | CompleteThemeCSSGenerator or ThemePackCSSGenerator | Every use of the tag |
| `ThemeMixin._setup_theme_context` | `mixins.py:97` | CompleteThemeCSSGenerator | Every LiveView mount + every theme switch event |
| `DesignSystemCSSGenerator.generate_css` | `design_system_css.py:306` | DesignSystemCSSGenerator (separate path) | On demand |

**Key observation**: The context processor and `{% theme_head %}` tag are the hot paths. In a typical app using the context processor, `generate_css()` runs on **every single page load**, rebuilding hundreds of lines of CSS string each time.

## 2. Cache Key Analysis

### CompleteThemeCSSGenerator

The output is fully determined by:
- `theme_name` (str) — selects the Theme object (typography, spacing, shadows, etc.)
- `color_preset` (str) — selects the color preset (light/dark HSL values)

**Proposed cache key**: `(theme_name, color_preset)`

The Theme and ThemePreset objects are looked up from module-level dicts (`THEMES`, `THEME_PRESETS`) that are populated at import time and never mutated. This makes the mapping from `(theme_name, color_preset)` to CSS output stable for the lifetime of the process.

### ThemePackCSSGenerator

The output is fully determined by:
- `pack_name` (str) — selects the ThemePack which includes `design_theme` and `color_preset` plus icon/animation/pattern/interaction/illustration styles

**Proposed cache key**: `pack_name`

### ThemeCSSGenerator (base color generator)

The output is determined by:
- `preset_name` (str)
- `custom_tokens` (dict or None)
- `include_base_styles` (bool)
- `include_utilities` (bool)
- `include_design_tokens` (bool)

For the CompleteThemeCSSGenerator usage, this is always called with just `preset_name` (defaults for the rest), so caching at the CompleteThemeCSSGenerator level subsumes this.

### DesignSystemCSSGenerator

The output is determined by:
- `design_system_name` (str)
- `color_preset_name` (str)
- `include_base_styles` (bool)
- `include_utilities` (bool)
- `css_prefix` (str)

**Proposed cache key**: `(design_system_name, color_preset_name, include_base_styles, include_utilities, css_prefix)`

## 3. Proposed Caching Approach

### Recommendation: Module-level `dict` cache (NOT `lru_cache`, NOT Django cache)

**Why not `functools.lru_cache`?**
- `lru_cache` works on functions, not methods. Using it on `generate_css()` would require making it a standalone function or using `__hash__`/`__eq__` on the class instance.
- The convenience function `generate_theme_css(theme_name, color_preset)` in `theme_css_generator.py` is a better caching target — it already has the right signature.

**Why not Django cache framework?**
- Overkill. The number of unique `(theme_name, color_preset)` combinations is tiny (e.g., 8 themes x 20 presets = 160 max).
- Adds a dependency on Django cache configuration being set up.
- Serialization/deserialization overhead for what is a pure in-memory lookup.

**Recommended approach**: Use `functools.lru_cache` on the module-level convenience functions, with a small `maxsize`.

### Implementation Plan

#### A. `theme_css_generator.py` — Cache `generate_theme_css()`

```python
from functools import lru_cache

@lru_cache(maxsize=256)
def generate_theme_css(theme_name: str, color_preset: str = None) -> str:
    generator = CompleteThemeCSSGenerator(theme_name, color_preset)
    return generator.generate_css()
```

Then update all call sites to use this function instead of instantiating `CompleteThemeCSSGenerator` directly.

**Problem**: Several call sites instantiate `CompleteThemeCSSGenerator` directly. These need to be refactored to go through the cached function.

Affected call sites that bypass the convenience function:
- `views.py:25-26` — direct instantiation
- `context_processors.py:35-36, 38-39` — direct instantiation
- `theme_tags.py:88-89, 125-126` — direct instantiation
- `mixins.py:96-97` — direct instantiation

#### B. `pack_css_generator.py` — Add cached convenience function

```python
from functools import lru_cache

@lru_cache(maxsize=64)
def generate_pack_css(pack_name: str) -> str:
    generator = ThemePackCSSGenerator(pack_name)
    return generator.generate_css()
```

Then update pack call sites similarly.

#### C. `css_generator.py` — Cache `generate_theme_css()` (color-only)

```python
@lru_cache(maxsize=64)
def generate_theme_css(preset_name="default", include_base_styles=True,
                       include_utilities=True, include_design_tokens=True) -> str:
    ...
```

This is already a standalone function with the right signature. However, the `color_preset` parameter in `CompleteThemeCSSGenerator` already flows through this, so caching at the `CompleteThemeCSSGenerator` level subsumes this. Could still be useful for direct callers.

#### D. `design_system_css.py` — Cache `generate_design_system_css()`

```python
@lru_cache(maxsize=256)
def generate_design_system_css(design_system_name="minimal", color_preset_name="default",
                                include_base_styles=True, include_utilities=True) -> str:
    ...
```

### Cache Invalidation

**Not needed for production**: Theme/preset definitions are static module-level data. They never change during a process lifetime.

**For development**: Add a `clear_css_cache()` utility that calls `.cache_clear()` on each cached function. This could be called from a management command or signal. Consider wiring it to Django's `autoreload` signal for dev convenience.

```python
def clear_css_cache():
    """Clear all CSS generation caches. Call after modifying theme definitions."""
    generate_theme_css.cache_clear()
    generate_pack_css.cache_clear()
    # etc.
```

## 4. Risk Assessment

### Thread Safety
- `lru_cache` is thread-safe in CPython (uses a lock internally). Safe for WSGI servers with threading (gunicorn sync workers, etc.).
- No risk of partial reads or corrupted state.

### Memory
- Each cached entry is a CSS string, typically 5-15 KB.
- With `maxsize=256`, worst case is ~4 MB. In practice, most apps use 1-3 combinations, so memory usage is negligible.
- `lru_cache` automatically evicts least-recently-used entries when full.

### Correctness
- Output is deterministic for same inputs (verified: all data comes from module-level constants).
- `color_preset` defaults to `None` in `generate_theme_css()`, which the constructor resolves to `self.theme.color_preset`. This means `generate_theme_css("material", None)` and `generate_theme_css("material", "default")` could produce the same CSS but be cached as different entries. **Mitigation**: Normalize `color_preset` to the theme's default before caching, or accept the minor duplication (2 entries instead of 1).

### Breaking Changes
- None. The public API (`generate_theme_css()`, class constructors) stays the same.
- Call sites that directly instantiate generators should be updated to use cached functions, but this is an internal refactor.

### Invalidation Edge Cases
- Hot reload in development: themes are module-level constants, so they reload with the module. `lru_cache` lives on the function object, which also reloads. No issue.
- Custom tokens via `ThemeCSSGenerator(custom_tokens={...})`: These bypass the cached path since they use direct instantiation. This is correct — custom tokens should not be cached generically.

## 5. Files to Modify

| File | Change |
|------|--------|
| `djust_theming/theme_css_generator.py` | Add `@lru_cache` to `generate_theme_css()`, normalize `color_preset` param |
| `djust_theming/pack_css_generator.py` | Add `generate_pack_css()` convenience function with `@lru_cache` |
| `djust_theming/css_generator.py` | Add `@lru_cache` to `generate_theme_css()` |
| `djust_theming/design_system_css.py` | Add `@lru_cache` to `generate_design_system_css()` |
| `djust_theming/views.py` | Use `generate_theme_css()` / `generate_pack_css()` instead of direct instantiation |
| `djust_theming/context_processors.py` | Use cached functions instead of direct instantiation |
| `djust_theming/templatetags/theme_tags.py` | Use cached functions instead of direct instantiation |
| `djust_theming/mixins.py` | Use `generate_theme_css()` instead of direct instantiation |
| Tests | Add tests for cache hit behavior and `clear_css_cache()` |

## 6. Estimated Impact

- **Context processor path** (hottest): Goes from ~1-2ms string building per request to ~0.001ms dict lookup after first call. On a site doing 100 req/s, this saves ~100-200ms of CPU per second.
- **Template tag path**: Same improvement when used instead of context processor.
- **View path**: Already has HTTP-level caching (ETag), but server-side cache avoids regeneration on ETag miss.
- **LiveView path**: Saves regeneration on every `_setup_theme_context()` call during theme switching.
