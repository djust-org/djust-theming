# Plan: Phase 1.4 + 1.5 + I25 -- Theme Registry + Validation + Dynamic Preset API

## Status
- **Branch**: `task/1.4-1.5-I25-registry-validation` (from `main`)
- **ENV_OK**: 238 tests passing, venv installed
- **CODE_CHANGES**: Fresh branch, zero delta from main
- **MERGE_CLEAN**: No conflicts

---

## Current State Analysis

### What exists today

1. **presets.py** -- `THEME_PRESETS: dict[str, ThemePreset]` (19 presets) with `get_preset(name)` and `list_presets()` module-level functions. All consumers import `THEME_PRESETS` directly.

2. **theme_packs.py** -- `DESIGN_SYSTEMS: Dict[str, DesignSystem]` (11 design systems) with `get_design_system(name)` and `get_all_design_systems()` module-level functions. Also imported directly by consumers.

3. **manager.py** -- `ThemeManager.get_state()` imports `DESIGN_SYSTEMS` at method level and validates `theme not in DESIGN_SYSTEMS`. `set_theme()` also validates against `DESIGN_SYSTEMS`. `set_preset()` validates against `THEME_PRESETS`.

4. **checks.py** -- `check_preset_valid` (E002) validates config preset against `THEME_PRESETS`. `check_design_system_valid` (E003) validates config theme against `DESIGN_SYSTEMS`. Both import dicts directly at module level.

5. **manifest.py** -- `ThemeManifest.validate()` checks `self.preset not in THEME_PRESETS` and `self.design_system not in DESIGN_SYSTEMS` (imports at method level). `load_theme_manifests()` discovers `theme.toml` files in a themes directory.

6. **template_resolver.py** -- Uses `ThemeManager.get_state().theme` to build template paths. No direct dict access. Already indirectly wired through ThemeManager.

7. **apps.py** -- `ready()` only imports `checks` to trigger `@register`. No discovery or registry population.

8. **management/commands/djust_theme.py** -- Has `create-theme` subcommand that scaffolds themes. Validates against `THEME_PRESETS` and `DESIGN_SYSTEMS` directly. Has `list-presets` subcommand.

### Direct dict access points (to be rewired)

| File | Access | What it reads |
|------|--------|---------------|
| `manager.py:162` | `from .theme_packs import DESIGN_SYSTEMS` | `get_state()` validation |
| `manager.py:199` | `theme not in DESIGN_SYSTEMS` | Fallback to "material" |
| `manager.py:203` | `preset not in THEME_PRESETS` | Fallback to "default" |
| `manager.py:231-233` | `from .theme_packs import DESIGN_SYSTEMS` | `set_theme()` validation |
| `manager.py:251` | `preset_name not in THEME_PRESETS` | `set_preset()` validation |
| `manager.py:312` | `for preset in THEME_PRESETS.values()` | `get_available_presets()` |
| `checks.py:7-9` | Module-level imports | E002/E003 checks |
| `checks.py:35` | `for preset_name, preset in THEME_PRESETS.items()` | W001 contrast check |
| `checks.py:131` | `preset not in THEME_PRESETS` | E002 |
| `checks.py:152` | `theme not in DESIGN_SYSTEMS` | E003 |
| `manifest.py:142-143` | `from .presets import THEME_PRESETS` etc. | `validate()` |
| `manifest.py:154` | `self.preset not in THEME_PRESETS` | validate preset |
| `manifest.py:161` | `self.design_system not in DESIGN_SYSTEMS` | validate design system |
| `djust_theme.py:12` | `from djust_theming.presets import THEME_PRESETS` | Multiple subcommands |
| `djust_theme.py:534` | `from djust_theming.theme_packs import DESIGN_SYSTEMS` | create-theme |

---

## Design

### 1. ThemeRegistry (new file: `registry.py`)

A thread-safe singleton that is the single source of truth for all registered presets and design systems (themes).

```python
# registry.py
import threading
from typing import Optional

class ThemeRegistry:
    """Singleton registry for theme presets and design systems.

    Thread-safe. Populated during AppConfig.ready() via discover().
    Third-party apps call register_preset()/register_theme() in their own ready().
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._presets = {}
                    cls._instance._themes = {}  # design systems
                    cls._instance._manifests = {}  # ThemeManifest objects
                    cls._instance._discovered = False
        return cls._instance

    # -- Registration API --

    def register_preset(self, name: str, preset) -> None:
        """Register a color preset. Overwrites if name exists."""
        with self._lock:
            self._presets[name] = preset

    def register_theme(self, name: str, theme) -> None:
        """Register a design system. Overwrites if name exists."""
        with self._lock:
            self._themes[name] = theme

    def register_manifest(self, name: str, manifest) -> None:
        """Register a parsed ThemeManifest."""
        with self._lock:
            self._manifests[name] = manifest

    # -- Lookup API --

    def get_preset(self, name: str, default=None):
        return self._presets.get(name, default)

    def get_theme(self, name: str, default=None):
        return self._themes.get(name, default)

    def get_manifest(self, name: str) -> Optional['ThemeManifest']:
        return self._manifests.get(name)

    def has_preset(self, name: str) -> bool:
        return name in self._presets

    def has_theme(self, name: str) -> bool:
        return name in self._themes

    def list_presets(self) -> dict:
        return dict(self._presets)

    def list_themes(self) -> dict:
        return dict(self._themes)

    def list_manifests(self) -> dict:
        return dict(self._manifests)

    # -- Discovery --

    def discover(self) -> None:
        """Populate registry from all sources. Called from apps.py ready()."""
        if self._discovered:
            return
        with self._lock:
            if self._discovered:
                return
            self._do_discover()
            self._discovered = True

    def _do_discover(self):
        """Internal: load from built-in dicts, DJUST_THEMES setting, themes_dir."""
        # 1. Built-in presets
        from .presets import THEME_PRESETS
        for name, preset in THEME_PRESETS.items():
            self._presets[name] = preset

        # 2. Built-in design systems
        from .theme_packs import DESIGN_SYSTEMS
        for name, ds in DESIGN_SYSTEMS.items():
            self._themes[name] = ds

        # 3. DJUST_THEMES setting (pip-installed theme packages)
        self._discover_from_settings()

        # 4. themes_dir (convention-based, from theme.toml files)
        self._discover_from_themes_dir()

    def _discover_from_settings(self):
        """Load themes from DJUST_THEMES setting."""
        from django.conf import settings
        theme_packages = getattr(settings, 'DJUST_THEMES', [])
        for package_name in theme_packages:
            try:
                self._load_theme_package(package_name)
            except Exception:
                import logging
                logging.getLogger(__name__).warning(
                    "Failed to load theme package '%s'", package_name
                )

    def _load_theme_package(self, package_name: str):
        """Load a pip-installed theme package by importing its module."""
        import importlib
        mod = importlib.import_module(package_name)
        # Convention: package exposes get_theme_manifest() -> ThemeManifest
        if hasattr(mod, 'get_theme_manifest'):
            manifest = mod.get_theme_manifest()
            self._manifests[manifest.name] = manifest
        # Convention: package exposes PRESETS dict
        if hasattr(mod, 'PRESETS'):
            for name, preset in mod.PRESETS.items():
                self._presets[name] = preset
        # Convention: package exposes DESIGN_SYSTEMS dict
        if hasattr(mod, 'DESIGN_SYSTEMS'):
            for name, ds in mod.DESIGN_SYSTEMS.items():
                self._themes[name] = ds

    def _discover_from_themes_dir(self):
        """Load theme.toml manifests from configured themes_dir."""
        from pathlib import Path
        from django.conf import settings
        from .manager import get_theme_config

        config = get_theme_config()
        themes_dir_rel = config.get('themes_dir', 'themes/')
        base_dir = getattr(settings, 'BASE_DIR', None)
        if not base_dir:
            return

        themes_dir = Path(base_dir) / themes_dir_rel
        if not themes_dir.is_dir():
            return

        from .manifest import load_theme_manifests
        for manifest in load_theme_manifests(themes_dir):
            self._manifests[manifest.name] = manifest

    # -- Reset (for testing) --

    @classmethod
    def _reset(cls):
        """Reset singleton. For tests only."""
        with cls._lock:
            cls._instance = None


# Module-level convenience accessor
def get_registry() -> ThemeRegistry:
    """Get the global ThemeRegistry singleton."""
    return ThemeRegistry()
```

**Key design decisions**:
- Singleton pattern with double-checked locking for thread safety
- `_reset()` classmethod for test isolation
- `discover()` is idempotent (runs once, guarded by `_discovered` flag)
- Three registration categories: presets, themes (design systems), manifests
- `_load_theme_package` uses conventions: `get_theme_manifest()`, `PRESETS`, `DESIGN_SYSTEMS`
- No breaking changes to existing module-level dicts -- they remain as the authoritative initial source

### 2. Wire ThemeManager to use ThemeRegistry

Replace direct `DESIGN_SYSTEMS` and `THEME_PRESETS` imports in `manager.py` with registry lookups:

| Current code | New code |
|---|---|
| `from .theme_packs import DESIGN_SYSTEMS` | `from .registry import get_registry` |
| `theme not in DESIGN_SYSTEMS` | `not get_registry().has_theme(theme)` |
| `preset not in THEME_PRESETS` | `not get_registry().has_preset(preset)` |
| `theme_name not in DESIGN_SYSTEMS` in `set_theme()` | `not get_registry().has_theme(theme_name)` |
| `preset_name not in THEME_PRESETS` in `set_preset()` | `not get_registry().has_preset(preset_name)` |
| `for preset in THEME_PRESETS.values()` in `get_available_presets()` | `for preset in get_registry().list_presets().values()` |

**Keep** the `from .presets import THEME_PRESETS, ThemePreset, get_preset` import at the top for `ThemePreset` type and `get_preset` function (which is also used for fallback). The `get_preset` convenience import can remain since the registry's `get_preset` has a different signature (returns None by default).

### 3. Wire checks.py to use ThemeRegistry

| Current code | New code |
|---|---|
| `from .presets import THEME_PRESETS` (module-level) | `from .registry import get_registry` |
| `from .theme_packs import DESIGN_SYSTEMS` (module-level) | Remove (use registry) |
| `for preset_name, preset in THEME_PRESETS.items()` (W001) | `for preset_name, preset in get_registry().list_presets().items()` |
| `preset not in THEME_PRESETS` (E002) | `not get_registry().has_preset(preset)` |
| `theme not in DESIGN_SYSTEMS` (E003) | `not get_registry().has_theme(theme)` |

Note: `from .presets import THEME_PRESETS` import at module level must remain for `check_preset_contrast` which iterates presets. We'll switch to `get_registry().list_presets()` instead. The `from .accessibility import AccessibilityValidator` stays.

### 4. Wire manifest.py validate() to use ThemeRegistry

Replace:
```python
def validate(self) -> list[str]:
    from .presets import THEME_PRESETS
    from .theme_packs import DESIGN_SYSTEMS
    ...
    if self.preset not in THEME_PRESETS:
    ...
    if self.design_system not in DESIGN_SYSTEMS:
```

With:
```python
def validate(self) -> list[str]:
    from .registry import get_registry
    registry = get_registry()
    ...
    if not registry.has_preset(self.preset):
        valid = ", ".join(sorted(registry.list_presets().keys()))
    ...
    if not registry.has_theme(self.design_system):
        valid = ", ".join(sorted(registry.list_themes().keys()))
```

### 5. Wire apps.py ready() to call registry.discover()

```python
def ready(self):
    from . import checks  # noqa: F401
    from .registry import get_registry
    get_registry().discover()
```

### 6. validate-theme management command

Add a `validate-theme` subcommand to the existing `djust_theme.py` command.

```
python manage.py djust_theme validate-theme my-theme
python manage.py djust_theme validate-theme --all
python manage.py djust_theme validate-theme --dir /path/to/themes/
```

**Validation checks**:
1. **TOML parsing** -- valid TOML file, no syntax errors
2. **Required fields** -- `[theme]` section with `name` and `version`
3. **Name format** -- matches `[a-z0-9][a-z0-9-]*` pattern
4. **Preset exists in registry** -- `tokens.preset` resolves via `get_registry().has_preset()`
5. **Design system exists in registry** -- `tokens.design_system` resolves via `get_registry().has_theme()`
6. **Static files exist** -- each entry in `static.css` and `static.fonts` resolves to an existing file relative to theme directory
7. **Token overrides are valid CSS property names** -- keys in `tokens.overrides` match known CSS custom property names from the token set (e.g., `primary`, `background`, `foreground`, etc.)
8. **Templates exist** (if any referenced in components/ dir) -- basic directory presence check

**Output**: Structured report with pass/fail per check, error/warning severity.

Implementation in `djust_theme.py`:
```python
# Add to add_arguments:
validate_parser = subparsers.add_parser(
    'validate-theme',
    help='Validate a theme manifest and its referenced files'
)
validate_parser.add_argument('theme_name', nargs='?', help='Theme name to validate')
validate_parser.add_argument('--all', action='store_true', help='Validate all discovered themes')
validate_parser.add_argument('--dir', type=str, help='Override themes directory')

# Add to handle():
elif subcommand == 'validate-theme':
    self.handle_validate_theme(options)
```

The `handle_validate_theme` method will:
1. Resolve the theme.toml path (from registry manifest, or by scanning themes_dir)
2. Call `ThemeManifest.from_toml()` (catches parse errors)
3. Call `manifest.validate()` (uses registry for preset/design system checks)
4. Run additional file existence checks (static files, template dirs)
5. Run token override validation (check against known ThemeTokens field names)
6. Print results with color-coded pass/fail

### 7. Update __init__.py exports

Add `ThemeRegistry` and `get_registry` to `__all__`:
```python
from .registry import ThemeRegistry, get_registry

__all__ = [
    ...
    # Registry
    "ThemeRegistry",
    "get_registry",
    ...
]
```

### 8. Known CSS token names for override validation

Extract the valid token names from `ThemeTokens` dataclass fields. The `validate-theme` command will use `ThemeTokens.__dataclass_fields__` to get the list of valid override keys. This avoids hardcoding a list.

---

## Files to Create

| File | Purpose |
|------|---------|
| `djust_theming/registry.py` | ThemeRegistry singleton |
| `tests/test_registry.py` | Registry unit tests |
| `tests/test_validate_theme_command.py` | validate-theme command tests |

## Files to Modify

| File | Changes |
|------|---------|
| `djust_theming/apps.py` | Add `get_registry().discover()` call in `ready()` |
| `djust_theming/manager.py` | Replace direct dict access with registry lookups |
| `djust_theming/checks.py` | Replace direct dict access with registry lookups |
| `djust_theming/manifest.py` | Replace direct dict access in `validate()` with registry lookups |
| `djust_theming/management/commands/djust_theme.py` | Add `validate-theme` subcommand, wire existing subcommands through registry |
| `djust_theming/__init__.py` | Export `ThemeRegistry` and `get_registry` |

## Files NOT Modified

| File | Reason |
|------|--------|
| `djust_theming/presets.py` | `THEME_PRESETS` dict stays as-is; registry reads from it |
| `djust_theming/theme_packs.py` | `DESIGN_SYSTEMS` dict stays as-is; registry reads from it |
| `djust_theming/template_resolver.py` | Already wired through ThemeManager; no direct dict access |
| `djust_theming/views.py` | Uses ThemeManager; no direct dict access |

---

## Test Plan

### test_registry.py

1. **test_singleton** -- Two calls to `ThemeRegistry()` return same instance
2. **test_register_preset** -- `register_preset("custom", preset)` then `get_preset("custom")` returns it
3. **test_register_theme** -- `register_theme("custom", ds)` then `get_theme("custom")` returns it
4. **test_register_manifest** -- register and retrieve a ThemeManifest
5. **test_has_preset / test_has_theme** -- boolean checks
6. **test_list_presets / test_list_themes** -- returns dict copies
7. **test_discover_populates_builtins** -- after `discover()`, all 19 presets and 11 design systems present
8. **test_discover_idempotent** -- calling `discover()` twice doesn't duplicate or error
9. **test_discover_themes_dir** -- with a tmp dir containing theme.toml, manifests are loaded
10. **test_discover_djust_themes_setting** -- mock a package in DJUST_THEMES, verify it loads
11. **test_thread_safety** -- concurrent register/get calls don't raise
12. **test_reset** -- `_reset()` clears singleton, new instance is empty
13. **test_overwrite_preset** -- registering same name overwrites
14. **test_get_preset_default** -- `get_preset("nonexistent")` returns None (or provided default)

### test_validate_theme_command.py

1. **test_validate_valid_theme** -- scaffolded theme passes all checks
2. **test_validate_missing_toml** -- theme dir without theme.toml reports error
3. **test_validate_invalid_toml** -- malformed TOML reports parse error
4. **test_validate_missing_name** -- TOML without `[theme].name` reports error
5. **test_validate_bad_preset** -- preset not in registry reports error
6. **test_validate_bad_design_system** -- design system not in registry reports error
7. **test_validate_missing_static_file** -- referenced CSS file doesn't exist reports warning
8. **test_validate_invalid_token_override** -- override key not in ThemeTokens reports warning
9. **test_validate_all_flag** -- `--all` validates all discovered themes
10. **test_validate_valid_token_override** -- override with valid key passes

### Existing test updates

- **test_checks.py** -- May need minor updates if E002/E003 error messages change (they shouldn't, only the source of truth changes)
- **test_manifest.py** -- `validate()` tests may need registry to be populated first (add `get_registry().discover()` in fixtures or setUp)
- **test_create_theme_command.py** -- Verify still works with registry

---

## Implementation Order

1. Create `registry.py` with ThemeRegistry class
2. Create `tests/test_registry.py` and verify registry works standalone
3. Update `apps.py` to call `discover()` in `ready()`
4. Update `manager.py` to use registry (rewire 5 access points)
5. Update `checks.py` to use registry (rewire 4 access points)
6. Update `manifest.py` `validate()` to use registry (rewire 2 access points)
7. Run existing tests -- fix any failures from registry not being populated in test fixtures
8. Add `validate-theme` subcommand to `djust_theme.py`
9. Create `tests/test_validate_theme_command.py`
10. Update `__init__.py` exports
11. Update management command to use registry for existing subcommands
12. Full test run, verify 238+ tests pass

---

## Risk Assessment

- **Low risk**: Registry is additive; existing dicts remain untouched
- **Medium risk**: Test fixtures may need registry population (conftest.py update)
- **Low risk**: Thread safety -- Django's `ready()` runs in main thread; registry is populated before request handling starts. Lock protects concurrent `register_preset()` calls from third-party apps.
- **No breaking changes**: All public APIs remain compatible. `THEME_PRESETS` and `DESIGN_SYSTEMS` dicts still work for direct access (they're the source data). Registry is the new recommended API.
