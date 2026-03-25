# Marketplace Specification

This document defines the metadata format for publishing djust-theming themes
to a future marketplace or package registry. It covers the `[marketplace]`
section in `theme.toml`, component coverage reporting, and the
`marketplace-info` CLI command.

## theme.toml `[marketplace]` section

The `[marketplace]` section is optional. When present it provides metadata
that a marketplace UI or package listing can use to display the theme.

```toml
[theme]
name = "aurora"
version = "1.2.0"
description = "A vibrant theme inspired by the Northern Lights"
author = "Jane Developer"
license = "MIT"

[tokens]
preset = "nord"
design_system = "material"

[marketplace]
screenshots = ["light.png", "dark.png", "dashboard.png"]
tags = ["dark", "vibrant", "material", "dashboard"]
compatibility_range = ">=0.3.0,<1.0.0"
preview_url = "https://aurora-theme.example.com/preview"
```

### Fields

| Field | Type | Description |
|---|---|---|
| `screenshots` | `list[str]` | Paths to screenshot images, relative to the theme directory. Recommended: at least one light-mode and one dark-mode screenshot. |
| `tags` | `list[str]` | Freeform tags for categorization and search. Common tags: `dark`, `light`, `minimal`, `corporate`, `material`, `vibrant`, `dashboard`, `responsive`. |
| `compatibility_range` | `str` | PEP 440 version specifier indicating which versions of djust-theming this theme supports. Example: `">=0.3.0,<1.0.0"`. |
| `preview_url` | `str` | URL to a live preview of the theme. Marketplace UIs can embed this in an iframe. |

All fields are optional. A theme without a `[marketplace]` section is still
valid and usable -- it just lacks the extra metadata for marketplace display.

## Component coverage

A theme can override some or all of the 24 built-in components by placing
template files in its `components/` directory. The remaining components
fall back to the default templates ("inherited").

Coverage is the percentage of components that have theme-specific overrides:

```
coverage = (overridden / total) * 100
```

A theme at 100% coverage overrides every component. A theme at 0% is
tokens-only (CSS custom properties) with no HTML changes.

### Coverage report via CLI

```bash
python manage.py djust_theme marketplace-info my-theme
```

Output:

```
Theme: my-theme v1.0.0
Description: A custom theme

Marketplace metadata:
  Tags: modern, dark
  Compatibility: >=0.3.0
  Preview URL: https://example.com

Component Coverage: 8.3% (2/24)

Overridden components:
  + button
  + card
Inherited (default) components:
  - alert
  - avatar
  - badge
  - breadcrumb
  - checkbox
  - dropdown
  - input
  - modal
  - nav
  - nav_group
  - nav_item
  - pagination
  - progress
  - radio
  - select
  - sidebar_nav
  - skeleton
  - table
  - tabs
  - textarea
  - toast
  - tooltip
```

Use `--dir` to point to a non-default themes directory:

```bash
python manage.py djust_theme marketplace-info my-theme --dir /path/to/themes
```

## Component Storybook

The component storybook at `theming/gallery/storybook/` provides a
developer-facing index of all components. Each component's detail page shows:

- Rendered variants with live examples
- Full context contract table (required and optional variables)
- Accessibility requirements
- Available slots
- CSS variables used by the component
- Raw template source code

This information is auto-generated from `contracts.py` and the default
template files. Theme authors can use the storybook to understand exactly
what each component expects and what they need to preserve when creating
overrides.

## Publishing workflow (future)

> This section describes a planned feature, not yet implemented.

1. Create your theme: `python manage.py djust_theme create-theme my-theme`
2. Customize templates and tokens
3. Add `[marketplace]` metadata to `theme.toml`
4. Add screenshots to the theme directory
5. Package: `python manage.py djust_theme create-package my-theme`
6. Verify: `python manage.py djust_theme marketplace-info my-theme`
7. Publish to PyPI: `cd djust-theme-my-theme && python -m build && twine upload dist/*`

In the future, a `djust_theme marketplace-publish` command may automate
steps 5-7 and register the theme with a central marketplace index.
