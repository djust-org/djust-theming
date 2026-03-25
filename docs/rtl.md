# RTL (Right-to-Left) Support

djust-theming provides full RTL support for languages like Arabic, Hebrew, Farsi,
Urdu, and others that read right-to-left.

## Quick Start

By default, direction is detected automatically from Django's `LANGUAGE_CODE`
setting. No configuration is needed for most projects.

```python
# settings.py
LANGUAGE_CODE = "ar"  # Arabic -- RTL is detected automatically
```

The `{% theme_head %}` tag sets `dir="rtl"` on the `<html>` element, and all
CSS properties adapt accordingly.

## Direction Configuration

The `direction` option in `DJUST_THEMING` controls text direction. It accepts
three values:

| Value    | Behaviour                                                   |
|----------|-------------------------------------------------------------|
| `"auto"` | **(default)** Detect from `settings.LANGUAGE_CODE`          |
| `"ltr"`  | Force left-to-right                                         |
| `"rtl"`  | Force right-to-left                                         |

```python
# settings.py
DJUST_THEMING = {
    "direction": "auto",  # or "ltr" / "rtl"
}
```

### Auto-Detection

When `direction` is `"auto"`, djust-theming checks the primary subtag of
`LANGUAGE_CODE` against a built-in set of RTL languages:

- Arabic (`ar`)
- Hebrew (`he`)
- Farsi / Persian (`fa`)
- Urdu (`ur`)
- Pashto (`ps`)
- Sindhi (`sd`)
- Central Kurdish / Sorani (`ckb`)
- Yiddish (`yi`)
- Divehi / Maldivian (`dv`)
- Kurdish (`ku`)
- Uyghur (`ug`)

Regional subtags are handled correctly -- `ar-sa` (Arabic, Saudi Arabia) is
detected as RTL because the primary subtag `ar` is in the list.

## Per-Theme Direction Override

A theme manifest (`theme.toml`) can declare a direction that overrides the
global config:

```toml
[theme]
name = "my-rtl-theme"
version = "1.0.0"
direction = "rtl"
```

This is useful for themes designed exclusively for RTL audiences.

## How It Works

### Logical CSS Properties

All directional CSS properties have been converted to
[CSS logical properties](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values).
This means layouts automatically mirror when the direction changes:

| Physical Property       | Logical Equivalent           |
|-------------------------|------------------------------|
| `margin-left`           | `margin-inline-start`        |
| `margin-right`          | `margin-inline-end`          |
| `padding-left`          | `padding-inline-start`       |
| `padding-right`         | `padding-inline-end`         |
| `border-left`           | `border-inline-start`        |
| `border-right`          | `border-inline-end`          |
| `left` (positioning)    | `inset-inline-start`         |
| `right` (positioning)   | `inset-inline-end`           |
| `text-align: left`      | `text-align: start`          |

Shorthand properties are also used where both sides are the same:

- `margin-inline` replaces paired `margin-left` + `margin-right`
- `padding-inline` replaces paired `padding-left` + `padding-right`
- `border-inline` replaces paired `border-left` + `border-right`

### `dir` Attribute on `<html>`

The `{% theme_head %}` template tag renders a script that sets
`dir="ltr"` or `dir="rtl"` on the `<html>` element before the page
paints. This prevents a flash of mis-directed content.

### RTL-Aware Component Overrides

Some components require explicit RTL overrides beyond logical properties.
These are scoped with `[dir="rtl"]` selectors:

**base.css:**

- **Sidebar active indicator** -- The slide-in animation reverses direction.
- **Nav link underline** -- The underline expansion animates from the correct side.
- **Toast notifications** -- Slide-in/slide-out animations reverse their
  `translateX` direction.

**components.css:**

- **Breadcrumb separator** -- Arrow-like separators are flipped with
  `scaleX(-1)`.
- **Theme preset select** -- The dropdown arrow repositions to the left side.
- **Pagination arrows** -- Previous/next SVG icons are mirrored with
  `scaleX(-1)`.
- **Progress bar** -- The indeterminate animation reverses direction.

## Utility Classes

The margin and padding utility classes use logical properties and work
correctly in both LTR and RTL contexts:

| Class    | Property                   |
|----------|----------------------------|
| `.ms-*`  | `margin-inline-start`      |
| `.me-*`  | `margin-inline-end`        |
| `.mx-*`  | `margin-inline`            |
| `.px-*`  | `padding-inline`           |
| `.start-0` | `inset-inline-start: 0`  |
| `.end-0`   | `inset-inline-end: 0`    |

## Browser Support

CSS logical properties are supported in all modern browsers (Chrome 87+,
Firefox 66+, Safari 15+, Edge 87+). For older browser support, consider
a PostCSS plugin that generates physical property fallbacks.

## Programmatic Access

```python
from djust_theming.manager import get_direction, RTL_LANGUAGES

direction = get_direction()  # Returns "ltr" or "rtl"
```

`get_direction()` resolves the configured direction, handling `"auto"`
detection internally. It always returns either `"ltr"` or `"rtl"`.
