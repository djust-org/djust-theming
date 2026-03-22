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
