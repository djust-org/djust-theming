# Theme Customization Tools

djust-theming ships with built-in developer tools for exploring, editing, and comparing themes. All tools live under the `theming/gallery/` URL namespace and share the same access control: always available when `DEBUG=True`, otherwise restricted to staff users (`is_staff`).

## Theme Gallery

The gallery renders every component with all variants on a single page. Use the preset selector at the top to switch between the 19 built-in color presets.

**URL:** `theming/gallery/`

**Query parameters:**

| Param | Default | Description |
|-------|---------|-------------|
| `preset` | `default` | Color preset to apply |

## Live Theme Editor

The editor provides an interactive two-panel interface for tweaking theme tokens in real time. Changes update CSS custom properties directly in the browser -- no server round-trip required for preview.

**URL:** `theming/gallery/editor/`

### Layout

- **Left sidebar:** Token controls (color pickers, radius slider, preset selector)
- **Right panel:** Live component preview showing buttons, cards, alerts, badges, inputs, tables, tabs, progress bars, and toasts

### Controls

| Control | Description |
|---------|-------------|
| Preset selector | Load any built-in preset as a starting point |
| Light / Dark tabs | Switch between light and dark mode token editing |
| Color inputs | Native `<input type="color">` for all 31 HSL tokens |
| Radius slider | `<input type="range">` from 0 to 2rem (0.125 step) |
| Reset button | Restore the currently selected preset defaults |
| Export button | Download the current token values as files |

### Token fields

The editor exposes all 31 color tokens:

`background`, `foreground`, `card`, `card-foreground`, `popover`, `popover-foreground`, `primary`, `primary-foreground`, `secondary`, `secondary-foreground`, `muted`, `muted-foreground`, `accent`, `accent-foreground`, `destructive`, `destructive-foreground`, `success`, `success-foreground`, `warning`, `warning-foreground`, `info`, `info-foreground`, `link`, `link-hover`, `code`, `code-foreground`, `selection`, `selection-foreground`, `border`, `input`, `ring`

Plus the `--radius` design token (border radius).

### Exporting a custom theme

Clicking **Export** sends the current token values to the server and triggers two file downloads:

1. **`tokens.css`** -- CSS custom property declarations for both light and dark modes
2. **`theme.toml`** -- A minimal theme manifest ready to drop into your `themes/` directory

Example exported `tokens.css`:

```css
/* djust-theming -- Custom theme tokens */

:root {
  --background: 0 0% 100%;
  --primary: 220 80% 50%;
  --radius: 0.75rem;
}

.dark,
[data-theme="dark"] {
  --background: 240 10% 4%;
  --primary: 220 80% 70%;
}
```

### Export endpoint

**URL:** `theming/gallery/editor/export/`
**Method:** POST only (GET returns 405)
**Content-Type:** `application/json`

Request body:

```json
{
  "name": "my-theme",
  "radius": 0.75,
  "tokens": {
    "light": {
      "background": {"h": 0, "s": 0, "l": 100},
      "primary": {"h": 220, "s": 80, "l": 50}
    },
    "dark": {
      "background": {"h": 240, "s": 10, "l": 4},
      "primary": {"h": 220, "s": 80, "l": 70}
    }
  }
}
```

Response:

```json
{
  "tokens_css": "/* djust-theming -- Custom theme tokens */\n...",
  "theme_toml": "[theme]\nname = \"my-theme\"\n..."
}
```

Input validation rules:

- **name:** Letters, digits, hyphens, underscores, spaces only. Max 64 characters.
- **radius:** Number between 0 and 4.
- **token names:** Lowercase letters, digits, hyphens, underscores only.
- **HSL values:** Must be numeric (int or float).

Invalid input returns a 400 response with an `{"error": "..."}` message.

## Diff View

The diff view shows two presets side by side for visual comparison. Each side loads the full gallery in an iframe with its own preset, so every component is compared at once.

**URL:** `theming/gallery/diff/`

**Query parameters:**

| Param | Default | Description |
|-------|---------|-------------|
| `left` | `default` | Preset for the left panel |
| `right` | `nord` | Preset for the right panel |

Changing either selector reloads the page with the new preset pair.

### Responsive behavior

On screens narrower than 768px, the two panels stack vertically instead of side by side.

## Access control

All three tools share the same access gate:

| Condition | Result |
|-----------|--------|
| `DEBUG=True` | Always accessible |
| `DEBUG=False` + `is_staff=True` | Accessible |
| `DEBUG=False` + `is_staff=False` | 403 Forbidden |

This prevents accidental exposure of developer tools in production while allowing staff users to use them when needed.

## URL summary

| URL | View | Name |
|-----|------|------|
| `theming/gallery/` | `gallery_view` | `djust_theming:gallery` |
| `theming/gallery/editor/` | `editor_view` | `djust_theming:editor` |
| `theming/gallery/editor/export/` | `editor_export_view` | `djust_theming:editor_export` |
| `theming/gallery/diff/` | `diff_view` | `djust_theming:diff` |

## Typical workflow

1. Open the **gallery** to see all components with the default preset
2. Open the **diff view** to compare two presets side by side
3. Pick a preset close to what you want
4. Open the **editor** with that preset (`?preset=nord`)
5. Tweak colors and radius until satisfied
6. Click **Export** to download `tokens.css` and `theme.toml`
7. Place the files in your theme directory (see [Theme Authoring Guide](theme-authoring.md))
8. Run `python manage.py djust_theme validate-theme my-theme` to verify
