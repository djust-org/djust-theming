# djust-theming Roadmap

> Goal: A complete theming system where full customization of look and feel is achieved by writing a new template set + design tokens. No Python code required to create a theme.

## Current State (v1.1.2)

What works today:
- 19 color presets (HSL-based, light/dark mode)
- 11 design systems (Material, iOS, Fluent, etc.) — CSS-only, no template variants
- 5 component templates (button, card, badge, alert, input)
- CSS variable generation pipeline (color + typography + spacing + shadows)
- Live theme switching via djust LiveView (no page reload)
- Tailwind CSS and shadcn/ui export/import
- Theme state persistence (cookies, session, localStorage)
- CLI management command

What's missing for "write a template, get a theme":
- Components are CSS-variable-driven but share one set of HTML templates — changing look requires CSS overrides, not template swaps
- No template discovery/override mechanism for theme packages
- Only 5 component templates — missing navigation, modals, tables, forms, etc.
- No layout templates (sidebar, topbar, full-page layouts)
- No page templates (login, error, dashboard shell)
- Design systems only output CSS — they should also provide template variants
- No way to package and distribute a complete theme
- ~~Component CSS is embedded in each template via `<style>` blocks — duplicated on every render, not deduplicated or cacheable~~ (Fixed: I2 extracted to `components.css`)
- No RTL/bidirectional layout support
- No responsive/breakpoint-aware token system
- No visual regression testing for theme authors

---

## Improvements: Fix Before Building New (Priority: Do First)

These are concrete issues found in the current codebase. They should be addressed before the phased work below, as several unblock Phase 1.

### ~~I1: Decouple Inline HTML from Python~~ (DONE — PR #7)

**Status**: Completed. Inline HTML/SVG/CSS removed from `mixins.py`, `components.py`, and `theme_tags.py`. All rendering now goes through Django templates. `theme_switcher.html` uses a `liveview` context variable to switch between `dj-click` (LiveView) and `data-djust-event` (vanilla) event bindings. 5 new templates created: `theme_head.html`, `theme_mode_button.html`, `preset_selector_dropdown.html`, `preset_selector_grid.html`, `preset_selector_list.html`.

### ~~I2: Extract Component CSS from Templates~~ (DONE — PR #8)

**Status**: Completed. Inline `<style>` blocks extracted from 6 component templates into `static/djust_theming/css/components.css`. Templates are now pure HTML. `{% theme_head %}` includes `components.css` automatically via `<link>` tag. Note: `base.css` retains its own component styles (different variant naming) for users who use `base.css` directly without template tags.

### ~~I3: ThemeManager Reinstantiates on Every Tag~~ (DONE — PR #9)

**Status**: Completed. New `get_theme_manager(request)` helper caches the `ThemeManager` instance on `request._djust_theme_manager`. All internal call sites (template tags, context processors, views, `ThemeMixin`) now use `get_theme_manager()` instead of `ThemeManager(request=request)`. `get_theme_manager` is exported from the top-level package.

### ~~I4: Static Asset Versioning~~ (DONE — PR #10)

**Status**: Completed. Replaced all manual `?v=N` cache busters with Django's `{% static %}` tag (in templates) and `staticfiles_storage.url()` (in Python). Fixed the version mismatch between theme_tags.py (v=2) and mixins.py (v=3). Now works automatically with `ManifestStaticFilesStorage` for content-hash-based cache busting.

### ~~I5: CSS Generation Caching~~ (DONE — PR #11)

**Status**: Completed. Added `@lru_cache` to all 4 CSS generation convenience functions. All call sites refactored to use cached functions. Added `clear_css_cache()` utility in `djust_theming/cache.py` for development-time invalidation. None-preset normalization prevents duplicate cache entries.

### ~~I6: Accessibility Contrast Validation at Preset Level~~ (DONE — PR #13)

**Status**: Completed. Added `djust_theming/checks.py` with Django system check (`djust_theming.W001`) that validates 12 foreground/background token pairs across all presets in both light and dark modes against WCAG AA 4.5:1 contrast ratio. Reports warnings, not errors. Also fixed bug in `accessibility.py` where `color_scale.l` should have been `color_scale.lightness`.

### ~~I7: Token Boundary Cleanup~~ (DONE — PR #14)

**Status**: Completed. `ThemeTokens` now contains only 29 color fields. `radius` moved to `ThemePreset.radius` (per-theme, not per-mode). Removed 4 unused animation CSS variables (`--card-lift-distance`, `--card-glow-opacity`, `--transition-speed`, `--animation-intensity`). Also fixed missing extension color fields in `high_contrast.py` and `shadcn.py`.

### ~~I8: Deprecate themes.py Properly~~ (DONE — PR #15)

**Status**: Completed. `THEMES` dict now wrapped in `_DeprecatedThemesDict` that emits `DeprecationWarning` on all access. `get_theme()` and `list_themes()` also emit warnings. `manager.py` now validates against `DESIGN_SYSTEMS` from `theme_packs.py`. Planned for removal in v2.0.

---

## Phase 1: Template Override System (Priority: Critical)

The foundation. Without this, themes are just color swaps.

### Execution Groups

Phase 1 and its related improvements are organized into execution groups that should be done together:

| Group | Tasks | Description |
|-------|-------|-------------|
| **A: CSS Infrastructure** | I16, I17, I21 | Color format interop, CSS namespace prefixing, brand color auto-palette. Pre-Phase 1 prerequisites. |
| **B: System Checks** | I23, I24 | AppConfig.ready() checks, dual CSS path consolidation. Standalone, extends existing checks.py. |
| **C: Template Resolution + CSS Layers** | 1.1, I9 | Template namespace resolution + CSS cascade layers. Both define how theme overrides take priority. |
| **D: Theme Manifest + Scaffold** | 1.2, 1.3 | Theme manifest spec + scaffold command. Scaffold generates from the manifest. |
| **E: Registry + Validation + Dynamic API** | 1.4, 1.5, I25 | Theme registry, validation command, dynamic preset registration. Tightly coupled. |
| **F: Optimization** | I10 | Critical CSS inlining. Standalone, can slot in anytime after Group C. |

### 1.1 Template Namespace Resolution

**Problem**: All components render from `djust_theming/components/*.html`. A theme author has no way to provide alternative templates.

**Solution**: Template loader that resolves by active theme name first, falling back to defaults.

```
Resolution order:
1. APP_DIRS: myapp/templates/djust_theming/themes/{theme_name}/components/button.html
2. Theme package: djust_theming/templates/djust_theming/themes/{theme_name}/components/button.html
3. Default: djust_theming/templates/djust_theming/components/button.html
```

- Add `ThemeTemplateLoader` (custom Django template loader) or use Django's built-in template resolution with a theme-aware prefix
- `ThemeManager` already knows the active theme name — wire it into template resolution
- Component tags (`theme_button`, etc.) resolve template path dynamically based on active theme

**Implementation detail**: The `theme_components.py` template tags currently use `@register.inclusion_tag('djust_theming/components/button.html')` which hardcodes the template path. These need to become dynamic — switch from `inclusion_tag` to `simple_tag` that calls `template.loader.select_template()` with a fallback chain:

```python
@register.simple_tag(takes_context=True)
def theme_button(context, text, variant='primary', size='md', **attrs):
    request = context.get('request')
    theme_name = _get_active_theme(request)
    tmpl = select_template([
        f'djust_theming/themes/{theme_name}/components/button.html',
        'djust_theming/components/button.html',
    ])
    return tmpl.render({'text': text, 'variant': variant, 'size': size, 'attrs': attrs})
```

### 1.2 Theme Manifest

Each theme is a directory with a `theme.toml` manifest:

```toml
[theme]
name = "corporate-clean"
version = "1.0.0"
description = "Clean corporate theme with sharp edges and system fonts"
author = "Jane Developer"
license = "MIT"

[extends]
base = "default"  # Inherit templates not overridden

[tokens]
preset = "blue"
design_system = "corporate"

[tokens.overrides]
radius = "0.25rem"
font-family-heading = "'Inter', system-ui, sans-serif"

[static]
css = ["extra.css"]        # Additional CSS files loaded after theme tokens
fonts = ["inter.woff2"]    # Font files served from theme's static dir
```

### 1.3 Theme Scaffold Command

```bash
python manage.py djust_theme create-theme my-theme --base default
```

Generates:
```
themes/my-theme/
├── theme.toml
├── tokens.css           # Design token overrides
├── components/          # Only override what you want
│   └── .gitkeep
├── layouts/
│   └── .gitkeep
├── pages/
│   └── .gitkeep
└── static/
    └── .gitkeep
```

### 1.4 Theme Registry

**Problem**: `ThemeManager` validates themes against `THEMES` dict from `themes.py` (design systems only). There's no registry for custom template-based themes.

**Solution**: A `ThemeRegistry` that discovers themes from:
1. Built-in design systems (existing `THEMES`)
2. `DJUST_THEMES` list in Django settings (pip-installed theme packages)
3. `themes/` directory in project templates (convention-based)

The registry merges all sources and provides a unified lookup for both `ThemeManager` and the template loader.

### 1.5 Theme Validation Command

```bash
python manage.py djust_theme validate my-theme
```

Checks:
- `theme.toml` is valid and all required fields present
- All overridden templates render without errors (dry-run with sample context)
- Component contracts satisfied (required HTML elements present in overridden templates)
- Token overrides reference valid CSS custom property names
- Accessibility: contrast ratios for any color token overrides
- Static files referenced in manifest exist

This prevents broken themes from reaching production.

---

## Phase 2: Component Library Expansion (Priority: High)

Expand from 5 to ~20 components. Each component = template + CSS, fully overridable per theme.

### 2.1 Missing Core Components

| Component | Template | Notes |
|-----------|----------|-------|
| `theme_modal` | `modal.html` | Backdrop, content, close button. Block tag for body. |
| `theme_dropdown` | `dropdown.html` | Trigger + menu. JS for open/close. |
| `theme_tabs` | `tabs.html` | Tab list + panels. djust reactive switching. |
| `theme_table` | `table.html` | Responsive, striped/hover variants. |
| `theme_pagination` | `pagination.html` | Prev/next + page numbers. |
| `theme_breadcrumb` | `breadcrumb.html` | Linked path segments. |
| `theme_avatar` | `avatar.html` | Image or initials fallback. |
| `theme_toast` | `toast.html` | Stackable notifications. Position variants. |
| `theme_progress` | `progress.html` | Determinate/indeterminate bar. |
| `theme_skeleton` | `skeleton.html` | Loading placeholder shapes. |
| `theme_tooltip` | `tooltip.html` | Hover/focus information popup. |
| `theme_select` | `select.html` | Styled native or custom dropdown. |
| `theme_textarea` | `textarea.html` | Multi-line input with label/error. |
| `theme_checkbox` | `checkbox.html` | Styled checkbox with label. |
| `theme_radio` | `radio.html` | Radio group with labels. |

### 2.2 Component Contract & Slot System

Each component template receives a fixed context dict. Theme authors override the template but must handle the same context variables. Document the contract per component:

```
# button.html contract
# Context: text (str), variant (str), size (str), disabled (bool), attrs (dict)
# Required elements: one <button> or <a> element with role="button"
# Must apply: variant class, size class
# Accessibility: must include aria-disabled when disabled=True
# Slots: icon, content, loading (see I11)
```

Contracts are enforced by the `validate` command (Phase 1.5) — it renders each overridden template with sample context and checks for required elements via HTML parsing.

**Slot system (I11)**: Every component template should use Django `{% block %}` tags for its composable parts from day one. This lets theme authors override specific slots via `{% extends %}` instead of copying the entire template. Components designed in Phase 2 must define slots; retrofitting slots later would break existing theme overrides. See I11 in "New Improvements" for details and examples.

### 2.3 Shared Component JavaScript

**Problem**: Components like modal, dropdown, tabs, and toast need JavaScript behaviors (open/close, tab switching, auto-dismiss). If each theme reimplements these, behavior diverges and bugs multiply.

**Solution**: A thin `djust_theming/js/components.js` that provides behavior hooks via data attributes (e.g., `data-theme-modal-trigger`, `data-theme-tab-panel`). Theme templates wire into these hooks with their own HTML structure. The JS handles state; the template handles appearance.

**Integration with djust**: When used inside a djust LiveView, components can optionally use `dj-click` directives instead of the vanilla JS hooks. The `components.js` detects whether djust is present and defers to it for event handling. This keeps theming usable outside of djust while being enhanced by it.

### 2.4 Component CSS Architecture

After I2 (extracting CSS from templates), establish a clear CSS architecture:

```
static/djust_theming/css/
├── tokens.css          # CSS custom properties (generated from Python)
├── base.css            # Reset, typography, utility classes
├── components.css      # All component styles (or split per-component)
└── layouts.css         # Layout-specific styles (Phase 3)
```

Rules:
- Component CSS uses only CSS custom properties — never hardcoded colors/sizes
- Class names follow BEM-lite: `.btn`, `.btn--primary`, `.btn--sm` (not `.btn-primary` to avoid ambiguity with CSS property-like names)
- Theme authors can override CSS by providing a `tokens.css` override (changes variables) or a full `components.css` replacement (changes structure)
- `{% theme_head %}` includes CSS in order: tokens → base → components → theme overrides

---

## Phase 3: Layout Templates (Priority: High)

Reusable page shells that theme authors can override.

### 3.1 Layout Types

| Layout | Template | Description |
|--------|----------|-------------|
| `base` | `layouts/base.html` | Root HTML with `{% theme_head %}`, body wrapper |
| `sidebar` | `layouts/sidebar.html` | Fixed sidebar + main content area |
| `topbar` | `layouts/topbar.html` | Fixed top navigation + content |
| `sidebar-topbar` | `layouts/sidebar-topbar.html` | Both sidebar and topbar |
| `centered` | `layouts/centered.html` | Centered content column (auth pages, landing) |
| `dashboard` | `layouts/dashboard.html` | Sidebar + topbar + content grid |
| `split` | `layouts/split.html` | Two-panel layout (e.g., list + detail) |

### 3.2 Layout Blocks

Standard block names that all layouts provide:

```html
{% block page_title %}{% endblock %}
{% block sidebar %}{% endblock %}
{% block topbar %}{% endblock %}
{% block content %}{% endblock %}
{% block footer %}{% endblock %}
{% block extra_css %}{% endblock %}
{% block extra_js %}{% endblock %}
```

### 3.3 Navigation Components

These pair with layouts:

| Component | Notes |
|-----------|-------|
| `theme_nav` | Horizontal nav bar with links, logo slot, action buttons |
| `theme_sidebar_nav` | Vertical nav with sections, icons, collapse |
| `theme_nav_item` | Single nav link with active state detection |
| `theme_nav_group` | Collapsible group of nav items |

### 3.4 Responsive Layout Tokens

Layouts need breakpoint-aware behavior. Add responsive tokens:

```css
:root {
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --sidebar-width: 16rem;
  --sidebar-collapsed-width: 4rem;
  --topbar-height: 3.5rem;
}
```

Layout templates use these tokens + CSS `@container` queries (where supported) for responsive behavior. Theme authors override layout dimensions via token overrides in `theme.toml`.

---

## Phase 4: Page Templates (Priority: Medium)

Pre-built pages that theme authors can override. These are the "starter kit" that makes a theme feel complete.

### 4.1 Auth Pages

- `pages/login.html` — Email/password + social login slots
- `pages/register.html` — Registration form
- `pages/password_reset.html` — Password reset request
- `pages/password_confirm.html` — New password entry

### 4.2 Error Pages

- `pages/404.html` — Not found
- `pages/500.html` — Server error
- `pages/403.html` — Permission denied

### 4.3 Utility Pages

- `pages/maintenance.html` — Maintenance mode
- `pages/empty_state.html` — No-data placeholder with CTA

### 4.4 Page Template Tags

```html
{% extends "djust_theming/layouts/centered.html" %}
{% load theme_pages %}

{% block content %}
    {% theme_login_form form next_url="/dashboard/" social_providers=social_providers %}
{% endblock %}
```

Page templates are opinionated compositions of layout + components. Theme authors override the full page template or just the components within it.

---

## Phase 5: Design System → Template Variants (Priority: Medium)

Currently, design systems (Material, iOS, Fluent, etc.) only produce CSS. They should also provide template variants where the HTML structure differs between systems.

**Example**: A Material button has a ripple effect `<span>` inside it. An iOS button does not. CSS alone can't add/remove DOM elements.

### 5.1 Built-in Theme Packs

Convert the 11 existing design systems into full theme packs (templates + tokens):

| Design System | Template Differences |
|---------------|---------------------|
| Material | Ripple overlays, elevation classes, FAB button variant |
| iOS | SF-style segmented controls, blur backdrops |
| Fluent | Acrylic backgrounds, reveal-highlight on hover |
| Neo-Brutalist | Thick borders, offset shadows in markup |
| Playful | SVG decorations, animated wrapper elements |

Not every design system needs unique templates — only where HTML structure must differ. Others inherit defaults and rely on CSS.

### 5.2 Installable Theme Packages

Allow pip-installable theme packages:

```bash
pip install djust-theme-material
```

Package provides:
```
djust_theme_material/
├── theme.toml
├── tokens.css
├── components/
├── layouts/
└── static/
```

Registered in Django settings:
```python
DJUST_THEMES = [
    'djust_theme_material',
]
```

### 5.3 Theme Package Cookiecutter

Provide a cookiecutter/copier template for creating new theme packages:

```bash
python manage.py djust_theme create-package my-theme-package
```

Generates a pip-installable Python package with the correct structure, `pyproject.toml`, and a README with publishing instructions.

---

## Phase 6: Form Integration (Priority: Medium)

Django forms should automatically render with theme styling.

### 6.1 Theme-Aware Form Renderer

```python
# settings.py
FORM_RENDERER = 'djust_theming.forms.ThemeFormRenderer'
```

All `{{ form.as_div }}` / `{{ form.as_p }}` output uses theme component templates.

### 6.2 Form Field Templates

Map Django form fields to themed components:
- `TextInput` → `theme_input`
- `Textarea` → `theme_textarea`
- `Select` → `theme_select`
- `CheckboxInput` → `theme_checkbox`
- `RadioSelect` → `theme_radio`

### 6.3 Form Layout Tag

```html
{% theme_form form layout="stacked" %}
{% theme_form form layout="horizontal" label_width="4" %}
{% theme_form form layout="inline" %}
```

### 6.4 Error Display Integration

Form validation errors render using `theme_alert` with `variant="destructive"`. Field-level errors appear inline below each input. Theme authors can override the error template (`components/form_error.html`) to change error presentation.

---

## Phase 7: RTL, Accessibility Modes & Print (Priority: Medium)

### 7.1 Bidirectional Layout Tokens

Add logical CSS properties throughout:

```css
/* Instead of margin-left, use margin-inline-start */
.sidebar { margin-inline-start: 0; width: var(--sidebar-width); }
.content { margin-inline-start: var(--sidebar-width); }
```

All layout and component CSS should use logical properties (`inline-start`/`inline-end` instead of `left`/`right`, `block-start`/`block-end` instead of `top`/`bottom`) so themes work correctly in RTL languages without additional overrides.

### 7.2 RTL Theme Flag

```toml
# theme.toml
[theme]
direction = "auto"  # "ltr", "rtl", or "auto" (detects from Django's LANGUAGE_CODE)
```

`{% theme_head %}` sets `dir` attribute on `<html>` element based on this setting.

### 7.3 RTL-Aware Components

Components with directional behavior (breadcrumbs, navigation, pagination) must use the direction token. The arrow/chevron icons flip automatically via CSS `transform: scaleX(-1)` when `[dir="rtl"]` is active.

### 7.4 Reduced Motion Support (I13)

Respect `prefers-reduced-motion` at the token level — all animation duration tokens collapse to `0ms` when the user preference is active. See I13 in "New Improvements" for implementation details. This ensures animated themes (Playful, Synthwave) are safe for users with vestibular disorders without theme authors needing to do anything.

### 7.5 High Contrast Mode (I13)

Respect `prefers-contrast: more` by adjusting border, ring, and muted token values for maximum visibility. The existing `high_contrast.py` module has some support; wire it into the token generation pipeline so it activates automatically via CSS media query rather than requiring explicit mode switching.

### 7.6 Print Stylesheet (I15)

Add `print.css` to the base theme — hides navigation, sidebars, footers, and interactive components. Forces high-contrast black-on-white colors. Theme authors can override. Included by `{% theme_head %}` with `media="print"`.

---

## Phase 8: Theme Preview & Inspector (Priority: Low)

### 8.1 Theme Gallery View

A single view that renders every component in every variant, with the active theme. Useful for theme development and QA.

```python
urlpatterns = [
    path('theming/gallery/', include('djust_theming.gallery.urls')),
]
```

### 8.2 Live Theme Editor

Extend the existing inspector to allow real-time token editing:
- Color picker for each token
- Typography controls (font, size, weight)
- Spacing/radius sliders
- Export modified theme as `theme.toml` + `tokens.css`

### 8.3 Theme Diff View

Side-by-side comparison of two themes rendering the same components.

### 8.4 Visual Regression Testing

Provide a test utility for theme authors:

```bash
python manage.py djust_theme snapshot my-theme
# Renders all components to screenshots using headless browser
# Stores in themes/my-theme/.snapshots/

python manage.py djust_theme diff my-theme
# Compares current render against stored snapshots
# Reports visual differences
```

This prevents unintended visual regressions when modifying theme templates or tokens.

---

## Phase 9: Documentation & Ecosystem (Priority: Low)

### 9.1 Theme Author Guide

Step-by-step guide: "Create your first theme in 10 minutes"
1. Scaffold a theme
2. Override button + card templates
3. Set custom tokens
4. Preview in gallery
5. Package and distribute

### 9.2 Component Storybook

Auto-generated documentation page for each component showing:
- All variants rendered
- Template source
- Context contract
- CSS variables used

### 9.3 Theme Marketplace Spec

Define the metadata format for a theme registry (future djust.org feature):
- Theme screenshots
- Compatibility version range
- Component coverage report
- Live preview link

### 9.4 Migration Guide

When component contracts change between versions, provide:
- A `BREAKING_CHANGES.md` per version documenting contract changes
- A `python manage.py djust_theme check-compat my-theme` command that reports which overridden templates need updating
- Semver: component contract changes = major version bump

---

## New Improvements (Added 2026-03-21)

These were identified during a full codebase review and fill gaps the original roadmap didn't cover.

### I9: CSS Cascade Layers for Theme Specificity (Priority: High — do with Phase 1)

**Problem**: When theme authors add custom CSS, specificity conflicts with component CSS are inevitable. A theme's `.btn { border-radius: 0 }` may lose to the built-in `.btn--primary` rule depending on load order. This will be the #1 support issue for theme authors.

**Fix**: Adopt CSS `@layer` throughout the CSS architecture:

```css
@layer base, tokens, components, layouts, theme;

@layer tokens { :root { --primary: 221 83% 53%; /* ... */ } }
@layer components { .btn { /* ... */ } }
@layer theme { /* theme author overrides always win */ }
```

Theme author CSS is placed in the `theme` layer automatically by `{% theme_head %}`. This gives predictable cascade behavior regardless of selector specificity. Browser support is excellent (95%+ as of 2025). This should be implemented alongside I2 (CSS extraction) since both restructure how CSS is organized.

### I10: Critical CSS Inlining (Priority: Medium — do with Phase 1)

**Problem**: Currently `{% theme_head %}` either inlines ALL generated CSS (large payload, blocks render) or links to an external CSS file (extra request, FOUC risk). There's no middle ground.

**Fix**: Split CSS generation into critical (tokens + above-the-fold component styles) and deferred (full component library). `{% theme_head %}` inlines the critical CSS in a `<style>` tag and `<link rel="preload">` loads the rest. For themes, critical CSS = tokens + layout CSS. Component CSS loads async. This keeps first paint fast regardless of theme complexity.

### I11: Component Slot System (Priority: High — add to Phase 2)

**Problem**: Current component templates are monolithic. To change just the icon inside a button, a theme author must copy and override the entire `button.html`. This leads to template drift — when the base template adds a new feature (e.g., loading spinner), overridden templates miss it.

**Fix**: Add named slots to component templates using Django template blocks:

```html
{# button.html — base template #}
<button class="btn btn--{{ variant }} btn--{{ size }}" {% for k, v in attrs.items %}{{ k }}="{{ v }}"{% endfor %}>
    {% block icon %}{% if icon %}<span class="btn__icon">{{ icon }}</span>{% endif %}{% endblock %}
    {% block content %}{{ text }}{% endblock %}
    {% block loading %}{% if loading %}<span class="btn__spinner"></span>{% endif %}{% endblock %}
</button>
```

Theme authors override specific blocks without touching the rest:

```html
{# themes/my-theme/components/button.html #}
{% extends "djust_theming/components/button.html" %}
{% block icon %}<svg class="my-icon">...</svg>{% endblock %}
```

This is the single most impactful change for theme author ergonomics. It reduces override surface area from "entire template" to "specific slot" while maintaining forward compatibility when the base template evolves.

### I12: Tree-Shaking for Component CSS (Priority: Medium — do after Phase 2)

**Problem**: After I2 extracts component CSS into files and Phase 2 adds 15 new components, the combined `components.css` will be substantial. A simple page using only buttons and cards loads CSS for all 20 components.

**Fix**: Two approaches (choose one):
1. **Per-component CSS files** + a `{% theme_component_css %}` tag that tracks which components were rendered and emits only their CSS links in the `{% block extra_css %}` of the layout. Requires a two-pass or deferred rendering approach.
2. **Build-time purge** via the CLI: `python manage.py djust_theme purge-css my-theme --scan templates/` scans templates for `{% theme_* %}` usage and outputs a minimal CSS bundle.

Option 1 is more aligned with djust's "no build step" philosophy. Option 2 is an optional optimization for production.

### I13: Reduced Motion & High Contrast Modes (Priority: Medium — add to Phase 7)

**Problem**: The current system has light/dark modes but no support for `prefers-reduced-motion` or `prefers-contrast`. Themes with animations (Playful, Synthwave) can cause issues for users with vestibular disorders.

**Fix**: Add media query awareness to the token system:

```css
@media (prefers-reduced-motion: reduce) {
    :root {
        --duration-fast: 0ms;
        --duration-normal: 0ms;
        --duration-slow: 0ms;
    }
}

@media (prefers-contrast: more) {
    :root {
        --border: 0 0% 0%;        /* Force solid borders */
        --ring: 0 0% 0%;          /* Force visible focus rings */
    }
}
```

Add `accessibility` section to `theme.toml`:

```toml
[accessibility]
reduced_motion = "respect"    # "respect" (honor user pref), "force" (always reduce), "ignore"
high_contrast = "respect"     # "respect", "force", "ignore"
min_target_size = "44px"      # WCAG 2.5.5 target size
```

The `validate` command (Phase 1.5) checks these settings and warns when a theme ignores accessibility preferences.

### I14: Theme Composition — Mix and Match (Priority: Low — after Phase 5)

**Problem**: Themes are currently monolithic — you choose one theme and get its colors, typography, spacing, and templates as a bundle. But a common desire is "I want the Material button style with Nord colors and Inter typography." There's no way to compose across themes.

**Fix**: Allow `theme.toml` to reference specific layers from other themes:

```toml
[compose]
colors = "nord"                    # Color tokens from Nord preset
typography = "corporate"           # Typography from Corporate design system
components = "material"            # Component templates from Material theme
layouts = "default"                # Layout templates from default
```

The `ThemeRegistry` resolves each layer independently. Template resolution checks the `components` source theme; token generation merges tokens from each layer. Conflicts are resolved by explicit `[tokens.overrides]`.

This is powerful but complex — defer to after Phase 5 when the registry and template resolution are mature enough to handle multi-source resolution.

### I15: Print Stylesheet Support (Priority: Low — add to Phase 7)

**Problem**: No consideration for `@media print`. Themes render poorly when printed — sidebars, navigation, dark backgrounds all appear.

**Fix**: Add a `print.css` to the base theme that hides navigation, sidebars, and interactive components. Adjusts colors to high-contrast black-on-white. Theme authors can override with their own `print.css` in the theme static directory. `{% theme_head %}` includes it with `media="print"`.

---

## New Improvements (Added 2026-03-22)

Identified during a deep codebase review focused on real-world theme authoring workflows and integration gaps.

### I16: Color Format Interoperability (Priority: High — do before Phase 1)

**Problem**: `ColorScale` only exports HSL (`to_hsl()`, `to_hsl_func()`). There's no `to_hex()` or `to_rgb()` method. Theme authors importing brand colors from Figma, Sketch, or design systems (which use hex/RGB) have no conversion path. The `hsl_to_rgb()` function exists in `accessibility.py` for contrast checking but isn't exported as a public API. Going the other direction (hex → HSL for creating a preset) requires manual conversion outside the system.

**Fix**:
1. Add `to_hex()`, `to_rgb()`, `to_rgb_func()` methods to `ColorScale`
2. Add `ColorScale.from_hex(hex_str)` and `ColorScale.from_rgb(r, g, b)` class methods
3. Export color conversion utilities from `djust_theming.colors` (new module, consolidates `accessibility.py` color math)
4. Add CLI support: `python manage.py djust_theme create-preset --from-hex "#1E40AF"` generates a full preset by deriving scales from a single brand color

This is high priority because theme authors' first action is often "I have my brand color in hex, how do I make a preset?" — that path must be frictionless.

### I17: CSS Namespace Prefixing (Priority: High — do with I2)

**Problem**: Component CSS classes are global and generic (`.btn`, `.card`, `.badge`, `.alert`). When djust-theming is embedded in an existing app that already defines `.btn` (Bootstrap, Bulma, custom CSS), styles collide. The roadmap assumes theme authors control the entire page, but real-world adoption often starts with "add djust-theming to one section of an existing app."

**Fix**: Add a configurable CSS prefix (default: `djt-`) to all component classes:

```python
# settings.py
DJUST_THEMING = {
    'CSS_PREFIX': 'djt-',  # or '' for no prefix
}
```

Generated CSS uses the prefix: `.djt-btn`, `.djt-card`, `.djt-badge`. Component templates reference `{{ css_prefix }}btn` or the tag resolves it. The prefix is injected once via `{% theme_head %}` as a CSS custom property `--djt-prefix` (for documentation) and applied at generation time.

**Migration**: Default prefix is `''` (empty) for v1.x backward compatibility. v2.0 changes default to `'djt-'`. A `python manage.py djust_theme migrate-prefix` command rewrites templates to use the new prefix.

This should be done alongside I2 (CSS extraction) since both restructure CSS class references.

### I18: Container-Scoped Theming (Priority: Medium — do after Phase 1)

**Problem**: Theme switching is page-global — `theme.js` sets `data-theme` and `data-theme-mode` on `<html>`. There's no way to apply different presets to different DOM subtrees. Real use cases: theme preview gallery (show all presets side-by-side), multi-tenant dashboards (each tenant card in their brand colors), A/B testing themes on sections of a page.

**Fix**: Support scoped theming via a `[data-theme-scope]` attribute:

```html
<div data-theme-scope data-theme-preset="nord" data-theme-mode="dark">
    {% theme_card title="Nord Dark" %}...{% endtheme_card %}
</div>
<div data-theme-scope data-theme-preset="rose" data-theme-mode="light">
    {% theme_card title="Rose Light" %}...{% endtheme_card %}
</div>
```

CSS tokens are scoped using attribute selectors: `[data-theme-preset="nord"] { --primary: ... }`. The `css_generator.py` already generates per-preset CSS — extend it to output scoped rules when `scoped=True`. `theme.js` gets a `DjustThemeScope` class that manages a subtree instead of the document root.

### I19: Shadow & Animation Token Pipeline (Priority: Medium — do with Phase 2)

**Problem**: `design_tokens.py` generates spacing, typography, and radius tokens, but shadows and animations are hardcoded in `base.css` (`--shadow-sm`, `--duration-fast`, etc.) and not part of the Python generation pipeline. Theme presets define `transition_speed` and `animation_intensity` properties, but these aren't exported as CSS custom properties by `css_generator.py`. Theme authors can't swap shadow systems (flat vs. material vs. neumorphic) or animation styles via tokens alone.

**Fix**:
1. Move shadow definitions from `base.css` into `design_tokens.py` as `ShadowScale` (matching the existing `ColorScale` pattern)
2. Add `AnimationTokens` class: `duration_fast`, `duration_normal`, `duration_slow`, `ease_default`, `ease_in`, `ease_out`, `ease_bounce`
3. Wire preset's `transition_speed` and `animation_intensity` into the CSS generation — `animation_intensity: 0` collapses all durations to `0ms` (same effect as `prefers-reduced-motion`)
4. Generate utility classes: `.shadow-sm`, `.shadow-md`, `.shadow-lg`, `.animate-fade-in`, `.animate-slide-up`
5. Add shadow presets (flat, material, neumorphic, inset) selectable in `theme.toml`:

```toml
[tokens]
shadow_style = "material"    # "flat", "material", "neumorphic", "inset"
```

### I20: Responsive Token System (Priority: Medium — do with Phase 3)

**Problem**: All tokens are flat — `--space-4: 1rem` is the same on mobile and desktop. `base.css` hardcodes `--sidebar-width: 300px` and `--navbar-height: 52px` with no responsive variants. Theme authors must write manual `@media` queries to adjust spacing, typography, and layout dimensions for different screen sizes. This defeats the "tokens are the single source of truth" principle.

**Fix**: Add responsive token variants to `design_tokens.py`:

```css
:root {
    --space-4: 1rem;
    --font-size-base: 1rem;
    --sidebar-width: 16rem;
}

@media (max-width: 768px) {
    :root {
        --space-4: 0.75rem;
        --font-size-base: 0.875rem;
        --sidebar-width: 0;  /* sidebar collapses on mobile */
    }
}
```

Theme authors control responsive behavior via `theme.toml`:

```toml
[tokens.responsive]
mobile_scale = 0.875      # Scale factor for spacing/typography on mobile
sidebar_collapse = "md"   # Breakpoint where sidebar collapses
```

The CSS generator emits responsive variants automatically. This keeps the "single source of truth" principle intact while enabling responsive theming without manual CSS.

### I21: Brand Color Auto-Palette Generator (Priority: Medium — do with I16)

**Problem**: Creating a full color preset requires defining 17+ token pairs (primary, secondary, muted, accent, etc. — each with foreground). Most theme authors start with 1-3 brand colors and want the rest derived automatically. Currently they must manually calculate every shade, which is error-prone and discourages preset creation.

**Fix**: Add a `PaletteGenerator` that derives a complete `ThemePreset` from minimal input:

```python
from djust_theming.palette import PaletteGenerator

preset = PaletteGenerator.from_brand_color(
    primary="#1E40AF",           # Required: one brand color
    secondary="#9333EA",         # Optional
    mode="professional",         # "professional", "playful", "muted", "vibrant"
)
```

Algorithm:
1. Convert input hex to HSL
2. Derive background/foreground from primary lightness (light mode: light bg, dark fg; dark mode: inverse)
3. Generate secondary from complementary hue if not provided
4. Generate accent from analogous hue
5. Derive muted/card/border by desaturating and shifting lightness
6. Auto-generate dark mode by inverting lightness scale
7. Validate contrast ratios (WCAG AA) and adjust if needed

CLI integration:
```bash
python manage.py djust_theme create-preset my-brand --primary "#1E40AF" --mode professional
# Outputs: presets/my_brand.py with full light/dark ThemePreset
```

### I22: Theme Inheritance Validation & Conflict Detection (Priority: Low — do with Phase 5)

**Problem**: When `theme.toml` declares `extends.base = "default"`, the system resolves templates by checking the theme directory first, then falling back to the base. But there's no validation that the overridden templates are compatible with the base theme's CSS. A theme could override `button.html` with HTML that uses class names the base CSS doesn't define, producing unstyled components. Similarly, if a theme provides `tokens.css` overrides that redefine structural tokens (not just colors), it could break layout assumptions in inherited templates.

**Fix**:
1. `validate` command checks that overridden templates reference only CSS classes defined in the theme's CSS + base CSS
2. Token overrides are type-checked: color tokens can only be overridden with color values, spacing tokens with length values, etc.
3. Warn when an overridden template removes required accessibility attributes (aria-*, role, etc.) present in the base
4. `python manage.py djust_theme diff my-theme default` shows exactly what a theme changes vs. its base — useful for code review and debugging

---

## New Improvements (Added 2026-03-22, batch 2)

Identified during deep source review of `manager.py`, `css_generator.py`, `theme_tags.py`, `views.py`, `presets.py`, `apps.py`, and `theme_components.py`. These address performance, architecture, and developer experience gaps not covered by I1–I22.

### I23: AppConfig.ready() System Checks (Priority: High — do with Phase 1)

**Problem**: `apps.py` has no `ready()` method. There are no Django system checks for misconfigurations. Common mistakes go undetected until runtime: missing `context_processors`, invalid `LIVEVIEW_CONFIG['theme']` values, references to non-existent presets or design systems, missing `djust_theming.urls` in `urlpatterns`. Other djust packages (e.g., core djust) use system checks extensively — djust-theming should match that pattern.

**Fix**:
1. Add `ready()` to `DjustThemingConfig` — register system checks
2. Implement checks in `djust_theming/checks.py`:
   - `djust_theming.E001`: `djust_theming.context_processors.theme_context` missing from TEMPLATES
   - `djust_theming.E002`: `LIVEVIEW_CONFIG['theme']['preset']` references unknown preset
   - `djust_theming.E003`: `LIVEVIEW_CONFIG['theme']['theme']` references unknown design system
   - `djust_theming.W001`: `djust_theming.urls` not included in urlpatterns (warning since CSS endpoint is optional when using inline CSS)
   - `djust_theming.W002`: Static files not collected (missing `collectstatic` for production)
3. This matches the djust core pattern (`djust.S001`–`djust.S005`) and catches misconfigurations at `manage.py check` time, not when a user hits a 500 error.

### I24: Dual CSS Generation Path Consolidation (Priority: High — do with I5)

**Problem**: CSS is generated in two independent code paths that can drift:
1. `theme_tags.py` `theme_head()` — inline CSS via `CompleteThemeCSSGenerator` or `ThemePackCSSGenerator`, with its own pack/theme/preset detection logic
2. `views.py` `theme_css_view()` — linked CSS via `_generate_css_content()`, with its own pack/theme/preset detection logic

Both paths duplicate the "which generator to use" decision. The ETag format in `views.py` (`theme-preset-mode-pack`) differs from the cache buster params in `theme_tags.py` (`?t=&p=&m=&pk=`). If generation logic changes in one path but not the other, inline and linked CSS can produce different output for the same theme state.

**Fix**: Extract a single `generate_theme_css(theme_state: ThemeState) -> str` function that both `theme_head()` and `theme_css_view()` call. The function handles pack vs. theme+preset detection, CSS generation, and caching (I5). Both consumers get identical output. ETag and cache buster derive from the same `ThemeState` hash.

### I25: Dynamic Preset Registration API (Priority: Medium — do with Phase 1)

**Problem**: `THEME_PRESETS` in `presets.py` is a module-level dict with 6 hardcoded presets. Additional presets (Cyberpunk, Forest, Amber, etc.) are defined in `theme_packs.py` but loaded through a different code path. There's no public API for apps to register custom presets at startup. A SaaS app that lets tenants pick brand colors can't add presets without monkey-patching the dict.

**Fix**:
1. Add `ThemeRegistry` class (planned for Phase 1.4) with `register_preset(name, preset)` and `get_preset(name)` methods
2. `ready()` in `apps.py` populates the registry from `THEME_PRESETS` + `theme_packs` + `DJUST_THEMES` setting
3. All code that reads presets goes through the registry, not direct dict access
4. Third-party apps call `ThemeRegistry.register_preset()` in their own `ready()` method
5. This is a prerequisite for Phase 1.4 anyway — building it early means I16/I21 (auto-palette) can register generated presets dynamically

### I26: Server-Side CSS Compression (Priority: Medium — do with I5)

**Problem**: `theme_css_view()` serves uncompressed CSS. For inline CSS via `theme_head()`, the full uncompressed CSS is embedded in every HTML response. A typical theme generates 8–12KB of CSS. With 20 components (Phase 2), this could reach 20–30KB. Django's `GZipMiddleware` handles response compression, but the inline `<style>` block isn't separately compressible — it inflates every HTML response.

**Fix**:
1. Add CSS minification to `generate_theme_css()` — strip comments, collapse whitespace, shorten zero values. Use a lightweight Python minifier (e.g., `csscompressor` or a simple regex-based minifier — no npm dependency)
2. For `theme_css_view()`: add `Content-Encoding: gzip` support (or rely on Django/WhiteNoise middleware)
3. For inline CSS: minification alone reduces payload by 30–40%; combined with HTML response compression, this is sufficient
4. Add `DJUST_THEMING['MINIFY_CSS']` setting (default: `not settings.DEBUG`) — skip minification in development for readability

### I27: Component Tag Test Harness (Priority: Medium — do before Phase 2)

**Problem**: Component template tags (`theme_button`, `theme_card`, etc.) have no visible test coverage. The 508 tests mentioned in Phase 1 summary are primarily for presets and design tokens. When Phase 2 adds 15 new components, there's no test pattern to follow. Component contracts (required HTML elements, accessibility attributes, context variables) described in Phase 2.2 need automated validation, but no test infrastructure exists for rendering components with sample context and asserting on the output HTML.

**Fix**:
1. Create `tests/test_components.py` with a `ComponentTestCase` base class that:
   - Renders a component tag with sample context
   - Parses output HTML (using `html.parser` or `BeautifulSoup`)
   - Asserts required elements exist (e.g., button has `<button>` or `<a role="button">`)
   - Asserts accessibility attributes present (`aria-disabled`, `role`, etc.)
   - Asserts CSS class names match expected pattern (respects I17 prefix)
2. Define contracts as data (dict of component → required elements/attrs) so the `validate` command (Phase 1.5) and tests share the same source of truth
3. Each new Phase 2 component gets a contract + test before implementation — test-driven component development

### I28: Theme State Hash for Cache Keys (Priority: Low — do with I5)

**Problem**: Multiple systems need to cache based on "current theme configuration" — CSS generation (I5), ETag (views.py), cache buster params (theme_tags.py), and future features like critical CSS (I10) and tree-shaking (I12). Each currently constructs its own cache key string from theme state fields. When a new field is added to `ThemeState` (e.g., `pack`), each cache key must be updated independently — easy to miss.

**Fix**: Add `ThemeState.cache_key() -> str` method that returns a stable hash of all state fields. All caching, ETag, and cache buster logic uses this single method. When `ThemeState` gains new fields, the hash updates automatically. Use `hashlib.md5` (not cryptographic, just cache keying) of the serialized state for a short, URL-safe key.

### I29: Graceful Degradation for Missing Theme Assets (Priority: Low — do with Phase 1)

**Problem**: If a theme references a static asset in `theme.toml` that doesn't exist (e.g., a font file was deleted, or a CSS override file was renamed), the failure mode is a silent 404 in the browser network tab. The theme renders but looks broken. Theme authors debugging their first theme won't know to check the network tab.

**Fix**:
1. `ThemeTemplateLoader` validates static asset references at theme discovery time (startup)
2. Missing assets → Django system check warning (`djust_theming.W003: Theme 'my-theme' references 'inter.woff2' but file not found`)
3. `{% theme_head %}` emits an HTML comment `<!-- djust-theming: WARNING: static file 'inter.woff2' not found -->` when `DEBUG=True`
4. The `validate` command (Phase 1.5) already checks this — but runtime detection catches issues that only appear in deployed environments

---

## New Improvements (Added 2026-03-22, batch 3)

Identified during a deep architecture review focused on modern CSS capabilities, color science, design tool workflows, and internationalization gaps. These address foundational decisions that will be increasingly expensive to change later.

### I49: OKLCH Color Space for Palette Generation (Priority: High — do with I16 + I21)

**Problem**: `ColorScale` uses HSL exclusively. HSL is perceptually non-uniform — rotating hue at constant saturation/lightness produces wildly different perceived brightness (yellow at L50 looks far brighter than blue at L50). This directly degrades I21 (auto-palette) output quality: derived secondary/accent colors look inconsistent because HSL "lies" about perceptual lightness. The CSS `oklch()` color space (supported in all modern browsers since 2023) is perceptually uniform and is now the recommended color space for design systems.

**Fix**:
1. Add `OklchColor` dataclass alongside `ColorScale`: `lightness: float` (0–1), `chroma: float` (0–0.4), `hue: float` (0–360)
2. Add bidirectional conversion: `ColorScale.to_oklch()` and `OklchColor.to_hsl()` (via sRGB intermediate)
3. Refactor `PaletteGenerator` (I21) to operate in OKLCH internally — derive complementary/analogous hues in OKLCH space where perceptual uniformity holds, then convert to HSL for CSS output
4. Add `color_space` option to `theme.toml`:

```toml
[tokens]
color_space = "oklch"    # "hsl" (default, backward compat) or "oklch"
```

When `oklch` is selected, CSS output uses `oklch()` function directly:
```css
:root { --primary: oklch(0.55 0.24 264); }
```

5. Keep HSL as default for v1.x backward compatibility. OKLCH becomes default in v2.0.

**Why this matters now**: I21 (auto-palette) is a Tier 1 item. If we build palette generation in HSL and later migrate to OKLCH, every generated preset needs re-derivation. Building OKLCH support alongside I21 avoids that rework.

### I50: Modern CSS Functions — color-mix() and light-dark() (Priority: High — do with I2 + I9)

**Problem**: The current system generates separate `:root` and `.dark` blocks with duplicate token lists — every color token is defined twice (light and dark variants). This doubles the CSS output size for color tokens and requires theme authors to maintain both variants. CSS `light-dark()` (baseline 2024, 94%+ browser support) and `color-mix()` (baseline 2023, 96%+ support) can dramatically simplify this.

**Fix**:
1. **`light-dark()` for dual-mode tokens**: Instead of generating two rule blocks:
```css
/* Old approach — 2 blocks */
:root { --background: 0 0% 100%; }
.dark { --background: 222 47% 11%; }
```
Generate a single block with `light-dark()`:
```css
/* New approach — 1 block */
:root { color-scheme: light dark; }
:root { --background: light-dark(hsl(0 0% 100%), hsl(222 47% 11%)); }
```
The browser selects the correct value based on `color-scheme` or `prefers-color-scheme`. This cuts color token CSS by ~40%.

2. **`color-mix()` for derived tokens**: Instead of pre-computing every shade in Python:
```css
--muted: color-mix(in oklch, var(--background) 90%, var(--foreground));
--border: color-mix(in oklch, var(--background) 80%, var(--foreground));
```
This means changing `--background` automatically updates derived tokens without re-generation. Theme authors adjust fewer tokens to get a complete palette.

3. **Progressive enhancement**: Add `modern_css` flag to settings:
```python
DJUST_THEMING = {
    'MODERN_CSS': True,     # Use light-dark(), color-mix() — default in v2.0
    # 'MODERN_CSS': False,  # Legacy: separate :root/.dark blocks — v1.x default
}
```

4. The CSS generator detects the flag and switches output format. Both paths produce visually identical results; modern path is smaller and more composable.

**Why this matters now**: I2 (CSS extraction) and I9 (cascade layers) restructure the entire CSS output. Adding `light-dark()` during that restructuring is cheap. Adding it after means rewriting the generator again.

### I51: CSS Nesting for Component Styles (Priority: Medium — do with Phase 2)

**Problem**: Component CSS files (after I2 extraction) will use flat selectors: `.btn { ... } .btn--primary { ... } .btn__icon { ... }`. Theme authors overriding component CSS must match this flat structure. Native CSS nesting (baseline 2023, 91%+ support) enables more readable, maintainable component styles — especially important when theme authors override component CSS.

**Fix**:
1. Write component CSS using native nesting where it improves readability:
```css
.btn {
    /* base styles */
    &--primary { background: hsl(var(--primary)); }
    &--sm { padding: var(--space-1) var(--space-2); }
    &:hover { opacity: 0.9; }
    &:focus-visible { outline: 2px solid hsl(var(--ring)); }
}
```

2. Document nesting as the recommended pattern for theme author CSS overrides
3. No configuration needed — this is a CSS authoring convention, not a runtime feature
4. For the 9% of browsers without nesting support: the CLI `purge-css` command (I12) can optionally flatten nested CSS via a simple transform, but this is an edge case not worth blocking on

### I52: Color Blindness Simulation for Theme Validation (Priority: Medium — do with I6)

**Problem**: `accessibility.py` validates contrast ratios (WCAG AA luminance) but doesn't simulate color vision deficiencies. A theme could pass all contrast checks while being unusable for the ~8% of males with red-green color blindness (deuteranopia/protanopia). The `validate` command (Phase 1.5) catches contrast issues but not "these two distinct states look identical to color-blind users."

**Fix**:
1. Add color vision simulation to `accessibility.py`:
   - `simulate_deuteranopia(color: ColorScale) -> ColorScale` — red-green (most common, ~6% males)
   - `simulate_protanopia(color: ColorScale) -> ColorScale` — red deficiency (~2% males)
   - `simulate_tritanopia(color: ColorScale) -> ColorScale` — blue-yellow (rare, ~0.01%)
   - Uses standard Brettel/Viénot/Mollon simulation matrices (well-documented, no dependencies needed)
2. `validate` command gains `--color-blind` flag:
```bash
python manage.py djust_theme validate my-theme --color-blind
# Checks that primary vs. destructive, success vs. warning, etc. remain distinguishable
# under deuteranopia/protanopia simulation
```
3. The check validates that *semantically different* token pairs (success/destructive, primary/accent, info/warning) maintain minimum ΔE (color difference) under simulation — not just contrast ratio
4. Report format: "Under deuteranopia simulation, `--success` and `--warning` have ΔE of 3.2 (minimum: 10). These states will appear nearly identical to ~6% of male users."

### I53: Internationalized Component Strings (Priority: Medium — do with Phase 2)

**Problem**: Component templates contain English-only labels and ARIA text. `theme_switcher.html` has hardcoded "Light", "Dark", "System" labels. `alert.html` has a hardcoded "×" close button with `aria-label="Close"`. When Phase 2 adds 15 new components (modal, toast, pagination, etc.), the hardcoded English strings will multiply. Theme authors building for non-English audiences must override every component template just to translate UI chrome — violating the "override only what you want" principle.

**Fix**:
1. Wrap all user-visible strings in `{% trans %}` tags (Django i18n):
```html
{# theme_switcher.html #}
<button aria-label="{% trans 'Toggle theme' %}">
    <span>{% trans "Light" %}</span>
    <span>{% trans "Dark" %}</span>
    <span>{% trans "System" %}</span>
</button>
```

2. Ship `locale/` directory with `.po` files for common languages (at minimum: en, es, fr, de, ja, zh, ar, pt)
3. Component strings are extracted via standard `django-admin makemessages`
4. Theme authors who need custom labels override via Django's translation mechanism (`locale/` in their project), not by overriding templates
5. This is a prerequisite for Phase 7 (RTL) — RTL languages need translated strings, not just flipped layout

**Why do this with Phase 2**: Every new component added without `{% trans %}` is technical debt. Retrofitting i18n into 20 component templates later means touching every template and breaking every theme override. Do it from day one.

### I54: Theme Performance Budget & Size Tracking (Priority: Medium — do with I26)

**Problem**: As the component library grows (Phase 2: 15 new components, Phase 3: layouts), CSS output size will increase significantly. There's no guardrail preventing a theme from ballooning to 100KB+ of CSS. No tooling to answer "how much CSS does my theme generate?" or "did this change increase CSS size?"

**Fix**:
1. Add `python manage.py djust_theme stats my-theme` command:
```
Theme: my-theme
Total CSS: 14.2 KB (gzip: 3.8 KB)
  Tokens:     2.1 KB  (15%)
  Base:       1.8 KB  (13%)
  Components: 8.4 KB  (59%)
  Layouts:    1.2 KB  (8%)
  Overrides:  0.7 KB  (5%)
Token count: 31 colors + 24 spacing + 12 typography = 67 total
Components used: 8 of 20
```

2. Add `performance` section to `theme.toml`:
```toml
[performance]
max_css_size = "50kb"        # Warn if total CSS exceeds this
max_gzip_size = "15kb"       # Warn if gzipped CSS exceeds this
```

3. `validate` command checks size budgets and warns when exceeded
4. The `stats` command outputs JSON with `--json` flag for CI integration:
```bash
python manage.py djust_theme stats my-theme --json | jq '.total_css_kb'
# Use in CI: fail build if CSS exceeds budget
```

### I55: Tokens Studio Import (Priority: Low — do with I30)

**Problem**: I30 covers W3C Design Tokens JSON (DTCG format), but the most widely-used design token tool is Tokens Studio for Figma (formerly "Figma Tokens"), which uses its own `.tokens.json` format. The Tokens Studio format includes features not in W3C DTCG: token sets, themes as set combinations, math expressions, and references (`{colors.primary.500}`). Teams using Tokens Studio (which has 200K+ Figma installs) can't import their tokens without manual conversion.

**Fix**:
1. Add `TokensStudioImporter` to `djust_theming/tokens_studio.py`
2. CLI: `python manage.py djust_theme tokens-studio-import tokens.json`
3. Maps Tokens Studio concepts to djust-theming:
   - Token sets → theme preset variants (light set → light mode, dark set → dark mode)
   - Color tokens → `ColorScale` via hex/rgb conversion (I16)
   - Typography tokens → design token overrides
   - Spacing/sizing tokens → spacing scale overrides
   - References (`{colors.primary}`) → resolved to concrete values during import
4. Round-trip: `tokens-studio-export` generates `.tokens.json` for pushing back to Figma

### I56: Language-Aware Font Stacks (Priority: Low — do with Phase 7)

**Problem**: Typography tokens define a single `--font-family-body` and `--font-family-heading` for all languages. CJK (Chinese, Japanese, Korean) text requires different fonts than Latin text. Arabic script requires fonts with proper ligature support. A theme using Inter for body text looks broken when rendering Japanese because Inter has no CJK glyphs — the browser falls back to a system CJK font with different metrics, causing layout shifts and inconsistent appearance.

**Fix**:
1. Add `[typography.locale]` section to `theme.toml`:
```toml
[typography]
font-family-body = "'Inter', system-ui, sans-serif"

[typography.locale.ja]
font-family-body = "'Noto Sans JP', 'Hiragino Sans', sans-serif"

[typography.locale.ar]
font-family-body = "'Noto Sans Arabic', 'Segoe UI', sans-serif"
direction = "rtl"

[typography.locale.zh-Hans]
font-family-body = "'Noto Sans SC', 'PingFang SC', sans-serif"
```

2. `{% theme_head %}` checks `LANGUAGE_CODE` (or `request.LANGUAGE_CODE` for per-request locale) and emits locale-specific font overrides
3. Default themes ship with sensible system font stacks for major language families
4. This complements Phase 7 (RTL) — Arabic RTL layout is incomplete without proper Arabic fonts

---

## Prioritized Execution Order

### Tier 0: Security & Resilience (Do Immediately — Before Any Feature Work)

| # | Item | Effort | Impact | Dependencies |
|---|------|--------|--------|--------------|
| I43 | Component parameter sanitization (XSS) | Low | **Critical** | None — `mark_safe(f'...')` with interpolated params is an active XSS vector |
| I57 + I132 | Cookie security hardening + stale cookie cleanup | Low | **Critical** | None — cookie values flow to template context without validation; stale cookies persist for 1 year |
| I58 | localStorage graceful degradation | Low | High | None — crashes theme init in Safari private browsing / sandboxed iframes |
| ~~I4~~ + I48 | ~~Static asset versioning~~ (DONE #10) + URL resolution | Low | High | I4 done; I48 may be resolved too (verify) |
| I120 | ThemeManager.toggle_mode() race condition | Low | High | None — TOCTOU race corrupts state in concurrent sessions/tabs |
| I122 | ThemeMixin._skip_render initialization | Low | High | None — latent `AttributeError` crash if subclass skips `super().mount()` |
| I121 | Module-level logger setup in manager.py | Low | Low | None — code hygiene, do alongside other Tier 0 fixes |

### Tier 1: Foundation (Do First — Unblocks Everything)

| # | Item | Effort | Impact | Dependencies |
|---|------|--------|--------|--------------|
| ~~I1~~ + I43 + I123 + I128 | ~~Decouple inline HTML~~ (DONE #7) + sanitize + anti-FOUC DRY + ThemeMixin type annotations | Low | High | None — I1 done; I43/I123/I128 still needed |
| ~~I2~~ + I17 + I34 + I50 + I61 + I129 | ~~Extract component CSS~~ (DONE #8) + namespace prefix + fallback chain + modern CSS + CSP modes + CSS fallback values | Medium | High | I2 done; remaining items restructure CSS output and delivery |
| I9 | CSS cascade layers (`@layer`) | Low | High | Do alongside I17 — structures CSS for theme overrides |
| I16 + I21 + I30 + I41 + I44 + I49 | Color format interop + auto-palette + W3C tokens + quality + validation + OKLCH | Medium | High | None — unblocks design-tool-to-theme workflow. I49 ensures palette generation is perceptually accurate from day one |
| ~~I23~~ + I84 | ~~AppConfig.ready() system checks~~ (partially DONE in I6 #13) + zero-config experience | Low | High | I6 added checks.py + ready(); I23 extends with config validation; I84 is standalone |
| ~~I3~~ | ~~ThemeManager caching on request~~ (DONE #9) | Low | Medium | None |
| ~~I5~~ + I24 + I28 + I45 + I124 | ~~CSS caching~~ (DONE #11) + path consolidation + state hash + graceful failure + fallback logging | Medium | High | I5 done; remaining items consolidate and harden |
| I27 + I60 + I126 | Component tag test harness + JS test suite + tag param validation | Medium | Medium | None — test harness defines valid param contracts; I126 catches typos at render time |
| I87 | djust-components integration strategy decision | Low | **Critical** | None — **BLOCKING for Phase 2 scope**. Decide before building any new components |
| I88 + I125 + I127 + I130 | Theme switching without djust LiveView + event error feedback + preset swatch mode fix + push_event warning | Medium | High | None — makes djust-theming standalone-viable; I125/I127/I130 fix UX gaps in theme switching |

### Tier 2: Template-Driven Theming (Core Vision)

| # | Item | Effort | Impact | Dependencies |
|---|------|--------|--------|--------------|
| **Phase 1** | **Template Override System** | **Medium** | **Critical** | **I1, I2, I9, I23** |
| I78 | Ejectable component pattern (copy-to-project) | Low | **High** | **Phase 1** — escape hatch for radical template restructuring, complements I11 slots |
| I73 | Theme selection via URL parameter | Low | High | Phase 1 (ThemeManager resolution) — high-value for demos/marketing/sharing |
| I37 | Token reference documentation generator | Medium | High | Phase 1 (token system stable) |
| I25 | Dynamic preset registration API | Medium | Medium | Phase 1 (ThemeRegistry) |
| I32 | Multi-tenant theme support | Medium | High | Phase 1 (ThemeRegistry) + I21 (auto-palette) |
| I10 | Critical CSS inlining | Medium | Medium | Phase 1 (`{% theme_head %}` rework) |
| I18 | Container-scoped theming | Medium | Medium | Phase 1 (template resolution) |
| I39 | Theme linting CLI | Medium | Medium | Phase 1 (themes exist to lint) |
| I75 | Theme export as standalone CSS | Medium | High | Phase 1 — unlocks use outside Django, prototyping, sharing |
| I29 | Graceful degradation for missing theme assets | Low | Low | Phase 1 (theme discovery) |
| I79 | Theme Token API for headless frontends | Medium | Medium | Phase 1 — enables React/Vue/Svelte consumers of theme tokens |
| **Phase 2** | **Component Library (15 new) + Slot System (I11)** | **High** | **High** | **Phase 1, I27, I87** |
| I80 | Template fragment library (icon, spinner, empty, close) | Low | **High** | **Do with Phase 2** — one fragment override propagates to all components |
| I81 | Accessibility tree validation for overrides | Medium | High | **Do with I27** — catches ARIA regressions in theme overrides |
| I85 | Dark mode image handling (`theme_picture` tag) | Low | Medium | **Do with Phase 2** — dark mode is half-baked without image awareness |
| I90 | Component state persistence across re-renders | Medium | High | **Do with Phase 2** — interactive components need state strategy from day one |
| I53 | Internationalized component strings (`{% trans %}`) | Low | High | **Do with Phase 2** — every component added without i18n is debt |
| I59 | JavaScript feature detection + minimum browser spec | Low | Medium | **Do with Phase 2** — `components.js` grows the compat surface |
| I62 | Focus styling standardization (`data-theme-interactive`) | Low | Medium | **Do with Phase 2** — prevents inconsistency in 15 new components |
| I51 | CSS nesting for component styles | Low | Medium | Phase 2 (authoring convention for new component CSS) |
| I19 + I63 + I71 | Shadow & animation tokens + animation consistency + @property animated tokens | Medium | High | Phase 2 (components need shadow/animation tokens; I71 enables smooth preset switching) |
| I46 | CSS transition on theme switch | Low | Medium | Phase 2 (View Transitions API, no-reload preset swap) — I71 makes this dramatically smoother |
| I26 + I54 | CSS minification/compression + performance budgets | Medium | Medium | I5 + I24 (single generation path) |
| **Phase 3** | **Layout Templates** | **Medium** | **High** | **Phase 1** |
| I86 | Theme-aware meta tags and PWA manifest | Low | Medium | **Do with Phase 3** — layouts own `<head>`, meta tags belong there |
| I20 | Responsive token system | Medium | High | Phase 3 (layouts need responsive behavior) |
| I38 | Component container queries | Medium | Medium | Phase 3 (layouts set container-type) |
| I72 | CSS subgrid for layout components | Medium | Medium | Phase 3 (card grids, form layouts need track alignment) |

### Tier 3: Polish & Ecosystem

| # | Item | Effort | Impact | Dependencies |
|---|------|--------|--------|--------------|
| ~~I6~~ + I52 | ~~Accessibility contrast validation~~ (DONE #13) + color blindness simulation | Low | Medium | I6 done; I52 catches issues contrast checks miss |
| I12 | Component CSS tree-shaking | Medium | Medium | Phase 2 |
| I65 | Compound component patterns (form groups, card grids, data tables) | Medium | High | Phase 2 (individual components must exist first) |
| Phase 4 | Page Templates | Low | Medium | Phase 3 |
| Phase 5 | Design System Template Variants | High | Medium | Phase 1 + 2 |
| I64 | Starter theme kits (SaaS, marketing, docs, admin) | Medium | **High** | Phase 5 (kits bundle layouts + components + tokens) |
| I68 | Theme migration assistant (`djust_theme migrate`) | Medium | High | Phase 5 (themes exist to migrate) |
| I33 | Component variant registration | Low | Medium | Phase 5 (ThemeRegistry mature) |
| I42 | Theme package dependency declaration | Low | Medium | Phase 5 (packages exist to version) |
| I55 | Tokens Studio import | Low | Medium | I30 (W3C tokens foundation) |
| I89 | Tailwind v4 CSS-first configuration | Low | Medium | I30 (design tool integration batch) |
| I91 | Theme versioning and compatibility matrix | Medium | Medium | Phase 5 (pip-installable themes create version risk) |
| Phase 6 | Form Integration | Medium | Medium | Phase 2 |
| I31 | Theme-aware Django admin | Medium | Medium | Phase 3 (layouts) |
| ~~I7~~ | ~~Token boundary cleanup~~ (DONE #14) | Low | Low | Before Phase 5 |
| ~~I8~~ | ~~Deprecate themes.py~~ (DONE #15) | Low | Low | Before Phase 5 |
| I22 + I77 | Theme inheritance validation + chain visualization | Low | Medium | Phase 5 |
| I131 | localStorage key collision in multi-app contexts | Low | Low | I18 (container-scoped theming handles CSS; I131 handles state) |
| I133 | Type hints across core modules + py.typed marker | Low | Medium | Incremental — no blocker, improves contributor DX and AI tooling |
| Phase 7 | RTL, Reduced Motion, Print (I13, I15) + I53 + I56 | Medium | Medium | Phase 2 + 3. I56 (locale fonts) completes i18n story |
| Phase 8 | Preview & Inspector | Low | Low | Phase 2 + 3 |
| I74 | Sample content fixtures for theme development | Low | Medium | Phase 8 (gallery needs realistic content to surface real bugs) |
| I66 | Theme preview thumbnail generation (SVG + screenshot) | Low | Medium | Phase 8 (gallery view to screenshot) |
| I35 + I40 | Theme dev server + HMR for templates | Medium | Medium | Phase 8 (gallery view) |
| I47 | Theme debugging overlay | Low | Medium | Phase 8 (debug tooling) |
| I36 | Theme snapshot testing for CI | Low | Medium | Phase 8 (testing infrastructure) |
| I14 | Theme Composition (mix and match) | High | Medium | Phase 5 |
| I69 | CSS `@scope` for partial theme application | Low | Low | I18 (container-scoped theming) |
| I67 | Theme usage analytics hook | Low | Low | Phase 5 (themes exist to track) |
| I76 | Token autocomplete schema for editors (VS Code, JetBrains) | Low | Medium | I37 (token reference — same source data) |
| I82 | Email-compatible theme export | Low | Medium | Phase 4 (page templates) — transactional emails match app theme |
| I83 | Theme conflict detection for multi-app projects | Low | Medium | Phase 5 (pip-installable themes create collision risk) |
| Phase 9 | Docs & Ecosystem | Low | Low | All above |
| I70 | Figma plugin for token sync | High | Medium | Phase 9 (ecosystem play) |

### Critical Path Summary

**Tier 0 first.** I43 + I57 + I58 are security/resilience fixes that should ship in a patch release (v1.1.3) before any feature work. Total effort: ~1 day. ~~I4~~ (static URL resolution) is done (#10); verify I48 is also resolved.

**I60 (JS test suite) is the gating item for Phase 2.** Every new JS behavior added without tests is a regression waiting to happen. Build the harness early so Phase 2's `components.js` development is test-driven from day one.

**I61 (CSP compatibility) should be designed with I2** even if full implementation is deferred. The CSS delivery pipeline (inline vs. linked vs. nonce) must be decided before I2 extracts CSS from templates — the extraction strategy depends on how CSS will be served.

**I78 (Ejectable Components) is the critical complement to I11 (Slots).** Together they form a two-tier override strategy: slots for surgical changes (override icon rendering without touching button structure), eject for radical rewrites (completely replace button HTML while preserving the contract). Without eject, theme authors who need 100% control must work around the inheritance system. The eject command should ship with Phase 1 since it's the escape hatch that makes template inheritance safe to adopt — authors know they can always eject if inheritance doesn't fit.

**I80 (Template Fragments) multiplies the value of every template override.** A theme that overrides `fragments/icon.html` once changes icon rendering across *every* component — buttons, badges, nav items, modals, alerts. Without fragments, the same icon override must be duplicated across 20 component templates. This is the DRY principle for templates and should be built into Phase 2's component architecture from day one.

**I81 (Accessibility Tree Validation) catches the class of bugs that visual testing misses.** A theme author who replaces `<button>` with a styled `<div>` creates a component that *looks* correct but is invisible to screen readers. This must be part of the I27 test harness before Phase 2 creates 15 new component contracts.

**The "golden path" for a theme author should be:**

```
1. Run: djust_theme create-preset --primary "#1E40AF"        → Full preset from one color (I16 + I21 + I49 OKLCH)
2. Run: djust_theme create-theme my-theme --preset my-brand   → Scaffold with manifest (Phase 1.3) + editor autocomplete (I76)
3. Override 2-3 component slots (i18n-ready, a11y-validated)  → Phase 2 + I11 + I53 + I81
3b. OR: djust_theme eject button card --theme my-theme        → Full control where slots aren't enough (I78)
4. Override fragments/icon.html once → all icons change        → I80 fragment library
5. Pick a layout template                                     → Phase 3
6. Preview with realistic content fixtures                     → I74 stress-tests edge cases
7. Run: djust_theme validate my-theme --color-blind --a11y    → I52 + I81 catch visual + structural a11y gaps
8. Run: djust_theme stats my-theme                            → I54 confirms CSS budget
9. Run: djust_theme export my-theme --output dist/            → I75 standalone CSS for sharing/prototyping
10. Deploy                                                    → light-dark() + @layer = minimal CSS, smooth transitions (I71)
```

**The "golden path" for a designer should be:**

```
1. Export design tokens from Figma as W3C JSON               → Standard designer workflow
2. Run: djust_theme import-tokens tokens.json --name my-brand → I30 (W3C import)
3. Run: djust_theme create-theme my-theme --preset my-brand   → Phase 1.3
4. Hand off to developer for template customization           → Phase 2 + I11
```

**The "golden path" for a SaaS/multi-tenant app should be:**

```
1. Tenant provides brand color at signup                      → Single hex input
2. PaletteGenerator creates preset automatically              → I21 (auto-palette)
3. TenantThemeResolver loads preset per-request                → I32 (multi-tenant)
4. Tenant sees branded UI with zero manual theming             → Fully automated
```

**I64 (Starter Theme Kits) is the highest-ROI item in Tier 3.** The blank-canvas problem is the #1 reason theme systems go unused — developers stare at an empty scaffold and don't know where to start. Shipping 3–4 opinionated kits (SaaS dashboard, marketing, docs, admin) immediately demonstrates the system's power AND serves as reference implementations for theme authors. Kits depend on Phase 5 (design system variants) but should be designed alongside Phase 3 (layouts) since each kit is primarily a layout choice + token selection.

**I65 (Compound Components) should ship with Phase 2.** Individual components alone don't solve the "consistent app" problem — it's the compositions (form groups, data tables, card grids) that make themes feel complete. Designing compound patterns alongside individual components prevents "composition drift" where every app invents its own component layout.

**I68 (Theme Migration Assistant) is essential before Phase 5 creates an ecosystem.** Without automated migration tooling, every djust-theming major version creates a support burden for theme authors. Build migration infrastructure early so the v1→v2 transition is smooth.

**Phases 1-3 + I16/I21 are the minimum viable "template-driven theming" system.** After those, a theme author can:
- Start from a single brand color and get a complete preset
- Create a theme directory with a manifest
- Override any component/layout template (or just specific slots within them via I11)
- Set custom design tokens
- Have Django resolve their templates automatically
- Write custom CSS that reliably wins via `@layer theme` (I9)
- Use namespaced classes that don't collide with existing CSS (I17)
- Get misconfigurations caught at startup, not in production (I23)
- Import tokens from Figma/design tools via W3C JSON format (I30)
- Browse all available tokens via CLI or gallery (I37)
- Get quality warnings when auto-generated palettes have accessibility issues (I41)

**Tier 0 (I43 + I57/I132 + I58 + I4/I48 + I120 + I122) is the most urgent work.** These are security and resilience fixes that affect every current deployment:
- I43: `mark_safe(f'...')` with interpolated params = XSS vector
- I57 + I132: Cookie values flow to template context without validation; stale cookies persist for 1 year after preset removal
- I58: `localStorage` crash in Safari private browsing kills theme initialization entirely
- I4/I48: Hardcoded `/static/` paths break CDN, custom prefix, and `ManifestStaticFilesStorage` deployments silently
- I120: `toggle_mode()` has a TOCTOU race — concurrent tabs can corrupt theme state
- I122: `_skip_render` is never initialized — `AttributeError` crash if subclass skips `super().mount()`

All are low-effort (< 1.5 days combined) and should ship as v1.1.3 patch before any feature work.

---

## New Improvements (Added 2026-03-22, batch 4)

Identified during architecture review focused on developer experience, resilience, and real-world theme authoring friction points.

### I92: Theme Hot-Reload via djust WebSocket (Priority: High — do with Phase 1)

**Problem**: Theme authors iterate by editing `theme.toml` or `tokens.css`, saving, then manually refreshing the browser. The feedback loop is slow — especially when tweaking color values where visual comparison needs to be instant. djust already has a WebSocket connection for LiveView updates, but theme file changes don't trigger re-renders. Outside of djust (plain Django), there's no reload mechanism at all.

**Fix**:
1. Add a `ThemeFileWatcher` that monitors the active theme directory for changes (using `watchfiles` — already a Django dev dependency via `runserver`)
2. When a theme file changes:
   - `theme.toml` change → invalidate `ThemeManager` cache (I3), re-resolve theme state
   - `tokens.css` change → invalidate CSS cache (I5), regenerate CSS
   - Template change → no server action needed (Django template loader picks up changes)
3. **With djust**: Send a `theme_reload` event over the existing WebSocket. Client-side JS re-fetches CSS via the `/theming/css/` endpoint and hot-swaps the `<link>` or `<style>` tag. No full page reload — just CSS swap. Templates require full re-render (send `html_update` like any other LiveView change).
4. **Without djust**: Add an optional `theme_dev.js` that polls `/theming/css/` with `If-None-Match` (ETag). On 200 (CSS changed), swap the stylesheet. On 304 (no change), no-op. Poll interval: 1s. Only loaded when `DEBUG=True`.
5. Add `DJUST_THEMING['HOT_RELOAD']` setting (default: `settings.DEBUG`).

**Why this matters**: The theme authoring loop must be as tight as frontend hot-reload. Every second of latency between "save" and "see result" compounds into hours of wasted time across a theme's development lifecycle. This is the single biggest DX win for theme authors.

### I93: CSS Custom Property Fallback Values (Priority: High — do with I2)

**Problem**: Component CSS references tokens as bare variables: `background: hsl(var(--primary))`. If a theme author's `tokens.css` override misses a token (typo, incomplete override, or new token added in an update), the variable resolves to the initial value (nothing), and the component renders with transparent/invisible backgrounds. The failure is silent — no console error, no visual indication of what went wrong. Theme authors debugging this stare at invisible buttons wondering what happened.

**Fix**:
1. All component CSS must use fallback values: `background: hsl(var(--primary, 221 83% 53%))` where the fallback is the default preset's value
2. Add a CSS generation step that injects fallbacks into component CSS from the default preset's token values
3. `theme.toml` can declare `[extends] base = "default"` — the base theme's tokens serve as fallbacks
4. The `validate` command (Phase 1.5) checks for missing tokens by comparing theme's defined tokens against the full token schema and warns about any gaps
5. In `DEBUG` mode, missing tokens emit a console warning via a CSS `@supports` trick or `theme_dev.js` check

**Why this matters**: Silent failures are the worst DX. A theme that "almost works" but has invisible components is harder to debug than one that fails loudly. Fallbacks make partial theme overrides safe by default.

### I94: Component Override Guide Generator (Priority: Medium — do with Phase 2)

**Problem**: Theme authors need to know what CSS classes to target, what template slots exist, and what tokens each component uses. The contracts (Phase 2.2) document the *requirements* but not the *anatomy*. A theme author looking at a button doesn't know that `.btn__icon` is the class for the icon slot, or that `--btn-padding-x` is the horizontal padding token. Currently this requires reading source code.

**Fix**:
1. Add `python manage.py djust_theme anatomy <component>` command:
```
$ python manage.py djust_theme anatomy button

button (button.html)
═══════════════════

HTML Structure:
  <button class="btn btn--{variant} btn--{size}">
    ├── {% block icon %} → .btn__icon
    ├── {% block content %} → (text node)
    └── {% block loading %} → .btn__spinner

CSS Tokens Used:
  --primary, --primary-foreground    (variant: primary)
  --secondary, --secondary-foreground (variant: secondary)
  --destructive, --destructive-foreground (variant: destructive)
  --radius                           (border-radius)
  --ring                             (focus outline)

Slots:
  icon     — Icon element before text. Default: conditional <span>
  content  — Main text content. Default: {{ text }}
  loading  — Loading spinner. Default: conditional <span>

Override Examples:
  Minimal: override just the icon slot
  Full:    eject with `djust_theme eject button --theme my-theme`
```

2. Auto-generate this from template source (parse `{% block %}` tags + CSS class references) — no manual maintenance
3. Add `--format html` flag that generates a browsable HTML page with live examples (feeds into Phase 8 gallery)
4. The `anatomy` data structure is also consumed by I76 (editor autocomplete) and I37 (token reference docs)

### I95: Progressive Enhancement Strategy & Browser Support Matrix (Priority: Medium — do before Phase 2)

**Problem**: The roadmap adopts multiple modern CSS features across different items: `@layer` (I9, 95% support), `light-dark()` (I50, 94%), `color-mix()` (I50, 96%), native nesting (I51, 91%), `oklch()` (I49, 93%), `@property` (I71, ~88%), `@container` (I38, 90%), `@scope` (I69, ~75%), CSS subgrid (I72, ~85%). Each item independently justifies its browser support, but there's no unified strategy. A theme author doesn't know the minimum browser target. If they use `oklch()` tokens but their users are on older Safari, they get broken colors with no fallback.

**Fix**:
1. Define a clear browser support matrix in `CONTRIBUTING.md` and the theme author guide:
   - **Tier A (must work)**: Chrome 105+, Firefox 121+, Safari 16.4+, Edge 105+ (~93% global coverage)
   - **Tier B (enhanced experience)**: Chrome 111+, Firefox 128+, Safari 17+ (~88% global coverage) — adds `@property`, native nesting
   - **Tier C (progressive)**: Latest stable of all browsers — adds `@scope`, CSS subgrid
2. CSS generator emits Tier A features by default. Tier B/C features are opt-in via:
```python
DJUST_THEMING = {
    'CSS_FEATURES': 'tier-a',  # 'tier-a' (default), 'tier-b', 'tier-c', 'latest'
}
```
3. For each Tier B/C feature, the generator emits both the modern syntax AND a Tier A fallback:
```css
/* Tier A fallback */
:root { --background: 0 0% 100%; }
.dark { --background: 222 47% 11%; }
/* Tier B enhancement */
@supports (color: light-dark(red, blue)) {
    :root { --background: light-dark(hsl(0 0% 100%), hsl(222 47% 11%)); }
}
```
4. `theme.toml` can declare a minimum browser tier:
```toml
[compatibility]
min_tier = "tier-b"   # Theme requires Tier B features (e.g., uses native nesting in overrides)
```
5. `validate` command checks theme CSS for features above its declared tier

**Why this matters**: Without a unified strategy, each modern CSS adoption is a gamble. A clear tier system lets theme authors make informed decisions and the generator handle fallbacks automatically.

### I96: Theme Inheritance Cycle Detection (Priority: Low — do with Phase 1)

**Problem**: `theme.toml` allows `extends.base = "other-theme"`. If theme A extends B and theme B extends A (directly or through a chain), the template resolver enters an infinite loop. Similarly, a chain longer than 3-4 levels deep is likely a mistake and will cause performance issues in template resolution (each render walks the full chain).

**Fix**:
1. `ThemeRegistry` validates the inheritance graph at startup (in `ready()`) — detect cycles using a simple DFS
2. System check `djust_theming.E004`: "Theme 'A' creates a circular inheritance: A → B → C → A"
3. System check `djust_theming.W004`: "Theme 'A' has inheritance depth of 5 (max recommended: 3)" — warning, not error, since deep chains are legal but suspicious
4. `ThemeTemplateLoader` has a hard depth limit (default: 10) to prevent infinite recursion even if cycle detection is bypassed

### I97: Theme Preview URL with Shareable State (Priority: Medium — do with I73)

**Problem**: I73 adds theme selection via URL parameter (e.g., `?theme=material`). But theme previewing also needs preset + mode + token overrides in the URL for sharing. A designer should be able to send a link like `?theme=my-theme&preset=brand&mode=dark` to a stakeholder for approval. Currently there's no way to encode theme state in a URL and have it override the session/cookie state temporarily without persisting it.

**Fix**:
1. Extend I73 to support full theme state in URL: `?djt_theme=name&djt_preset=name&djt_mode=light|dark`
2. URL params override session/cookie state for that request only — they don't persist (no cookie write)
3. Add `{% theme_preview_url %}` template tag that generates a shareable URL with current theme state encoded
4. For token overrides, support a compact format: `?djt_tokens=primary:221.83.53,radius:0.5rem` (Base64-encoded for complex values)
5. The preview URL is shown in the inspector (Phase 8) and the gallery view — click any theme variant to get a copyable URL
6. Security: URL params are read-only previews. They never write to session or cookies. Validate all param values against registered presets/themes.

### I98: Token Diff Command (Priority: Low — do with Phase 1)

**Problem**: When comparing themes or debugging why a component looks different between two themes, there's no tool to see exactly which tokens differ. A theme author extending another theme needs to know "what did my parent theme actually set?" Theme authors debugging a visual discrepancy need to know "which token is different between my-theme and default?"

**Fix**:
1. Add `python manage.py djust_theme diff <theme-a> <theme-b>` command:
```
$ python manage.py djust_theme diff my-theme default

Token Differences: my-theme vs default
═══════════════════════════════════════

  Token                   my-theme              default
  ─────────────────────   ───────────────────   ───────────────────
  --primary               210 90% 45%           221 83% 53%
  --radius                0.25rem               0.5rem
  --font-family-heading   'Inter', sans-serif   system-ui, sans-serif

  Changed: 3 tokens
  Identical: 64 tokens
  Only in my-theme: 0
  Only in default: 0
```

2. Add `--mode light|dark` flag to compare specific mode variants
3. Add `--format json` for programmatic consumption
4. This is distinct from I22 (inheritance validation) — I22 checks compatibility, I98 shows values

### I99: Semantic Token Aliases (Priority: Medium — do with Phase 2)

**Problem**: Token names like `--primary`, `--secondary`, `--destructive` are generic design system terms. Real applications think in domain-specific terms: `--price-color`, `--header-bg`, `--sidebar-nav-active`. Currently there's no way to create semantic aliases that map to theme tokens. Theme authors who want `--cta-button-bg` to always track `--primary` must duplicate the value — and when the preset changes `--primary`, the alias is stale.

**Fix**:
1. Add `[tokens.aliases]` section to `theme.toml`:
```toml
[tokens.aliases]
cta-button-bg = "var(--primary)"
cta-button-fg = "var(--primary-foreground)"
price-color = "var(--success)"
sidebar-bg = "var(--card)"
header-bg = "color-mix(in oklch, hsl(var(--background)) 95%, hsl(var(--primary)))"
```

2. Aliases are emitted as additional CSS custom properties in the tokens layer:
```css
@layer tokens {
    :root {
        /* ... standard tokens ... */
        --cta-button-bg: var(--primary);
        --price-color: var(--success);
        --sidebar-bg: var(--card);
        --header-bg: color-mix(in oklch, hsl(var(--background)) 95%, hsl(var(--primary)));
    }
}
```

3. Aliases follow the token cascade — when `--primary` changes (preset switch, mode toggle), aliases update automatically because they use `var()` references
4. The `anatomy` command (I94) shows available aliases alongside standard tokens
5. Apps can define project-level aliases in settings (not just theme-level), useful for domain-specific vocabulary that shouldn't be in a reusable theme

**Why this matters**: Bridging the gap between generic design tokens and domain-specific styling vocabulary makes themes more maintainable. Instead of searching "which token is my CTA button using?", developers reference semantic names that self-document intent.

### I100: Theme Testing Fixtures with Edge-Case Content (Priority: Low — do with I74)

**Problem**: I74 provides sample content fixtures for theme development (realistic text, images, data). But the most revealing content for testing themes isn't "normal" — it's edge cases: extremely long titles that wrap, empty states, single-character names, RTL text mixed with LTR, very long unbreakable strings (URLs, hashes), components with 0 items vs 1000 items, deeply nested navigation. Theme authors need pathological content to surface layout bugs.

**Fix**:
1. Ship two fixture sets: `sample_content` (realistic) and `stress_content` (edge cases)
2. `stress_content` includes:
   - Titles: 5 words, 50 words, 200 characters with no spaces (tests overflow/truncation)
   - Numbers: 0, 1, 999, 1000000 (tests digit width, locale formatting)
   - Text: Latin, CJK, Arabic, Devanagari mixed in same page (tests font stacks)
   - Lists: 0 items, 1 item, 3 items, 50 items (tests empty states, pagination, scroll)
   - Images: missing image (tests alt text/fallback), tiny (16x16), huge (4000px wide)
   - Tables: 2 columns, 20 columns (tests horizontal scroll), 1 row, 500 rows
3. Gallery view (Phase 8) has a toggle: "Normal content" / "Stress test"
4. `validate` command gains `--stress` flag that renders all components with stress fixtures and checks for CSS overflow, text truncation, and layout breakage

---

## Updated Prioritization Notes (2026-03-22)

### Tier 1 Additions

| # | Item | Effort | Impact | Rationale |
|---|------|--------|--------|-----------|
| I92 | Theme hot-reload via file watcher + WS/polling | Medium | **High** | The #1 DX win for theme authors. Tight feedback loop = more themes created. Do with Phase 1. |
| I93 | CSS custom property fallback values | Low | **High** | Silent failures from missing tokens are the #1 debugging pain. Do with I2 (CSS extraction). |

### Tier 2 Additions

| # | Item | Effort | Impact | Rationale |
|---|------|--------|--------|-----------|
| I94 | Component anatomy/override guide generator | Medium | High | Reduces "how do I override this?" friction. Do with Phase 2. |
| I95 | Progressive enhancement strategy + browser tiers | Low | High | Unified strategy prevents per-feature browser gambles. Do before Phase 2. |
| I97 | Theme preview URL with shareable state | Low | High | Designers/stakeholders can review themes via link. Do with I73. |
| I99 | Semantic token aliases | Low | Medium | Bridges design tokens ↔ domain vocabulary. Do with Phase 2. |

### Tier 3 Additions

| # | Item | Effort | Impact | Rationale |
|---|------|--------|--------|-----------|
| I96 | Theme inheritance cycle detection | Low | Low | Safety net. Do with Phase 1. |
| I98 | Token diff command | Low | Medium | Debugging tool. Do with Phase 1. |
| I100 | Stress-test content fixtures | Low | Medium | Edge cases surface real bugs. Do with I74. |

### Updated Critical Path

**I92 (Hot-Reload) should be in Tier 1**, not deferred to Phase 8. Theme authoring DX is a gating factor for adoption. Without hot-reload, theme authors will judge the system as "painful" within the first 10 minutes of trying it. The implementation is low-complexity: file watcher + CSS swap (no template HMR needed — Django handles that). Wire into djust's WebSocket when available, fall back to polling when not.

**I93 (Fallback Values) should be bundled with I2** (CSS extraction). When CSS moves from inline `<style>` to external files, all `var()` references should include fallbacks from day one. Retrofitting fallbacks later means touching every component CSS file.

**I95 (Browser Tiers) must be decided before Phase 2** starts adding modern CSS features to 15 new components. Without the decision, each component author makes ad-hoc browser support choices that create an inconsistent baseline.

**The golden path for a theme author gains two steps:**

```
0. (New) Start dev server with hot-reload enabled       → I92 — instant CSS feedback
...
3c. (New) Run: djust_theme anatomy button               → I94 — know exactly what to target
...
```

**Tier 1 items should be done next** — they are small-to-medium fixes that unblock Phase 1 and dramatically improve the theme authoring experience. I2 + I9 + I17 + I34 + I61 together are especially important: component templates must be pure HTML structure, CSS must use cascade layers with fallback values, class names must be collision-safe, and the CSS delivery pipeline must support CSP-strict deployments before theme authors can meaningfully adopt the system.

**I23 (System Checks) should be done early in Tier 1** — it's low effort, high impact, and matches the pattern already established by djust core. Every misconfiguration caught at startup is a support ticket avoided.

**I5 + I24 + I28 + I45 (CSS caching + path consolidation + state hash + graceful failure) are the key performance and resilience items.** Currently every page load regenerates CSS from scratch. With Phase 2 adding 15 components, uncached generation will become a measurable bottleneck. Consolidating the dual generation paths (inline vs. linked) into one function eliminates a class of subtle divergence bugs. The state hash unifies all cache keying. I45 ensures that a CSS generation failure (invalid preset, corrupted tokens) falls back to minimal CSS rather than crashing the page with a 500 — critical for theme development where errors are frequent.

**I27 (Component Test Harness) must exist before Phase 2** — adding 15 components without a test pattern leads to untested components and undefined contracts. Building the harness first means every Phase 2 component gets contract-driven tests from day one.

**I11 (Component Slots) must be built into Phase 2** from the start — retrofitting slots into existing components after theme authors have already written overrides would be a breaking change. Design with slots from day one.

**I16 + I21 + I30 + I41 + I44 (Color interop + auto-palette + W3C tokens + quality controls + input validation) are the highest-ROI developer experience items.** Most theme authors will arrive with a hex color, not HSL values. Designers will arrive with Figma exports in JSON. Making both paths seamless is the difference between "cool framework" and "I shipped a custom theme in 10 minutes." I41 (quality controls) prevents the auto-palette from producing unusable themes with edge-case inputs — essential for the SaaS/multi-tenant use case where brand colors are untrusted user input. I44 (ColorScale validation) ensures the auto-palette never generates out-of-bounds HSL values that render differently across browsers.

**I37 (Token Documentation Generator) is critical for Phase 1 adoption.** The first thing a theme author asks is "what tokens can I override?" Without a discoverable answer, they'll read source code, guess wrong, and file issues. A `djust_theme tokens` CLI command and gallery reference tab answer this question definitively. This is low-hanging fruit once the token system is stable.

**I32 (Multi-Tenant Theme Support) is a strategic item** — it directly enables the djustlive PaaS use case (per-tenant branding) and is the killer feature for SaaS apps. Architecturally it's clean: a `ThemeResolver` protocol + one implementation. Low risk, high reward for the djust ecosystem.

**I34 (CSS Fallback Chain) is defensive design** — it prevents the most common failure mode for new theme authors (missing token → invisible text). Adding fallbacks to all `var()` references is mechanical work best done alongside I2 (CSS extraction). Doing it later means every component's CSS needs a second pass.

**I38 (Component Container Queries) should ship with Phase 3** — layouts set `container-type: inline-size` on content regions, and components should respond to their container width from day one. Retrofitting container queries after components are deployed means every existing theme's custom component CSS needs updating.

**I39 (Theme Linting) complements Phase 1's `validate` command.** Validation catches structural errors; linting catches quality issues (hardcoded colors, missing dark mode, specificity violations). Together they form a complete quality gate for themes. This is especially important once third-party themes exist — low-quality themes reflect poorly on the ecosystem.

**I40 (Template HMR) transforms the theme development inner loop.** CSS token changes are already live-updatable via CSS custom properties — the dev server just needs to swap the stylesheet. Template changes trigger targeted re-render via djust LiveView. This makes theme development feel as fast as editing in browser DevTools, which is the standard theme authors expect from modern tools.

**I71 (CSS @property for animated tokens) is the polish multiplier for I46.** I46 proposes smooth theme switching but without `@property`, custom property transitions are impossible — browsers can't interpolate string-typed variables. I71 makes preset switching visually smooth at the per-token level (each color channel animates independently). The effort is low (emit `@property` declarations in the CSS generator), the visual impact is dramatic, and it builds on I19 (animation tokens) naturally. Schedule it alongside I19 + I46.

**I73 (URL parameter theme selection) should ship with Phase 1.** It's low effort (add one more layer to `ThemeManager.get_state()` resolution), and it unlocks three high-value workflows: marketing demo links, theme preview sharing, and djustlive iframe embedding with per-customer presets. Without URL params, every demo or preview requires manual theme switching — a friction point that kills adoption at the "show it to stakeholders" stage.

**I75 (Standalone CSS export) is a strategic reach item for Tier 2.** Theming systems that only work inside their host framework have limited adoption. Exporting standalone CSS files means: front-end developers can prototype themes in CodePen without Django, designers can preview in Storybook, static sites can use djust-theming's token system, and theme packages can include pre-built CSS for zero-config use. This is what makes djust-theming a *design system platform*, not just a Django plugin.

**I42 (Package Dependencies) is essential before Phase 5 ships.** Without version compatibility declarations, every djust-theming upgrade risks breaking installed themes with no diagnostic path. Build the `[requires]` manifest section and compatibility checker before encouraging a theme package ecosystem.

**I46 (CSS Transition on Theme Switch) is a polish item for Phase 2.** The jarring instant color swap and full-page reload on preset change undermines the "live theme switching" value prop. The View Transitions API provides a smooth crossfade for supported browsers. More importantly, preset switches should fetch new CSS via the endpoint (no reload) — this is architecturally clean once I5/I24 consolidate CSS generation.

**I47 (Theme Debugging Overlay) should be designed with Phase 1 even though it ships with Phase 8.** The `data-theme-component` attribute (which template rendered this component) and `data-theme-resolved` attribute (which token values are active) need to be baked into the component rendering pipeline from day one. Adding them later means modifying every component template. The overlay UI itself is Phase 8, but the data attributes are Phase 1 infrastructure.

---

## New Improvements (Added 2026-03-22, batch 3)

Identified during automated roadmap review. Focus: real-world theme authoring friction, multi-tenant integration, and missing developer ergonomics.

### I30: W3C Design Tokens JSON Export/Import (Priority: High — do with I16)

**Problem**: The theming system only speaks HSL CSS custom properties. The W3C Design Tokens Community Group format (JSON) is becoming the standard interchange between design tools (Figma, Sketch, Adobe XD) and code. Designers export tokens as JSON; developers import them. Without W3C format support, the handoff between designer → developer requires manual translation. The Tailwind and shadcn exports exist, but these are framework-specific — W3C is framework-agnostic and increasingly universal.

**Fix**:
1. Add `djust_theming/tokens_export.py` with `export_w3c_tokens(theme_state) -> dict` that outputs tokens in W3C Design Tokens format:
   ```json
   {
     "color": {
       "primary": { "$value": "#1E40AF", "$type": "color" },
       "background": { "$value": "#FFFFFF", "$type": "color" }
     },
     "spacing": {
       "sm": { "$value": "0.5rem", "$type": "dimension" }
     }
   }
   ```
2. Add `import_w3c_tokens(json_data) -> ThemePreset` to create a preset from imported tokens
3. CLI: `python manage.py djust_theme export-tokens --format w3c > tokens.json`
4. CLI: `python manage.py djust_theme import-tokens tokens.json --name my-brand`
5. This complements I16 (color format interop) — together they make djust-theming a first-class citizen in design tool workflows

### I31: Theme-Aware Django Admin (Priority: Medium — do after Phase 3)

**Problem**: Many Django projects need a branded admin experience. Django admin uses its own CSS that's completely disconnected from djust-theming. A project that invests in a custom theme still has a generic admin. This is especially jarring for SaaS products where the admin is customer-facing.

**Fix**:
1. Add `DjustAdminSite` (subclass of `django.contrib.admin.AdminSite`) that injects theme CSS via `each_context()`
2. Provide `templates/admin/base_site.html` override that includes `{% theme_head %}` and wraps admin in theme CSS variables
3. Map admin's CSS classes to theme tokens: `--admin-header-bg: hsl(var(--primary))`, `--admin-link: hsl(var(--primary))`, etc.
4. Theme authors can override `admin/base_site.html` in their theme directory for full admin customization
5. Setting: `DJUST_THEMING['THEME_ADMIN'] = True` (default: `False` to avoid surprises)

This is a "wow" feature — branded admin with zero effort beyond enabling the setting.

### I32: Multi-Tenant Theme Support (Priority: Medium — do after Phase 1)

**Problem**: SaaS apps built with djust often need per-tenant theming — each customer sees their own brand colors. The current `ThemeManager` reads from `LIVEVIEW_CONFIG` (global) and session (per-user). There's no tenant-level override. djustlive (the PaaS platform in this workspace) needs exactly this: each deployed app should have its own theme preset derived from the customer's brand color.

**Fix**:
1. Add a `ThemeResolver` protocol/ABC with a `resolve(request) -> ThemeState | None` method
2. Default resolver reads from session/config (current behavior)
3. Add `TenantThemeResolver` that checks `request.tenant.theme_preset` (or similar) before falling back to default
4. Setting: `DJUST_THEMING['THEME_RESOLVER'] = 'myapp.resolvers.TenantThemeResolver'`
5. The resolver is called once per request (cached on `request._djust_theme_state` per I3)
6. Combine with I21 (auto-palette): tenant provides one hex color at signup → `PaletteGenerator` creates their preset → stored in DB → `TenantThemeResolver` loads it

This bridges djust-theming and djustlive: tenants get branded apps automatically.

### I33: Component Variant Registration (Priority: Low — do with Phase 5)

**Problem**: Component tags (`theme_button`, etc.) accept a fixed set of variants (e.g., `primary`, `secondary`, `destructive`, `ghost`, `link`). A theme author wanting to add a custom variant (e.g., `gradient`, `outline-primary`, `neon`) has two bad options: (a) abuse `**attrs` to pass custom CSS classes, or (b) fork the template tag. Neither is discoverable or validated.

**Fix**:
1. Add variant registration to the `ThemeRegistry`:
   ```python
   ThemeRegistry.register_variant('button', 'gradient', css_class='btn--gradient')
   ```
2. Theme's `theme.toml` can declare custom variants:
   ```toml
   [variants.button]
   gradient = { class = "btn--gradient", description = "Gradient fill button" }
   neon = { class = "btn--neon", description = "Glowing neon outline" }
   ```
3. Component tags validate variant names against registered variants
4. `validate` command checks that CSS for registered variants exists in the theme's CSS
5. Gallery view (Phase 8) automatically renders custom variants

### I34: CSS Custom Property Fallback Chain (Priority: High — do with I2)

**Problem**: Token references in component CSS have no fallback values: `color: hsl(var(--primary))`. If a theme overrides tokens but misses one, or if a component references a token the preset doesn't define, the result is invisible text or broken layout with no visible error. This is especially dangerous for theme authors extending base themes — they don't know which tokens are required vs. optional.

**Fix**:
1. All CSS token references include a fallback: `color: hsl(var(--primary, 221 83% 53%))` (the default preset's value)
2. `css_generator.py` generates fallback values from the `default` preset automatically
3. Component CSS linting (part of I27 test harness): check that every `var(--token)` reference includes a fallback
4. This makes themes resilient to incomplete token definitions — missing tokens silently fall back to sensible defaults rather than breaking

### I35: Theme Development Server Mode (Priority: Medium — do with Phase 8)

**Problem**: Developing a theme requires: edit template → reload browser → check all components → repeat. There's no live feedback loop. The inspector (Phase 8) helps with token editing, but template changes still require manual reload and navigation to each component.

**Fix**:
1. `python manage.py djust_theme dev my-theme` starts a development server showing the theme gallery (Phase 8.1) with auto-reload
2. File watcher on the theme directory triggers browser reload via SSE (not WebSocket — simpler, no djust dependency)
3. Gallery view shows all components in all variants side-by-side — one glance to see the full theme
4. Console overlay shows CSS validation warnings, missing tokens, and contrast issues in real-time
5. "Diff" panel comparing current theme render vs. the base theme it extends

This is the "inner loop" tool that makes theme development fast and enjoyable.

### I36: Theme Snapshot Testing for CI (Priority: Low — do with Phase 8)

**Problem**: Phase 8.4 describes visual regression testing via screenshots, but this requires a headless browser — heavy for CI. Many theme authors just want "did my template change break the HTML structure?" without pixel comparison.

**Fix**:
1. `python manage.py djust_theme snapshot my-theme --format html` renders all components and saves the HTML output (no browser needed)
2. `python manage.py djust_theme diff my-theme --format html` compares HTML snapshots using Python's `difflib`
3. Structural diff: ignores whitespace, attribute order; flags added/removed elements and changed classes
4. CI-friendly: runs in seconds, no browser dependency, outputs diff as GitHub-compatible annotation format
5. Complement (not replace) the pixel-based visual testing in Phase 8.4 — HTML snapshots catch structural regressions, pixel snapshots catch visual ones

---

## New Improvements (Added 2026-03-22, batch 4)

Identified during automated roadmap review. Focus: theme author inner-loop productivity, token discoverability, component-level responsiveness, and production readiness gaps.

### I37: Token Reference Documentation Generator (Priority: High — do with Phase 1)

**Problem**: Theme authors need to know what tokens exist, what they control, and what sensible values look like. Currently, the only way to discover available tokens is to read `presets.py`, `design_tokens.py`, and `css_generator.py` source code. This is hostile to non-Python-fluent designers and front-end developers — the target audience for theming. Without a token reference, theme authors guess at token names, misspell them (e.g., `--primary-forground`), and see silent failures (the fallback chain from I34 hides the error).

**Fix**:
1. Add `python manage.py djust_theme tokens [--theme default] [--format table|json|css]` command that outputs all available tokens with:
   - Token name (`--primary`, `--space-4`, `--font-size-base`)
   - Category (color, spacing, typography, shadow, animation, layout)
   - Current value (resolved for the specified theme/preset)
   - Description (what it controls, e.g., "Primary brand color, used for buttons, links, and active states")
   - Overridable (yes/no — some tokens are computed and shouldn't be overridden directly)
2. `--format css` outputs a `tokens-reference.css` file with all tokens as commented CSS custom properties — paste into an editor for autocomplete
3. `--format json` outputs W3C-compatible JSON (ties into I30)
4. The gallery view (Phase 8.1) renders a "Token Reference" tab showing all tokens with live color swatches
5. Token descriptions are defined once in Python (as docstrings or a `TOKEN_DOCS` dict) and flow into CLI, gallery, and exported formats

This is the documentation equivalent of I23 (system checks) — it prevents confusion before it starts. High priority because every theme author hits this wall within minutes of starting.

### I38: Component Container Queries for Context-Aware Sizing (Priority: Medium — do with Phase 3)

**Problem**: The roadmap mentions `@container` queries for layout templates (Phase 3.4 resolved decision) but doesn't address component-level container awareness. A `theme_card` rendered in a 250px sidebar column should look different from one in a 900px main content area — different padding, font sizes, image aspect ratios. Currently, components use fixed token values regardless of their container size. Theme authors must write manual `@container` rules for every component × container combination, which is combinatorial and tedious.

**Fix**:
1. All layout templates (Phase 3) set `container-type: inline-size` on content regions (sidebar, main, panel)
2. Component CSS includes built-in container query breakpoints for common adaptations:
   ```css
   .card { padding: var(--space-4); }
   @container (max-width: 400px) {
       .card { padding: var(--space-2); }
       .card__title { font-size: var(--font-size-sm); }
   }
   ```
3. Add responsive component tokens: `--card-padding-compact`, `--card-padding-normal` that container queries switch between
4. Theme authors can override the container breakpoint thresholds in `theme.toml`:
   ```toml
   [tokens.containers]
   compact_threshold = "400px"
   narrow_threshold = "600px"
   ```
5. Components that don't need container awareness (badge, tooltip) skip this — only structurally significant components (card, table, modal, tabs, navigation) get container-responsive CSS

This ensures components "just work" in any layout context — sidebar, dashboard grid, split panel — without theme authors writing responsive overrides per component.

### I39: Theme Linting CLI (Priority: Medium — do after Phase 1)

**Problem**: The `validate` command (Phase 1.5) checks structural correctness — does the theme render, are contracts satisfied, do static files exist? But it doesn't catch style quality issues: unused token overrides (defined in `tokens.css` but not referenced anywhere), overly specific selectors that fight the `@layer` system, `!important` usage (sign of specificity problems), hardcoded colors instead of token references, missing dark mode variants for custom CSS.

**Fix**:
1. `python manage.py djust_theme lint my-theme` performs CSS-level quality analysis:
   - **Unused tokens**: Token overrides in `tokens.css` not referenced by any component CSS or template `style` attribute
   - **Hardcoded values**: Color values (`#xxx`, `rgb()`, `hsl()`) in component CSS that should use tokens
   - **Specificity violations**: Selectors with ID selectors, `!important`, or specificity > `(0,3,0)` that bypass the layer system
   - **Missing dark mode**: Custom CSS with color values but no `[data-theme-mode="dark"]` counterpart
   - **Accessibility**: Inline `font-size` below 12px, `line-height` below 1.2, missing `focus-visible` styles
2. Output as warnings (not errors) — themes may have legitimate reasons for exceptions
3. `--fix` flag auto-fixes simple issues (e.g., replace `#1E40AF` with `hsl(var(--primary))` when the value matches a known token)
4. Integrates with CI: `--format github` outputs GitHub Actions annotation format

This complements `validate` (structural) with `lint` (quality). Together they catch configuration errors, contract violations, and style anti-patterns before deployment.

### I40: Theme Hot Module Replacement for Templates (Priority: Medium — do with I35)

**Problem**: I35 proposes a dev server with file watching and browser reload. But full page reload is disruptive — it resets scroll position, form state, and djust LiveView connections. Modern frontend tools (Vite, Turbopack) use HMR to update only the changed module. For a theming system, the "module" is a component template or CSS file — only the affected component should re-render, not the whole page.

**Fix**:
1. Theme dev server (I35) injects a small SSE client script that listens for file change events
2. **CSS changes**: When a `.css` file in the theme directory changes, inject the updated stylesheet without full reload (swap the `<link>` tag's `href` with a cache-busted URL). This is trivial and provides instant feedback for token tweaks.
3. **Template changes**: When a component template changes, the SSE event includes the component name. If djust LiveView is present, trigger a `_force_rerender` on all active views (existing mechanism). If not, fall back to full reload.
4. **Token changes**: When `tokens.css` changes, swap the `<style>` block containing generated tokens. All components update instantly because they reference CSS custom properties.
5. File watcher uses Django's built-in `StatReloader` mechanism — no new dependency

The key insight: CSS custom properties are live-updatable without DOM changes. Token edits → instant visual feedback. Template edits → targeted re-render. This makes the theme authoring loop feel as fast as browser DevTools.

### I41: Preset Derivation Quality Controls (Priority: Medium — do with I21)

**Problem**: I21 describes auto-generating a full preset from a single brand color via `PaletteGenerator`. The algorithm (derive secondary from complementary hue, accent from analogous hue, etc.) works for "normal" brand colors but produces poor results at the extremes: very light colors (pastels) generate invisible borders on white backgrounds; very dark colors create insufficient contrast in dark mode; pure grays (0 saturation) produce a monochrome palette with no accent differentiation; neon/high-saturation colors (e.g., `#00FF00`) create eye-strain palettes.

**Fix**:
1. Add a `PaletteQualityChecker` that scores generated presets on:
   - WCAG AA contrast ratios for all foreground/background pairs (existing in `accessibility.py`)
   - **Perceptual distinctness**: Key tokens (primary, secondary, accent, destructive) must be perceptually distinguishable (ΔE > 20 in CIELAB space)
   - **Saturation sanity**: No token exceeds saturation 95% (eye strain) or drops below 5% when source color has saturation > 30%
   - **Lightness range**: Background-to-foreground lightness range ≥ 60% (ensures readability)
2. When quality checks fail, `PaletteGenerator` auto-adjusts:
   - Boost saturation for grays (add 10-15% saturation to accent colors)
   - Clamp neons (reduce saturation to 80%)
   - Adjust pastel backgrounds (darken foreground, add border tokens)
3. CLI output shows quality score: `✓ Generated preset "my-brand" — quality: 94/100 (AA compliant, 2 warnings)`
4. Warnings explain what was adjusted and why

This prevents the "garbage in, garbage out" problem. A SaaS tenant providing `#FFFF00` as their brand color should still get a usable theme, not an accessibility nightmare.

### I42: Theme Package Dependency Declaration (Priority: Low — do with Phase 5)

**Problem**: Phase 5.2 describes pip-installable theme packages, but there's no mechanism for a theme to declare compatibility with specific djust-theming versions or require other packages. A theme built for djust-theming v2.0 (with `@layer` support, slot system, 20 components) will silently break on v1.x (no layers, no slots, 5 components). Worse, a theme extending another theme package (e.g., `djust-theme-material`) has no way to declare that dependency.

**Fix**:
1. `theme.toml` gains a `[requires]` section:
   ```toml
   [requires]
   djust_theming = ">=2.0,<3.0"     # semver range
   extends_package = "djust-theme-material>=1.0"  # optional: pip package dependency
   components = ["button", "card", "modal", "tabs"]  # components this theme overrides (for tree-shaking/validation)
   ```
2. `ThemeRegistry` checks version compatibility at discovery time — incompatible themes are excluded with a system check warning
3. `python manage.py djust_theme check-compat my-theme` reports:
   - Missing required components (theme overrides `modal.html` but `modal` component doesn't exist in this version)
   - Deprecated tokens used in `tokens.css`
   - Template slot names that changed between versions
4. `pyproject.toml` template (Phase 5.3 cookiecutter) auto-populates `[requires]` from the current installed version

This is essential for a healthy theme ecosystem — without version gates, every djust-theming upgrade is a potential theme breakage event with no diagnostic tooling.

---

## New Improvements (Added 2026-03-22, batch 5)

Identified during automated deep-dive into `components.py`, `manager.py`, `context_processors.py`, `theme.js`, `accessibility.py`, and `theme_tags.py`. Focus: security hardening, resilience under failure, and UX polish gaps.

### I43: Component Parameter Sanitization (Priority: Critical — do with I1)

**Problem**: `components.py` uses `mark_safe()` on f-strings that interpolate user-controllable parameters. For example, `ThemeSwitcher.render()` and `PresetSelector.render()` inject `variant`, `size`, `layout`, and preset `name` directly into HTML attributes and class names without escaping. While these values currently come from Python code (not direct user input), the template tag API accepts arbitrary `**attrs` that are rendered into HTML attributes unescaped. If any code path passes unsanitized user input as a variant or attribute value, it's XSS:

```python
# components.py — current pattern (vulnerable if attrs contains user input)
mark_safe(f'<button class="btn btn-{variant} btn-{size}" {attrs_str}>{text}</button>')
```

**Fix**:
1. Replace all `mark_safe(f'...')` in `components.py` with `format_html()` for attribute interpolation
2. Validate `variant` and `size` against an allowlist before rendering (reject unknown values with a warning)
3. Escape all `**attrs` values through `escape()` before HTML attribute injection
4. Add the same treatment to `templatetags/theme_components.py` which has the same pattern
5. This is critical because I1 (move HTML to templates) will eliminate most of this code, but until I1 is complete, the Python-rendered HTML is the active code path and must be secure

### I44: ColorScale Input Validation (Priority: Medium — do with I16)

**Problem**: `ColorScale(h, s, lightness)` accepts raw integers with no bounds validation. `with_lightness(l)` and `with_saturation(s)` create new instances without clamping. A value of `lightness=150` or `saturation=-10` silently produces invalid CSS (`hsl(220, -10%, 150%)`) that browsers interpret unpredictably — Chrome clamps, Safari ignores, Firefox renders differently. The `PaletteGenerator` (I21) will programmatically create `ColorScale` values from arithmetic, making out-of-bounds values likely during derivation.

**Fix**:
1. Add `__post_init__` validation to `ColorScale`: clamp `h` to 0-360, `s` to 0-100, `lightness` to 0-100
2. `with_lightness()` and `with_saturation()` clamp values before creating new instances
3. Add `ColorScale.is_valid() -> bool` for explicit validation in test/debug contexts
4. Log a warning (not error) when clamping occurs — helps theme authors catch palette derivation bugs
5. This is a prerequisite for I21 (auto-palette) since generated values may exceed bounds during complementary/analogous hue calculations

### I45: Graceful CSS Generation Failure (Priority: High — do with I5)

**Problem**: `context_processors.py` calls `CompleteThemeCSSGenerator.generate_css()` and embeds the result in every template context. If CSS generation raises an exception (invalid preset name, corrupted design tokens, missing pack), the entire page render crashes with a 500 error. The user sees a Django error page instead of their app with degraded styling. This is especially dangerous during theme development — a typo in a token override shouldn't take down the whole app.

**Fix**:
1. Wrap CSS generation in `context_processors.py` with try/except that falls back to minimal CSS (just the default preset's tokens)
2. Log the error with full traceback at `ERROR` level
3. When `DEBUG=True`, inject an HTML comment `<!-- djust-theming: CSS generation failed: {error} -->` so theme authors see the issue in View Source
4. Add the same resilience to `views.py` `theme_css_view()` — return a 200 with fallback CSS and a CSS comment explaining the error, rather than a 500
5. The fallback CSS should be pre-generated at startup and cached — never depend on runtime generation for the error fallback itself

### I46: CSS Transition on Theme Switch (Priority: Low — do with Phase 2)

**Problem**: When switching presets or toggling light/dark mode, `theme.js` either (a) swaps CSS variables instantly (mode toggle) or (b) triggers a full page reload (preset switch). The instant swap is jarring — all colors change simultaneously with no transition. The full reload is even worse — white flash, scroll position lost, form state reset. Modern theming systems (macOS appearance, Tailwind dark mode) use a smooth crossfade. djust LiveView's `push_event('theme_update')` avoids reload for mode changes, but preset changes still reload.

**Fix**:
1. Add a CSS transition on the `:root` element for color properties: `transition: background-color 200ms ease, color 200ms ease`
2. For preset switches (which change all tokens), use the View Transitions API (`document.startViewTransition()`) where supported — provides a smooth crossfade of the entire page
3. Fallback for browsers without View Transitions: add a brief `opacity: 0.95` fade on `<body>` during token swap
4. For `theme.js` preset changes: instead of `window.location.reload()`, fetch the new CSS via `theme_css_view()` endpoint and inject it — no reload needed
5. Add `DJUST_THEMING['TRANSITION_DURATION']` setting (default: `200ms`, set to `0` to disable)

### I47: Theme Debugging Overlay (Priority: Low — do with Phase 8)

**Problem**: When a theme doesn't look right, there's no diagnostic tool to understand why. The inspector (Phase 8) provides a general token editor, but doesn't answer the specific questions theme authors have: "Which CSS layer is this rule coming from?", "Is my token override actually being applied or is it shadowed?", "Which template is rendering this component — my override or the default?" These questions require reading browser DevTools and Django debug toolbar, which theme authors (often designers, not backend developers) may not be comfortable with.

**Fix**:
1. Add a `{% theme_debug %}` template tag (only renders when `DEBUG=True`) that injects a floating overlay showing:
   - Active theme name, preset, mode
   - Template resolution path for each visible component (which file was used)
   - Token override chain (default value → theme override → inline override)
   - CSS layer each visible rule belongs to
2. Components rendered via `theme_*` tags include a `data-theme-component` attribute with the component name and resolved template path
3. The overlay is toggleable via keyboard shortcut (`Ctrl+Shift+T`) and remembers its state in localStorage
4. Performance: overlay queries DOM lazily (on open, not on every render)
5. This is Phase 8 territory but should be designed alongside Phase 1 — the `data-theme-component` attributes should be added from the start so the overlay has data to show

### I48: Static URL Resolution in Template Tags (Priority: High — do with I4)

**Problem**: `theme_tags.py:111` hardcodes `/static/djust_theming/css/theme.js` with a manual `?v=2` cache buster. `mixins.py:120` does the same with `?v=3`. This breaks when:
- `STATIC_URL` is set to a CDN (`https://cdn.example.com/static/`)
- `STATIC_URL` has a non-default prefix (`/assets/`)
- `ManifestStaticFilesStorage` is used (adds content hashes, not manual version params)
- WhiteNoise with `CompressedManifestStaticFilesStorage` is active

The result: theme JS fails to load in production for any non-default static file setup. This is currently undetectable (no system check) and manifests as a broken theme switcher with no console error (the script 404s silently via `<script>` tag).

**Fix**:
1. Replace hardcoded paths with `django.templatetags.static.static('djust_theming/css/theme.js')` in both `theme_tags.py` and `mixins.py`
2. Remove manual `?v=N` cache busters — Django's static file storage handles cache invalidation
3. Add system check `djust_theming.W004`: warn if `djust.contrib.staticfiles` not in `INSTALLED_APPS` (static file resolution won't work)
4. This should be done alongside I4 (static asset versioning) since both address the same root cause

---

## New Improvements (Added 2026-03-22, batch 6)

Identified during automated deep-dive into `theme.js` client-side behavior, cross-referencing against CSS-side improvements already planned. Focus: client-side security, resilience, and testing gaps that affect production deployments.

### I57: Cookie Security Hardening (Priority: Critical — do immediately)

**Problem**: `theme.js` sets three cookies (`djust_theme`, `djust_theme_preset`, `djust_theme_pack`) with `SameSite=Lax` but without `HttpOnly` or `Secure` flags. While theme preferences aren't sensitive data themselves, the missing `Secure` flag means cookies are sent over plain HTTP, and the cookie-setting pattern establishes a bad precedent in the codebase. More importantly, if a page has an XSS vulnerability elsewhere, an attacker can read/write theme cookies via `document.cookie` to fingerprint users or test cookie manipulation as a stepping stone.

Additionally, `manager.py` reads cookie values and uses them to select presets/themes without validating against the allowed preset list first. A crafted cookie value like `"><script>alert(1)</script>` would pass through to `ThemeState.preset` and potentially be rendered in template context (e.g., `theme_preset_selector` shows the active preset name).

**Fix**:
1. Add `Secure` flag to all cookie sets in `theme.js` when `window.location.protocol === 'https:'`
2. `manager.py` `get_state()` must validate cookie values against known preset/theme/pack names before using them — reject unknown values and fall back to defaults
3. Template tags that render the active preset name must escape it (covered by I43, but the cookie → state → template path needs explicit testing)
4. Document that `HttpOnly` cannot be set on these cookies since `theme.js` must read them client-side — this is an accepted trade-off, but the validation in step 2 mitigates the risk

### I58: localStorage Graceful Degradation (Priority: High — do with I57)

**Problem**: `theme.js` calls `localStorage.getItem()` and `localStorage.setItem()` in multiple places (mode persistence, FOUC prevention, system preference caching) without try/catch. In Safari private browsing (pre-2022), sandboxed iframes, and some enterprise browser configurations, `localStorage` is disabled and throws a `SecurityError` on access. This crashes the entire theme initialization, leaving the page in an unstyled state with no theme applied. The anti-FOUC script runs early — a crash here means the user sees a white flash followed by broken styling.

**Fix**:
1. Wrap all `localStorage` access in a `safeStorage` helper:
   ```javascript
   const safeStorage = {
       get(key) { try { return localStorage.getItem(key); } catch { return null; } },
       set(key, val) { try { localStorage.setItem(key, val); } catch {} },
       remove(key) { try { localStorage.removeItem(key); } catch {} }
   };
   ```
2. Replace all direct `localStorage.*` calls with `safeStorage.*`
3. When localStorage is unavailable, fall back to cookie-only persistence (already used server-side)
4. Add a `storage: 'localStorage' | 'cookie' | 'memory'` diagnostic to the debug overlay (I47)

### I59: JavaScript Feature Detection & Minimum Browser Spec (Priority: Medium — do with Phase 2)

**Problem**: `theme.js` uses `matchMedia`, `CustomEvent`, `requestAnimationFrame`, `document.documentElement.dataset`, and CSS custom property manipulation without feature detection. While these APIs are well-supported in modern browsers (95%+), the failure mode when they're missing is an unhandled exception that breaks all theme functionality — not graceful degradation. Phase 2 will add `components.js` with dropdown/modal/tab behaviors using `MutationObserver`, `IntersectionObserver`, and potentially `Popover API` — the compat surface grows.

**Fix**:
1. Document minimum browser requirements in README: "Chrome 96+, Firefox 95+, Safari 15.4+, Edge 96+" (matches CSS `@layer` support from I9)
2. `theme.js` initialization checks for required APIs and sets a `window.__djustThemeSupported = true/false` flag
3. When unsupported, skip JS-driven theme switching entirely — CSS `prefers-color-scheme` media query provides a basic light/dark experience without JS
4. `components.js` (Phase 2) uses the same feature gate — interactive components degrade to static HTML when JS features are missing
5. No polyfills — the philosophy is graceful degradation, not backward compatibility

### I60: Client-Side Theme Test Suite (Priority: Medium — do before Phase 2)

**Problem**: Test coverage is Python-only (`test_presets.py`, `test_design_tokens.py`, `test_css_generator.py`). `theme.js` has zero test coverage — no tests for: mode toggle persistence round-trip, FOUC prevention timing, system preference change listener, cookie ↔ localStorage sync, `djust-theme-changed` CustomEvent dispatch, or the anti-FOUC inline script behavior. Phase 2 adds `components.js` with dropdown/modal/tab JS behaviors — without a test harness, JS bugs will ship undetected.

**Fix**:
1. Add `tests/js/` directory with a lightweight test runner (Vitest or plain Node.js test runner — no heavy framework)
2. Unit tests for `theme.js`:
   - Mode toggle: `setMode('dark')` → `localStorage.getItem('mode') === 'dark'` AND cookie set
   - Preset switch: `setPreset('nord')` → `document.documentElement.dataset.themePreset === 'nord'`
   - System preference: mock `matchMedia` change → mode updates
   - FOUC prevention: inline script sets `data-theme-mode` before DOMContentLoaded
   - `safeStorage` fallback (I58): localStorage disabled → falls back to cookies
3. Integration tests: render a component template, verify theme switching updates CSS variables
4. Run in CI alongside Python tests: `make test-js` target in Makefile
5. This must exist before Phase 2's `components.js` work — test-driven JS development

### I61: Content Security Policy (CSP) Compatibility (Priority: Medium — do with I2)

**Problem**: The current system has multiple CSP conflicts:
1. `{% theme_head %}` inlines CSS via `<style>` tags — requires `style-src 'unsafe-inline'`
2. Context processor embeds SVG data URIs in template context — requires `img-src data:`
3. `theme.js` manipulates `element.style` properties — requires `style-src 'unsafe-inline'`
4. The inspector (Phase 8) likely needs `eval()` for live token editing — requires `script-src 'unsafe-eval'`

Apps with strict CSP policies cannot use djust-theming without weakening their CSP. This is a blocker for security-conscious enterprises.

**Fix**:
1. Support nonce-based inline styles: `{% theme_head csp_nonce=request.csp_nonce %}` adds `nonce` attribute to all `<style>` tags
2. Move SVG icons from data URIs to external SVG files in `static/` — eliminates `data:` requirement
3. Document minimum CSP requirements for each feature level:
   - **Basic** (linked CSS only): no special CSP needed
   - **Inline CSS** (default): `style-src 'nonce-{value}'`
   - **Theme switching**: `style-src 'unsafe-inline'` (JS sets inline styles)
   - **Inspector**: additional `script-src 'unsafe-eval'` (development only)
4. Add `DJUST_THEMING['CSP_MODE'] = 'nonce' | 'inline' | 'external'` setting:
   - `'external'`: all CSS via linked files — strictest CSP, extra HTTP request
   - `'nonce'`: inline CSS with nonce — good balance
   - `'inline'`: current behavior — simplest, requires `unsafe-inline`
5. This aligns with I2 (CSS extraction) and I10 (critical CSS) — the CSS delivery pipeline needs to support all three modes

### I62: Focus Styling Standardization (Priority: Low — do with Phase 2)

**Problem**: Focus styles are inconsistent across the 5 existing component templates. `button.html` uses inline `:focus-visible { outline: 2px solid hsl(var(--ring)) }`. `input.html` uses a CSS class `.focus-ring`. `card.html` has no focus styles at all (cards can be interactive via `dj-click`). `design_tokens.py` generates `.focus-ring` utility class with `--ring` token, but components don't consistently use it. When Phase 2 adds 15 new components, this inconsistency will multiply.

**Fix**:
1. Define a single focus pattern in `components.css` (after I2 extraction):
   ```css
   @layer components {
       [data-theme-interactive]:focus-visible {
           outline: 2px solid hsl(var(--ring, 221 83% 53%));
           outline-offset: 2px;
       }
   }
   ```
2. All interactive component templates add `data-theme-interactive` attribute — focus styles apply automatically
3. Theme authors override focus appearance by redefining `--ring` and `--ring-offset` tokens, or by targeting `[data-theme-interactive]:focus-visible` in their theme CSS layer
4. Remove inline `:focus-visible` rules from individual component templates
5. Add focus style check to I27 (component test harness): every interactive component must have `data-theme-interactive` attribute

### I63: Animation Token Consistency (Priority: Low — do with I19)

**Problem**: `design_tokens.py` generates `--duration-fast`, `--duration-normal`, `--duration-slow` tokens, but `base.css` hardcodes animation durations: `pulse: 2s cubic-bezier(...)`, `fade-in: 300ms ease`, etc. These hardcoded values ignore both the design system's `animation_intensity` setting and the `prefers-reduced-motion` token override (I13). A theme author setting `animation_intensity: 0` (no animations) still gets the hardcoded pulse and fade animations.

**Fix**:
1. Replace hardcoded animation durations in `base.css` with token references: `pulse: var(--duration-slow) cubic-bezier(...)`
2. Add `--ease-default`, `--ease-in`, `--ease-out`, `--ease-bounce` tokens to `design_tokens.py` (ties into I19)
3. `@keyframes` definitions stay in `base.css` but `animation` shorthand properties use duration tokens
4. This ensures `prefers-reduced-motion` (I13) collapses ALL animation durations — both token-driven and keyframe-based — to `0ms`

---

## New Improvements (Added 2026-03-22, batch 7)

Identified during automated roadmap review. Focus: theme distribution, design-to-code pipeline, compound component patterns, starter kits, and production observability gaps not covered by I1–I63.

### I64: Starter Theme Kits for Common App Types (Priority: High — do with Phase 5)

**Problem**: After Phase 1–3 ship (template overrides, 20 components, layouts), a theme author can build anything — but the blank canvas is paralyzing. The most common request will be "I'm building a SaaS dashboard / marketing site / documentation site — give me a starting point." Currently, the only starting point is `djust_theme create-theme` which scaffolds an empty directory. There's no opinionated "SaaS dashboard theme" or "docs site theme" that bundles a layout + component overrides + sensible tokens.

**Fix**:
1. Ship 3–4 starter kits as built-in themes that are fully functional out of the box:
   - `saas-dashboard`: Sidebar layout, dense table styling, card-based metrics, muted color palette, compact spacing
   - `marketing`: Centered layout, hero sections, large typography, bold primary colors, generous spacing
   - `docs`: Topbar + sidebar layout, code block styling, breadcrumbs, table of contents component, readable typography
   - `admin`: Topbar + sidebar layout, data-dense tables, form-heavy styling, compact spacing
2. Each kit is a complete theme directory (templates, tokens, CSS overrides) demonstrating best practices
3. `python manage.py djust_theme create-theme my-theme --kit saas-dashboard` scaffolds from a kit instead of empty
4. Kits serve dual purpose: jumpstart for builders AND reference implementations for theme authors learning the system
5. These are distinct from design systems (Material, iOS, etc.) — kits are about *app type*, systems are about *visual style*. A SaaS dashboard can use Material or iOS visual style.

### I65: Compound Component Patterns (Priority: Medium — do with Phase 2)

**Problem**: Phase 2 defines 15 individual components (modal, tabs, table, etc.) but doesn't address compound patterns — components composed of other components. Real apps use patterns like: form groups (label + input + error + help text), card lists (repeating cards in a grid), data tables (table + pagination + filters + bulk actions), dialog flows (modal + form + button group). Theme authors need to override these compositions, not just individual components. Without compound component templates, every app reimplements the same layout-of-components differently, making themes look inconsistent across apps.

**Fix**:
1. Add compound component templates alongside individual components:
   - `form_group.html`: Label + field widget + error + help text — wraps any input component
   - `card_grid.html`: Responsive grid of cards with configurable columns
   - `data_table.html`: Table + pagination + optional search/filter bar
   - `dialog.html`: Modal + form + button group (confirm/cancel pattern)
   - `stat_card.html`: Metric value + label + trend indicator + sparkline slot
   - `nav_section.html`: Nav group with collapsible subsections
2. Compound templates use `{% include %}` to render child components — theme authors can override the compound template, the child components, or both
3. Component contracts document which child components are used, so overriding a child ripples into all compounds
4. Template tags: `{% theme_form_group field label="Name" help="Enter full name" %}`

### I66: Theme Preview Thumbnail Generation (Priority: Medium — do with Phase 8)

**Problem**: Phase 8 describes a gallery view and visual regression testing, but there's no way to generate a static preview image of a theme. This is critical for: (a) the `create-preset` CLI output (show what the palette looks like without launching a browser), (b) theme marketplace listings (Phase 9.3), (c) the preset selector UI (currently text-only, should show color swatches), (d) README/documentation (embed preview images). Without auto-generated previews, theme authors must manually screenshot their themes for distribution.

**Fix**:
1. `python manage.py djust_theme preview my-theme --output preview.png` renders a standardized component showcase to an image
2. Use a headless browser (Playwright, via optional dependency) to render the gallery view (Phase 8.1) and capture a screenshot
3. For environments without a browser (CI), generate an SVG preview from token values alone — a simple grid of color swatches + typography samples + button/card preview, rendered via Python SVG generation (no browser needed)
4. `python manage.py djust_theme preview my-theme --format svg` for the lightweight variant
5. The SVG preview is embedded in `theme.toml` metadata:
   ```toml
   [theme]
   preview = "preview.svg"    # Auto-generated, committed to version control
   ```
6. Preset selector component (Phase 2) renders SVG previews inline for visual theme browsing

### I67: Theme Usage Analytics Hook (Priority: Low — do with Phase 5)

**Problem**: SaaS apps offering theme selection to users have no insight into which themes/presets are popular. The multi-tenant resolver (I32) selects themes per-tenant, but there's no instrumentation for: how many users use each preset, which presets have high bounce rates (suggesting poor quality), whether users switch presets frequently (suggesting dissatisfaction), or which custom presets are created via auto-palette (I21). Without analytics, theme library curation is guesswork.

**Fix**:
1. Add an optional `ThemeAnalytics` hook in `ThemeManager`:
   ```python
   DJUST_THEMING = {
       'ANALYTICS_BACKEND': 'myapp.analytics.ThemeAnalyticsBackend',  # or None to disable
   }
   ```
2. The backend receives events: `theme_selected(preset, mode, source)`, `theme_switched(from_preset, to_preset)`, `preset_created(name, source_color)`
3. Default backend: no-op (zero overhead when disabled)
4. Ship a `DjangoORMAnalyticsBackend` that stores events in a simple model — one migration, queryable via Django admin
5. This is opt-in and adds zero overhead when disabled. Privacy-conscious: only records theme choices, not user identity (unless the backend implementation adds it)

### I68: Theme Migration Assistant (Priority: Medium — do with Phase 5)

**Problem**: I42 describes version compatibility declarations in `theme.toml`, but doesn't address the actual migration path. When djust-theming v2.0 changes component contracts (adds required slots, renames tokens, changes CSS class patterns), every custom theme needs updating. Without migration tooling, theme authors face a wall of deprecation warnings and must manually diff their templates against the new defaults. This is the #1 cause of ecosystem fragmentation in theming systems (WordPress theme ecosystem is a cautionary tale).

**Fix**:
1. `python manage.py djust_theme migrate my-theme --to 2.0` performs automated migration:
   - Renames deprecated token names in `tokens.css` (e.g., `--radius` → `--border-radius`)
   - Updates CSS class names in overridden templates (per I17 prefix changes)
   - Adds missing required slots to overridden component templates (by diffing against the new base template and inserting `{% block new_slot %}{% endblock %}`)
   - Updates `theme.toml` schema (new required fields, deprecated options)
2. Generates a migration report: what was auto-fixed, what needs manual attention
3. `--dry-run` mode previews changes without writing
4. djust-theming ships `MIGRATIONS.md` per version documenting all breaking changes and the automated fixes available
5. The migration tooling reads from `theme.toml`'s `[requires]` section to know which version the theme was built for

### I69: CSS Scope for Partial Theme Application (Priority: Low — do after I18)

**Problem**: I18 (container-scoped theming) allows different presets in different DOM subtrees. But it uses `data-theme-scope` attributes which only scope CSS custom property values — the component CSS rules (`.btn`, `.card`, etc.) remain global. In a page that mixes djust-theming components with non-themed content (e.g., embedding themed widgets in an existing Bootstrap app), the global component CSS bleeds out. CSS `@scope` (baseline 2024, ~80% support) provides true CSS containment.

**Fix**:
1. Add a `{% theme_scope %}...{% endtheme_scope %}` block tag that wraps content in a `<div data-theme-scope>` and generates scoped CSS:
   ```css
   @scope ([data-theme-scope]) {
       .btn { /* only applies inside scope */ }
       .card { /* only applies inside scope */ }
   }
   ```
2. The `scope` CSS delivery mode generates all component CSS inside `@scope` blocks
3. Setting: `DJUST_THEMING['CSS_SCOPE'] = True` (default: `False` — global CSS for full-page themes)
4. When combined with I17 (namespace prefix), this provides belt-and-suspenders isolation for embedding scenarios
5. Fallback for browsers without `@scope`: the I17 prefix alone prevents class name collisions, though specificity scoping is lost

### I70: Figma Plugin for Token Sync (Priority: Low — do after Phase 9)

**Problem**: I30 (W3C token import) and I55 (Tokens Studio import) support one-time import from design tools. But the designer-developer workflow is iterative — designers tweak tokens in Figma, developers pull changes, designers see the result, repeat. Without bidirectional sync, every iteration requires a manual export-import cycle. Figma plugins for design systems (like Tokens Studio) have shown this workflow is the gold standard — but they require a Figma plugin, not just CLI tools.

**Fix**:
1. Publish a Figma plugin: "djust Theme Sync"
2. Plugin reads `theme.toml` + `tokens.css` from a connected git repo (via GitHub/GitLab API) and populates Figma variables
3. Designer edits Figma variables → plugin exports as W3C JSON → opens a PR with updated `tokens.json`
4. Developer runs `djust_theme import-tokens tokens.json` to update the theme
5. **Simpler MVP**: A Figma-compatible REST endpoint in `djust_theming` that serves current tokens as JSON. The Figma plugin polls this endpoint and syncs variables. No git integration needed for v1.
6. This is a post-Phase-9 "ecosystem" item — the core theming system must be stable before investing in tooling integrations

---

## New Improvements (Added 2026-03-22, batch 8)

Identified during automated roadmap review. Focus: modern CSS capabilities that unlock smoother theming, theme portability, developer tooling for token authoring, and content fixtures for theme development.

### I71: CSS @property for Type-Safe Animated Token Transitions (Priority: High — do with I46 + I19)

**Problem**: I46 proposes smooth theme switching via CSS transitions on `:root` color properties. But CSS custom properties (`--primary: 221 83% 53%`) are strings — browsers can't interpolate between them. `transition: --primary 200ms ease` is a no-op because the browser doesn't know `--primary` is a color. The View Transitions API (I46) provides a crossfade workaround, but it's a whole-page effect — it can't animate individual token values smoothly (e.g., a button's background transitioning from blue to green when switching presets).

CSS `@property` (baseline 2024, 93%+ support) registers custom properties with types, enabling native interpolation:

```css
@property --primary-h { syntax: '<number>'; inherits: true; initial-value: 221; }
@property --primary-s { syntax: '<percentage>'; inherits: true; initial-value: 83%; }
@property --primary-l { syntax: '<percentage>'; inherits: true; initial-value: 53%; }
```

With registered properties, `transition: --primary-h 200ms, --primary-s 200ms, --primary-l 200ms` actually works — the browser smoothly interpolates each channel.

**Fix**:
1. `css_generator.py` emits `@property` declarations for all color tokens, decomposed into H/S/L channels (or L/C/H for OKLCH when I49 is active)
2. Component CSS references the composed value: `background: hsl(var(--primary-h) var(--primary-s) var(--primary-l))`
3. A single CSS rule enables smooth preset switching: `* { transition: --primary-h 200ms, --primary-s 200ms, --primary-l 200ms; }` (only on `:root` to avoid layout thrashing)
4. Add `DJUST_THEMING['ANIMATE_TOKENS'] = True` setting (default: `False` — opt-in since it adds ~2KB of `@property` declarations)
5. When combined with I46 (no-reload preset switch), this produces a smooth per-token color animation instead of a jarring instant swap — the visual quality difference is dramatic
6. Non-color tokens (spacing, radius, typography) are NOT animated — only color channels benefit from interpolation

**Why this matters**: Smooth theme transitions are the single most visible "polish" feature. Users notice jarring color swaps. This is what separates a professional theming system from a CSS variable swap.

### I72: CSS Subgrid for Layout Components (Priority: Medium — do with Phase 3)

**Problem**: Phase 3 defines layout templates (sidebar, topbar, dashboard) and Phase 2 adds compound components like card grids and data tables. These layouts use CSS Grid for overall page structure. But child components (cards in a grid, cells in a table, form labels in a horizontal form) need to align to the parent grid's tracks. Without `subgrid`, each card must independently define its own grid — leading to misaligned baselines, inconsistent gutters, and manual `min-height` hacks to keep cards the same height.

CSS `subgrid` (baseline 2023, 93%+ support) solves this: a child grid can inherit track sizing from its parent.

**Fix**:
1. Layout templates use `display: grid; grid-template-columns: subgrid` on content regions where alignment matters
2. `card_grid.html` (I65 compound component) uses subgrid so all cards align:
   ```css
   .card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); }
   .card-grid > .card { display: grid; grid-template-rows: subgrid; grid-row: span 3; }
   ```
   This makes card header, body, and footer rows align across all cards in a row — a common design requirement
3. `form_group.html` (I65) uses subgrid for horizontal form label alignment:
   ```css
   .form-horizontal { display: grid; grid-template-columns: var(--form-label-width, 8rem) 1fr; }
   .form-group { display: grid; grid-template-columns: subgrid; grid-column: span 2; }
   ```
4. Add `--grid-gap` and `--grid-columns` tokens to `design_tokens.py` — theme authors control grid behavior via tokens
5. Fallback for the ~7% without subgrid: flexbox with `min-height` (functional but less aligned)

### I73: Theme Selection via URL Parameter (Priority: Medium — do with Phase 1)

**Problem**: There's no way to share a URL that forces a specific theme/preset. Use cases: (a) marketing site linking to themed demos (`/demo?theme=material&preset=nord`), (b) theme authors sharing preview links, (c) A/B testing with URL-based bucketing, (d) djustlive embedding customer previews in iframes with preset URL params. Currently, theme state is session/cookie-bound — sharing a URL doesn't share the theme.

**Fix**:
1. `ThemeManager.get_state()` checks URL query parameters first (highest priority):
   - `?djust_theme=material` — sets design system
   - `?djust_preset=nord` — sets color preset
   - `?djust_mode=dark` — sets mode
2. URL params are validated against known values (reuse I57's validation)
3. URL params are ephemeral — they don't persist to cookie/session unless `?djust_persist=true` is also set
4. `theme.js` reads URL params on init and applies them before FOUC prevention runs
5. Add `{% theme_url preset="nord" mode="dark" %}` template tag that generates a URL preserving current path with theme params appended
6. Security: URL params only accept known preset/theme names (I57 validation), preventing injection via crafted URLs

This is high-value for the marketing/demo use case and costs almost nothing to implement since `ThemeManager` already has a layered resolution strategy.

### I74: Sample Content Fixtures for Theme Development (Priority: Medium — do with Phase 8)

**Problem**: Phase 8 describes a theme gallery that renders every component in every variant. But components rendered with placeholder text ("Button", "Card Title", "Alert message") don't reveal real-world styling issues: long text overflow, mixed content (text + images + badges), empty states, error states, loading states. Theme authors need realistic content to see how their theme handles edge cases. Currently there's no fixture system — the gallery will render toy examples that don't surface layout bugs.

**Fix**:
1. Add `djust_theming/fixtures/` directory with JSON fixture sets:
   - `default.json` — Standard English content, medium-length strings, representative data
   - `stress.json` — Long strings, many items, deeply nested content, Unicode edge cases
   - `minimal.json` — Single character labels, empty optionals, minimum viable content
   - `rtl.json` — Arabic/Hebrew content for RTL testing (Phase 7)
   - `cjk.json` — Chinese/Japanese content for font/typography testing (I56)
2. Gallery view (Phase 8.1) loads a fixture set and renders all components with that data
3. `python manage.py djust_theme preview my-theme --fixture stress` renders with stress-test content
4. Theme authors can add custom fixtures in their theme directory: `themes/my-theme/fixtures/custom.json`
5. The `validate` command (Phase 1.5) renders each overridden component with all fixture sets and checks for: text overflow, missing elements, broken layout (elements overflowing parent)

### I75: Theme Export as Standalone CSS (Priority: Medium — do after Phase 1)

**Problem**: djust-theming generates CSS dynamically via Python. This works perfectly inside Django but makes the theming system unusable outside Django: static site generators, non-Django backends, vanilla HTML prototypes, Storybook instances, Figma plugin previews. The tokens and component CSS are excellent — but locked inside a Django runtime. Making themes exportable as standalone CSS files dramatically increases the system's reach and utility.

**Fix**:
1. `python manage.py djust_theme export my-theme --output ./dist/` generates:
   ```
   dist/
   ├── tokens.css          # All CSS custom properties (light + dark)
   ├── base.css            # Reset, typography, utilities
   ├── components.css      # All component styles
   ├── layouts.css         # Layout styles (if applicable)
   ├── theme-overrides.css # Theme-specific overrides
   ├── theme.css           # Single bundled file (all above concatenated)
   └── theme.min.css       # Minified bundle
   ```
2. Exported CSS is self-contained — no Django template tags, no Python runtime needed
3. Component HTML contracts are documented alongside: `dist/contracts.json` lists required HTML structure per component
4. This enables: prototyping themes in CodePen/JSFiddle, using themes in non-Django projects, sharing themes with front-end developers who don't use Django
5. The export respects all CSS architecture decisions: `@layer` ordering (I9), namespace prefix (I17), cascade layers, `light-dark()` (I50)
6. `--watch` flag re-exports on file change for iterative development outside Django

### I76: Token Autocomplete Schema for Editors (Priority: Low — do with I37)

**Problem**: I37 (token reference documentation) generates token lists for CLI and gallery. But the primary place theme authors write token overrides is their code editor (VS Code, JetBrains, etc.). Without autocomplete, they type `var(--prm` and get no suggestions — they must switch to the CLI or gallery to look up token names, then switch back. This context-switching breaks flow. Modern editors support CSS custom property autocomplete via JSON schema or `.css` reference files.

**Fix**:
1. `python manage.py djust_theme tokens --format vscode` generates `.vscode/css-custom-data.json`:
   ```json
   {
     "version": 1.1,
     "properties": [],
     "atDirectives": [],
     "pseudoClasses": [],
     "pseudoElements": [],
     "cssCustomProperties": [
       { "name": "--primary", "description": "Primary brand color", "syntax": "<color>" },
       { "name": "--space-4", "description": "Standard spacing unit (1rem)", "syntax": "<length>" }
     ]
   }
   ```
2. VS Code recognizes this file automatically and provides autocomplete + hover documentation for all theme tokens
3. `--format jetbrains` generates `web-types.json` for JetBrains IDEs
4. The scaffold command (Phase 1.3) auto-generates the editor config for the active theme
5. Token descriptions flow from the same `TOKEN_DOCS` source as I37 — single source of truth

### I77: Theme Inheritance Chain Visualization (Priority: Low — do with I22)

**Problem**: When themes compose (I14) or extend (Phase 1.2), the resolution chain for any given template or token becomes non-obvious. A button template might come from the active theme, fall back to its base theme, and ultimately resolve to the default. A token might be overridden at the theme level, inherited from the design system, or computed from the preset. When styling doesn't look right, theme authors need to understand the resolution chain — "where is this value actually coming from?"

**Fix**:
1. `python manage.py djust_theme resolve my-theme --component button` shows the full resolution chain:
   ```
   Component: button
   Template: themes/my-theme/components/button.html  (overridden)
     ↳ extends: djust_theming/components/button.html  (default)
     ↳ slots overridden: icon, loading
     ↳ slots inherited: content

   Token: --primary
     ↳ Value: 221 83% 53%
     ↳ Source: themes/my-theme/tokens.css (theme override)
     ↳ Base value: 210 40% 98% (default preset)
   ```
2. `--all` flag shows resolution for every component and token — the complete theme "exploded view"
3. The debug overlay (I47) shows this per-component in the browser when hovering over a component
4. This is the "X-ray mode" for themes — essential for debugging complex inheritance chains

---

## New Improvements (Added 2026-03-22, batch 9)

Identified during automated roadmap review. Focus: closing the gap between "CSS variable theming" and "full template-driven customization", improving the theme authoring inner loop, and enabling themes to work beyond Django HTML.

### I78: Ejectable Component Pattern — Copy-to-Project Workflow (Priority: High — do with Phase 1)

**Problem**: The current override system (Phase 1.1) uses Django template inheritance — theme authors extend base templates and override blocks. This works for slot-level changes (I11) but fails when a theme author needs to radically restructure a component. Extending `button.html` and overriding every block is worse than writing a new `button.html` from scratch. The shadcn/ui model ("eject" a component into your project, own it completely) is extremely popular precisely because it gives full control without fighting an inheritance chain.

**Fix**:
1. `python manage.py djust_theme eject button --theme my-theme` copies the default `button.html` + `button.css` into the theme directory as a standalone override:
   ```
   themes/my-theme/components/button.html     # Full copy, not extending base
   themes/my-theme/css/components/button.css   # Extracted component CSS
   ```
2. The ejected template includes a comment header documenting the component contract (required context variables, accessibility requirements, CSS class expectations) so the author knows the rules
3. Ejected components are marked in `theme.toml` automatically:
   ```toml
   [ejected]
   components = ["button", "card"]   # These are fully owned, not inherited
   ```
4. The `validate` command (Phase 1.5) applies different checks to ejected vs. inherited components:
   - Inherited: checks that overridden blocks still satisfy contracts
   - Ejected: checks the full HTML output satisfies the contract (required elements, ARIA attributes, CSS classes)
5. `djust_theme migrate` (I68) warns about ejected components when the base template changes — the author must manually reconcile
6. The `eject` command supports `--all` to eject every component (for themes that want total control) and `--diff` to show what changed in the base since ejection

**Why this matters**: Phase 1's inheritance model and I11's slot system handle 80% of customizations elegantly. But the remaining 20% — where the HTML structure must be fundamentally different — need an escape hatch. Without eject, theme authors fork the entire template repository. Eject provides controlled divergence with contract enforcement.

### I79: Theme Token API for Headless Frontends (Priority: Medium — do after Phase 1)

**Problem**: djust-theming generates CSS and HTML templates for Django server-rendered pages. But modern apps increasingly use Django as an API backend with React/Vue/Svelte frontends. These frontends need the theme's design tokens (colors, spacing, typography) in a format they can consume — CSS custom properties work for vanilla HTML but don't integrate with CSS-in-JS, Tailwind config, or native mobile design systems. I75 (standalone CSS export) partially addresses this but requires a build step. A runtime API endpoint serving tokens as JSON enables real-time theme switching in JS frontends.

**Fix**:
1. Add `/api/theme/tokens/` endpoint returning the active theme's tokens as JSON:
   ```json
   {
     "preset": "nord",
     "mode": "dark",
     "tokens": {
       "colors": { "primary": {"hsl": "220 83% 53%", "hex": "#1E40AF", "rgb": "30 64 175"} },
       "spacing": { "4": "1rem", "8": "2rem" },
       "typography": { "font-size-base": "1rem", "font-family-body": "'Inter', sans-serif" }
     }
   }
   ```
2. Support `?preset=nord&mode=dark` query params for specific configurations
3. Add `?format=tailwind` to output a Tailwind `theme.extend` object directly consumable by Tailwind CSS config
4. Add `?format=css-vars` to output just the CSS custom property declarations (like I75 but without the full file structure)
5. ETag and Cache-Control headers per theme state (reuse I28 state hash)
6. Setting: `DJUST_THEMING['ENABLE_API'] = True` (default: `False` — opt-in to avoid exposing an endpoint)

This bridges server-rendered Django apps with JS-heavy frontends. A React dashboard can fetch theme tokens from Django and apply them via CSS variables or CSS-in-JS, keeping the single source of truth in djust-theming.

### I80: Template Fragment Library — Reusable Micro-Templates (Priority: Medium — do with Phase 2)

**Problem**: Django template `{% block %}` tags work for component-level slots (I11) but are too coarse for micro-patterns that appear across multiple components. Examples: icon rendering (SVG inline vs. icon font vs. image — same choice everywhere), loading spinner (used in buttons, cards, tables, modals), empty state message (used in tables, lists, card grids), status indicator dot (used in badges, nav items, user avatars). Currently each component template implements these micro-patterns independently. When a theme author wants all icons to use a custom icon library, they must override every component that renders icons.

**Fix**:
1. Add `djust_theming/templates/djust_theming/fragments/` directory with micro-templates:
   - `icon.html` — Renders an icon from name. Default: inline SVG. Theme override: swap to icon font, image, or custom SVG sprite
   - `spinner.html` — Loading indicator. Default: CSS spinner. Theme override: custom animation, skeleton, dots
   - `empty.html` — Empty state with message + optional CTA. Default: centered text. Theme override: illustration + styled message
   - `status_dot.html` — Colored dot indicator. Default: CSS circle. Theme override: shape, animation, size
   - `close_button.html` — Dismiss/close control. Default: × character. Theme override: SVG icon, styled button
2. Component templates use `{% include "djust_theming/fragments/icon.html" with name=icon %}` instead of inline SVG
3. Theme resolution applies to fragments just like components — `themes/my-theme/fragments/icon.html` overrides the default
4. Overriding one fragment changes the micro-pattern everywhere — override `icon.html` once, all icons across all components use the new rendering
5. Fragment contracts are minimal: receive a few context variables, output a single HTML element

This is the "Don't Repeat Yourself" principle applied to templates. It multiplies the value of theme overrides — one fragment change propagates to every component that uses it.

### I81: Accessibility Tree Validation for Theme Overrides (Priority: Medium — do with I27)

**Problem**: I52 covers color blindness simulation and I6 covers contrast validation. But a theme override can break accessibility in ways that aren't color-related: removing `role` attributes, dropping `aria-label` text, breaking focus order, nesting interactive elements (button inside button), or omitting required landmark regions. The `validate` command (Phase 1.5) checks for required HTML elements but doesn't verify the accessibility tree structure. WCAG compliance requires correct ARIA semantics, not just correct visual appearance.

**Fix**:
1. Extend I27 (component test harness) with accessibility tree assertions:
   - Every interactive component must have a `role` or use a semantic element (`<button>`, `<a>`, `<input>`)
   - Components with visible text must have matching `aria-label` or use the text as the accessible name
   - Modal/dialog components must have `aria-modal="true"` and trap focus
   - Tab components must use `role="tablist"`, `role="tab"`, `role="tabpanel"` with correct `aria-selected` / `aria-controls` linkage
   - Forms must have `<label>` associated via `for` attribute or wrapping
2. Define accessibility contracts per component alongside HTML contracts (Phase 2.2):
   ```python
   COMPONENT_A11Y_CONTRACTS = {
       'button': {'roles': ['button'], 'required_attrs': ['aria-disabled|disabled']},
       'modal': {'roles': ['dialog'], 'required_attrs': ['aria-modal', 'aria-labelledby']},
       'tabs': {'roles': ['tablist', 'tab', 'tabpanel'], 'required_attrs': ['aria-selected']},
   }
   ```
3. `validate --a11y` renders each overridden component and parses the HTML to verify accessibility contracts
4. Report format: "Theme 'my-theme' button.html: missing role='button' on interactive element (found <div> without role)" — actionable, specific
5. This catches the most common accessibility regression: theme authors using `<div>` with `onclick` instead of `<button>`, or dropping ARIA attributes to simplify their override

### I82: Email-Compatible Theme Export (Priority: Low — do after Phase 4)

**Problem**: Many Django apps send transactional emails (welcome, password reset, invoices) that should match the app's visual theme. Email HTML has severe CSS constraints: no custom properties, no `@layer`, no `@media` in many clients, inline styles required. djust-theming's token-based approach is the opposite of what email needs. Theme authors who invest in a custom theme still send generic unstyled emails. There's no path from "I have a djust theme" to "my emails match my theme."

**Fix**:
1. `python manage.py djust_theme export-email my-theme --output templates/email/` generates email-compatible templates:
   - Token values resolved to concrete CSS values (no `var()` references)
   - All styles inlined via a lightweight CSS inliner (no external dependency — use simple regex-based inliner for the limited CSS subset)
   - Responsive via `@media` only (no container queries)
   - Dark mode via `@media (prefers-color-scheme: dark)` (supported by Apple Mail, Gmail, Outlook 365)
2. Email templates use the same color tokens but resolved to hex values: `background-color: #1E40AF` instead of `background-color: hsl(var(--primary))`
3. Export includes: `email_base.html` (layout), `email_button.html` (CTA button), `email_card.html` (content card), `email_footer.html` (unsubscribe/legal)
4. These are Django templates, not standalone HTML — they use `{% block %}` for content injection
5. Pair with I66 (preview thumbnails): `djust_theme preview my-theme --format email` shows how email templates look in popular clients (via HTML preview, not actual email send)

### I83: Theme Conflict Detection for Multi-App Projects (Priority: Low — do with Phase 5)

**Problem**: Django projects often include multiple third-party apps, each potentially bundling their own djust-theming components or CSS. When two apps override the same component template (e.g., both provide a custom `button.html`), Django's template resolution picks one silently based on `INSTALLED_APPS` order. The "losing" app's template is invisible — no warning, no diagnostic. With pip-installable theme packages (Phase 5.2), this becomes a real issue: `djust-theme-material` and `djust-theme-ios` both override `button.html`, and the user installs both.

**Fix**:
1. `ThemeRegistry` (Phase 1.4) tracks which package provides each template override
2. System check `djust_theming.W005`: warn when multiple installed themes override the same component template
3. `python manage.py djust_theme conflicts` lists all template collisions:
   ```
   Component: button.html
     Override 1: djust-theme-material (installed via pip)
     Override 2: themes/my-theme/ (local project)
     Active: themes/my-theme/ (wins by INSTALLED_APPS order)
   ```
4. `theme.toml` can declare explicit conflict resolution:
   ```toml
   [overrides.priority]
   button = "local"      # Use local override, ignore package overrides
   modal = "material"    # Use material package's modal
   ```
5. This is essential for an ecosystem with installable theme packages — without conflict detection, the "install two themes" experience is confusing and fragile

## New Improvements (Added 2026-03-22, batch 4)

Identified during a strategic review focused on real-world adoption friction, ecosystem integration, and architectural gaps that become expensive to fix later.

### I84: Zero-Config INSTALLED_APPS Experience (Priority: High — do with I23)

**Problem**: Getting started requires 3 separate configuration steps beyond `INSTALLED_APPS`: adding the context processor, including URL patterns, and optionally configuring `LIVEVIEW_CONFIG`. Competing systems (Tailwind, Bootstrap) work immediately after install. The current setup creates a "configuration cliff" where the first 5 minutes of adoption are spent on boilerplate rather than seeing results.

**Fix**:
1. `AppConfig.ready()` (I23) auto-registers the context processor if not present via `django.template.engines['django'].engine.context_processors.append()` — same pattern Django's `SecurityMiddleware` uses for auto-detection
2. Make URL inclusion optional: when `djust_theming.urls` is not in `urlpatterns`, serve CSS inline (already the default mode). The URL route is only needed for linked CSS delivery. Remove `W001` check — make it a `DEBUG`-level note instead
3. Add a `{% load theme_tags %}` → `{% theme_head %}` quick-start path that works with ZERO configuration beyond `INSTALLED_APPS`:
```python
# settings.py — this alone should work
INSTALLED_APPS = [
    ...
    'djust_theming',
]
```
4. All other settings (`LIVEVIEW_CONFIG['theme']`, `DJUST_THEMING`, etc.) become opt-in refinements, not prerequisites

### I85: Dark Mode Image Handling (Priority: Medium — do with Phase 2)

**Problem**: Theme switching changes colors but ignores images. A company logo on a white background disappears when switching to dark mode. Illustrations with light-colored elements become invisible. Charts and diagrams need dark-mode variants. There's no mechanism for theme-aware image rendering in component templates or layouts.

**Fix**:
1. Add `theme_picture` template tag that wraps `<picture>` with theme-mode-aware `<source>` elements:
```html
{% theme_picture "logo.png" dark="logo-dark.png" alt="Company Logo" %}
{# Renders: #}
<picture>
    <source srcset="logo-dark.png" media="(prefers-color-scheme: dark)">
    <img src="logo.png" alt="Company Logo">
</picture>
```
2. For images without dark variants, add CSS filter tokens:
```css
[data-theme-mode="dark"] img:not([data-theme-exempt]) {
    filter: brightness(var(--img-brightness, 0.9)) contrast(var(--img-contrast, 1.1));
}
```
3. Add `[images]` section to `theme.toml` for theme-specific image overrides:
```toml
[images]
logo = { light = "logo.svg", dark = "logo-white.svg" }
favicon = { light = "favicon.ico", dark = "favicon-dark.ico" }
```
4. `{% theme_head %}` emits `<link rel="icon">` with media queries for dark-mode favicon if configured

### I86: Theme-Aware Meta Tags and PWA Manifest (Priority: Medium — do with Phase 3)

**Problem**: The `theme-color` meta tag, PWA `manifest.json` colors, and `apple-mobile-web-app-status-bar-style` are hardcoded per-project. When a user switches themes, the browser chrome (status bar, tab color) doesn't update. Multi-tenant apps need different `theme-color` per tenant. PWA manifest `background_color` and `theme_color` don't reflect the active theme.

**Fix**:
1. `{% theme_head %}` emits `<meta name="theme-color">` derived from the active preset's `--primary` token, with `media` attribute for light/dark:
```html
<meta name="theme-color" content="#1E40AF" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#3B82F6" media="(prefers-color-scheme: dark)">
```
2. Add a `theme_manifest` view that serves dynamic `manifest.json` with colors from the active preset
3. Client-side JS updates `theme-color` meta tag when preset changes (already manages `data-theme-*` attributes — add `meta[name=theme-color]` update)
4. Theme authors can override in `theme.toml`:
```toml
[meta]
theme_color = { light = "#1E40AF", dark = "#3B82F6" }
status_bar_style = "default"  # "default", "black", "black-translucent"
```

### I87: djust-components Integration Strategy (Priority: High — do before Phase 2)

**Problem**: The `djust-components` package already provides 31 components (buttons, modals, cards, etc.) with their own CSS and template system. `djust-theming` plans to build 20 components in Phase 2 that overlap significantly. Without a clear integration strategy, users face a confusing choice: "Do I use `{% theme_button %}` or `{% dj_button %}`?" Two component libraries competing for the same DOM elements is a recipe for CSS conflicts and developer confusion.

**Fix**: Choose one of these strategies and commit before Phase 2:

**Option A: djust-theming wraps djust-components** (recommended)
- Phase 2 components are thin wrappers that delegate to `djust-components` for HTML structure
- `djust-theming` provides the CSS token layer; `djust-components` provides the HTML/JS layer
- Theme overrides work via `djust-components`' existing template system
- `{% theme_button %}` resolves to `{% dj_button %}` with theme CSS classes injected
- Avoids duplicate code and leverages the 31 already-built components

**Option B: djust-theming replaces djust-components**
- Phase 2 builds all components from scratch within djust-theming
- djust-components becomes deprecated or optional
- More work but cleaner architecture (no cross-package dependency)

**Option C: Shared component contract with independent implementations**
- Define a component contract (context variables, accessibility requirements) shared by both
- Each package implements independently but template overrides from one work in the other
- Most flexible but highest maintenance burden

Document the chosen strategy in this roadmap. The decision affects Phase 2's entire scope, timeline, and test strategy.

### I88: Theme Switching Without djust LiveView (Priority: High — do with Phase 1)

**Problem**: Live theme switching (no page reload) currently requires djust LiveView (`ThemeMixin` with WebSocket event handlers). Plain Django apps using `djust-theming` without the core `djust` framework can only switch themes via full page reload (form POST or JavaScript cookie + reload). This is a significant adoption barrier — teams evaluate djust-theming independently before committing to the full djust framework.

**Fix**:
1. Enhance `theme.js` to handle preset switching entirely client-side:
   - Store preset CSS as `data-theme-preset-css` attribute on `<style>` element (already present when using inline CSS mode)
   - On preset change: fetch new CSS from `theme_css_view` endpoint via `fetch()`, swap `<style>` content, update `data-theme-preset` attribute
   - Cookie update triggers server-side session sync on next request
2. Add `{% theme_switcher mode="client" %}` that renders a switcher using vanilla JS only (no `dj-click` directives)
3. When djust is detected (`window.djust` exists), automatically upgrade to WebSocket-based switching for seamless VDOM integration
4. This makes `djust-theming` fully functional as a standalone Django package:
```python
# No djust dependency needed for basic theming
INSTALLED_APPS = ['djust_theming']
# Theme switching works via client-side JS
```

### I89: Tailwind v4 CSS-First Configuration (Priority: Medium — do with I30)

**Problem**: The current Tailwind integration (`tailwind.py`, `djust_theme tailwind-config` CLI command) generates `tailwind.config.js` — the v3 configuration format. Tailwind v4 (released January 2025) uses CSS-first configuration via `@theme` and `@import` directives. The v3 config approach is deprecated and will eventually be removed. Theme authors using Tailwind v4 have no integration path.

**Fix**:
1. Add Tailwind v4 CSS export:
```bash
python manage.py djust_theme tailwind-config --version 4
# Outputs CSS instead of JS:
```
```css
@import "tailwindcss";
@theme {
    --color-primary: hsl(var(--primary));
    --color-secondary: hsl(var(--secondary));
    --color-background: hsl(var(--background));
    /* ... all tokens mapped to Tailwind v4 theme keys */
}
```
2. Detect Tailwind version from project (check for `@config` in CSS vs. `tailwind.config.js`) and output the appropriate format
3. Keep v3 export as default until v4 adoption exceeds 50% (track via npm download stats)
4. Add `--format` flag: `--format v3` (JS config), `--format v4` (CSS `@theme`), `--format both`

### I90: Component State Persistence Across Re-renders (Priority: Medium — do with Phase 2)

**Problem**: Interactive components (tabs, accordions, modals, dropdowns) have UI state (which tab is active, whether modal is open). In djust LiveView, a server-side re-render replaces DOM content, potentially resetting component state. The DOM morphing in djust preserves element identity, but component JS state (stored in closures or variables) is lost. Phase 2 adds 15 new interactive components — without a state persistence strategy, every re-render resets open dropdowns, active tabs, and scroll positions.

**Fix**:
1. `components.js` (Phase 2.3) stores interactive state in `data-theme-state` attributes on the component root element:
```html
<div data-theme-tabs data-theme-state='{"active":"tab2"}'>
```
2. After DOM morph, `components.js` reads `data-theme-state` to restore state. djust's morph algorithm already preserves attributes on matched elements.
3. For djust LiveView: register state with the server via `dj-model` so state survives full re-renders:
```html
<div data-theme-tabs dj-model="active_tab">
```
4. For plain Django: state is client-side only (data attributes + localStorage fallback)
5. Document the state persistence contract: theme authors using `components.js` data-attribute hooks get persistence for free; custom JS implementations must handle it themselves

### I91: Theme Versioning and Compatibility Matrix (Priority: Medium — do with Phase 5)

**Problem**: When djust-theming adds new component contracts (Phase 2), changes token names, or modifies slot definitions, installed themes may break silently. There's no mechanism to declare "this theme was built for djust-theming 1.x" or to detect incompatibility at startup. Theme authors have no way to specify which version of the theming system their theme targets, and users have no warning when updating djust-theming might break their active theme.

**Fix**:
1. Add `requires` field to `theme.toml`:
```toml
[theme]
name = "my-theme"
requires = ">=1.2,<2.0"    # semver range of djust-theming versions
```
2. System check `djust_theming.E004`: error when installed theme's `requires` range doesn't include current djust-theming version
3. `python manage.py djust_theme compat my-theme` reports:
   - Which components the theme overrides that have changed since the theme's target version
   - New required slots/context variables the theme's templates don't handle
   - Deprecated tokens the theme still uses
4. `CHANGELOG.md` (already exists) gets structured machine-readable sections per version listing contract changes
5. `djust_theme migrate my-theme --to 2.0` (I68) uses the compat report to auto-fix what it can

---

## Priority Rebalancing Notes (2026-03-22)

**Items to elevate:**
- **I84 (Zero-config)**: Currently not in the roadmap. Should be Tier 1 — adoption friction is the biggest threat to the theming system's success. If getting started takes more than 2 minutes, teams won't evaluate it.
- **I87 (djust-components integration)**: A blocking architectural decision that must be resolved before Phase 2 begins. Without it, Phase 2 risks building 15 components that duplicate existing work.
- **I88 (Theme switching without djust)**: Critical for standalone adoption. djust-theming should be a fully functional Django package that becomes *enhanced* by djust, not *dependent* on it.

**Items to potentially defer:**
- **I49 (OKLCH)**: Marked High but adds significant complexity for v1.x. Consider: build I21 (auto-palette) in HSL first, add OKLCH as an option in v2.0. HSL palettes are "good enough" for most use cases and the HSL→OKLCH migration path is straightforward since both are just different representations of color.
- **I70 (Figma plugin)**: Requires Figma API expertise and ongoing maintenance. Consider partnering with an existing Figma-to-tokens tool rather than building a plugin from scratch.
- **I14 (Theme composition)**: Architecturally complex with limited real-world demand. Single-theme selection covers 95% of use cases. Defer to v3.0.

**Missing from execution order table:**
- I84, I85, I86, I87, I88, I89, I90, I91 need to be integrated into the tier table. Suggested placement:
  - Tier 1: I84 (zero-config), I87 (djust-components strategy), I88 (standalone switching)
  - Tier 2: I85 (dark images), I86 (meta/PWA), I90 (state persistence)
  - Tier 3: I89 (Tailwind v4), I91 (versioning)

---

## New Improvements (Added 2026-03-22, batch 10)

Identified during automated roadmap review. Focus: production-scale multi-tenant performance, modern CSS platform APIs for interactive components, theme lifecycle management, and animation orchestration gaps that become critical as the component library grows.

### I92: Multi-Tenant Preset Cache Budget (Priority: High — do with I32 + I5)

**Problem**: I32 (multi-tenant theme support) describes a `TenantThemeResolver` that loads per-tenant presets, and I5 (CSS caching) adds `@lru_cache` for generated CSS. But neither addresses the production reality: a SaaS app with 500 tenants, each with an auto-generated preset (I21), creates 500 unique CSS outputs. An unbounded `@lru_cache` consumes ~5KB × 500 = 2.5MB of Python memory per worker — multiplied by N Gunicorn workers. With 1000+ tenants (djustlive's target), this becomes a significant memory pressure.

**Fix**:
1. Replace `@lru_cache` with a bounded LRU: `functools.lru_cache(maxsize=N)` where `N` defaults to `DJUST_THEMING['CSS_CACHE_SIZE']` (default: 100)
2. For deployments exceeding the cache size, add Django cache framework backend: `DJUST_THEMING['CSS_CACHE_BACKEND'] = 'default'` stores generated CSS in Redis/Memcached — shared across workers, survives restarts
3. Add `python manage.py djust_theme cache-stats` showing hit rate, memory usage, and eviction count — essential for capacity planning
4. Pre-warm the cache at startup for the N most-recently-active tenants (query from DB or read from a `popular_presets.json` sidecar)
5. For the linked CSS path (`theme_css_view`): add `Cache-Control: public, max-age=86400, stale-while-revalidate=3600` — CDN caches per-tenant CSS, eliminating Python generation for repeat requests entirely

**Why this matters now**: I32 and I5 are both Tier 1/2 items. Building them without a cache budget creates a performance cliff at scale that's expensive to retrofit — the cache key structure (I28) and generation function signature (I24) must accommodate bounded caching from day one.

### I93: CSS `@starting-style` for Component Enter Animations (Priority: Medium — do with Phase 2)

**Problem**: Phase 2 adds interactive components (modal, dropdown, toast, tooltip) that need enter/exit animations. I46 covers theme-level transitions. I71 covers token-value interpolation. But *component-level* enter animations (modal slides up, toast fades in, dropdown scales from origin) currently require JavaScript to add/remove animation classes. CSS `@starting-style` (baseline 2024, 85%+ support) enables declarative entry animations on elements that transition from `display: none` to visible — no JS class toggling needed.

**Fix**:
1. Component CSS for modal, dropdown, toast, tooltip uses `@starting-style` for enter animations:
```css
.modal {
    opacity: 1;
    transform: translateY(0);
    transition: opacity var(--duration-normal) ease, transform var(--duration-normal) ease,
                display var(--duration-normal) allow-discrete;
    @starting-style {
        opacity: 0;
        transform: translateY(1rem);
    }
}
```
2. Pair with `transition-behavior: allow-discrete` to animate `display` property changes
3. Exit animations use `[data-closing]` attribute set by `components.js` before removing the element (the JS requirement for exit is acceptable — CSS has no `@ending-style`)
4. Animation durations reference tokens (I19): `var(--duration-normal)` — `prefers-reduced-motion` (I13) collapses these to `0ms` automatically
5. Fallback for the ~15% without `@starting-style`: instant show/hide (functional, just not animated)

**Why do this with Phase 2**: Every interactive component needs an enter animation strategy. Choosing `@starting-style` over JS class-toggle now means all 15 new components use a consistent, declarative, token-driven animation pattern. Retrofitting later means modifying every component's CSS and JS.

### I94: Native Popover API for Overlay Components (Priority: Medium — do with Phase 2)

**Problem**: Phase 2 components — dropdown, tooltip, modal, toast — are all overlay patterns. The traditional approach (absolute positioning + z-index + JS focus trap + click-outside detection + scroll lock) is complex, fragile, and duplicated per component. The HTML Popover API (baseline 2024, 91%+ support) provides native support for: top-layer rendering (no z-index wars), light-dismiss (click-outside closes), focus management, and `::backdrop` styling.

**Fix**:
1. Modal uses `<dialog popover="manual">` for explicit open/close control with native `::backdrop`
2. Dropdown uses `<div popover="auto">` for auto-dismiss on click-outside — eliminates click-outside JS entirely
3. Tooltip uses `<div popover="hint">` (where supported) with CSS anchor positioning for zero-JS tooltip placement
4. Toast uses `<div popover="manual">` with JS-controlled auto-dismiss timer
5. `components.js` detects Popover API support and uses it; falls back to traditional absolute positioning + z-index for older browsers
6. Theme authors style `::backdrop` via tokens: `--backdrop-color`, `--backdrop-blur` (already conceptually present in modal designs)
7. Add `[popover]` to the component CSS architecture (I9 layers):
```css
@layer components {
    [popover] { /* base overlay styles */ }
    [popover]::backdrop { background: hsl(var(--backdrop, 0 0% 0% / 0.5)); }
}
```

**Why this matters**: The Popover API eliminates the single most complex piece of component JS — overlay management. `components.js` (Phase 2.3) becomes dramatically simpler. Focus trapping, scroll locking, and click-outside detection are browser-native. This reduces the JS surface area theme authors need to understand when customizing interactive components.

### I95: Animation Choreography for Compound Components (Priority: Low — do with I65)

**Problem**: I19 (animation tokens) and I71 (`@property` animated transitions) handle single-element animations. But compound interactions involve coordinated multi-element choreography: modal open = backdrop fade (100ms) → content slide up (200ms, starts at 50ms) → focus moves to first input (after animation). Toast stack = new toast slides in → existing toasts shift down with staggered delays. Tab switch = old panel fades out → new panel fades in (crossfade). Without choreography tokens, each theme reimplements these sequences independently, producing inconsistent timing.

**Fix**:
1. Add choreography tokens to `design_tokens.py`:
```css
:root {
    --stagger-delay: 50ms;       /* delay between staggered items */
    --sequence-gap: 100ms;       /* gap between choreography phases */
    --enter-duration: var(--duration-normal);
    --exit-duration: calc(var(--duration-normal) * 0.75); /* exits are faster */
}
```
2. Compound component CSS uses `transition-delay` computed from choreography tokens:
```css
.modal::backdrop { transition-delay: 0ms; }
.modal__content { transition-delay: var(--sequence-gap); }
.modal__content .btn:first-child { transition-delay: calc(var(--sequence-gap) * 2); }
```
3. Theme authors adjust choreography by overriding `--stagger-delay` and `--sequence-gap` — one token change affects all compound animations
4. `prefers-reduced-motion` collapses all choreography to instant (delays → `0ms`, durations → `0ms`)

### I96: Theme Preset Preloading for Instant Switching (Priority: Low — do with I46)

**Problem**: I46 (CSS transition on theme switch) proposes fetching new CSS from `theme_css_view()` on preset change. But network latency means a 100–500ms gap between click and visual update — noticeable and jarring, especially compared to the smooth `@property` animations (I71). The preset selector shows all available presets; the user's next preset choice is predictable (they hover before clicking).

**Fix**:
1. `theme.js` preset selector adds `mouseenter`/`focusin` listener on preset options
2. On hover: `<link rel="prefetch" href="/theme/css/?preset=nord&mode=dark">` — browser fetches CSS in background
3. On click: CSS is already cached by the browser — `fetch()` returns instantly from cache, transition is smooth
4. For inline CSS mode: prefetch the CSS content via `fetch()` and store in a JS Map; on click, swap `<style>` content from the Map
5. Budget: prefetch adds ~5–15KB of background network per hovered preset. Acceptable for theme switching UI where the user is actively browsing presets
6. `DJUST_THEMING['PREFETCH_PRESETS'] = True` (default: `True`) — disable for bandwidth-constrained environments

### I97: Palette Derivation Audit Trail (Priority: Low — do with I21)

**Problem**: I21 (auto-palette) generates a full `ThemePreset` from a single brand color via algorithmic derivation. When the generated palette doesn't look right ("why is my secondary purple when I gave it a blue?"), there's no way to understand how the algorithm derived each token. The derivation is opaque — the output is a preset with no record of the input color, derivation mode, or intermediate calculations. For multi-tenant SaaS (I32), debugging "tenant X says their theme looks wrong" requires re-running the generator and comparing outputs.

**Fix**:
1. `PaletteGenerator` records derivation metadata alongside the preset:
```python
preset = PaletteGenerator.from_brand_color(primary="#1E40AF", mode="professional")
preset.metadata  # PaletteMetadata instance
# {
#   "source_color": "#1E40AF",
#   "source_hsl": "221 83% 40%",
#   "mode": "professional",
#   "derivation": {
#     "secondary": {"method": "complementary", "hue_shift": 180, "result": "41 83% 40%"},
#     "accent": {"method": "analogous", "hue_shift": 30, "result": "251 83% 40%"},
#     "muted": {"method": "desaturate", "saturation_factor": 0.3, "result": "221 25% 85%"},
#   },
#   "quality_score": 94,
#   "adjustments": ["clamped secondary saturation from 95% to 80%"],
#   "generated_at": "2026-03-22T14:30:00Z"
# }
```
2. CLI: `python manage.py djust_theme inspect-preset my-brand` shows the derivation chain
3. For multi-tenant: store `PaletteMetadata` alongside the preset in the database — enables support debugging and preset regeneration with tweaked parameters
4. `validate --explain` includes derivation reasoning in its output

---

## Reprioritization Notes (2026-03-22, batch 10)

### Items to consolidate

Several improvement items overlap significantly and should be implemented as a single unit:

1. **I19 + I63 + I71 + I95** — All animation-related. Implement as "Animation System": tokens (I19) → consistency (I63) → `@property` registration (I71) → choreography (I95). One coherent animation architecture, not four separate changes.

2. **I16 + I21 + I44 + I49 + I97** — All color pipeline. Implement as "Color Engine": format interop (I16) → input validation (I44) → OKLCH (I49) → auto-palette (I21) → audit trail (I97). The color pipeline should be designed holistically.

3. **I5 + I24 + I26 + I28 + I45 + I92** — All CSS generation pipeline. Implement as "CSS Generation Engine": consolidate paths (I24) → state hash (I28) → caching with budget (I5 + I92) → compression (I26) → graceful failure (I45). These are inseparable — changing one affects all others.

### Strategic sequencing insight

The roadmap currently treats Phase 1 (template overrides) and the Color Engine (I16/I21/I49) as parallel workstreams. In practice, they should be **sequential** — template overrides first, then color tools:

- **Why**: Theme authors need to *see* the override system working before they invest in creating custom presets. If preset creation is polished but template overrides don't exist yet, the system is just a fancy color picker — not the "template-driven theming" vision.
- **Exception**: I16 (hex/RGB conversion) is genuinely blocking — theme authors can't even *start* without it. Ship I16 with Phase 1. Defer I21/I49/I97 to after Phase 1 is stable.

### Deferred items (move to v2.0+ backlog)

These items are well-specified but their complexity/risk exceeds their near-term value:

- **I14 (Theme composition/mix-and-match)** — Architecturally seductive but real-world demand is near-zero. No competing theming system offers this. Defer to v3.0.
- **I70 (Figma plugin)** — Requires a separate engineering discipline (Figma API, plugin distribution, ongoing maintenance). Partner with Tokens Studio rather than building a competitor. Remove from roadmap; add as "Ecosystem: consider partnership" note.
- **I55 (Tokens Studio import)** — Dependent on I70's value thesis. If Tokens Studio partnership happens, this becomes their responsibility. Defer.
- **I82 (Email-compatible export)** — Valuable but tangential to the core theming mission. Consider as a separate package (`djust-theming-email`) rather than core roadmap. Defer to post-v2.0.

### Updated tier placement for new items

| # | Item | Tier | Dependencies |
|---|------|------|--------------|
| I92 | Multi-tenant preset cache budget | Tier 1 | I5 + I24 + I32 — must be designed with CSS generation engine |
| I93 | CSS `@starting-style` enter animations | Tier 2 | Phase 2 — animation strategy for all interactive components |
| I94 | Native Popover API for overlays | Tier 2 | Phase 2 — overlay strategy for modal/dropdown/tooltip/toast |
| I95 | Animation choreography tokens | Tier 3 | I65 (compound components) + I19 (animation tokens) |
| I96 | Preset preloading for instant switching | Tier 3 | I46 (CSS transition on theme switch) |
| I97 | Palette derivation audit trail | Tier 3 | I21 (auto-palette) |

### Revised critical path (incorporating all batches)

```
Tier 0 (patch v1.1.3):
  I43 + I57 + I58 + I4/I48 → security/resilience fixes

Tier 1 (v1.2 — Foundation):
  I1 → I2+I9+I17+I34+I50+I61 → I3 → I5+I24+I28+I45+I92 → I23+I84 → I16 → I27+I60 → I87 → I88

Phase 1 (v1.3 — Template Override System):
  Template namespace resolution → manifest → scaffold → registry → validation

Tier 2 (v1.4 — Components):
  Phase 2 + I11+I53+I80+I81+I85+I90+I93+I94 → I65 → Phase 3 + I86+I20

Tier 3+ (v2.0+):
  I21+I49+I97 → Phase 4 → Phase 5+I64 → Phase 6 → Phase 7 → Phase 8+I74 → Phase 9
```

Key change from previous critical path: **I92 joins the CSS generation engine cluster in Tier 1** (cache budget must be designed with the generation pipeline, not bolted on after), and **I93+I94 join Phase 2** (animation strategy and overlay strategy must be decided before building 15 interactive components).

---

## New Improvements (Added 2026-03-22, batch 11)

Identified during a strategic review of the complete roadmap. Focus: migration from existing systems, theme lifecycle operations, AI-assisted theme creation, and production deployment gaps that none of the 100+ existing items address.

### I101: Migration Path from Bootstrap/Tailwind/shadcn (Priority: High — do with Phase 1)

**Problem**: The roadmap has excellent import/export for design tokens (I16, I30, I55, I89) but no migration path for teams already using Bootstrap, Tailwind UI, or shadcn/ui components. These are the three most common CSS frameworks. A team evaluating djust-theming asks "can I migrate my existing Bootstrap theme?" — the answer today is "start over." This is a hard adoption barrier for the primary target audience: teams with existing projects that want to adopt djust's reactive model without losing their visual investment.

**Fix**:
1. Add `python manage.py djust_theme migrate-from bootstrap --input custom.css` that:
   - Parses Bootstrap CSS variables (`--bs-primary`, `--bs-body-bg`, etc.) and maps to djust-theming tokens
   - Generates a `ThemePreset` from extracted color values
   - Outputs a mapping report showing Bootstrap vars → djust tokens
2. Add `djust_theme migrate-from tailwind --input tailwind.config.js` (v3) or `--input app.css` (v4):
   - Reads Tailwind theme colors, spacing, typography
   - Maps to djust-theming tokens (Tailwind's naming is close to ours)
3. Add `djust_theme migrate-from shadcn --input components.json` or `--input globals.css`:
   - shadcn's CSS variable names are nearly identical to djust-theming's (`--primary`, `--secondary`, `--muted`, etc.)
   - This should be the easiest migration — potentially zero manual adjustment
4. Migration produces: a preset file, a `theme.toml`, and a diff report showing which tokens mapped cleanly vs. which need manual review
5. Document each migration path with a step-by-step guide

**Why this is high priority**: The easiest way to grow adoption is to lower the switching cost from the incumbents. shadcn migration in particular should be near-automatic given the token naming overlap.

### I102: Theme Rollback and Safe Deployment (Priority: Medium — do with Phase 1)

**Problem**: When a theme change breaks the UI in production (missing token, bad template override, CSS generation error), there's no quick rollback. The `validate` command (Phase 1.5) catches many issues pre-deploy, but some failures only manifest at runtime with real data (e.g., a component that works in gallery but breaks with a 200-character title). Currently, rolling back requires reverting code and redeploying. For multi-tenant SaaS (I32), a bad tenant-generated preset shouldn't require a code deploy to fix.

**Fix**:
1. Add `ThemeState.fallback_preset` field (default: `"default"`) — when CSS generation fails for the active preset, automatically fall back instead of crashing (extends I45)
2. `ThemeManager` records the last successfully rendered preset per session. On error, reverts to the last-known-good preset and logs a warning
3. For multi-tenant: `TenantThemeResolver` caches the last working `ThemeState` per tenant. If a newly generated preset (from I21 auto-palette) fails validation, the resolver continues serving the previous working preset and notifies admins
4. Add `python manage.py djust_theme activate my-theme --canary 10%` for gradual rollout — serves the new theme to 10% of sessions (based on session cookie hash modulo), monitors for errors, and auto-rolls back if error rate exceeds threshold
5. Admin UI: `{% theme_admin_bar %}` shows current theme state for staff users, with a one-click "revert to default" button

### I103: AI-Assisted Theme Generation via Prompt (Priority: Medium — do with I21)

**Problem**: The "golden path" for theme creation starts with either a hex color (I21) or a design token export (I30). But the most natural way developers describe a desired theme is in words: "a calm, professional theme with blue accents and lots of whitespace" or "a dark cyberpunk theme with neon green highlights." The djust manifesto states "AI-Ready by Design" — the theming system should leverage this principle for theme creation, not just for app logic. An LLM can translate a natural language description into theme parameters better than most developers can manually specify them.

**Fix**:
1. Add `python manage.py djust_theme generate --prompt "calm professional theme with navy blue accents"`:
   - Uses a structured prompt template to extract: primary color family, mood (professional/playful/minimal), density (spacious/dense), radius (sharp/rounded/pill), typography style (serif/sans-serif/monospace)
   - Maps extracted attributes to `PaletteGenerator` parameters (I21) and design token overrides
   - Generates a complete `theme.toml` + `tokens.css` + preset
2. The prompt-to-theme mapping does NOT require a live LLM call — it uses a deterministic keyword-to-parameter mapper:
   - "professional" → muted saturation, system fonts, medium radius
   - "playful" → high saturation, rounded radius, larger spacing
   - "dark" → dark mode default, high-contrast tokens
   - "cyberpunk" → neon accent colors, monospace headings, sharp radius
3. Optional LLM integration via `DJUST_THEMING['AI_BACKEND'] = 'openai'` for more nuanced prompt interpretation — generates the parameter dict, then the deterministic generator produces the theme
4. Store the original prompt in `theme.toml` metadata for reproducibility:
   ```toml
   [theme]
   generated_from = "calm professional theme with navy blue accents"
   generated_at = "2026-03-22T14:30:00Z"
   ```
5. This directly enables a djustlive feature: "Describe your app's look and feel" → instant custom theme for deployed apps

**Why this matters**: This collapses the theme creation funnel from "understand tokens → pick colors → configure manifest" to "describe what you want." The deterministic mapper (no LLM needed) handles 80% of cases. The optional LLM path handles the nuanced 20%.

### I104: Theme Documentation Site Generator (Priority: Medium — do with Phase 9)

**Problem**: Phase 9 describes a "Theme Author Guide" and "Component Storybook" as documentation deliverables. But theme *consumers* (developers using a published theme) also need documentation: what tokens the theme defines, what components it overrides, what design decisions it embodies, and how to customize it further. Currently, a theme package is a collection of files with no generated documentation. Theme authors must manually write README files. The I37 (token reference) and I94 (anatomy) commands generate information but don't produce a browsable documentation site.

**Fix**:
1. `python manage.py djust_theme docs my-theme --output ./docs/` generates a static documentation site:
   - Token reference with color swatches, typography samples, spacing visualization
   - Component gallery showing every component in every variant
   - Override guide per component (from I94 anatomy data)
   - Inheritance chain visualization (from I77 resolve data)
   - Theme comparison vs. default (from I98 diff data)
2. Output is static HTML + CSS — no Django runtime needed, deployable to GitHub Pages
3. Uses the theme's own tokens to style the documentation site (dogfooding)
4. `--watch` flag for live-updating docs during development
5. Theme packages (Phase 5.2) include a `docs/` directory auto-generated at publish time

### I105: Template Resolution Performance Budget (Priority: Medium — do with Phase 1)

**Problem**: Phase 1's template resolution walks a fallback chain per component render: check theme directory → check base theme → check default. With Django's file-based template loader, each check is a filesystem stat. A page rendering 20 components with a 3-level inheritance chain = 60 filesystem stats per request. For high-traffic production sites, this adds measurable latency. The problem compounds with I14 (theme composition) where resolution checks multiple source themes.

**Fix**:
1. Cache template resolution results in `ThemeTemplateLoader` — once `button.html` resolves to `themes/my-theme/components/button.html`, cache that path for the lifetime of the process (invalidated on theme change or `DEBUG=True`)
2. At theme discovery time (startup), pre-scan all theme directories and build a resolution map: `{(theme_name, component_name): resolved_path}` stored in `ThemeRegistry`
3. `select_template()` calls in component tags hit the pre-built map — zero filesystem stats at request time
4. Add `python manage.py djust_theme bench my-theme` command that renders all components 1000 times and reports:
   ```
   Template resolution: avg 0.02ms/component (cached) vs 1.2ms/component (uncached)
   CSS generation: avg 0.5ms/request (cached) vs 12ms/request (uncached)
   Total theme overhead per request: ~0.9ms (20 components)
   ```
5. System check `djust_theming.W006`: warn when template resolution for any component exceeds 5ms (suggests broken cache or excessive inheritance depth)

### I106: Theme-Aware Error Boundaries (Priority: Low — do with Phase 2)

**Problem**: When a theme author's template override has a Django template syntax error (unclosed tag, undefined variable, missing closing block), the entire page crashes with a 500. The error message references the theme template but the crash takes down the whole page — including navigation, allowing the user to recover. In development this is annoying; in production it's dangerous if the theme was partially deployed.

**Fix**:
1. Component template tags (`theme_button`, etc.) wrap `tmpl.render()` in a try/except
2. On `TemplateSyntaxError` or `VariableDoesNotExist`:
   - Log the error with the theme template path and full traceback
   - Fall back to rendering the default (non-themed) template for that component
   - When `DEBUG=True`, render an inline error boundary showing the error message styled as a red-bordered box replacing the component — visible but not page-breaking
3. Error boundary HTML:
   ```html
   <div class="djt-error-boundary" style="border:2px solid red;padding:8px;font-family:monospace;font-size:12px">
     ⚠ Theme error in button.html: Unclosed tag 'if' at line 5
     <br>Falling back to default template.
   </div>
   ```
4. In production (`DEBUG=False`): silently render the default template, log the error. Users see unstyled components but the page works.
5. `validate` command already catches most syntax errors pre-deploy — error boundaries are the runtime safety net for the cases validation misses.

### I107: CSS Container Style Queries for Mode-Aware Components (Priority: Low — do with I18)

**Problem**: I18 (container-scoped theming) allows different presets/modes per DOM subtree. But component CSS currently uses `[data-theme-mode="dark"]` selectors on `:root` for dark mode variations. In a scoped context (light page with a dark sidebar), components in the sidebar can't inherit the scoped mode via `:root` — they need to query their container's style. CSS Container Style Queries (`@container style(--theme-mode: dark)`) enable this: components check their nearest container's custom property value instead of a global attribute.

**Fix**:
1. Layout templates (Phase 3) set `--theme-mode: light` or `--theme-mode: dark` as a CSS custom property on their container element (alongside `container-type`)
2. Component CSS uses container style queries for mode-aware styles:
   ```css
   .card { background: hsl(var(--card)); }
   @container style(--theme-mode: dark) {
       .card { box-shadow: none; border: 1px solid hsl(var(--border)); }
   }
   ```
3. This enables true per-region dark mode: a light-mode page can have a dark sidebar where all components automatically adapt — without any JavaScript or `data-` attribute propagation
4. Browser support (~80% as of 2026) — Tier C feature per I95 (progressive enhancement). Fallback: `[data-theme-mode="dark"]` ancestor selector (current approach)
5. Combine with I18's `[data-theme-scope]`: the scope element sets both `data-theme-scope` (for token scoping) and `--theme-mode` (for container style queries)

---

## Strategic Review & Simplification Notes (2026-03-22)

### Roadmap Complexity Assessment

The roadmap now contains 100+ improvement items across 11 batches, 9 phases, and 4 tiers. This is comprehensive but risks paralysis — no team can execute 100+ items with clarity. The following simplification recommendations aim to reduce cognitive overhead without losing the vision.

### Recommended Consolidation Groups

Rather than tracking 100+ items individually, organize execution around **7 work packages** that each deliver a coherent capability:

1. **WP-SECURITY** (ship as v1.1.3 patch, ~1 day):
   I43 + I57 + I58 + I4/I48 — security hardening + resilience

2. **WP-CSS-ENGINE** (Tier 1, ~1 week):
   I1 + I2 + I9 + I17 + I34 + I50 + I61 + I93 + I3 + I5 + I24 + I26 + I28 + I45 + I92
   Deliverable: CSS extracted from templates into layered files, cached, compressed, CSP-compatible, with fallback values

3. **WP-COLOR-ENGINE** (Tier 1, ~3 days):
   I16 + I44 + I21 + I41 + I49 + I30 + I101
   Deliverable: Create a preset from hex/RGB/OKLCH, import from Figma/W3C/Bootstrap/shadcn, auto-derive full palette with quality controls

4. **WP-DX-FOUNDATION** (Tier 1, ~3 days):
   I23 + I84 + I88 + I87 + I27 + I60
   Deliverable: Zero-config install, standalone switching without djust, system checks, component test harness, JS test suite, djust-components integration decision

5. **WP-TEMPLATE-SYSTEM** (Phase 1, ~1 week):
   Phase 1.1-1.5 + I78 + I11 + I73 + I37 + I25 + I92 + I96 + I102 + I105
   Deliverable: Template override system with manifest, scaffold, registry, validation, eject, slots, URL params, token docs, rollback

6. **WP-COMPONENT-LIBRARY** (Phase 2, ~2 weeks):
   Phase 2.1-2.4 + I11 + I53 + I80 + I81 + I85 + I90 + I93 + I94 + I65 + I99 + I106
   Deliverable: 20 components with slots, i18n, fragments, a11y validation, compound patterns, error boundaries, native popover/animations

7. **WP-LAYOUTS** (Phase 3, ~1 week):
   Phase 3.1-3.4 + I86 + I20 + I38 + I72
   Deliverable: 7 layout templates with responsive tokens, container queries, subgrid, meta tags

### Execution Sequence

```
v1.1.3:  WP-SECURITY
v1.2.0:  WP-CSS-ENGINE → WP-COLOR-ENGINE → WP-DX-FOUNDATION  (can partially overlap)
v1.3.0:  WP-TEMPLATE-SYSTEM
v1.4.0:  WP-COMPONENT-LIBRARY
v1.5.0:  WP-LAYOUTS
v2.0.0:  Phase 4 (Pages) + Phase 5 (Design System Variants) + I64 (Starter Kits)
v2.1.0:  Phase 6 (Forms) + Phase 7 (RTL/A11y/Print)
v3.0.0:  Phase 8 (Inspector) + Phase 9 (Docs/Ecosystem) + I103 (AI themes) + I104 (Doc generator)
```

### Items to Cut or Defer Indefinitely

These items are well-specified but their ROI doesn't justify the complexity:

- **I14 (Theme Composition/Mix-and-Match)** → Cut. No competing system offers this. Single-theme selection covers 99% of real use cases. The composition model adds significant complexity to the registry and template resolver for a feature nobody has asked for.
- **I70 (Figma Plugin)** → Cut from core roadmap. This requires a separate engineering discipline. Partner with Tokens Studio or Figma's built-in variable system instead. Keep I30 (W3C import) as the standard interchange.
- **I55 (Tokens Studio Import)** → Defer to community contribution. The W3C JSON format (I30) is the standard path. Tokens Studio can export W3C JSON.
- **I82 (Email-Compatible Export)** → Defer to a separate package (`djust-theming-email`). Email CSS is a fundamentally different domain.
- **I67 (Usage Analytics Hook)** → Defer. Premature for v1.x. Theme authors need the theming system to work before they need analytics about it.
- **I95 (Animation Choreography Tokens)** → Defer. Nice-to-have polish that adds complexity to the token system. Let theme authors handle choreography in their own CSS.
- **I97 (Palette Derivation Audit Trail)** → Defer. Useful for debugging but adds data model complexity. A `--verbose` flag on the generate command achieves 80% of the value.

### The One-Page Summary

If someone asks "what IS djust-theming?", this is the answer after the complete roadmap is executed:

> **djust-theming** is a template-driven theming system for Django. Start from a single brand color or a Figma export. Get a complete preset with light/dark mode, WCAG-validated contrast, and 67+ design tokens. Override any component's HTML via template inheritance or eject for full control. 20+ components with slots, i18n, accessibility contracts. 7 layout templates with responsive tokens. CSS cascade layers prevent specificity wars. Works standalone with vanilla Django, enhanced by djust LiveView for instant switching. Zero build step, zero npm, ~50KB CSS budget. Validate, lint, and stress-test your theme before deploy. Package and distribute via pip.

Everything in the roadmap serves this paragraph.

---

## Design Principles

1. **Templates over CSS** — If the visual change requires different HTML structure, use a template override, not a CSS hack.
2. **Convention over configuration** — Standard directory layout, standard block names, standard context variables. No registration boilerplate.
3. **Inherit everything, override anything** — A theme that overrides zero templates is valid (pure token customization). A theme that overrides every template is also valid. A theme that overrides one slot in one component is also valid (I11).
4. **Components are contracts** — The context variables a component receives are its API. Theme authors must handle the same inputs. Output HTML can differ entirely.
5. **Zero JS for theming** — Template overrides and CSS tokens handle all visual customization. JavaScript is only for interactive behaviors (dropdowns, modals) that are shared across themes.
6. **Logical properties for layout** — All CSS uses logical properties (`inline-start`/`block-end`) instead of physical (`left`/`top`) so themes work in RTL without additional overrides.
7. **CSS lives in CSS files, HTML lives in templates** — No `<style>` blocks in component templates. No HTML strings in Python. Clean separation enables independent override of structure vs. styling.
8. **Layers prevent specificity wars** — All CSS uses `@layer` ordering (`base → tokens → components → layouts → theme`). Theme author CSS always wins without needing `!important` or high-specificity selectors.
9. **Respect user preferences** — Honor `prefers-reduced-motion`, `prefers-contrast`, and `prefers-color-scheme`. Themes that ignore accessibility preferences must explicitly opt out in their manifest, and the validator warns about it.

---

## Resolved Decisions

These were previously open questions, now decided:

- **Template language**: Django templates. Jinja2 is faster but compatibility with the djust ecosystem (template tags, inclusion tags, block inheritance) is more important.
- **Theme-specific static assets**: Use Django's `STATICFILES_FINDERS` with a `ThemeStaticFinder` that discovers static files from active theme packages. Fonts and images go in `themes/{name}/static/`.
- **Theme inspector access**: Gated by `DJUST_THEME_INSPECTOR_ENABLED` setting (default: `settings.DEBUG`). The `@csrf_exempt` on inspector views will be replaced with proper auth check.
- **Component JS strategy**: Vanilla JS data-attribute hooks for broad compatibility. When djust is present, components detect it and defer to `dj-click`/`dj-model` directives. This keeps theming usable outside of djust LiveViews.
- **Theme inheritance depth**: Single level for v1.0 — any theme extends "default" only. Multi-level inheritance (theme families) deferred to v2.0 to avoid complexity.
- **CSS architecture**: Extracted from templates into standalone CSS files. Components reference CSS classes only. This is a hard requirement for the template override system to work cleanly.
- **Container queries**: Yes — adopt `@container` as the primary responsive strategy for components (Phase 3 layouts). Fallback to `@media` for the ~5% of browsers without support. Components that need context-aware sizing (card in sidebar vs. card in main content) benefit enormously from `@container`. Layout templates wrap content areas with `container-type: inline-size`.
- **CSS layers (`@layer`)**: Yes — adopt throughout (I9). Layer order: `@layer base, tokens, components, layouts, theme`. Browser support is 95%+ (2025). The predictable cascade is essential for theme authoring — without it, theme authors need deep knowledge of built-in selector specificity to write reliable overrides.
- **Theme hot-reload in development**: Yes, but lightweight. `ThemeTemplateLoader` adds theme directories to Django's `DIRS` setting. Django's built-in `--reload` with `StatReloader` already watches `DIRS` for changes. No custom file watcher needed — just ensure theme template directories are registered at startup.
- **Performance budget**: Yes — the `validate` command warns when total theme CSS exceeds 50KB (gzipped). Not enforced as a hard error since some themes (e.g., design system variants with many component overrides) may legitimately exceed this. The warning includes a breakdown by layer so authors can identify bloat.

---

## Numbering Conflict Resolution (2026-03-22)

Batches 4 and 10 both used I92–I97. Renumbering batch 10 items to I108–I113 to avoid collision:

| Old # | New # | Title |
|-------|-------|-------|
| I92 (batch 10) | I108 | Multi-Tenant Preset Cache Budget |
| I93 (batch 10) | I109 | CSS `@starting-style` for Component Enter Animations |
| I94 (batch 10) | I110 | Native Popover API for Overlay Components |
| I95 (batch 10) | I111 | Animation Choreography for Compound Components |
| I96 (batch 10) | I112 | Theme Preset Preloading for Instant Switching |
| I97 (batch 10) | I113 | Palette Derivation Audit Trail |

All references in the execution order and critical path sections should use the new numbers. The batch 4 items (I92–I100) retain their original numbers.

---

## New Improvements (Added 2026-03-22, batch 12)

Fresh review focused on: deploy-time optimization, ecosystem integration with popular Django packages, modern CSS platform APIs, developer tooling gaps, and the "last mile" between having a theming system and it being adopted in real projects.

### I114: Deploy-Time CSS Pre-Generation via collectstatic (Priority: High — do with WP-CSS-ENGINE)

**Problem**: CSS is generated at runtime on every request (even with I5 caching, the first request per preset per worker regenerates). For production deployments, this is wasteful — theme tokens and presets are static at deploy time. CDN-served apps can't use the `theme_css_view` endpoint without origin hits. Static site deployments (WhiteNoise, Nginx) have no Python runtime to generate CSS at all. The `collectstatic` step is the natural hook for pre-generating CSS, but djust-theming doesn't participate in it.

**Fix**:
1. Add a `ThemeStaticFilesStorage` that pre-generates CSS for all registered presets during `collectstatic`:
   ```
   STATIC_ROOT/djust_theming/css/
   ├── default-light.css
   ├── default-dark.css
   ├── nord-light.css
   ├── nord-dark.css
   └── ... (one file per preset × mode)
   ```
2. `{% theme_head mode="static" %}` links to the pre-generated CSS file instead of inlining or calling the view
3. The `theme.js` preset switcher swaps `<link>` href between pre-generated files — zero server round-trips
4. For multi-tenant (I32): `djust_theme prebuild --presets tenant1,tenant2,...` pre-generates tenant CSS at deploy time
5. Setting: `DJUST_THEMING['CSS_MODE'] = 'static' | 'dynamic' | 'inline'`:
   - `'static'`: pre-generated files via collectstatic (production, CDN-friendly)
   - `'dynamic'`: `theme_css_view` endpoint (current behavior, needed for runtime-generated tenant presets)
   - `'inline'`: embedded in HTML (current default, zero extra requests)
6. This eliminates all runtime CSS generation for apps with a fixed set of presets — the most common case

**Why this is high priority**: Production performance. Every other CSS optimization (I5 caching, I26 compression, I28 state hash) optimizes runtime generation. This eliminates it entirely. Pre-generated CSS can be served by CDN with infinite cache TTL. Combined with I71 (`@property` animations), preset switching becomes: swap one `<link>` tag → browser interpolates all colors smoothly → zero server involvement.

### I115: Integration with django-crispy-forms and django-allauth (Priority: Medium — do with Phase 6)

**Problem**: Phase 6 (Form Integration) describes a `ThemeFormRenderer` that themes Django's built-in form rendering. But the two most popular Django form/auth packages — django-crispy-forms (7K+ GitHub stars) and django-allauth (9K+ GitHub stars) — have their own template systems that bypass Django's form renderer. A project using crispy-forms renders forms via `{% crispy form %}`, not `{{ form.as_div }}`. A project using allauth has login/signup/password-reset pages in `allauth/templates/`. Neither gets themed automatically by Phase 6's `ThemeFormRenderer`. Since these are the most-used Django packages for the exact pages themes need to style (auth flows, forms), ignoring them means most real projects need manual work after adopting djust-theming.

**Fix**:
1. **django-crispy-forms**: Ship a `DjustThemingFormHelper` or a crispy template pack (`djust_theming/crispy/`) that renders crispy-forms using theme component templates. Setting:
   ```python
   CRISPY_TEMPLATE_PACK = 'djust_theming'
   ```
   This makes `{% crispy form %}` output theme-styled HTML with correct CSS classes and token-driven styling.
2. **django-allauth**: Ship template overrides in `djust_theming/templates/allauth/` that extend theme layouts and use theme components for auth forms. Enable via:
   ```python
   INSTALLED_APPS = [
       'djust_theming',      # Must be before allauth
       'allauth',
       'allauth.account',
   ]
   ```
   Django's template resolution picks djust-theming's overrides first.
3. **django-tables2**: Optional integration — map `django_tables2.Table` rendering to `theme_table` component CSS classes
4. Each integration is optional — only activates when the target package is in `INSTALLED_APPS`
5. Test suite: render allauth login page + crispy form with every preset, validate HTML structure

**Why this matters**: The fastest way to prove djust-theming's value is "install it, and your existing allauth login page looks branded." If the first thing a developer sees after installing djust-theming is an unthemed allauth page, they'll question whether the system works with real apps.

### I116: CSS Anchor Positioning for Tooltip and Dropdown (Priority: Medium — do with Phase 2)

**Problem**: Phase 2 adds tooltip, dropdown, and popover components that need to position themselves relative to a trigger element. Traditional approaches use JavaScript (measure trigger position, calculate offset, handle viewport collisions, reposition on scroll/resize). The I110 (Popover API) handles top-layer rendering but NOT positioning — a popover still appears at its DOM position, not anchored to its trigger. CSS Anchor Positioning (baseline 2025, ~85% support) solves this entirely in CSS: an element declares its anchor, the browser handles all positioning, viewport collision, and scroll tracking natively.

**Fix**:
1. Trigger elements use `anchor-name`:
   ```css
   .dropdown-trigger { anchor-name: --dropdown; }
   ```
2. Overlay elements use `position-anchor` + `position-area`:
   ```css
   .dropdown-menu {
       position: fixed;
       position-anchor: --dropdown;
       position-area: block-end span-inline-end;
       position-try: flip-block, flip-inline;  /* auto-flip if clipped */
   }
   ```
3. No JavaScript positioning logic needed — browser handles anchor tracking, viewport collision, and scroll repositioning
4. `components.js` is dramatically simpler: just toggle `[popover]` open/close, browser handles placement
5. Fallback for ~15% without anchor positioning: absolute positioning + JS measurement (traditional approach in `components.js`)
6. Theme authors can override positioning via tokens:
   ```toml
   [tokens.overlays]
   dropdown_placement = "block-end"    # "block-end", "block-start", "inline-end", "inline-start"
   dropdown_offset = "4px"
   ```

**Why do this with Phase 2**: Every overlay component (dropdown, tooltip, popover, select) needs a positioning strategy. Choosing CSS Anchor Positioning now means these components are CSS-native with JS as fallback. Choosing JS positioning now means all 4+ components have complex measurement code that becomes legacy when anchor positioning reaches Tier A browser support (~2027).

### I117: Django Debug Toolbar Integration Panel (Priority: Low — do with Phase 8)

**Problem**: Theme development debugging currently requires: checking cookies in browser DevTools, reading source HTML for `data-theme-*` attributes, inspecting CSS in Elements panel for active token values, checking Django logs for CSS generation errors. I47 (Theme Debugging Overlay) addresses the browser side, but server-side debugging (why did `ThemeManager` pick this preset? how long did CSS generation take? was it cached?) requires Django Debug Toolbar — the standard Django development tool. No panel exists for djust-theming.

**Fix**:
1. Add `djust_theming.debug.DjustThemingPanel` (Django Debug Toolbar panel):
   ```python
   # settings.py
   DEBUG_TOOLBAR_PANELS = [
       ...,
       'djust_theming.debug.DjustThemingPanel',
   ]
   ```
2. Panel shows:
   - **Theme State**: active theme, preset, mode, resolution source (cookie/session/URL/config/tenant)
   - **CSS Generation**: time (ms), cache hit/miss, output size (bytes), generation path (inline/linked/static)
   - **Template Resolution**: per-component resolution chain (which template was used, fallback attempts)
   - **Token Values**: all active tokens with rendered colors (swatches), showing overrides vs. defaults
   - **System Checks**: any warnings from `djust_theming.checks` for the current request context
3. Zero overhead when Debug Toolbar is not installed — panel class only imported when `debug_toolbar` is in `INSTALLED_APPS`
4. This complements I47 (browser-side overlay) with server-side insight

### I118: Theme Smoke Test Command (Priority: Medium — do with I27)

**Problem**: The `validate` command (Phase 1.5) checks theme structure — valid manifest, templates render, contracts satisfied. But it doesn't test the theme *end-to-end*: does `{% theme_head %}` actually produce valid CSS? Do all `{% theme_* %}` tags render without error when used together in a page? Does the CSS-to-HTML integration work (CSS classes in generated CSS match classes in rendered HTML)? The test harness (I27) tests individual components in isolation. Neither tests the full page render path that real users experience.

**Fix**:
1. `python manage.py djust_theme smoke-test my-theme` renders a full test page that uses every component, every layout, every variant:
   - Renders `{% theme_head %}` and verifies output is valid CSS (parses without error)
   - Renders every `{% theme_* %}` component tag with sample context
   - Cross-references: every CSS class referenced in component HTML exists in the generated CSS
   - Cross-references: every CSS variable referenced in generated CSS is defined in the token output
   - Checks for HTML validity (unclosed tags, mismatched elements)
2. Outputs a report:
   ```
   Theme: my-theme
   ✓ theme_head: 14.2 KB CSS, valid, 67 tokens defined
   ✓ button: 5 variants rendered, all CSS classes resolved
   ✓ card: 3 variants rendered, all CSS classes resolved
   ✗ modal: CSS class ".modal-backdrop" in HTML not found in generated CSS
     → Hint: Did you mean ".modal-overlay"? (found in components.css)
   ✓ Cross-reference: 0 undefined CSS variables, 0 orphaned CSS rules

   Result: 19/20 components passed, 1 issue found
   ```
3. This is the "integration test" complement to `validate` (structural) and `lint` (quality) — it tests the assembled system, not individual parts
4. Run in CI: `djust_theme smoke-test my-theme --exit-code` returns non-zero on failures

### I119: Theme Adoption Quickstart — One-Command Demo (Priority: High — do with I84)

**Problem**: I84 (zero-config) removes configuration barriers. But the first thing a developer evaluating djust-theming wants to see is the system working — not reading docs, not configuring settings, not scaffolding a theme. The ideal evaluation path is: `pip install djust-theming` → one command → see a themed page with components, preset switcher, dark mode. Currently, reaching that first visual impression requires: create a Django project, add to settings, create a template, add `{% theme_head %}`, add `{% theme_switcher %}`, add component tags, run the server, visit the page. That's 7+ steps before seeing any output.

**Fix**:
1. `python manage.py djust_theme demo` launches a self-contained demo page at `localhost:8000/theming/demo/`:
   - Shows every component in every variant
   - Includes a working preset switcher and mode toggle
   - Renders a sample layout (sidebar + content)
   - Requires ONLY `'djust_theming'` in `INSTALLED_APPS` and `include('djust_theming.demo.urls')` in urlpatterns (or auto-included when `DEBUG=True` via I84)
2. Demo page is a single Django view + template bundled with djust-theming — no external dependencies
3. Demo URL is gated behind `DEBUG=True` — never accessible in production
4. Demo page includes a "Getting Started" section showing the minimal code to reproduce each component
5. This is the "playground" that converts evaluators into adopters. The demo answers "what does this look like?" in under 60 seconds.

**Why this is high priority**: The adoption funnel has a massive drop-off between "pip install" and "first visual result." Every additional step between install and seeing output loses potential adopters. A one-command demo eliminates that gap entirely. This is how Tailwind CSS, Storybook, and shadcn/ui hook developers — they show results before requiring investment.

---

## Updated Work Package Summary (2026-03-22, batch 12 additions)

### WP-CSS-ENGINE additions
- **I114** (Deploy-time CSS pre-generation) — adds `static` CSS mode, eliminates runtime generation for fixed presets

### WP-DX-FOUNDATION additions
- **I119** (One-command demo) — the single highest-impact adoption accelerator, bundle with I84 zero-config
- **I118** (Smoke test command) — end-to-end integration test, bundle with I27 test harness

### WP-COMPONENT-LIBRARY additions
- **I116** (CSS Anchor Positioning) — eliminates JS positioning for overlay components, do with Phase 2
- **I115** (crispy-forms + allauth integration) — makes themes work with the most popular Django packages, do with Phase 6

### WP-LAYOUTS additions (none)

### Tier 3 additions
- **I117** (Django Debug Toolbar panel) — server-side debugging companion to I47 browser overlay

### Updated Execution Sequence

```
v1.1.3:  WP-SECURITY (I43 + I57 + I58 + I4/I48)

v1.2.0:  WP-CSS-ENGINE (I1 + I2 + I9 + I17 + I34 + I50 + I61 + I93 + I3 + I5 + I24 + I26 + I28 + I45 + I108 + I114)
         WP-COLOR-ENGINE (I16 + I44 + I21 + I41 + I49 + I30 + I101)
         WP-DX-FOUNDATION (I23 + I84 + I119 + I88 + I87 + I27 + I60 + I118)

v1.3.0:  WP-TEMPLATE-SYSTEM (Phase 1.1-1.5 + I78 + I11 + I73 + I37 + I25 + I92 + I96 + I102 + I105)

v1.4.0:  WP-COMPONENT-LIBRARY (Phase 2.1-2.4 + I11 + I53 + I80 + I81 + I85 + I90 + I109 + I110 + I116 + I65 + I99 + I106)

v1.5.0:  WP-LAYOUTS (Phase 3.1-3.4 + I86 + I20 + I38 + I72)

v2.0.0:  Phase 4 (Pages) + Phase 5 (Design System Variants) + I64 (Starter Kits) + I115 (crispy/allauth)
v2.1.0:  Phase 6 (Forms) + Phase 7 (RTL/A11y/Print)
v3.0.0:  Phase 8 (Inspector + I117) + Phase 9 (Docs/Ecosystem) + I103 (AI themes) + I104 (Doc generator)
```

### Key Priority Changes from This Review

1. **I114 (Pre-generated CSS) elevated to WP-CSS-ENGINE**. Runtime CSS generation is the wrong default for production. Pre-generation via `collectstatic` should be the recommended production path from v1.2 onward. This changes the performance story from "we cache it" to "we don't generate it at all."

2. **I119 (One-command demo) is the most impactful single item for adoption**. It should ship in the same release as I84 (zero-config). Together they create the "60-second evaluation" path: `pip install djust-theming` → add to `INSTALLED_APPS` → `manage.py djust_theme demo` → see everything working. No other item in the roadmap has this conversion-rate impact.

3. **I116 (CSS Anchor Positioning) reduces Phase 2 JS complexity by ~50%**. The biggest risk in Phase 2 is `components.js` growing into a complex positioning/collision-detection library. CSS Anchor Positioning eliminates that entire concern for overlay components. With I110 (Popover API) handling top-layer and I116 handling positioning, `components.js` shrinks to: open/close state management + keyboard navigation. That's it. This dramatically reduces the Phase 2 timeline and maintenance burden.

4. **I115 (crispy-forms + allauth) should move to v2.0, not Phase 6**. Phase 6 is "Form Integration" which is about Django's built-in form rendering. crispy-forms and allauth are the packages real projects use. Shipping v2.0 with both form renderer + package integrations means the "forms" story is complete in one release.

5. **I118 (Smoke test) fills the critical gap between unit tests (I27) and manual QA**. The validate + lint + smoke-test trifecta gives theme authors confidence at three levels: structure → quality → integration. This should exist before Phase 2 creates 15 new components — the smoke test catches CSS-HTML mismatches that unit tests miss.

### Numbering Convention Going Forward

To avoid further conflicts, each batch should claim a contiguous range and document it in a header comment.

---

## New Improvements (Added 2026-03-22, batch 5 — I120–I133)

Identified during a deep code review of `manager.py`, `mixins.py`, `theme_tags.py`, `theme_components.py`, `css_generator.py`, `theme.js`, `context_processors.py`, and `views.py`. This batch focuses on **runtime safety**, **developer experience**, and **code hygiene** — issues that affect every current deployment but aren't architectural (unlike the Phase-level items).

### I120: Race Condition in ThemeManager.toggle_mode() (Priority: High — do with Tier 0)

**Problem**: `toggle_mode()` (manager.py) calls `get_state()`, computes the new mode, then `set_mode()`. Between `get_state()` and `set_mode()`, another request or tab could modify the session, causing `toggle_mode()` to operate on stale state. This creates a TOCTOU (time-of-check-to-time-of-use) race: two rapid toggles from different tabs can both read "light" and both write "dark" — no actual toggle occurs.

**Fix**: Refactor `toggle_mode()` to read the current mode inside `set_mode()`, making the read-compute-write atomic within a single session access. Alternatively, use Django's `request.session.cycle_key()` or compare-and-swap pattern. For the cookie path (which can't be atomic), accept eventual consistency but ensure server-side session is authoritative.

### I121: Module-Level Logger Setup (Priority: Low — do with Tier 0)

**Problem**: `manager.py` calls `import logging` and `logger = logging.getLogger(__name__)` INSIDE `get_state()`, which runs on every template tag invocation. Python caches imports, but `getLogger()` does a dict lookup on every call. More importantly, this pattern is non-standard Django — loggers belong at module scope.

**Fix**: Move `import logging` to the top of `manager.py` and `logger = logging.getLogger(__name__)` to module level. One-line change, eliminates per-request logger resolution overhead.

### I122: ThemeMixin._skip_render Not Initialized (Priority: High — do with Tier 0)

**Problem**: `ThemeMixin` sets `self._skip_render = True` inside `_push_theme_update()` (mixins.py), but `_skip_render` is never initialized at class level or in `mount()`. If a subclass calls any theme method before `mount()` completes, or if a subclass forgets `super().mount()`, accessing `self._skip_render` raises `AttributeError`. This is a latent crash waiting for the wrong subclass pattern.

**Fix**: Initialize `_skip_render = False` as a class attribute alongside `_theme_manager = None` at the top of `ThemeMixin`. This follows the same pattern djust core uses for `_skip_render` in `LiveView`.

### I123: Anti-FOUC Script DRY Violation (Priority: Medium — do with I1)

**Problem**: The anti-FOUC (Flash of Unstyled Content) script is hardcoded identically in THREE places: `mixins.py` (~line 92), `theme_tags.py` (~line 87), and `context_processors.py` (~line 41). Each is a slightly different copy of the same ~15-line JavaScript snippet. When a FOUC fix is needed (e.g., the Safari private browsing fix in I58), all three must be updated independently — easy to miss.

**Fix**: Extract to a single `djust_theming.utils.get_anti_fouc_script()` function that returns the script string. All three consumers call this function. When I1 moves inline HTML to templates, this function moves to a shared template fragment (`_anti_fouc.html`) that all three include via `{% include %}`.

### I124: Silent Theme Pack Fallback — No Logging (Priority: Medium — do with I5/I24)

**Problem**: When `ThemePackCSSGenerator` raises `ValueError` (pack not found), the except blocks in `theme_tags.py`, `views.py`, and `context_processors.py` silently fall back to `CompleteThemeCSSGenerator`. No log message, no console warning, no HTML comment. A theme pack that fails to load (missing file, import error, renamed pack) is invisible to the developer — the page renders with wrong colors and no diagnostic.

**Fix**: Add `logger.warning(f"Theme pack '{state.pack}' failed to load: {e}; falling back to theme='{state.theme}' preset='{state.preset}'")` in every except block. In DEBUG mode, also emit an HTML comment `<!-- djust-theming WARNING: pack '{pack}' failed, using fallback -->` so it's visible in View Source. This aligns with I29 (graceful degradation) but is specifically about the Python fallback path, not missing static assets.

### I125: ThemeMixin Event Handlers Return No Feedback on Invalid Input (Priority: Medium — do with I88)

**Problem**: `set_theme_mode()` and `set_theme_preset()` in `mixins.py` silently return early when receiving invalid values (e.g., `mode="invalid"`, `preset="nonexistent"`). No server-side log, no client-side error event, no djust error push. The UI remains in whatever state it was in — the user clicks a theme option and nothing happens with no indication why.

**Fix**:
1. Log a warning: `logger.warning(f"Invalid theme preset '{preset}' — not in registry")`
2. Push a client error event via djust: `self.push_event('theme_error', {'message': f'Unknown preset: {preset}'})`
3. If djust is not available (standalone mode per I88), return an error in the HTTP response
4. The `theme.js` client listens for `theme_error` events and logs to console (development) or dispatches a `CustomEvent` (for app-level error handling)

### I126: Template Tag Parameters Not Validated (Priority: Medium — do with I27)

**Problem**: Template tag functions like `theme_preset_selector(layout=...)` accept any string for enum-like parameters. Passing `layout="grdi"` (typo) produces no error — the component renders with broken layout and no diagnostic. Same issue for `variant` on buttons, `size` on inputs, etc. Template authors discover typos only by visual inspection.

**Fix**:
1. Define valid values as constants: `VALID_LAYOUTS = {"dropdown", "grid", "list"}`
2. Validate in each tag function: `if layout not in VALID_LAYOUTS: raise TemplateSyntaxError(f"Invalid layout '{layout}'. Valid: {VALID_LAYOUTS}")`
3. Add these validations to the I27 component test harness — each component's contract includes its valid parameter values
4. In production (`DEBUG=False`), log a warning instead of raising to avoid crashing pages over a typo

### I127: Preset Color Swatch Shows Wrong Mode (Priority: Low — do with I88)

**Problem**: The theme switcher's preset color swatch (manager.py ~line 248) always uses `preset.dark.primary.to_hsl()` regardless of the current mode. Users in light mode see dark-mode colors in the preset selector, which don't match what they'll actually see. This creates a confusing "the swatch color doesn't match my theme" experience.

**Fix**: Use `preset.light.primary` when `resolved_mode == "light"`, `preset.dark.primary` when `resolved_mode == "dark"`. For `resolved_mode == "system"`, use `prefers-color-scheme` detection (already available via `theme.js`) to select the appropriate swatch. The swatch should update when the user toggles mode — this naturally fits with the I88 standalone theme switching work.

### I128: ThemeMixin Context Attributes Undeclared — No IDE Support (Priority: Low — do with I1)

**Problem**: `ThemeMixin._setup_theme_context()` dynamically sets instance attributes (`self.theme_head`, `self.theme_css`, `self.theme_switcher`, `self.theme_preset`, `self.theme_mode`, etc.) with no class-level type annotations. IDEs and type checkers can't discover these attributes. Template authors using `{{ theme_head }}` in templates get no autocomplete or validation.

**Fix**: Add typed class-level declarations to `ThemeMixin`:
```python
class ThemeMixin:
    theme_head: str = ""
    theme_css: str = ""
    theme_switcher: str = ""
    theme_preset: str = ""
    theme_mode: str = ""
    theme_mode_toggle: str = ""
    _theme_manager: Optional['ThemeManager'] = None
    _skip_render: bool = False  # Also fixes I122
```

This enables IDE autocomplete, mypy checking, and serves as documentation for theme authors. When I1 moves HTML to templates, these attributes may change type (from `str` to `SafeString` or template objects) — the type annotations document the contract.

### I129: CSS Custom Property Fallback Values Missing (Priority: Medium — do with I2)

**Problem**: Component CSS uses `hsl(var(--primary))` without fallback values. If CSS loads before the `:root` token block (e.g., due to `@layer` ordering in I9, or a slow network splitting the CSS payload), `var(--primary)` is undefined and the component renders with transparent/invisible colors. The anti-FOUC script handles dark/light mode switching but doesn't address token availability.

**Fix**: Include fallback values in component CSS for critical tokens:
```css
.btn--primary { background: hsl(var(--primary, 221 83% 53%)); }
```

The fallback values come from the `default` preset. The CSS generator can inject these automatically when `DJUST_THEMING['CSS_FALLBACKS'] = True` (default in v2.0). This is a defense-in-depth measure — it shouldn't normally trigger, but prevents broken rendering when it does.

### I130: ThemeMixin push_event Availability — Silent Degradation (Priority: Medium — do with I88)

**Problem**: `ThemeMixin._push_theme_update()` checks `hasattr(self, 'push_event')` and silently does nothing if djust's `LiveView` isn't the base class. This means a developer using `ThemeMixin` with a plain Django `View` gets a theme switcher that appears to work (server state updates) but never pushes live updates to the client. There's no log, no error, no indication that reactive switching is disabled.

**Fix**:
1. On first `mount()` or first theme operation, check for `push_event` and log: `logger.info("ThemeMixin: djust LiveView detected — reactive theme switching enabled")` or `logger.warning("ThemeMixin: push_event not available — theme changes require page reload. Use djust.LiveView for reactive switching.")`
2. Set `self._theme_reactive = hasattr(self, 'push_event')` in `mount()` so subsequent checks use a boolean instead of repeated `hasattr()` calls
3. Document in the ThemeMixin docstring: "For reactive theme switching, inherit from `djust.LiveView`. For static themes, `ThemeMixin` works with any Django view but requires page reload on change."

### I131: localStorage Key Collision in Multi-App Contexts (Priority: Low — do with I18)

**Problem**: `theme.js` uses global localStorage keys like `'djust-theme-mode'`, `'djust-theme-preset'`. If two djust-theming instances are embedded in the same origin (e.g., two micro-frontend apps, or a main app + admin panel on the same domain), they share and overwrite each other's theme state. This also applies to iframes on the same origin.

**Fix**: Add an optional `data-theme-app-id` attribute on the `<html>` element (set by `{% theme_head %}`):
```html
<html data-theme-app-id="my-app">
```

`theme.js` reads this and prefixes all storage keys: `my-app:djust-theme-mode`. Default (no `data-theme-app-id`) uses unprefixed keys for backward compatibility. This complements I18 (container-scoped theming) which handles CSS scoping — I131 handles *state* scoping.

### I132: Stale Theme Cookies — No Version/Cleanup Mechanism (Priority: Low — do with I57)

**Problem**: `theme.js` sets cookies with `max-age=31536000` (1 year). If a preset or design system is renamed or removed between deployments, stale cookies reference a name that no longer exists. `ThemeManager.get_state()` validates against `THEMES`/`THEME_PRESETS` and falls back to default, but the stale cookie persists for up to a year — every request carries dead cookie data, and every request triggers the fallback validation path.

**Fix**:
1. Add a `djust_theme_version` cookie set to a hash of registered preset/theme names
2. On `theme.js` init, compare the version cookie against a `data-theme-version` attribute on `<html>` (set by `{% theme_head %}`)
3. If versions differ, clear all `djust_theme_*` cookies and re-initialize from defaults
4. Server-side: `ThemeManager.get_state()` clears invalid cookies in the response (set `max-age=0`) instead of silently falling back — this actively cleans up stale state

### I133: Type Hints Missing Across Core Modules (Priority: Low — do incrementally)

**Problem**: `manager.py`, `css_generator.py`, `context_processors.py`, and `views.py` have minimal or no type annotations. Functions like `get_theme_config()`, `_get_session_data()`, `generate_css()` have no return type hints. The `session` property in `ThemeManager` returns `None | Session` with no annotation. This blocks mypy/pyright adoption and makes the codebase harder for contributors and AI tools to reason about.

**Fix**:
1. Add a `py.typed` marker file to the package
2. Add type annotations incrementally, starting with public API functions:
   - `ThemeManager.get_state() -> ThemeState`
   - `ThemeManager.set_mode(mode: str) -> None`
   - `generate_css(theme_name: str, preset: str) -> str`
   - `theme_context(request: HttpRequest) -> dict[str, Any]`
3. Add `mypy` to CI with `--strict` on new files, `--ignore-missing-imports` on existing
4. Priority: type the `ThemeState` and `ThemeManager` API first since those are what theme authors and djust integrations interact with

---

### Batch 5 Priority Assessment

**Add to Tier 0 (security/resilience — ship in v1.1.3):**
- **I120** (toggle race condition) — data corruption risk in concurrent sessions
- **I122** (_skip_render initialization) — latent `AttributeError` crash

**Add to Tier 1 (foundation — do with related items):**
- **I123** (anti-FOUC DRY) — do with I1 (both eliminate inline HTML duplication)
- **I124** (silent fallback logging) — do with I5/I24 (CSS generation path consolidation)
- **I126** (tag param validation) — do with I27 (component test harness defines valid params)
- **I129** (CSS fallback values) — do with I2 (CSS extraction restructures all component CSS)
- **I130** (push_event warning) — do with I88 (standalone theme switching)

**Add to Tier 2 (template-driven theming):**
- **I125** (event handler feedback) — do with I88 (standalone mode needs error path)
- **I127** (preset swatch mode) — do with I88 (switcher UX improvements)
- **I128** (type annotations on ThemeMixin) — do with I1 (mixin rewrite)

**Add to Tier 3 (polish):**
- **I131** (localStorage key collision) — do with I18 (container-scoped theming)
- **I132** (stale cookie cleanup) — do with I57 (cookie security hardening)
- **I133** (type hints) — incremental, no blocker

### Updated Tier 0

| # | Item | Effort | Impact | Dependencies |
|---|------|--------|--------|--------------|
| I43 | Component parameter sanitization (XSS) | Low | **Critical** | None |
| I57 + I132 | Cookie security hardening + stale cookie cleanup | Low | **Critical** | None |
| I58 | localStorage graceful degradation | Low | High | None |
| I4 + I48 | Static asset versioning + URL resolution | Low | High | None |
| I120 | ThemeManager.toggle_mode() race condition | Low | High | None — data corruption in concurrent sessions |
| I122 | ThemeMixin._skip_render initialization | Low | High | None — latent AttributeError crash |
| I121 | Module-level logger setup | Low | Low | None — do alongside other Tier 0 fixes |

### Updated Tier 1 Additions

| # | Item | Effort | Impact | Dependencies |
|---|------|--------|--------|--------------|
| I123 | Anti-FOUC script DRY extraction | Low | Medium | Do with I1 — both eliminate inline HTML duplication |
| I126 | Template tag parameter validation | Low | Medium | Do with I27 — test harness defines valid param contracts |
| I129 | CSS custom property fallback values | Low | Medium | Do with I2 — component CSS restructure is the right moment |
| I130 | push_event availability warning | Low | Medium | Do with I88 — standalone mode awareness |
| I124 | Silent theme pack fallback logging | Low | Medium | Do with I5/I24 — CSS generation path consolidation |
