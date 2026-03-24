# Form Integration

djust-theming provides automatic CSS class injection for Django forms, a `{% theme_form %}` template tag for quick themed form rendering, and themed error display.

## Setup

Add the custom form renderer to your Django settings:

```python
# settings.py
FORM_RENDERER = "djust_theming.forms.ThemeFormRenderer"
```

With this setting, every `{{ form }}` and `{{ form.as_div }}` call in your templates will render widgets with themed CSS classes automatically.

## How it works

`ThemeFormRenderer` overrides Django's default widget templates. Each widget type gets a semantic CSS class:

| Widget            | CSS class           |
|-------------------|---------------------|
| TextInput         | `theme-input`       |
| EmailInput        | `theme-input`       |
| PasswordInput     | `theme-input`       |
| NumberInput       | `theme-input`       |
| URLInput          | `theme-input`       |
| DateInput         | `theme-input`       |
| SearchInput       | `theme-input`       |
| TelInput          | `theme-input`       |
| Textarea          | `theme-textarea`    |
| Select            | `theme-select`      |
| CheckboxInput     | `theme-checkbox`    |
| RadioSelect       | `theme-radio`       |
| FileInput         | `theme-file-input`  |
| HiddenInput       | *(no class added)*  |

If you have a `css_prefix` configured (e.g. `"dj-"`), it is prepended to every class: `dj-theme-input`, `dj-theme-select`, etc.

## `{% theme_form %}` tag

For full control over form rendering with themed layouts, use the `theme_form` template tag:

```html
{% load theme_form_tags %}

<form method="post">
    {% csrf_token %}
    {% theme_form form %}
    <button type="submit" class="theme-btn">Submit</button>
</form>
```

### Layouts

The tag supports three layout modes via the `layout` keyword argument:

**Stacked (default)** — Labels above fields, one field per row:

```html
{% theme_form form layout="stacked" %}
```

**Horizontal** — Labels beside fields, suitable for wider screens:

```html
{% theme_form form layout="horizontal" %}
```

**Inline** — All fields in a single row, suitable for search bars and filters:

```html
{% theme_form form layout="inline" %}
```

Each layout wraps the form in a container div with a layout-specific class: `theme-form-stacked`, `theme-form-horizontal`, or `theme-form-inline`.

### What `{% theme_form %}` renders

For each visible field, the tag outputs:

```html
<div class="theme-form-field">
    <label for="id_name" class="theme-label">Name</label>
    <div class="theme-help-text" id="id_name_helptext">Your full name</div>
    <input type="text" name="name" id="id_name" ...>
    <!-- field errors appear here when the form is invalid -->
</div>
```

Hidden fields are appended at the end of the form container without wrapper markup.

## Error display

### Field-level errors

When a form is submitted with invalid data, field errors appear directly beneath each widget:

```html
<span class="theme-field-error" role="alert">This field is required.</span>
```

Errors include `role="alert"` for screen reader accessibility.

### Form-level (non-field) errors

Non-field errors from `form.clean()` are rendered at the top of the form as a themed alert:

```html
<div class="theme-form-errors alert alert-destructive" role="alert">
    <ul class="theme-error-list">
        <li>Passwords do not match.</li>
    </ul>
</div>
```

### Standalone error tag

To render non-field errors separately (e.g. outside `{% theme_form %}`):

```html
{% load theme_form_tags %}
{% theme_form_errors form %}
```

This outputs the same alert markup, or nothing if there are no non-field errors.

## `{% get_css_prefix %}` tag

Expose the configured `css_prefix` in your templates for custom markup:

```html
{% load theme_form_tags %}
{% get_css_prefix as prefix %}
<div class="{{ prefix }}theme-input-group">
    {{ form.search }}
    <button class="{{ prefix }}theme-btn">Go</button>
</div>
```

## Customizing error display

### CSS classes reference

| Element              | CSS class              | Purpose                         |
|----------------------|------------------------|---------------------------------|
| Form container       | `theme-form-{layout}`  | Layout wrapper (stacked/horizontal/inline) |
| Field wrapper        | `theme-form-field`     | Groups label + widget + errors  |
| Label                | `theme-label`          | Field label styling             |
| Help text            | `theme-help-text`      | Descriptive text below label    |
| Field error          | `theme-field-error`    | Individual field validation error |
| Non-field error box  | `theme-form-errors`    | Container for form-level errors |
| Error list           | `theme-error-list`     | `<ul>` inside error box         |

### Styling errors

Target error classes in your theme CSS:

```css
.theme-field-error {
    color: var(--color-destructive);
    font-size: var(--text-sm);
    margin-top: var(--space-1);
}

.theme-form-errors {
    border: 1px solid var(--color-destructive);
    border-radius: var(--radius-md);
    padding: var(--space-3);
    margin-bottom: var(--space-4);
}
```

## Security

All error messages, labels, and help text are escaped via Django's `conditional_escape()` before being inserted into HTML. The form rendering does not bypass Django's auto-escaping in widget templates.
