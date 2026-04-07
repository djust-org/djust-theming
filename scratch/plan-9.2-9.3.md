# Plan: Phase 9.2 + 9.3 -- Component Storybook + Marketplace Spec

## Overview

Two deliverables:
1. **Component Storybook (9.2):** Auto-generated component documentation pages within the gallery module
2. **Marketplace Spec (9.3):** Metadata format spec document + CLI coverage reporter

---

## 9.2 -- Component Storybook

### Design

Add two new views to the existing `djust_theming/gallery/` module:

1. **Storybook Index** (`theming/gallery/storybook/`) -- Lists all 24 components with name, description (from contract), required/optional context count, slot count. Links to detail pages.

2. **Storybook Detail** (`theming/gallery/storybook/<component>/`) -- Per-component page showing:
   - **Rendered variants:** All variants from `_EXAMPLE_BUILDERS` in `gallery/context.py`
   - **Template source code:** Raw HTML source of the default template (read from `djust_theming/components/<name>.html`)
   - **Context contract table:** Required and optional context vars (name, type, default, required flag) from `contracts.py`
   - **Accessibility requirements:** From contract's `accessibility` field
   - **Available slots:** From contract's `available_slots` field
   - **CSS variables used:** Extracted from template source via regex for `var(--<name>)`

### Files to create/modify

- **`djust_theming/gallery/storybook.py`** -- New module with:
  - `get_component_template_source(name)` -- reads raw template HTML
  - `extract_css_variables(template_source)` -- regex extracts `--var-name` from template
  - `build_storybook_index_context()` -- builds index page context
  - `build_storybook_detail_context(component_name)` -- builds detail page context

- **`djust_theming/gallery/views.py`** -- Add:
  - `storybook_index_view(request)` -- renders index
  - `storybook_detail_view(request, component_name)` -- renders detail (404 for unknown)

- **`djust_theming/gallery/urls.py`** -- Add:
  - `path("storybook/", views.storybook_index_view, name="storybook")`
  - `path("storybook/<str:component_name>/", views.storybook_detail_view, name="storybook_detail")`

- **`djust_theming/templates/djust_theming/gallery/storybook_index.html`** -- Index template
- **`djust_theming/templates/djust_theming/gallery/storybook_detail.html`** -- Detail template

- **`tests/test_storybook.py`** -- Tests for:
  - URL resolution (index + detail)
  - Access control (same as gallery: DEBUG or is_staff)
  - Index content: lists all 24 components, links to detail pages
  - Detail content: shows contract table, template source, slots, CSS vars
  - Detail 404 for unknown component
  - `get_component_template_source()` returns HTML
  - `extract_css_variables()` finds CSS vars
  - `build_storybook_index_context()` returns all components
  - `build_storybook_detail_context()` returns full detail data

### Access control

Same as gallery: `_check_access(request)` (DEBUG or is_staff).

---

## 9.3 -- Marketplace Spec

### Design

Two deliverables:

1. **Spec document** (`docs/marketplace-spec.md`) -- Documents:
   - `[marketplace]` section format for `theme.toml`
   - Fields: `screenshots`, `tags`, `compatibility_range`, `preview_url`
   - Example TOML
   - Component coverage concept (which components a theme overrides vs inherits)

2. **CLI reporter** (`marketplace-info` subcommand) -- `manage.py djust_theme marketplace-info <theme-name>`:
   - Reads theme manifest
   - Scans `components/` directory for template overrides
   - Compares against `COMPONENT_CONTRACTS` to produce coverage report
   - Reports: overridden components, inherited (default) components, coverage percentage
   - Reads `[marketplace]` section from theme.toml if present

### Files to create/modify

- **`docs/marketplace-spec.md`** -- New spec document
- **`djust_theming/manifest.py`** -- Extend `ThemeManifest` with optional marketplace fields:
  - `screenshots: list[str]`
  - `tags: list[str]`
  - `compatibility_range: str`
  - `preview_url: str`
  - Parse from `[marketplace]` section in `from_toml()`
  - Serialize in `to_toml()`

- **`djust_theming/gallery/storybook.py`** -- Add `get_component_coverage(theme_name, themes_dir)` function (reusable by both storybook and CLI)

- **`djust_theming/management/commands/djust_theme.py`** -- Add `marketplace-info` subcommand

- **`tests/test_marketplace.py`** -- Tests for:
  - `ThemeManifest` marketplace field parsing
  - `ThemeManifest` marketplace field serialization
  - `get_component_coverage()` function
  - `marketplace-info` command output (overridden/inherited/coverage)
  - `marketplace-info` with missing theme (error)
  - `marketplace-info` with marketplace section in toml

---

## Test-first order

1. Write `tests/test_storybook.py` (storybook views + helpers)
2. Implement `djust_theming/gallery/storybook.py`
3. Update `djust_theming/gallery/views.py` + `urls.py`
4. Create storybook templates
5. Write `tests/test_marketplace.py`
6. Extend `ThemeManifest` with marketplace fields
7. Implement `get_component_coverage()` in storybook.py
8. Add `marketplace-info` subcommand
9. Write `docs/marketplace-spec.md`
10. Update CHANGELOG.md
