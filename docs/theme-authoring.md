# Theme Authoring Guide

This guide covers the full workflow for creating, developing, and publishing djust-theming themes.

## Two ways to create a theme

djust-theming supports two kinds of themes:

1. **Local themes** -- directories inside your project's `themes/` folder. Good for project-specific customization.
2. **Theme packages** -- pip-installable Python packages. Good for sharing themes across projects or publishing to PyPI.

Both use the same `theme.toml` manifest and the same template/token override system. The difference is packaging and distribution.

## Creating a local theme

Use the `create-theme` subcommand to scaffold a theme directory inside your project:

```bash
python manage.py djust_theme create-theme my-theme \
    --preset blue \
    --design-system material
```

This creates:

```
themes/my-theme/
    theme.toml          # manifest (name, preset, design system)
    tokens.css          # CSS custom property overrides
    components/         # component template overrides
    layouts/            # layout template overrides
    pages/              # page template overrides
    static/css/         # additional stylesheets
    static/fonts/       # custom web fonts
```

Options:

| Flag | Default | Description |
|------|---------|-------------|
| `--preset` | `default` | Color preset from `THEME_PRESETS` |
| `--design-system` | `material` | Design system from `DESIGN_SYSTEMS` |
| `--base` | (none) | Base theme to extend |
| `--dir` | `BASE_DIR/themes/` | Override themes directory |
| `--force` | off | Overwrite existing theme directory |

## Creating a theme package

Use the `create-package` subcommand to generate a pip-installable Python package:

```bash
python manage.py djust_theme create-package my-theme \
    --author "Jane Doe" \
    --preset blue \
    --design-system material
```

This creates a complete Python package ready for development and publishing:

```
djust-theme-my-theme/
    pyproject.toml              # build metadata (setuptools)
    README.md                   # installation instructions
    LICENSE                     # MIT license
    djust_theme_my_theme/
        __init__.py             # package marker
        theme.toml              # theme manifest
        tokens.css              # CSS custom property overrides
        templates/              # component template overrides
            djust_theming/themes/my-theme/components/
        static/                 # CSS and font assets
            djust_theme_my_theme/css/
            djust_theme_my_theme/fonts/
```

Options:

| Flag | Default | Description |
|------|---------|-------------|
| `--author` | `"Theme Author"` | Author name for pyproject.toml |
| `--preset` | `default` | Color preset from `THEME_PRESETS` |
| `--design-system` | `material` | Design system from `DESIGN_SYSTEMS` |
| `--dir` | current directory | Output directory for the package |
| `--force` | off | Overwrite existing package directory |

## Developing your theme

### Customizing tokens

Edit `tokens.css` to override CSS custom properties. These are applied after the preset tokens, so you only need to specify what you want to change:

```css
:root {
    --primary: 220 90% 56%;
    --radius: 0.75rem;
}
```

### Overriding component templates

Place HTML templates in the `components/` directory (local themes) or `templates/djust_theming/themes/<name>/components/` (packages). The template resolution system will prefer your overrides over the defaults.

For example, to customize the button component, create `components/button.html` with your own markup. Use the same context variables as the default template (`css_prefix`, `variant`, `size`, `text`, `slot_content`).

### Adding static assets

Place CSS files in `static/css/` and fonts in `static/fonts/`. Reference them in your `theme.toml` under the `[static]` section:

```toml
[static]
css = ["static/css/custom.css"]
fonts = ["static/fonts/MyFont.woff2"]
```

## Validating your theme

Run the validation command to check your theme manifest and file references:

```bash
# Validate a specific theme
python manage.py djust_theme validate-theme my-theme

# Validate all themes
python manage.py djust_theme validate-theme --all
```

## Publishing a theme package to PyPI

Once your theme package is ready:

### 1. Install the package locally for testing

```bash
cd djust-theme-my-theme
pip install -e .
```

### 2. Add it to your Django project

```python
# settings.py
INSTALLED_APPS = [
    ...
    "djust_theming",
    "djust_theme_my_theme",
]

LIVEVIEW_CONFIG = {
    "theme": {
        "packages": ["djust-theme-my-theme"],
    }
}
```

### 3. Verify it works

Start your development server and confirm the theme loads correctly. Component templates from your package should take priority when the theme is active.

### 4. Build and publish

```bash
pip install build twine

python -m build
twine upload dist/*
```

Your theme will be available for anyone to install with:

```bash
pip install djust-theme-my-theme
```

## Workflow summary

| Step | Local theme | Theme package |
|------|-------------|---------------|
| **Create** | `djust_theme create-theme` | `djust_theme create-package` |
| **Develop** | Edit files in `themes/` | Edit files in package dir |
| **Test** | `djust_theme validate-theme` | `pip install -e .` + validate |
| **Share** | Copy directory | `python -m build && twine upload dist/*` |
