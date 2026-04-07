# Plan: Phase 1.2 + 1.3 - Theme Manifest + Scaffold Command

## Status: IMPLEMENTATION_COMPLETE
## Branch: task/1.2-1.3-theme-manifest-scaffold
## Date: 2026-03-23

---

## Stage Results

| Stage | Result |
|-------|--------|
| 1 - Environment Check | ENV_OK |
| 2 - Change Detection | CODE_CHANGES: None (fresh branch from main) |
| 3 - Conflict Check | MERGE_CLEAN |
| 5 - Implementation | COMPLETE — 47 new tests (30 manifest + 17 command), 238 total pass |

---

## Existing Code Analysis

### management/commands/djust_theme.py
- Subcommand-based command using `add_subparsers(dest='subcommand')`
- Existing subcommands: `tailwind-config`, `export-colors`, `list-presets`, `generate-examples`, `shadcn-import`, `shadcn-export`, `init`
- Pattern: each subcommand has its own `handle_<subcommand>` method
- New `create-theme` subcommand will follow this pattern

### template_resolver.py
- Resolves templates via fallback chain: `djust_theming/themes/{theme_name}/components/{component}.html` -> `djust_theming/components/{component}.html`
- `theme_name` comes from `ThemeState.theme` (the design system name: material, ios, fluent, etc.)
- Integration point: user themes should add a third candidate at highest priority: `{THEMES_DIR}/{manifest_name}/components/{component}.html`

### presets.py - ThemePreset
- `ThemePreset` dataclass: `name`, `display_name`, `light: ThemeTokens`, `dark: ThemeTokens`, `description`, `radius`
- `ThemeTokens` dataclass has ~30 ColorScale fields (background, foreground, primary, secondary, muted, accent, destructive, success, warning, info, link, code, selection, border, input, ring + foreground pairs)
- `THEME_PRESETS` dict: 19 presets (default, shadcn, blue, green, purple, orange, rose, natural20, catppuccin, rose_pine, tokyo_night, nord, synthwave, cyberpunk, outrun, forest, amber, slate, nebula)

### theme_packs.py - DESIGN_SYSTEMS
- Valid design system names: material, ios, fluent, playful, corporate, dense, minimalist, neo_brutalist, elegant, retro

### manager.py - DEFAULT_CONFIG
- Config keys: theme (design system), preset (color preset), default_mode, persist_in_session, session_key, enable_dark_mode, css_prefix, use_css_layers, css_layer_order
- Config read from `settings.LIVEVIEW_CONFIG['theme']`

---

## Design: theme.toml Schema

```toml
[theme]
name = "my-theme"
version = "0.1.0"
description = "A custom theme for my project"
author = "Developer Name"
license = "MIT"

[extends]
base = "default"  # Optional: base theme to inherit from (another theme dir name)

[tokens]
preset = "blue"                    # One of the 19 THEME_PRESETS keys
design_system = "material"         # One of the 10 DESIGN_SYSTEMS keys

[tokens.overrides]
# CSS custom property overrides (applied after preset tokens)
# Keys are CSS custom property names WITHOUT the -- prefix
# Values are raw CSS values
primary = "220 90% 56%"            # HSL values (matches existing format)
primary-foreground = "0 0% 100%"
radius = "0.75"                    # Border radius in rem

[static]
css = ["static/css/custom.css"]    # Additional CSS files to include
fonts = ["static/fonts/inter.woff2"]  # Font files
```

### Validation Rules
- `[theme].name`: required, must be valid Python/filesystem identifier (lowercase, hyphens, underscores)
- `[theme].version`: required, semver string
- `[tokens].preset`: must exist in `THEME_PRESETS`
- `[tokens].design_system`: must exist in `DESIGN_SYSTEMS`
- `[extends].base`: if present, the base theme directory must exist
- `[tokens.overrides]` keys: validated against known CSS custom property names from ThemeTokens
- `[static].css` / `[static].fonts`: paths relative to theme directory

---

## Design: ThemeManifest dataclass (manifest.py)

```python
# djust_theming/manifest.py

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

@dataclass
class ThemeManifest:
    """Parsed and validated theme.toml manifest."""

    # [theme] section
    name: str
    version: str
    description: str = ""
    author: str = ""
    license: str = ""

    # [extends] section
    base: Optional[str] = None

    # [tokens] section
    preset: str = "default"
    design_system: str = "material"
    overrides: dict[str, str] = field(default_factory=dict)

    # [static] section
    css: list[str] = field(default_factory=list)
    fonts: list[str] = field(default_factory=list)

    # Internal (not from TOML)
    path: Optional[Path] = None  # Directory containing theme.toml

    @classmethod
    def from_toml(cls, toml_path: Path) -> "ThemeManifest":
        """Parse and validate a theme.toml file."""
        ...

    def validate(self) -> list[str]:
        """Return list of validation error messages (empty = valid)."""
        ...

    def to_toml(self) -> str:
        """Serialize back to TOML string (for scaffold generation)."""
        ...
```

### Parsing
- Uses `tomllib` (stdlib Python 3.11+) to parse TOML
- Validates all fields against known preset/design_system names
- Returns typed dataclass for downstream use

### Integration with template_resolver.py
- The manifest `name` field becomes the theme lookup name
- Template resolution chain becomes 3 levels:
  1. `{THEMES_DIR}/{manifest.name}/components/{component}.html` (user theme override)
  2. `djust_theming/themes/{design_system}/components/{component}.html` (design system)
  3. `djust_theming/components/{component}.html` (default fallback)
- This requires a small change to `template_resolver.py` to accept an optional `user_theme_dir`
- The manifest's `design_system` field feeds into the existing `state.theme` used by the resolver

---

## Design: create-theme Scaffold Command

### Invocation
```bash
python manage.py djust_theme create-theme my-theme --base default --preset blue --design-system material
```

### Arguments
| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `theme_name` | positional | required | Theme directory name |
| `--base` | optional | None | Base theme to extend |
| `--preset` | optional | "default" | Color preset from THEME_PRESETS |
| `--design-system` | optional | "material" | Design system from DESIGN_SYSTEMS |
| `--dir` | optional | from config | Override THEMES_DIR |

### Generated Directory Structure
```
themes/my-theme/
  theme.toml           # Manifest with provided options
  tokens.css           # CSS custom property overrides (empty/commented template)
  components/          # Component template overrides (empty dir with .gitkeep)
  layouts/             # Layout template overrides (empty dir with .gitkeep)
  pages/               # Page template overrides (empty dir with .gitkeep)
  static/
    css/               # Custom CSS (empty dir with .gitkeep)
    fonts/             # Custom fonts (empty dir with .gitkeep)
```

### Theme Directory Location
- Configurable via `DJUST_THEMING['THEMES_DIR']` (new config key added to DEFAULT_CONFIG)
- Default: `'themes/'` relative to `settings.BASE_DIR`
- Resolved at runtime: `Path(settings.BASE_DIR) / config['THEMES_DIR']`

### tokens.css Template Content
```css
/* Theme: my-theme
 * Preset: blue | Design System: material
 *
 * Override CSS custom properties here.
 * These are applied AFTER the preset tokens.
 *
 * Example:
 *   :root {
 *     --primary: 220 90% 56%;
 *     --radius: 0.75rem;
 *   }
 */
```

---

## Implementation Plan (Files to Create/Modify)

### New Files

1. **`djust_theming/manifest.py`** (~120 lines)
   - `ThemeManifest` dataclass
   - `from_toml(path)` classmethod - parse + validate
   - `to_toml()` method - serialize for scaffold
   - `validate()` method - check preset/design_system/name validity
   - `load_theme_manifests(themes_dir)` - discover + load all themes

2. **`tests/test_manifest.py`** (~150 lines)
   - Test TOML parsing with valid/invalid manifests
   - Test validation (bad preset, bad design_system, missing name)
   - Test `to_toml()` round-trip
   - Test `load_theme_manifests()` discovery

3. **`tests/test_create_theme_command.py`** (~120 lines)
   - Test scaffold creates correct directory structure
   - Test theme.toml content matches arguments
   - Test validation rejects bad preset/design_system names
   - Test `--dir` override
   - Test error when theme already exists

### Modified Files

4. **`djust_theming/management/commands/djust_theme.py`** (add ~80 lines)
   - Add `create-theme` subparser with arguments
   - Add `handle_create_theme(options)` method
   - Uses `ThemeManifest.to_toml()` to generate theme.toml
   - Creates directory structure with `.gitkeep` files

5. **`djust_theming/manager.py`** (add ~5 lines)
   - Add `'themes_dir': 'themes/'` to `DEFAULT_CONFIG`

6. **`djust_theming/__init__.py`** (add import)
   - Export `ThemeManifest` from public API

### NOT Modified (Phase 1.2/1.3 only - template_resolver integration is Phase 1.4+)

- `template_resolver.py` - will be updated in a later phase when manifest-based resolution is wired up
- `presets.py` - manifest references presets by name, no changes needed
- `theme_packs.py` - manifest references design systems by name, no changes needed

---

## Dependency Graph

```
manifest.py (new)
  ├── reads: presets.THEME_PRESETS (validation)
  ├── reads: theme_packs.DESIGN_SYSTEMS (validation)
  └── uses: tomllib (stdlib)

djust_theme.py create-theme (modified)
  ├── uses: manifest.ThemeManifest
  ├── reads: manager.get_theme_config() for THEMES_DIR
  └── creates: directory structure + files

manager.py (modified)
  └── adds: themes_dir to DEFAULT_CONFIG
```

---

## Test Strategy

1. Unit tests for `ThemeManifest.from_toml()` with fixture TOML files
2. Unit tests for `ThemeManifest.validate()` covering all validation rules
3. Integration test calling `create-theme` command and verifying output
4. Edge cases: duplicate theme name, invalid characters in name, missing required fields

---

## Open Questions (Resolved)

1. **Should manifest.py import from presets/theme_packs at parse time?** Yes - validation needs access to valid names. Lazy import to avoid circular deps.
2. **TOML library?** `tomllib` (stdlib 3.11+). Add `tomli` as fallback for 3.10 if needed (check pyproject.toml python-requires).
3. **Should create-theme refuse to overwrite?** Yes - error if directory already exists, add `--force` flag for override.
