# djust-theming Example Project

A complete Django application demonstrating all features of djust-theming (Phases 1-9).

## Features Demonstrated

- 24 theme-aware components (button, card, badge, alert, input, select, textarea, checkbox, radio, modal, dropdown, tabs, table, pagination, breadcrumb, avatar, toast, progress, skeleton, tooltip, nav, sidebar nav, nav item, nav group)
- 19 color presets (Default, Shadcn, Blue, Green, Purple, Orange, Rose, Natural20, Catppuccin, Rose Pine, Tokyo Night, Nord, Synthwave, Cyberpunk, Outrun, Forest, Amber, Slate, Nebula)
- 11 design systems (Material, iOS, Fluent, Minimalist, Playful, Corporate, Retro, Elegant, Neo-Brutalist, Organic, Dense)
- 6 layout templates (Topbar, Sidebar, Sidebar+Topbar, Centered, Dashboard, Split)
- 8+ page templates (Login, Register, Password Reset, Password Confirm, 404, 403, 500, Maintenance, Empty State)
- Django form integration (stacked, horizontal, inline layouts with themed error display)
- Theme packs (bundled design system + color + icon + animation + pattern combos)
- Light/Dark/System mode switching
- Tailwind CSS integration and shadcn/ui compatibility
- Built-in gallery, storybook, editor, and diff tools (via `/theming/gallery/`)
- Theme inspector with real-time CSS generation
- Critical CSS splitting and deferred CSS loading
- CSS prefix isolation support
- CSS cascade layers support
- RTL direction support

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

## Pages

| URL | Page | Features |
|-----|------|----------|
| `/` | Homepage | Feature overview, architecture guide, quick start |
| `/components/` | Component Library | All 24 components with live demos and code snippets |
| `/forms/` | Form Integration | Django form rendering with 3 layouts and error display |
| `/layouts/` | Layout Templates | 6 layout templates with visual previews and block reference |
| `/pages/` | Page Templates | Auth, error, and utility page fragments |
| `/design-systems/` | Design Systems | 11 design systems with live preview and color mixing |
| `/presets/` | Color Presets | 19 color palettes with light/dark previews |
| `/packs/` | Theme Packs | Complete theme bundles with all style dimensions |
| `/inspector/` | Theme Inspector | Debug theme combinations, view generated CSS |
| `/tailwind/` | Tailwind Integration | Config generation, theme color utilities, @apply examples |
| `/theming/gallery/` | Gallery | Visual theme browser (built-in) |
| `/theming/gallery/storybook/` | Storybook | Component isolation testing (built-in) |
| `/theming/gallery/editor/` | Editor | Live theme customization (built-in) |
| `/theming/gallery/diff/` | Diff | Compare theme CSS output (built-in) |

## Project Structure

```
example_project/
├── manage.py
├── requirements.txt
├── example_project/
│   ├── settings.py              # LIVEVIEW_CONFIG with all theme settings
│   ├── urls.py                  # Includes djust_theming.urls at /theming/
│   └── wsgi.py
└── theme_demo/
    ├── views.py                 # Demo views for all features
    ├── urls.py                  # App URLs (13 routes)
    └── templates/theme_demo/
        ├── base.html            # Base template with full navigation
        ├── index.html           # Homepage with feature overview
        ├── components.html      # All 24 components showcase
        ├── forms.html           # Django form integration demo
        ├── layouts.html         # Layout template showcase
        ├── pages.html           # Page template demos
        ├── presets.html         # 19 color presets gallery
        ├── design_systems.html  # 11 design systems with mixer
        ├── packs.html           # Theme packs gallery
        ├── themes.html          # Legacy theme switcher
        ├── inspector.html       # Theme inspector tool
        └── tailwind.html        # Tailwind integration demo
```

## Template Tag Libraries

```django
{% load theme_tags %}         {# theme_head, theme_switcher, theme_mode_toggle, theme_preset_selector #}
{% load theme_components %}   {# 24 UI components #}
{% load theme_form_tags %}    {# theme_form, theme_form_errors, get_css_prefix #}
{% load theme_pages %}        {# auth, error, and utility page fragments #}
```

## Configuration

All settings in `example_project/settings.py`:

```python
LIVEVIEW_CONFIG = {
    'theme': {
        'preset': 'blue',          # Any of 19 presets
        'default_mode': 'system',  # light, dark, or system
        'persist_in_session': True,
        'enable_dark_mode': True,
        'css_prefix': '',          # CSS class prefix for isolation
        'critical_css': True,      # Split into critical/deferred CSS
        'use_css_layers': False,   # Enable CSS cascade layers
        'direction': 'ltr',       # Text direction: ltr or rtl
        'themes_dir': '',          # Custom themes directory
    }
}
```

## CLI Commands

```bash
python manage.py djust_theme list-presets          # List all 19 presets
python manage.py djust_theme tailwind-config       # Generate Tailwind config
python manage.py djust_theme shadcn-import theme.json  # Import shadcn theme
python manage.py djust_theme shadcn-export --preset blue  # Export to shadcn format
python manage.py djust_theme export-colors --preset blue  # Export color tokens
python manage.py djust_theme generate-examples     # Generate @apply CSS examples
```

## License

MIT - Same as djust-theming
