# Task I1: Decouple Inline HTML from Python -- Analysis

**Branch:** task/I1-decouple-inline-html
**Date:** 2026-03-22
**Status:** Analysis complete

---

## 1. Current Structure and Patterns

### Files with inline HTML generation

| File | Class/Function | Inline HTML Technique | Lines |
|------|---------------|----------------------|-------|
| `djust_theming/mixins.py` | `ThemeMixin._render_theme_switcher()` | f-string with SVG icons, CSS, mode buttons, preset select | 137-179 |
| `djust_theming/mixins.py` | `ThemeMixin._setup_theme_context()` | f-string for `anti_fouc` script, `theme_head`, `css_include` | 92-120 |
| `djust_theming/components.py` | `ThemeModeButton.render()` | f-string for button HTML with SVG icons | 101-119 |
| `djust_theming/components.py` | `ThemeModeButton._get_mode_icon()` | Raw SVG string literals | 121-126 |
| `djust_theming/components.py` | `PresetSelector._render_dropdown()` | f-string for `<select>` with `<option>` elements | 168-184 |
| `djust_theming/components.py` | `PresetSelector._render_grid()` | f-string for grid of `<button>` elements | 186-205 |
| `djust_theming/components.py` | `PresetSelector._render_list()` | f-string for radio button list | 207-230 |
| `djust_theming/templatetags/theme_tags.py` | `theme_head()` | f-string for `<script>`, `<style>`, `<link>` tags | 34-118 |
| `djust_theming/templatetags/theme_components.py` | `theme_icon()` | Dict of SVG strings returned via `mark_safe` | 129-148 |

### Files already using templates correctly

| File | Pattern | Template |
|------|---------|----------|
| `djust_theming/components.py` | `ThemeSwitcher.render()` | `djust_theming/theme_switcher.html` (via `render_to_string`) |
| `djust_theming/templatetags/theme_tags.py` | `theme_switcher` tag | `djust_theming/theme_switcher.html` (via `@inclusion_tag`) |
| `djust_theming/templatetags/theme_components.py` | `theme_button`, `theme_card`, `theme_badge`, `theme_alert`, `theme_input` | Respective component templates (via `@inclusion_tag`) |

### Existing templates

- `djust_theming/templates/djust_theming/theme_switcher.html` -- Full switcher with mode buttons + preset select + CSS
- `djust_theming/templates/djust_theming/components/button.html`
- `djust_theming/templates/djust_theming/components/card.html`
- `djust_theming/templates/djust_theming/components/badge.html`
- `djust_theming/templates/djust_theming/components/input.html`
- `djust_theming/templates/djust_theming/components/alert.html`

---

## 2. Code Smells and Issues

### Issue A: Mixin duplicates the template-tag HTML (HIGHEST PRIORITY)

`ThemeMixin._render_theme_switcher()` (lines 137-179) builds the exact same theme switcher UI as `theme_switcher.html`, but:
- Uses f-strings instead of the existing template
- Uses `dj-click`/`dj-change` attributes (LiveView events) while the template uses `data-djust-event`/`data-djust-params`
- Has slightly different HTML structure (no `show_labels` support, no `show_presets` guard, no `aria-hidden` on SVGs)
- Has minified inline CSS vs. the template's readable CSS
- Any change to the switcher UI must be made in two places

### Issue B: Mixin builds `theme_head` from f-strings

`ThemeMixin._setup_theme_context()` (lines 92-120) constructs the anti-FOUC script, CSS link/style tag, and JS include as raw f-strings. This duplicates the same logic in `theme_tags.theme_head()`.

### Issue C: `ThemeModeButton` renders entirely from f-strings

`ThemeModeButton.render()` (lines 101-119) and `_get_mode_icon()` (lines 121-126) use inline HTML. No template exists for this component.

### Issue D: `PresetSelector` renders three layouts from f-strings

`PresetSelector._render_dropdown()`, `_render_grid()`, `_render_list()` (lines 168-230) all use f-strings with `mark_safe`. No templates exist for any of these layouts.

### Issue E: `theme_icon` tag uses inline SVG dict

`theme_components.py` `theme_icon()` (lines 129-148) stores SVG icons as a Python dict and returns them via `mark_safe`.

### Issue F: `theme_head` tag builds inline HTML

`theme_tags.py` `theme_head()` (lines 34-118) builds the anti-FOUC `<script>`, `<style>`/`<link>`, and JS `<script>` tags inline.

---

## 3. Proposed Refactoring Approach

### Step 1: Create a LiveView-compatible theme switcher template

Create `djust_theming/templates/djust_theming/theme_switcher_liveview.html` (or parameterize the existing template with a variable like `event_style`).

**Preferred approach:** Add a context variable `use_liveview_events` to the existing `theme_switcher.html`. When true, render `dj-click="set_theme_mode" data-dj-mode="..."` attributes; when false, render `data-djust-event="set_theme_mode" data-djust-params='...'`.

Then refactor `ThemeMixin._render_theme_switcher()` to call `render_to_string("djust_theming/theme_switcher.html", context)` with `use_liveview_events=True`.

### Step 2: Create `theme_head.html` template

Create `djust_theming/templates/djust_theming/theme_head.html` containing:
- Anti-FOUC script block
- CSS block (either `<style>` or `<link>`)
- Optional JS `<script>` include

Both `theme_tags.theme_head()` and `ThemeMixin._setup_theme_context()` render this template with context.

### Step 3: Create `theme_mode_button.html` template

Create `djust_theming/templates/djust_theming/components/theme_mode_button.html`.

Refactor `ThemeModeButton.render()` to call `render_to_string(...)`.
Refactor `theme_tags.theme_mode_toggle` to use `@inclusion_tag(...)`.

### Step 4: Create preset selector templates

Create three templates:
- `djust_theming/templates/djust_theming/components/preset_selector_dropdown.html`
- `djust_theming/templates/djust_theming/components/preset_selector_grid.html`
- `djust_theming/templates/djust_theming/components/preset_selector_list.html`

Refactor `PresetSelector._render_*()` methods to call `render_to_string(...)`.
Refactor `theme_tags.theme_preset_selector` to use templates.

### Step 5: Create SVG icon templates (optional/low priority)

Create `djust_theming/templates/djust_theming/icons/{name}.svg` for each icon.
Refactor `theme_icon()` tag to load from template files.

This is lower priority since the icons are small and rarely change.

### Step 6: Update `theme_tags.theme_head` to use template

Convert from `format_html` + `mark_safe` to `@inclusion_tag("djust_theming/theme_head.html")`.

---

## 4. Files Affected

### Files to modify

| File | Changes |
|------|---------|
| `djust_theming/mixins.py` | Remove `_render_theme_switcher()` inline HTML; use `render_to_string` with the shared template. Remove inline `theme_head` construction; use shared `theme_head.html`. |
| `djust_theming/components.py` | `ThemeModeButton.render()`: use template. `PresetSelector._render_*()`: use templates. Remove `_get_mode_icon()`. |
| `djust_theming/templatetags/theme_tags.py` | `theme_head()`: render via template. `theme_mode_toggle()`: switch to `@inclusion_tag`. `theme_preset_selector()`: switch to `@inclusion_tag`. |
| `djust_theming/templatetags/theme_components.py` | `theme_icon()`: optionally move to template-based SVGs. |
| `djust_theming/templates/djust_theming/theme_switcher.html` | Add conditional `use_liveview_events` block for `dj-click` vs `data-djust-event` attributes. |

### New files to create

| File | Purpose |
|------|---------|
| `djust_theming/templates/djust_theming/theme_head.html` | Shared anti-FOUC + CSS + JS template |
| `djust_theming/templates/djust_theming/components/theme_mode_button.html` | Mode toggle button template |
| `djust_theming/templates/djust_theming/components/preset_selector_dropdown.html` | Dropdown preset selector |
| `djust_theming/templates/djust_theming/components/preset_selector_grid.html` | Grid preset selector |
| `djust_theming/templates/djust_theming/components/preset_selector_list.html` | List preset selector |

### Files NOT affected (already template-based)

- `djust_theming/templates/djust_theming/components/button.html`
- `djust_theming/templates/djust_theming/components/card.html`
- `djust_theming/templates/djust_theming/components/badge.html`
- `djust_theming/templates/djust_theming/components/input.html`
- `djust_theming/templates/djust_theming/components/alert.html`

---

## 5. Risk Assessment

### What could break

| Risk | Severity | Mitigation |
|------|----------|------------|
| **LiveView event binding changes** -- The mixin currently uses `dj-click`/`dj-change` while the template tag version uses `data-djust-event`/`data-djust-params`. Merging to a single template must preserve both binding styles. | HIGH | Use a conditional block in the template (`{% if use_liveview_events %}`) to emit the correct attributes. Test both code paths. |
| **HTML whitespace/formatting differences** -- Moving from f-strings to templates may change whitespace. Most cases this is harmless, but snapshot tests would break. | LOW | No snapshot tests exist. Visual testing recommended. |
| **CSS duplication** -- The inline CSS in `_render_theme_switcher()` is minified; the template version is readable. Need to ensure we don't ship both. | MEDIUM | Remove all inline CSS from Python; single source of truth is the template. |
| **`theme_head` output changes** -- The mixin constructs `theme_head` differently from the tag (e.g., script version `v=3` vs `v=2`, `id` attribute on style tag). Unifying these may change output for existing users. | MEDIUM | Audit differences and normalize. Document any changes in release notes. |
| **`mark_safe` removal** -- Moving to templates removes explicit `mark_safe` calls, which is actually safer. However, template auto-escaping could break if context values contain HTML that should be rendered raw. | LOW | The main raw content is CSS (passed via `{% autoescape off %}` or `|safe` filter in the template). Test CSS output. |
| **Missing template loader** -- If `djust_theming` is not in `INSTALLED_APPS`, templates won't be found. | LOW | Already a requirement; `ThemeSwitcher.render()` already uses `render_to_string`. |

### What tests cover this

- `tests/test_presets.py` -- Tests preset data structures only. Does NOT test HTML rendering.
- **No tests exist for:**
  - `ThemeMixin` rendering
  - `ThemeModeButton` rendering
  - `PresetSelector` rendering
  - `theme_head` tag output
  - `theme_mode_toggle` tag output
  - `theme_preset_selector` tag output
  - `theme_switcher` tag output

### Recommended test additions (before or during refactor)

1. **Rendering regression tests** -- Capture current HTML output of each component/tag, then verify the template-based version produces equivalent (or improved) output.
2. **Template tag smoke tests** -- Verify each tag renders without errors in a test Django template context.
3. **LiveView integration test** -- Verify `ThemeMixin._setup_theme_context()` produces renderable HTML with correct event bindings.

---

## 6. Implementation Priority

1. **ThemeMixin._render_theme_switcher()** -- Highest impact. Eliminates the biggest source of duplicated HTML (~40 lines of f-string HTML+CSS). Should reuse `theme_switcher.html`.
2. **ThemeMixin._setup_theme_context() theme_head** -- Second highest. Eliminates duplicated anti-FOUC script and CSS/JS includes.
3. **PresetSelector._render_*()** -- Three methods with ~60 lines of f-string HTML total.
4. **ThemeModeButton.render()** -- Smaller but still inline HTML.
5. **theme_tags.theme_head()** -- Lower priority since template tags are already the "template layer", but still worth extracting for DRY with the mixin.
6. **theme_icon()** -- Lowest priority; small dict of SVGs.

---

## 7. Key Design Decision: LiveView vs Tag Event Attributes

The central challenge is that the theme switcher template uses two different event binding conventions:

- **Template tag version** (for vanilla Django): `data-djust-event="set_theme_mode"` + `data-djust-params='{"mode": "dark"}'`
- **Mixin/LiveView version** (for djust LiveView): `dj-click="set_theme_mode"` + `data-dj-mode="dark"`

**Recommended approach:** Add a template variable `liveview` (default `False`). The template conditionally renders the appropriate attributes:

```html
{% if liveview %}
    dj-click="set_theme_mode" data-dj-mode="{{ mode }}"
{% else %}
    data-djust-event="set_theme_mode"
    data-djust-params='{"mode": "{{ mode }}"}'
{% endif %}
```

This keeps a single template with both rendering paths, avoiding duplication entirely.
