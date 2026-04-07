# Plan: Phase 3.3 -- Navigation Components

## Overview
Add 4 navigation components: `theme_nav`, `theme_sidebar_nav`, `theme_nav_item`, `theme_nav_group`.
These wrap the existing `.navbar` and `.sidebar` CSS classes in base.css into reusable, contract-driven template tags.

## Components

### 1. theme_nav_item
**Purpose**: Single navigation link with active state detection.

- **Tag**: `theme_nav_item(context, label, url, icon=None, active=None, badge=None, **attrs)`
- **Template**: `djust_theming/components/nav_item.html`
- **Renders**: `<a>` link with `.nav-link` class
- **Context**: `label` (str, required), `url` (str, required), `icon` (Optional[str]), `active` (Optional[bool]), `badge` (Optional[str])
- **Active detection**: If `active` is None, auto-detect via `request.path == url` or `request.path.startswith(url)` (for non-root URLs)
- **Slots**: `slot_icon`, `slot_badge`
- **Accessibility**: `aria-current="page"` when active
- **Contract elements**: `RequiredElement(tag="a")`

### 2. theme_nav_group
**Purpose**: Collapsible group of nav items with a heading.

- **Tag**: `theme_nav_group(context, label, items=None, icon=None, expanded=True, **attrs)`
- **Template**: `djust_theming/components/nav_group.html`
- **Renders**: `<details>/<summary>` for native collapse behavior
- **Context**: `label` (str, required), `items` (list, optional), `icon` (Optional[str]), `expanded` (bool, default True)
- **Slots**: `slot_label`, `slot_items`
- **Accessibility**: `<details>` provides native expand/collapse semantics
- **Contract elements**: `RequiredElement(tag="details")`, `RequiredElement(tag="summary")`
- **CSS**: Uses `.sidebar-title` for summary styling, `.sidebar-menu` for items container

### 3. theme_nav
**Purpose**: Horizontal navigation bar.

- **Tag**: `theme_nav(context, brand=None, items=None, **attrs)`
- **Template**: `djust_theming/components/nav.html`
- **Renders**: `<nav role="navigation">` with `.navbar` class
- **Context**: `brand` (Optional[str]), `items` (list of nav item dicts: `{label, url, icon?, active?, badge?}`)
- **Slots**: `slot_brand`, `slot_items`, `slot_actions`
- **Accessibility**: `role="navigation"`, `aria-label="Main"`
- **Contract elements**: `RequiredElement(tag="nav", attrs={"role": "navigation"})`, `RequiredElement(tag="a")`(from items)
- **CSS**: Uses `.navbar`, `.navbar-inner`, `.navbar-brand`, `.navbar-nav`, `.navbar-actions`, `.nav-link`

### 4. theme_sidebar_nav
**Purpose**: Vertical sidebar navigation with sections.

- **Tag**: `theme_sidebar_nav(context, sections=None, **attrs)`
- **Template**: `djust_theming/components/sidebar_nav.html`
- **Renders**: `<nav role="navigation" aria-label="Sidebar">` with `.sidebar` class
- **Context**: `sections` (list of dicts: `{title, items}`)
- **Slots**: `slot_header`, `slot_sections`, `slot_footer`
- **Accessibility**: `role="navigation"`, `aria-label="Sidebar"`
- **Contract elements**: `RequiredElement(tag="nav", attrs={"role": "navigation", "aria-label": "Sidebar"})`
- **CSS**: Uses `.sidebar`, `.sidebar-title`, `.sidebar-menu`, `.sidebar-item`
- **Collapsible**: `data-theme-sidebar-collapse` attribute for JS-driven collapse

## Files to Create/Modify

### New Files
1. `djust_theming/templates/djust_theming/components/nav_item.html`
2. `djust_theming/templates/djust_theming/components/nav_group.html`
3. `djust_theming/templates/djust_theming/components/nav.html`
4. `djust_theming/templates/djust_theming/components/sidebar_nav.html`
5. `tests/test_navigation_components.py`

### Modified Files
1. `djust_theming/contracts.py` -- Add 4 new contracts
2. `djust_theming/templatetags/theme_components.py` -- Add 4 new tags
3. `tests/component_test_base.py` -- Register new tags in `render_component()`
4. `CHANGELOG.md` -- Document new components

## Test Plan (TDD)
1. Contract definition tests (contracts exist, fields correct, a11y requirements)
2. Rendering tests per component (elements, classes, content)
3. Active state detection tests (auto-detect, explicit override)
4. Slot tests (slot_brand, slot_items, etc.)
5. Accessibility tests (aria-current, aria-label, role)
6. Contract validation (assert_contract for each)
7. Edge cases (empty items, single item, no brand)

## Implementation Order
1. Contracts (all 4)
2. Tests (RED)
3. Templates (4 HTML files)
4. Template tags (4 tag functions)
5. Update component_test_base.py tag_map
6. Tests (GREEN)
7. CHANGELOG
