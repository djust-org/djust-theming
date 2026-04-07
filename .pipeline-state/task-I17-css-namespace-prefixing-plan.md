# Plan: I17 — CSS Namespace Prefixing

## Problem

djust-theming uses generic CSS class names (`.btn`, `.card`, `.alert`, `.badge`, `.input`, etc.) that collide with Bootstrap, Bulma, and other CSS frameworks. Users who include djust-theming alongside another CSS framework get broken styles.

## Design Decision: Where to Apply the Prefix

### Scope: components.css only (primary target)

The prefix applies to the **component classes** in `components.css` and the corresponding **component templates**. These are the classes most likely to collide (`.btn`, `.card`, `.alert`, `.badge`, `.input`, etc.).

**base.css is opt-in and out of scope for v1.** Users who include `base.css` via `{% static %}` are explicitly choosing to use the utility/layout system; they accept those class names. Prefixing 200+ utility classes (`.mt-2`, `.flex`, `.gap-4`) would be impractical and confusing.

**performance.css references component classes** (`.btn`, `.card`, `.badge`, `.alert`) — these references must also respect the prefix, but performance.css is a static file. We will generate it dynamically or document the limitation.

### Scope: theme_css_generator.py

The `CompleteThemeCSSGenerator._generate_component_styles()` method outputs `.btn`, `.card`, `.form-input` selectors. These must also be prefixed.

The `_generate_typography_classes()` method outputs utility classes (`.font-sans`, `.text-xs`, etc.) — these will NOT be prefixed (same reasoning as base.css).

## Configuration

### Settings key

```python
# In Django settings.py
LIVEVIEW_CONFIG = {
    "theme": {
        "css_prefix": "dj-",   # All component classes become .dj-btn, .dj-card, etc.
    }
}
```

- **Key**: `css_prefix` inside the existing `LIVEVIEW_CONFIG["theme"]` dict
- **Default**: `""` (empty string) for full backward compatibility
- **Convention**: Prefix should end with `-` if non-empty (e.g., `"dj-"`, `"djt-"`)

### Access via existing pattern

```python
# In manager.py DEFAULT_CONFIG:
DEFAULT_CONFIG = {
    ...
    "css_prefix": "",  # new key
}

# Access:
config = get_theme_config()
prefix = config["css_prefix"]
```

## Prefix Flow

### 1. CSS Generation (components.css replacement)

**Problem**: `components.css` is a static file. With a configurable prefix, it must become dynamic.

**Solution**: New function `generate_component_css(prefix="")` in a new module `component_css_generator.py` (or add to existing `css_generator.py`).

- Takes the prefix as an argument
- Returns CSS string with all class names prefixed
- Called from `theme_head` template tag (already generates CSS dynamically)

**theme_head.html change**: Instead of `<link rel="stylesheet" href="{% static 'djust_theming/css/components.css' %}">`, render inline `<style>` for component CSS when prefix is set, or keep the static link when prefix is empty.

### 2. Template Rendering (component templates)

Each component template hardcodes class names:
- `button.html`: `class="btn btn-{{ variant }} btn-{{ size }}"`
- `card.html`: `class="card"`, `class="card-header"`, etc.
- `alert.html`: `class="alert alert-{{ variant }}"`, etc.
- `badge.html`: `class="badge badge-{{ variant }}"`
- `input.html`: `class="input-group"`, `class="input-label"`, `class="input"`
- `theme_switcher.html`: `class="theme-switcher"`, `class="theme-mode-controls"`, etc.

**Solution**: Pass `css_prefix` into every component template context, then use it:

```html
<!-- button.html -->
<button class="{{ css_prefix }}btn {{ css_prefix }}btn-{{ variant }} {{ css_prefix }}btn-{{ size }}">
```

**How prefix reaches templates**:
- `theme_components.py` inclusion tags: Add `css_prefix` to each tag's returned context dict by reading `get_theme_config()["css_prefix"]`.
- `theme_tags.py` for `theme_switcher`: Add `css_prefix` to `ThemeSwitcher.get_context()` and `ThemeSwitcherConfig`.
- `theme_head` tag: Already has access to `get_theme_config()`.

### 3. theme_css_generator.py

`_generate_component_styles()` generates `.btn` / `.card` / `.form-input` selectors. These must use the prefix.

**Solution**: Pass prefix into `CompleteThemeCSSGenerator.__init__()` and use it in `_generate_component_styles()`.

### 4. performance.css

This static file references `.btn`, `.card`, `.badge`, `.alert`, `.theme-switcher`, etc.

**Solution for v1**: Document that `performance.css` does not support prefixing. If prefix is set, the `theme_head` tag should either:
- Skip including `performance.css` and generate a prefixed version inline, OR
- Include it as-is (the selectors won't match, so they're harmless dead CSS)

**Recommended**: Option B for v1 simplicity. Performance.css optimizations are nice-to-have, not critical. Dead selectors cause zero harm.

## Class Name Inventory (components.css)

Classes that need prefixing:

| Component | Classes |
|-----------|---------|
| Alert | `alert`, `alert-content`, `alert-title`, `alert-message`, `alert-dismiss`, `alert-default`, `alert-success`, `alert-warning`, `alert-destructive` |
| Badge | `badge`, `badge-default`, `badge-secondary`, `badge-success`, `badge-warning`, `badge-destructive`, `badge-outline` |
| Button | `btn`, `btn-sm`, `btn-md`, `btn-lg`, `btn-primary`, `btn-secondary`, `btn-destructive`, `btn-ghost`, `btn-link` |
| Card | `card`, `card-header`, `card-title`, `card-body`, `card-footer` |
| Input | `input-group`, `input-label`, `input` |
| Theme Switcher | `theme-switcher`, `theme-mode-controls`, `theme-mode-btn`, `theme-preset-select`, `theme-preset-controls` |

## Implementation Plan

### Files to modify:

1. **`manager.py`** — Add `"css_prefix": ""` to `DEFAULT_CONFIG`
2. **`component_css_generator.py`** (NEW) — Function `generate_component_css(prefix: str = "") -> str` that returns components.css content with prefix applied to all class selectors
3. **`theme_css_generator.py`** — Accept `css_prefix` param, pass to `_generate_component_styles()`
4. **`templatetags/theme_tags.py`** — In `theme_head()`, conditionally generate component CSS inline (when prefix is set) instead of linking static file; pass `css_prefix` to template
5. **`templatetags/theme_components.py`** — Add `css_prefix` to every inclusion tag context
6. **`templates/djust_theming/theme_head.html`** — Support inline component CSS block
7. **`templates/djust_theming/components/*.html`** (all 5 templates) — Use `{{ css_prefix }}` before each class name
8. **`templates/djust_theming/theme_switcher.html`** — Use `{{ css_prefix }}` before each class name
9. **`components.py`** — Add `css_prefix` to `ThemeSwitcher.get_context()` and `ThemeModeButton.get_context()`
10. **`checks.py`** — Add system check: warn if `css_prefix` is set but doesn't end with `-`

### Files NOT modified:
- `base.css` — Utility classes, opt-in, not prefixed
- `performance.css` — Dead selectors are harmless when prefix is active
- `css_generator.py` — Color CSS variables, no class selectors to prefix

### New files:
- `component_css_generator.py` — Generates prefixed component CSS

## Test Strategy

### New test file: `tests/test_css_prefix.py`

1. **test_default_prefix_empty** — `get_theme_config()["css_prefix"]` is `""` by default
2. **test_prefix_in_generated_component_css** — With prefix `"dj-"`, `generate_component_css("dj-")` output contains `.dj-btn` not `.btn`
3. **test_no_prefix_backward_compat** — With empty prefix, output is identical to current `components.css`
4. **test_prefix_in_theme_css_generator** — `CompleteThemeCSSGenerator` with prefix generates `.dj-btn` in component styles
5. **test_component_template_context_has_prefix** — Each inclusion tag returns `css_prefix` in context
6. **test_theme_head_inline_css_when_prefix** — When prefix is set, `theme_head` renders inline component CSS
7. **test_theme_head_static_link_when_no_prefix** — When no prefix, `theme_head` links to static `components.css`
8. **test_system_check_warns_on_bad_prefix** — Prefix without trailing `-` triggers warning

### Existing tests:
- All 67 existing tests must continue to pass (backward compat)

## Backward Compatibility

- Default `css_prefix` is `""` — zero change for existing users
- When prefix is empty, `theme_head` still links to the static `components.css` file (no performance regression)
- Component templates render identical HTML when prefix is empty (`{{ css_prefix }}btn` = `btn`)
- No breaking changes to any public API

## Risk Assessment

- **Low risk**: Configuration is opt-in, default is empty string
- **Template changes**: Simple string concatenation, easily auditable
- **CSS generation**: New module, doesn't touch existing `css_generator.py`
- **Performance**: When prefix is empty, no change. When set, component CSS is inlined (same as theme CSS already is)
