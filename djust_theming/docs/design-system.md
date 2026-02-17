# Design System - djust_theming

Comprehensive design foundation for djust applications with spacing, typography, colors, and interactive states.

## Overview

The djust_theming design system provides:

- **Theme-agnostic design tokens** - Spacing, typography, and structural styling that work with any color palette
- **Automatic theme integration** - Color system (light/dark modes) + design tokens in one generated stylesheet
- **Semantic component patterns** - Consistent interactive states, typography hierarchy, and layout utilities
- **Zero configuration** - Design tokens are included by default when you use djust_theming

## Quick Start

Design tokens are automatically included when you use djust_theming:

```python
# settings.py
INSTALLED_APPS = [
    'djust_theming',
    # ...
]

TEMPLATES = [
    {
        'BACKEND': 'djust_theming.backend.DjustThemeEngine',
        'OPTIONS': {
            'preset': 'default',  # or 'slate', 'rose', 'blue', etc.
        },
    },
]

MIDDLEWARE = [
    'djust_theming.middleware.ThemeMiddleware',
    # ...
]

# Context processor (adds {{ theme_head }} to all templates)
TEMPLATES[0]['OPTIONS']['context_processors'] = [
    'djust_theming.context_processors.theme_context',
    # ...
]
```

In your base template:

```html
<!DOCTYPE html>
<html>
<head>
    {{ theme_head|safe }}
</head>
<body>
    <!-- Your content -->
    {{ theme_switcher|safe }}
</body>
</html>
```

That's it! All design tokens are now available as CSS variables.

## Design Tokens Reference

### Spacing Scale

Consistent spacing using a 4px base unit:

| Variable | Value | Pixels | Common Use |
|----------|-------|--------|------------|
| `--space-0` | 0 | 0px | Reset spacing |
| `--space-1` | 0.25rem | 4px | Tight inline spacing |
| `--space-2` | 0.5rem | 8px | Small gaps, compact layouts |
| `--space-3` | 0.75rem | 12px | Default inline spacing |
| `--space-4` | 1rem | 16px | Default block spacing |
| `--space-5` | 1.25rem | 20px | Medium gaps |
| `--space-6` | 1.5rem | 24px | Section spacing |
| `--space-8` | 2rem | 32px | Large section gaps |
| `--space-10` | 2.5rem | 40px | Extra large spacing |
| `--space-12` | 3rem | 48px | Page-level spacing |
| `--space-16` | 4rem | 64px | Very large spacing |
| `--space-20` | 5rem | 80px | Massive spacing |
| `--space-24` | 6rem | 96px | Maximum spacing |

**Usage:**

```css
.my-component {
  margin-bottom: var(--space-4);  /* 16px */
  padding: var(--space-3);         /* 12px */
  gap: var(--space-2);             /* 8px */
}
```

### Typography

#### Font Sizes

| Variable | Value | Pixels | Use Case |
|----------|-------|--------|----------|
| `--text-xs` | 0.75rem | 12px | Labels, tiny text |
| `--text-sm` | 0.875rem | 14px | Secondary text |
| `--text-base` | 1rem | 16px | Body text |
| `--text-lg` | 1.125rem | 18px | Slightly larger body |
| `--text-xl` | 1.25rem | 20px | H5, subheadings |
| `--text-2xl` | 1.5rem | 24px | H4, card titles |
| `--text-3xl` | 1.875rem | 30px | H3, section headings |
| `--text-4xl` | 2.25rem | 36px | H2, page titles |
| `--text-5xl` | 3rem | 48px | H1, hero text |
| `--text-6xl` | 3.75rem | 60px | Extra large display |

#### Line Heights

| Variable | Value | Use Case |
|----------|-------|----------|
| `--leading-none` | 1 | Icons, dense layouts |
| `--leading-tight` | 1.25 | Headings |
| `--leading-snug` | 1.375 | Subheadings |
| `--leading-normal` | 1.5 | Body text |
| `--leading-relaxed` | 1.625 | Long-form content |
| `--leading-loose` | 2 | Very spacious text |

#### Font Weights

| Variable | Value | Weight Name |
|----------|-------|-------------|
| `--font-thin` | 100 | Thin |
| `--font-extralight` | 200 | Extra Light |
| `--font-light` | 300 | Light |
| `--font-normal` | 400 | Normal |
| `--font-medium` | 500 | Medium |
| `--font-semibold` | 600 | Semibold |
| `--font-bold` | 700 | Bold |
| `--font-extrabold` | 800 | Extra Bold |
| `--font-black` | 900 | Black |

**Typography Classes:**

The design system includes semantic typography classes:

```html
<!-- Headings -->
<h2 class="h2">Section Heading</h2>
<h3 class="h3">Subsection</h3>
<h4 class="h4">Card Title</h4>

<!-- Body text -->
<p class="text-body">Default paragraph text</p>
<span class="text-small">Secondary information</span>
<span class="text-tiny">Helper text or labels</span>

<!-- Text styles -->
<span class="text-uppercase">Uppercase text</span>
<p class="text-balance">Balanced text wrapping</p>
<p class="text-pretty">Pretty text wrapping (CSS Text 4)</p>
```

### Border Radius

Extended radius tokens based on the theme's `--radius` variable:

| Variable | Formula | Use Case |
|----------|---------|----------|
| `--radius-sm` | `--radius - 0.125rem` | Nested elements |
| `--radius-md` | `--radius` | Standard components |
| `--radius-lg` | `--radius + 0.125rem` | Large components |
| `--radius-xl` | `--radius + 0.25rem` | Cards, modals |
| `--radius-2xl` | `--radius + 0.5rem` | Hero sections |
| `--radius-full` | `9999px` | Pills, badges |

**Usage:**

```css
.button {
  border-radius: var(--radius-md);
}

.badge {
  border-radius: var(--radius-full);
}
```

### Transitions and Animations

Consistent timing for UI animations:

| Variable | Value | Use Case |
|----------|-------|----------|
| `--duration-fast` | 150ms | Hover states, quick feedback |
| `--duration-normal` | 200ms | Default transitions |
| `--duration-slow` | 300ms | Complex animations |
| `--duration-slower` | 500ms | Major state changes |

**Easing curves:**

| Variable | Curve | Use Case |
|----------|-------|----------|
| `--ease-in` | cubic-bezier(0.4, 0, 1, 1) | Elements leaving |
| `--ease-out` | cubic-bezier(0, 0, 0.2, 1) | Elements entering |
| `--ease-in-out` | cubic-bezier(0.4, 0, 0.2, 1) | Smooth back-and-forth |

**Usage:**

```css
.button {
  transition: background-color var(--duration-fast) var(--ease-out);
}
```

### Shadows

Theme-aware shadows that adapt to light/dark modes:

| Variable | Light Mode | Dark Mode | Use Case |
|----------|------------|-----------|----------|
| `--shadow-sm` | Subtle | Subtle | Inline elements |
| `--shadow-md` | Medium | Medium | Cards, dropdowns |
| `--shadow-lg` | Large | Large | Modals, overlays |
| `--shadow-xl` | Extra large | Extra large | Floating panels |

**Usage:**

```css
.card {
  box-shadow: var(--shadow-md);
}
```

## Component Patterns

### Interactive States

The design system provides a `.interactive` base class for consistent hover/focus/active/disabled states:

```html
<button class="interactive">
  <!-- Hover: accent background -->
  <!-- Active: scale(0.98) -->
  <!-- Focus: ring outline -->
  <!-- Disabled: 50% opacity, no pointer events -->
</button>
```

**Link styling:**

```html
<a href="#" class="link">
  <!-- Color: primary -->
  <!-- Hover: underline appears -->
  <!-- Focus: ring outline -->
</a>
```

**Focus rings:**

```html
<input class="focus-ring" />           <!-- Outline with offset -->
<button class="focus-ring-inset" />    <!-- Inset outline -->
```

### Layout Utilities

**Text truncation:**

```html
<div class="truncate">This text will be truncated with ellipsis...</div>

<div class="line-clamp-2">
  This text will be limited to 2 lines with an ellipsis at the end if it overflows beyond that height.
</div>

<!-- Also: .line-clamp-3, .line-clamp-4 -->
```

**Custom scrollbars:**

```html
<div class="custom-scrollbar" style="max-height: 300px; overflow-y: auto;">
  <!-- Themed scrollbar with hover effect -->
</div>
```

### Animation Utilities

Built-in animations for common UI patterns:

```html
<!-- Fade effects -->
<div class="fade-in">Appears smoothly</div>
<div class="fade-out">Disappears smoothly</div>

<!-- Slide effects -->
<div class="slide-in-right">Slides in from right</div>
<div class="slide-out-right">Slides out to right</div>

<!-- Status indicators -->
<span class="pulse">Pulsing element</span>
<div class="spin">Spinning loader</div>
```

**Custom animations:**

Use the keyframes directly:

```css
.my-element {
  animation: fadeIn var(--duration-normal) ease;
}

.my-loader {
  animation: spin 1s linear infinite;
}
```

## Color System Integration

Design tokens integrate seamlessly with djust_theming's color system. All theme colors are available as CSS variables:

### Core Colors

| Variable | Purpose |
|----------|---------|
| `--background` | Page background |
| `--foreground` | Primary text |
| `--card` | Card/surface background |
| `--muted` | Muted background |
| `--muted-foreground` | Secondary text |
| `--accent` | Hover/highlight |
| `--primary` | Primary brand color |
| `--secondary` | Secondary color |
| `--destructive` | Error/danger |
| `--success` | Success/positive |
| `--warning` | Warning/caution |
| `--border` | Border color |
| `--input` | Input background |
| `--ring` | Focus ring |

**Usage with design tokens:**

```css
.my-component {
  padding: var(--space-4);
  font-size: var(--text-sm);
  background: hsl(var(--card));
  color: hsl(var(--card-foreground));
  border: 1px solid hsl(var(--border));
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  transition: all var(--duration-fast) ease;
}

.my-component:hover {
  background: hsl(var(--accent));
  box-shadow: var(--shadow-md);
}
```

## Advanced Usage

### Customizing Design Tokens

You can selectively include or exclude design token categories:

```python
from djust_theming.design_tokens import generate_design_tokens_css

# Include only typography and interactive patterns
custom_css = generate_design_tokens_css(
    include_typography=True,
    include_interactive=True,
    include_layout=False,
    include_animations=False,
)
```

### Programmatic CSS Generation

Generate CSS with design tokens programmatically:

```python
from djust_theming.css_generator import ThemeCSSGenerator

generator = ThemeCSSGenerator(
    preset_name='slate',
    include_design_tokens=True,  # Default: True
    include_base_styles=True,
    include_utilities=True,
)

css = generator.generate_css()
```

### Disabling Design Tokens

If you only want theme colors without design tokens:

```python
generator = ThemeCSSGenerator(
    preset_name='default',
    include_design_tokens=False,
)
```

## Migration Guide

### Migrating from Inline Values

Before:

```css
.button {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  border-radius: 0.375rem;
  transition: all 150ms ease;
}
```

After:

```css
.button {
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-sm);
  border-radius: var(--radius-md);
  transition: all var(--duration-fast) ease;
}
```

### Migrating from Tailwind Utilities

The design system complements Tailwind CSS. Use Tailwind for layout/spacing utilities, design tokens for consistent values:

Before:

```html
<div class="p-4 text-sm rounded-md">...</div>
```

After (mixing Tailwind with design system):

```html
<div class="p-4 rounded-md" style="font-size: var(--text-sm);">...</div>
```

Or use pure design system classes:

```html
<div class="text-small" style="padding: var(--space-4); border-radius: var(--radius-md);">...</div>
```

## Best Practices

### 1. Use spacing tokens consistently

```css
/* ✅ Good - uses spacing scale */
.component {
  margin-bottom: var(--space-4);
  padding: var(--space-3);
}

/* ❌ Bad - arbitrary values */
.component {
  margin-bottom: 18px;
  padding: 11px;
}
```

### 2. Use typography classes for headings

```html
<!-- ✅ Good - semantic typography -->
<h2 class="h2">Section Title</h2>

<!-- ❌ Bad - inline styles -->
<h2 style="font-size: 1.875rem; font-weight: 700;">Section Title</h2>
```

### 3. Combine design tokens with theme colors

```css
/* ✅ Good - uses both systems */
.button {
  padding: var(--space-2) var(--space-4);
  background: hsl(var(--primary));
  border-radius: var(--radius-md);
  transition: background var(--duration-fast) ease;
}

/* ❌ Bad - hardcoded colors */
.button {
  padding: var(--space-2) var(--space-4);
  background: #3b82f6;  /* Don't hardcode colors */
}
```

### 4. Use semantic animation utilities

```html
<!-- ✅ Good - uses utility class -->
<div class="fade-in">Content</div>

<!-- ❌ Bad - inline animation -->
<div style="animation: fadeIn 0.2s ease;">Content</div>
```

### 5. Leverage theme-aware shadows

```css
/* ✅ Good - adapts to theme -->
.card {
  box-shadow: var(--shadow-md);
}

/* ❌ Bad - fixed shadow -->
.card {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
```

## Examples

### Complete Button Component

```css
.btn {
  /* Spacing */
  padding: var(--space-2) var(--space-4);

  /* Typography */
  font-size: var(--text-sm);
  font-weight: var(--font-medium);

  /* Colors */
  background: hsl(var(--primary));
  color: hsl(var(--primary-foreground));
  border: 1px solid hsl(var(--primary));

  /* Borders */
  border-radius: var(--radius-md);

  /* Transitions */
  transition: all var(--duration-fast) var(--ease-out);

  /* Cursor */
  cursor: pointer;
}

.btn:hover {
  background: hsl(var(--primary) / 0.9);
  box-shadow: var(--shadow-sm);
}

.btn:active {
  transform: scale(0.98);
}

.btn:focus-visible {
  outline: 2px solid hsl(var(--ring));
  outline-offset: 2px;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

### Complete Card Component

```css
.card {
  /* Spacing */
  padding: var(--space-6);

  /* Colors */
  background: hsl(var(--card));
  color: hsl(var(--card-foreground));
  border: 1px solid hsl(var(--border));

  /* Borders */
  border-radius: var(--radius-xl);

  /* Shadows */
  box-shadow: var(--shadow-sm);

  /* Transitions */
  transition: box-shadow var(--duration-normal) var(--ease-out);
}

.card:hover {
  box-shadow: var(--shadow-md);
}

.card-title {
  font-size: var(--text-2xl);
  font-weight: var(--font-semibold);
  line-height: var(--leading-tight);
  margin-bottom: var(--space-4);
}

.card-body {
  font-size: var(--text-base);
  line-height: var(--leading-normal);
  color: hsl(var(--muted-foreground));
}
```

### Form Input

```css
.input {
  /* Spacing */
  padding: var(--space-2) var(--space-3);

  /* Typography */
  font-size: var(--text-sm);

  /* Colors */
  background: hsl(var(--background));
  color: hsl(var(--foreground));
  border: 1px solid hsl(var(--border));

  /* Borders */
  border-radius: var(--radius-md);

  /* Transitions */
  transition: border-color var(--duration-fast) ease,
              box-shadow var(--duration-fast) ease;
}

.input::placeholder {
  color: hsl(var(--muted-foreground));
}

.input:focus {
  outline: none;
  border-color: hsl(var(--ring));
  box-shadow: 0 0 0 2px hsl(var(--ring) / 0.2);
}

.input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

## FAQ

### Q: Do I need to manually add design tokens?

No. Design tokens are automatically included when you use `djust_theming`. The `theme_head` template variable includes everything.

### Q: Can I use design tokens without theme colors?

Yes. Set `include_design_tokens=True` and `include_utilities=False` when generating CSS, or use design tokens alongside your own color system.

### Q: Are design tokens compatible with Tailwind CSS?

Yes. Design tokens use CSS custom properties (variables), so they work alongside Tailwind. Use Tailwind for layout utilities (flex, grid, gap) and design tokens for consistent values (spacing, typography, transitions).

### Q: How do I override design tokens?

You can override any token in your own CSS:

```css
:root {
  --space-4: 1.5rem;  /* Override to 24px instead of 16px */
  --text-base: 1.125rem;  /* Override to 18px instead of 16px */
}
```

### Q: Do design tokens work in all browsers?

Yes. CSS custom properties are supported in all modern browsers (Chrome, Firefox, Safari, Edge). For IE11, you would need a PostCSS plugin to convert variables to static values.

### Q: Can I use design tokens in JavaScript?

Yes. Access them via `getComputedStyle`:

```javascript
const spaceUnit = getComputedStyle(document.documentElement)
  .getPropertyValue('--space-4');  // Returns "1rem"
```

## Further Reading

- [Theme Presets](./presets.md) - Available color schemes
- [Theme Manager](./manager.md) - Runtime theme switching
- [CSS Generator](./css-generator.md) - Programmatic CSS generation
- [djust Documentation](https://github.com/Photon1c/djust) - LiveView framework
