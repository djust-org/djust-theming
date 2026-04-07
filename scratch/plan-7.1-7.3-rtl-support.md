# Plan: Phase 7.1 + 7.2 + 7.3 -- RTL Support

## Overview

Add full RTL (right-to-left) support to djust-theming via:
1. **Logical properties (7.1)** -- Convert physical directional CSS properties to logical equivalents
2. **Direction config (7.2)** -- Add `direction` to DEFAULT_CONFIG with auto-detection from Django's LANGUAGE_CODE
3. **RTL-aware components (7.3)** -- Add `[dir="rtl"]` overrides for components with directional visual elements

## Audit Summary: Directional Properties Found

### base.css
- `.sidebar` `border-right` -> `border-inline-end`
- `.sidebar-item-count` `margin-left: auto` -> `margin-inline-start: auto`
- `.container` `padding-left/padding-right` -> `padding-inline`
- `.search-icon` `left: 12px` -> `inset-inline-start: 12px`
- `.search-input` `padding: ... 0.65rem 0.9rem 0.65rem 2.4rem` -> keep shorthand but fix padding-inline-start
- `.table th, .table td` `text-align: left` -> `text-align: start`
- `.alert-close` `margin-left: auto` -> `margin-inline-start: auto`
- `.toast-container` `right: var(--space-4)` -> `inset-inline-end: var(--space-4)`
- `.list-group-flush .list-group-item` `border-left/right: none` -> `border-inline: none`
- `.spinner-border` `border-right-color` -> `border-inline-end-color`
- `.me-*` utilities -> `margin-inline-end`
- `.ms-*` utilities -> `margin-inline-start`
- `.mx-*` utilities -> `margin-inline`
- `.px-*` utilities -> `padding-inline`
- `.end-0` `right: 0` -> `inset-inline-end: 0`
- `.start-0` `left: 0` -> `inset-inline-start: 0`
- `.nav-link::after` `left: 50%` / `left: 0` -> `inset-inline-start`
- `.sidebar-item::before` `left: 0` -> `inset-inline-start: 0`

### layouts.css
- `.layout-sidebar__aside` `border-right` -> `border-inline-end` (3 occurrences)
- Mobile fallbacks: `border-right: none` -> `border-inline-end: none` (3 occurrences)

### components.css
- `.modal-close` `right: 0.75rem; top: 0.75rem` -> `inset-inline-end: 0.75rem`
- `.dropdown-left` `left: 0` -> `inset-inline-start: 0`
- `.dropdown-right` `right: 0` -> `inset-inline-end: 0`
- `.dropdown-item` `text-align: left` -> `text-align: start`
- `.table caption` `text-align: left` -> `text-align: start`
- `.table th` `text-align: left` -> `text-align: start`
- `.breadcrumb-separator` `margin: 0 0.5rem` -> `margin-inline: 0.5rem`
- `.toast-top-right/bottom-right` `right` -> `inset-inline-end`
- `.toast-top-left/bottom-left` `left` -> `inset-inline-start`
- `.theme-preset-select` `padding: ... 2rem ... 0.75rem` -> directional padding
- `.theme-preset-select` `background-position: right 0.5rem center` -> keep with RTL override
- Tooltip `left/right` positions -> `inset-inline-start/end`

### pages.css
- `.page-error .page-description` `margin-left/right: auto` -> `margin-inline: auto`
- `.page-utility .page-description` same
- `.page-progress` same

### performance.css
- No directional properties to convert (all transforms/opacity)

## Direction Config (7.2)

### Changes to manager.py
- Add `"direction": "auto"` to `DEFAULT_CONFIG`
- Valid values: `"ltr"`, `"rtl"`, `"auto"`

### Changes to theme_head.html
- Set `dir` attribute on `<html>` element in the anti-FOUC script
- When "auto", detect from Django's `LANGUAGE_CODE`

### Changes to theme_tags.py
- Pass `direction` value to theme_head.html context
- Add `get_direction()` helper that resolves "auto" -> actual direction

### Changes to manifest.py
- Add optional `direction` field to `ThemeManifest` (from `[theme]` section)

### RTL language detection
- Maintain a set of RTL language codes: ar, he, fa, ur, ps, sd, ckb, yi, dv, ku, ug
- When direction is "auto", check `settings.LANGUAGE_CODE` prefix against this set

## RTL-Aware Components (7.3)

Add `[dir="rtl"]` CSS overrides in a new section at the end of each CSS file:

### base.css RTL section
- `.sidebar-item::before` flip from left to right
- `.nav-link::after` flip from left to right
- Toast slide animations: reverse translateX direction

### components.css RTL section
- `.breadcrumb-separator` content: consider flip via `transform: scaleX(-1)` if using arrow chars
- `.theme-preset-select` background-position flip
- `.modal-close` position flip (already handled by logical properties)
- Pagination prev/next arrows: `transform: scaleX(-1)` on SVG icons

### layouts.css RTL section
- Not needed if logical properties are used correctly

## Test Plan

### test_rtl_support.py

1. **CSS logical property tests**
   - Assert no `margin-left`/`margin-right` remain in base.css (except `margin-left: auto; margin-right: auto` pairs which become `margin-inline: auto`)
   - Assert no `padding-left`/`padding-right` remain (except paired as `padding-inline`)
   - Assert no `border-left`/`border-right` remain (except paired or `border-inline`)
   - Assert no `text-align: left` remains (should be `text-align: start`)
   - Assert no bare `left:`/`right:` remain for positioning (should be `inset-inline-*`)

2. **Direction config tests**
   - Test DEFAULT_CONFIG includes `direction: "auto"`
   - Test `get_direction()` returns "ltr" when LANGUAGE_CODE is "en"
   - Test `get_direction()` returns "rtl" when LANGUAGE_CODE is "ar"
   - Test `get_direction()` returns "rtl" when LANGUAGE_CODE is "he"
   - Test `get_direction()` returns explicit "ltr"/"rtl" when configured
   - Test `get_direction()` with language codes that have region (e.g. "ar-sa")

3. **Theme head direction tests**
   - Test theme_head.html sets `dir` attribute
   - Test direction="auto" resolves correctly for LTR language
   - Test direction="auto" resolves correctly for RTL language
   - Test explicit direction="rtl" is passed through

4. **RTL-aware component CSS tests**
   - Assert `[dir="rtl"]` rules exist in components.css
   - Assert breadcrumb separator handles RTL
   - Assert toast positions use logical properties
   - Assert pagination/nav arrows flip

5. **Manifest direction field tests**
   - Test ThemeManifest parses `direction` from [theme] section
   - Test ThemeManifest defaults to no direction (inherits config)
   - Test ThemeManifest.to_toml() includes direction when set

## Files Changed

- `djust_theming/static/djust_theming/css/base.css` -- logical property conversion + RTL overrides
- `djust_theming/static/djust_theming/css/components.css` -- logical property conversion + RTL overrides
- `djust_theming/static/djust_theming/css/layouts.css` -- logical property conversion
- `djust_theming/static/djust_theming/css/pages.css` -- logical property conversion
- `djust_theming/manager.py` -- add `direction` to DEFAULT_CONFIG, add `get_direction()`
- `djust_theming/manifest.py` -- add `direction` field
- `djust_theming/templates/djust_theming/theme_head.html` -- add `dir` attribute
- `djust_theming/templatetags/theme_tags.py` -- pass direction to template
- `tests/test_rtl_support.py` -- new test file
- `CHANGELOG.md` -- document changes
