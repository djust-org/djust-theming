# Analysis: I3 — ThemeManager Per-Request Caching

## Problem

`ThemeManager` is reinstantiated on every template tag call within a single request. A typical page using `{% theme_head %}`, `{% theme_switcher %}`, `{% theme_mode_toggle %}`, and `{% theme_preset_selector %}` creates **4+ separate ThemeManager instances**, each re-reading `get_theme_config()` from Django settings and potentially re-reading session/cookie data via `get_state()`.

## Current Instantiation Sites

### template tags (theme_tags.py) — 8 instantiations per request (worst case)

| Line | Tag function | Creates ThemeManager |
|------|-------------|---------------------|
| 58 | `theme_head` | `ThemeManager(request=request)` |
| 114 | `theme_css` | `ThemeManager(request=request)` |
| 151 | `theme_switcher` | `ThemeManager(request=request)` |
| 177 | `theme_mode_toggle` | `ThemeManager(request=request)` |
| 203 | `theme_preset_selector` | `ThemeManager(request=request)` |
| 223 | `theme_preset` | `ThemeManager(request=request)` |
| 238 | `theme_mode` | `ThemeManager(request=request)` |
| 251 | `theme_resolved_mode` | `ThemeManager(request=request)` |

### context_processors.py — 1 instantiation

| Line | Function | Creates ThemeManager |
|------|----------|---------------------|
| 24 | `theme_context` | `ThemeManager(request=request)` |

### views.py — 2 instantiations per CSS view request

| Line | Function | Creates ThemeManager |
|------|----------|---------------------|
| 13 | `_generate_css_content` | `ThemeManager(request=request)` |
| 31 | `_css_etag` | `ThemeManager(request=request)` |

### mixins.py — 1 instantiation (in mount, stored on self)

| Line | Function | Creates ThemeManager |
|------|----------|---------------------|
| 75 | `ThemeMixin.mount` | `ThemeManager(request=request)` |

### components.py — fallback instantiation (3 classes)

| Line | Class | Creates ThemeManager |
|------|-------|---------------------|
| 46 | `ThemeSwitcher.__init__` | `theme_manager or ThemeManager()` |
| 92 | `ThemeModeButton.__init__` | `theme_manager or ThemeManager()` |
| 130 | `PresetSelector.__init__` | `theme_manager or ThemeManager()` |

These are **fallback-only** — the template tags already pass a manager instance to these constructors. No change needed here.

## Proposed Approach

### Add `get_theme_manager(request)` helper in `manager.py`

```python
def get_theme_manager(request: HttpRequest | None = None) -> ThemeManager:
    """
    Get or create a cached ThemeManager for the given request.

    Caches the instance on ``request._djust_theme_manager`` so that
    multiple template tags / context processors within the same
    request reuse a single ThemeManager (same pattern Django uses
    for ``request.user``).
    """
    if request is not None:
        manager = getattr(request, '_djust_theme_manager', None)
        if manager is not None:
            return manager
        manager = ThemeManager(request=request)
        request._djust_theme_manager = manager
        return manager
    # No request — cannot cache, return fresh instance
    return ThemeManager(request=None)
```

### Update all call sites

Replace `ThemeManager(request=request)` with `get_theme_manager(request)` in:

1. **`djust_theming/templatetags/theme_tags.py`** — all 8 tag functions (lines 58, 114, 151, 177, 203, 223, 238, 251)
2. **`djust_theming/context_processors.py`** — `theme_context` (line 24)
3. **`djust_theming/views.py`** — `_generate_css_content` and `_css_etag` (lines 13, 31)
4. **`djust_theming/mixins.py`** — `ThemeMixin.mount` (line 75)

### Do NOT change

- **`djust_theming/components.py`** — These use `theme_manager or ThemeManager()` as a fallback for when no manager is passed. The callers (template tags) will now pass a cached manager. The fallback `ThemeManager()` (no request) cannot be cached anyway. Leave as-is.

## Files Affected

| File | Change |
|------|--------|
| `djust_theming/manager.py` | Add `get_theme_manager()` helper function |
| `djust_theming/templatetags/theme_tags.py` | Replace 8 `ThemeManager(request=request)` calls with `get_theme_manager(request)` |
| `djust_theming/context_processors.py` | Replace 1 `ThemeManager(request=request)` call |
| `djust_theming/views.py` | Replace 2 `ThemeManager(request=request)` calls |
| `djust_theming/mixins.py` | Replace 1 `ThemeManager(request=request)` call |
| `tests/test_manager_caching.py` | New test file for caching behavior |

**Total: 5 source files modified, 1 test file added.**

## Risk Assessment

### Risk: LOW

1. **No behavioral change** — `get_theme_manager()` returns the exact same `ThemeManager` instance that would have been created. The only difference is reuse within a single request. The `ThemeManager.__init__` is side-effect-free (just reads config and stores request ref).

2. **No cross-request leakage** — Cache lives on the `request` object, which is scoped to a single HTTP request. When the request is garbage-collected, so is the cached manager. This is the same proven pattern Django uses for `request.user`.

3. **Mutation safety** — `ThemeManager.set_mode()`, `set_preset()`, and `set_theme()` write to the session, not to the manager's internal state. The `get_state()` method reads from cookies/session each time it's called. So sharing a manager instance does not cause stale-state issues between different template tags. Each call to `get_state()` still reads fresh data.

4. **No-request fallback** — When `request` is `None` (e.g., management commands, component fallbacks), the helper returns a fresh instance every time. No change in behavior.

5. **Thread safety** — Django request objects are not shared across threads. The `_djust_theme_manager` attribute is request-local.

### Edge case: `views.py` dual instantiation

The `theme_css_view` endpoint calls `_css_etag` (creates ThemeManager) and then `_generate_css_content` (creates another ThemeManager). With caching, the same instance is reused. This is safe because both functions only call `get_state()` which is a read-only operation.

### Testing plan

- Verify `get_theme_manager(request)` returns cached instance on second call
- Verify `get_theme_manager(None)` returns fresh instance each time
- Verify template tags share the same manager within a request
- Verify no regression in existing preset tests

## Status

**ANALYSIS_COMPLETE** — Ready for implementation.
