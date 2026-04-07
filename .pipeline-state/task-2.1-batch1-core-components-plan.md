# Phase 2.1 Batch 1: Core Interactive Components Plan

## Overview
Add 5 new component template tags (modal, dropdown, tabs, table, pagination) plus a shared `components.js` behavior layer.

## Components

### 1. theme_modal
- **Tag**: `{% theme_modal id="myModal" title="Title" %}...body...{% end_theme_modal %}` (simple_tag with kwargs)
- **Context vars**: `id` (required), `title` (optional), `size` ("sm"/"md"/"lg", default "md"), `css_prefix`, `attrs`
- **Slots**: `slot_header`, `slot_body`, `slot_footer`, `slot_close`
- **HTML**: `<div data-theme-modal="{id}">` backdrop + dialog container with role="dialog", aria-modal="true", aria-labelledby
- **JS**: Trigger via `data-theme-modal-open="{id}"`, close via `data-theme-modal-close`, ESC key, backdrop click
- **Contract**: RequiredElement div with role="dialog", AccessibilityRequirement aria-modal="true", aria-labelledby

### 2. theme_dropdown
- **Tag**: `{% theme_dropdown id="dd1" label="Menu" %}...items...{% end_theme_dropdown %}`
- **Context vars**: `id` (required), `label` (required), `align` ("left"/"right", default "left"), `css_prefix`, `attrs`
- **Slots**: `slot_trigger`, `slot_menu`
- **HTML**: `<div data-theme-dropdown="{id}">` trigger button + menu container with role="menu"
- **JS**: Toggle via click, close on click-outside, keyboard nav (ArrowDown/Up, Escape)
- **Contract**: RequiredElement div, button with aria-expanded, div with role="menu"
- **Accessibility**: aria-expanded on trigger, role="menu" on container, aria-haspopup="true"

### 3. theme_tabs
- **Tag**: `{% theme_tabs id="tabs1" tabs=tab_list active=0 %}`
- **Context vars**: `id` (required), `tabs` (required, list of dicts with "label" and "content" keys), `active` (default 0), `css_prefix`, `attrs`
- **Slots**: none (tabs are data-driven)
- **HTML**: `<div data-theme-tabs="{id}">` with role="tablist" button list + tabpanels
- **JS**: Tab switching, ARIA management, keyboard nav (ArrowLeft/Right)
- **Contract**: RequiredElement div, [role="tablist"], button with role="tab", div with role="tabpanel"
- **Accessibility**: role="tablist", role="tab" with aria-selected, role="tabpanel" with aria-labelledby

### 4. theme_table
- **Tag**: `{% theme_table headers=headers rows=rows variant="striped" %}`
- **Context vars**: `headers` (required, list of strings), `rows` (required, list of lists), `variant` ("default"/"striped"/"hover", default "default"), `caption` (optional), `css_prefix`, `attrs`
- **Slots**: `slot_caption`, `slot_header`, `slot_body`, `slot_footer`
- **HTML**: `<div class="table-container"><table>` with responsive wrapper
- **JS**: None (pure HTML/CSS)
- **Contract**: RequiredElement table, RequiredElement div (wrapper)
- **Accessibility**: caption when provided

### 5. theme_pagination
- **Tag**: `{% theme_pagination current_page=page total_pages=total url_pattern="/items/?page={}" %}`
- **Context vars**: `current_page` (required, int), `total_pages` (required, int), `url_pattern` (required, str with {} placeholder), `show_edges` (bool, default True), `css_prefix`, `attrs`
- **Slots**: `slot_prev`, `slot_next`
- **HTML**: `<nav aria-label="Pagination">` with page links
- **JS**: None (pure HTML links)
- **Contract**: RequiredElement nav with aria-label
- **Accessibility**: aria-label="Pagination", aria-current="page" on active

## components.js
- IIFE, no dependencies
- Auto-init on DOMContentLoaded
- `initModals()`: listen for data-theme-modal-open clicks, handle ESC, backdrop click
- `initDropdowns()`: listen for data-theme-dropdown clicks, handle click-outside, keyboard nav
- `initTabs()`: listen for data-theme-tabs clicks, handle ArrowLeft/Right
- Detect djust LiveView (check `window.djustClient`) and defer event wiring if present
- Re-init on `djust:dom-update` event for LiveView compatibility
- Include in theme_head.html via `<script src="{% static 'djust_theming/js/components.js' %}" defer>`

## File Changes

### New files:
- `djust_theming/templates/djust_theming/components/modal.html`
- `djust_theming/templates/djust_theming/components/dropdown.html`
- `djust_theming/templates/djust_theming/components/tabs.html`
- `djust_theming/templates/djust_theming/components/table.html`
- `djust_theming/templates/djust_theming/components/pagination.html`
- `djust_theming/static/djust_theming/js/components.js`
- `tests/test_batch1_components.py`

### Modified files:
- `djust_theming/contracts.py` -- add 5 new contracts
- `djust_theming/templatetags/theme_components.py` -- add 5 new tags
- `djust_theming/static/djust_theming/css/components.css` -- add modal, dropdown, tabs, table, pagination styles
- `djust_theming/templates/djust_theming/theme_head.html` -- add components.js script tag
- `tests/component_test_base.py` -- extend render_component and tag_map for new components
- `CHANGELOG.md` -- add batch 1 entry

## Test Plan
- Contract definition tests for all 5 new components
- Basic render tests for each component
- Slot override tests for modal, dropdown, table
- Accessibility assertion tests (role="dialog", role="menu", role="tablist", aria-label)
- CSS class/variant tests
- Backward compatibility (existing 5 components still pass)
