# djust-theming Example Project

A complete Django application demonstrating all features of djust-theming.

## Features Demonstrated

- ✅ All 7 theme presets (Default, Shadcn, Blue, Green, Purple, Orange, Rose)
- ✅ Light/Dark/System mode switching
- ✅ Component library (Buttons, Cards, Badges, Alerts, Inputs)
- ✅ Tailwind CSS integration
- ✅ shadcn/ui compatibility
- ✅ Reactive theme switching (with djust LiveView - optional)

## Quick Start

### 1. Install Dependencies

```bash
cd example_project
pip install -r requirements.txt
```

### 2. Run the Development Server

```bash
python manage.py runserver
```

### 3. Open in Browser

Visit http://localhost:8000

## Project Structure

```
example_project/
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── example_project/
│   ├── settings.py             # Project settings
│   ├── urls.py                 # URL configuration
│   └── wsgi.py                 # WSGI application
└── theme_demo/
    ├── views.py                # Demo views
    ├── urls.py                 # App URLs
    └── templates/
        └── theme_demo/
            ├── base.html       # Base template with navigation
            ├── index.html      # Homepage
            ├── components.html # Component showcase
            ├── presets.html    # Preset gallery
            └── tailwind.html   # Tailwind integration demo
```

## Pages

### Homepage (`/`)
- Overview of djust-theming features
- Feature grid with all capabilities
- Quick start guide
- Try it now section

### Components (`/components/`)
- Complete component library showcase
- Buttons (5 variants, 3 sizes)
- Badges (6 variants)
- Alerts (4 variants with dismissal)
- Form inputs with labels
- Cards with headers and footers

### Presets (`/presets/`)
- Gallery of all 7 built-in presets
- Light and dark mode color previews
- shadcn/ui import/export instructions
- Current preset indicator

### Tailwind Integration (`/tailwind/`)
- Config generation instructions
- Theme color utilities showcase
- Background, border, and text colors
- Opacity modifiers
- @apply directive examples

## Customization

### Change Default Preset

Edit `example_project/settings.py`:

```python
LIVEVIEW_CONFIG = {
    'theme': {
        'preset': 'purple',  # Change to: default, shadcn, blue, green, purple, orange, rose
        'default_mode': 'dark',  # Change to: light, dark, system
    }
}
```

### Add Custom Components

1. Create a new component template in `djust_theming/templates/djust_theming/components/`
2. Add a template tag in `djust_theming/templatetags/theme_components.py`
3. Use it in your templates: `{% my_component %}`

### Import shadcn Theme

```bash
# Download a theme from themes.shadcn.com
python manage.py djust_theme shadcn-import path/to/theme.json --register
```

## djust LiveView Integration (Optional)

To enable reactive theme switching without page reload:

1. Install djust:
   ```bash
   pip install djust
   ```

2. Add to `INSTALLED_APPS` in settings.py:
   ```python
   INSTALLED_APPS = [
       'channels',
       'djust',
       ...
   ]
   ```

3. Create a LiveView version of the demo

See the main [djust-theming README](../README.md) for full LiveView integration guide.

## CLI Commands

Generate Tailwind config:
```bash
python manage.py djust_theme tailwind-config --preset blue
```

Export colors:
```bash
python manage.py djust_theme export-colors --preset blue --format json
```

List presets:
```bash
python manage.py djust_theme list-presets
```

Generate @apply examples:
```bash
python manage.py djust_theme generate-examples
```

## Troubleshooting

### Theme switcher not working
- Ensure `djust_theming` is in `INSTALLED_APPS`
- Check that `theme_context` processor is added to `TEMPLATES` settings
- Verify `{{ theme_head }}` is in your template's `<head>`

### Components not rendering
- Make sure you load template tags: `{% load theme_components %}`
- Check that `djust_theming` templates are accessible

### Tailwind colors not working
- Run `djust-theme tailwind-config` to generate config
- Ensure the config is in your project root
- Restart your Tailwind build process

## Learn More

- [djust-theming Documentation](../README.md)
- [djust LiveView](https://djust.org)
- [shadcn/ui](https://ui.shadcn.com)
- [Tailwind CSS](https://tailwindcss.com)

## License

MIT - Same as djust-theming
