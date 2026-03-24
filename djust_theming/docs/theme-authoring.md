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

## Creating Installable Theme Packages

You can distribute themes as pip-installable Python packages. This is the recommended approach for sharing themes with the community or across multiple projects.

### Package Structure

```
djust-theme-nord/
  pyproject.toml
  djust_theme_nord/
    __init__.py            # Exposes get_theme_manifest(), PRESETS, DESIGN_SYSTEMS
    templates/
      djust_theming/
        themes/
          nord/
            components/
              button.html  # Theme-specific component templates
              card.html
    static/
      djust_theming/
        themes/
          nord/
            tokens.css     # Custom token overrides
```

### `__init__.py` Conventions

Your package must expose one or more of these module-level attributes:

```python
# djust_theme_nord/__init__.py
from pathlib import Path
from djust_theming.manifest import ThemeManifest

def get_theme_manifest():
    """Return the theme manifest for this package."""
    return ThemeManifest(
        name="nord",
        version="1.0.0",
        description="Nord color palette theme for djust-theming",
        author="Your Name",
        license="MIT",
        preset="default",
        design_system="material",
        path=Path(__file__).parent,
    )

# Optional: export custom presets
PRESETS = {
    "nord-frost": ThemePreset(...),
    "nord-aurora": ThemePreset(...),
}

# Optional: export custom design systems
DESIGN_SYSTEMS = {
    "nord-ds": DesignSystem(...),
}
```

The registry calls `get_theme_manifest()` and automatically detects the `templates/` directory inside your package. You do not need to set `templates_dir` manually -- the registry detects it by looking for a `templates/` subdirectory next to your `__init__.py`.

### `pyproject.toml`

```toml
[project]
name = "djust-theme-nord"
version = "1.0.0"
description = "Nord theme for djust-theming"
dependencies = ["djust-theming>=0.3.0"]

[tool.setuptools.packages.find]
include = ["djust_theme_nord*"]

[tool.setuptools.package-data]
djust_theme_nord = [
    "templates/**/*.html",
    "static/**/*.css",
    "static/**/*.woff2",
]
```

### Installing a Theme Package

```bash
pip install djust-theme-nord
```

Then add it to your Django settings:

```python
# settings.py
DJUST_THEMES = [
    "djust_theme_nord",
]
```

The registry discovers the package at startup and registers its manifest, presets, and design systems. Templates from the package are available through `ThemePackageLoader`.

### Template Loading for Packages

To use templates from installed theme packages, add `ThemePackageLoader` to your template loaders:

```python
# settings.py
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "OPTIONS": {
        "loaders": [
            "djust_theming.loaders.ThemePackageLoader",
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    },
}]
```

`ThemePackageLoader` queries the registry for all manifests that have a `templates_dir` and makes those directories available to Django's template engine. This means `{% theme_button %}` can resolve to a template shipped inside a pip package.

### Publishing

1. Build the package: `python -m build`
2. Upload to PyPI: `twine upload dist/*`
3. Users install with `pip install djust-theme-nord` and add the package name to `DJUST_THEMES`

## Theme Registry

All presets, design systems, and manifests are managed through the **Theme Registry** -- a thread-safe singleton that acts as the single source of truth at runtime. The registry is populated automatically during Django startup (`AppConfig.ready()`).

### How Discovery Works

When your Django app starts, the registry loads data from four sources in order:

1. **Built-in presets** -- All 19 presets from `THEME_PRESETS` (default, blue, green, purple, etc.)
2. **Built-in design systems** -- All 11 design systems from `DESIGN_SYSTEMS` (material, ios, fluent, etc.)
3. **`DJUST_THEMES` setting** -- pip-installed theme packages listed in your Django settings
4. **`themes/` directory** -- `theme.toml` manifests discovered by scanning the configured themes directory

You do not need to call any registration functions for built-in themes or themes in your `themes/` directory. They are registered automatically.

### Querying the Registry

```python
from djust_theming.registry import get_registry

registry = get_registry()

# Check if a preset exists
registry.has_preset("blue")        # True
registry.has_preset("nonexistent") # False

# Get a preset (returns None if missing)
preset = registry.get_preset("blue")

# List all registered presets
for name, preset in registry.list_presets().items():
    print(f"{name}: {preset.display_name}")

# Same API for design systems
registry.has_theme("material")
registry.get_theme("ios")
registry.list_themes()

# Theme manifests (from theme.toml files)
registry.get_manifest("my-brand")
registry.list_manifests()
```

### Installing Third-Party Theme Packages

Add pip-installed theme packages to the `DJUST_THEMES` setting:

```python
# settings.py
DJUST_THEMES = [
    "djust_theme_nord",      # hypothetical pip package
    "djust_theme_catppuccin",
]
```

Each package should expose one or more of these by convention:

- `get_theme_manifest()` -- returns a `ThemeManifest` instance
- `PRESETS` -- dict of `{name: ThemePreset}`
- `DESIGN_SYSTEMS` -- dict of `{name: DesignSystem}`

## Validating Themes

Use the `validate-theme` management command to check a theme manifest for errors and warnings before deploying.

### Usage

```bash
# Validate a single theme
python manage.py djust_theme validate-theme my-brand

# Validate all themes in the themes directory
python manage.py djust_theme validate-theme --all

# Validate themes in a custom directory
python manage.py djust_theme validate-theme my-brand --dir=/path/to/themes
python manage.py djust_theme validate-theme --all --dir=/path/to/themes
```

### What Gets Checked

The validator runs these checks:

| Check | Severity | Description |
|-------|----------|-------------|
| TOML parse | Error | `theme.toml` must be valid TOML |
| `[theme].name` | Error | Must be present |
| `[theme].version` | Error | Must be present |
| Name format | Error | Must match `[a-z0-9][a-z0-9-]*` |
| Preset exists | Error | `[tokens].preset` must be a registered preset |
| Design system exists | Error | `[tokens].design_system` must be a registered design system |
| Static CSS files | Warning | Referenced CSS files in `[static].css` must exist on disk |
| Static font files | Warning | Referenced font files in `[static].fonts` must exist on disk |
| Override keys | Warning | Keys in `[tokens.overrides]` must match `ThemeTokens` field names |

### Example Output

```
Validating theme: my-brand
----------------------------------------
  PASS: All checks passed.
```

```
Validating theme: broken-theme
----------------------------------------
  ERROR: Unknown preset 'nonexistent'. Valid presets: blue, default, ...
  WARNING: Static CSS file not found: static/css/missing.css
  WARNING: Unknown override key 'nonexistent_token' -- not a ThemeTokens field.
  PASS: Valid (with 2 warning(s)).
```
