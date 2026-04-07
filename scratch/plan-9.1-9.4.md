# Plan: Phase 9.1 + 9.4 — Theme Author Guide + Migration Guide + check-compat command

## Overview

Three deliverables:
1. **Getting Started Guide (9.1)** — `docs/getting-started.md`
2. **BREAKING_CHANGES.md (9.4)** — `docs/BREAKING_CHANGES.md`
3. **check-compat command (9.4)** — `manage.py djust_theme check-compat <theme-name>`

## 1. Getting Started Guide (`docs/getting-started.md`)

"Create your first theme in 10 minutes" tutorial:

- **Step 1:** Create a theme with `manage.py djust_theme create-theme my-theme --preset blue`
  - Show the generated directory structure
- **Step 2:** Override button + card templates
  - Copy default templates, modify CSS classes/markup
  - Show the template resolution fallback chain
- **Step 3:** Set custom tokens in `tokens.css`
  - Override `--primary`, `--radius`, etc.
- **Step 4:** Preview in the gallery
  - Visit `/theming/gallery/?preset=...`
  - Use the live editor for real-time tweaks
- **Step 5:** Package and publish
  - `create-package`, `pip install -e .`, `twine upload`

Code blocks for each step. References to existing docs (theme-authoring.md, customization.md).

## 2. BREAKING_CHANGES.md (`docs/BREAKING_CHANGES.md`)

Format:
```
# Breaking Changes

## Format

Each entry: version, component, what changed, migration steps.

## v1.0 (Baseline)

Current component contracts are the v1.0 baseline.
No breaking changes yet — this document will track future changes.

### Contract Summary

Table listing each component, its required elements, required context vars,
and available slots (derived from contracts.py COMPONENT_CONTRACTS).
```

This gives theme authors a reference for what the contracts look like at v1.0,
so future changes can be documented as diffs.

## 3. check-compat command

### Design

New subcommand: `manage.py djust_theme check-compat <theme-name>`

**Flags:**
- `theme-name` (positional) — theme directory name
- `--dir` — override themes directory
- `--all` — check all themes

**Logic (in `djust_theming/compat.py`):**

`check_theme_compat(theme_dir: Path) -> list[CompatIssue]`

1. Find all `.html` files in theme's `components/` directory (these are overrides)
2. For each override file, derive component name from filename (e.g., `button.html` -> `button`)
3. Look up `COMPONENT_CONTRACTS[component_name]`
4. Read the template source
5. Check:
   - **Required elements:** For each `RequiredElement`, check that the tag appears in the template (simple regex/string search for `<tag` and any required attrs)
   - **Required context vars:** For each required `ContextVar`, check that `{{ var_name }}` or `{% if var_name %}` or similar appears in template
   - **Available slots:** Report slots from the contract that are not referenced in the template (as info/warning, not error, since slots are optional)
6. Return list of `CompatIssue(component, severity, message)`

### CompatIssue dataclass

```python
@dataclass
class CompatIssue:
    component: str
    severity: str  # "error", "warning", "info"
    message: str
```

### Command integration

Add `check-compat` subparser to `djust_theme.py`. Handler calls `check_theme_compat()` for each theme directory, prints results with color coding.

### Tests (`tests/test_check_compat.py`)

TDD approach — write tests first:

1. **test_no_overrides_returns_empty** — theme with no component overrides -> no issues
2. **test_valid_button_override_no_issues** — button.html with `<button>` and `{{ text }}` -> no issues
3. **test_missing_required_element** — button.html without `<button>` -> error
4. **test_missing_required_attr** — alert.html with `<div>` but no `role="alert"` -> error
5. **test_missing_required_context_var** — button.html without `{{ text }}` -> error
6. **test_unused_slot_warning** — button.html that doesn't reference `slot_icon` -> info
7. **test_unknown_component_skipped** — `foobar.html` in components/ -> warning about no contract
8. **test_command_output_pass** — invoke via management command, check stdout for PASS
9. **test_command_output_errors** — invoke via management command, check stdout for ERROR lines
10. **test_multiple_required_elements** — dropdown needs `<div>` + `<button aria-haspopup="true">` -> check both
11. **test_check_compat_all_flag** — `--all` validates all themes in directory

## File Changes

| File | Action |
|------|--------|
| `docs/getting-started.md` | Create |
| `docs/BREAKING_CHANGES.md` | Create |
| `djust_theming/compat.py` | Create |
| `djust_theming/management/commands/djust_theme.py` | Add check-compat subcommand |
| `tests/test_check_compat.py` | Create (TDD) |
| `CHANGELOG.md` | Update |
