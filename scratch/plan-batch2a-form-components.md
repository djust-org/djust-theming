# Plan: Phase 2.1 Batch 2a — Form Components

## Overview
Add 4 new form components (select, textarea, checkbox, radio) following the established
pattern from existing components (input.html, contracts.py, theme_components.py, component_test_base.py).

## Components

### 1. theme_select
- **Template:** `djust_theming/templates/djust_theming/components/select.html`
- **Tag:** `theme_select(context, name, label=None, options=None, placeholder='', **attrs)`
- **Context vars:**
  - Required: `name` (str)
  - Optional: `label` (Optional[str]), `options` (list of dicts with value/label), `placeholder` (str), `css_prefix` (str), `attrs` (dict)
- **Slots:** `slot_label`, `slot_select`, `slot_help_text`, `slot_error`
- **HTML:** `<div>` wrapper with `<label>` and `<select>` with `<option>` elements
- **A11y:** Label `for` attribute referencing select `id`

### 2. theme_textarea
- **Template:** `djust_theming/templates/djust_theming/components/textarea.html`
- **Tag:** `theme_textarea(context, name, label=None, placeholder='', rows=4, **attrs)`
- **Context vars:**
  - Required: `name` (str)
  - Optional: `label` (Optional[str]), `placeholder` (str), `rows` (int), `css_prefix` (str), `attrs` (dict)
- **Slots:** `slot_label`, `slot_textarea`, `slot_help_text`, `slot_error`
- **HTML:** `<div>` wrapper with `<label>` and `<textarea>`
- **A11y:** Label `for` attribute referencing textarea `id`

### 3. theme_checkbox
- **Template:** `djust_theming/templates/djust_theming/components/checkbox.html`
- **Tag:** `theme_checkbox(context, name, label='', **attrs)`
- **Context vars:**
  - Required: `name` (str)
  - Optional: `label` (str), `description` (Optional[str]), `css_prefix` (str), `attrs` (dict)
- **Slots:** `slot_label`, `slot_description`
- **HTML:** `<div>` wrapper with `<input type="checkbox">` and `<label>`
- **A11y:** Label `for` attribute referencing checkbox `id`

### 4. theme_radio
- **Template:** `djust_theming/templates/djust_theming/components/radio.html`
- **Tag:** `theme_radio(context, name, options=None, **attrs)`
- **Context vars:**
  - Required: `name` (str)
  - Optional: `label` (Optional[str]), `options` (list of value/label dicts), `selected` (str), `css_prefix` (str), `attrs` (dict)
- **Slots:** `slot_label`, `slot_options`
- **HTML:** `<fieldset>` with `<legend>`, containing `<input type="radio">` + `<label>` per option
- **A11y:** `role="radiogroup"` on fieldset, each radio has associated label via `for`

## Files to Create
1. `tests/test_batch2a_form_components.py` — Tests (write first)
2. `djust_theming/templates/djust_theming/components/select.html`
3. `djust_theming/templates/djust_theming/components/textarea.html`
4. `djust_theming/templates/djust_theming/components/checkbox.html`
5. `djust_theming/templates/djust_theming/components/radio.html`

## Files to Modify
1. `djust_theming/contracts.py` — Add 4 new contract definitions + register in COMPONENT_CONTRACTS
2. `djust_theming/templatetags/theme_components.py` — Add 4 new tag functions
3. `tests/component_test_base.py` — Add 4 new components to render_component tag_map
4. `CHANGELOG.md` — Document new components

## Test Plan
- Contract definition tests (contracts exist, required fields, slots, a11y requirements)
- Rendering tests (default rendering, with label, with placeholder, with options)
- Slot override tests (each slot overrides default content)
- Accessibility tests (label-for linkage, role attributes)
- Contract validation tests (assert_contract passes for each component)
- Attribute passthrough tests (required, disabled, checked, etc.)
