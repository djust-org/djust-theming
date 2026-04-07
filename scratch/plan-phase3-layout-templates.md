# Phase 3.1 + 3.2 + 3.4: Layout Templates + Standard Blocks + Responsive Tokens

## Overview

Create 7 layout templates that provide structural HTML skeletons for common application
patterns. Each layout uses Django template inheritance ({% extends %}), defines standard
blocks, and is styled via layout-specific CSS that uses responsive design tokens.

## Existing Foundation

- `base.css` already has `.app-layout`, `.navbar`, `.sidebar`, `.content-pane`, `.container`
  classes with `--navbar-height`, `--sidebar-width`, `--content-max-width` tokens
- `design_tokens.py` generates `:root` CSS custom properties (spacing, typography, radius,
  transitions, shadows) and utility classes
- `template_resolver.py` resolves templates with theme-specific overrides via
  `_get_theme_template_candidates()` / `select_template()`
- `theme_head.html` renders anti-FOUC script, critical CSS, deferred CSS, component CSS, JS

## Design Decisions

### Template Location
`djust_theming/templates/djust_theming/layouts/` -- follows existing template namespace.
Theme overrides at `djust_theming/themes/{theme}/layouts/{layout}.html`.

### Template Resolution
Add `_get_layout_candidates()` and `resolve_layout_template()` to `template_resolver.py`
so layouts participate in the same theme-override chain as components.

### CSS Strategy
- New file: `djust_theming/static/djust_theming/css/layouts.css`
- Wrapped in `@layer base` (layout is structural, below components)
- Uses existing tokens plus new responsive tokens from `design_tokens.py`

### Responsive Tokens (added to design_tokens.py)
```css
:root {
  /* Breakpoints */
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;

  /* Layout dimensions */
  --sidebar-width: 280px;
  --sidebar-collapsed-width: 64px;
  --topbar-height: 56px;
}
```
New function: `get_layout_tokens() -> str`
Added to `generate_design_tokens_root_css()`.

## 7 Layout Templates

### 1. base.html (Root Layout)
**File:** `layouts/base.html`
**Blocks:** `page_title`, `head_extra`, `body_class`, `content`, `footer`, `extra_css`, `extra_js`
**Structure:**
```html
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block page_title %}{% endblock %}</title>
  {% theme_head %}
  <link rel="stylesheet" href="{% static 'djust_theming/css/layouts.css' %}">
  {% block head_extra %}{% endblock %}
  {% block extra_css %}{% endblock %}
</head>
<body class="layout-base {% block body_class %}{% endblock %}">
  {% block content %}{% endblock %}
  {% block footer %}{% endblock %}
  {% block extra_js %}{% endblock %}
</body>
</html>
```

### 2. sidebar.html (Sidebar Layout)
**Extends:** `layouts/base.html`
**Blocks:** `sidebar`, `content`
**CSS class:** `.layout-sidebar` -- grid: fixed sidebar left + scrollable main
```
+------------------+---------------------+
| sidebar (fixed)  |  content (scroll)   |
|                  |                     |
+------------------+---------------------+
```

### 3. topbar.html (Topbar Layout)
**Extends:** `layouts/base.html`
**Blocks:** `topbar`, `content`
**CSS class:** `.layout-topbar` -- grid: fixed top nav + content below
```
+---------------------------------------+
| topbar (fixed)                         |
+---------------------------------------+
| content (scroll)                       |
+---------------------------------------+
```

### 4. sidebar-topbar.html (Sidebar + Topbar Layout)
**Extends:** `layouts/base.html`
**Blocks:** `sidebar`, `topbar`, `content`
**CSS class:** `.layout-sidebar-topbar`
```
+------------------+---------------------+
| sidebar (fixed)  | topbar (fixed)      |
|                  +---------------------+
|                  | content (scroll)    |
+------------------+---------------------+
```

### 5. centered.html (Centered Layout)
**Extends:** `layouts/base.html`
**Blocks:** `content`
**CSS class:** `.layout-centered` -- max-width centered column, good for auth/landing
```
+---------------------------------------+
|         +--centered--+                |
|         | content    |                |
|         +------------+                |
+---------------------------------------+
```

### 6. dashboard.html (Dashboard Layout)
**Extends:** `layouts/sidebar-topbar.html`
**Blocks:** `content` (with grid wrapper)
**CSS class:** `.layout-dashboard` -- inherits sidebar+topbar, adds content grid
```
+------------------+---------------------+
| sidebar          | topbar              |
|                  +---------------------+
|                  | content (grid)      |
+------------------+---------------------+
```

### 7. split.html (Split Panel Layout)
**Extends:** `layouts/base.html`
**Blocks:** `panel_left`, `panel_right`
**CSS class:** `.layout-split` -- two-panel (list + detail)
```
+-------------------+-------------------+
| panel_left        | panel_right       |
| (list, fixed-w)   | (detail, flex)    |
+-------------------+-------------------+
```

## Files to Create/Modify

### New Files
1. `djust_theming/templates/djust_theming/layouts/base.html`
2. `djust_theming/templates/djust_theming/layouts/sidebar.html`
3. `djust_theming/templates/djust_theming/layouts/topbar.html`
4. `djust_theming/templates/djust_theming/layouts/sidebar_topbar.html`
5. `djust_theming/templates/djust_theming/layouts/centered.html`
6. `djust_theming/templates/djust_theming/layouts/dashboard.html`
7. `djust_theming/templates/djust_theming/layouts/split.html`
8. `djust_theming/static/djust_theming/css/layouts.css`
9. `tests/test_layout_templates.py`

### Modified Files
1. `djust_theming/design_tokens.py` -- add `get_layout_tokens()`, update `generate_design_tokens_root_css()`
2. `djust_theming/template_resolver.py` -- add `resolve_layout_template()` and `_get_layout_candidates()`
3. `CHANGELOG.md` -- add entry

## Test Plan (TDD)

### test_layout_templates.py
1. **Template existence** -- each of the 7 templates can be loaded by Django's template engine
2. **Template inheritance** -- sidebar extends base, topbar extends base, sidebar_topbar extends base, centered extends base, dashboard extends sidebar_topbar, split extends base
3. **Block presence** -- each template defines its documented blocks (verify with {% block X %}content{% endblock %})
4. **Theme head inclusion** -- base.html renders {% theme_head %} output
5. **CSS class application** -- each layout applies its `.layout-*` body class
6. **Layout resolution** -- `resolve_layout_template()` returns correct template with theme fallback
7. **Responsive tokens** -- `get_layout_tokens()` returns breakpoint and dimension variables
8. **Layout CSS file** -- `layouts.css` exists and contains expected selectors
9. **Layouts CSS uses @layer base** -- CSS is wrapped in `@layer base`

## Implementation Order
1. Write tests (TDD)
2. Add `get_layout_tokens()` to `design_tokens.py`
3. Add `resolve_layout_template()` to `template_resolver.py`
4. Create `layouts.css`
5. Create 7 layout templates
6. Run tests, fix any failures
7. Update CHANGELOG
