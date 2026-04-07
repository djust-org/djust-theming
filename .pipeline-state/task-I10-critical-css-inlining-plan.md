# I10: Critical CSS Inlining — Implementation Plan

## Problem

All theme CSS is currently delivered as a single block — either fully inlined in a `<style>` tag or fully linked via a `<link>` tag. This means ~10-20KB of CSS blocks first paint, including component styles and utilities that aren't needed until after the page renders.

## Design

### CSS Split Definition

**Critical CSS** (inlined in `<style>`, ~2-4KB) — needed for first paint:
- `@layer` order declaration
- `:root` CSS custom properties (color tokens, light mode)
- Dark mode selectors (`.dark`, `[data-theme="dark"]`)
- System preference media query
- Design tokens (spacing, typography, shadows, border-radius, animation vars)
- Theme-specific `:root` vars from `CompleteThemeCSSGenerator._generate_theme_vars()`

**Deferred CSS** (async-loaded via `<link>`, larger) — not needed for first paint:
- Base styles (body resets, transition rules, `*` selectors)
- Utility classes (`.bg-*`, `.text-*`, `.border-*`, etc.)
- Typography utility classes (`.font-sans`, `.text-xs`, etc.)
- Component styles (`.btn`, `.card`, `.form-input`, etc.)

### Delivery Mechanism

When `critical_css` is enabled (default):
1. Critical CSS goes in `<style data-djust-theme-critical>` tag (inlined)
2. Deferred CSS goes via: `<link rel="preload" href="..." as="style" onload="this.onload=null;this.rel='stylesheet'">`
3. `<noscript><link rel="stylesheet" href="..."></noscript>` fallback
4. A new Django view serves the deferred CSS at a URL endpoint

When `critical_css` is disabled:
- Current behavior preserved — all CSS in one `<style>` or `<link>` block

### Configuration

```python
LIVEVIEW_CONFIG = {
    "theme": {
        "critical_css": True,  # default: True. False = inline everything (legacy behavior)
    }
}
```

### Files to Change

1. **`djust_theming/css_generator.py`** — Add `generate_critical_css()` and `generate_deferred_css()` methods to `ThemeCSSGenerator`
2. **`djust_theming/theme_css_generator.py`** — Add `generate_critical_css()` and `generate_deferred_css()` methods to `CompleteThemeCSSGenerator`
3. **`djust_theming/manager.py`** — Add `generate_critical_css_for_state()` and `generate_deferred_css_for_state()` functions; add `critical_css` to `DEFAULT_CONFIG`
4. **`djust_theming/views.py`** — Add `deferred_theme_css` view endpoint
5. **`djust_theming/urls.py`** — Add URL pattern for deferred CSS view
6. **`djust_theming/templatetags/theme_tags.py`** — Update `theme_head()` to split CSS when `critical_css` is enabled
7. **`djust_theming/templates/djust_theming/theme_head.html`** — Add deferred CSS loading markup
8. **`tests/test_critical_css.py`** — TDD tests

### Implementation Order

1. Write tests (TDD)
2. Add `generate_critical_css()` / `generate_deferred_css()` to `ThemeCSSGenerator`
3. Add same split to `CompleteThemeCSSGenerator`
4. Add `generate_critical_css_for_state()` / `generate_deferred_css_for_state()` to manager
5. Add deferred CSS view + URL
6. Update `theme_head()` tag and template
7. Update CHANGELOG
