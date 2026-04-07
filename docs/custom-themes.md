# Custom Themes

Register your own color presets, design systems, and theme packs so they appear in `{% theme_panel %}` alongside the built-in themes.

## Quick Start

Add a custom color preset in your app's `apps.py`:

```python
# myapp/apps.py
from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = "myapp"

    def ready(self):
        from djust_theming import register_preset
        from djust_theming.presets import ThemePreset, ThemeTokens

        register_preset("brand", ThemePreset(
            name="brand",
            display_name="My Brand",
            description="Custom brand colors",
            light=ThemeTokens(
                background="0 0% 100%",
                foreground="222 47% 11%",
                primary="221 83% 53%",
                primary_foreground="210 40% 98%",
                secondary="210 40% 96%",
                secondary_foreground="222 47% 11%",
                muted="210 40% 96%",
                muted_foreground="215 16% 47%",
                accent="210 40% 96%",
                accent_foreground="222 47% 11%",
                destructive="0 84% 60%",
                destructive_foreground="210 40% 98%",
                border="214 32% 91%",
                input="214 32% 91%",
                ring="221 83% 53%",
                card="0 0% 100%",
                card_foreground="222 47% 11%",
            ),
            dark=ThemeTokens(
                background="222 47% 11%",
                foreground="210 40% 98%",
                primary="217 91% 60%",
                primary_foreground="222 47% 11%",
                # ... remaining dark tokens
            ),
        ))
```

The preset immediately appears in the theme panel's Color dropdown and can be selected by users.

## Registration API

All registration functions should be called in `AppConfig.ready()` to ensure they run after Django initializes but before the first request.

### `register_preset(name, preset)`

Register a custom color preset (color palette with light/dark modes).

```python
from djust_theming import register_preset
from djust_theming.presets import ThemePreset, ThemeTokens

register_preset("ocean", ThemePreset(
    name="ocean",
    display_name="Ocean Blue",
    description="Deep blue oceanic palette",
    light=ThemeTokens(primary="200 80% 50%", ...),
    dark=ThemeTokens(primary="200 80% 65%", ...),
))
```

**Required `ThemeTokens` fields:** `background`, `foreground`, `primary`, `primary_foreground`, `secondary`, `secondary_foreground`, `muted`, `muted_foreground`, `accent`, `accent_foreground`, `destructive`, `destructive_foreground`, `border`, `input`, `ring`, `card`, `card_foreground`.

All values are HSL strings without the `hsl()` wrapper (e.g., `"220 90% 56%"`).

### `register_design_system(name, design_system)`

Register a custom design system (typography, spacing, shapes — no colors).

```python
from djust_theming import register_design_system
from djust_theming.theme_packs import (
    DesignSystem, TypographyStyle, LayoutStyle,
    SurfaceStyle, IconStyleConfig, AnimationConfig, InteractionConfig,
)

register_design_system("compact", DesignSystem(
    name="compact",
    display_name="Compact",
    typography=TypographyStyle(
        name="compact",
        heading_font="Inter",
        body_font="Inter",
        base_size="14px",
        heading_weight="600",
    ),
    layout=LayoutStyle(
        name="compact",
        border_radius_sm="0.125rem",
        border_radius_md="0.25rem",
        border_radius_lg="0.5rem",
        button_shape="rounded",
    ),
    surface=SurfaceStyle(name="compact"),
    icons=IconStyleConfig(name="compact"),
    animation=AnimationConfig(name="compact"),
    interaction=InteractionConfig(name="compact"),
))
```

### `register_theme_pack(name, pack)`

Register a complete theme pack that bundles a design system + color preset.

```python
from djust_theming import register_theme_pack
from djust_theming.theme_packs import (
    ThemePack, IconStyle, AnimationStyle, PatternStyle,
    InteractionStyle, IllustrationStyle,
)

register_theme_pack("my_brand", ThemePack(
    name="my_brand",
    display_name="My Brand",
    description="Complete brand experience",
    category="professional",
    design_theme="compact",      # references registered design system
    color_preset="ocean",        # references registered color preset
    icon_style=IconStyle(name="my_brand", style="outline", weight="1.5"),
    animation_style=AnimationStyle(name="my_brand"),
    pattern_style=PatternStyle(name="my_brand"),
    interaction_style=InteractionStyle(name="my_brand"),
    illustration_style=IllustrationStyle(name="my_brand"),
))
```

Theme packs appear in the theme panel's Theme dropdown.

## Pip-Installable Theme Packages

You can distribute themes as pip packages. The registry auto-discovers them via the `DJUST_THEMES` setting:

```python
# settings.py
DJUST_THEMES = ["my_theme_package"]
```

Your package should expose one or more of:

```python
# my_theme_package/__init__.py
from djust_theming.presets import ThemePreset, ThemeTokens

PRESETS = {
    "my_preset": ThemePreset(...),
}

DESIGN_SYSTEMS = {
    "my_design": DesignSystem(...),
}

THEME_PACKS = {
    "my_pack": ThemePack(...),
}
```

## Overriding Built-in Themes

Register with the same name as a built-in to override it:

```python
# Override the default "blue" preset with your brand's blue
register_preset("blue", ThemePreset(
    name="blue",
    display_name="Brand Blue",
    light=ThemeTokens(primary="210 100% 45%", ...),
    dark=ThemeTokens(primary="210 100% 60%", ...),
))
```

## Using with `{% theme_panel %}`

Registered themes automatically appear in the theme panel — no template changes needed:

```html
{% load theme_tags %}
{% theme_panel %}
```
