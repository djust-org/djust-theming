# Getting Started: Create Your First Theme in 10 Minutes

This tutorial walks through creating a custom theme from scratch, previewing it, and packaging it for distribution. By the end you will have a working theme with custom colors, modified components, and the knowledge to publish it to PyPI.

## Prerequisites

- A Django project with `djust_theming` installed and in `INSTALLED_APPS`
- Python 3.10+

## Step 1: Scaffold a new theme

Run the `create-theme` command to generate a theme directory:

```bash
python manage.py djust_theme create-theme my-theme --preset blue
```

This creates the following structure inside your project:

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

The `theme.toml` manifest records which color preset and design system your theme uses:

```toml
[theme]
name = "my-theme"
version = "0.1.0"
description = "Custom theme: my-theme"

[tokens]
preset = "blue"
design_system = "material"
```

You can change the design system with `--design-system` (options: material, ios, fluent, neo-brutalist, playful, minimalist, corporate, retro, elegant, organic, dense) and extend an existing theme with `--base`.

## Step 2: Override component templates

Copy the default button template into your theme's `components/` directory, then modify it:

```bash
# Copy the default button template
cp .venv/lib/python3.12/site-packages/djust_theming/templates/djust_theming/components/button.html \
   themes/my-theme/components/button.html
```

Edit `themes/my-theme/components/button.html` to customize the markup. For example, add an icon wrapper:

```html
<button class="{{ css_prefix }}btn {{ css_prefix }}btn-{{ variant }} {{ css_prefix }}btn-{{ size }} {% if attrs.class %}{{ attrs.class }}{% endif %}"
        {% if attrs.id %}id="{{ attrs.id }}"{% endif %}
        {% if attrs.type %}type="{{ attrs.type }}"{% endif %}>
    {% if slot_icon %}<span class="btn-icon">{{ slot_icon|safe }}</span> {% endif %}
    {% if slot_content %}{{ slot_content|safe }}{% else %}{{ text }}{% endif %}
</button>
```

Do the same for cards or any other component you want to customize. The template resolution system automatically prefers your overrides over the defaults.

**Important:** Your overrides must satisfy the component contract. Every button template must include a `<button>` element and reference the `{{ text }}` context variable. Run `check-compat` (Step 4b) to verify.

The available components and their contracts are documented in `docs/BREAKING_CHANGES.md`.

## Step 3: Customize design tokens

Edit `themes/my-theme/tokens.css` to override CSS custom properties. These apply after the preset tokens, so you only need to specify what you want to change:

```css
:root {
    /* Brand colors (HSL values without hsl() wrapper) */
    --primary: 220 90% 56%;
    --primary-foreground: 0 0% 100%;

    /* Border radius */
    --radius: 0.75rem;

    /* Custom accent */
    --accent: 280 60% 50%;
    --accent-foreground: 0 0% 100%;
}
```

Every token from the preset can be overridden. Common tokens to customize:

| Token | Description | Example |
|-------|-------------|---------|
| `--primary` | Primary brand color | `220 90% 56%` |
| `--secondary` | Secondary color | `210 40% 96%` |
| `--accent` | Accent color | `280 60% 50%` |
| `--background` | Page background | `0 0% 100%` |
| `--foreground` | Default text color | `222 47% 11%` |
| `--radius` | Border radius | `0.75rem` |
| `--ring` | Focus ring color | `220 90% 56%` |

## Step 4: Preview your theme

### 4a. Use the gallery

Start your development server and visit the theme gallery to see every component rendered with your theme:

```
http://localhost:8000/theming/gallery/
```

Use the preset selector at the top to switch between presets. If you have configured your theme in `LIVEVIEW_CONFIG`, it will be active automatically.

For real-time token tweaking without editing files, use the live editor:

```
http://localhost:8000/theming/gallery/editor/
```

The editor lets you adjust colors and radius with visual controls and export the result as `tokens.css`.

### 4b. Validate your theme

Run validation to check your manifest and file references:

```bash
python manage.py djust_theme validate-theme my-theme
```

Run the compatibility checker to verify your template overrides match the component contracts:

```bash
python manage.py djust_theme check-compat my-theme
```

This reports:
- **ERROR** if a required element is missing (e.g., button.html without `<button>`)
- **ERROR** if a required context variable is not referenced (e.g., button.html without `{{ text }}`)
- **WARNING** if a template file has no matching contract
- **INFO** if an optional slot is not used

Fix any errors before publishing.

## Step 5: Package and publish

### 5a. Generate a package scaffold

```bash
python manage.py djust_theme create-package my-theme \
    --author "Your Name" \
    --preset blue
```

This creates a complete pip-installable package:

```
djust-theme-my-theme/
    pyproject.toml
    README.md
    LICENSE
    djust_theme_my_theme/
        __init__.py
        theme.toml
        tokens.css
        templates/
        static/
```

Copy your customized files from `themes/my-theme/` into the package:

```bash
cp themes/my-theme/tokens.css djust-theme-my-theme/djust_theme_my_theme/tokens.css
cp themes/my-theme/components/*.html \
   djust-theme-my-theme/djust_theme_my_theme/templates/djust_theming/themes/my-theme/components/
```

### 5b. Test locally

```bash
cd djust-theme-my-theme
pip install -e .
```

Add the package to your project settings:

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

Verify everything works with `validate-theme` and `check-compat`.

### 5c. Publish to PyPI

```bash
pip install build twine
python -m build
twine upload dist/*
```

Your theme is now installable by anyone:

```bash
pip install djust-theme-my-theme
```

## Next steps

- **Theme Authoring Guide** (`docs/theme-authoring.md`) -- detailed reference for all theme features
- **Customization Tools** (`docs/customization.md`) -- gallery, live editor, and diff view
- **Component Contracts** (`docs/BREAKING_CHANGES.md`) -- contract reference and migration tracking
- **Accessibility** (`docs/accessibility.md`) -- a11y requirements for theme overrides
