# Changelog

All notable changes to djust-theming will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
