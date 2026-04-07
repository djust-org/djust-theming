# Plan: Phase 8.2 + 8.3 -- Live Theme Editor + Diff View

## Overview

Add two new gallery sub-pages:
1. **Live Editor (8.2)** -- Interactive token editor with real-time CSS preview and theme export
2. **Diff View (8.3)** -- Side-by-side preset comparison using iframes

Both share the same DEBUG/is_staff access control as the gallery view.

## Architecture Decisions

- **No build step**: All JS is vanilla, inline in templates. No npm.
- **No server round-trip for preview**: JS updates CSS custom properties on `document.documentElement` directly.
- **Export is server-side**: POST JSON token values, server generates theme.toml + tokens.css via existing `ThemePreset`/`ThemeCSSGenerator` infrastructure.
- **Diff view uses iframes**: Each iframe loads the existing gallery page with `?preset=<name>`, avoiding code duplication.

## New Files

### Python
- `djust_theming/gallery/views.py` -- Add `editor_view`, `editor_export_view`, `diff_view` (extend existing file)
- `djust_theming/gallery/urls.py` -- Add 3 new URL patterns (extend existing file)
- `tests/test_editor_view.py` -- Tests for editor view, export endpoint, diff view

### Templates
- `djust_theming/templates/djust_theming/gallery/editor.html` -- Editor page
- `djust_theming/templates/djust_theming/gallery/diff.html` -- Diff comparison page

## URL Structure

| URL | View | Name |
|-----|------|------|
| `theming/gallery/editor/` | `editor_view` | `editor` |
| `theming/gallery/editor/export/` | `editor_export_view` | `editor_export` |
| `theming/gallery/diff/` | `diff_view` | `diff` |

## Live Editor (8.2)

### View: `editor_view(request)`
- Same access control as `gallery_view`
- Reads `?preset=<name>` to set initial token values
- Builds context with:
  - `presets` list (from `list_presets()`)
  - `current_preset` name
  - `preset_tokens` -- serialized light/dark ThemeTokens as JSON for JS initialization
  - `token_fields` -- ordered list of token field metadata (name, css_var, type: color|radius)
  - Gallery sample data (reuse `_template_sample_data()` + `build_gallery_context()`)

### Template: `editor.html`
- Two-panel layout: left sidebar (controls), right main (live preview)
- Left panel:
  - Preset selector dropdown (loads preset tokens into controls)
  - Color token controls: native `<input type="color">` for each HSL token (converted to/from hex for the color picker)
  - Radius slider: `<input type="range" min="0" max="2" step="0.125">`
  - "Reset" button to restore preset defaults
  - "Export" button to POST and download
- Right panel:
  - Embedded gallery component showcase (same HTML as gallery.html but inline, not iframe)
  - Uses `{% include %}` of component sections or direct tag rendering
- JS behavior:
  - On color input change: convert hex to HSL, set `document.documentElement.style.setProperty('--token-name', hslValue)`
  - On radius change: set `--radius` custom property
  - On preset select change: fetch preset tokens from embedded JSON data, update all controls + CSS vars
  - On export click: collect all current token values, POST as JSON to export endpoint

### View: `editor_export_view(request)`
- POST only (405 for GET)
- Reads JSON body: `{ "tokens": { "light": {...}, "dark": {...} }, "radius": 0.5, "name": "custom" }`
- Generates `tokens.css` using the token values (CSS custom properties)
- Generates `theme.toml` manifest
- Returns JSON response with `{ "tokens_css": "...", "theme_toml": "..." }` for client-side download

## Diff View (8.3)

### View: `diff_view(request)`
- Same access control
- Reads `?left=<preset>&right=<preset>` query params (defaults: left=default, right=nord)
- Context: `presets` list, `left_preset`, `right_preset`

### Template: `diff.html`
- Top bar: two preset selectors (left/right), changing reloads the page
- Two side-by-side iframes, each loading `theming/gallery/?preset=<name>`
- Minimal CSS for the split layout

## Token Serialization (for JS)

Convert ThemeTokens to a JSON-friendly dict:
```python
def serialize_tokens(tokens: ThemeTokens) -> dict:
    """Convert ThemeTokens to {field_name: {"h": int, "s": int, "l": int}}."""
```

Convert ThemePreset to full JSON structure:
```python
def serialize_preset(preset: ThemePreset) -> dict:
    """Return {"light": {...}, "dark": {...}, "radius": float}."""
```

These go in `gallery/context.py` or a small helper in the gallery module.

## Test Plan

### test_editor_view.py

**URL resolution (3 tests)**
- editor URL resolves to `editor_view`
- editor_export URL resolves to `editor_export_view`
- diff URL resolves to `diff_view`

**Access control (6 tests)**
- Editor: 200 in DEBUG, 403 non-staff non-DEBUG, 200 staff non-DEBUG
- Diff: 200 in DEBUG, 403 non-staff non-DEBUG, 200 staff non-DEBUG

**Editor content (4 tests)**
- Contains color input controls
- Contains radius slider
- Contains preset selector
- Contains export button

**Editor export (4 tests)**
- GET returns 405
- Valid POST returns 200 JSON with tokens_css and theme_toml keys
- tokens_css contains CSS custom properties
- theme_toml contains [theme] section

**Diff content (3 tests)**
- Contains two iframes
- Contains left/right preset selectors
- Default presets are applied (default + nord in content)

**Preset loading (2 tests)**
- ?preset=nord loads nord token values in editor
- Editor page contains serialized preset JSON data

Total: ~22 tests

## Implementation Order

1. Add `serialize_tokens()` and `serialize_preset()` helpers to `gallery/context.py`
2. Write tests (TDD)
3. Add views to `gallery/views.py`
4. Add URL patterns to `gallery/urls.py`
5. Create `editor.html` template
6. Create `diff.html` template
7. Run tests, iterate
8. Update CHANGELOG
