# Layout Templates

djust-theming ships with 7 layout templates that provide structural HTML skeletons for common application patterns. Each layout uses Django template inheritance, defines standard blocks, and is styled with responsive CSS that adapts to different screen sizes.

## Quick Start

Extend any layout in your own templates:

```html
{% extends "djust_theming/layouts/sidebar.html" %}

{% block page_title %}My App{% endblock %}

{% block sidebar %}
  <nav>
    <a href="/">Home</a>
    <a href="/settings">Settings</a>
  </nav>
{% endblock %}

{% block sidebar_content %}
  <h1>Welcome</h1>
  <p>Your main content goes here.</p>
{% endblock %}
```

The base layout automatically includes `{% theme_head %}` (which injects all theme CSS, design tokens, and anti-FOUC handling) and loads `layouts.css` for structural styling.

## Available Layouts

### base.html

The root layout that all other layouts extend. Provides the HTML shell, theme integration, and foundational blocks.

```
+---------------------------------------+
| <head> with theme_head + layouts.css  |
+---------------------------------------+
| body.layout-base                      |
|   content                             |
|   footer                              |
+---------------------------------------+
```

**Blocks:**

| Block | Purpose |
|-------|---------|
| `page_title` | Content of the `<title>` tag |
| `head_extra` | Additional `<head>` elements (meta tags, fonts, etc.) |
| `extra_css` | Additional `<link>` or `<style>` tags |
| `body_class` | Additional CSS classes on `<body>` |
| `content` | Main page content |
| `footer` | Footer area, after content |
| `extra_js` | Additional `<script>` tags, at end of body |

**Example:**

```html
{% extends "djust_theming/layouts/base.html" %}

{% block page_title %}Home{% endblock %}
{% block body_class %}home-page{% endblock %}

{% block content %}
  <main>
    <h1>Hello World</h1>
  </main>
{% endblock %}

{% block footer %}
  <footer>Copyright 2026</footer>
{% endblock %}
```

---

### sidebar.html

Fixed sidebar on the left with scrollable main content. On mobile (< 768px), the sidebar stacks above the content.

```
+------------------+---------------------+
| sidebar (fixed)  |  sidebar_content    |
|                  |  (scrollable)       |
+------------------+---------------------+
```

**Extends:** `base.html`
**CSS class:** `.layout-sidebar`

**Blocks (in addition to base blocks):**

| Block | Purpose |
|-------|---------|
| `sidebar` | Sidebar navigation/content |
| `sidebar_content` | Main content area next to sidebar |

**Example:**

```html
{% extends "djust_theming/layouts/sidebar.html" %}

{% block page_title %}Dashboard{% endblock %}

{% block sidebar %}
  <nav aria-label="Main navigation">
    <a href="/dashboard">Dashboard</a>
    <a href="/reports">Reports</a>
    <a href="/settings">Settings</a>
  </nav>
{% endblock %}

{% block sidebar_content %}
  <h1>Dashboard</h1>
  <p>Content here...</p>
{% endblock %}
```

---

### topbar.html

Sticky navigation bar at the top with content below.

```
+---------------------------------------+
| topbar (sticky)                       |
+---------------------------------------+
| topbar_content (scrollable)           |
+---------------------------------------+
```

**Extends:** `base.html`
**CSS class:** `.layout-topbar`

**Blocks (in addition to base blocks):**

| Block | Purpose |
|-------|---------|
| `topbar` | Top navigation bar content |
| `topbar_content` | Main content below the topbar |

**Example:**

```html
{% extends "djust_theming/layouts/topbar.html" %}

{% block page_title %}My Site{% endblock %}

{% block topbar %}
  <a href="/">Logo</a>
  <nav>
    <a href="/about">About</a>
    <a href="/contact">Contact</a>
  </nav>
{% endblock %}

{% block topbar_content %}
  <h1>Welcome</h1>
{% endblock %}
```

---

### sidebar_topbar.html

Combines a fixed sidebar with a sticky topbar. The topbar spans the area to the right of the sidebar. On mobile, both collapse to stacked layout.

```
+------------------+---------------------+
| sidebar (fixed)  | topbar (sticky)     |
|                  +---------------------+
|                  | sidebar_topbar_     |
|                  | content (scroll)    |
+------------------+---------------------+
```

**Extends:** `base.html`
**CSS class:** `.layout-sidebar-topbar`

**Blocks (in addition to base blocks):**

| Block | Purpose |
|-------|---------|
| `sidebar` | Sidebar navigation/content |
| `topbar` | Top navigation bar content |
| `sidebar_topbar_content` | Main content area |

**Example:**

```html
{% extends "djust_theming/layouts/sidebar_topbar.html" %}

{% block page_title %}Admin Panel{% endblock %}

{% block sidebar %}
  <nav>
    <a href="/admin/users">Users</a>
    <a href="/admin/settings">Settings</a>
  </nav>
{% endblock %}

{% block topbar %}
  <span>Admin Panel</span>
  <button>Logout</button>
{% endblock %}

{% block sidebar_topbar_content %}
  <h1>User Management</h1>
{% endblock %}
```

---

### centered.html

Content centered horizontally with a max-width container. Ideal for login pages, landing pages, and form-focused views.

```
+---------------------------------------+
|         +--centered--+                |
|         | centered_  |                |
|         | content    |                |
|         +------------+                |
+---------------------------------------+
```

**Extends:** `base.html`
**CSS class:** `.layout-centered`

**Blocks (in addition to base blocks):**

| Block | Purpose |
|-------|---------|
| `centered_content` | Content rendered inside the centered container (max-width 40rem) |

**Example:**

```html
{% extends "djust_theming/layouts/centered.html" %}

{% block page_title %}Login{% endblock %}

{% block centered_content %}
  <h1>Sign In</h1>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Log In</button>
  </form>
{% endblock %}
```

---

### dashboard.html

Extends `sidebar_topbar.html` with a responsive grid in the content area. Content automatically reflows from 1 column (mobile) to 2 columns (tablet) to 3 columns (desktop).

```
+------------------+---------------------+
| sidebar          | topbar              |
|                  +---------------------+
|                  | dashboard_content   |
|                  | (responsive grid)   |
+------------------+---------------------+
```

**Extends:** `sidebar_topbar.html`
**CSS class:** `.layout-dashboard`

**Blocks (in addition to sidebar_topbar blocks):**

| Block | Purpose |
|-------|---------|
| `dashboard_content` | Grid items placed inside a responsive CSS Grid |

**Example:**

```html
{% extends "djust_theming/layouts/dashboard.html" %}

{% block page_title %}Dashboard{% endblock %}

{% block sidebar %}
  <nav>
    <a href="/dashboard">Overview</a>
    <a href="/analytics">Analytics</a>
  </nav>
{% endblock %}

{% block topbar %}
  <span>Dashboard</span>
{% endblock %}

{% block dashboard_content %}
  <div class="card">Revenue: $12,345</div>
  <div class="card">Users: 1,234</div>
  <div class="card">Orders: 567</div>
  <div class="card">Conversion: 4.2%</div>
{% endblock %}
```

---

### split.html

Two-panel layout for list/detail views (e.g., email client, file browser). Left panel has fixed width, right panel fills remaining space. Collapses to stacked on mobile.

```
+-------------------+-------------------+
| panel_left        | panel_right       |
| (fixed width)     | (flexible)        |
+-------------------+-------------------+
```

**Extends:** `base.html`
**CSS class:** `.layout-split`

**Blocks (in addition to base blocks):**

| Block | Purpose |
|-------|---------|
| `panel_left` | Left panel (typically a list) |
| `panel_right` | Right panel (typically detail view) |

**Example:**

```html
{% extends "djust_theming/layouts/split.html" %}

{% block page_title %}Messages{% endblock %}

{% block panel_left %}
  <ul>
    {% for msg in messages %}
      <li><a href="?id={{ msg.id }}">{{ msg.subject }}</a></li>
    {% endfor %}
  </ul>
{% endblock %}

{% block panel_right %}
  {% if selected_message %}
    <h2>{{ selected_message.subject }}</h2>
    <p>{{ selected_message.body }}</p>
  {% else %}
    <p>Select a message to read it.</p>
  {% endif %}
{% endblock %}
```

## Responsive Behavior

All layouts use CSS design tokens for responsive breakpoints and structural dimensions:

| Token | Value | Purpose |
|-------|-------|---------|
| `--breakpoint-sm` | 640px | Small devices |
| `--breakpoint-md` | 768px | Tablets |
| `--breakpoint-lg` | 1024px | Desktops |
| `--breakpoint-xl` | 1280px | Large desktops |
| `--sidebar-width` | 280px | Default sidebar width |
| `--sidebar-collapsed-width` | 64px | Sidebar when collapsed |
| `--topbar-height` | 56px | Default topbar height |

### Mobile Behavior

Layouts with sidebars (`sidebar`, `sidebar_topbar`, `split`) collapse to a stacked (vertical) layout at screen widths below 768px. The sidebar becomes full-width and stacks above the main content.

The `dashboard` grid adapts its column count:
- **Mobile** (< 768px): 1 column
- **Tablet** (768px - 1023px): 2 columns
- **Desktop** (1024px+): 3 columns

## Theme Overrides

Layouts participate in the same theme-override system as components. To provide a theme-specific layout, place it at:

```
your_project/
  templates/
    djust_theming/
      themes/
        corporate/
          layouts/
            sidebar.html      # Corporate-specific sidebar
            dashboard.html    # Corporate-specific dashboard
```

When the active theme is `corporate`, `{% extends "djust_theming/layouts/sidebar.html" %}` will resolve the corporate version first. If no override exists, the default layout is used.

You can also use `resolve_layout_template()` in Python:

```python
from djust_theming.template_resolver import resolve_layout_template

def my_view(request):
    layout = resolve_layout_template(request, "sidebar")
    # layout is a Template object resolved for the current theme
```

## CSS Architecture

Layout styles live in `djust_theming/static/djust_theming/css/layouts.css`, wrapped in `@layer base` so they sit below component styles in the CSS cascade. This means component styles will always win over layout styles when there are conflicts, which is the correct behavior.

Each layout uses BEM-style class naming:
- `.layout-sidebar__container` -- the flex container
- `.layout-sidebar__aside` -- the sidebar element
- `.layout-sidebar__main` -- the main content area

The CSS uses theme-aware colors via CSS custom properties (`hsl(var(--card))`, `hsl(var(--border))`), so layouts automatically adapt to light/dark mode and theme changes.

## Accessibility

Layout templates include appropriate ARIA attributes:
- Sidebar `<aside>` elements have `role="navigation"` and `aria-label="Sidebar"`
- Topbar `<header>` elements have `role="banner"`
- Content areas use `<main>` elements where appropriate

## Extending Layouts

You can create your own layout that extends any of the built-in layouts:

```html
{# my_app/templates/my_app/layouts/admin.html #}
{% extends "djust_theming/layouts/sidebar_topbar.html" %}

{% block sidebar %}
  {# Your standard admin sidebar #}
  {% include "my_app/partials/admin_nav.html" %}
{% endblock %}

{% block topbar %}
  {# Your standard admin topbar #}
  {% include "my_app/partials/admin_header.html" %}
{% endblock %}
```

Then your page templates extend your custom layout:

```html
{% extends "my_app/layouts/admin.html" %}

{% block sidebar_topbar_content %}
  <h1>Admin Page</h1>
{% endblock %}
```

This gives you a consistent admin shell across all admin pages, while still benefiting from theme integration and responsive behavior.
