# djust-theming

<p align="center">
  <strong>A production-ready theming system for Django</strong>
</p>

<p align="center">
  shadcn/ui-inspired • Reactive • Tailwind-ready • Component Library
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> •
  <a href="#features">Features</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#license">License</a>
</p>

---

A **shadcn/ui-inspired theming system** for Django. Provides CSS custom properties-based theming with light/dark mode support, multiple color presets, and seamless Django template integration.

Works standalone with any Django project, or integrates deeply with [djust](https://djust.org) LiveViews for reactive theme switching.

## Features

### Core Theming
- 🎨 **7 built-in presets**: Default, Shadcn, Blue, Green, Purple, Orange, Rose
- 🌓 **Light/Dark/System mode** with anti-FOUC (Flash of Unstyled Content) protection
- 📦 **Context processor** for template variable injection
- 💾 **Session + localStorage persistence**
- 🍪 **Cookie-based preset** for server-side rendering

### djust LiveView Integration (v0.2.0)
- 🔌 **LiveView mixin** for reactive theme switching
- ⚡ **No page reload** - instant theme changes via WebSocket
- 🔄 **Server-side state sync** - themes persist across sessions
- 🎯 **Compatible with djust-experimental**

### Tailwind CSS Support (v0.3.0)
- 🎨 **Generate tailwind.config.js** with theme CSS variables
- 🎯 **Use theme colors in Tailwind** classes (`bg-primary`, `text-accent`, etc.)
- 📝 **@apply support** for custom CSS components
- 🔄 **Export colors** in JSON/Python formats

### shadcn/ui Compatibility (v0.4.0)
- 🔄 **Import/Export** shadcn theme JSON
- 🌐 **100% compatible** with themes.shadcn.com
- 📦 **Round-trip** import/export without data loss
- 🎨 **Share themes** with the shadcn community

### Component Library (v0.5.0)
- 🧩 **Ready-to-use components**: Button, Card, Badge, Alert, Input
- 🎨 **Automatically themed** - adapt to your preset and mode
- ♿ **Accessible** and responsive
- 🔌 **Template tags** for easy integration

### Powerful CLI (v0.6.0)
- 🚀 **Quick setup** with `djust-theme init`
- 🎨 **Generate configs** for Tailwind, shadcn, examples
- 📋 **List presets**, export colors, import themes
- 💡 **Interactive** with helpful error messages

## Quick Start

### Option 1: Try the Example App

The fastest way to see djust-theming in action:

```bash
cd example_project
pip install -r requirements.txt
pip install -e ..
python manage.py runserver
```

Visit http://localhost:8000 to explore all features interactively.

### Option 2: Install in Your Project

```bash
pip install djust-theming
```

### 2. Configure

```python
# settings.py
INSTALLED_APPS = [
    'djust_theming',
    # ...
]

TEMPLATES = [{
    # ...
    'OPTIONS': {
        'context_processors': [
            # ... existing processors ...
            'djust_theming.context_processors.theme_context',
        ],
    },
}]

# Optional: customize defaults
LIVEVIEW_CONFIG = {
    'theme': {
        'preset': 'blue',           # default preset
        'default_mode': 'system',    # light, dark, or system
        'persist_in_session': True,
        'enable_dark_mode': True,
    }
}
```

### 3. Use in Templates

```html
{% load static %}
<!DOCTYPE html>
<html>
<head>
    {{ theme_head }}
    <link href="{% static 'djust_theming/css/base.css' %}" rel="stylesheet">
</head>
<body>
    <nav class="navbar">
        <div class="navbar-inner">
            <span class="navbar-brand">My App</span>
            {{ theme_switcher }}
        </div>
    </nav>

    <div class="main-area">
        <div class="content-pane">
            <div class="card">
                <div class="card-header">Dashboard</div>
                <div class="card-body">
                    <p class="text-muted">Welcome!</p>
                    <button class="btn btn-primary">Get Started</button>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
```

### Or with Template Tags

```html
{% load theme_tags static %}
<!DOCTYPE html>
<html>
<head>
    {% theme_head %}
    <link href="{% static 'djust_theming/css/base.css' %}" rel="stylesheet">
</head>
<body>
    {% theme_switcher show_labels=False %}
    {% theme_mode_toggle %}
    {% theme_preset_selector layout="grid" %}
</body>
</html>
```

## Available Presets

| Preset | Use Case | Primary Color |
|--------|----------|---------------|
| `default` | Neutral zinc — professional | Zinc/Gray |
| `shadcn` | shadcn/ui compatibility | Zinc/Gray |
| `blue` | Corporate, business apps | Blue |
| `green` | Finance, sustainability | Green |
| `purple` | Creative, premium apps | Purple |
| `orange` | Energetic, warm interfaces | Orange |
| `rose` | Modern, approachable | Rose/Pink |

## Custom Presets

```python
from djust_theming.presets import ThemePreset, ThemeTokens, ColorScale, THEME_PRESETS

MY_THEME = ThemePreset(
    name="custom",
    display_name="Custom",
    description="My custom theme",
    light=ThemeTokens(
        background=ColorScale(0, 0, 100),
        foreground=ColorScale(240, 10, 4),
        primary=ColorScale(200, 80, 50),
        primary_foreground=ColorScale(0, 0, 98),
        # ... all other tokens
    ),
    dark=ThemeTokens(
        # ... dark mode tokens
    ),
)

# Register it
THEME_PRESETS["custom"] = MY_THEME
```

## CSS Design System

The included `base.css` provides a complete design system:

- **Layout**: `.app-layout`, `.navbar`, `.sidebar`, `.content-pane`, `.container`
- **Components**: `.card`, `.btn`, `.badge`, `.alert`, `.modal`, `.toast`, `.empty-state`, `.stat-card`
- **Forms**: `.form-input`, `.form-select`, `.form-group`, `.form-label`, `.search-input`
- **Tables**: `.table`, `.table-hover`, `.table-responsive`
- **Utilities**: spacing (`.mt-4`, `.p-3`), flex (`.flex`, `.items-center`), text (`.text-sm`, `.font-bold`), colors (`.text-muted`, `.bg-muted`)
- **Animations**: fade, slide, shimmer skeleton, loading dots, toast transitions

All components use CSS custom properties from the theme, so they automatically adapt to any preset and light/dark mode.

## djust LiveView Integration

**NEW in v0.2.0:** Reactive theme switching without page reload! 🎉

```python
from djust import LiveView
from djust_theming import ThemeMixin

class DashboardView(ThemeMixin, LiveView):
    template_name = "dashboard.html"

    def mount(self, request, **kwargs):
        super().mount(request, **kwargs)
        # Theme context is automatically available:
        # self.theme_head, self.theme_switcher,
        # self.theme_preset, self.theme_mode
```

**In your template:**

```html
<!DOCTYPE html>
<html>
<head>
    {{ theme_head }}  <!-- Injects CSS + JS automatically -->
    <link href="{% static 'djust_theming/css/base.css' %}" rel="stylesheet">
</head>
<body>
    <!-- Theme switcher with reactive controls (uses dj-click/dj-change) -->
    {{ theme_switcher }}

    <!-- Your content here -->
</body>
</html>
```

**Features:**
- ✅ Theme variables injected into LiveView context via ThemeMixin
- ✅ Reactive theme mode switching (light/dark/system) without page reload
- ✅ Reactive preset switching with CSS hot-swapping (no reload needed!)
- ✅ Server-side state sync via WebSocket (`push_event`)
- ✅ Works with djust v0.3+ (djust-experimental compatible)

**How it works:**
1. User clicks theme switcher → sends `dj-click` event to server
2. Server updates theme state and pushes CSS update via `push_event('theme_update', {...})`
3. Client receives WebSocket event and updates CSS + DOM instantly (no page reload!)

This provides a **Phoenix LiveView-style reactive theming** experience.

## Tailwind CSS Integration

**NEW in v0.3.0:** First-class Tailwind CSS support! 🎨

djust-theming now generates Tailwind configs that map to your theme's CSS variables, allowing you to use theme colors directly in Tailwind classes and `@apply` directives.

### Quick Start

```bash
# Generate tailwind.config.js for your chosen preset
python manage.py djust_theme tailwind-config --preset blue --output tailwind.config.js

# Or use the default preset
python manage.py djust_theme tailwind-config
```

### Using Theme Colors in Tailwind

Once configured, use theme colors in your templates:

```html
<!-- Use theme colors in Tailwind classes -->
<button class="bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded-md">
  Primary Button
</button>

<div class="bg-card text-card-foreground border border-border rounded-lg p-6">
  Card content
</div>

<input class="bg-background border-input focus:ring-ring focus:ring-2 rounded-md px-3 py-2" />
```

### Using @apply with Theme Colors

Generate CSS examples:

```bash
python manage.py djust_theme generate-examples --output theme-components.css
```

Then use `@apply` in your CSS:

```css
.btn-primary {
  @apply bg-primary text-primary-foreground px-4 py-2 rounded-md;
  @apply hover:opacity-90 transition-opacity;
}

.card {
  @apply bg-card text-card-foreground rounded-lg border border-border;
  @apply shadow-sm p-6;
}
```

### CLI Commands

```bash
# Generate Tailwind config
python manage.py djust_theme tailwind-config [--preset PRESET] [--output FILE]

# Export colors in JSON/Python format
python manage.py djust_theme export-colors --preset blue --format json

# List available presets
python manage.py djust_theme list-presets

# Generate @apply examples
python manage.py djust_theme generate-examples --output theme.css
```

### Python API

```python
from djust_theming.tailwind import (
    generate_tailwind_config,
    export_preset_as_tailwind_colors,
    generate_tailwind_apply_examples,
)

# Generate config programmatically
config = generate_tailwind_config(preset_name='blue', extend_colors=True)
with open('tailwind.config.js', 'w') as f:
    f.write(config)

# Export colors as Python dict
colors = export_preset_as_tailwind_colors('blue')
print(colors['light-primary'])  # 'hsl(221, 83%, 53%)'
```

### Available Theme Colors in Tailwind

All theme colors are available as Tailwind utilities:

- `bg-primary`, `text-primary`, `border-primary`, etc.
- `bg-secondary`, `text-secondary`, etc.
- `bg-accent`, `bg-muted`, `bg-destructive`
- `bg-success`, `bg-warning` (extensions)
- `bg-card`, `bg-popover`, `bg-background`
- `border-border`, `border-input`
- `ring-ring` (for focus states)

All colors support opacity modifiers: `bg-primary/50`, `text-accent/80`, etc.

## shadcn/ui Compatibility

**NEW in v0.4.0:** Import and export themes in shadcn/ui format! 🔄

djust-theming is now fully compatible with shadcn/ui themes. Import themes from themes.shadcn.com or export your djust presets to share with the shadcn community.

### Import shadcn Theme

```bash
# Import a shadcn theme JSON file
python manage.py djust_theme shadcn-import my-theme.json

# Import and register it in THEME_PRESETS
python manage.py djust_theme shadcn-import my-theme.json --register
```

### Export to shadcn Format

```bash
# Export a djust preset to shadcn JSON format
python manage.py djust_theme shadcn-export --preset blue --output blue-theme.json
```

This JSON file can be:
- Uploaded to themes.shadcn.com
- Imported into other shadcn/ui projects
- Shared with the shadcn community

### Python API

```python
from djust_theming.shadcn import (
    import_shadcn_theme_from_file,
    export_to_shadcn_format,
    export_shadcn_theme_to_file,
)

# Import a shadcn theme
preset = import_shadcn_theme_from_file('custom-theme.json')
from djust_theming.presets import THEME_PRESETS
THEME_PRESETS[preset.name] = preset

# Export to shadcn format
theme_json = export_to_shadcn_format('blue')
print(theme_json['cssVars']['light']['primary'])  # '221.2 83.2% 53.3%'

# Save to file
export_shadcn_theme_to_file('blue', 'blue-theme.json')
```

### Format Compatibility

djust-theming uses the same HSL-based CSS variable system as shadcn/ui, ensuring 100% compatibility:

- ✅ All shadcn color tokens supported
- ✅ Light and dark mode variants
- ✅ Border radius configuration
- ✅ Extension tokens (success, warning) preserved
- ✅ Round-trip import/export without data loss

This means you can:
1. Find a theme you like on themes.shadcn.com
2. Download the JSON
3. Import it into djust-theming
4. Use it in your Django app with all djust features (reactive switching, Tailwind integration, etc.)

## Component Library

**NEW in v0.5.0:** Pre-built theme-aware components! 🧩

djust-theming includes a library of ready-to-use components that automatically adapt to your theme and light/dark mode.

### Quick Start

```html
{% load theme_components %}

<!-- Button variants -->
{% theme_button "Save" variant="primary" %}
{% theme_button "Cancel" variant="secondary" %}
{% theme_button "Delete" variant="destructive" %}

<!-- Cards -->
{% theme_card title="User Profile" %}
    <p>Profile content here</p>
{% end_theme_card %}

<!-- Badges -->
{% theme_badge "New" variant="success" %}
{% theme_badge "Beta" variant="secondary" %}

<!-- Alerts -->
{% theme_alert "Operation successful!" variant="success" dismissible=True %}

<!-- Inputs -->
{% theme_input "email" label="Email Address" placeholder="you@example.com" type="email" %}
```

### Available Components

All components use theme CSS variables and automatically adapt to theme changes:

| Component | Variants | Usage |
|-----------|----------|-------|
| `theme_button` | primary, secondary, destructive, ghost, link | Buttons with consistent styling |
| `theme_card` | - | Card containers with header/body/footer |
| `theme_badge` | default, secondary, success, warning, destructive, outline | Small status indicators |
| `theme_alert` | default, success, warning, destructive | Alert messages with optional dismissal |
| `theme_input` | - | Form inputs with labels |
| `theme_icon` | check, x, alert, info | SVG icons (integrate your own icon library) |

### Styling

All components are:
- ✅ Fully themed with CSS variables
- ✅ Automatically adapt to light/dark mode
- ✅ Responsive and accessible
- ✅ Customizable via additional classes
- ✅ No JavaScript required (except dismissible alerts)

### Custom Styling

Add custom classes to any component:

```html
{% theme_button "Submit" variant="primary" class="w-full mt-4" %}
{% theme_card title="Stats" class="shadow-lg" %}
```

### Integration with Tailwind

Components work seamlessly with Tailwind classes:

```html
{% theme_button "Click me" variant="primary" class="px-8 py-4 text-lg" %}
```

## API

### Python

- `ThemeManager(request)` — Manage theme state for a session
- `ThemeCSSGenerator(preset_name)` — Generate CSS from tokens
- `ThemeSwitcher(theme_manager, config)` — Render switcher component
- `ThemeModeButton(theme_manager)` — Simple toggle button
- `PresetSelector(theme_manager, layout)` — Preset selector (dropdown/grid/list)

### Template Tags

- `{% theme_head %}` — CSS variables + anti-FOUC script
- `{% theme_css %}` — CSS only (no scripts)
- `{% theme_switcher %}` — Full switcher UI
- `{% theme_mode_toggle %}` — Light/dark toggle button
- `{% theme_preset_selector layout="grid" %}` — Preset picker
- `{% theme_preset %}` — Current preset name
- `{% theme_mode %}` — Current mode setting
- `{% theme_resolved_mode %}` — Resolved mode (always light/dark)

### JavaScript

```javascript
// Available globally as window.djustTheme
djustTheme.setMode('dark');      // 'light', 'dark', 'system'
djustTheme.toggle();             // Toggle light/dark
djustTheme.setPreset('blue');    // Change preset (triggers reload)
djustTheme.getMode();            // Current mode setting
djustTheme.getResolvedMode();    // Always 'light' or 'dark'

// Events
window.addEventListener('djust-theme-changed', (e) => {
    console.log(e.detail.mode, e.detail.resolvedMode);
});
```

## Example Project

A complete Django application demonstrating all features is included in the `example_project/` directory.

**Features:**
- Homepage with feature overview
- Component library showcase
- Theme preset gallery
- Tailwind CSS integration examples
- Interactive theme switching

See [example_project/README.md](example_project/README.md) for setup instructions.

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Support

- 📖 [Documentation](https://djust.org/theming/)
- 🐛 [Issues](https://github.com/djust-org/djust-theming/issues)
- 💬 [Discussions](https://github.com/djust-org/djust-theming/discussions)

## License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2026 djust contributors

---

**Made with ❤️ by the djust community**
