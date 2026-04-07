# Plan: Phase 2.1 Batch 2b -- 6 Utility Components

## Components

### 1. theme_breadcrumb
- **Tag**: `theme_breadcrumb(context, items, separator="/")`
- **Context vars**: `items` (list of {label, url}), `separator` (str), `css_prefix`, `attrs`
- **Slots**: `slot_separator`
- **HTML**: `<nav aria-label="Breadcrumb"><ol>` with `<li>` per item. Last item gets `aria-current="page"` and no link.
- **Contract**: Required element `nav` with `aria-label="Breadcrumb"`, `ol` tag. Accessibility: `aria-current="page"` on last item, `aria-label="Breadcrumb"` on nav.
- **CSS**: `.breadcrumb`, `.breadcrumb-list`, `.breadcrumb-item`, `.breadcrumb-link`, `.breadcrumb-separator`, `.breadcrumb-current`

### 2. theme_avatar
- **Tag**: `theme_avatar(context, src=None, alt="", name="", size="md")`
- **Context vars**: `src`, `alt`, `name` (for initials fallback), `size` (sm/md/lg), `css_prefix`, `attrs`
- **Slots**: `slot_image`, `slot_fallback`
- **HTML**: `<div>` wrapper. If `slot_image` or `src`, render `<img>`. Otherwise render initials from `name`.
- **Contract**: Required element `div`. No strict a11y beyond `alt` on img.
- **CSS**: `.avatar`, `.avatar-sm`, `.avatar-md`, `.avatar-lg`, `.avatar-image`, `.avatar-fallback`

### 3. theme_toast
- **Tag**: `theme_toast(context, message, variant="info", position="top-right", duration=5000)`
- **Context vars**: `message`, `variant` (success/warning/error/info), `position` (top-right, bottom-right, top-left, bottom-left), `duration` (ms), `css_prefix`, `attrs`
- **Slots**: `slot_message`, `slot_actions`
- **HTML**: `<div role="status" aria-live="polite" data-theme-toast data-duration="...">`. Close button inside.
- **Contract**: Required element `div` with `role="status"`. Accessibility: role=status, aria-live=polite.
- **CSS**: `.toast`, `.toast-success`, `.toast-warning`, `.toast-error`, `.toast-info`, `.toast-close`, `.toast-top-right`, `.toast-bottom-right`, etc.

### 4. theme_progress
- **Tag**: `theme_progress(context, value=None, max=100, label="")`
- **Context vars**: `value` (int or None for indeterminate), `max`, `label`, `css_prefix`, `attrs`
- **Slots**: `slot_label`
- **HTML**: `<div role="progressbar" aria-valuenow="..." aria-valuemin="0" aria-valuemax="...">` with inner bar. When value is None, indeterminate.
- **Contract**: Required element `div` with `role="progressbar"`. Accessibility: role=progressbar.
- **CSS**: `.progress`, `.progress-bar`, `.progress-indeterminate`, `.progress-label`

### 5. theme_skeleton
- **Tag**: `theme_skeleton(context, variant="text", width="100%", height="1rem")`
- **Context vars**: `variant` (text/circle/rect), `width`, `height`, `css_prefix`, `attrs`
- **Slots**: none
- **HTML**: `<div aria-hidden="true">` with shimmer animation.
- **Contract**: Required element `div`. No a11y (decorative).
- **CSS**: `.skeleton`, `.skeleton-text`, `.skeleton-circle`, `.skeleton-rect`, `@keyframes skeleton-shimmer`

### 6. theme_tooltip
- **Tag**: `theme_tooltip(context, text, position="top")`
- **Context vars**: `text` (tooltip content), `position` (top/bottom/left/right), `css_prefix`, `attrs`
- **Slots**: `slot_content`
- **HTML**: `<span data-tooltip="..." data-tooltip-position="...">` wrapping slot_content or text.
- **Contract**: Required element `span` with `data-tooltip`. CSS-only via `::after` pseudo-element.
- **CSS**: `[data-tooltip]`, `[data-tooltip]::after`, `[data-tooltip-position="top"]::after`, etc.

## Files to Create/Modify

### New Files
1. `djust_theming/templates/djust_theming/components/breadcrumb.html`
2. `djust_theming/templates/djust_theming/components/avatar.html`
3. `djust_theming/templates/djust_theming/components/toast.html`
4. `djust_theming/templates/djust_theming/components/progress.html`
5. `djust_theming/templates/djust_theming/components/skeleton.html`
6. `djust_theming/templates/djust_theming/components/tooltip.html`
7. `tests/test_batch2b_utility_components.py`

### Modified Files
1. `djust_theming/contracts.py` -- 6 new contracts + add to COMPONENT_CONTRACTS dict
2. `djust_theming/templatetags/theme_components.py` -- 6 new tag functions
3. `djust_theming/static/djust_theming/css/components.css` -- CSS for 6 new components
4. `tests/component_test_base.py` -- add 6 new tag imports + tag_map entries
5. `CHANGELOG.md` -- document new components

## Test Plan (TDD)
For each component:
1. Contract definition tests (exists, correct fields)
2. Rendering tests (correct elements, attributes, variants)
3. Slot override tests
4. Accessibility tests
5. Contract validation test (assert_contract)
