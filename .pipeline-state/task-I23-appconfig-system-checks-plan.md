# I23: AppConfig System Checks - Implementation Plan

## Overview
Add three new Django system checks to catch misconfigurations at startup:
- **E001**: Missing `djust_theming.context_processors.theme_context` in TEMPLATES context_processors
- **E002**: Invalid preset name in `LIVEVIEW_CONFIG['theme']['preset']`
- **E003**: Invalid design system name in `LIVEVIEW_CONFIG['theme']['theme']`

## Existing Code Context

### checks.py (current)
- `check_preset_contrast` (W001) - validates WCAG AA contrast ratios for all presets
- `check_css_prefix` (W002/E004) - validates css_prefix format
- Both registered via `@register(Tags.compatibility)` and auto-imported in `apps.py` `ready()`

### manager.py
- `get_theme_config()` merges `LIVEVIEW_CONFIG['theme']` over `DEFAULT_CONFIG`
- `DEFAULT_CONFIG` has `"preset": "default"` and `"theme": "material"`

### presets.py
- `THEME_PRESETS` dict: 19 keys (default, shadcn, blue, green, purple, orange, rose, natural20, catppuccin, rose_pine, tokyo_night, nord, synthwave, cyberpunk, outrun, forest, amber, slate, nebula)

### theme_packs.py
- `DESIGN_SYSTEMS` dict: 11 keys (material, ios, fluent, playful, corporate, dense, minimalist, neo_brutalist, elegant, retro, organic)

## Implementation Details

### E001: Missing context_processor
- Check `django.conf.settings.TEMPLATES` for any backend that includes `djust_theming.context_processors.theme_context` in `OPTIONS.context_processors`
- Error level (not warning) because templates will fail without it
- Only check if `djust_theming` is in INSTALLED_APPS (it will be since the check runs from the app)

### E002: Invalid preset
- Read `LIVEVIEW_CONFIG['theme']['preset']` via `get_theme_config()`
- Validate against `THEME_PRESETS.keys()`
- Only fire if preset is explicitly set (not just the default)
- Actually, check the resolved config value against THEME_PRESETS keys

### E003: Invalid design system (theme)
- Read `LIVEVIEW_CONFIG['theme']['theme']` via `get_theme_config()`
- Validate against `DESIGN_SYSTEMS.keys()`
- Same approach as E002

## Test Plan (TDD)
File: `tests/test_checks.py` (extend existing)

### E001 tests:
1. `test_e001_fires_when_context_processor_missing` - TEMPLATES with no theme_context
2. `test_e001_passes_when_context_processor_present` - TEMPLATES with theme_context
3. `test_e001_passes_with_multiple_backends` - at least one backend has it
4. `test_e001_fires_when_templates_empty` - TEMPLATES = []

### E002 tests:
1. `test_e002_fires_on_invalid_preset` - preset="nonexistent"
2. `test_e002_passes_on_valid_preset` - preset="default"
3. `test_e002_passes_on_default_config` - no LIVEVIEW_CONFIG set

### E003 tests:
1. `test_e003_fires_on_invalid_design_system` - theme="nonexistent"
2. `test_e003_passes_on_valid_design_system` - theme="material"
3. `test_e003_passes_on_default_config` - no LIVEVIEW_CONFIG set

## Files to Modify
1. `djust_theming/checks.py` - add 3 new check functions
2. `tests/test_checks.py` - add test classes for E001, E002, E003
3. `CHANGELOG.md` - add entry under [Unreleased]
