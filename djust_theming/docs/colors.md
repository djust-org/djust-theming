# Color System Reference

Complete guide to djust-theming's color system with expanded semantic tokens.

## Color Token Overview

djust-theming provides 31 semantic color tokens that adapt to light and dark themes:

### Core Structure (12 tokens)

| Token | Purpose | Light Mode | Dark Mode |
|-------|---------|------------|-----------|
| `--background` | Page background | White/very light | Very dark |
| `--foreground` | Primary text | Very dark | White/very light |
| `--card` | Card/surface background | White/very light | Dark |
| `--card-foreground` | Text on cards | Dark | Light |
| `--popover` | Popover backgrounds | White | Dark |
| `--popover-foreground` | Text in popovers | Dark | Light |
| `--muted` | Muted backgrounds | Light gray | Dark gray |
| `--muted-foreground` | Secondary text | Medium gray | Medium gray |
| `--accent` | Hover/highlight background | Very light | Dark |
| `--accent-foreground` | Text on accent | Dark | Light |
| `--border` | Border color | Light gray | Dark gray |
| `--input` | Input background/border | Light gray | Dark gray |

### Primary Actions (2 tokens)

| Token | Purpose | Usage |
|-------|---------|-------|
| `--primary` | Primary brand color | CTAs, active states, links |
| `--primary-foreground` | Text on primary | White text on primary buttons |

### Secondary Actions (2 tokens)

| Token | Purpose | Usage |
|-------|---------|-------|
| `--secondary` | Secondary color | Alternative actions, less prominent buttons |
| `--secondary-foreground` | Text on secondary | Dark text on secondary buttons |

### Status States (10 tokens)

| Token | Purpose | Usage |
|-------|---------|-------|
| `--destructive` | Error/danger color | Delete buttons, error messages |
| `--destructive-foreground` | Text on destructive | White text on red backgrounds |
| `--success` | Success/positive color | Success messages, completed states |
| `--success-foreground` | Text on success | White text on green backgrounds |
| `--warning` | Warning/caution color | Warning messages, pending states |
| `--warning-foreground` | Text on warning | White/dark text on yellow backgrounds |
| `--info` | Informational color | Info messages, help text |
| `--info-foreground` | Text on info | White text on blue backgrounds |
| `--selection` | Text selection highlight | Browser text selection color |
| `--selection-foreground` | Selected text color | Text color when selected |

### Links (2 tokens)

| Token | Purpose | Usage |
|-------|---------|-------|
| `--link` | Default link color | Hyperlinks, inline links |
| `--link-hover` | Link hover state | Slightly lighter/darker than default |

### Code (2 tokens)

| Token | Purpose | Usage |
|-------|---------|-------|
| `--code` | Code block background | Inline code, code blocks |
| `--code-foreground` | Code text color | Text in code blocks |

### Focus (1 token)

| Token | Purpose | Usage |
|-------|---------|-------|
| `--ring` | Focus ring color | Outline on focused elements |

## Usage in CSS

### Theme Colors (use with `hsl()`)

All color tokens are HSL values without the `hsl()` wrapper. Always wrap them:

```css
.button {
  background: hsl(var(--primary));
  color: hsl(var(--primary-foreground));
  border: 1px solid hsl(var(--border));
}

.button:hover {
  background: hsl(var(--primary) / 0.9);  /* 90% opacity */
}
```

### Utility Classes

Use pre-built utility classes for common patterns:

```html
<!-- Backgrounds -->
<div class="bg-primary">Primary background</div>
<div class="bg-success">Success background</div>
<div class="bg-info">Info background</div>
<div class="bg-code">Code background</div>

<!-- Text colors -->
<span class="text-primary">Primary text</span>
<span class="text-success">Success text</span>
<span class="text-info">Info text</span>
<span class="text-link">Link text</span>
<span class="text-muted-foreground">Muted text</span>

<!-- Borders -->
<div class="border border-primary">Primary border</div>
<div class="border border-success">Success border</div>
<div class="border border-info">Info border</div>
```

## Theme Preset Color Examples

### Default (Neutral Zinc)

```css
/* Light Mode */
--primary: 240 6% 10%;           /* Very dark blue-gray */
--success: 142 76% 36%;          /* Green */
--warning: 38 92% 50%;           /* Amber */
--destructive: 0 84% 60%;        /* Red */
--info: 199 89% 48%;             /* Blue */
--link: 221 83% 53%;             /* Bright blue */
--code: 240 5% 94%;              /* Very light gray */
--selection: 240 100% 80%;       /* Light blue */

/* Dark Mode */
--primary: 0 0% 98%;             /* Almost white */
--success: 142 69% 28%;          /* Darker green */
--warning: 38 92% 40%;           /* Darker amber */
--destructive: 0 62% 30%;        /* Dark red */
--info: 199 89% 60%;             /* Lighter blue */
--link: 221 83% 65%;             /* Brighter blue */
--code: 240 4% 12%;              /* Very dark gray */
--selection: 240 100% 30%;       /* Dark blue */
```

### Blue Theme

```css
/* Light Mode */
--primary: 221 83% 53%;          /* Blue */
--link: 221 83% 53%;             /* Blue (matches primary) */
--code: 221 95% 94%;             /* Very light blue tint */
--selection: 221 100% 80%;       /* Light blue */

/* Dark Mode */
--primary: 224 76% 48%;          /* Blue */
--link: 221 83% 65%;             /* Lighter blue */
--code: 221 30% 12%;             /* Dark with blue tint */
--selection: 221 100% 30%;       /* Dark blue */
```

### Green Theme

```css
/* Light Mode */
--primary: 142 76% 36%;          /* Green */
--link: 142 76% 40%;             /* Green (slightly lighter) */
--code: 142 20% 94%;             /* Light green tint */
--selection: 142 100% 80%;       /* Light green */

/* Dark Mode */
--primary: 142 69% 45%;          /* Green */
--link: 142 69% 45%;             /* Green (matches primary) */
--code: 142 30% 12%;             /* Dark with green tint */
--selection: 142 100% 30%;       /* Dark green */
```

## Semantic Color Guidelines

### When to Use Each Color

#### Primary

- Main call-to-action buttons ("Sign Up", "Submit", "Create")
- Active navigation items
- Selected/focused states
- Primary brand elements

#### Secondary

- Alternative actions ("Cancel", "Skip", "Back")
- Less important buttons
- Secondary brand elements

#### Destructive

- Delete actions
- Remove/revoke buttons
- Error messages
- Failed states

#### Success

- Completed tasks
- Success messages
- Positive feedback
- "Done" or "Passed" states

#### Warning

- Caution messages
- Pending states
- Required attention
- Validation warnings

#### Info

- Informational messages
- Help text
- Tips and hints
- Non-critical notifications

#### Link

- Hyperlinks in body text
- Navigation links in content
- Reference links

#### Code

- Inline code snippets
- Code block backgrounds
- Monospace text backgrounds

#### Selection

- Browser text selection
- Custom selection highlights
- Highlighted search results

## Accessibility

### Contrast Requirements

All foreground/background pairs meet WCAG AA contrast requirements (4.5:1 for normal text, 3:1 for large text):

- `--primary` + `--primary-foreground` ✓
- `--success` + `--success-foreground` ✓
- `--warning` + `--warning-foreground` ✓
- `--destructive` + `--destructive-foreground` ✓
- `--info` + `--info-foreground` ✓
- `--code` + `--code-foreground` ✓
- `--selection` + `--selection-foreground` ✓

### Color Blindness

Status colors are chosen to be distinguishable for common color blindness types:

- **Protanopia/Deuteranopia** (red-green): Destructive (red) vs Success (green) have different lightness
- **Tritanopia** (blue-yellow): Info (blue) vs Warning (yellow) have different saturation

Always use additional indicators beyond color (icons, labels, patterns).

## Advanced Patterns

### Alpha Transparency

Use alpha channel for hover states and overlays:

```css
.button:hover {
  background: hsl(var(--primary) / 0.9);  /* 90% opacity */
}

.overlay {
  background: hsl(var(--background) / 0.8);  /* 80% opacity */
}
```

### Color Mixing

Combine colors for custom states:

```css
.warning-card {
  background: hsl(var(--warning) / 0.1);  /* 10% warning tint */
  border-left: 3px solid hsl(var(--warning));
  color: hsl(var(--foreground));
}

.info-banner {
  background: hsl(var(--info) / 0.1);
  color: hsl(var(--info-foreground));
}
```

### Gradient Backgrounds

```css
.gradient-header {
  background: linear-gradient(
    135deg,
    hsl(var(--primary)),
    hsl(var(--accent))
  );
  color: hsl(var(--primary-foreground));
}
```

## Component Examples

### Status Badge

```html
<span class="badge badge-success">Completed</span>
<span class="badge badge-warning">Pending</span>
<span class="badge badge-destructive">Failed</span>
<span class="badge badge-info">New</span>
```

### Alert Boxes

```css
.alert {
  padding: 1rem;
  border-radius: var(--radius);
  border-left: 4px solid;
}

.alert-success {
  background: hsl(var(--success) / 0.1);
  border-color: hsl(var(--success));
  color: hsl(var(--success-foreground));
}

.alert-warning {
  background: hsl(var(--warning) / 0.1);
  border-color: hsl(var(--warning));
  color: hsl(var(--warning-foreground));
}

.alert-info {
  background: hsl(var(--info) / 0.1);
  border-color: hsl(var(--info));
  color: hsl(var(--info-foreground));
}
```

### Styled Links

```html
<a href="#" class="link">Learn more →</a>
```

```css
.link {
  color: hsl(var(--link));
  text-decoration: none;
  transition: color 150ms ease;
}

.link:hover {
  color: hsl(var(--link-hover));
  text-decoration: underline;
}
```

### Code Blocks

```html
<code>const theme = 'dark';</code>
```

```css
code {
  background: hsl(var(--code));
  color: hsl(var(--code-foreground));
  padding: 0.125rem 0.375rem;
  border-radius: calc(var(--radius) - 0.125rem);
  font-family: monospace;
  font-size: 0.875em;
}
```

## Best Practices

### ✅ Do

- Use semantic colors for their intended purpose
- Always pair colors with their foreground variants
- Use alpha transparency for subtle effects
- Provide non-color indicators (icons, labels)

### ❌ Don't

- Don't hardcode hex colors (`#3b82f6`)
- Don't use colors outside their semantic meaning (e.g., destructive for success)
- Don't forget foreground colors (ensure text is readable)
- Don't rely solely on color to convey meaning

## FAQ

### Q: Can I customize color values?

Yes. Override any color token in your CSS:

```css
:root {
  --primary: 220 90% 56%;  /* Custom blue */
  --success: 150 80% 40%;  /* Custom green */
}
```

### Q: How do I create a custom status color?

Define custom tokens and utility classes:

```css
:root {
  --custom: 280 70% 50%;  /* Purple */
  --custom-foreground: 0 0% 100%;
}

.bg-custom {
  background: hsl(var(--custom));
  color: hsl(var(--custom-foreground));
}
```

### Q: Can I use RGB instead of HSL?

HSL is recommended for easier manipulation (lightness, saturation adjustments), but you can convert:

```css
/* HSL to RGB conversion */
--primary-rgb: 59 130 246;  /* Equivalent to hsl(221 83% 53%) */
background: rgb(var(--primary-rgb));
```

### Q: How do I test color contrast?

Use browser DevTools or online tools like:
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- Chrome DevTools → Elements → Accessibility pane

## Summary

- **31 semantic color tokens** covering all common UI needs
- **8 new tokens** (info, link, code, selection) added in Phase 1
- **7 theme presets** with customized color values
- **Accessible color pairs** meeting WCAG AA standards
- **Utility classes** for rapid development
- **Zero configuration** - works automatically with djust_theming

For complete design system reference, see [Design System Guide](./design-system.md).
