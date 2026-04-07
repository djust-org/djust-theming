# I2: Extract Component CSS from Templates -- Analysis

**Date**: 2026-03-22
**Branch**: task/I2-extract-component-css
**Status**: Analysis complete

---

## 1. Component Templates with Inline `<style>` Blocks

Six templates contain `<style>` blocks that must be extracted:

| Template | Style Lines | CSS Classes Defined |
|---|---|---|
| `components/alert.html` (L20-82) | 62 lines | `.alert`, `.alert-content`, `.alert-title`, `.alert-message`, `.alert-dismiss`, `.alert-default`, `.alert-success`, `.alert-warning`, `.alert-destructive` |
| `components/badge.html` (L6-49) | 43 lines | `.badge`, `.badge-default`, `.badge-secondary`, `.badge-success`, `.badge-warning`, `.badge-destructive`, `.badge-outline` |
| `components/button.html` (L8-99) | 91 lines | `.btn`, `.btn:focus-visible`, `.btn:disabled`, `.btn-sm`, `.btn-md`, `.btn-lg`, `.btn-primary`, `.btn-secondary`, `.btn-destructive`, `.btn-ghost`, `.btn-link` |
| `components/card.html` (L18-47) | 29 lines | `.card`, `.card-header`, `.card-title`, `.card-body`, `.card-footer` |
| `components/input.html` (L18-59) | 41 lines | `.input-group`, `.input-label`, `.input`, `.input::placeholder`, `.input:focus`, `.input:disabled` |
| `theme_switcher.html` (L68-145) | 77 lines | `.theme-switcher`, `.theme-mode-controls`, `.theme-mode-btn`, `.theme-mode-btn:hover`, `.theme-mode-btn.active`, `.theme-mode-btn svg`, `.theme-preset-select`, dark mode overrides |

**Templates WITHOUT inline styles** (already pure HTML):
- `components/preset_selector_dropdown.html`
- `components/preset_selector_grid.html`
- `components/preset_selector_list.html`
- `components/theme_mode_button.html`
- `theme_head.html`

---

## 2. Current CSS Inclusion via `{% theme_head %}`

`theme_tags.py:theme_head()` (L35-95) renders `theme_head.html` which outputs:
1. Anti-FOUC inline script (sets `data-theme` attribute before paint)
2. `{{ css_block }}` -- theme CSS custom properties (variables like `--primary`, `--background`, etc.)
3. Optional `<script src="theme.js">` include

The `css_block` is either inline `<style>` or a `<link>` tag pointing to a CSS endpoint. It contains **only CSS custom property definitions** (theme tokens), NOT component styles.

Component CSS is currently duplicated in the DOM every time a component template is rendered.

---

## 3. Existing Static CSS Structure

```
djust_theming/static/djust_theming/css/
  base.css          -- Full design system (~1400 lines): tokens, layout, components, utilities, animations
  performance.css   -- Transition optimizations, scroll perf, reduced-motion (~274 lines)
```

### CRITICAL: `base.css` Already Has Component Styles

`base.css` defines its own versions of the same component classes:

| Component | base.css Location | Inline Template Location | Overlap? |
|---|---|---|---|
| `.btn` / buttons | L396-495 | `button.html` L8-99 | YES -- different definitions |
| `.card` | L497-533 | `card.html` L18-47 | YES -- different definitions |
| `.badge` | L686-748 | `badge.html` L6-49 | YES -- different variants (base.css has `.badge-primary`, `.badge-danger`; inline has `.badge-default`, `.badge-destructive`) |
| `.alert` | L750-792 | `alert.html` L20-82 | YES -- different variant names (base.css has `.alert-danger`; inline has `.alert-destructive`) |
| `.input` / forms | L535-653 | `input.html` L18-59 | PARTIAL -- base.css has richer form styles |
| `.theme-*` switcher | Not in base.css | `theme_switcher.html` L68-145 | NO -- only in inline |

The inline template styles and `base.css` are **not identical** -- they use different variant naming conventions and have different property values. This is a source of confusion and potential conflicts depending on load order.

---

## 4. `theme_head.html` Template

Located at `djust_theming/templates/djust_theming/theme_head.html` (19 lines).

Renders:
1. Anti-FOUC script
2. `{{ css_block }}` (theme variable CSS)
3. Optional JS include

This template is the natural injection point for a `<link>` to the new `components.css` file.

---

## 5. Proposed Refactoring Approach

### Strategy: Consolidate into a single `components.css` file

Per the ROADMAP guidance: "Move component CSS to `static/djust_theming/css/components/button.css` (one file per component) or consolidate into `base.css`."

Recommended: Create a **single** `components.css` file rather than per-component files. Rationale:
- Only 6 components with styles -- splitting into 6 tiny files adds HTTP requests for minimal benefit
- Simpler for theme authors to override one file
- ROADMAP I7 (tree-shaking) is a future task -- premature to split now

### Step-by-step Plan

**Step 1: Reconcile inline styles with base.css styles**

The inline template styles and `base.css` define overlapping but different CSS for the same class names. We must decide which is canonical:
- **Inline template styles** use naming consistent with the component tag API (e.g., `btn-destructive`, `badge-destructive`, `alert-destructive`)
- **base.css styles** use a different convention (e.g., `btn-danger`, `badge-danger`, `alert-danger`)

Decision: The **inline template styles are canonical** since they match the component API (`variant="destructive"` maps to `.alert-destructive`). The `base.css` versions serve a different purpose (generic design system for manual HTML usage).

Action: The new `components.css` will contain the inline template styles. The `base.css` component sections remain as-is (they serve users who use `base.css` directly without the component tags). No removal from `base.css` in this task.

**Step 2: Create `static/djust_theming/css/components.css`**

Extract all `<style>` block content from the 6 templates into a single file, organized by component:
1. Alert styles (from `alert.html`)
2. Badge styles (from `badge.html`)
3. Button styles (from `button.html`)
4. Card styles (from `card.html`)
5. Input styles (from `input.html`)
6. Theme switcher styles (from `theme_switcher.html`)

**Step 3: Remove `<style>` blocks from all 6 templates**

Each template becomes pure HTML structure only.

**Step 4: Update `theme_head.html` to include `components.css`**

Add a `<link>` tag for the new stylesheet:
```html
<link rel="stylesheet" href="{% static 'djust_theming/css/components.css' %}">
```

This requires adding `{% load static %}` to the template.

**Step 5: Update `theme_tags.py:theme_head()` to pass component CSS path**

Either:
- (a) Add the static file reference directly in `theme_head.html` using `{% static %}`, OR
- (b) Pass the URL as a context variable from `theme_head()` to the template

Option (a) is simpler and preferred.

**Step 6: Update tests**

- Verify component templates no longer contain `<style>` blocks
- Verify `{% theme_head %}` output includes the `components.css` link
- Verify component rendering still produces correct HTML (no style tags)

---

## 6. Files Affected

### Modified
| File | Change |
|---|---|
| `djust_theming/templates/djust_theming/components/alert.html` | Remove `<style>` block (L20-82) |
| `djust_theming/templates/djust_theming/components/badge.html` | Remove `<style>` block (L6-49) |
| `djust_theming/templates/djust_theming/components/button.html` | Remove `<style>` block (L8-99) |
| `djust_theming/templates/djust_theming/components/card.html` | Remove `<style>` block (L18-47) |
| `djust_theming/templates/djust_theming/components/input.html` | Remove `<style>` block (L18-59) |
| `djust_theming/templates/djust_theming/theme_switcher.html` | Remove `<style>` block (L68-145) |
| `djust_theming/templates/djust_theming/theme_head.html` | Add `{% load static %}` and `<link>` for `components.css` |

### Created
| File | Content |
|---|---|
| `djust_theming/static/djust_theming/css/components.css` | Consolidated CSS from all 6 templates (~343 lines) |

### NOT Modified (intentionally)
| File | Reason |
|---|---|
| `djust_theming/templatetags/theme_tags.py` | No changes needed if `theme_head.html` uses `{% static %}` directly |
| `djust_theming/static/djust_theming/css/base.css` | Separate design system file; overlapping styles serve different use case |
| `djust_theming/static/djust_theming/css/performance.css` | Unrelated to this task |
| `djust_theming/components.py` | No inline CSS rendering found |
| `djust_theming/mixins.py` | No inline CSS rendering found (I1 already moved HTML to templates) |

---

## 7. Risk Assessment

### Low Risk
- **Template changes are mechanical**: Removing `<style>` blocks is straightforward deletion with no logic changes
- **CSS content is unchanged**: The CSS moves verbatim; no rules are added, removed, or modified
- **Backward compatible**: Pages that already include `base.css` will still work (base.css has its own component styles)

### Medium Risk
- **Duplicate CSS definitions**: After extraction, both `components.css` and `base.css` will define styles for `.btn`, `.card`, `.badge`, `.alert` with different variant names. If a page loads both, the cascade order matters. This is an existing problem (inline styles already conflict with base.css) -- extraction does not make it worse, but does not fix it either. **Recommend documenting this as a follow-up task.**
- **Cache invalidation**: New static file means first load after upgrade requires a fresh fetch. Using Django's `ManifestStaticFilesStorage` or a version query param mitigates this. The current `theme.js` already uses manual `?v=` versioning.
- **Theme authors overriding templates**: If a theme author has overridden a component template AND kept the `<style>` block, they will now get double CSS (their override's inline + the new `components.css`). **Recommend documenting in CHANGELOG as a breaking change with migration guidance.**

### No Risk
- **Templates without styles**: 4 component templates and `theme_head.html` have no inline styles and are unaffected
- **Python code**: No Python files need modification (template tag context, component classes are unaffected)
- **JavaScript**: `theme.js` is unaffected

---

## 8. Open Questions

1. **Should `base.css` component sections be deprecated?** The existence of both `components.css` and `base.css` component styles is confusing. Recommend adding a deprecation comment to the base.css component sections pointing to `components.css` as the canonical source. Full removal is a separate task.

2. **Should `components.css` be included unconditionally?** Current plan includes it via `{% theme_head %}`. If a page does not use `{% theme_head %}` but uses component tags directly, they lose styling. This matches the existing contract (components always required `{% theme_head %}` for theme variables anyway).

3. **`{% static %}` tag in `theme_head.html`**: This requires `{% load static %}` in the template. Since `theme_head.html` uses `{% autoescape off %}`, we need to verify `{% load static %}` works correctly alongside it. (It does -- `{% load %}` is independent of autoescape context.)
