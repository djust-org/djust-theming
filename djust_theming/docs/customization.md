# Customization Guide

This guide covers how to customize djust-theming's templates, CSS, and behavior for your project.

## Template Overrides

All djust-theming components render through Django templates, which means you can override any component's HTML by providing your own template with the same path.

### How It Works

djust-theming looks for templates under `djust_theming/` in your template directories. Django's template resolution order means your project's templates take priority over the package defaults.

To override a component template, create a file at the same path in your project's `templates/` directory:

```
your_project/
  templates/
    djust_theming/
      theme_head.html              # Override the <head> block
      theme_switcher.html          # Override the theme switcher widget
      components/
        button.html                # Override button rendering
        card.html                  # Override card rendering
        alert.html                 # Override alert rendering
        badge.html                 # Override badge rendering
        input.html                 # Override input rendering
```

### Available Templates

| Template | Rendered by | Purpose |
|----------|-------------|---------|
| `djust_theming/theme_head.html` | `{% theme_head %}` | Anti-FOUC script, CSS variables, component stylesheet, theme.js |
| `djust_theming/theme_switcher.html` | `{% theme_switcher %}` / `ThemeMixin` | Mode toggle + preset selector widget |
| `djust_theming/components/button.html` | `{% theme_button %}` | Button with variant/size support |
| `djust_theming/components/card.html` | `{% theme_card %}` | Card container with header/body/footer |
| `djust_theming/components/alert.html` | `{% theme_alert %}` | Alert box with variant and dismiss |
| `djust_theming/components/badge.html` | `{% theme_badge %}` | Inline badge with variant |
| `djust_theming/components/input.html` | `{% theme_input %}` | Form input group with label |
| `djust_theming/components/theme_mode_button.html` | `{% theme_mode_toggle %}` | Sun/moon toggle button |
| `djust_theming/components/preset_selector_dropdown.html` | `{% theme_preset_selector layout="dropdown" %}` | Preset dropdown |
| `djust_theming/components/preset_selector_grid.html` | `{% theme_preset_selector layout="grid" %}` | Preset button grid |
| `djust_theming/components/preset_selector_list.html` | `{% theme_preset_selector layout="list" %}` | Preset radio list |

### Template Context Variables

Each template receives context variables you can use in your overrides:

**theme_head.html:**
- `loading_class` -- whether to add a `loading` class to `<html>`
- `css_block` -- the generated CSS custom properties (rendered by the generator)
- `include_js` -- whether to include `theme.js`

**theme_switcher.html:**
- `presets` -- list of available preset dicts (`name`, `display_name`)
- `current_preset` -- name of the active preset
- `current_mode` -- current mode (`light`, `dark`, `system`)
- `liveview` -- `True` when rendered from a djust LiveView (see below)

**Component templates (button, card, alert, badge, input):**
- Each receives its own set of context variables (variant, size, title, message, etc.)
- Check the default template source for the full list

### LiveView vs Vanilla Event Bindings

The `theme_switcher.html` template uses a `liveview` context variable to switch between two event systems:

```html
{% if liveview %}
  {# djust LiveView -- uses dj-click/dj-change for WebSocket events #}
  <button dj-click="set_theme_mode" data-dj-mode="light">Light</button>
{% else %}
  {# Vanilla Django -- uses data attributes for JS-handled events #}
  <button data-djust-event="set_theme_mode" data-djust-params='{"mode": "light"}'>Light</button>
{% endif %}
```

When overriding `theme_switcher.html`, preserve this conditional if you need to support both djust LiveView and vanilla Django usage.

---

## Color Conversions

djust-theming provides a set of pure color conversion functions in `djust_theming.colors`, plus convenience methods on `ColorScale` for converting between HSL, RGB, and hex formats.

### Standalone Functions

All six functions are exported from the top-level package:

```python
from djust_theming import hsl_to_rgb, rgb_to_hsl, hex_to_rgb, rgb_to_hex, hex_to_hsl, hsl_to_hex
```

**HSL to RGB and back:**

```python
# HSL values: h (0-360), s (0-100), l (0-100)
# RGB values: r, g, b each 0-255

hsl_to_rgb(0, 100, 50)      # (255, 0, 0)  — pure red
hsl_to_rgb(120, 100, 50)    # (0, 255, 0)  — pure green
hsl_to_rgb(240, 100, 50)    # (0, 0, 255)  — pure blue

rgb_to_hsl(255, 0, 0)       # (0, 100, 50) — pure red
rgb_to_hsl(59, 130, 246)    # (217, 91, 60) — approximately
```

**Hex to RGB and back:**

```python
hex_to_rgb("#ff0000")        # (255, 0, 0)
hex_to_rgb("#fff")           # (255, 255, 255)  — 3-digit shorthand
hex_to_rgb("3b82f6")         # (59, 130, 246)   — # prefix is optional

rgb_to_hex(255, 0, 0)        # "#ff0000"
rgb_to_hex(59, 130, 246)     # "#3b82f6"
```

**Hex to HSL and back (composed from the above):**

```python
hex_to_hsl("#ff0000")        # (0, 100, 50)
hsl_to_hex(0, 100, 50)      # "#ff0000"
hsl_to_hex(0, 0, 100)       # "#ffffff"
```

### ColorScale Methods

`ColorScale` has instance methods for output and class methods for construction:

**Output methods (instance):**

```python
from djust_theming.presets import ColorScale

color = ColorScale(221, 83, 53)

color.to_hsl()       # "221 83% 53%"         — CSS variable value
color.to_hsl_func()  # "hsl(221, 83%, 53%)"  — CSS function
color.to_hex()       # "#3b82f6"             — hex string
color.to_rgb()       # (59, 130, 246)        — RGB tuple
color.to_rgb_func()  # "rgb(59, 130, 246)"   — CSS function
```

**Factory methods (class):**

```python
# Create a ColorScale from a hex color (e.g., from a design tool)
color = ColorScale.from_hex("#3b82f6")
# color.h, color.s, color.lightness are set to the HSL equivalent

# Create a ColorScale from RGB values
color = ColorScale.from_rgb(59, 130, 246)
```

This is useful when importing colors from design tools that export hex or RGB values. For example, to build a custom preset from Figma hex colors:

```python
from djust_theming.presets import ThemePreset, ThemeTokens, ColorScale, THEME_PRESETS

MY_PRESET = ThemePreset(
    name="figma-export",
    display_name="Figma Export",
    light=ThemeTokens(
        background=ColorScale.from_hex("#ffffff"),
        foreground=ColorScale.from_hex("#0f172a"),
        primary=ColorScale.from_hex("#3b82f6"),
        primary_foreground=ColorScale.from_hex("#f8fafc"),
        # ... remaining tokens
    ),
    dark=ThemeTokens(
        # ... dark mode tokens
    ),
)

THEME_PRESETS["figma-export"] = MY_PRESET
```

### Rounding Behavior

`ColorScale` stores HSL values as integers (h, s, lightness). When converting from hex or RGB to HSL, values are rounded to the nearest integer. This means a hex-to-HSL-to-hex round trip may differ by up to 1-2 per RGB channel. Hex-to-RGB-to-hex round trips are lossless.

---

## Token Architecture

djust-theming separates concerns into two token layers: **color tokens** (theme-dependent, light/dark aware) and **structural tokens** (theme-agnostic, set once).

### Color Tokens (`ThemeTokens`)

`ThemeTokens` holds HSL color values that change between light and dark mode. Each `ThemePreset` contains two `ThemeTokens` instances (one for light, one for dark). These generate CSS custom properties like `--primary`, `--background`, `--destructive-foreground`, etc.

Color tokens are the values that change when a user switches presets or toggles dark mode.

```python
from djust_theming.presets import ThemeTokens, ColorScale

light_tokens = ThemeTokens(
    background=ColorScale(0, 0, 100),     # White
    foreground=ColorScale(240, 10, 4),     # Near-black
    primary=ColorScale(220, 70, 50),       # Blue
    primary_foreground=ColorScale(0, 0, 98),
    # ... all 29 color fields
)
```

The full list of color tokens (29 fields):

| Category | Tokens |
|----------|--------|
| **Backgrounds** | `background`, `foreground` |
| **Card** | `card`, `card_foreground` |
| **Popover** | `popover`, `popover_foreground` |
| **Primary** | `primary`, `primary_foreground` |
| **Secondary** | `secondary`, `secondary_foreground` |
| **Muted** | `muted`, `muted_foreground` |
| **Accent** | `accent`, `accent_foreground` |
| **Destructive** | `destructive`, `destructive_foreground` |
| **Success** | `success`, `success_foreground` |
| **Warning** | `warning`, `warning_foreground` |
| **Info** | `info`, `info_foreground` |
| **Link** | `link`, `link_hover` |
| **Code** | `code`, `code_foreground` |
| **Selection** | `selection`, `selection_foreground` |
| **UI elements** | `border`, `input`, `ring` |

### Structural Tokens (`ThemePreset` + `design_tokens`)

Structural tokens control layout, spacing, typography, and radius. They do not change between light and dark mode.

**`ThemePreset.radius`** -- a `float` that sets the base border radius for the preset, output as `--radius: {value}rem` in `:root`. Most presets use `0.5` (default); some use `0.75` for a more rounded feel.

```python
from djust_theming.presets import ThemePreset

preset = ThemePreset(
    name="brand",
    display_name="Brand",
    light=light_tokens,
    dark=dark_tokens,
    radius=0.75,  # More rounded corners
)
```

**`design_tokens`** -- the `design_tokens.py` module generates theme-agnostic structural CSS custom properties that apply regardless of which preset is active:

| Token group | Examples | Source |
|-------------|----------|--------|
| **Spacing** | `--space-1` through `--space-24` (4px to 96px) | `get_spacing_tokens()` |
| **Typography** | `--font-size-xs` through `--font-size-4xl`, `--line-height-*`, `--font-weight-*` | `get_typography_tokens()` |
| **Radius scale** | `--radius-sm`, `--radius-md`, `--radius-lg`, `--radius-xl`, `--radius-2xl`, `--radius-full` | `get_radius_extensions()` |
| **Transitions** | `--duration-fast`, `--duration-normal`, `--duration-slow`, `--ease-in`, `--ease-out` | `get_transition_tokens()` |
| **Shadows** | `--shadow-sm`, `--shadow-md`, `--shadow-lg` (theme-aware) | `get_shadow_tokens()` |

The radius scale tokens are derived from `--radius` via CSS `calc()`, so changing `ThemePreset.radius` automatically adjusts the entire radius scale.

### Why This Separation Matters

Keeping color tokens separate from structural tokens means:

1. **Presets stay simple** -- A preset defines colors and a radius value. It does not need to redefine spacing, typography, or transitions.
2. **Light/dark mode is clean** -- Only color values change between modes. Structural values like radius, spacing, and transitions stay constant.
3. **Custom presets are easy to create** -- Define 29 color fields per mode plus an optional radius. Everything else is inherited from the design system.

### Creating a Custom Preset

```python
# settings.py or a presets module
from djust_theming.presets import ThemePreset, ThemeTokens, ColorScale, THEME_PRESETS

MY_PRESET = ThemePreset(
    name="brand",
    display_name="Brand Colors",
    description="Corporate brand theme",
    radius=0.625,  # Custom border radius (in rem)
    light=ThemeTokens(
        background=ColorScale(0, 0, 100),
        foreground=ColorScale(210, 20, 10),
        card=ColorScale(0, 0, 99),
        card_foreground=ColorScale(210, 20, 10),
        popover=ColorScale(0, 0, 100),
        popover_foreground=ColorScale(210, 20, 10),
        primary=ColorScale(210, 80, 45),
        primary_foreground=ColorScale(0, 0, 98),
        secondary=ColorScale(210, 10, 95),
        secondary_foreground=ColorScale(210, 20, 10),
        muted=ColorScale(210, 10, 95),
        muted_foreground=ColorScale(210, 10, 40),
        accent=ColorScale(210, 10, 95),
        accent_foreground=ColorScale(210, 20, 10),
        destructive=ColorScale(0, 84, 60),
        destructive_foreground=ColorScale(0, 0, 98),
        success=ColorScale(142, 76, 36),
        success_foreground=ColorScale(0, 0, 98),
        warning=ColorScale(38, 92, 50),
        warning_foreground=ColorScale(0, 0, 98),
        info=ColorScale(199, 89, 48),
        info_foreground=ColorScale(0, 0, 98),
        link=ColorScale(210, 80, 45),
        link_hover=ColorScale(210, 80, 35),
        code=ColorScale(210, 10, 94),
        code_foreground=ColorScale(210, 20, 20),
        selection=ColorScale(210, 100, 80),
        selection_foreground=ColorScale(210, 20, 10),
        border=ColorScale(210, 10, 90),
        input=ColorScale(210, 10, 90),
        ring=ColorScale(210, 80, 45),
    ),
    dark=ThemeTokens(
        # ... dark mode colors
    ),
)

THEME_PRESETS["brand"] = MY_PRESET
```

---

## Migrating from THEMES to DESIGN_SYSTEMS

The `themes.py` module (`THEMES` dict, `get_theme()`, `list_themes()`) is deprecated. All access now emits `DeprecationWarning`. The replacement is `theme_packs.py`, which provides `DESIGN_SYSTEMS` -- the same 11 design systems (material, ios, fluent, minimalist, playful, corporate, retro, elegant, neo\_brutalist, organic, dense) with a cleaner architecture that separates design dimensions from color presets.

The old module will continue to work throughout the 1.x series but will be removed in 2.0.

### Quick Reference

| Old (deprecated) | New |
|-------------------|-----|
| `from djust_theming.themes import THEMES` | `from djust_theming.theme_packs import DESIGN_SYSTEMS` |
| `from djust_theming.themes import get_theme` | `from djust_theming.theme_packs import get_design_system` |
| `from djust_theming.themes import list_themes` | `from djust_theming.theme_packs import get_all_design_systems` |
| `THEMES["material"]` returns a `Theme` | `DESIGN_SYSTEMS["material"]` returns a `DesignSystem` |
| `get_theme("material")` | `get_design_system("material")` |
| `list_themes()` | `get_all_design_systems()` |

### Step-by-Step Migration

**1. Update imports**

```python
# Before
from djust_theming.themes import THEMES, get_theme, list_themes

# After
from djust_theming.theme_packs import DESIGN_SYSTEMS, get_design_system, get_all_design_systems
```

**2. Replace dict lookups**

If you only check whether a theme name is valid (key existence), the change is a direct substitution:

```python
# Before
if theme_name in THEMES:
    ...

# After
if theme_name in DESIGN_SYSTEMS:
    ...
```

**3. Update attribute access**

`Theme` and `DesignSystem` have different structures. If you read attributes from theme objects, map them to the new equivalents:

| `Theme` attribute | `DesignSystem` equivalent | Notes |
|-------------------|---------------------------|-------|
| `theme.display_name` | `ds.display_name` | Same |
| `theme.description` | `ds.description` | Same |
| `theme.typography.font_sans` | `ds.typography.font_family` | Renamed |
| `theme.typography.font_mono` | `ds.typography.font_mono` | Same |
| `theme.typography.text_base` | `ds.typography.base_size` | Renamed |
| `theme.spacing.base` | `ds.layout.base_spacing` | Moved to `layout` |
| `theme.border_radius.*` | `ds.surface.border_radius` | Consolidated |
| `theme.shadows.*` | `ds.surface.shadow_*` | Moved to `surface` |
| `theme.animations.*` | `ds.animation.*` | Moved |
| `theme.component_styles.*` | `ds.interaction.*` | Moved |

**4. Iterate over all design systems**

```python
# Before
for name, theme in THEMES.items():
    print(name, theme.display_name)

# After
for name, ds in DESIGN_SYSTEMS.items():
    print(name, ds.display_name)
```

**5. Verify with warnings enabled**

Run your project with deprecation warnings visible to find any remaining references:

```bash
python -W default::DeprecationWarning manage.py runserver
```

Any remaining `themes.py` usage will print a warning with the import location, making it straightforward to find and update.

### What About theme_css_generator.py?

`theme_css_generator.py` still imports from `themes.py` internally to generate CSS from `Theme` objects. This is intentional -- it will be migrated to use `DesignSystem` objects in a future release. You do not need to change anything if you use `generate_theme_css()` or `CompleteThemeCSSGenerator` directly; they will continue to work.

---

## CSS Architecture

djust-theming ships two CSS files with distinct purposes:

### base.css (manual include)

A full design system with layout, generic components, forms, tables, and utilities. Include it explicitly:

```html
<link href="{% static 'djust_theming/css/base.css' %}" rel="stylesheet">
```

### components.css (auto-included)

Styles for template-tag components (`{% theme_button %}`, `{% theme_card %}`, etc.). This file is **automatically included** by `{% theme_head %}` -- you do not need to add it manually.

Components styled in `components.css`:
- `.alert` with variants (default, success, warning, destructive)
- `.badge` with variants (default, secondary, success, warning, destructive, outline)
- `.btn` with sizes (sm, md, lg) and variants (primary, secondary, destructive, ghost, link)
- `.card` with header/title/body/footer
- `.input-group`, `.input-label`, `.input`
- `.theme-switcher`, `.theme-mode-btn`, `.theme-preset-select`

### Overriding Component Styles

All component CSS uses CSS custom properties (e.g., `--primary`, `--foreground`, `--radius`). To change a component's look:

1. **Change the theme** -- switch presets or design systems to change colors, spacing, and radius globally
2. **Override specific properties** -- add your own CSS after `{% theme_head %}` to override specific styles
3. **Replace the template** -- override the component template to change the HTML structure entirely (the CSS classes remain the same)

### Adding CSS for New Components

If you create new component templates, add their CSS to your project's own stylesheet rather than modifying `components.css`. Your CSS can reference the same CSS custom properties:

```css
.my-component {
  background: hsl(var(--card));
  color: hsl(var(--card-foreground));
  border: 1px solid hsl(var(--border));
  border-radius: var(--radius);
  padding: var(--spacing-4);
}
```

---

## Performance

### CSS Generation Caching

CSS generation (theme variables, design tokens) is cached using `lru_cache`. The same theme + preset combination produces identical CSS, so it's only generated once per process lifetime.

This means:
- First request for a theme/preset combination generates the CSS
- All subsequent requests serve from cache (no computation)
- Cache is per-process (each worker has its own cache)

### Clearing the Cache

If you modify presets or design tokens at runtime (rare in production), clear the cache:

```python
from djust_theming import clear_css_cache

# After modifying THEME_PRESETS or design tokens
clear_css_cache()
```

This is mainly useful during development. In production, the cache is populated on first use and remains valid for the process lifetime.

### ThemeManager Caching

The `ThemeManager` instance is cached per-request on `request._djust_theme_manager`. If a page uses 4-5 theme template tags, they all share the same `ThemeManager` instance instead of creating separate ones.

To access the theme manager in your own code:

```python
from djust_theming import get_theme_manager

def my_view(request):
    manager = get_theme_manager(request)
    state = manager.get_state()
    # state.mode, state.preset, state.theme
```

This returns the same cached instance that template tags use, so there's no extra overhead.

---

## Static File Handling

### Automatic Cache Busting

djust-theming uses Django's `{% static %}` tag and `staticfiles_storage.url()` for all asset references. This means:

- Assets respect your `STATIC_URL` setting (works with CDNs, custom prefixes)
- If you use `ManifestStaticFilesStorage`, assets get automatic content-hash-based cache busting
- No manual `?v=N` cache busters to maintain

### Required Static Files

These are bundled with the package and served automatically:

| File | Included by | Purpose |
|------|-------------|---------|
| `djust_theming/js/theme.js` | `{% theme_head %}` (when `include_js=True`) | Client-side theme switching, anti-FOUC, localStorage persistence |
| `djust_theming/css/components.css` | `{% theme_head %}` (always) | Component styles for template tags |
| `djust_theming/css/base.css` | Manual `<link>` tag | Full design system (optional) |

Run `python manage.py collectstatic` to collect these into your `STATIC_ROOT` for production.

---

## Accessibility Contrast Validation

djust-theming includes a Django system check that validates the contrast ratios of all registered theme presets against WCAG AA standards at startup. This runs automatically when Django starts (e.g., `runserver`, `migrate`, `check`) and requires no configuration.

### What It Checks

The system check validates 12 foreground/background token pairs across both light and dark modes for every preset in `THEME_PRESETS`:

| Foreground Token | Background Token | Description |
|------------------|------------------|-------------|
| `foreground` | `background` | Main text on page background |
| `card_foreground` | `card` | Text on card surfaces |
| `popover_foreground` | `popover` | Text on popover/tooltip surfaces |
| `primary_foreground` | `primary` | Text on primary buttons/elements |
| `secondary_foreground` | `secondary` | Text on secondary elements |
| `muted_foreground` | `muted` | Subdued text on muted backgrounds |
| `accent_foreground` | `accent` | Text on accent-colored elements |
| `destructive_foreground` | `destructive` | Text on destructive/danger elements |
| `success_foreground` | `success` | Text on success elements |
| `warning_foreground` | `warning` | Text on warning elements |
| `info_foreground` | `info` | Text on informational elements |
| `code_foreground` | `code` | Text on code block backgrounds |

Each pair is tested against the WCAG AA minimum contrast ratio of **4.5:1** for normal text.

### What Warnings Look Like

If a preset fails a contrast check, Django will print a warning during startup:

```
System check identified some issues:

WARNINGS:
?: (djust_theming.W001) Preset "synthwave" dark mode: text on muted contrast ratio 3.12:1 < 4.5:1 (WCAG AA)
    HINT: Adjust muted_foreground or muted to achieve at least 4.5:1 contrast.
?: (djust_theming.W001) Preset "outrun" light mode: text on warning contrast ratio 2.87:1 < 4.5:1 (WCAG AA)
    HINT: Adjust warning_foreground or warning to achieve at least 4.5:1 contrast.
```

These are **warnings, not errors** -- they will not prevent your application from starting. They serve as informational guidance to help you improve the accessibility of your themes.

### Silencing Warnings

If you have reviewed a warning and determined it is acceptable for your use case (e.g., the token pair is used for decorative elements rather than readable text), you can silence it using Django's `SILENCED_SYSTEM_CHECKS` setting:

```python
# settings.py

# Silence all djust-theming contrast warnings
SILENCED_SYSTEM_CHECKS = ["djust_theming.W001"]
```

This is a standard Django mechanism -- see the [Django system checks documentation](https://docs.djangoproject.com/en/stable/ref/checks/) for details.

### Running Checks Manually

You can run the system checks at any time:

```bash
python manage.py check
```

Or filter to only compatibility checks (where the contrast check is registered):

```bash
python manage.py check --tag compatibility
```

### Custom Presets

If you register custom presets in `THEME_PRESETS`, they are automatically included in the contrast validation. This helps catch accessibility issues early when creating new color schemes:

```python
from djust_theming.presets import ThemePreset, ThemeTokens, ColorScale, THEME_PRESETS

MY_PRESET = ThemePreset(
    name="brand",
    display_name="Brand",
    description="Corporate brand colors",
    light=ThemeTokens(
        background=ColorScale(0, 0, 100),
        foreground=ColorScale(0, 0, 10),
        # ... tokens with sufficient contrast
    ),
    dark=ThemeTokens(
        # ... dark mode tokens
    ),
)

THEME_PRESETS["brand"] = MY_PRESET
# The next time Django starts, "brand" will be checked automatically.
```
