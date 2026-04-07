# Plan: Phase 5.3 -- create-package management command

## Goal
Add a `create-package` subcommand to `djust_theme` that generates a pip-installable
theme package directory with proper Python packaging structure.

## Command Interface
```
python manage.py djust_theme create-package <package-name> \
    [--author "Name"] [--preset blue] [--design-system material] \
    [--dir <output-dir>] [--force]
```

## Generated Structure
```
djust-theme-<name>/
  pyproject.toml
  README.md
  LICENSE
  djust_theme_<name>/
    __init__.py
    theme.toml
    tokens.css
    templates/
      djust_theming/
        themes/
          <name>/
            components/
              .gitkeep
    static/
      djust_theme_<name>/
        css/
          .gitkeep
        fonts/
          .gitkeep
```

## Validation Rules
- Package name: lowercase letters, digits, hyphens only (`^[a-z0-9][a-z0-9-]*$`)
- No path traversal (same regex handles it)
- Preset must exist in registry
- Design system must exist in registry
- Rejects overwrite unless --force

## Key Decisions
- Package directory name: `djust-theme-{name}` (hyphenated, pip convention)
- Python package name: `djust_theme_{name}` (underscored, Python convention)
- pyproject.toml includes `djust-theming>=0.3.0` as dependency
- README.md includes installation + INSTALLED_APPS instructions
- LICENSE defaults to MIT
- theme.toml uses ThemeManifest.to_toml() (reuse existing serialization)
- tokens.css uses same template as create-theme command

## Implementation Steps

### 1. Tests (TDD) -- `tests/test_create_package_command.py`
Test classes:
- **TestPackageStructure** -- verifies all files/dirs are created
  - test_creates_package_root_directory
  - test_creates_pyproject_toml
  - test_creates_readme
  - test_creates_license
  - test_creates_python_package_dir_with_init
  - test_creates_theme_toml
  - test_creates_tokens_css
  - test_creates_template_dirs_with_gitkeep
  - test_creates_static_dirs_with_gitkeep
- **TestPyprojectContent** -- verifies pyproject.toml fields
  - test_pyproject_has_package_name
  - test_pyproject_has_author
  - test_pyproject_has_djust_theming_dependency
  - test_pyproject_has_correct_python_package_name
- **TestThemeTomlContent** -- verifies theme.toml
  - test_theme_toml_has_correct_name
  - test_theme_toml_has_preset
  - test_theme_toml_has_design_system
- **TestCreatePackageValidation** -- input validation
  - test_rejects_invalid_name
  - test_rejects_path_traversal
  - test_rejects_invalid_preset
  - test_rejects_invalid_design_system
  - test_error_when_package_exists
  - test_force_overwrites_existing
- **TestOutputDir** -- output location
  - test_creates_in_current_dir_by_default (uses cwd)
  - test_dir_override

### 2. Command Implementation -- modify `djust_theme.py`
- Add `create-package` subparser with arguments
- Add `handle_create_package()` method
- Wire into `handle()` dispatch

### 3. CHANGELOG entry
Add entry under [Unreleased] / Added.

## Files Changed
- `djust_theming/management/commands/djust_theme.py` -- add subcommand
- `tests/test_create_package_command.py` -- new test file
- `CHANGELOG.md` -- add entry
