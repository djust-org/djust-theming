# Migrating from `djust-theming` to `djust.theming`

This repo is deprecated. All functionality is now in the `djust` core package.

## 1. Replace the install

```diff
- pip install djust-theming
+ pip install djust
```

## 2. Update imports

Grep-replace the top-level package name:

```bash
# macOS:
grep -rl 'djust_theming' . | xargs sed -i '' 's/djust_theming/djust.theming/g'
# Linux:
grep -rl 'djust_theming' . | xargs sed -i     's/djust_theming/djust.theming/g'
```

## 3. Import mapping

| Before                                    | After                                 |
| ----------------------------------------- | ------------------------------------- |
| `from djust_theming import X`             | `from djust.theming import X`         |
| `import djust_theming`                    | `from djust import theming`           |
| `'djust_theming'` in `INSTALLED_APPS`     | `'djust.theming'`                     |

All public names (`ThemeManager`, `ThemeState`, `ThemeMixin`, `ThemeSwitcher`, `ThemeCSSGenerator`, `ThemeRegistry`, `get_registry`, `register_preset`, `register_design_system`, `register_theme_pack`, `ThemePreset`, `ThemeTokens`, `ColorScale`, `THEME_PRESETS`, `DEFAULT_THEME`, `BLUE_THEME`, `GREEN_THEME`, `PURPLE_THEME`, `ORANGE_THEME`, `ROSE_THEME`, `PaletteGenerator`, Tailwind helpers, color utilities, cache helpers) are re-exported from `djust.theming` with the same signatures.

## 4. Remove the old dep

Once imports are migrated and tests pass, remove `djust-theming` from your `pyproject.toml` / `requirements.txt`. The shim package depends on `djust>=0.5.6rc1` so djust is already installed.
