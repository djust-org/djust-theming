# djust-theming Project Memory

## Project Structure
- Library: `djust_theming/` — theming layer for djust framework
- Example project: `example_project/` — demo Django app
- Tests: `tests/` — pytest-based, 5 tests in `tests/test_presets.py`
- Scratch: `scratch/` — temporary scripts (committed per CLAUDE.md convention)
- CI: `.github/workflows/` — test.yml, publish.yml, release.yml

## Key Files
- `djust_theming/components.py` — uses `mark_safe` (lines 72, 119, 184, 205, 230)
- `djust_theming/templatetags/theme_tags.py` — uses `mark_safe` (lines 115-117, 147, 202, 229)
- `djust_theming/context_processors.py` — uses `mark_safe` (lines 64-65)
- `djust_theming/templatetags/theme_components.py` — uses `mark_safe` (line 148)
- `djust_theming/inspector.py` — uses `@csrf_exempt` (line 273); needs auth controls confirmed

## Security Notes (Pre-existing, not yet audited)
- Multiple `mark_safe` usages in theming components — need audit to confirm no user-controlled data flows in
- `@csrf_exempt` in inspector.py — confirm alternative auth/authorization exists
- These were flagged by security scan on 2026-02-27; unresolved

## CI / GitHub Actions
- All three workflows use `actions/setup-python@v6` (updated from v5 in task/259)
- Python matrix: 3.10, 3.11, 3.12
- Build Python: 3.12
- `gh` CLI not available in the shell environment — PR creation must be done manually

## Workflow Notes
- `manage.py add_task` and `manage.py memory_write` commands referenced in pipeline instructions are NOT available in this project (no djust-orchestrator installed here)
- Version: currently 1.1.0 (bumped in task/259 branch alongside actions/setup-python v6 upgrade)

## Pipeline Learnings (task/259, 2026-02-27)
- For Dependabot bump PRs: consider approving/merging the existing PR directly rather than creating a parallel branch — avoids duplicate PR confusion
- `gh` CLI absence should be detected in Environment Check stage, not discovered at Commit & PR stage
- `scratch/` test files for structural invariants (CI version checks) border on useful permanent tests — move to `tests/` or clean up before committing
- Cost was $1.96 for a 3-line CI change — lightweight mode warranted for trivial Dependabot bumps
