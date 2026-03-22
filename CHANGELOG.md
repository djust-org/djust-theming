# Changelog

All notable changes to djust-theming will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
