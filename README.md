# djust-theming

<p align="center">
  <strong>A production-ready theming system for Django</strong>
</p>

<p align="center">
  shadcn/ui-inspired • Reactive • Tailwind-ready • 24 Components • RTL Support
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

### Design Systems & Color Presets
- **11 design systems**: Material, iOS, Fluent, Minimalist, Playful, Corporate, Retro, Elegant, Neo-Brutalist, Organic, Dense
- **19 color presets**: Default, Shadcn, Blue, Green, Purple, Orange, Rose, Cyberpunk, Forest, Amber, Slate, Nebula, Natural 20, Catppuccin Mocha, Rosé Pine, Tokyo Night, Nord, Synthwave '84, Outrun
- **Mix & match**: Combine any design system with any color preset (209 combinations)
- **Complete control**: Typography, spacing, shadows, animations, border radius, component styles
- **Light/Dark/System mode** with anti-FOUC (Flash of Unstyled Content) protection
- **Context processor** for template variable injection
- **Session + localStorage persistence**
- **Cookie-based preset** for server-side rendering

### Component Library
- **24 ready-to-use components**: Button, Card, Badge, Alert, Input, Modal, Dropdown, Tabs, Table, Pagination, Select, Textarea, Checkbox, Radio, Breadcrumb, Avatar, Toast, Progress, Skeleton, Tooltip, Nav, Sidebar Nav, Nav Item, Nav Group
- **Automatically themed** — adapt to your preset and mode
- **Accessible** — ARIA roles, keyboard navigation, screen reader support
- **Template tags** for easy integration
- **Slot system** for composable customization
- **Interactive components** — Modal, Dropdown, and Tabs include a zero-dependency JS behavior layer

### Layout Templates
- **7 pre-built responsive layouts**: base, sidebar, topbar, sidebar_topbar, centered, dashboard, split
- **Django template inheritance** with standard blocks
- **ARIA landmarks** and semantic HTML
- **Responsive CSS** with breakpoint tokens

### Page Templates
- **9 ready-to-use pages**: login, register, password reset, password confirm, 403, 404, 500, maintenance, empty state
- **CSRF protection** built-in for auth forms
- **Customizable** via template blocks and slots

### Form Integration
- **`{% theme_form %}`** tag for instant form theming
- **ThemeFormRenderer** for Django's form rendering framework
- **3 layouts**: stacked, horizontal, inline
- **Error display** with `{% theme_form_errors %}`
- **22 themed widget templates** for all standard Django form fields

### Navigation Components
- **4 navigation components**: nav, sidebar_nav, nav_item, nav_group
- **Auto-active-state detection** from `request.path`
- **Native `<details>/<summary>` collapse** — no JS dependency for nav groups
- **ARIA accessible** with roles and keyboard support

### RTL & Bidirectional Text
- **Logical CSS properties** (margin-inline-start, border-inline-end, etc.)
- **Auto-detection** from Django's `LANGUAGE_CODE` setting
- **Per-theme direction override** via `direction` config or `theme.toml`
- **Component-specific RTL** overrides for sidebar, breadcrumb, toast, pagination

### Developer Tools
- **Component Gallery** at `/theming/gallery/` — all 24 components with every variant
- **Live Theme Editor** — real-time CSS preview with full customization and export
- **Side-by-side Diff View** — compare any two presets
- **Component Storybook** — detail pages with rendered variants, source, contracts, and CSS variables
- **DEBUG/is_staff gated** for production safety

### Performance
- **Critical CSS inlining** — tokens and dark mode inlined in `<style>`, utilities deferred via `<link rel="preload">`
- **`critical_css` config option** (default `True`) for automatic splitting
- **`<noscript>` fallback** for deferred CSS
- **ETag and Cache-Control headers** on deferred CSS endpoint
- **LRU-cached CSS generation** — no redundant regeneration

### Theme Template Overrides
- **Per-theme template overrides** — provide different HTML for each design system
- **Convention-based resolution** — `themes/{theme_name}/components/{component}.html`
- **Automatic fallback** — falls back to default template when no override exists
- **CSS cascade layers** — predictable `@layer` ordering (base, tokens, components, theme)

### djust LiveView Integration
- **LiveView mixin** for reactive theme switching
- **No page reload** — instant theme changes via WebSocket
- **Server-side state sync** — themes persist across sessions

### Tailwind CSS Support
- **Generate tailwind.config.js** with theme CSS variables
- **Use theme colors in Tailwind** classes (`bg-primary`, `text-accent`, etc.)
- **@apply support** for custom CSS components
- **Export colors** in JSON/Python formats

### shadcn/ui Compatibility
- **Import/Export** shadcn theme JSON
- **100% compatible** with themes.shadcn.com
- **Round-trip** import/export without data loss

## Quick Start

### Option 1: Try the Example App

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

### Configure

```python
# settings.py
INSTALLED_APPS = [
    'djust_theming',
    # ...
]

# urls.py
from django.urls import path, include

urlpatterns = [
    # ...
    path('theming/', include('djust_theming.urls')),
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
        'theme': 'material',        # Design system (material, ios, fluent, etc.)
        'preset': 'blue',           # Color preset
        'default_mode': 'system',   # light, dark, or system
        'persist_in_session': True,
        'enable_dark_mode': True,
        'css_prefix': '',           # Namespace prefix for component classes (e.g. 'dj-')
        'critical_css': True,       # Split CSS into critical (inlined) + deferred
    }
}
```

### Use in Templates

```html
{% load theme_tags theme_components %}
<!DOCTYPE html>
<html>
<head>
    {% theme_head %}
</head>
<body>
    {% theme_switcher %}

    {% theme_button "Get Started" variant="primary" %}
    {% theme_card title="Dashboard" %}
        <p>Card content here</p>
    {% end_theme_card %}
    {% theme_alert "Operation successful!" variant="success" dismissible=True %}
</body>
</html>
```

## CSS Architecture

Understanding how the CSS layers work is essential for consuming projects. djust-theming generates three layers of CSS custom properties:

### Layer 1: Color Tokens (generated per preset)

Raw HSL tuples on `:root` and `[data-theme="dark"]`. These are **not directly usable** as colors — they must be wrapped in `hsl()`:

```css
/* Generated by djust-theming — do NOT redefine these in your own CSS */
:root {
  --primary: 240 6% 10%;       /* HSL tuple, not a color */
  --background: 0 0% 100%;
  --border: 240 6% 90%;
  --muted-foreground: 240 5% 40%;
  /* ... 30+ tokens */
}
[data-theme="dark"] {
  --primary: 240 100% 90%;
  --background: 240 10% 3%;
  /* ... */
}
```

### Layer 2: Bridge Variables (`base.css`)

`base.css` maps raw tokens to **semantic, ready-to-use CSS variables**. This is the layer your custom CSS should reference:

```css
/* From base.css — these are real colors you can use directly */
--color-bg: hsl(var(--background));
--color-bg-subtle: hsl(var(--muted));
--color-bg-card: hsl(var(--card));
--color-text: hsl(var(--foreground));
--color-text-secondary: hsl(var(--muted-foreground));
--color-border: hsl(var(--border));
--color-primary: hsl(var(--primary));
--color-success: hsl(var(--success));
--color-warning: hsl(var(--warning));
--color-danger: hsl(var(--destructive));
```

`base.css` also provides design tokens for spacing, typography, border radius, shadows, and transitions.

### Layer 3: Component Styles (`components.css`)

Pre-built component styles that reference both raw tokens (`hsl(var(--primary))`) and bridge variables. Loaded automatically by `{% theme_head %}`.

### Using Theme Variables in Custom CSS

Always use the `--color-*` bridge variables from `base.css` for your own styles:

```css
/* Correct — uses bridge variables, adapts to any theme */
.my-sidebar {
  background: var(--color-bg-subtle);
  color: var(--color-text);
  border-right: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  font-family: var(--font-sans);
}

.my-badge {
  background: var(--color-primary);
  color: hsl(var(--primary-foreground));
}
```

```css
/* WRONG — hardcoded colors that ignore theme changes */
.my-sidebar {
  background: #f9fafb;
  color: #111827;
  border: 1px solid #e5e7eb;
}
```

### Common Pitfall: Overriding Theme Tokens

If your CSS defines `:root { --primary: ...; --background: ...; }`, it will **override** the theme's generated tokens and theme switching will appear broken. djust-theming wraps its output in `@layer tokens { }`, so any unlayered CSS with the same variable names will win in the cascade.

**Rule:** Never redefine `--primary`, `--background`, `--foreground`, `--border`, `--muted`, or any other token listed above in your own `:root`. Let djust-theming own those.

### CSS Load Order

When integrating manually (without `{% theme_head %}`), load CSS in this order:

```html
<head>
  <!-- 1. Theme tokens (color + design system variables) -->
  <style data-djust-theme>{{ theme_css }}</style>

  <!-- 2. Bridge layer (maps tokens to semantic --color-* variables) -->
  <link rel="stylesheet" href="{% static 'djust_theming/css/base.css' %}">

  <!-- 3. Component styles -->
  <link rel="stylesheet" href="{% static 'djust_theming/css/components.css' %}">

  <!-- 4. Your own CSS (uses --color-* and --space-* variables, never redefines tokens) -->
  <link rel="stylesheet" href="{% static 'myapp/css/custom.css' %}">
</head>
```

### Available Bridge Variables

| Variable | Maps to | Use for |
|----------|---------|---------|
| `--color-bg` | `--background` | Page background |
| `--color-bg-subtle` | `--muted` | Subtle backgrounds (cards, sidebars) |
| `--color-bg-card` | `--card` | Card surfaces |
| `--color-text` | `--foreground` | Primary text |
| `--color-text-secondary` | `--muted-foreground` | Secondary/muted text |
| `--color-border` | `--border` | Borders, dividers |
| `--color-border-subtle` | `--border` (50%) | Subtle borders |
| `--color-primary` | `--primary` | Primary accent color |
| `--color-success` | `--success` | Success states |
| `--color-warning` | `--warning` | Warning states |
| `--color-danger` | `--destructive` | Error/danger states |
| `--color-info` | `--info` | Informational states |
| `--color-surface` | `--secondary` | Interactive surfaces |
| `--color-surface-hover` | `--accent` | Hover backgrounds |

| Variable | Use for |
|----------|---------|
| `--font-sans` | Body text font stack |
| `--font-mono` | Code/monospace font stack |
| `--space-1` to `--space-24` | Spacing (4px grid) |
| `--radius-sm/md/lg/xl/full` | Border radius |
| `--shadow-sm/md/lg/xl` | Box shadows |
| `--duration-fast/normal/slow` | Transition durations |
| `--text-xs` to `--text-5xl` | Font sizes |

## Design Systems

**11 Design Systems** control all non-color visual aspects:

| System | Description |
|--------|-------------|
| **Material** | Google's Material Design with elevation-based hierarchy |
| **iOS** | Apple's design language with fluid animations |
| **Fluent** | Microsoft's Fluent Design System with depth and motion |
| **Minimalist** | Pure, distraction-free design with maximum content focus |
| **Playful** | Fun, energetic design with bouncy animations |
| **Corporate** | Professional, clean design for business applications |
| **Retro** | Classic web aesthetic with pixel-perfect design |
| **Elegant** | Premium design with serif fonts and generous spacing |
| **Neo-Brutalist** | Bold, dramatic design with sharp edges and high contrast |
| **Organic** | Soft, rounded design inspired by natural forms |
| **Dense** | Compact, information-dense design for data-heavy interfaces |

### Example Combinations

```python
# Material Design + Cyberpunk colors
LIVEVIEW_CONFIG = {
    'theme': {
        'theme': 'material',
        'preset': 'cyberpunk',
    }
}

# iOS + Forest green palette
LIVEVIEW_CONFIG = {
    'theme': {
        'theme': 'ios',
        'preset': 'forest',
    }
}

# Neo-Brutalist + Amber gold
LIVEVIEW_CONFIG = {
    'theme': {
        'theme': 'neo_brutalist',
        'preset': 'amber',
    }
}
```

## Available Presets

| Preset | Use Case | Style |
|--------|----------|-------|
| `default` | Neutral zinc — professional | Light/dark zinc |
| `shadcn` | shadcn/ui compatibility | Light/dark zinc |
| `blue` | Corporate, business apps | Blue |
| `green` | Finance, sustainability | Green |
| `purple` | Creative, premium apps | Purple |
| `orange` | Energetic, warm interfaces | Orange |
| `rose` | Modern, approachable | Rose/Pink |
| `cyberpunk` | High-tech, gaming | Neon cyan/magenta |
| `forest` | Nature, eco apps | Deep green |
| `amber` | Dashboards, terminals | Warm amber/gold |
| `slate` | Minimal, focus-first | Monochrome |
| `nebula` | Dark data-heavy apps | Deep space violet |
| `natural20` | Developer tools, terminals | Bloomberg-inspired cyan |
| `catppuccin` | Developer editors | Soothing pastels (Mocha) |
| `rose_pine` | Elegant developer tools | Muted pine pastels |
| `tokyo_night` | Code editors | Vibrant Tokyo neon |
| `nord` | Arctic-inspired UIs | Cool blue/gray |
| `synthwave` | Retro, 80s aesthetic | Glowing pink/cyan |
| `outrun` | Retro racing aesthetic | Hot pink/purple sunset |

## Components

**24 pre-built theme-aware components** via template tags:

```html
{% load theme_components %}

{% theme_button "Save" variant="primary" %}
{% theme_card title="User Profile" %}...{% end_theme_card %}
{% theme_badge "New" variant="success" %}
{% theme_alert "Saved!" variant="success" dismissible=True %}
{% theme_input "email" label="Email" placeholder="you@example.com" type="email" %}
{% theme_modal id="confirm" title="Confirm" size="md" %}
{% theme_dropdown id="actions" label="Actions" align="right" %}
{% theme_tabs id="settings" tabs=tab_list active=0 %}
{% theme_table headers=headers rows=rows variant="striped" caption="Users" %}
{% theme_pagination current_page=page total_pages=total url_pattern="/items/?page={}" %}
{% theme_select "country" label="Country" options=countries %}
{% theme_textarea "bio" label="Biography" rows=6 %}
{% theme_checkbox "agree" label="I agree to terms" %}
{% theme_radio "size" label="Size" options=sizes selected="md" %}
{% theme_breadcrumb items=breadcrumbs separator=">" %}
{% theme_avatar name="John Doe" size="md" %}
{% theme_toast "Saved!" variant="success" %}
{% theme_progress value=75 max=100 label="Upload" %}
{% theme_skeleton variant="text" width="200px" %}
{% theme_tooltip "Help text" position="top" %}
{% theme_nav brand="MyApp" items=nav_items %}
{% theme_sidebar_nav sections=sidebar_sections %}
{% theme_nav_item label="Home" url="/" %}
{% theme_nav_group label="Admin" items=admin_items expanded=True %}
```

### Component Reference

| Component | Variants | Slots | Usage |
|-----------|----------|-------|-------|
| `theme_button` | primary, secondary, destructive, ghost, link | icon, content, loading | Buttons with consistent styling |
| `theme_card` | - | header, body, footer | Card containers |
| `theme_badge` | default, secondary, success, warning, destructive | content | Small status indicators |
| `theme_alert` | default, success, warning, destructive | icon, message, actions, dismiss | Alert messages |
| `theme_input` | - | label, input, help_text, error | Form inputs with labels |
| `theme_modal` | sm, md, lg | header, body, footer, close | Dialog overlays |
| `theme_dropdown` | left, right (alignment) | trigger, menu | Dropdown menus |
| `theme_tabs` | - | (data-driven) | Tabbed interfaces |
| `theme_table` | default, striped, hover | caption, header, body, footer | Data tables |
| `theme_pagination` | - | prev, next | Page navigation |
| `theme_select` | - | label, select, help_text, error | Styled select dropdowns |
| `theme_textarea` | - | label, textarea, help_text, error | Multi-line text inputs |
| `theme_checkbox` | - | label, description | Single checkboxes |
| `theme_radio` | - | label, options | Radio button groups |
| `theme_breadcrumb` | - | separator | Navigation breadcrumb trails |
| `theme_avatar` | sm, md, lg | image, fallback | User avatars |
| `theme_toast` | success, warning, error, info | message, actions | Notification toasts |
| `theme_progress` | determinate, indeterminate | label | Progress bars |
| `theme_skeleton` | text, circle, rect | - | Loading placeholders |
| `theme_tooltip` | top, bottom, left, right | content | CSS-only tooltips |
| `theme_nav` | - | brand, items | Top navigation bar |
| `theme_sidebar_nav` | - | sections | Sidebar navigation |
| `theme_nav_item` | - | icon, badge | Individual nav links |
| `theme_nav_group` | - | label, items | Collapsible nav groups |

## Forms

Theme any Django form instantly:

```html
{% load theme_form_tags %}

{% theme_form form layout="stacked" %}
{% theme_form form layout="horizontal" %}
{% theme_form form layout="inline" %}

{# Error display #}
{% theme_form_errors form %}
```

Or use `ThemeFormRenderer` in settings:

```python
FORM_RENDERER = 'djust_theming.forms.ThemeFormRenderer'
```

See [Form Integration Guide](docs/forms.md) for details.

## CLI Commands

```bash
# Setup
python manage.py djust_theme init                    # Initialize djust-theming in your project

# Theme authoring
python manage.py djust_theme create-theme my-theme   # Scaffold a new theme directory
python manage.py djust_theme create-package my-theme  # Scaffold a pip-installable theme package
python manage.py djust_theme validate-theme my-theme  # Validate theme manifest and files
python manage.py djust_theme check-compat my-theme    # Check theme compatibility with contracts

# Presets & colors
python manage.py djust_theme list-presets              # List all available presets
python manage.py djust_theme export-colors --preset blue --format json

# Tailwind integration
python manage.py djust_theme tailwind-config --preset blue --output tailwind.config.js
python manage.py djust_theme generate-examples --output theme.css

# shadcn/ui integration
python manage.py djust_theme shadcn-import my-theme.json
python manage.py djust_theme shadcn-export --preset blue --output blue-theme.json

# Marketplace
python manage.py djust_theme marketplace-info my-theme  # Show marketplace metadata
```

## API

### Python

- `get_theme_manager(request)` — Get or create a cached `ThemeManager` for the request
- `generate_css_for_state(state, css_prefix="")` — Generate complete CSS for a `ThemeState`
- `ThemeManager(request)` — Manage theme state for a session
- `ThemeCSSGenerator(preset_name)` — Generate CSS from tokens
- `clear_css_cache()` — Clear all CSS generation `lru_cache` entries
- `PaletteGenerator.from_brand_colors(primary, secondary=None, accent=None, mode="professional")` — Generate a complete `ThemePreset` from 1-3 hex brand colors. Modes: `professional`, `playful`, `muted`, `vibrant`. WCAG AA compliant.
- Color utilities: `hsl_to_rgb`, `rgb_to_hsl`, `hex_to_rgb`, `rgb_to_hex`, `hex_to_hsl`, `hsl_to_hex`
- `ColorScale.from_hex(hex_str)` / `ColorScale.from_rgb(r, g, b)` — Construct from hex or RGB
- `ColorScale.to_hex()` / `ColorScale.to_rgb()` / `ColorScale.to_rgb_func()` — Convert to other formats

### Template Tags

```
{% load theme_tags %}            # Core tags
{% load theme_components %}      # Component tags
{% load theme_form_tags %}       # Form tags
{% load theme_pages %}           # Page template tags
```

| Tag | Purpose |
|-----|---------|
| `{% theme_head %}` | CSS variables + anti-FOUC script + component CSS |
| `{% theme_css %}` | CSS only (no scripts) |
| `{% theme_switcher %}` | Full switcher UI (mode toggle + preset selector) |
| `{% theme_mode_toggle %}` | Light/dark toggle button |
| `{% theme_preset_selector layout="grid" %}` | Preset picker (dropdown, grid, or list) |
| `{% theme_preset %}` | Current preset name |
| `{% theme_mode %}` | Current mode setting |
| `{% theme_resolved_mode %}` | Resolved mode (always light/dark) |
| `{% theme_form form layout="stacked" %}` | Themed form rendering |
| `{% theme_form_errors form %}` | Form error display |

### JavaScript

```javascript
// Available globally as window.djustTheme
djustTheme.setMode('dark');      // 'light', 'dark', 'system'
djustTheme.toggle();             // Toggle light/dark
djustTheme.setPreset('blue');    // Change preset
djustTheme.getMode();            // Current mode setting
djustTheme.getResolvedMode();    // Always 'light' or 'dark'

// Events
window.addEventListener('djust-theme-changed', (e) => {
    console.log(e.detail.mode, e.detail.resolvedMode);
});
```

## System Checks

djust-theming registers Django system checks that run at startup:

| Check | Severity | Description |
|-------|----------|-------------|
| `djust_theming.W001` | Warning | Preset color pair fails WCAG AA contrast ratio (4.5:1) |
| `djust_theming.W002` | Warning | CSS prefix is missing a trailing dash |
| `djust_theming.E001` | Error | `djust_theming.context_processors.theme_context` not in TEMPLATES |
| `djust_theming.E002` | Error | Configured preset name doesn't exist |
| `djust_theming.E003` | Error | Configured design system name doesn't exist |
| `djust_theming.E004` | Error | CSS prefix contains invalid characters |

Silence specific checks after review:

```python
SILENCED_SYSTEM_CHECKS = ["djust_theming.W001"]
```

## CSS Files Reference

| File | Purpose | Loaded by |
|------|---------|-----------|
| `base.css` | Bridge variables (`--color-*`), design tokens (spacing, typography, radius, shadows), layout utilities | Manual `<link>` or `{% theme_head %}` |
| `components.css` | Styles for all 24 template-tag components | `{% theme_head %}` (automatic) |
| `print.css` | Print-friendly overrides (hides interactive elements, forces readable colors) | Manual `<link media="print">` |

All styles use CSS custom properties and automatically adapt to any preset and light/dark mode. See [CSS Architecture](#css-architecture) for integration details.

## Documentation

- **[Getting Started](docs/getting-started.md)** — Create your first theme in 10 minutes
- **[Customization Guide](docs/customization.md)** — Gallery, live editor, two-panel customization
- **[Form Integration](docs/forms.md)** — `{% theme_form %}` tag, ThemeFormRenderer, widget templates
- **[RTL Support](docs/rtl.md)** — Right-to-left language support, logical properties, direction config
- **[Page Templates](docs/pages.md)** — 9 pre-built page templates (auth, errors, maintenance)
- **[Theme Authoring](docs/theme-authoring.md)** — Create, validate, and publish themes
- **[Accessibility](docs/accessibility.md)** — Reduced motion, high contrast, print stylesheet
- **[Breaking Changes](docs/BREAKING_CHANGES.md)** — Component contract changes and migration guide
- **[Marketplace Spec](docs/marketplace-spec.md)** — Theme marketplace metadata and publishing
- **[Component Contracts](djust_theming/docs/component-contracts.md)** — Machine-readable specs for all 24 components
- **[Layout Templates](djust_theming/docs/layouts.md)** — 7 responsive layout templates
- **[Design System](djust_theming/docs/design-system.md)** — Spacing, typography, color tokens
- **[Color System](djust_theming/docs/colors.md)** — HSL color system and custom presets

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Support

- [Issues](https://github.com/djust-org/djust-theming/issues)
- [Discussions](https://github.com/djust-org/djust-theming/discussions)

## License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2026 djust contributors
