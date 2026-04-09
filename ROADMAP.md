# djust-theming Roadmap

> Goal: A complete theming system where full customization of look and feel is achieved by writing a new template set + design tokens. No Python code required to create a theme.

## Current State (v0.4.0rc3)

What works today:
- 34 color presets (HSL-based, light/dark mode) with registration API for custom themes
- ThemeTokens: 29 color fields + selection, surface levels, radius
- SurfaceTreatment dataclass (glass/gradient/noise) — only used by djust.org theme so far
- CSS variable generation pipeline (color + typography + spacing + shadows)
- Live theme switching via djust LiveView (no page reload)
- Theme state persistence (cookies, session, localStorage)
- FOUC elimination via critical CSS + deferred transitions
- @layer removed from all CSS for reliable specificity
- Django system check for WCAG AA contrast validation
- CLI management command

### Theme Catalog (34 presets)

| Category | Themes | Notes |
|----------|--------|-------|
| **Neutrals** | Default (Zinc), Shadcn, Slate, Mono | Foundation themes |
| **Single-hue** | Blue, Green, Purple, Orange, Rose | Simple brand colors |
| **Dev Classics** | Dracula, Gruvbox, Solarized, Nord, Catppuccin, Rosé Pine, Tokyo Night | Community favorites |
| **Neon/Retro** | Synthwave '84, Cyberpunk, Outrun, Neon Noir, Cyberdeck | Dark-first, vivid |
| **Nature** | Forest, Solarpunk, Aurora, Ocean, Ember | Organic palettes |
| **Design-forward** | Bauhaus, Ink, Paper, Amber, Natural 20 | Conceptual themes |
| **Accessibility** | High Contrast | WCAG AAA target |
| **Brand** | djust.org | Internal dogfood theme |

---

## Milestone 1: Theme Quality Audit (Priority: High)

Fix the two-tier quality gap. The "famous" themes (Dracula, Catppuccin, Rosé Pine) have traced-to-spec values; the batch-added themes don't. Users will notice.

### 1.1 Spec-Trace Gruvbox, Solarized, Nord

**Problem**: These 3 themes have huge community followings with published official specs. Current values are HSL approximations without hex comments.

**Work**:
- Gruvbox: trace to github.com/morhetz/gruvbox palette (bg0–bg4, fg0–fg4, red/green/yellow/blue/purple/aqua/orange)
- Solarized: trace to ethanschoonover.com/solarized (base03–base3, yellow/orange/red/magenta/violet/blue/cyan/green)
- Nord: trace to nordtheme.com (polar night, snow storm, frost, aurora)
- Add hex comments on every line like the Dracula overhaul
- Verify official light variants exist (Solarized Light is canonical; Gruvbox Light is official; Nord Light is less defined)

### 1.2 Surface + Selection Token Deformulification

**Problem**: 25+ themes use identical copy-paste patterns for surfaces and selections:
```python
# Every theme does this:
surface_1=ColorScale(hue, 5, 6)    # ← same lightness values
surface_2=ColorScale(hue, 5, 10)
surface_3=ColorScale(hue, 5, 14)
selection=ColorScale(hue, 80, 85)  # ← same saturation/lightness
```

**Work**:
- Themes with official specs: use their actual surface hierarchy (Gruvbox bg0–bg4, Solarized base03–base00, Nord polar night 0–3)
- Themes without specs: at minimum vary the saturation and spacing per theme personality (Ink should have tighter, more muted steps; Synthwave should have more saturated, wider steps)
- Selection colors should reference the theme's accent/primary, not a generic formula

### 1.3 Light Mode Pass

**Problem**: Dark-first themes (Ember, Neon Noir, Cyberdeck, Synthwave, Outrun) likely have underwhelming light modes — just inverted lightness. Dracula's Alucard overhaul proved that a bespoke light mode transforms the theme.

**Work**:
- Audit each dark-first theme's light mode for personality (does it look like "that theme" or "generic light"?)
- Ember light: should feel like warm afternoon, not just "orange on white"
- Neon Noir light: maybe a crisp daylight-noir with muted neons? Or mark as dark-only if a light mode doesn't make sense
- Consider adding `supports_light: bool` to ThemePreset so the UI can hide the mode toggle for dark-only themes

### 1.4 Radius + SurfaceTreatment Personality

**Problem**: Only 9 of 34 themes set `radius`. Only djust.org uses `SurfaceTreatment`. These are free personality wins being left on the table.

**Work**:
- Bauhaus: `radius=0` (geometric, hard edges)
- Ink: `radius=0` (calligraphy is sharp)
- Cyberpunk/Cyberdeck: `radius=0.125` (techy, slightly rounded)
- Paper: `radius=0.25` (soft but not bubbly)
- Catppuccin/Rosé Pine: keep `0.75` (pillowy)
- Synthwave/Neon Noir: `SurfaceTreatment(style='glass', glass_blur='16px')` — neon themes want glow
- Paper: `SurfaceTreatment(style='noise', noise_opacity=0.04)` — paper grain
- Ink: no treatment (flat, intentional)

### 1.5 Accessibility Audit Across All 34

**Problem**: The Django system check validates contrast, but has it been run against the new batch of themes? Several themes (Synthwave dark, Neon Noir, Cyberpunk) are likely at the edge of AA ratios for `muted_foreground` on `background`.

**Work**:
- Run the system check, collect all warnings
- Fix violations — or document intentional exceptions for "decorative" themes
- Especially check: `muted_foreground` on `background`, `link` on `card`, `warning_foreground` on `warning`

---

## Milestone 2: New "Famous" Theme Presets (Priority: Medium)

Add themes people actively search for. Each one gets the Dracula treatment: official hex values, per-line comments, bespoke light/dark modes.

### 2.1 One Dark Pro
The most-installed VS Code theme. Well-defined palette. Dark-first with a clean light variant (Atom One Light).

### 2.2 GitHub (Primer)
Light and dark modes from GitHub's Primer design system. Extremely practical — every developer knows what it looks like. Bonus: validates that the token system works for "corporate clean" aesthetics, not just editor themes.

### 2.3 Kanagawa
Neovim community darling. Japanese-wave-inspired, darker and more muted than Tokyo Night. Pairs with Ink as "the Japan collection."

### 2.4 Everforest
The nature equivalent of Gruvbox — soft green with warm undertones. Large vim/neovim following. More refined than Solarpunk for the "gentle nature" slot.

### 2.5 Moonlight
VS Code theme with a unique indigo-purple base (distinct from Dracula's purple). Popular in the aesthetic-coding community.

---

## Milestone 3: Theme Organization + UX (Priority: Medium)

34 themes is past the point where "pick from a flat list" works well.

### 3.1 Theme Categories/Tags

**Problem**: A user browsing 34+ themes has no structure. They don't know that Gruvbox and Solarized are "developer classics" or that Synthwave and Outrun are both retro-neon.

**Work**:
- Add `category: str` to ThemePreset (or `tags: list[str]`)
- Categories: Developer Classics, Neon & Retro, Nature & Organic, Minimalist, Accessibility, Brand
- Theme picker UI groups by category

### 3.2 Theme Metadata Enrichment

**Work**:
- Add `default_mode` display hint so dark-first themes show their dark mode in previews
- Add optional `homepage: str` for themes with official sites (draculatheme.com, nordtheme.com, etc.)
- Add optional `author: str` for community-contributed themes

### 3.3 Theme Search/Filter

For the theme panel: filter by category, search by name, filter "dark-first" vs "light-first."

---

## Milestone 4: Quality-of-Life Infrastructure (Priority: Medium-Low)

### 4.1 Theme Contrast Report Command

`python manage.py theme_contrast_report` — generates a table of all 34 themes with their AA/AAA pass/fail for every foreground/background pair. Machine-readable output for CI.

### 4.2 Theme Preview Gallery

A standalone HTML page (or management command that generates one) showing every theme's light and dark mode with sample components. Useful for documentation and visual regression checking.

### 4.3 Theme Diff Tool

`python manage.py theme_diff dracula gruvbox` — shows which tokens differ and by how much. Useful when creating new themes to ensure they're actually distinct from existing ones.

---

## Milestone 5: Theme Authoring (Priority: Low — after quality stabilizes)

### 5.1 Theme Scaffold Command

`python manage.py create_theme my_theme` — generates a starter ThemePreset with all required fields, sensible defaults, and inline comments explaining each token.

### 5.2 Theme Import from External Formats

Import from:
- VS Code `.json` theme files (map editor colors to ThemeTokens)
- Tailwind `theme.extend.colors` config
- shadcn/ui CSS variables

### 5.3 AI-Assisted Theme Generation

`register_preset("warm-ocean", from_prompt="warm ocean blues with sandy accents")` — uses the palette derivation system to generate a full ThemeTokens from a natural language description. Stretch goal.

---

## Backlog (unscheduled, revisit after v0.4.0 stable)

These are real needs but don't block the current trajectory:

- **RTL/bidirectional layout tokens** — important for internationalization, not urgent for theming core
- **Container-scoped theming** — nested themes within a page (e.g., dark sidebar in light page)
- **Print stylesheet per theme** — print.css exists but isn't theme-aware
- **Email-compatible theme export** — inline CSS for HTML emails
- **Responsive/breakpoint token system** — tokens that change at breakpoints
- **Template override system** — the original Phase 1 vision of themes-as-template-sets (revisit once component library stabilizes in djust-components)

---

## Design Principles

1. **Official specs over approximations** — if a theme has a published palette, use it exactly
2. **Both modes must have personality** — a light mode that's just "inverted dark" isn't done
3. **Tokens should feel intentional** — no copy-paste surface/selection formulas across themes
4. **Accessibility is non-negotiable** — every theme must pass AA for body text pairs
5. **Less is more** — 34 excellent themes beats 60 mediocre ones; quality > quantity
