# Customization Guide

This guide covers how to customize djust-theming's templates, CSS, and behavior for your project.

## Template Overrides

All djust-theming components render through Django templates, which means you can override any component's HTML. There are two levels of template override: **global overrides** that apply regardless of theme, and **theme-specific overrides** that only activate when a particular design system theme is active.

### How It Works

When a component tag renders (e.g., `{% theme_button %}`), djust-theming resolves the template using a two-step fallback chain:

1. **Theme-specific override**: `djust_theming/themes/{theme_name}/components/{component}.html`
2. **Default template**: `djust_theming/components/{component}.html`

The first template found wins. If no theme-specific override exists, the default template (shipped with the package) is used. This resolution uses Django's `select_template()`, so templates can live in any configured template directory.

### Global Overrides

To override a component template for all themes, create a file at the default path in your project's `templates/` directory:

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

### Theme-Specific Overrides

To override a template only when a specific design system theme is active (e.g., "corporate"), place the template under `themes/{theme_name}/`:

```
your_project/
  templates/
    djust_theming/
      themes/
        corporate/
          theme_switcher.html                   # Corporate-specific switcher
          components/
            button.html                         # Corporate-specific button
            card.html                           # Corporate-specific card
        ios/
          components/
            button.html                         # iOS-specific button
```

When the active theme is `corporate`, `{% theme_button %}` renders `djust_theming/themes/corporate/components/button.html`. When the theme switches to `material` (which has no override), it falls back to `djust_theming/components/button.html`.

This is useful when different design systems need fundamentally different HTML structures -- for example, a Material Design button with a ripple effect container versus a Minimalist button with no wrapper elements.

### Built-in Design System Variants

Five design systems ship with HTML-different template variants for `button` and `card` components. These variants use design-system-specific markup that goes beyond CSS-only differences:

| Design System | Button Variant | Card Variant | Extra |
|---------------|---------------|--------------|-------|
| **material** | Ripple effect container (`btn-ripple`) | Elevated surface (`card-elevated`) | -- |
| **ios** | SF-style button (`btn-sf`) | Grouped inset card (`card-grouped`) | Segmented control tabs (`segmented-control`) |
| **fluent** | Reveal highlight (`btn-reveal`) | Acrylic background (`card-acrylic`) | -- |
| **neo_brutalist** | Offset shadow (`btn-offset`) | Thick border (`card-border-thick`) | -- |
| **playful** | Bounce animation (`btn-bounce`) | Decorated container (`card-decorated`) | -- |

The remaining design systems (minimalist, corporate, retro, elegant, organic, dense) are **CSS-only** -- they use the default component templates and achieve their visual identity entirely through CSS custom properties and token values.

When a variant system is active, the template resolver automatically selects the design-system-specific template. For components that don't have a variant override (e.g., `alert` under material), the default template is used.

### Resolution Order Summary

For `{% theme_button %}` with the active theme set to `corporate`:

| Priority | Template path | Source |
|----------|---------------|--------|
| 1 | `djust_theming/themes/corporate/components/button.html` | Your project (theme-specific) |
| 2 | `djust_theming/components/button.html` | Your project (global override) or package default |

For `{% theme_switcher %}` with the active theme set to `ios`:

| Priority | Template path | Source |
|----------|---------------|--------|
| 1 | `djust_theming/themes/ios/theme_switcher.html` | Your project (theme-specific) |
| 2 | `djust_theming/theme_switcher.html` | Your project (global override) or package default |

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
| `djust_theming/layouts/base.html` | `{% extends %}` | Root layout with theme integration |
| `djust_theming/layouts/sidebar.html` | `{% extends %}` | Sidebar + main content |
| `djust_theming/layouts/topbar.html` | `{% extends %}` | Sticky topbar + content |
| `djust_theming/layouts/sidebar_topbar.html` | `{% extends %}` | Sidebar + topbar combined |
| `djust_theming/layouts/centered.html` | `{% extends %}` | Centered max-width container |
| `djust_theming/layouts/dashboard.html` | `{% extends %}` | Sidebar + topbar + responsive grid |
| `djust_theming/layouts/split.html` | `{% extends %}` | Two-panel list/detail view |

For full layout documentation including blocks, responsive behavior, and examples, see the [Layout Templates Guide](layouts.md).

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
- See [Component Contracts Reference](component-contracts.md) for the full list per component

### Component Slots

Every component template supports **slot variables** -- optional context variables that let you inject custom HTML into specific sections of a component without overriding the entire template. Slots are the recommended approach when you need to customize part of a component (e.g., add an icon to a button) while keeping the rest of the default structure.

#### How slots work

When you pass a slot variable to a component tag, it replaces the corresponding default content. If no slot is provided, the component renders its default output -- so existing code is unaffected.

#### Slot examples

**Button with icon:**

```html
{% theme_button text="Save" slot_icon='<svg class="icon-save" width="16" height="16"><use href="#save"/></svg>' %}
```

This renders the SVG before the button text. Without `slot_icon`, just the text appears.

**Button with loading spinner:**

```html
{% theme_button text="Submit" slot_loading='<span class="spinner"></span> Saving...' %}
```

`slot_loading` replaces all button content (both icon and text), useful for async states.

**Card with custom header and footer:**

```html
{% theme_card slot_header='<div class="flex items-center"><img src="avatar.png" class="avatar"/> <h3>User Profile</h3></div>' slot_footer='<button class="btn btn-primary">Edit</button>' %}
```

**Alert with actions:**

```html
{% theme_alert message="Delete this item?" variant="warning" slot_actions='<button class="btn btn-destructive">Delete</button> <button class="btn btn-secondary">Cancel</button>' %}
```

**Input with help text and error:**

```html
{% theme_input name="email" label="Email" slot_help_text="We will never share your email." slot_error="Please enter a valid email address." %}
```

**Input with custom element (textarea instead of input):**

```html
{% theme_input name="bio" label="Biography" slot_input='<textarea name="bio" id="bio" rows="4" class="input"></textarea>' %}
```

#### Available slots per component

| Component | Slots |
|-----------|-------|
| Button | `slot_icon`, `slot_content`, `slot_loading` |
| Card | `slot_header`, `slot_body`, `slot_footer` |
| Alert | `slot_icon`, `slot_message`, `slot_actions`, `slot_dismiss` |
| Badge | `slot_content` |
| Input | `slot_label`, `slot_input`, `slot_help_text`, `slot_error` |

For full details on each slot (what it overrides, priority rules, accessibility requirements), see the [Component Contracts Reference](component-contracts.md).

#### Slots in template overrides

If you are writing a theme-specific template override (see Template Overrides above), you can reference slot variables in your custom template. The slot values are passed through the template context:

```html
{# templates/djust_theming/themes/corporate/components/button.html #}
<button class="corporate-btn corporate-btn-{{ variant }}">
    {% if slot_loading %}
        {{ slot_loading|safe }}
    {% else %}
        {% if slot_icon %}<span class="corporate-icon">{{ slot_icon|safe }}</span>{% endif %}
        {% if slot_content %}{{ slot_content|safe }}{% else %}{{ text }}{% endif %}
    {% endif %}
</button>
```

**Important:** Slot variables contain trusted developer-supplied HTML and use the `|safe` filter. Never pass user input directly into slot variables.

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

## CSS Cascade Layers

djust-theming wraps all generated CSS in [CSS cascade layers](https://developer.mozilla.org/en-US/docs/Web/CSS/@layer) to give you predictable control over specificity. This means you can override any framework style without resorting to `!important` or fighting selector specificity.

### Layer Order

All generated CSS begins with a layer order declaration:

```css
@layer base, tokens, components, theme;
```

This establishes a priority hierarchy (lowest to highest):

| Layer | Priority | Contents |
|-------|----------|----------|
| `base` | Lowest | Reset styles, body defaults, transition rules, reduced-motion media query |
| `tokens` | Low | CSS custom properties (`:root` vars, dark mode vars, system preference, design tokens) |
| `components` | Medium | Utility classes, component styles (`.btn`, `.card`, `.form-input`), typography classes |
| `theme` | Highest | Reserved for theme author overrides -- empty by default |

### How to Use the `theme` Layer

The `theme` layer is declared in the layer order but left empty by the framework. To override any framework style, wrap your CSS in `@layer theme { ... }`:

```css
/* your-custom.css */
@layer theme {
  .btn {
    border-radius: 0;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .card {
    border: 2px solid hsl(var(--border));
    box-shadow: none;
  }
}
```

Because `theme` is declared after `components` in the layer order, your styles automatically win over the framework's component styles -- no `!important` needed, regardless of selector specificity.

### Where Layers Are Applied

The framework applies layers automatically across all CSS output paths:

| CSS Source | Layer | Notes |
|-----------|-------|-------|
| `:root` vars, dark mode, design tokens | `tokens` | Generated by `{% theme_head %}` |
| Base element styles (body, transitions) | `base` | Generated by `{% theme_head %}` |
| Utility classes (`.bg-primary`, `.text-*`, `.btn-*`) | `components` | Generated by `{% theme_head %}` |
| `components.css` (static file) | `components` | Loaded via `<link>` or inlined with prefix |
| Typography classes (`.text-xs`, `.font-bold`) | `components` | Generated for design system themes |
| Theme component styles (`.btn`, `.card`, `.form-input`) | `components` | Generated for design system themes |
| Theme pack additions (icons, animations, patterns) | `theme` | Generated for theme packs |

### Disabling CSS Layers

If you need the pre-1.1 behavior (flat CSS with no `@layer` wrapping), set `use_css_layers` to `False` in your settings:

```python
# settings.py
LIVEVIEW_CONFIG = {
    'theme': {
        'use_css_layers': False,  # Disable @layer wrapping
    }
}
```

When disabled, all CSS is output without any `@layer` wrappers, behaving identically to versions before 1.1.

### Customizing Layer Order

You can also change the layer order string (advanced usage):

```python
LIVEVIEW_CONFIG = {
    'theme': {
        'css_layer_order': 'base, tokens, components, utilities, theme',
    }
}
```

### Browser Support

CSS cascade layers are supported in all modern browsers (Chrome 99+, Firefox 97+, Safari 15.4+, Edge 99+). For older browsers, layers are ignored and styles fall back to standard cascade behavior, which matches the pre-1.1 output.

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

## Registering Presets and Themes at Runtime (Third-Party Apps)

If you are building a reusable Django app that ships its own presets or design systems, use the **Theme Registry API** to register them dynamically. This is the recommended approach for pip-installable theme packages.

### register_preset / register_theme

Call these in your app's `AppConfig.ready()` method, which runs after `djust_theming` has initialized the registry:

```python
# my_theme_app/apps.py
from django.apps import AppConfig


class MyThemeAppConfig(AppConfig):
    name = "my_theme_app"

    def ready(self):
        from djust_theming.registry import get_registry
        from .presets import NORD_PRESET, CATPPUCCIN_PRESET
        from .design_systems import CUSTOM_DS

        registry = get_registry()

        # Register custom color presets
        registry.register_preset("nord", NORD_PRESET)
        registry.register_preset("catppuccin", CATPPUCCIN_PRESET)

        # Register a custom design system
        registry.register_theme("my-design-system", CUSTOM_DS)
```

**Important**: Ensure your app appears *after* `djust_theming` in `INSTALLED_APPS` so that the registry is already populated when your `ready()` runs:

```python
INSTALLED_APPS = [
    # ...
    "djust_theming",
    "my_theme_app",  # After djust_theming
]
```

### register_manifest

To register a `ThemeManifest` (parsed from a `theme.toml`) programmatically:

```python
from djust_theming.registry import get_registry
from djust_theming.manifest import ThemeManifest

manifest = ThemeManifest(
    name="my-packaged-theme",
    version="1.0.0",
    description="A theme distributed as a pip package",
    preset="blue",
    design_system="material",
)

get_registry().register_manifest("my-packaged-theme", manifest)
```

### Package Convention for DJUST_THEMES

If your theme package is listed in the `DJUST_THEMES` setting, the registry will auto-import it and look for these module-level attributes:

```python
# my_theme_package/__init__.py

from djust_theming.manifest import ThemeManifest
from djust_theming.presets import ThemePreset, ThemeTokens, ColorScale


def get_theme_manifest():
    """Return a ThemeManifest for this package."""
    return ThemeManifest(
        name="my-theme",
        version="1.0.0",
        preset="custom-preset",
        design_system="material",
    )


# Optional: export presets
PRESETS = {
    "custom-preset": ThemePreset(
        name="custom-preset",
        display_name="Custom Preset",
        light=ThemeTokens(...),
        dark=ThemeTokens(...),
    ),
}

# Optional: export design systems
DESIGN_SYSTEMS = {
    "custom-ds": ...,
}
```

Then in Django settings:

```python
DJUST_THEMES = ["my_theme_package"]
```

### Thread Safety

The registry is a thread-safe singleton. All `register_*` methods acquire a lock internally, so you can safely call them from multiple app `ready()` methods without coordination. Read-only methods (`get_preset`, `has_theme`, `list_presets`, etc.) are safe to call from any thread at any time.

### Validating After Registration

After registering custom presets or themes, you can validate them with the management command:

```bash
python manage.py djust_theme validate-theme my-packaged-theme
```

Or run Django's system checks, which will verify that configured presets and design systems exist in the registry:

```bash
python manage.py check --tag compatibility
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

## Programmatic CSS Generation

If you need to generate theme CSS outside of templates (e.g., in a management command, an API endpoint, or a background task), use `generate_css_for_state()`:

```python
from djust_theming import generate_css_for_state, get_css_prefix, get_theme_manager

# From a request (uses session/cookie state)
manager = get_theme_manager(request)
state = manager.get_state()
css = generate_css_for_state(state, css_prefix=get_css_prefix())

# Or build a ThemeState manually
from djust_theming import ThemeState

state = ThemeState(
    theme="material",
    preset="blue",
    mode="dark",
    resolved_mode="dark",
    pack=None,
)
css = generate_css_for_state(state)
```

### How it works

`generate_css_for_state(state, css_prefix="")` is the single entry point for CSS generation:

1. If `state.pack` is set, it tries `generate_pack_css(pack_name=state.pack)`.
2. If the pack is not found (or no pack is set), it falls back to `generate_theme_css(theme_name=state.theme, color_preset=state.preset, css_prefix=css_prefix)`.

This is the same logic used internally by `{% theme_head %}`, `{% theme_css %}`, the linked-CSS view, the context processor, and `ThemeMixin`. You do not need to call `generate_theme_css()` or `generate_pack_css()` directly unless you need lower-level control.

### `get_css_prefix()`

Returns the `css_prefix` string from `LIVEVIEW_CONFIG["theme"]["css_prefix"]`, defaulting to `""`. Pass this to `generate_css_for_state()` when you want component class names to be prefixed.

---

## CSS Namespace Prefixing

djust-theming uses generic CSS class names like `.btn`, `.card`, `.alert`, and `.badge` for its component templates. If your project also includes Bootstrap, Bulma, or another CSS framework that uses these same class names, the styles will collide.

To avoid collisions, you can configure a **CSS namespace prefix** that is prepended to every component class name.

### Configuration

Add `css_prefix` to your `LIVEVIEW_CONFIG["theme"]` settings:

```python
# settings.py
LIVEVIEW_CONFIG = {
    "theme": {
        "css_prefix": "dj-",   # All component classes become .dj-btn, .dj-card, etc.
    }
}
```

- **Default:** `""` (empty string) -- no prefix, full backward compatibility.
- **Convention:** The prefix should end with `-` for readable class names (e.g., `"dj-"` produces `.dj-btn`). If you omit the trailing dash, a Django system check (`djust_theming.W002`) will warn you.

### What Gets Prefixed

Component CSS classes used by `{% theme_button %}`, `{% theme_card %}`, `{% theme_alert %}`, `{% theme_badge %}`, `{% theme_input %}`, and `{% theme_switcher %}` are all prefixed:

| Original class | Prefixed (with `"dj-"`) |
|----------------|-------------------------|
| `.btn` | `.dj-btn` |
| `.btn-primary` | `.dj-btn-primary` |
| `.card` | `.dj-card` |
| `.card-header` | `.dj-card-header` |
| `.alert` | `.dj-alert` |
| `.badge` | `.dj-badge` |
| `.input` | `.dj-input` |
| `.input-group` | `.dj-input-group` |
| `.theme-switcher` | `.dj-theme-switcher` |
| `.theme-mode-btn` | `.dj-theme-mode-btn` |

### What Does NOT Get Prefixed

- **`base.css` utility classes** (`.mt-2`, `.flex`, `.gap-4`, `.font-sans`, etc.) -- these are opt-in via a manual `<link>` tag and are not changed by the prefix setting.
- **CSS custom properties** (`--primary`, `--background`, `--radius`, etc.) -- these are variables, not class names.
- **Typography classes** in theme CSS (`.font-sans`, `.text-xs`, etc.) -- these are utilities, not component selectors.

### How It Works

When `css_prefix` is empty (the default), `{% theme_head %}` includes the static `components.css` file via a `<link>` tag, exactly as before.

When `css_prefix` is set to a non-empty value:

1. `{% theme_head %}` generates the component CSS inline (in a `<style>` tag) with all class selectors rewritten to include the prefix.
2. All component templates (`button.html`, `card.html`, etc.) render class names with the prefix: `class="{{ css_prefix }}btn"` becomes `class="dj-btn"`.
3. The `CompleteThemeCSSGenerator` also applies the prefix to component selectors it generates (`.btn`, `.card`, `.form-input`).

### Using Prefixed Classes in Your Own Templates

If you write HTML manually (instead of using template tags), use the prefixed class names:

```html
<!-- Without prefix (default) -->
<button class="btn btn-primary">Click</button>

<!-- With css_prefix="dj-" -->
<button class="dj-btn dj-btn-primary">Click</button>
```

If you override component templates, your templates receive `{{ css_prefix }}` in their context:

```html
<!-- your_project/templates/djust_theming/components/button.html -->
<button class="{{ css_prefix }}btn {{ css_prefix }}btn-{{ variant }}">
    {{ text }}
</button>
```

### Combining with Bootstrap or Other Frameworks

A typical setup for using djust-theming alongside Bootstrap:

```python
# settings.py
LIVEVIEW_CONFIG = {
    "theme": {
        "css_prefix": "dj-",
        "preset": "blue",
    }
}
```

```html
{% load theme_tags theme_components static %}
<head>
    {% theme_head %}
    <link href="bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <!-- Bootstrap button (uses .btn) -->
    <button class="btn btn-primary">Bootstrap Button</button>

    <!-- djust-theming button (uses .dj-btn via template tag) -->
    {% theme_button "Themed Button" variant="primary" %}
</body>
```

Both sets of classes coexist without collision.

### System Check

If you set `css_prefix` without a trailing `-`, Django will emit a warning at startup:

```
?: (djust_theming.W002) css_prefix "dj" does not end with "-". Component classes
   will render as ".djbtn" instead of ".dj-btn". Consider using "dj-" for cleaner
   class names.
    HINT: Add a trailing "-" to css_prefix, e.g. "dj-" instead of "dj".
```

Silence this warning with `SILENCED_SYSTEM_CHECKS = ["djust_theming.W002"]` if the behavior is intentional.

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

### Critical CSS Inlining

By default, djust-theming splits generated CSS into two parts to improve first-paint performance:

**Critical CSS** (inlined in `<style>`, ~2-4KB) — everything needed for first paint:
- `@layer` order declaration
- `:root` CSS custom properties (color tokens, light/dark mode)
- Dark mode selectors (`.dark`, `[data-theme="dark"]`)
- `prefers-color-scheme` media query
- Design tokens (spacing, typography scale, border-radius, shadows, animation vars)
- Theme-specific `:root` vars (from the active design system theme)

**Deferred CSS** (async-loaded via `<link rel="preload">`, larger) — not needed for first paint:
- Base element styles (body resets, transition rules)
- Utility classes (`.bg-*`, `.text-*`, `.border-*`, etc.)
- Typography utility classes (`.font-sans`, `.text-xs`, etc.)
- Component styles (`.btn`, `.card`, `.form-input`, etc.)

The deferred CSS is loaded asynchronously using the `preload`/`onload` pattern with a `<noscript>` fallback, so it never blocks rendering.

#### Configuration

Critical CSS splitting is enabled by default. To disable it and restore legacy behavior (all CSS in one `<style>` block):

```python
LIVEVIEW_CONFIG = {
    "theme": {
        "critical_css": False,  # default: True
    }
}
```

When enabled, `{% theme_head %}` outputs:

1. A `<style data-djust-theme-critical>` tag with the critical CSS inlined
2. A `<link rel="preload" href="..." as="style">` tag that async-loads the deferred CSS
3. A `<noscript>` fallback for the deferred CSS

When disabled, `{% theme_head %}` outputs a single `<style data-djust-theme>` tag with all CSS (the pre-I10 behavior).

#### Deferred CSS Endpoint

The deferred CSS is served by a dedicated Django view at the `deferred.css` URL within the djust-theming URL namespace. This endpoint:

- Sets `Cache-Control: max-age=3600, private` for efficient caching
- Uses `ETag` headers for conditional requests (304 Not Modified)
- Varies by `Cookie` so user-specific theme settings are respected

Make sure your URL configuration includes `djust_theming.urls`:

```python
urlpatterns = [
    path("djust-theming/", include("djust_theming.urls")),
]
```

#### Programmatic Access

If you need critical or deferred CSS separately (e.g., for a custom rendering pipeline):

```python
from djust_theming import (
    generate_critical_css_for_state,
    generate_deferred_css_for_state,
    get_theme_manager,
)

def my_view(request):
    manager = get_theme_manager(request)
    state = manager.get_state()

    critical = generate_critical_css_for_state(state)
    deferred = generate_deferred_css_for_state(state)
```

You can also use the generator classes directly:

```python
from djust_theming.css_generator import ThemeCSSGenerator

gen = ThemeCSSGenerator(preset_name="default")
critical = gen.generate_critical_css()   # tokens + layer declaration
deferred = gen.generate_deferred_css()   # base styles + utilities
```

#### Performance Benefits

On a typical page, critical CSS inlining reduces render-blocking CSS from ~15-20KB to ~2-4KB. The deferred CSS loads in parallel without blocking first paint, resulting in faster Largest Contentful Paint (LCP) and reduced Cumulative Layout Shift (CLS) because token variables are available immediately for the initial render.

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

## Brand Color Auto-Palette Generator

Instead of manually defining all 31 color tokens for light and dark modes, you can generate a complete `ThemePreset` from just your brand color(s) using `PaletteGenerator`.

### Basic Usage

```python
from djust_theming import PaletteGenerator
from djust_theming.presets import THEME_PRESETS

# Generate from a single brand color
preset = PaletteGenerator.from_brand_colors("#3b82f6")

# Register it for use in your app
THEME_PRESETS[preset.name] = preset
```

This produces a full `ThemePreset` with:
- Light mode: all 31 `ThemeTokens` fields as `ColorScale` instances
- Dark mode: all 31 `ThemeTokens` fields as `ColorScale` instances
- A generated `name`, `display_name`, and `description`
- A `radius` value appropriate for the chosen mode

### Providing Secondary and Accent Colors

You can supply up to three brand colors. Colors you omit are derived automatically:

```python
# Primary only -- secondary (complementary, 180 deg) and accent (analogous, 30 deg) are derived
preset = PaletteGenerator.from_brand_colors("#3b82f6")

# Primary + secondary -- accent is derived
preset = PaletteGenerator.from_brand_colors("#3b82f6", secondary="#10b981")

# All three -- no derivation needed
preset = PaletteGenerator.from_brand_colors(
    "#3b82f6", secondary="#10b981", accent="#f59e0b"
)
```

Both 6-digit (`#3b82f6`) and 3-digit (`#f00`) hex formats are accepted, with or without the `#` prefix. Invalid hex strings raise `ValueError`.

### Generation Modes

The `mode` parameter controls how the palette feels. Each mode adjusts saturation scaling, hue offsets for derived colors, background tinting, and border radius:

```python
preset = PaletteGenerator.from_brand_colors("#3b82f6", mode="vibrant")
```

| Mode | Saturation | Hue Spread | Radius | Best For |
|------|-----------|------------|--------|----------|
| `professional` (default) | 0.85x | Narrow | 0.5 rem | Business apps, corporate sites |
| `playful` | 1.15x | Wide | 0.75 rem | Consumer apps, marketing pages |
| `muted` | 0.55x | Narrow | 0.375 rem | Content-focused, editorial |
| `vibrant` | 1.30x | Wide | 0.5 rem | Creative tools, dashboards |

An invalid mode raises `ValueError`:

```python
PaletteGenerator.from_brand_colors("#3b82f6", mode="neon")
# ValueError: Invalid mode 'neon'. Choose from: professional, playful, muted, vibrant
```

### WCAG Contrast Validation

Every generated palette is automatically validated against WCAG AA contrast requirements. For each foreground/background pair (13 text pairs at 4.5:1, plus borders at 3:1), the generator:

1. Calculates the contrast ratio using the WCAG relative luminance formula
2. If the ratio is below the minimum, adjusts the foreground lightness via binary search until it passes
3. Applies this fix to both light and dark mode tokens independently

This means **every palette passes WCAG AA** out of the box, regardless of the input color. Even problematic inputs like very light colors (`#eeeeee`) produce accessible output.

The validated pairs include:
- `foreground` / `background`, `card_foreground` / `card`, `popover_foreground` / `popover`
- `primary_foreground` / `primary`, `secondary_foreground` / `secondary`, `accent_foreground` / `accent`
- `muted_foreground` / `muted`
- `destructive_foreground` / `destructive`, `success_foreground` / `success`, `warning_foreground` / `warning`, `info_foreground` / `info`
- `code_foreground` / `code`, `selection_foreground` / `selection`
- `link` / `background` (links must be readable on the page)
- `border` / `background` (minimum 3:1 for UI components)

### Complete Example

```python
# settings.py or a presets module loaded at startup
from djust_theming import PaletteGenerator
from djust_theming.presets import THEME_PRESETS

# Generate a vibrant palette from Spotify's brand green
spotify_preset = PaletteGenerator.from_brand_colors(
    primary="#1DB954",
    mode="vibrant",
)

# Register it so it appears in the theme switcher and system checks
THEME_PRESETS[spotify_preset.name] = spotify_preset

# You can also inspect the generated tokens
print(spotify_preset.light.primary.to_hex())   # hex value close to #1DB954
print(spotify_preset.dark.primary.to_hex())     # lighter variant for dark mode
print(spotify_preset.radius)                    # 0.5 (vibrant mode default)
```

### How Colors Are Derived

When secondary or accent colors are not provided, the generator derives them from the primary color's hue:

- **Secondary**: Rotated by the mode's `secondary_hue_offset` (e.g., 180 degrees for professional/muted, 150 for playful, 120 for vibrant)
- **Accent**: Rotated by the mode's `accent_hue_offset` (e.g., 30 degrees for professional, 60 for playful)
- Derived colors have their saturation scaled by the mode's `sat_scale` factor

Semantic colors (destructive, success, warning, info) use fixed hues (red, green, amber, blue) with saturation adjusted by the mode, ensuring they are always recognizable.

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

## System Checks Reference

djust-theming registers several Django system checks that run automatically at startup (`runserver`, `migrate`, `check`). These catch common misconfigurations before they cause runtime errors.

### All Checks

| ID | Level | What it catches | How to fix |
|----|-------|-----------------|------------|
| `W001` | Warning | A theme preset has a foreground/background pair with contrast ratio below WCAG AA (4.5:1). Checks 12 token pairs across light and dark modes for every preset in `THEME_PRESETS`. | Adjust the foreground or background `ColorScale` lightness values until the pair achieves at least 4.5:1 contrast. |
| `W002` | Warning | `css_prefix` does not end with `-`. Classes will render as `.prefixbtn` instead of `.prefix-btn`. | Add a trailing hyphen to your prefix, e.g. `"dj-"` instead of `"dj"`. |
| `E001` | Error | `djust_theming.context_processors.theme_context` is missing from all TEMPLATES backends' `context_processors` lists. Template variables like `theme_head`, `theme_switcher`, etc. will not be available. | Add `"djust_theming.context_processors.theme_context"` to `TEMPLATES[0]['OPTIONS']['context_processors']` in your settings. |
| `E002` | Error | `LIVEVIEW_CONFIG['theme']['preset']` is set to a name that does not exist in `THEME_PRESETS`. | Change the preset value to one of the registered preset names (e.g. `"default"`, `"shadcn"`, `"nord"`). Run `python -c "from djust_theming.presets import THEME_PRESETS; print(sorted(THEME_PRESETS))"` to see all valid names. |
| `E003` | Error | `LIVEVIEW_CONFIG['theme']['theme']` is set to a name that does not exist in `DESIGN_SYSTEMS`. | Change the theme value to one of the registered design system names (e.g. `"material"`, `"ios"`, `"fluent"`). Run `python -c "from djust_theming.theme_packs import DESIGN_SYSTEMS; print(sorted(DESIGN_SYSTEMS))"` to see all valid names. |
| `E004` | Error | `css_prefix` contains invalid characters (anything other than letters, digits, and hyphens) or does not start with a letter. This prevents CSS injection and malformed selectors. | Use a prefix containing only ASCII letters, digits, and hyphens, starting with a letter. Example: `"dj-"`, `"myapp-"`. |

### Running Checks

All checks are registered under the `compatibility` tag:

```bash
# Run all system checks
python manage.py check

# Run only djust-theming checks (compatibility tag)
python manage.py check --tag compatibility
```

### Silencing Checks

Use Django's `SILENCED_SYSTEM_CHECKS` setting to suppress specific checks you have reviewed and accepted:

```python
# settings.py
SILENCED_SYSTEM_CHECKS = [
    "djust_theming.W001",  # Silence contrast ratio warnings
    "djust_theming.W002",  # Silence css_prefix hyphen warning
]
```

Errors (`E001`-`E004`) indicate broken configuration that will cause runtime failures. Silence them only if you are certain the check does not apply to your setup.

## Theme Gallery

The theme gallery is a built-in developer tool that renders every component in every variant on a single page. It helps you visually verify your theme customizations, compare presets, and check component rendering across all 24 components.

### Setup

Include the djust-theming URLs in your project's `urls.py`:

```python
# urls.py
from django.urls import include, path

urlpatterns = [
    path("theming/", include("djust_theming.urls")),
    # ...
]
```

The gallery is then available at `/theming/gallery/`.

### Access Control

The gallery is gated for production safety:

- **`DEBUG=True`**: The gallery is accessible to all users without authentication.
- **`DEBUG=False`**: Only users with `request.user.is_staff == True` can access the gallery. All other requests receive a `403 Forbidden` response.

This means the gallery is always available during local development but locked down in production. Staff users (Django admin users) can still access it in production for theme verification.

### Preset Switcher

The gallery includes a preset dropdown at the top of the page. Use the `?preset=<name>` query parameter to switch between color presets (e.g., `/theming/gallery/?preset=nord`). The dropdown submits automatically on change, re-rendering all components with the selected preset's color tokens.

### What the Gallery Shows

The gallery renders every registered component with representative examples:

- **Buttons**: All 5 variants (primary, secondary, destructive, ghost, link) and 3 sizes (sm, md, lg)
- **Alerts**: All 4 variants (default, success, warning, destructive) plus dismissible
- **Badges**: All 5 variants (default, secondary, success, warning, destructive)
- **Tables**: 3 variants (default, striped, hover)
- **Modals**: 3 sizes (sm, md, lg) with trigger buttons
- **Toasts**: 4 variants (success, warning, error, info)
- **Progress bars**: 25%, 50%, 75%, 100%, and indeterminate
- **Skeletons**: 3 shapes (text, circle, rect)
- **Tooltips**: 4 positions (top, bottom, left, right)
- **Avatars**: 3 sizes (sm, md, lg)
- **Forms**: Input, select, textarea, checkbox, radio with sample data
- **Navigation**: Nav, sidebar nav, nav items, nav groups, breadcrumbs
- **Cards, Dropdowns, Tabs, Pagination**: With representative configurations
