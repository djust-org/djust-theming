# I4: Static Asset Versioning — Analysis

## Problem Summary

`theme.js` is referenced with manual `?v=N` cache busters that are **already out of sync**:

| Location | Version | Path |
|---|---|---|
| `theme_tags.py:98` | `"2"` | Passed as `js_version` to `theme_head.html` |
| `mixins.py:115` | `"3"` | Passed as `js_version` to `theme_head.html` |
| `context_processors.py:58` | `"2"` | Hardcoded inline HTML (does NOT use `theme_head.html`) |

The template `theme_head.html:20` renders:
```html
<script src="/static/djust_theming/js/theme.js?v={{ js_version }}" defer></script>
```

There are **two separate problems** here:

1. **Version mismatch**: `theme_tags.py` says `v=2`, `mixins.py` says `v=3`. Users hitting the same `theme.js` file through different code paths may get stale cached versions.
2. **Hardcoded `/static/` prefix**: All three locations use `/static/djust_theming/js/theme.js` instead of Django's `staticfiles_storage.url()` or `{% static %}`. This breaks when `STATIC_URL` is a CDN, custom prefix, or when `ManifestStaticFilesStorage` is active (which appends content hashes).

Note: `theme_head.html:19` already uses `{% static %}` correctly for `components.css`:
```html
<link rel="stylesheet" href="{% static 'djust_theming/css/components.css' %}">
```
This inconsistency within the same template underscores the bug.

## Related Task: I48

ROADMAP I48 ("Static URL Resolution in Template Tags") addresses the hardcoded `/static/` prefix problem and explicitly states it should be done alongside I4. Both fix the same root cause. This analysis covers both.

## All `?v=` and Hardcoded Static Path References

### JS versioning (`theme.js`)

1. **`djust_theming/templatetags/theme_tags.py:98`** — `"js_version": "2"` passed to template
2. **`djust_theming/mixins.py:115`** — `"js_version": "3"` passed to template
3. **`djust_theming/context_processors.py:58`** — Hardcoded `?v=2` in inline HTML string
4. **`djust_theming/templates/djust_theming/theme_head.html:20`** — Template renders `?v={{ js_version }}`

### CSS cache busters (theme state-based, NOT version numbers)

5. **`djust_theming/templatetags/theme_tags.py:66-71`** — `cache_buster = f"t={state.theme}&p={state.preset}&m={state.mode}"` for CSS `<link>` tag
6. **`djust_theming/mixins.py:103-106`** — Same pattern duplicated for mixin CSS `<link>` tag

The CSS cache busters (items 5-6) are **not part of this task** — they use theme state to invalidate CSS when the theme changes, which is correct behavior. They are duplicated code (addressed by future refactoring), but the values are consistent.

## Proposed Approach: `staticfiles_storage.url()` (Recommended)

### Why NOT a `THEME_JS_VERSION` constant

A single constant (e.g., `THEME_JS_VERSION = "3"`) would fix the mismatch but:
- Still requires manual bumping on every `theme.js` change
- Still uses hardcoded `/static/` prefix (doesn't fix I48)
- Doesn't work with `ManifestStaticFilesStorage` (which adds content hashes)
- Adds a maintenance burden that Django already solves

### Why `staticfiles_storage.url()`

Django's `staticfiles_storage.url()` (from `django.contrib.staticfiles.storage`):
- Respects `STATIC_URL` (CDN, custom prefix)
- With `ManifestStaticFilesStorage`, appends content-based hashes automatically — no manual versioning needed
- With default `StaticFilesStorage`, returns the plain URL (no hash, but `STATIC_URL` is respected)
- Works identically in Python code (`theme_tags.py`, `mixins.py`, `context_processors.py`) and templates (`{% static %}`)

### Implementation Plan

#### 1. Template: `theme_head.html` (line 20)

Replace the hardcoded path + `?v={{ js_version }}` with `{% static %}`:

```html
{# Before #}
{% if include_js %}<script src="/static/djust_theming/js/theme.js?v={{ js_version }}" defer></script>{% endif %}

{# After #}
{% if include_js %}<script src="{% static 'djust_theming/js/theme.js' %}" defer></script>{% endif %}
```

The template already loads `{% load static %}` on line 2. The `js_version` context variable becomes unnecessary.

#### 2. `theme_tags.py` (line 94-99)

Remove `js_version` from the template context dict:

```python
# Before
html = render_to_string("djust_theming/theme_head.html", {
    "loading_class": True,
    "css_block": css_block,
    "include_js": include_js,
    "js_version": "2",
})

# After
html = render_to_string("djust_theming/theme_head.html", {
    "loading_class": True,
    "css_block": css_block,
    "include_js": include_js,
})
```

#### 3. `mixins.py` (line 111-116)

Same removal:

```python
# Before
self.theme_head = mark_safe(render_to_string("djust_theming/theme_head.html", {
    "loading_class": False,
    "css_block": css_block,
    "include_js": True,
    "js_version": "3",
}))

# After
self.theme_head = mark_safe(render_to_string("djust_theming/theme_head.html", {
    "loading_class": False,
    "css_block": css_block,
    "include_js": True,
}))
```

#### 4. `context_processors.py` (line 56-58)

This file builds HTML as a raw f-string and does NOT use `theme_head.html`. Two options:

**Option A (minimal):** Use `staticfiles_storage.url()` in the f-string:
```python
from django.contrib.staticfiles.storage import staticfiles_storage
js_url = staticfiles_storage.url('djust_theming/js/theme.js')
theme_head = f"""{anti_fouc_script}
<style data-djust-theme>{css}</style>
<script src="{js_url}" defer></script>"""
```

**Option B (better, aligns with I1):** Refactor `context_processors.py` to use `theme_head.html` template like the other two paths. This eliminates the duplicated anti-FOUC script (lines 41-53) and brings all three code paths through the same template. However, this is a larger change that overlaps with I1's deduplication work.

**Recommendation:** Option A for this task. Option B can be done as a follow-up or as part of I1 completion.

#### 5. Version constant cleanup

Remove `__version__ = "0.1.0"` from `__init__.py:46` or update it to match `pyproject.toml` (`0.3.0`). This is not directly part of I4 but is a version mismatch worth noting. (Out of scope — flag only.)

## Files Affected

| File | Change |
|---|---|
| `djust_theming/templates/djust_theming/theme_head.html` | Replace hardcoded path with `{% static %}`, remove `?v={{ js_version }}` |
| `djust_theming/templatetags/theme_tags.py` | Remove `"js_version": "2"` from context dict |
| `djust_theming/mixins.py` | Remove `"js_version": "3"` from context dict |
| `djust_theming/context_processors.py` | Replace hardcoded path with `staticfiles_storage.url()` |

## Files NOT Affected

- `theme_head.html` line 19 (`components.css`) — already uses `{% static %}` correctly
- CSS cache buster params in `theme_tags.py:66-71` and `mixins.py:103-106` — these are theme-state-based, not version-based; they serve a different purpose

## Risk Assessment

| Risk | Severity | Mitigation |
|---|---|---|
| `staticfiles` app not in `INSTALLED_APPS` | Low | `{% static %}` raises `ImproperlyConfigured` — loud failure, easy to diagnose. ROADMAP suggests adding system check `W004` but that's a separate task. |
| `ManifestStaticFilesStorage` users get different URL format | None (positive) | This is the whole point — they get content-hashed URLs that bust cache automatically. |
| `context_processors.py` still builds inline HTML | Low | Using `staticfiles_storage.url()` is safe and well-tested Django API. Full template migration is a follow-up. |
| Breaking change for users who override `theme_head.html` | Very Low | Template still has the same structure. The only change is the `<script src>` line. Custom overrides that hardcode their own JS path are unaffected. |
| `render_to_string` without `RequestContext` may not resolve `{% static %}` | Low | `{% static %}` does not require request context — it uses `staticfiles_storage` directly. Already proven by line 19 of the same template (`components.css`). |
| Removal of `js_version` variable | None | No external template or code references this variable outside the three files listed. |

## Estimated Scope

- **Lines changed**: ~10
- **Complexity**: Low — straightforward removal of manual versioning in favor of existing Django infrastructure
- **Testing**: Verify `{% static %}` resolves correctly in `theme_head.html`; verify `context_processors.py` produces correct URL; verify no remaining `?v=` references for `theme.js`
