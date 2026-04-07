# I24: CSS Path Consolidation Analysis

## Duplicated Pattern

All 4 callers repeat the same logic:
1. Get ThemeState (via manager.get_state())
2. Get config + css_prefix (via get_theme_config() + config.get("css_prefix", ""))
3. If state.pack: try generate_pack_css(pack_name=state.pack), catch ValueError
4. Fallback: generate_theme_css(theme_name=state.theme, color_preset=state.preset, css_prefix=prefix)

## Four Callers

### 1. theme_tags.py - theme_head() (lines 81-93)
- Inline CSS path when link_css=False (or link_css fallback)
- Pack detection -> fallback to theme generator
- Gets css_prefix separately (also used for component CSS)

### 2. theme_tags.py - theme_css() (lines 131-142)
- Same pack-or-theme logic, standalone tag
- Gets prefix from config independently

### 3. views.py - _generate_css_content() (lines 11-26)
- Linked CSS path (served via HTTP)
- Same pack-or-theme logic

### 4. context_processors.py - theme_context() (lines 29-38)
- Context processor path
- Same logic but slightly different structure (no empty-string init, uses if/else)

### 5. mixins.py - _setup_theme_context() (lines 96-98)
- **BUG**: Does NOT check state.pack at all! Only calls generate_theme_css()
- Missing pack support entirely

## Proposed Solution

Create `generate_css_for_state(state: ThemeState, css_prefix: str = "") -> str` in a new
central location. Best candidate: add it to `djust_theming/css_generation.py` (new module)
or add it to `manager.py` alongside ThemeState. Since it depends on ThemeState and the
generators, placing it in a new `css_generation.py` keeps manager.py focused on state.

Actually, the simplest approach: add it directly to `manager.py` since ThemeState lives
there and it's already imported by all 4 callers. This avoids a new module.

### Function signature:
```python
def generate_css_for_state(state: ThemeState, css_prefix: str = "") -> str:
    """Generate CSS for a given theme state, handling pack-vs-theme selection."""
    if state.pack:
        try:
            from .pack_css_generator import generate_pack_css
            return generate_pack_css(pack_name=state.pack)
        except ValueError:
            pass
    from .theme_css_generator import generate_theme_css
    return generate_theme_css(
        theme_name=state.theme,
        color_preset=state.preset,
        css_prefix=css_prefix,
    )
```

### Helper for getting css_prefix:
Most callers also need css_prefix from config. Add a convenience:
```python
def get_css_prefix() -> str:
    """Get the configured CSS namespace prefix."""
    return get_theme_config().get("css_prefix", "")
```

### Caller changes:
- **theme_tags.py theme_head()**: Replace lines 83-93 with `css = generate_css_for_state(state, css_prefix)`
- **theme_tags.py theme_css()**: Replace lines 131-142 with single call
- **views.py _generate_css_content()**: Replace lines 17-26 with single call
- **context_processors.py theme_context()**: Replace lines 31-38 with single call
- **mixins.py _setup_theme_context()**: Replace line 98 with single call (FIXES pack bug)

## Behavior Preservation
- Pack-first-then-fallback logic preserved exactly
- ValueError catch on pack preserved
- css_prefix passed through to theme generator preserved
- Pack CSS does NOT use css_prefix (current behavior, pack_css_generator ignores it)
- Mixin gets FIXED to support packs (was missing before)
