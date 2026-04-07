# Phase 8.1: Theme Gallery View

## Goal
Create a developer-facing gallery view that renders every component in every variant, so theme authors can visually verify all 24 components at a glance. Accessible at `theming/gallery/`, gated by `DEBUG=True` or `staff_member_required`.

## Architecture

### Module: `djust_theming/gallery/`
```
djust_theming/gallery/
    __init__.py
    views.py         # gallery_view function-based view
    urls.py          # URL pattern: "gallery/" -> gallery_view
    context.py       # Build context dicts for all 24 components with all variants
    templates/
        djust_theming/gallery/
            gallery.html        # Main gallery page (extends centered layout)
            _component_section.html  # Reusable section for one component
```

### Components & Variants (from contracts.py)

All 24 components from COMPONENT_CONTRACTS:

| Component | Variants | Sizes | Notes |
|-----------|----------|-------|-------|
| button | primary, secondary, destructive, ghost, link | sm, md, lg | + slot_icon |
| card | (no variant) | - | title, footer, slot_header/body/footer |
| alert | default, success, warning, destructive | - | dismissible=True/False |
| badge | default, secondary, success, warning, destructive | - | |
| input | - | - | label, placeholder, type variations |
| modal | - | sm, md, lg | title, slot_body |
| dropdown | - | - | align=left/right |
| tabs | - | - | 3-tab example |
| table | default, striped, hover | - | caption, sample data |
| pagination | - | - | multi-page example |
| select | - | - | label, options, placeholder |
| textarea | - | - | label, placeholder, rows |
| checkbox | - | - | label, description |
| radio | - | - | label, options |
| breadcrumb | - | - | 3-item example |
| avatar | - | sm, md, lg | src vs initials fallback |
| toast | success, warning, error, info | - | position variations |
| progress | - | - | determinate (25/50/75/100) + indeterminate |
| skeleton | text, circle, rect | - | width/height variations |
| tooltip | - | - | position: top, bottom, left, right |
| nav_item | - | - | active/inactive, badge |
| nav_group | - | - | expanded/collapsed |
| nav | - | - | brand, items |
| sidebar_nav | - | - | sections |

### View Design

```python
def gallery_view(request):
    # Gated: only available when DEBUG=True or user is staff
    # Builds context with sample data for every component
    # Passes list of component sections to template
    # Includes preset_names for a preset switcher form at top
```

### URL Integration

- `djust_theming/gallery/urls.py`: `path("", views.gallery_view, name="gallery")`
- `djust_theming/urls.py`: `path("gallery/", include("djust_theming.gallery.urls"))`
- Final URL: `theming/gallery/` (when included as `path("theming/", include("djust_theming.urls"))`)

### Template Design

`gallery.html` extends `djust_theming/layouts/base.html` (not centered -- we need full width for all components).

Structure:
- Preset switcher at top (form with select, submits to same page via GET `?preset=`)
- For each component: `<section>` with heading, grid of variant examples
- Uses `{% load theme_components %}` to render each component via its template tag
- Inline CSS for gallery-specific layout (grid, spacing, section styling)

### Access Control

```python
from django.conf import settings
from django.http import HttpResponseForbidden

def gallery_view(request):
    if not settings.DEBUG and not (hasattr(request, 'user') and request.user.is_staff):
        return HttpResponseForbidden("Gallery is only available in DEBUG mode or for staff users.")
    ...
```

### Test Plan

1. `test_gallery_view_accessible_in_debug` -- Returns 200 when DEBUG=True
2. `test_gallery_view_forbidden_non_debug_non_staff` -- Returns 403 when DEBUG=False and anonymous
3. `test_gallery_view_accessible_for_staff` -- Returns 200 when DEBUG=False and user.is_staff=True
4. `test_gallery_view_contains_all_components` -- Response contains heading for each of 24 components
5. `test_gallery_view_contains_variant_examples` -- Button section has primary/secondary/destructive variants
6. `test_gallery_view_preset_switcher` -- Response contains preset select form
7. `test_gallery_view_preset_param` -- `?preset=nord` changes the rendered preset
8. `test_gallery_url_resolves` -- URL reverse resolves correctly
9. `test_gallery_context_builder` -- `build_gallery_context()` returns entries for all 24 components
10. `test_gallery_context_button_variants` -- Button context includes all variant values

### Files to Create
- `djust_theming/gallery/__init__.py`
- `djust_theming/gallery/views.py`
- `djust_theming/gallery/urls.py`
- `djust_theming/gallery/context.py`
- `djust_theming/gallery/templates/djust_theming/gallery/gallery.html`
- `tests/test_gallery_view.py`

### Files to Modify
- `djust_theming/urls.py` -- include gallery URLs
- `CHANGELOG.md` -- add entry
