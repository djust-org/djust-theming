# Changelog

All notable changes to djust-theming will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
