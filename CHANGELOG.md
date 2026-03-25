# Changelog

All notable changes to djust-theming will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Reduced motion, high contrast, and print stylesheet (Phase 7.4 + 7.5 + 7.6)** -- Three accessibility and print features. **Reduced motion (7.4):** New `get_reduced_motion_css()` function in `djust_theming.design_tokens` generates a `@media (prefers-reduced-motion: reduce)` block that overrides all duration tokens (`--duration-fast`, `--duration-normal`, `--duration-slow`, `--duration-slower`) to `0ms` and forces `animation-duration: 0.01ms !important`, `animation-iteration-count: 1 !important`, `transition-duration: 0.01ms !important`, `scroll-behavior: auto !important` on all elements. Automatically included in `generate_design_tokens_css()` and `generate_design_tokens_classes_css()` output. **High contrast (7.5):** New `get_high_contrast_css()` function generates a `@media (prefers-contrast: more)` block that introduces `--border-width: 2px`, `--ring-width: 3px`, `--ring-offset: 3px` tokens, forces `border-style: solid` on all elements, enhances `:focus-visible` outlines with the ring token, and increases border width on `.btn`, `.card-theme`, `.input-theme`, and badge components. **Print stylesheet (7.6):** New `djust_theming/static/djust_theming/css/print.css` with `@media print` rules that hide `.sidebar`, `.navbar`, `.theme-switcher`, `.theme-mode-btn`, `.theme-preset-select`, `.toast`, `.modal-overlay`, and `button[type="button"]`; force white background and black text; remove `box-shadow`, `text-shadow`, animations, and transitions; display link URLs via `a[href]::after { content: " (" attr(href) ")" }`; control page breaks (`page-break-after: avoid` on headings, `page-break-inside: avoid` on images/cards/tables); and expand main content to full width. `theme_head.html` now includes `<link rel="stylesheet" href="print.css" media="print">`. 22 new tests.

- **RTL support (Phase 7.1 + 7.2 + 7.3)** -- Full right-to-left language support. **Logical properties (7.1):** All directional CSS properties across `base.css`, `components.css`, `layouts.css`, and `pages.css` converted to CSS logical properties: `margin-left`/`margin-right` to `margin-inline-start`/`margin-inline-end`/`margin-inline`, `padding-left`/`padding-right` to `padding-inline`, `border-left`/`border-right` to `border-inline-start`/`border-inline-end`, `left`/`right` positioning to `inset-inline-start`/`inset-inline-end`, `text-align: left` to `text-align: start`. Utility classes (`.me-*`, `.ms-*`, `.mx-*`, `.px-*`, `.start-0`, `.end-0`) updated accordingly. **Direction config (7.2):** New `direction` config option in `DEFAULT_CONFIG` (default `"auto"`). Accepts `"ltr"`, `"rtl"`, or `"auto"`. Auto mode detects RTL from Django's `LANGUAGE_CODE` against a built-in set of RTL language codes (Arabic, Hebrew, Farsi, Urdu, Pashto, Sindhi, Kurdish, Yiddish, Divehi, Uyghur). New `get_direction()` function in `djust_theming.manager` and `RTL_LANGUAGES` constant. `theme_head.html` now sets `dir` attribute on `<html>` element via the anti-FOUC script. `ThemeManifest` gains optional `direction` field in `[theme]` section for per-theme direction override, included in `from_toml()` parsing and `to_toml()` serialization. **RTL-aware components (7.3):** `[dir="rtl"]` CSS overrides in `base.css` for sidebar active indicator, nav-link underline animation, and toast slide animations (reversed `translateX`). `[dir="rtl"]` overrides in `components.css` for breadcrumb separator flip (`scaleX(-1)`), theme preset select dropdown arrow position, pagination prev/next arrow flip, and progress bar indeterminate animation reversal. 71 new tests.

### Added
- **Django form integration (Phase 6)** -- New `ThemeFormRenderer` (`djust_theming.forms.ThemeFormRenderer`) subclasses Django's `DjangoTemplates` renderer, overriding widget templates to inject theme CSS classes automatically. When configured as `FORM_RENDERER = "djust_theming.forms.ThemeFormRenderer"` in settings, all `{{ form }}` and `{{ form.as_div }}` output uses themed templates. **Widget templates (6.2):** 18 Django widget template overrides in `djust_theming/form_templates/django/forms/widgets/` add `theme-input`, `theme-textarea`, `theme-select`, `theme-checkbox`, `theme-radio`, `theme-file-input` CSS classes to their respective widgets. Covers text, email, password, number, URL, date, search, tel, textarea, select, checkbox, radio, and file inputs. Hidden inputs are intentionally excluded. Form-level templates override `div.html` (wraps fields in `theme-form-group` divs), `field.html` (applies `theme-label` to labels and `theme-help-text` to help text), and `errors/list/ul.html` (adds `theme-field-errors` class). All templates respect `css_prefix` via `{% get_css_prefix %}` tag. **{% theme_form %} tag (6.3):** New `theme_form_tags` template tag library with `{% theme_form form %}` for rendering complete themed forms. Supports three layouts: `stacked` (default, label above field), `horizontal` (label and field side by side), `inline` (all fields in a row). Renders each visible field with label (`theme-label`), help text (`theme-help-text`), widget, and field-level errors (`theme-field-error` with `role="alert"`). Hidden fields appended at end. `{% theme_form_errors form %}` standalone tag renders form-level non-field errors as a destructive alert. `{% get_css_prefix %}` exposes the configured CSS prefix for use in templates. **Error display (6.4):** Form-level non-field errors rendered as `theme-form-errors alert alert-destructive` div with error list. Field-level errors rendered as inline `theme-field-error` spans with `role="alert"` for accessibility. Template fragments at `djust_theming/forms/form_errors.html` and `field_errors.html` for standalone use. 57 new tests.

### Added
- **`create-package` management command (Phase 5.3)** -- New `python manage.py djust_theme create-package <name>` subcommand generates a pip-installable theme package scaffold. Produces a complete Python package directory (`djust-theme-<name>/`) with `pyproject.toml` (build metadata, `djust-theming>=0.3.0` dependency), `README.md` (installation and `INSTALLED_APPS` instructions), `LICENSE` (MIT), and a Python package (`djust_theme_<name>/`) containing `__init__.py`, `theme.toml` (via `ThemeManifest.to_toml()`), `tokens.css` (CSS custom property override template), a `templates/djust_theming/themes/<name>/components/` directory for component template overrides, and `static/djust_theme_<name>/css/` + `fonts/` directories for assets. Supports `--author`, `--preset`, `--design-system`, `--dir` (output location), and `--force` (overwrite). Validates package name (lowercase alphanumeric + hyphens), preset, and design system against the registry. 27 new tests.
- **Template variants for 5 design systems (Phase 5.1)** -- Material, iOS, Fluent, Neo-Brutalist, and Playful design systems now ship HTML-different template overrides for button and card components. Material adds a `btn-ripple` overlay span and `card-elevated` class. iOS adds `btn-sf` class and `card-grouped` style, plus a `segmented-control` tabs variant that replaces tab buttons with segment buttons. Fluent adds `btn-reveal` highlight wrapper and `card-acrylic` backdrop. Neo-Brutalist wraps buttons in `btn-offset` shadow container and cards in `card-border-thick` container. Playful wraps buttons in `btn-bounce` animation wrapper and adds decorative SVG corner elements to cards via `card-decorated`. The other 6 design systems (Minimalist, Corporate, Retro, Elegant, Organic, Dense) inherit default templates -- CSS-only differences. All variants preserve the same context variable contract (`css_prefix`, `variant`, `size`, `text`, `slot_*`). Templates live at `djust_theming/templates/djust_theming/themes/{design_system}/components/{component}.html` and are resolved automatically by the existing `select_template` fallback chain. 11 new template files.
- **Installable theme package discovery (Phase 5.2)** -- `ThemeRegistry._load_theme_package()` now auto-detects a `templates/` directory in pip-installed theme packages and stores it as `ThemeManifest.templates_dir`. New `djust_theming.loaders.ThemePackageLoader` (a Django filesystem template loader subclass) dynamically includes template directories from all registered theme packages, enabling `{% theme_button %}` to resolve theme-specific templates from third-party packages without requiring them in `INSTALLED_APPS`. New `get_installed_template_dirs()` helper returns all package template directories from the registry. 81 new tests (55 for template variants, 26 for installable packages).

### Added
- **9 page templates + `theme_pages` tag library (Phase 4)** -- New `theme_pages` template tag library with 9 page-level tags that render complete page fragments composing existing components (card, input, button, checkbox). **Auth pages** (4): `theme_login_page` renders a login form with email/password inputs, remember-me checkbox, forgot-password link, social login slot (`slot_social`), and register link; `theme_register_page` renders a registration form with name/email/password/confirm inputs, terms checkbox, and sign-in link; `theme_password_reset_page` renders an email-only form with description text and back-to-login link; `theme_password_confirm_page` renders new-password + confirm inputs. All auth forms use `method="post"`, configurable `action` URL, and proper `<label>` associations. **Error pages** (3): `theme_404_page`, `theme_500_page`, and `theme_403_page` render large error code display, heading, description, and action buttons (Go home, Try again, Go back). 404 supports `slot_illustration`. 500 supports optional `retry_url`. **Utility pages** (2): `theme_maintenance_page` renders a maintenance notice with `slot_illustration`, `slot_eta`, and `slot_progress` for countdown/progress display; `theme_empty_state_page` renders a placeholder with `slot_icon` and optional CTA button (`cta_text` + `cta_url`). All pages support `css_prefix`, theme-specific template overrides via `resolve_page_template()` (`djust_theming/themes/{theme}/pages/{page}.html` -> `djust_theming/pages/{page}.html`), and follow the same tag pattern as components. New `pages.css` static file with `@layer components` provides structural styles for all page patterns. 106 new tests.

### Added
- **4 navigation components (Phase 3.3)** -- `theme_nav`, `theme_sidebar_nav`, `theme_nav_item`, and `theme_nav_group` template tags with full contract definitions, slot support, and accessibility attributes. `theme_nav_item` renders an `<a>` link with `.nav-link` class, auto-detects active state from `request.path` (or accepts explicit `active` bool), adds `aria-current="page"` when active, and supports `slot_icon`/`slot_badge`. `theme_nav_group` renders a `<details>/<summary>` collapsible group with `.sidebar-title` heading and `.sidebar-menu` items container, expanded by default, with `slot_label`/`slot_items`. `theme_nav` renders a horizontal `<nav role="navigation" aria-label="Main">` bar with `.navbar` class, optional brand text, items list, and `slot_brand`/`slot_items`/`slot_actions`. `theme_sidebar_nav` renders a vertical `<nav role="navigation" aria-label="Sidebar">` with `.sidebar` class, sectioned layout with `.sidebar-title` headings and `.sidebar-item` links, `data-theme-sidebar-collapse` attribute for JS-driven collapse, and `slot_header`/`slot_sections`/`slot_footer`. All components use existing CSS classes from `base.css` (`.navbar`, `.navbar-inner`, `.navbar-brand`, `.navbar-nav`, `.navbar-actions`, `.nav-link`, `.sidebar`, `.sidebar-title`, `.sidebar-menu`, `.sidebar-item`), follow theme-aware template resolution, support `css_prefix`, and have contract-driven test coverage. 62 new tests.

### Added
- **7 layout templates (Phase 3.1 + 3.2)** -- `base.html`, `sidebar.html`, `topbar.html`, `sidebar_topbar.html`, `centered.html`, `dashboard.html`, and `split.html` in `djust_theming/templates/djust_theming/layouts/`. Base provides the root HTML document with `{% theme_head %}`, viewport meta, and `layouts.css` include; defines blocks `page_title`, `head_extra`, `body_class`, `content`, `footer`, `extra_css`, `extra_js`. Sidebar provides fixed sidebar + scrollable main (blocks: `sidebar`, `sidebar_content`). Topbar provides sticky top navigation + content below (blocks: `topbar`, `topbar_content`). Sidebar-topbar combines both patterns (blocks: `sidebar`, `topbar`, `sidebar_topbar_content`). Centered provides a max-width centered column for auth/landing pages (block: `centered_content`). Dashboard extends sidebar-topbar with a responsive grid content area (block: `dashboard_content`). Split provides a two-panel list+detail layout (blocks: `panel_left`, `panel_right`). All layouts use Django template inheritance, apply `.layout-*` CSS classes, collapse to single-column on mobile via media queries, and participate in theme-specific template override resolution via `resolve_layout_template()`.
- **Responsive layout tokens (Phase 3.4)** -- New `get_layout_tokens()` function in `djust_theming.design_tokens` generates CSS custom properties for responsive breakpoints (`--breakpoint-sm/md/lg/xl` at 640/768/1024/1280px) and structural dimensions (`--sidebar-width: 280px`, `--sidebar-collapsed-width: 64px`, `--topbar-height: 56px`). Tokens are included in `generate_design_tokens_root_css()` output.
- **Layout CSS (`layouts.css`)** -- New static CSS file at `djust_theming/static/djust_theming/css/layouts.css` wrapped in `@layer base`. Contains structural styles for all 7 layout patterns with responsive media queries for mobile collapse. Automatically included by the base layout template.
- **Layout template resolution** -- New `_get_layout_candidates()` and `resolve_layout_template()` in `djust_theming.template_resolver` enable theme-specific layout overrides following the same fallback chain as components (`themes/{theme}/layouts/{name}.html` -> `layouts/{name}.html`).
- 63 new tests covering layout tokens, template existence, inheritance chains, block presence, CSS class application, CSS file contents, and theme head inclusion.

### Added
- **6 new utility components (Phase 2.1 Batch 2b)** -- `theme_breadcrumb`, `theme_avatar`, `theme_toast`, `theme_progress`, `theme_skeleton`, and `theme_tooltip` template tags with full contract definitions, slot support, and accessibility attributes. Breadcrumb renders `<nav aria-label="Breadcrumb">` with `<ol>` of linked segments, last item marked `aria-current="page"`, and `slot_separator` for custom separators. Avatar supports `src` image with `alt` text or automatic initials fallback from `name`, three sizes (sm/md/lg), and `slot_image`/`slot_fallback`. Toast provides fixed-position notifications with variant (success/warning/error/info), position variants (top-right, top-left, bottom-right, bottom-left), `data-theme-toast`/`data-duration` for JS auto-dismiss, `role="status"` + `aria-live="polite"`, close button, and `slot_message`/`slot_actions`. Progress renders `role="progressbar"` with `aria-valuenow`/`aria-valuemin`/`aria-valuemax`, determinate (percentage bar) vs indeterminate (animated) modes, and `slot_label`. Skeleton provides loading placeholders with three variants (text/circle/rect), configurable width/height, CSS shimmer animation, and `aria-hidden="true"`. Tooltip is CSS-only via `[data-tooltip]` attribute + `::after` pseudo-element with four position variants (top/bottom/left/right) and `slot_content`. All components follow existing patterns: theme-aware template resolution, `css_prefix` support, `_extract_slots()` helper, and contract-driven test harness. 83 new tests.

### Added
- **4 new form components (Phase 2.1 Batch 2a)** -- `theme_select`, `theme_textarea`, `theme_checkbox`, and `theme_radio` template tags with full contract definitions, slot support, and accessibility attributes. Select provides native `<select>` with options list, placeholder, `slot_label`/`slot_select`/`slot_help_text`/`slot_error`. Textarea supports configurable rows, placeholder, `slot_label`/`slot_textarea`/`slot_help_text`/`slot_error`. Checkbox renders `<input type="checkbox">` with label and description, `slot_label`/`slot_description`. Radio renders a `<fieldset role="radiogroup">` with `<legend>`, per-option radio inputs with associated labels, and `slot_label`/`slot_options`. All components follow existing patterns: theme-aware template resolution, `css_prefix` support, `_extract_slots()` helper for slot passthrough via `**attrs`, and contract-driven test harness. 67 new tests.

### Added
- **5 new interactive components (Phase 2.1 Batch 1)** -- `theme_modal`, `theme_dropdown`, `theme_tabs`, `theme_table`, and `theme_pagination` template tags with full contract definitions, slot support, and accessibility attributes. Modal supports backdrop click/ESC dismissal with `data-theme-modal-open`/`data-theme-modal-close` triggers, size variants (sm/md/lg), and `slot_header`/`slot_body`/`slot_footer`/`slot_close`. Dropdown provides trigger+menu with `role="menu"`, `aria-haspopup`, `aria-expanded`, keyboard navigation, and `slot_trigger`/`slot_menu`. Tabs implement `role="tablist"`/`role="tab"`/`role="tabpanel"` with `aria-selected`, `aria-controls`/`aria-labelledby`, and ArrowLeft/Right keyboard navigation. Table wraps responsive scrollable container with striped/hover variants and `slot_caption`/`slot_header`/`slot_body`/`slot_footer`. Pagination generates page links with `aria-label="Pagination"`, `aria-current="page"`, edge detection with ellipsis, and `slot_prev`/`slot_next`. All components follow existing patterns: theme-aware template resolution, `css_prefix` support, and contract-driven test harness. 69 new tests.
- **`components.js` behavior layer** -- Thin (~4KB) IIFE script that auto-initializes modals, dropdowns, and tabs via `data-theme-*` attribute hooks on `DOMContentLoaded`. Handles ESC-to-close modals, click-outside-to-close dropdowns, and Arrow key tab navigation. Re-initializes on `djust:dom-update` for djust LiveView compatibility. Included automatically via `{% theme_head %}`. Exposed as `window.djustComponents` for manual re-init.

### Added
- **Component slot system (Phase 2.2 / I11)** -- All 5 component templates (`button.html`, `card.html`, `alert.html`, `badge.html`, `input.html`) now support composable slot variables for overriding default content sections. Button supports `slot_icon`, `slot_content`, and `slot_loading`; Card supports `slot_header`, `slot_body`, and `slot_footer`; Alert supports `slot_icon`, `slot_message`, `slot_actions`, and `slot_dismiss`; Badge supports `slot_content`; Input supports `slot_label`, `slot_input`, `slot_help_text`, and `slot_error`. Slot values are rendered with `|safe` to allow HTML content. When no slot variable is provided, the original default rendering is used -- fully backward compatible.
- **Component contracts (`djust_theming.contracts`)** -- New module defining machine-readable contracts for each component: required/optional context variables, required HTML elements, accessibility requirements (e.g. `role="alert"`, `for` attribute on labels), and available slot names. Contracts are exposed as `ComponentContract` dataclasses in `COMPONENT_CONTRACTS` dict.
- **Component test harness (I27)** -- New `ComponentTestCase` base class in `tests/component_test_base.py` with helpers for rendering components and asserting HTML structure: `render_component()`, `assert_has_element()`, `assert_has_class()`, `assert_contains()`, `assert_not_contains()`, `assert_accessible()`, and `assert_contract()`. Uses stdlib `html.parser` for lightweight HTML assertion parsing. 57 new tests cover contracts, slots, accessibility, backward compatibility, and rendering for all 5 components.

### Added
- **Critical CSS Inlining (I10)** — CSS output is now split into critical (inlined) and deferred (async-loaded) parts for faster first paint. Critical CSS (~2-4KB) includes `@layer` declarations, CSS custom properties/tokens, dark mode selectors, system preference media queries, and theme variables (typography, spacing, shadows). Deferred CSS (base styles, utility classes, typography classes, component styles) is loaded asynchronously via `<link rel="preload" as="style">` with a `<noscript>` fallback. New config option `LIVEVIEW_CONFIG["theme"]["critical_css"]` (default `True`); set to `False` to restore legacy behavior (all CSS in one block). New functions `generate_critical_css_for_state()` and `generate_deferred_css_for_state()` in `djust_theming.manager` (and exported from top-level package). New `ThemeCSSGenerator.generate_critical_css()` / `generate_deferred_css()` and `CompleteThemeCSSGenerator.generate_critical_css()` / `generate_deferred_css()` methods. New `/deferred.css` view endpoint with ETag and Cache-Control headers. Updated `theme_head.html` template and `{% theme_head %}` tag.
- **Theme Registry (Phase 1.4)** — New `ThemeRegistry` singleton in `djust_theming.registry` serves as the single source of truth for all registered presets, design systems, and theme manifests. Thread-safe with `threading.Lock`. Populated during `AppConfig.ready()` via `discover()`, which loads built-in presets from `THEME_PRESETS`, built-in design systems from `DESIGN_SYSTEMS`, pip-installed theme packages from the `DJUST_THEMES` setting, and `theme.toml` manifests from the configured `themes_dir`. Third-party apps can call `get_registry().register_preset()` / `get_registry().register_theme()` in their own `ready()`. Exported from top-level package as `ThemeRegistry` and `get_registry`.
- **`validate-theme` management command (Phase 1.5)** — New `python manage.py djust_theme validate-theme <name>` subcommand validates a theme manifest and its referenced files. Checks include: TOML parsing, required fields, name format, preset/design system existence in registry, static file existence (CSS and fonts), and token override key validation against `ThemeTokens` dataclass fields. Supports `--all` to validate all themes in the themes directory and `--dir` to override the themes directory. Prints structured pass/fail results with error/warning severity.

### Changed
- **All consumers rewired to ThemeRegistry** — `ThemeManager`, `checks.py` (E002/E003/W001), `manifest.py` `validate()`, and all management command subcommands now use `get_registry()` for preset and design system lookups instead of importing `THEME_PRESETS` and `DESIGN_SYSTEMS` dicts directly. Existing dicts remain as authoritative initial data sources read by the registry during discovery.

### Added
- **Theme manifest system (Phase 1.2)** — New `ThemeManifest` dataclass in `djust_theming.manifest` for parsing, validating, and serializing `theme.toml` files. Supports `[theme]`, `[extends]`, `[tokens]`, `[tokens.overrides]`, and `[static]` sections. Validates theme names against `[a-z0-9-]` pattern to prevent path traversal, and validates preset/design_system references against registered `THEME_PRESETS` and `DESIGN_SYSTEMS`. Uses `tomllib` (stdlib 3.11+) with `tomli` fallback for Python 3.10. Includes `load_theme_manifests()` discovery function. `ThemeManifest` is exported from the top-level `djust_theming` package.
- **`create-theme` scaffold command (Phase 1.3)** — New `python manage.py djust_theme create-theme <name>` subcommand that scaffolds a complete theme directory with `theme.toml`, `tokens.css` template, and subdirectories (`components/`, `layouts/`, `pages/`, `static/css/`, `static/fonts/`) with `.gitkeep` files. Supports `--preset`, `--design-system`, `--base`, `--dir`, and `--force` options. Theme name validation rejects invalid characters and path traversal attempts. Refuses to overwrite existing themes unless `--force` is provided.
- **`themes_dir` configuration key** — New `themes_dir` key in `DEFAULT_CONFIG` (`manager.py`), defaulting to `'themes/'` relative to `settings.BASE_DIR`. Used by `create-theme` to determine where to scaffold new themes.

### Added
- **Template namespace resolution (Phase 1.1)** — All component template tags now support theme-specific template overrides. When a design system theme is active (e.g. `material`), the framework first looks for `djust_theming/themes/{theme_name}/components/{component}.html` before falling back to the default `djust_theming/components/{component}.html`. This uses Django's `select_template()` for zero-overhead fallback. New `djust_theming.template_resolver` module provides `resolve_component_template()` and `resolve_theme_template()` helpers. All 5 component tags (`theme_button`, `theme_card`, `theme_badge`, `theme_alert`, `theme_input`) and `theme_switcher` have been converted from `@register.inclusion_tag` to `@register.simple_tag(takes_context=True)` to support dynamic template resolution. The `ThemeSwitcher`, `ThemeModeButton`, and `PresetSelector` Python classes also use the same resolution chain. Existing templates and behavior are fully preserved -- the default template always ships with the package.
- **CSS Cascade Layers (I9)** — All generated CSS is now wrapped in `@layer` declarations for predictable specificity ordering. Layer order: `@layer base, tokens, components, theme;`. Color variables and design tokens go in `@layer tokens`, base styles in `@layer base`, utility classes and component styles in `@layer components`. Theme authors can use `@layer theme { ... }` to override anything without `!important`. The static `components.css` file is also wrapped in `@layer components`. Theme pack CSS wraps pack-specific additions (icons, animations, patterns, interactions, illustrations) in `@layer theme`. Two new config options: `LIVEVIEW_CONFIG["theme"]["use_css_layers"]` (default `True`) and `LIVEVIEW_CONFIG["theme"]["css_layer_order"]` (default `"base, tokens, components, theme"`). Set `use_css_layers` to `False` to disable layer wrapping for backward compatibility.

### Added
- **`generate_css_for_state()` convenience function (I24)** — New `generate_css_for_state(state, css_prefix="")` function in `djust_theming.manager` (and exported from `djust_theming`) consolidates the pack-or-theme CSS generation logic that was previously duplicated across 5 call sites (template tags, views, context processors, and ThemeMixin). Accepts a `ThemeState` and optional `css_prefix`, tries the pack CSS generator first (if `state.pack` is set), then falls back to the theme CSS generator. A companion `get_css_prefix()` helper returns the configured `css_prefix` from `LIVEVIEW_CONFIG`. Both are exported from the top-level package.

### Fixed
- **ThemeMixin now supports theme packs (I24)** — `ThemeMixin._setup_theme_context()` previously called `generate_theme_css()` directly, ignoring `state.pack` entirely. It now uses the centralized `generate_css_for_state()`, which correctly tries pack CSS first before falling back to theme CSS.

### Changed
- **AppConfig system checks for misconfigurations (I23)** — Three new Django system checks catch configuration errors at startup: `E001` verifies `djust_theming.context_processors.theme_context` is in at least one TEMPLATES backend's `context_processors` list, `E002` validates `LIVEVIEW_CONFIG['theme']['preset']` against registered `THEME_PRESETS` keys, and `E003` validates `LIVEVIEW_CONFIG['theme']['theme']` against registered `DESIGN_SYSTEMS` keys. All three are errors (not warnings) since they indicate broken configuration that will cause runtime failures.
- **Brand Color Auto-Palette Generator (I21)** — New `PaletteGenerator` class that derives a complete `ThemePreset` (light + dark modes, all 31 color fields) from 1-3 brand colors. Supports 4 generation modes (`professional`, `playful`, `muted`, `vibrant`) that control saturation, hue offsets, and border radius. Automatically derives secondary (complementary) and accent (analogous) colors when not provided. All foreground/background pairs are validated against WCAG AA contrast ratios (4.5:1 for text, 3:1 for UI borders) with automatic lightness adjustment when contrast is insufficient. Usage: `PaletteGenerator.from_brand_colors("#3b82f6", mode="vibrant")`. Exported from the top-level `djust_theming` package.
- **CSS namespace prefixing (I17)** — New `css_prefix` option in `LIVEVIEW_CONFIG["theme"]` allows prefixing all component CSS class names (e.g. `.btn` becomes `.dj-btn`) to avoid collisions with Bootstrap, Bulma, or other CSS frameworks. Default is `""` (empty string) for full backward compatibility. When a prefix is set, `{% theme_head %}` renders component CSS inline with prefixed selectors instead of linking the static `components.css` file. All component templates (`button.html`, `card.html`, `alert.html`, `badge.html`, `input.html`, `theme_switcher.html`) use `{{ css_prefix }}` for class names. A new system check (`djust_theming.W002`) warns if the prefix does not end with `-`.
- **Color format interoperability (I16)** — New `djust_theming.colors` module with 6 pure conversion functions: `hsl_to_rgb`, `rgb_to_hsl`, `hex_to_rgb`, `rgb_to_hex`, `hex_to_hsl`, `hsl_to_hex`. All functions are exported from the top-level package. `ColorScale` gains 5 new methods: `to_hex()`, `to_rgb()`, `to_rgb_func()` for output, and `from_hex()`, `from_rgb()` class methods for construction from hex/RGB values. The existing `hsl_to_rgb` in `AccessibilityValidator` now delegates to the shared `colors` module, eliminating duplicated color math.

### Deprecated
- **`themes.py` module deprecated in favor of `theme_packs.py` (I8)** — The `THEMES` dict, `get_theme()`, and `list_themes()` in `djust_theming.themes` now emit `DeprecationWarning` on every access. Use `DESIGN_SYSTEMS`, `get_design_system()`, and `get_all_design_systems()` from `djust_theming.theme_packs` instead. The old module still works and will continue to work for the remainder of the 1.x series, but will be removed in 2.0. See the [migration guide](djust_theming/docs/customization.md#migrating-from-themes-to-design_systems) for details.

### Changed
- **`ThemeManager` validates against `DESIGN_SYSTEMS` (I8)** — `ThemeManager.get_state()` and `ThemeManager.set_theme()` now validate theme names against `DESIGN_SYSTEMS` from `theme_packs.py` instead of the deprecated `THEMES` dict from `themes.py`. Both registries contain the same 11 keys, so this is a non-breaking change.

### Added
- **Accessibility contrast validation system check (I6)** — A new Django system check (`djust_theming.W001`) validates all registered `THEME_PRESETS` against WCAG AA contrast ratios (4.5:1) at startup. Checks 12 foreground/background token pairs across both light and dark modes for every preset. Issues are reported as warnings so projects are informed but never blocked. Silence individual warnings with Django's `SILENCED_SYSTEM_CHECKS` setting.

### Fixed
- **Bug fix in `AccessibilityValidator.hsl_to_rgb()`** — Fixed `AttributeError` where the method accessed `color_scale.l` instead of the correct `color_scale.lightness` attribute on `ColorScale` objects.
- **Missing fields in high-contrast presets** — All `HIGH_CONTRAST_PRESETS` and `create_high_contrast_tokens()` now include the 8 extension fields (`info`, `link`, `code`, `selection` + foregrounds) that were missing since 1.1.0, preventing `TypeError` on import.
- **Missing fields in shadcn importer** — `_parse_shadcn_vars()` now parses the 8 extension color tokens, preventing `TypeError` when importing shadcn themes.

### Changed
- **Token boundary cleanup (I7)** — `ThemeTokens` now contains **color tokens only**. The `radius` field has moved from `ThemeTokens` to `ThemePreset`, and four animation fields (`card_lift_distance`, `card_glow_opacity`, `transition_speed`, `animation_intensity`) have been removed entirely.
  - **Breaking: Python API** — `ThemeTokens.radius` no longer exists. Use `ThemePreset.radius` instead. `ThemeTokens.card_lift_distance`, `.card_glow_opacity`, `.transition_speed`, and `.animation_intensity` have no replacement.
  - **Breaking: CSS output** — The CSS custom properties `--card-lift-distance`, `--card-glow-opacity`, `--transition-speed`, and `--animation-intensity` are no longer emitted. If your CSS references these variables, remove those references or define the variables in your own stylesheet. These variables had no internal consumers.
  - **Non-breaking: `--radius`** — The `--radius` CSS variable is still emitted in `:root` with the same values as before. It now appears once (in `:root`) instead of being duplicated in `.dark` and `prefers-color-scheme` blocks.
  - **shadcn import/export** — Radius is now read from/written to `ThemePreset.radius`. The shadcn JSON format is unchanged.
- **CSS generation caching with `lru_cache` (I5)** — All four CSS generation convenience functions (`generate_theme_css` in `css_generator.py` and `theme_css_generator.py`, `generate_pack_css` in `pack_css_generator.py`, `generate_design_system_css` in `design_system_css.py`) are now decorated with `@lru_cache`. Every call site (views, context processors, template tags, `ThemeMixin`) has been refactored to use the cached functions instead of instantiating generator classes directly. After the first call for a given `(theme_name, color_preset)` combination, subsequent calls return the cached string in ~0.001ms instead of rebuilding CSS from scratch. A new `clear_css_cache()` utility (exported from the top-level package) calls `.cache_clear()` on all cached functions for development use. Thread-safe, memory-bounded, zero breaking changes.
- **Static asset versioning via Django staticfiles (I4)** — Replaced manual `?v=N` cache busters on `theme.js` with Django's `{% static %}` tag (in templates) and `staticfiles_storage.url()` (in Python). Fixes version mismatch where `theme_tags.py` used `v=2` and `mixins.py` used `v=3`. Static URLs now respect `STATIC_URL` and work with `ManifestStaticFilesStorage` for automatic content-hashed cache busting. Also resolves I48 (hardcoded `/static/` prefix).
- **Cache ThemeManager per request (I3)** — New `get_theme_manager(request)` helper caches a single `ThemeManager` instance on `request._djust_theme_manager` so that multiple template tags and context processors within the same request reuse one manager instead of creating separate instances. All internal call sites (`theme_tags`, `context_processors`, `views`, `ThemeMixin`) now use `get_theme_manager()`. `get_theme_manager` is exported from the top-level `djust_theming` package.
- **Extract component CSS from templates (I2)** — Inline `<style>` blocks removed from all 6 component templates (`alert.html`, `badge.html`, `button.html`, `card.html`, `input.html`, `theme_switcher.html`) and consolidated into a single static file `djust_theming/static/djust_theming/css/components.css`. Component templates are now pure HTML structure. The `{% theme_head %}` tag automatically includes `components.css` via a `<link>` tag.
  - **Migration note for theme authors**: If you have overridden a component template and kept its `<style>` block, you may now get duplicate CSS (your inline styles plus the new `components.css`). Remove the `<style>` block from your overridden template and either rely on `components.css` or provide your own static CSS file.
- **Decouple inline HTML from Python (I1)** — All UI rendering in `components.py`, `mixins.py`, and `theme_tags.py` now uses Django templates instead of Python f-strings
  - `ThemeModeButton` renders via `djust_theming/components/theme_mode_button.html`
  - `PresetSelector` renders via layout-specific templates (`preset_selector_dropdown.html`, `preset_selector_grid.html`, `preset_selector_list.html`)
  - `ThemeMixin._setup_theme_context()` renders `theme_head` and `theme_switcher` via shared templates (`theme_head.html`, `theme_switcher.html`)
  - `theme_head` template tag renders via `djust_theming/theme_head.html`
  - `theme_switcher.html` now supports a `liveview` context variable for `dj-click`/`dj-change` event bindings (LiveView) vs `data-djust-event` (vanilla Django)
- No changes to public API or rendered HTML output; these are internal refactors

## [1.1.2] - 2026-02-19

### Added
- 4 new presets: **Forest** (deep green), **Amber** (warm amber/gold terminal), **Slate** (minimal monochrome), **Nebula** (deep space violet)
- `animation_intensity` property on `ThemePreset` (`subtle`, `moderate`, `dramatic`) for per-preset animation tuning
- Pastel and neon presets use `animation_intensity="subtle"` for a calmer feel

## [1.1.1] - 2026-02-18

### Added
- **Natural 20** preset — dark-first Bloomberg Terminal-inspired theme with cyan accents
- **4 pastel presets**: Catppuccin Mocha, Rosé Pine, Tokyo Night, Nord — developer-editor inspired
- **3 neon presets**: Synthwave '84, Outrun (and additional iconic neon palette)

### Fixed
- Improved text contrast in `default` and `shadcn` presets for better readability
- Improved contrast across all original presets (blue, green, purple, orange, rose)

## [1.1.0] - 2026-02-17

### Added
- 🎨 **Comprehensive Design System Foundation**
- Design tokens module with spacing scale, typography hierarchy, and structural utilities
- 13 spacing tokens from 4px to 96px (`--space-1` to `--space-24`)
- 28 typography tokens (font sizes, line heights, font weights)
- Extended border radius tokens (`--radius-sm` to `--radius-full`)
- Transition timing tokens (durations and easing curves)
- Theme-aware shadow tokens that adapt to light/dark modes
- Animation keyframes (fadeIn, slideInFromRight, pulse, spin)

### Added - New Semantic Colors
- 8 new color tokens added to all theme presets (total: 31 color tokens)
- `--info` / `--info-foreground` - Informational states (blue)
- `--link` / `--link-hover` - Hyperlink colors with hover variant
- `--code` / `--code-foreground` - Code block backgrounds
- `--selection` / `--selection-foreground` - Text selection highlights

### Added - Utility Classes
- Typography classes: `.h1`-`.h6`, `.text-body`, `.text-small`, `.text-tiny`
- Interactive patterns: `.interactive`, `.link`, `.focus-ring`
- Layout utilities: `.truncate`, `.line-clamp-{2,3,4}`, `.custom-scrollbar`
- Animation classes: `.fade-in`, `.slide-in-right`, `.pulse`, `.spin`
- Color utilities: `.bg-info`, `.text-link`, `.border-info`, etc.

### Added - Default Component Styles
- Links automatically themed with `--link` and `--link-hover` colors
- Code blocks themed with `--code` background and `--code-foreground` text
- Text selection themed with `--selection` colors

### Added - Documentation
- `djust_theming/docs/design-system.md` - Comprehensive design system guide (469 lines)
- `djust_theming/docs/colors.md` - Complete color reference (425 lines)
- `djust_theming/docs/PHASE1-SUMMARY.md` - Implementation summary (883 lines)

### Changed
- ThemeCSSGenerator now includes design tokens by default (`include_design_tokens=True`)
- All theme presets updated with new semantic color values
- ColorScale dataclass: renamed `l` parameter to `lightness` for clarity (no breaking change in usage)

### Fixed
- Code formatting: split long font-family line for linting compliance

## [1.0.0] - 2026-02-04

### Added
- 🎉 **Production-ready release**
- Complete documentation and examples
- MIT License
- CHANGELOG
- PyPI-ready package configuration

### Changed
- Enhanced README with comprehensive feature overview
- Improved CLI help messages
- Better error handling across all modules

## [0.6.0] - 2026-02-04

### Added
- **CLI & DX Improvements**
- `djust-theme init` command for project setup
- `--with-tailwind` flag to generate Tailwind config during init
- `--with-examples` flag to generate example templates
- Interactive project initialization with validation
- Better CLI error messages and help text

### Changed
- Improved command-line interface user experience
- Enhanced documentation for CLI commands

## [0.5.0] - 2026-02-04

### Added
- **Component Library**
- `theme_button` - Themed button component with 5 variants
- `theme_card` - Card container with header/body/footer
- `theme_badge` - Status badge with 6 variants
- `theme_alert` - Alert messages with dismissal support
- `theme_input` - Themed form input with labels
- `theme_icon` - SVG icon helper
- All components use theme CSS variables
- Automatic light/dark mode adaptation
- Tailwind CSS integration for components

### Changed
- Enhanced component styling system
- Improved accessibility for all components

## [0.4.0] - 2026-02-04

### Added
- **shadcn/ui Compatibility**
- `djust-theme shadcn-import` command
- `djust-theme shadcn-export` command
- Parse shadcn theme JSON format
- Export djust presets to shadcn format
- 100% format compatibility with shadcn/ui
- Round-trip import/export without data loss

### Changed
- Enhanced theme format to match shadcn/ui specifications
- Updated documentation with shadcn integration examples

## [0.3.0] - 2026-02-04

### Added
- **Tailwind CSS Integration**
- `generate_tailwind_config()` function
- `djust-theme tailwind-config` command
- Export theme colors as Tailwind config
- Support for `@apply` with theme colors
- `djust-theme export-colors` command
- `djust-theme generate-examples` command for @apply patterns
- Automatic CSS variable mapping for Tailwind

### Changed
- Enhanced CLI with multiple subcommands
- Improved documentation with Tailwind examples

## [0.2.0] - 2026-02-04

### Added
- **djust LiveView Integration**
- `ThemeMixin` for LiveView classes
- Reactive theme switching without page reload
- Server-side state sync via WebSocket
- `push_event('theme_update')` for reactive CSS updates
- Compatible with djust-experimental
- Event handlers: `set_theme_mode`, `set_theme_preset`, `toggle_theme_mode`, `cycle_theme_preset`

### Fixed
- `{{ theme_head }}` now works in LiveView templates
- Theme context properly injected via ThemeMixin
- CSS hot-swapping for preset changes
- WebSocket event listener for `djust:push_event`

### Changed
- Updated JavaScript to listen for `djust:push_event` events
- Improved theme switching UX with instant updates

## [0.1.0] - 2026-02-03

### Added
- Initial release
- 7 built-in theme presets (Default, Shadcn, Blue, Green, Purple, Orange, Rose)
- Light/Dark/System mode support
- Anti-FOUC protection
- Django template tags: `{% theme_head %}`, `{% theme_switcher %}`, `{% theme_mode_toggle %}`
- Context processor for template variable injection
- Session + localStorage persistence
- Cookie-based preset for SSR
- 700+ utility classes in base.css
- HSL-based color system (shadcn/ui compatible)
- `ThemeManager` for state management
- `ThemeCSSGenerator` for CSS generation
- Complete design system with components

[1.1.2]: https://github.com/djust-org/djust-theming/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/djust-org/djust-theming/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/djust-org/djust-theming/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/djust-org/djust-theming/compare/v0.6.0...v1.0.0
[0.6.0]: https://github.com/djust-org/djust-theming/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/djust-org/djust-theming/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/djust-org/djust-theming/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/djust-org/djust-theming/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/djust-org/djust-theming/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/djust-org/djust-theming/releases/tag/v0.1.0
