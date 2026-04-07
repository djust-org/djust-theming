# Plan: Phase 1.1 + I9 — Template Namespace Resolution + CSS Cascade Layers

**Branch:** `task/1.1-I9-template-resolution-css-layers`
**Date:** 2026-03-23
**Status:** PLANNING

---

## Part A: Phase 1.1 — Template Namespace Resolution

### Problem

All component template tags in `theme_components.py` use hardcoded template paths (e.g., `@register.inclusion_tag('djust_theming/components/button.html')`). There is no way for a theme to provide its own template override for a component. A "corporate" theme might want a completely different button HTML structure, but currently the only customization is via CSS variables.

### Current Architecture

1. **`theme_components.py`** — 5 inclusion tags (`theme_button`, `theme_card`, `theme_badge`, `theme_alert`, `theme_input`) + 1 simple tag (`theme_icon`). All use `@register.inclusion_tag(...)` with static template paths.

2. **`theme_tags.py`** — `theme_switcher` uses `@register.inclusion_tag(...)` with a static path. `theme_mode_toggle` and `theme_preset_selector` use `render_to_string()` with static paths via `components.py`.

3. **`components.py`** — `ThemeSwitcher`, `ThemeModeButton`, `PresetSelector` classes call `render_to_string()` with hardcoded template paths.

4. **`manager.py`** — `ThemeState` holds `theme` (design system name like "material"), `preset` (color preset name), `mode`, and `pack`. The active theme name is available via `state.theme`. Access to `ThemeManager` requires `request` (from session/cookies).

5. **Templates** — All live under `djust_theming/templates/djust_theming/components/*.html` and `djust_theming/templates/djust_theming/theme_*.html`.

### Design Decisions

#### D1: How to get the active theme name in template tags

The `theme_components.py` tags do NOT take context (`takes_context=False`), so they have no access to `request`. The `theme_tags.py` tags DO take context and already call `get_theme_manager(request)`.

**Decision:** Convert the 5 `theme_components.py` inclusion tags from `@register.inclusion_tag(...)` to `@register.simple_tag(takes_context=True)` that manually call `render_to_string()` with a dynamically resolved template path. This follows the same pattern already used by `theme_mode_toggle` and `theme_preset_selector` in `theme_tags.py`.

The `theme_switcher` inclusion tag in `theme_tags.py` also needs conversion since it has a hardcoded template path.

#### D2: Template fallback chain (`select_template`)

Use Django's `django.template.loader.select_template()` which tries templates in order and uses the first one found.

**Fallback chain for a component (e.g., "button"):**
```
1. djust_theming/themes/{theme_name}/components/button.html   (theme-specific override)
2. djust_theming/components/button.html                        (default)
```

For the theme switcher:
```
1. djust_theming/themes/{theme_name}/theme_switcher.html
2. djust_theming/theme_switcher.html
```

**Why `themes/{theme_name}/...` instead of `{theme_name}/...`?** Keeps overrides namespaced under `djust_theming/themes/` to avoid collisions with user app templates.

#### D3: Which tags need to become dynamic

All tags that render templates:

| Tag | File | Current Mechanism | Change Needed |
|-----|------|-------------------|---------------|
| `theme_button` | `theme_components.py` | `@register.inclusion_tag` (static) | Convert to `simple_tag` + `select_template` |
| `theme_card` | `theme_components.py` | `@register.inclusion_tag` (static) | Convert to `simple_tag` + `select_template` |
| `theme_badge` | `theme_components.py` | `@register.inclusion_tag` (static) | Convert to `simple_tag` + `select_template` |
| `theme_alert` | `theme_components.py` | `@register.inclusion_tag` (static) | Convert to `simple_tag` + `select_template` |
| `theme_input` | `theme_components.py` | `@register.inclusion_tag` (static) | Convert to `simple_tag` + `select_template` |
| `theme_switcher` | `theme_tags.py` | `@register.inclusion_tag` (static) | Convert to `simple_tag` + `select_template` |
| `theme_mode_toggle` | `theme_tags.py` | `render_to_string` (static path) | Use `select_template` |
| `theme_preset_selector` | `theme_tags.py` | `render_to_string` (static path) | Use `select_template` |

The `theme_icon` simple tag renders inline SVG (no template) — no change needed.

The Python classes in `components.py` (`ThemeSwitcher`, `ThemeModeButton`, `PresetSelector`) also need updating since they call `render_to_string` with hardcoded paths.

#### D4: Handle case where no theme override exists (graceful fallback)

`select_template()` handles this natively. If the theme-specific template does not exist, it falls to the default. No extra error handling needed — `select_template()` raises `TemplateDoesNotExist` only if ALL candidates are missing, which can't happen since the default template ships with the package.

#### D5: Helper function for template resolution

Create a utility function to avoid code duplication:

```python
# In a new file: djust_theming/template_resolver.py
# Or at the top of theme_components.py

from django.template.loader import select_template
from .manager import get_theme_manager

def resolve_component_template(request, component_name: str) -> str:
    """
    Resolve the template for a component, checking theme-specific override first.

    Args:
        request: Django HttpRequest (for theme state)
        component_name: e.g., "button", "card", "theme_switcher"

    Returns:
        Template object from select_template()
    """
    manager = get_theme_manager(request)
    state = manager.get_state()
    theme_name = state.theme

    # For components under components/ subdirectory
    candidates = [
        f"djust_theming/themes/{theme_name}/components/{component_name}.html",
        f"djust_theming/components/{component_name}.html",
    ]

    return select_template(candidates)
```

A second variant for top-level templates (theme_switcher, theme_head):

```python
def resolve_theme_template(request, template_name: str):
    manager = get_theme_manager(request)
    state = manager.get_state()
    theme_name = state.theme

    candidates = [
        f"djust_theming/themes/{theme_name}/{template_name}.html",
        f"djust_theming/{template_name}.html",
    ]

    return select_template(candidates)
```

### Implementation Steps (1.1)

1. **Create `djust_theming/template_resolver.py`** with `resolve_component_template()` and `resolve_theme_template()` helpers.

2. **Modify `theme_components.py`:**
   - Change all 5 inclusion tags from `@register.inclusion_tag(...)` to `@register.simple_tag(takes_context=True)`.
   - Each tag: get request from context, resolve template via helper, render with `render_to_string`, return `mark_safe(html)`.
   - Still pass the same context dict (text, variant, size, attrs, css_prefix).

3. **Modify `theme_tags.py`:**
   - `theme_switcher`: convert from `@register.inclusion_tag` to `@register.simple_tag(takes_context=True)` with dynamic template resolution.
   - `theme_mode_toggle`: already a simple_tag — update the `ThemeModeButton.render()` call or resolve template inline.
   - `theme_preset_selector`: already a simple_tag — update `PresetSelector.render()` call or resolve template inline.

4. **Modify `components.py`:**
   - `ThemeSwitcher.render()`: accept optional `request` parameter or use stored manager to resolve template.
   - `ThemeModeButton.render()`: same approach.
   - `PresetSelector._render_*()`: same approach.

5. **Add tests:**
   - Test that default templates are used when no override exists.
   - Test that theme-specific templates are used when they exist (create temp templates in test).
   - Test fallback behavior.

---

## Part B: I9 — CSS Cascade Layers

### Problem

All generated CSS (tokens, base styles, utilities, component styles, theme pack styles) exists in a flat cascade. This makes specificity unpredictable when:
- Theme authors want to override component styles
- Multiple CSS sources combine (inline generated + static `components.css`)
- Users add their own custom CSS

### Current CSS Architecture

1. **`css_generator.py` (`ThemeCSSGenerator`)** — Generates:
   - `:root { ... }` — light mode CSS custom properties (tokens)
   - `.dark, [data-theme="dark"] { ... }` — dark mode overrides
   - `@media (prefers-color-scheme: dark)` — system preference
   - Base styles (body, *, transitions)
   - Utility classes (.bg-*, .text-*, .border-*, .btn-*, .card-theme, etc.)

2. **`theme_css_generator.py` (`CompleteThemeCSSGenerator`)** — Generates:
   - All of the above via `ColorCSSGenerator.generate_css()`
   - `:root { ... }` theme-specific vars (typography, spacing, radius, shadows, animations)
   - Typography utility classes
   - Component styles (.btn, .card, .form-input) based on theme's component_styles config

3. **`component_css_generator.py`** — Reads `static/djust_theming/css/components.css` and optionally applies prefix. This CSS contains the actual component styles used by template tags.

4. **`pack_css_generator.py`** — Generates all of the above plus icon, animation, pattern, interaction, and illustration styles.

5. **`static/djust_theming/css/components.css`** — Flat CSS file with alert, badge, button, card, input, theme-switcher styles. Loaded via `<link>` or inlined with prefix.

6. **`static/djust_theming/css/base.css`** — Large file with additional base styles.

### Design Decisions

#### D6: Layer order

```css
@layer base, tokens, components, theme;
```

- **`base`** — Reset/base styles (body background, *, transitions, reduced-motion). Lowest priority.
- **`tokens`** — CSS custom properties (:root vars, dark mode vars, system preference media query, design tokens).
- **`components`** — Component styles from `components.css` and theme-generated component styles (.btn, .card, .form-input, etc.), plus utility classes.
- **`theme`** — Theme author overrides. Highest priority. This layer is declared empty by the framework; theme authors populate it.

**Why this order?**
- Tokens in their own layer because they're variable declarations that shouldn't compete with selectors.
- Components above tokens so component selectors can use `hsl(var(...))` references and be overridable.
- Theme layer on top gives theme authors a guaranteed way to override anything without `!important`.

#### D7: Where each layer wrapping happens

| CSS Source | Layer | Where Wrapping Happens |
|-----------|-------|----------------------|
| Base styles (`_generate_base_styles`) | `base` | `css_generator.py` — wrap output in `@layer base { ... }` |
| `:root` vars, dark mode, system pref, design tokens | `tokens` | `css_generator.py` — wrap output in `@layer tokens { ... }` |
| Utility classes (`_generate_utilities`) | `components` | `css_generator.py` — wrap output in `@layer components { ... }` |
| Typography classes | `components` | `theme_css_generator.py` — wrap output in `@layer components { ... }` |
| Theme component styles (.btn, .card, .form-input) | `components` | `theme_css_generator.py` — wrap output in `@layer components { ... }` |
| `components.css` (static file) | `components` | Add `@layer components { ... }` wrapper to static file |
| `component_css_generator.py` output | `components` | Wrap the output of `generate_component_css()` |
| Pack styles (icon, animation, pattern, etc.) | `theme` | `pack_css_generator.py` — wrap pack-specific additions in `@layer theme { ... }` |

#### D8: Layer order declaration placement

The `@layer base, tokens, components, theme;` declaration MUST appear before any `@layer` block. It will be:

- Emitted as the very first line of generated CSS in `ThemeCSSGenerator.generate_css()` and `CompleteThemeCSSGenerator.generate_css()`.
- Also included in `components.css` as a comment reference (the actual declaration comes from the generated CSS which loads first via `{% theme_head %}`).

#### D9: How theme author CSS gets into the 'theme' layer

Theme authors use:
```css
@layer theme {
  .btn { /* custom overrides */ }
}
```

The framework documents this convention. The `theme` layer is declared in the layer order but left empty by the framework. Since the layer order is declared upfront, even if the theme author's CSS loads after the framework CSS, their `@layer theme { ... }` block will have higher priority than `@layer components { ... }`.

This requires no framework code changes beyond declaring the layer order — it's a CSS convention that theme authors follow.

#### D10: Backward compatibility

Wrapping existing CSS in `@layer` blocks is a **breaking change** for users who have custom CSS that relies on the current flat cascade. However:
- The layer order declaration ensures the framework's own styles layer correctly.
- Users without custom CSS see no difference.
- Users with custom CSS can wrap theirs in `@layer theme { ... }` for guaranteed override.
- Add a `LIVEVIEW_CONFIG["theme"]["use_css_layers"]` boolean (default `True`) to allow opting out during migration.

### Implementation Steps (I9)

1. **Add layer order config:**
   - Add `"use_css_layers": True` to `DEFAULT_CONFIG` in `manager.py`.
   - Add `"css_layer_order": "base, tokens, components, theme"` to `DEFAULT_CONFIG`.

2. **Modify `css_generator.py` (`ThemeCSSGenerator`):**
   - Add `use_layers: bool` parameter (read from config).
   - In `generate_css()`: emit `@layer base, tokens, components, theme;` as first line.
   - Wrap `_generate_light_mode()` + `_generate_dark_mode()` + `_generate_system_preference()` + design tokens output in `@layer tokens { ... }`.
   - Wrap `_generate_base_styles()` output in `@layer base { ... }`.
   - Wrap `_generate_utilities()` output in `@layer components { ... }`.
   - When `use_layers=False`, emit CSS as today (no wrapping).

3. **Modify `theme_css_generator.py` (`CompleteThemeCSSGenerator`):**
   - Read `use_css_layers` from config.
   - Wrap `_generate_theme_vars()` in `@layer tokens { ... }`.
   - Wrap `_generate_typography_classes()` in `@layer components { ... }`.
   - Wrap `_generate_component_styles()` in `@layer components { ... }`.
   - The layer order declaration comes from the inner `ColorCSSGenerator` output, so don't duplicate it.

4. **Modify `component_css_generator.py`:**
   - Read `use_css_layers` from config.
   - Wrap the output of `generate_component_css()` in `@layer components { ... }`.

5. **Modify static `components.css`:**
   - Wrap entire file contents in `@layer components { ... }`.
   - This handles the case when it's loaded via `<link>` tag (no prefix).

6. **Modify `pack_css_generator.py`:**
   - Wrap pack-specific additions (icon, animation, pattern, interaction, illustration) in `@layer theme { ... }`.
   - The base theme CSS from `CompleteThemeCSSGenerator` already handles its own layers.

7. **Update `theme_head.html` / `theme_tags.py`:**
   - No changes needed if layer declarations are inside the generated CSS.

8. **Add tests:**
   - Test that generated CSS contains `@layer` declarations when enabled.
   - Test that `@layer` is absent when `use_css_layers=False`.
   - Test correct nesting / order of layers.
   - Test `components.css` wrapping.

---

## File Change Summary

### New Files
- `djust_theming/template_resolver.py` — Template resolution helpers

### Modified Files
- `djust_theming/templatetags/theme_components.py` — Convert inclusion_tags to simple_tags with dynamic template resolution
- `djust_theming/templatetags/theme_tags.py` — Dynamic template resolution for theme_switcher, mode_toggle, preset_selector
- `djust_theming/components.py` — Dynamic template resolution in render methods
- `djust_theming/manager.py` — Add `use_css_layers` and `css_layer_order` config defaults
- `djust_theming/css_generator.py` — Add `@layer` wrapping to generated CSS sections
- `djust_theming/theme_css_generator.py` — Add `@layer` wrapping to theme vars, typography, component styles
- `djust_theming/component_css_generator.py` — Add `@layer components` wrapping to output
- `djust_theming/pack_css_generator.py` — Add `@layer theme` wrapping to pack-specific styles
- `djust_theming/static/djust_theming/css/components.css` — Wrap in `@layer components`
- `tests/` — New test files for template resolution and CSS layers

### Unchanged Files
- `djust_theming/templates/djust_theming/components/*.html` — No changes to default templates
- `djust_theming/templates/djust_theming/theme_*.html` — No changes to default templates
- `djust_theming/context_processors.py` — No changes (does not use component template resolution)

---

## Implementation Order

1. **Phase 1.1 first** (template resolution) — It's self-contained and touches different code than I9.
2. **I9 second** (CSS layers) — Builds on the stable base.
3. Run full test suite after each phase.

## Risk Assessment

- **Template resolution:** Low risk. `select_template` is a standard Django pattern. Existing behavior is preserved since the default template always exists in the fallback chain.
- **CSS layers:** Medium risk. Wrapping in `@layer` changes cascade behavior. The opt-out config (`use_css_layers`) mitigates this. Need thorough CSS output testing.
- **Backward compatibility:** The `use_css_layers=True` default means existing users get layers automatically. If any user has custom CSS that depends on specificity ordering, they'll need to wrap it in `@layer theme { ... }`. Documenting this is essential.
