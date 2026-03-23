# Theme Authoring Guide

This guide explains how to create, configure, and distribute custom themes for djust-theming.

## Quick Start

Scaffold a new theme with the management command:

```bash
python manage.py djust_theme create-theme my-brand
```

This creates the following directory structure under your project's `themes/` directory:

```
themes/
  my-brand/
    theme.toml        # Theme manifest (name, preset, design system)
    tokens.css        # CSS custom property overrides
    components/       # Component template overrides
    layouts/          # Layout template overrides
    pages/            # Page template overrides
    static/
      css/            # Additional stylesheets
      fonts/          # Custom web fonts
```

## Theme Manifest (`theme.toml`)

Every theme requires a `theme.toml` manifest file. This is the single source of truth for theme metadata and configuration.

### Full Example

```toml
[theme]
name = "my-brand"
version = "0.1.0"
description = "Corporate brand theme"
author = "Your Name"
license = "MIT"

[extends]
base = "default"

[tokens]
preset = "blue"
design_system = "material"

[tokens.overrides]
primary = "220 90% 56%"
radius = "0.75"

[static]
css = ["static/css/custom.css"]
fonts = ["static/fonts/inter.woff2"]
```

### Section Reference

#### `[theme]` (required)

| Field         | Required | Description                              |
|---------------|----------|------------------------------------------|
| `name`        | Yes      | Theme directory name. Lowercase letters, digits, and hyphens only (`[a-z0-9-]`). Must start with a letter or digit. |
| `version`     | Yes      | Semantic version string (e.g. `"0.1.0"`) |
| `description` | No       | Short description of the theme           |
| `author`      | No       | Theme author name                        |
| `license`     | No       | License identifier (e.g. `"MIT"`)        |

#### `[extends]` (optional)

| Field  | Description                                              |
|--------|----------------------------------------------------------|
| `base` | Name of another theme to extend. The child theme inherits templates and tokens from the base, then applies its own overrides on top. |

#### `[tokens]` (optional)

| Field           | Default      | Description                                    |
|-----------------|--------------|------------------------------------------------|
| `preset`        | `"default"`  | Color preset from `THEME_PRESETS`. Run `python manage.py djust_theme list-presets` to see all available presets. |
| `design_system` | `"material"` | Design system from `DESIGN_SYSTEMS`. Available: `material`, `ios`, `fluent`, `ant`, `carbon`, `chakra`, `mantine`, `spectrum`, `polaris`, `lightning`, `evergreen`. |

#### `[tokens.overrides]` (optional)

Key-value pairs of CSS custom property overrides. These are applied after the preset tokens, allowing you to tweak individual values:

```toml
[tokens.overrides]
primary = "220 90% 56%"
secondary = "180 60% 45%"
radius = "0.5rem"
```

Values use HSL space-separated format (hue saturation% lightness%) for color tokens.

#### `[static]` (optional)

| Field  | Description                                              |
|--------|----------------------------------------------------------|
| `css`  | List of additional CSS files to include                  |
| `fonts`| List of font files bundled with the theme                |

Paths are relative to the theme directory.

## Scaffold Command Reference

```
python manage.py djust_theme create-theme <name> [options]
```

### Arguments

| Argument | Description                                               |
|----------|-----------------------------------------------------------|
| `name`   | Theme directory name (lowercase letters, digits, hyphens) |

### Options

| Option              | Default      | Description                              |
|---------------------|--------------|------------------------------------------|
| `--preset`          | `default`    | Color preset to use in the manifest      |
| `--design-system`   | `material`   | Design system to use in the manifest     |
| `--base`            | (none)       | Base theme to extend                     |
| `--dir`             | (from config)| Override the themes directory path        |
| `--force`           | `false`      | Overwrite an existing theme directory     |

### Examples

```bash
# Basic theme with defaults
python manage.py djust_theme create-theme my-brand

# Theme with a specific preset and design system
python manage.py djust_theme create-theme corporate \
    --preset=blue --design-system=fluent

# Theme that extends another theme
python manage.py djust_theme create-theme dark-corporate --base=corporate

# Scaffold into a custom directory
python manage.py djust_theme create-theme my-theme --dir=/path/to/themes

# Overwrite an existing theme
python manage.py djust_theme create-theme my-theme --force
```

## Theme Name Rules

Theme names must match the pattern `[a-z0-9][a-z0-9-]*`:

- Only lowercase ASCII letters, digits, and hyphens
- Must start with a letter or digit (not a hyphen)
- No spaces, underscores, dots, or special characters

Valid: `my-theme`, `brand2024`, `dark-mode`
Invalid: `My Theme`, `my_theme`, `../etc`, `-leading-hyphen`

This constraint prevents path traversal attacks and ensures theme names are safe for use as directory names and CSS identifiers.

## Themes Directory Configuration

By default, themes live in `BASE_DIR/themes/`. You can change this in your Django settings:

```python
LIVEVIEW_CONFIG = {
    "theme": {
        "themes_dir": "custom-themes/",  # Relative to BASE_DIR
    }
}
```

Or override per-command with `--dir`.

## Loading Themes Programmatically

Use `ThemeManifest` to parse and validate themes in Python:

```python
from pathlib import Path
from djust_theming.manifest import ThemeManifest, load_theme_manifests

# Parse a single theme
manifest = ThemeManifest.from_toml(Path("themes/my-brand/theme.toml"))
print(manifest.name)       # "my-brand"
print(manifest.preset)     # "blue"

# Validate
errors = manifest.validate()
if errors:
    for err in errors:
        print(f"Error: {err}")

# Discover all themes in a directory
manifests = load_theme_manifests(Path("themes/"))
for m in manifests:
    print(f"{m.name} v{m.version} (preset: {m.preset})")

# Serialize back to TOML
toml_string = manifest.to_toml()
```

## Customizing Tokens

After scaffolding, edit `tokens.css` to override CSS custom properties:

```css
/* themes/my-brand/tokens.css */
:root {
    --primary: 220 90% 56%;
    --primary-foreground: 0 0% 100%;
    --radius: 0.75rem;
}

.dark {
    --primary: 220 80% 65%;
}
```

These overrides are applied after the preset tokens, so you only need to specify the values you want to change.

## Overriding Component Templates

Place template files in the `components/`, `layouts/`, or `pages/` subdirectories to override the defaults:

```
themes/my-brand/
  components/
    button.html       # Custom button template
    card.html         # Custom card template
  layouts/
    base.html         # Custom base layout
```

See the [Customization Guide](customization.md) for details on template resolution order.

## Distributing Themes

A theme is a self-contained directory. To share it:

1. Ensure `theme.toml` is complete (name, version, description, author, license)
2. Include all static assets (CSS, fonts) in the `static/` subdirectory
3. Package the entire theme directory

Recipients can drop the directory into their `themes/` folder and it will be discovered automatically by `load_theme_manifests()`.
