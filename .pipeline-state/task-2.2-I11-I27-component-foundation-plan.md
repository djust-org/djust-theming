# Plan: Phase 2 Foundation — Component Contracts + Slot System (2.2/I11) + Test Harness (I27)

## Overview

Add composable slot blocks to all 5 component templates, define machine-readable
component contracts, and build a `ComponentTestCase` base class that validates
rendered HTML against those contracts.

## 1. Slot System (I11) — Template Changes

Current templates use simple variable interpolation. We add `{% block %}` tags so
theme authors can override individual parts when extending the base template.

**Important constraint:** The existing template tags call `tmpl.render(ctx)` where
`ctx` is a plain `dict`, not a Django `Context`. Django `{% block %}` tags only
work inside `{% extends %}` chains. Therefore, we use a **conditional-include**
pattern: each template section is wrapped in an `{% if %}` guard that checks for
an override variable, and renders the override content when present, otherwise
renders the default. This keeps backward compatibility (all existing tag calls
produce identical output).

Actually, re-examining: `select_template()` returns a `Template` object, and
`tmpl.render(ctx)` with a dict creates a `Context` internally. Django block/extends
requires parent template awareness. Since component templates are standalone (not
extended), we cannot use `{% block %}`. Instead we use **slot variables**: optional
context variables (`slot_icon`, `slot_content`, etc.) that override default content
when provided.

### button.html slots
- `slot_icon` — renders before text (icon HTML)
- `slot_content` — overrides `{{ text }}` entirely
- `slot_loading` — replaces content with loading indicator

### card.html slots
- `slot_header` — overrides default `<h3>{{ title }}</h3>` header
- `slot_body` — overrides `{{ content }}` body
- `slot_footer` — overrides `{{ footer }}` footer

### alert.html slots
- `slot_icon` — renders icon area before message
- `slot_message` — overrides `{{ message }}`
- `slot_actions` — renders action buttons area
- `slot_dismiss` — overrides default dismiss button

### badge.html slots
- `slot_content` — overrides `{{ text }}`

### input.html slots
- `slot_label` — overrides default label
- `slot_input` — overrides default `<input>` element
- `slot_help_text` — renders help text below input
- `slot_error` — renders error message below input

## 2. Component Contracts (`contracts.py`)

A data structure per component defining:
- `name` — component identifier
- `required_context` — list of `{name, type, default}` dicts
- `required_elements` — list of `{tag, attrs}` dicts (must appear in output)
- `required_accessibility` — list of `{attr, value_pattern}` dicts
- `available_slots` — list of slot variable names

Stored as a `COMPONENT_CONTRACTS` dict keyed by component name.

## 3. Test Harness (I27) — `ComponentTestCase`

Base class in `tests/component_test_base.py`:
- `render_component(tag_name, **kwargs)` — calls the template tag function directly
  with a mock context and returns the HTML string
- `assert_has_element(html, tag, attrs={})` — parses HTML, checks for element
- `assert_has_class(html, class_name)` — checks any element has class
- `assert_accessible(html, component_name)` — validates against contract a11y reqs
- `assert_slots_work(component_name, slot_overrides)` — verifies slot content appears

Uses `html.parser` (stdlib) for lightweight HTML assertion parsing. Inherits from
`unittest.TestCase` for compatibility with both pytest and Django test runner.

## 4. Test Plan (`tests/test_components.py`)

### Contract tests (per component)
- Required context produces valid output
- Missing optional context still renders
- Required HTML elements present
- Accessibility attributes present

### Slot tests (per component)
- Default rendering (no slots) matches current output
- Each slot variable overrides the correct section
- Multiple slots can be used simultaneously

### Regression tests
- CSS prefix applied to all class names
- Variant parameter changes output classes
- All 5 components render without error with minimal context

## Files to Create/Modify

| File | Action |
|------|--------|
| `djust_theming/contracts.py` | Create — contract definitions |
| `tests/component_test_base.py` | Create — ComponentTestCase base |
| `tests/test_components.py` | Create — component + slot + contract tests |
| `djust_theming/templates/djust_theming/components/button.html` | Modify — add slots |
| `djust_theming/templates/djust_theming/components/card.html` | Modify — add slots |
| `djust_theming/templates/djust_theming/components/alert.html` | Modify — add slots |
| `djust_theming/templates/djust_theming/components/badge.html` | Modify — add slots |
| `djust_theming/templates/djust_theming/components/input.html` | Modify — add slots |
| `CHANGELOG.md` | Modify — add entries |
