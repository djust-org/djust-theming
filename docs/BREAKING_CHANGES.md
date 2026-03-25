# Breaking Changes

This document tracks changes to component contracts that may affect existing theme overrides. Theme authors should consult this file when upgrading djust-theming and run `check-compat` to verify their templates.

## Format

Each entry includes:

- **Version** -- the djust-theming version where the change was introduced
- **Component** -- the affected component name
- **Change** -- what changed in the contract (added/removed elements, context vars, slots)
- **Migration steps** -- what theme authors need to do to update their overrides

## Checking compatibility

Run the compatibility checker to verify your theme overrides against the current contracts:

```bash
# Check a specific theme
python manage.py djust_theme check-compat my-theme

# Check all themes
python manage.py djust_theme check-compat --all
```

## v1.0 (Baseline)

The current component contracts represent the v1.0 baseline. No breaking changes have been introduced yet. This section documents the contract as of v1.0 so that future changes can be tracked as diffs.

### Contract summary

| Component | Required elements | Required context | Available slots |
|-----------|-------------------|------------------|-----------------|
| alert | `<div role="alert">` | message | slot_icon, slot_message, slot_actions, slot_dismiss |
| avatar | `<div>` | (none) | slot_image, slot_fallback |
| badge | `<span>` | text | slot_content |
| breadcrumb | `<nav aria-label="Breadcrumb">`, `<ol>` | items | slot_separator |
| button | `<button>` | text | slot_icon, slot_content, slot_loading |
| card | `<div>` | (none) | slot_header, slot_body, slot_footer |
| checkbox | `<div>`, `<input type="checkbox">` | name | slot_label, slot_description |
| dropdown | `<div>`, `<button aria-haspopup="true">` | id, label | slot_trigger, slot_menu |
| input | `<div>` | name | slot_label, slot_input, slot_help_text, slot_error |
| modal | `<div role="dialog">` | id | slot_header, slot_body, slot_footer, slot_close |
| nav | `<nav role="navigation">` | (none) | slot_brand, slot_items, slot_actions |
| nav_group | `<details>`, `<summary>` | label | slot_label, slot_items |
| nav_item | `<a>` | label, url | slot_icon, slot_badge |
| pagination | `<nav aria-label="Pagination">` | current_page, total_pages, url_pattern | slot_prev, slot_next |
| progress | `<div role="progressbar">` | (none) | slot_label |
| radio | `<fieldset role="radiogroup">` | name | slot_label, slot_options |
| select | `<div>`, `<select>` | name | slot_label, slot_select, slot_help_text, slot_error |
| sidebar_nav | `<nav role="navigation" aria-label="Sidebar">` | (none) | slot_header, slot_sections, slot_footer |
| skeleton | `<div aria-hidden="true">` | (none) | (none) |
| table | `<div>`, `<table>` | headers, rows | slot_caption, slot_header, slot_body, slot_footer |
| tabs | `<div>` | id, tabs | (none) |
| textarea | `<div>`, `<textarea>` | name | slot_label, slot_textarea, slot_help_text, slot_error |
| toast | `<div role="status">` | message | slot_message, slot_actions |
| tooltip | `<span>` | text | slot_content |

### Notes

- **Required elements** must appear in the rendered HTML output. Attributes listed (e.g., `role="alert"`) must also be present.
- **Required context** variables must be referenced in the template via `{{ var }}` or `{% if var %}` patterns.
- **Available slots** are optional. Templates that omit them will receive an informational note from `check-compat` but no error.
- All components also accept optional `css_prefix` and `attrs` context variables. These are not listed above because they are optional across all components.
