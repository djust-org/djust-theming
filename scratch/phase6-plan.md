# Phase 6: Form Integration Plan

## Overview
Integrate djust-theming with Django's form rendering system so `{{ form }}` and `{{ form.as_div }}` automatically apply theme CSS classes. Plus a `{% theme_form %}` tag for layout control.

## 6.1: ThemeFormRenderer

**File:** `djust_theming/forms.py`

Subclass `django.forms.renderers.DjangoTemplates`. Override `engine` property to add our templates directory (containing themed widget/field/form templates) to the DIRS list alongside Django's defaults.

```python
class ThemeFormRenderer(DjangoTemplates):
    """Form renderer that applies djust-theming CSS classes to all widgets."""

    @cached_property
    def engine(self):
        # Our templates dir takes priority (listed first in DIRS)
        theme_templates_dir = Path(__file__).parent / "templates" / "djust_theming" / "form_templates"
        return self.backend({
            "APP_DIRS": True,
            "DIRS": [
                theme_templates_dir,
                Path(django.forms.__file__).parent / "templates",
            ],
            "NAME": "djust_themed_forms",
            "OPTIONS": {},
        })
```

The key insight: Django's renderers use their own engine (not the project's TEMPLATES). By putting our template dir first, our `django/forms/widgets/input.html` overrides Django's default.

**Usage:** In settings.py: `FORM_RENDERER = "djust_theming.forms.ThemeFormRenderer"`

## 6.2: Field Templates (Widget Overrides)

**Location:** `djust_theming/templates/djust_theming/form_templates/django/forms/`

Override Django's form templates to inject theme CSS classes:

### Widget templates (`django/forms/widgets/`)
These templates receive a `widget` context var from Django. We add theme CSS classes.

- `input.html` — adds `{prefix}input` class to `<input>`
- `text.html`, `email.html`, `password.html`, `number.html`, `url.html`, `date.html`, `search.html`, `tel.html` — include themed `input.html`
- `textarea.html` — adds `{prefix}textarea` class
- `select.html` — adds `{prefix}select` class
- `checkbox.html` — adds `{prefix}checkbox` class (wraps in checkbox-group div)
- `radio.html` — uses `multiple_input.html` with `{prefix}radio-group` class
- `file.html` — adds `{prefix}file-input` class

### Form-level templates (`django/forms/`)
- `div.html` — wraps fields in `{prefix}form-group` divs
- `field.html` — applies `{prefix}input-label` to labels, `{prefix}input-help` to help text

### Error templates (`django/forms/errors/list/`)
- `ul.html` — uses `{prefix}field-errors` class on `<ul>`

**CSS prefix handling:** Since Django's widget rendering doesn't have our template context, the widget templates will read the css_prefix from `get_theme_config()` via a custom template tag (`{% get_css_prefix %}`) loaded in each template. This is cleaner than hardcoding.

Actually, simpler approach: since these are Django widget templates (not our component templates), and the css_prefix is a global setting, we'll use a `{% get_css_prefix as prefix %}` tag. But since widget templates can't load custom tags easily...

**Revised approach:** Use a simple template filter or just directly reference the CSS classes without prefix (they still work). Actually the cleanest way: create a custom template tag library `theme_form_tags` with a `{% load theme_form_tags %}{% css_prefix %}` pattern. Each widget template loads it.

Even simpler: the `attrs.html` template already handles adding attrs. We can just ensure the widget `attrs` dict includes our classes by using a custom widget mixin approach.

**Final approach (simplest, most Django-native):** Override `django/forms/div.html` and `django/forms/field.html` to add theme classes. For widgets, we override the templates to add CSS classes directly. Since css_prefix is a global config value (not per-request), we can load it via a simple tag.

Template structure:
```
djust_theming/form_templates/
  django/
    forms/
      div.html          — themed form layout
      field.html         — themed field wrapper
      errors/
        list/
          ul.html        — themed error list
      widgets/
        attrs.html       — original (unchanged)
        input.html       — adds theme class
        textarea.html    — adds theme class
        select.html      — adds theme class
        checkbox.html    — wrapped in theme class div
        radio.html       — themed radio group
        multiple_input.html — themed wrapper
        text.html, email.html, password.html, number.html,
        url.html, date.html, file.html, search.html, tel.html — include themed input.html
```

## 6.3: {% theme_form %} Tag

**File:** `djust_theming/templatetags/theme_form_tags.py`

A template tag library with:

```python
@register.inclusion_tag("djust_theming/forms/theme_form.html", takes_context=True)
def theme_form(context, form, layout="stacked", action="", method="post", show_errors=True):
    ...
```

**Layouts:**
- `stacked` (default): label above field, full width
- `horizontal`: label and field side by side (using CSS grid)
- `inline`: all fields in a row (using CSS flexbox)

**Template:** `djust_theming/templates/djust_theming/forms/theme_form.html`
- Renders `form.non_field_errors` as `theme_alert variant="destructive"`
- Iterates fields, rendering each with label, widget, help_text, and field errors
- Respects layout classes

Also provides:
- `{% get_css_prefix as prefix %}` — for use in widget templates
- `{% theme_form_errors form %}` — standalone error display

## 6.4: Error Display

**Templates:**
- `djust_theming/templates/djust_theming/forms/form_errors.html` — form-level non_field_errors as themed alert
- `djust_theming/templates/djust_theming/forms/field_errors.html` — field-level errors as inline spans

Error styling uses existing alert component CSS for form-level, and new `{prefix}field-error` class for field-level.

## Files to Create/Modify

### New files:
1. `djust_theming/forms.py` — ThemeFormRenderer
2. `djust_theming/templatetags/theme_form_tags.py` — theme_form tag, get_css_prefix tag
3. `djust_theming/templates/djust_theming/form_templates/django/forms/div.html`
4. `djust_theming/templates/djust_theming/form_templates/django/forms/field.html`
5. `djust_theming/templates/djust_theming/form_templates/django/forms/errors/list/ul.html`
6. `djust_theming/templates/djust_theming/form_templates/django/forms/widgets/input.html`
7. `djust_theming/templates/djust_theming/form_templates/django/forms/widgets/attrs.html`
8. `djust_theming/templates/djust_theming/form_templates/django/forms/widgets/textarea.html`
9. `djust_theming/templates/djust_theming/form_templates/django/forms/widgets/select.html`
10. `djust_theming/templates/djust_theming/form_templates/django/forms/widgets/checkbox.html`
11. `djust_theming/templates/djust_theming/form_templates/django/forms/widgets/radio.html`
12. `djust_theming/templates/djust_theming/form_templates/django/forms/widgets/multiple_input.html`
13. `djust_theming/templates/djust_theming/form_templates/django/forms/widgets/text.html` (+ email, password, number, url, date, file, search, tel)
14. `djust_theming/templates/djust_theming/forms/theme_form.html`
15. `djust_theming/templates/djust_theming/forms/form_errors.html`
16. `djust_theming/templates/djust_theming/forms/field_errors.html`
17. `tests/test_form_integration.py`

### Test coverage targets:
- ThemeFormRenderer resolves themed templates
- Widget templates add correct CSS classes
- theme_form tag renders stacked/horizontal/inline layouts
- Form-level errors render as alerts
- Field-level errors render inline
- css_prefix is applied throughout
- Works with standard Django forms
- Hidden fields handled correctly
