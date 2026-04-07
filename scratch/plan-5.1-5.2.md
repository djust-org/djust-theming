# Plan: Phase 5.1+5.2 -- Theme Packs with Template Variants + Installable Packages

## Goal
1. Create template variants for 5 design systems (material, ios, fluent, neo_brutalist, playful) where HTML structure genuinely differs from the default.
2. Wire installable package discovery so `DJUST_THEMES = ["djust_theming_corporate"]` resolves the package's templates and adds them to the template resolver search path.
3. The other 6 design systems (minimalist, corporate, retro, elegant, organic, dense) remain CSS-only -- they inherit default templates.

## Current State
- `template_resolver.py` already builds a 2-candidate fallback chain: `themes/{theme}/components/{name}.html` -> `components/{name}.html`
- `registry.py` already has `_load_theme_package()` that imports a package and reads `get_theme_manifest()`, `PRESETS`, `DESIGN_SYSTEMS` -- but does NOT handle template directory injection.
- Component templates (button, card, tabs) are generic/flat HTML. No design-system-specific markup exists yet.

## Design

### 5.1: Template Variants (5 design systems x 2 components each = 10 templates)

**button.html variants** (all preserve the same context variables: css_prefix, variant, size, attrs, slot_loading, slot_icon, slot_content, text):
- `material/components/button.html` -- wraps content in a `<span class="{css_prefix}btn-ripple">` overlay for Material ripple effect
- `ios/components/button.html` -- adds `{css_prefix}btn-sf` class for SF Symbol-style weighting
- `fluent/components/button.html` -- wraps in `<span class="{css_prefix}btn-reveal">` for Fluent reveal-highlight
- `neo_brutalist/components/button.html` -- wraps in `<div class="{css_prefix}btn-offset">` for offset shadow container
- `playful/components/button.html` -- wraps in `<span class="{css_prefix}btn-bounce">` for bounce animation wrapper

**card.html variants**:
- `material/components/card.html` -- adds `{css_prefix}card-elevated` class for Material elevation
- `ios/components/card.html` -- adds `{css_prefix}card-grouped` class for iOS grouped-style
- `fluent/components/card.html` -- adds `<div class="{css_prefix}card-acrylic">` backdrop wrapper
- `neo_brutalist/components/card.html` -- wraps in `<div class="{css_prefix}card-border-thick">` with thick border container
- `playful/components/card.html` -- adds decorative corner SVGs via `{css_prefix}card-decorated` class

**tabs.html variant** (ios only -- segmented control is structurally different):
- `ios/components/tabs.html` -- renders as `<div class="{css_prefix}segmented-control">` with segment buttons instead of tab buttons

Template location: `djust_theming/templates/djust_theming/themes/{design_system}/components/{component}.html`

### 5.2: Installable Package Discovery

Enhance `registry._load_theme_package()` to:
1. After importing the package module, resolve its filesystem path via `importlib.resources.files(package_name)` (Python 3.9+) or `Path(mod.__file__).parent`
2. Check for `templates/` subdirectory in the package
3. Store the template directory path on the manifest (new `ThemeManifest.templates_dir` field)
4. Add a new function `get_package_template_dirs()` in `template_resolver.py` that queries the registry for all installed packages with template dirs
5. Enhance `_get_component_candidates()` to insert package template paths into the fallback chain:
   - `{pkg_templates_dir}/djust_theming/themes/{ds}/components/{component}.html`
   - `djust_theming/themes/{theme}/components/{component}.html` (local project override)
   - `djust_theming/components/{component}.html` (default)

Actually, simpler approach: Django's `APP_DIRS=True` already scans `templates/` in all installed apps. If the theme package is a proper Django app in `INSTALLED_APPS` and has `templates/djust_theming/themes/{name}/...`, select_template will find it automatically.

For packages that are NOT full Django apps (just listed in `DJUST_THEMES`), we need to:
1. Resolve the package's templates directory
2. Dynamically add it to Django's template dirs via the `DIRS` setting OR provide a custom template loader

**Chosen approach**: Store `templates_dir` on the registry per-package. Provide `get_installed_template_dirs()` that returns all package template dirs. Users add `djust_theming.template_loaders.ThemePackageLoader` to their TEMPLATES config, OR we document that theme packages should be added to INSTALLED_APPS.

**Simplest viable approach**: Enhance `_load_theme_package()` to detect `templates/` dir and store it. Provide a Django template engine `Loader` subclass (`ThemePackageLoader`) that adds those dirs. The loader is optional -- if packages are in INSTALLED_APPS, APP_DIRS handles it.

## File Changes

### New files:
1. `djust_theming/templates/djust_theming/themes/material/components/button.html`
2. `djust_theming/templates/djust_theming/themes/material/components/card.html`
3. `djust_theming/templates/djust_theming/themes/ios/components/button.html`
4. `djust_theming/templates/djust_theming/themes/ios/components/card.html`
5. `djust_theming/templates/djust_theming/themes/ios/components/tabs.html`
6. `djust_theming/templates/djust_theming/themes/fluent/components/button.html`
7. `djust_theming/templates/djust_theming/themes/fluent/components/card.html`
8. `djust_theming/templates/djust_theming/themes/neo_brutalist/components/button.html`
9. `djust_theming/templates/djust_theming/themes/neo_brutalist/components/card.html`
10. `djust_theming/templates/djust_theming/themes/playful/components/button.html`
11. `djust_theming/templates/djust_theming/themes/playful/components/card.html`
12. `djust_theming/loaders.py` -- ThemePackageLoader (Django template loader)
13. `tests/test_theme_variants.py` -- tests for template variants
14. `tests/test_installable_packages.py` -- tests for package discovery + loader

### Modified files:
1. `djust_theming/registry.py` -- enhance `_load_theme_package()` to detect and store template dirs
2. `djust_theming/manifest.py` -- add `templates_dir` field to ThemeManifest
3. `djust_theming/template_resolver.py` -- add `get_installed_template_dirs()` helper
4. `CHANGELOG.md` -- document changes

## Test Strategy (TDD)

### Test file: `tests/test_theme_variants.py`
1. Test that each of the 5 design systems has variant templates for button and card
2. Test that ios has a tabs variant
3. Test that variant templates contain the design-system-specific markup (ripple span, elevated class, etc.)
4. Test that `_get_component_candidates("material", "button")` returns the right paths
5. Test that `resolve_component_template()` with theme="material" resolves the material button variant
6. Test that the 6 CSS-only systems fall back to default templates

### Test file: `tests/test_installable_packages.py`
1. Test `_load_theme_package()` detects templates dir in a mock package
2. Test `_load_theme_package()` stores templates_dir on manifest
3. Test `ThemePackageLoader` returns template sources from registered package dirs
4. Test `get_installed_template_dirs()` returns dirs from registry
5. Test end-to-end: mock package with template -> resolves via loader
