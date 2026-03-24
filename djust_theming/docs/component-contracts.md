# Component Contracts Reference

Every djust-theming component has a **contract** -- a machine-readable specification of the context variables it expects, the HTML elements it must produce, its accessibility requirements, and the slots available for customization. Theme authors can rely on these contracts to build overrides that work correctly.

The contracts live in `djust_theming/contracts.py` and are used by the test harness to validate both the default templates and any theme-specific overrides you create.

---

## Button

**Template tag:** `{% theme_button text="Save" %}`

### Context variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `text` | str | Yes | -- | Button label text |
| `variant` | str | No | `"primary"` | Visual variant (`primary`, `secondary`, `destructive`, etc.) |
| `size` | str | No | `"md"` | Size class (`sm`, `md`, `lg`) |
| `css_prefix` | str | No | `""` | CSS class prefix (e.g. `"dj-"`) |
| `attrs` | dict | No | `{}` | Extra HTML attributes (`id`, `class`, `onclick`, `type`) |

### Required HTML elements

- `<button>` -- the root element

### Accessibility

No additional ARIA requirements beyond standard `<button>` semantics.

### Slots

| Slot variable | What it overrides | Example use |
|---------------|-------------------|-------------|
| `slot_icon` | Prepends icon before text | SVG icon before label |
| `slot_content` | Replaces `{{ text }}` entirely | Rich button content with icon + text |
| `slot_loading` | Replaces all content (icon + text) | Spinner during async action |

**Slot priority:** `slot_loading` > `slot_icon` + `slot_content` > default `{{ text }}`.

---

## Card

**Template tag:** `{% theme_card title="Title" content="Body" %}`

### Context variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `title` | str or None | No | `None` | Card header title |
| `content` | str | No | `""` | Card body text |
| `footer` | str or None | No | `None` | Card footer text |
| `css_prefix` | str | No | `""` | CSS class prefix |
| `attrs` | dict | No | `{}` | Extra HTML attributes |

### Required HTML elements

- `<div>` -- the card container

### Accessibility

No additional ARIA requirements.

### Slots

| Slot variable | What it overrides | Example use |
|---------------|-------------------|-------------|
| `slot_header` | Replaces `<h3>{{ title }}</h3>` header | Custom header with icon + title |
| `slot_body` | Replaces `{{ content }}` body | Rich body with multiple paragraphs |
| `slot_footer` | Replaces `{{ footer }}` footer | Action buttons in footer |

---

## Alert

**Template tag:** `{% theme_alert message="Something happened" variant="warning" %}`

### Context variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `message` | str | Yes | -- | Alert message text |
| `title` | str or None | No | `None` | Optional bold title above message |
| `variant` | str | No | `"default"` | Visual variant (`default`, `success`, `warning`, `destructive`) |
| `dismissible` | bool | No | `False` | Show dismiss button |
| `css_prefix` | str | No | `""` | CSS class prefix |
| `attrs` | dict | No | `{}` | Extra HTML attributes |

### Required HTML elements

- `<div role="alert">` -- the alert container with ARIA role

### Accessibility

| Requirement | Details |
|-------------|---------|
| `role="alert"` | The container div must have `role="alert"` so screen readers announce it |

### Slots

| Slot variable | What it overrides | Example use |
|---------------|-------------------|-------------|
| `slot_icon` | Adds icon area before message | SVG warning icon |
| `slot_message` | Replaces `{{ message }}` | Rich message with links |
| `slot_actions` | Adds action buttons area | Confirm/cancel buttons |
| `slot_dismiss` | Replaces default dismiss button (when `dismissible=True`) | Custom close button |

---

## Badge

**Template tag:** `{% theme_badge text="New" variant="success" %}`

### Context variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `text` | str | Yes | -- | Badge label text |
| `variant` | str | No | `"default"` | Visual variant (`default`, `secondary`, `success`, etc.) |
| `css_prefix` | str | No | `""` | CSS class prefix |
| `attrs` | dict | No | `{}` | Extra HTML attributes |

### Required HTML elements

- `<span>` -- the badge element

### Accessibility

No additional ARIA requirements.

### Slots

| Slot variable | What it overrides | Example use |
|---------------|-------------------|-------------|
| `slot_content` | Replaces `{{ text }}` entirely | Icon + text badge |

---

## Input

**Template tag:** `{% theme_input name="email" label="Email" type="email" %}`

### Context variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `name` | str | Yes | -- | Input name and id attribute |
| `label` | str or None | No | `None` | Label text (generates `<label for="name">`) |
| `placeholder` | str | No | `""` | Input placeholder text |
| `type` | str | No | `"text"` | Input type (`text`, `email`, `password`, etc.) |
| `css_prefix` | str | No | `""` | CSS class prefix |
| `attrs` | dict | No | `{}` | Extra HTML attributes (`value`, `required`, `disabled`, `readonly`) |

### Required HTML elements

- `<div>` -- the input group wrapper

### Accessibility

| Requirement | Details |
|-------------|---------|
| `<label for="...">` | When a label is present, it must use the `for` attribute referencing the input's id |

### Slots

| Slot variable | What it overrides | Example use |
|---------------|-------------------|-------------|
| `slot_label` | Replaces default `<label>` | Custom label with required indicator |
| `slot_input` | Replaces default `<input>` | `<textarea>`, `<select>`, or custom input |
| `slot_help_text` | Adds help text below input | "We'll never share your email." |
| `slot_error` | Adds error message below input | Validation error message |

---

## Modal

**Template tag:** `{% theme_modal id="confirm" title="Confirm Action" %}`

Opens a dialog overlay. Trigger it with `<button data-theme-modal-open="confirm">Open</button>`.

### Context variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `id` | str | Yes | -- | Unique modal identifier (used by JS open/close triggers) |
| `title` | str or None | No | `None` | Modal title (renders in header, sets `aria-labelledby`) |
| `size` | str | No | `"md"` | Size class (`sm`, `md`, `lg`) |
| `css_prefix` | str | No | `""` | CSS class prefix |
| `attrs` | dict | No | `{}` | Extra HTML attributes |

### Required HTML elements

- `<div role="dialog">` -- the dialog container with `aria-modal="true"`

### Accessibility

| Requirement | Details |
|-------------|---------|
| `role="dialog"` | The dialog container must have `role="dialog"` |
| `aria-modal="true"` | Marks the dialog as modal (traps focus semantically) |
| `aria-labelledby` | References the title element when a title is provided |
| `aria-label="Close"` | Close button must have an accessible label |

### Slots

| Slot variable | What it overrides | Example use |
|---------------|-------------------|-------------|
| `slot_header` | Replaces `<h2>{{ title }}</h2>` header | Custom header with icon + title |
| `slot_body` | Replaces modal body content | Rich body with form fields |
| `slot_footer` | Adds footer area (hidden by default) | Confirm/cancel action buttons |
| `slot_close` | Replaces default close button (X icon) | Custom close button |

### JavaScript behavior

Included automatically via `components.js` (loaded by `{% theme_head %}`):

- **Open:** Click any element with `data-theme-modal-open="{id}"` attribute
- **Close:** Click the close button (`data-theme-modal-close`), press Escape, or click the backdrop
- **Focus management:** Focus moves to the dialog on open
- **Scroll lock:** `body` overflow is hidden while modal is open

### Usage example

```html
{% load theme_components %}

<!-- Trigger button (place anywhere on the page) -->
<button data-theme-modal-open="confirm-delete">Delete Item</button>

<!-- Modal definition -->
{% theme_modal id="confirm-delete" title="Confirm Deletion" size="sm" %}
```

To add a footer with action buttons, render the template directly with `slot_footer`:

```python
# In your view or custom tag
tmpl = resolve_component_template(request, "modal")
html = tmpl.render({
    "id": "confirm-delete",
    "title": "Confirm Deletion",
    "size": "sm",
    "css_prefix": "",
    "attrs": {},
    "slot_footer": '<button data-theme-modal-close>Cancel</button>'
                   '<button class="btn-destructive">Delete</button>',
})
```

---

## Dropdown

**Template tag:** `{% theme_dropdown id="actions" label="Actions" %}`

A trigger button that opens a menu of items below it.

### Context variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `id` | str | Yes | -- | Unique dropdown identifier |
| `label` | str | Yes | -- | Text shown on the trigger button |
| `align` | str | No | `"left"` | Menu alignment (`left` or `right`) |
| `css_prefix` | str | No | `""` | CSS class prefix |
| `attrs` | dict | No | `{}` | Extra HTML attributes |

### Required HTML elements

- `<div>` -- the dropdown wrapper
- `<button aria-haspopup="true">` -- the trigger button

### Accessibility

| Requirement | Details |
|-------------|---------|
| `aria-haspopup="true"` | Trigger button announces it opens a menu |
| `aria-expanded` | Reflects open/closed state (`"true"` or `"false"`) |
| `role="menu"` | The dropdown menu container |

### Slots

| Slot variable | What it overrides | Example use |
|---------------|-------------------|-------------|
| `slot_trigger` | Replaces entire trigger button | Custom button with icon |
| `slot_menu` | Fills the menu content area | List of `<a role="menuitem">` links |

### JavaScript behavior

- **Toggle:** Click trigger to open/close
- **Click outside:** Closes the menu
- **Keyboard:** ArrowDown/ArrowUp navigate items, Escape closes and returns focus to trigger
- **Focus:** First menu item receives focus on open

### Usage example

```html
{% load theme_components %}

{% theme_dropdown id="user-menu" label="Account" align="right" %}
```

Populate the menu via `slot_menu`:

```python
tmpl = resolve_component_template(request, "dropdown")
html = tmpl.render({
    "id": "user-menu",
    "label": "Account",
    "align": "right",
    "css_prefix": "",
    "attrs": {},
    "slot_menu": '<a href="/profile" role="menuitem">Profile</a>'
                 '<a href="/settings" role="menuitem">Settings</a>'
                 '<a href="/logout" role="menuitem">Sign Out</a>',
})
```

---

## Tabs

**Template tag:** `{% theme_tabs id="settings" tabs=tab_list active=0 %}`

A tabbed interface where each tab shows a content panel.

### Context variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `id` | str | Yes | -- | Unique tabs identifier |
| `tabs` | list | Yes | -- | List of dicts, each with `"label"` and `"content"` keys |
| `active` | int | No | `0` | Zero-based index of the initially active tab |
| `css_prefix` | str | No | `""` | CSS class prefix |
| `attrs` | dict | No | `{}` | Extra HTML attributes |

### Required HTML elements

- `<div>` -- the tabs wrapper

### Accessibility

| Requirement | Details |
|-------------|---------|
| `role="tablist"` | Container for tab buttons |
| `role="tab"` | Each tab button, with `aria-selected` and `aria-controls` |
| `role="tabpanel"` | Each content panel, with `aria-labelledby` referencing its tab |
| `tabindex="-1"` | Inactive tabs are removed from the tab order |

### Slots

No slots -- tabs are data-driven via the `tabs` list.

### JavaScript behavior

- **Click:** Activates the clicked tab and shows its panel
- **Keyboard:** ArrowLeft/ArrowRight cycle tabs, Home/End jump to first/last
- **ARIA:** `aria-selected`, `tabindex`, and `hidden` attributes update automatically

### Usage example

```html
{% load theme_components %}

{% theme_tabs id="settings" tabs=tab_list active=0 %}
```

Where `tab_list` is provided from your view context:

```python
# views.py
def settings_view(request):
    tab_list = [
        {"label": "General", "content": "<p>General settings here.</p>"},
        {"label": "Security", "content": "<p>Security settings here.</p>"},
        {"label": "Notifications", "content": "<p>Notification preferences.</p>"},
    ]
    return render(request, "settings.html", {"tab_list": tab_list})
```

---

## Table

**Template tag:** `{% theme_table headers=headers rows=rows variant="striped" %}`

A responsive data table with a scrollable wrapper.

### Context variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `headers` | list | Yes | -- | List of column header strings |
| `rows` | list | Yes | -- | List of row lists (each row is a list of cell values) |
| `variant` | str | No | `"default"` | Visual variant (`default`, `striped`, `hover`) |
| `caption` | str or None | No | `None` | Optional table caption for accessibility |
| `css_prefix` | str | No | `""` | CSS class prefix |
| `attrs` | dict | No | `{}` | Extra HTML attributes |

### Required HTML elements

- `<div>` -- responsive wrapper container
- `<table>` -- the data table

### Accessibility

No additional ARIA requirements beyond semantic `<table>`, `<thead>`, `<tbody>`, and optional `<caption>`.

### Slots

| Slot variable | What it overrides | Example use |
|---------------|-------------------|-------------|
| `slot_caption` | Replaces `<caption>{{ caption }}</caption>` | Rich caption with count |
| `slot_header` | Replaces entire `<thead>` content | Custom header with sorting icons |
| `slot_body` | Replaces entire `<tbody>` content | Custom rows with action buttons |
| `slot_footer` | Adds a `<tfoot>` section (hidden by default) | Summary row with totals |

### Usage example

```html
{% load theme_components %}

{% theme_table headers=headers rows=rows variant="striped" caption="User Directory" %}
```

```python
# views.py
def user_list(request):
    headers = ["Name", "Email", "Role"]
    rows = [
        ["Alice", "alice@example.com", "Admin"],
        ["Bob", "bob@example.com", "Editor"],
        ["Carol", "carol@example.com", "Viewer"],
    ]
    return render(request, "users.html", {"headers": headers, "rows": rows})
```

---

## Pagination

**Template tag:** `{% theme_pagination current_page=page total_pages=total url_pattern="/items/?page={}" %}`

Page navigation controls with previous/next links and page numbers.

### Context variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `current_page` | int | Yes | -- | Current page number (1-based) |
| `total_pages` | int | Yes | -- | Total number of pages |
| `url_pattern` | str | Yes | -- | URL pattern with `{}` placeholder for page number |
| `show_edges` | bool | No | `True` | Whether to show first/last page links with ellipsis |
| `css_prefix` | str | No | `""` | CSS class prefix |
| `attrs` | dict | No | `{}` | Extra HTML attributes |

### Required HTML elements

- `<nav aria-label="Pagination">` -- the navigation landmark

### Accessibility

| Requirement | Details |
|-------------|---------|
| `aria-label="Pagination"` | The nav element is labelled for screen readers |
| `aria-current="page"` | The active page number is marked as current |
| `aria-disabled="true"` | Disabled prev/next links are marked for assistive technology |
| `aria-label="Previous page"` / `"Next page"` | Prev/next links have accessible labels |

### Slots

| Slot variable | What it overrides | Example use |
|---------------|-------------------|-------------|
| `slot_prev` | Replaces the "Prev" link/span | Custom previous button with icon |
| `slot_next` | Replaces the "Next" link/span | Custom next button with icon |

### Usage example

```html
{% load theme_components %}

{% theme_pagination current_page=page total_pages=total_pages url_pattern="/articles/?page={}" %}
```

```python
# views.py
from django.core.paginator import Paginator

def article_list(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 25)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return render(request, "articles.html", {
        "articles": page_obj,
        "page": page_obj.number,
        "total_pages": paginator.num_pages,
    })
```

---

## Select

**Template tag:** `{% theme_select name="country" label="Country" %}`

A styled `<select>` dropdown with optional label, placeholder, and option list.

### Context variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `name` | str | Yes | -- | Select name and id attribute |
| `label` | str or None | No | `None` | Label text (generates `<label for="name">`) |
| `options` | list | No | `None` | List of dicts with `value` and `label` keys (optionally `selected: True`) |
| `placeholder` | str | No | `""` | Disabled placeholder option text |
| `css_prefix` | str | No | `""` | CSS class prefix |
| `attrs` | dict | No | `{}` | Extra HTML attributes (`required`, `disabled`) |

### Required HTML elements

- `<div>` -- the select group wrapper
- `<select>` -- the select element

### Accessibility

| Requirement | Details |
|-------------|---------|
| `<label for="...">` | When a label is present, it must use the `for` attribute referencing the select's id |

### Slots

| Slot variable | What it overrides | Example use |
|---------------|-------------------|-------------|
| `slot_label` | Replaces default `<label>` | Custom label with required indicator |
| `slot_select` | Replaces default `<select>` and its options | Custom select with optgroups |
| `slot_help_text` | Adds help text below select | "Choose your country of residence." |
| `slot_error` | Adds error message below select | Validation error message |

### Usage example

```html
{% load theme_components %}

{% theme_select name="country" label="Country" options=country_list placeholder="Choose one" %}
```

```python
# views.py
def signup(request):
    country_list = [
        {"value": "us", "label": "United States"},
        {"value": "ca", "label": "Canada"},
        {"value": "gb", "label": "United Kingdom"},
    ]
    return render(request, "signup.html", {"country_list": country_list})
```

---

## Textarea

**Template tag:** `{% theme_textarea name="bio" label="Biography" rows=6 %}`

A multi-line text input with optional label, placeholder, and configurable row height.

### Context variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `name` | str | Yes | -- | Textarea name and id attribute |
| `label` | str or None | No | `None` | Label text (generates `<label for="name">`) |
| `placeholder` | str | No | `""` | Textarea placeholder text |
| `rows` | int | No | `4` | Number of visible text rows |
| `css_prefix` | str | No | `""` | CSS class prefix |
| `attrs` | dict | No | `{}` | Extra HTML attributes (`required`, `disabled`, `readonly`, `value`) |

### Required HTML elements

- `<div>` -- the textarea group wrapper
- `<textarea>` -- the textarea element

### Accessibility

| Requirement | Details |
|-------------|---------|
| `<label for="...">` | When a label is present, it must use the `for` attribute referencing the textarea's id |

### Slots

| Slot variable | What it overrides | Example use |
|---------------|-------------------|-------------|
| `slot_label` | Replaces default `<label>` | Custom label with character count |
| `slot_textarea` | Replaces default `<textarea>` | Custom textarea with auto-resize |
| `slot_help_text` | Adds help text below textarea | "Maximum 500 characters." |
| `slot_error` | Adds error message below textarea | Validation error message |

### Usage example

```html
{% load theme_components %}

{% theme_textarea name="bio" label="Biography" placeholder="Tell us about yourself..." rows=6 %}
```

---

## Checkbox

**Template tag:** `{% theme_checkbox name="agree" label="I agree to the terms" %}`

A single checkbox input with optional label and description text.

### Context variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `name` | str | Yes | -- | Checkbox name and id attribute |
| `label` | str | No | `""` | Label text next to the checkbox |
| `description` | str or None | No | `None` | Help text shown below the label |
| `css_prefix` | str | No | `""` | CSS class prefix |
| `attrs` | dict | No | `{}` | Extra HTML attributes (`checked`, `required`, `disabled`, `value`) |

### Required HTML elements

- `<div>` -- the checkbox group wrapper
- `<input type="checkbox">` -- the checkbox input

### Accessibility

| Requirement | Details |
|-------------|---------|
| `<label for="...">` | When a label is present, it must use the `for` attribute referencing the checkbox's id |

### Slots

| Slot variable | What it overrides | Example use |
|---------------|-------------------|-------------|
| `slot_label` | Replaces default `<label>` | Custom label with link to terms |
| `slot_description` | Replaces default description text | Rich description with formatting |

### Usage example

```html
{% load theme_components %}

{% theme_checkbox name="agree" label="I agree to the terms" description="Please read the terms before continuing." %}
```

---

## Radio

**Template tag:** `{% theme_radio name="size" label="Size" options=size_options %}`

A radio button group rendered as a `<fieldset>` with `<legend>`, containing one radio input per option.

### Context variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `name` | str | Yes | -- | Shared name attribute for all radio inputs |
| `label` | str or None | No | `None` | Group label (renders as `<legend>`) |
| `options` | list | No | `None` | List of dicts with `value` and `label` keys |
| `selected` | str | No | `""` | Value of the pre-selected option |
| `css_prefix` | str | No | `""` | CSS class prefix |
| `attrs` | dict | No | `{}` | Extra HTML attributes (`required`, `disabled`) |

### Required HTML elements

- `<fieldset role="radiogroup">` -- the radio group container

### Accessibility

| Requirement | Details |
|-------------|---------|
| `role="radiogroup"` | The fieldset must have `role="radiogroup"` for screen readers |
| `<label for="...">` | Each radio input has an associated label via the `for` attribute (id format: `{name}_{value}`) |

### Slots

| Slot variable | What it overrides | Example use |
|---------------|-------------------|-------------|
| `slot_label` | Replaces default `<legend>` | Custom legend with icon |
| `slot_options` | Replaces all generated radio inputs and labels | Custom layout (e.g. card-style options) |

### Usage example

```html
{% load theme_components %}

{% theme_radio name="size" label="Size" options=size_options selected="md" %}
```

```python
# views.py
def product_detail(request):
    size_options = [
        {"value": "sm", "label": "Small"},
        {"value": "md", "label": "Medium"},
        {"value": "lg", "label": "Large"},
    ]
    return render(request, "product.html", {"size_options": size_options})
```

---

## Breadcrumb

**Template tag:** `{% theme_breadcrumb items=breadcrumbs separator=">" %}`

A navigation breadcrumb trail showing the user's location in a page hierarchy.

### Context variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `items` | list | Yes | -- | List of dicts with `label` and `url` keys |
| `separator` | str | No | `"/"` | Separator character between breadcrumb items |
| `css_prefix` | str | No | `""` | CSS class prefix |
| `attrs` | dict | No | `{}` | Extra HTML attributes |

### Required HTML elements

- `<nav aria-label="Breadcrumb">` -- the navigation landmark
- `<ol>` -- ordered list of breadcrumb items

### Accessibility

| Requirement | Details |
|-------------|---------|
| `aria-label="Breadcrumb"` | The nav element is labelled for screen readers |
| `aria-current="page"` | The last item is marked as the current page |

### Slots

| Slot variable | What it overrides | Example use |
|---------------|-------------------|-------------|
| `slot_separator` | Replaces the default separator character | Custom arrow icon between items |

### Usage example

```html
{% load theme_components %}

{% theme_breadcrumb items=breadcrumbs separator=">" %}
```

```python
# views.py
def product_detail(request):
    breadcrumbs = [
        {"label": "Home", "url": "/"},
        {"label": "Products", "url": "/products/"},
        {"label": "Widget", "url": "/products/widget/"},
    ]
    return render(request, "product.html", {"breadcrumbs": breadcrumbs})
```

---

## Avatar

**Template tag:** `{% theme_avatar src="/img/user.jpg" alt="John Doe" size="lg" %}`

A user avatar displaying an image or initials fallback derived from the user's name.

### Context variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `src` | str or None | No | `None` | Image URL |
| `alt` | str | No | `""` | Alt text for the image |
| `name` | str | No | `""` | Full name (used for initials fallback when no image) |
| `size` | str | No | `"md"` | Size class (`sm`, `md`, `lg`) |
| `css_prefix` | str | No | `""` | CSS class prefix |
| `attrs` | dict | No | `{}` | Extra HTML attributes |

### Required HTML elements

- `<div>` -- the avatar container

### Accessibility

No additional ARIA requirements. When an image is shown, the `alt` attribute provides accessible text.

### Slots

| Slot variable | What it overrides | Example use |
|---------------|-------------------|-------------|
| `slot_image` | Replaces default `<img>` element | Custom image with status indicator overlay |
| `slot_fallback` | Replaces initials fallback | Custom icon or SVG placeholder |

**Slot priority:** `slot_image` > `src` image > `slot_fallback` > initials from `name`.

### Usage example

```html
{% load theme_components %}

<!-- With image -->
{% theme_avatar src="/img/user.jpg" alt="John Doe" size="lg" %}

<!-- With initials fallback -->
{% theme_avatar name="John Doe" size="md" %}
```

---

## Toast

**Template tag:** `{% theme_toast "Saved!" variant="success" %}`

A notification message that appears temporarily to inform the user of an action result.

### Context variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `message` | str | Yes | -- | Toast message text |
| `variant` | str | No | `"info"` | Visual variant (`success`, `warning`, `error`, `info`) |
| `position` | str | No | `"top-right"` | Screen position (`top-right`, `top-left`, `bottom-right`, `bottom-left`) |
| `duration` | int | No | `5000` | Auto-dismiss duration in milliseconds |
| `css_prefix` | str | No | `""` | CSS class prefix |
| `attrs` | dict | No | `{}` | Extra HTML attributes |

### Required HTML elements

- `<div role="status">` -- the toast container with ARIA live region

### Accessibility

| Requirement | Details |
|-------------|---------|
| `role="status"` | The toast is announced by screen readers as a status update |
| `aria-live="polite"` | Screen readers announce the toast without interrupting current speech |
| `aria-label="Dismiss"` | The close button has an accessible label |

### Slots

| Slot variable | What it overrides | Example use |
|---------------|-------------------|-------------|
| `slot_message` | Replaces default `{{ message }}` text | Rich message with icon and formatting |
| `slot_actions` | Adds action buttons area | Undo button |

### Usage example

```html
{% load theme_components %}

{% theme_toast "File saved successfully!" variant="success" %}
{% theme_toast "Network error" variant="error" position="bottom-right" duration=8000 %}
```

---

## Progress

**Template tag:** `{% theme_progress value=75 max=100 label="Upload" %}`

A progress bar showing completion state. Supports both determinate (with value) and indeterminate (without value) modes.

### Context variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `value` | int or None | No | `None` | Current value (`None` for indeterminate/loading state) |
| `max` | int | No | `100` | Maximum value |
| `label` | str | No | `""` | Accessible label text |
| `css_prefix` | str | No | `""` | CSS class prefix |
| `attrs` | dict | No | `{}` | Extra HTML attributes |

### Required HTML elements

- `<div role="progressbar">` -- the progress container with ARIA role

### Accessibility

| Requirement | Details |
|-------------|---------|
| `role="progressbar"` | The element is identified as a progress indicator |
| `aria-valuemin="0"` | Minimum value is always 0 |
| `aria-valuemax` | Set to the `max` value |
| `aria-valuenow` | Set to the current `value` (omitted when indeterminate) |
| `aria-label` | Set to the `label` text when provided |

### Slots

| Slot variable | What it overrides | Example use |
|---------------|-------------------|-------------|
| `slot_label` | Replaces the default label div | Custom label with percentage text |

### Usage example

```html
{% load theme_components %}

<!-- Determinate progress -->
{% theme_progress value=75 max=100 label="Upload progress" %}

<!-- Indeterminate loading -->
{% theme_progress label="Loading..." %}
```

---

## Skeleton

**Template tag:** `{% theme_skeleton variant="text" width="200px" %}`

A loading placeholder with a shimmer animation. Used as a content placeholder while data is being fetched.

### Context variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `variant` | str | No | `"text"` | Shape variant (`text`, `circle`, `rect`) |
| `width` | str | No | `"100%"` | CSS width value |
| `height` | str | No | `"1rem"` | CSS height value |
| `css_prefix` | str | No | `""` | CSS class prefix |
| `attrs` | dict | No | `{}` | Extra HTML attributes |

### Required HTML elements

- `<div aria-hidden="true">` -- the skeleton element (hidden from assistive technology)

### Accessibility

The skeleton is purely decorative and is hidden from screen readers via `aria-hidden="true"`.

### Slots

No slots -- skeleton is a simple decorative element.

### Usage example

```html
{% load theme_components %}

<!-- Text placeholder -->
{% theme_skeleton variant="text" width="200px" %}

<!-- Circle placeholder (avatar) -->
{% theme_skeleton variant="circle" width="3rem" height="3rem" %}

<!-- Rectangle placeholder (image) -->
{% theme_skeleton variant="rect" width="100%" height="200px" %}
```

---

## Tooltip

**Template tag:** `{% theme_tooltip "Help text" position="top" %}`

A CSS-only tooltip that appears on hover. Uses `data-tooltip` and `::after` pseudo-element for zero-JavaScript rendering.

### Context variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `text` | str | Yes | -- | Tooltip text shown on hover |
| `position` | str | No | `"top"` | Tooltip position (`top`, `bottom`, `left`, `right`) |
| `css_prefix` | str | No | `""` | CSS class prefix |
| `attrs` | dict | No | `{}` | Extra HTML attributes |

### Required HTML elements

- `<span data-tooltip="...">` -- the tooltip wrapper with tooltip text in a data attribute

### Accessibility

The tooltip text is conveyed via `data-tooltip` and rendered as a CSS `::after` pseudo-element on hover. For full screen reader support, consider adding `aria-describedby` or `title` in your theme override.

### Slots

| Slot variable | What it overrides | Example use |
|---------------|-------------------|-------------|
| `slot_content` | Replaces the inline text display (tooltip text remains in `data-tooltip`) | Wrap a button or icon with a tooltip |

### Usage example

```html
{% load theme_components %}

<!-- Simple text tooltip -->
{% theme_tooltip "Click to save your changes" position="top" %}

<!-- Tooltip wrapping a button -->
{% theme_tooltip "Delete this item permanently" slot_content="<button>Delete</button>" %}
```

---

## Nav Item

**Template tag:** `{% theme_nav_item "Home" "/" %}`

A single navigation link with automatic active state detection from `request.path`.

### Context variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `label` | str | Yes | -- | Link text |
| `url` | str | Yes | -- | Link URL |
| `icon` | str or None | No | `None` | Optional icon name/text |
| `active` | bool or None | No | `None` | Explicit active state; auto-detects from `request.path` when `None` |
| `badge` | str or None | No | `None` | Optional badge text (e.g. notification count) |
| `css_prefix` | str | No | `""` | CSS class prefix |
| `attrs` | dict | No | `{}` | Extra HTML attributes |

### Required HTML elements

- `<a>` -- the navigation link

### Accessibility

| Requirement | Details |
|-------------|---------|
| `aria-current="page"` | Active nav item must have `aria-current="page"` for screen readers |

### Slots

| Slot variable | What it overrides | Example use |
|---------------|-------------------|-------------|
| `slot_icon` | Replaces default icon `<span>` | Custom SVG icon |
| `slot_badge` | Replaces default badge `<span>` | Custom badge with styling |

### Usage example

```html
{% load theme_components %}

{% theme_nav_item "Home" "/" %}
{% theme_nav_item "Inbox" "/inbox/" badge="5" %}
{% theme_nav_item "Dashboard" "/dash/" active=True %}
```

---

## Nav Group

**Template tag:** `{% theme_nav_group "Admin" items=admin_links %}`

A collapsible group of navigation items using native `<details>/<summary>` for expand/collapse behavior.

### Context variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `label` | str | Yes | -- | Group heading text |
| `items` | list | No | `None` | List of dicts with `label`, `url`, and optional `icon`, `badge` keys |
| `icon` | str or None | No | `None` | Optional icon for the group heading |
| `expanded` | bool | No | `True` | Whether the group is expanded by default |
| `css_prefix` | str | No | `""` | CSS class prefix |
| `attrs` | dict | No | `{}` | Extra HTML attributes |

### Required HTML elements

- `<details>` -- the collapsible container
- `<summary>` -- the clickable heading

### Accessibility

Native `<details>/<summary>` provides built-in expand/collapse semantics.

### Slots

| Slot variable | What it overrides | Example use |
|---------------|-------------------|-------------|
| `slot_label` | Replaces the `{{ label }}` text inside `<summary>` | Custom heading with icon + text |
| `slot_items` | Replaces the rendered item links | Custom navigation items layout |

### Usage example

```html
{% load theme_components %}

{% theme_nav_group "Admin" items=admin_links %}
{% theme_nav_group "Settings" items=settings_links expanded=False %}
```

```python
# views.py
admin_links = [
    {"label": "Users", "url": "/admin/users/"},
    {"label": "Roles", "url": "/admin/roles/", "badge": "3"},
]
```

---

## Nav

**Template tag:** `{% theme_nav brand="MyApp" items=nav_items %}`

A horizontal navigation bar with brand area, navigation links, and an actions slot.

### Context variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `brand` | str or None | No | `None` | Brand text or name |
| `items` | list | No | `None` | List of dicts with `label`, `url`, and optional `icon`, `active`, `badge` keys |
| `css_prefix` | str | No | `""` | CSS class prefix |
| `attrs` | dict | No | `{}` | Extra HTML attributes |

### Required HTML elements

- `<nav role="navigation">` -- the navigation landmark

### Accessibility

| Requirement | Details |
|-------------|---------|
| `role="navigation"` | The nav element identifies as a navigation landmark |
| `aria-label="Main"` | Labels the nav for screen readers |

### Slots

| Slot variable | What it overrides | Example use |
|---------------|-------------------|-------------|
| `slot_brand` | Replaces default brand text | Logo image or rich brand markup |
| `slot_items` | Replaces the rendered item links | Custom nav items with dropdowns |
| `slot_actions` | Adds an actions area (login button, theme switcher, etc.) | `<button>Login</button>` |

### Usage example

```html
{% load theme_components %}

{% theme_nav brand="MyApp" items=nav_items %}
{% theme_nav brand="MyApp" slot_actions="<button>Login</button>" %}
```

```python
# views.py
nav_items = [
    {"label": "Home", "url": "/", "active": True},
    {"label": "About", "url": "/about/"},
    {"label": "Contact", "url": "/contact/"},
]
```

---

## Sidebar Nav

**Template tag:** `{% theme_sidebar_nav sections=sidebar_sections %}`

A vertical sidebar navigation with titled sections. Designed for sidebar and dashboard layouts.

### Context variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `sections` | list | No | `None` | List of dicts with `title` and `items` keys. Each item has `label`, `url`, and optional `icon`, `active`, `badge`. |
| `css_prefix` | str | No | `""` | CSS class prefix |
| `attrs` | dict | No | `{}` | Extra HTML attributes |

### Required HTML elements

- `<nav role="navigation" aria-label="Sidebar">` -- the sidebar navigation landmark

### Accessibility

| Requirement | Details |
|-------------|---------|
| `role="navigation"` | The nav element identifies as a navigation landmark |
| `aria-label="Sidebar"` | Distinguishes sidebar nav from main nav for screen readers |

### Slots

| Slot variable | What it overrides | Example use |
|---------------|-------------------|-------------|
| `slot_header` | Adds a header area above sections | Brand logo, user name |
| `slot_sections` | Replaces all rendered sections | Fully custom section layout |
| `slot_footer` | Adds a footer area below sections | Logout button, version info |

### JavaScript behavior

The `data-theme-sidebar-collapse` attribute on the `<nav>` element enables JavaScript-driven sidebar collapse (implemented by the application or a future djust-theming JS module).

### Usage example

```html
{% load theme_components %}

{% theme_sidebar_nav sections=sidebar_sections %}
```

```python
# views.py
sidebar_sections = [
    {
        "title": "Main",
        "items": [
            {"label": "Dashboard", "url": "/dashboard/", "active": True},
            {"label": "Reports", "url": "/reports/"},
        ],
    },
    {
        "title": "Settings",
        "items": [
            {"label": "Profile", "url": "/settings/profile/"},
            {"label": "Billing", "url": "/settings/billing/", "badge": "!"},
        ],
    },
]
```

---

## Using contracts programmatically

You can access contracts in Python for validation or tooling:

```python
from djust_theming.contracts import get_contract, COMPONENT_CONTRACTS

# Get a single contract
button = get_contract("button")
print(button.available_slots)  # ('slot_icon', 'slot_content', 'slot_loading')

# Iterate all contracts
for name, contract in COMPONENT_CONTRACTS.items():
    print(f"{name}: {len(contract.available_slots)} slots")
```

## Testing theme overrides against contracts

The `ComponentTestCase` base class (in `tests/component_test_base.py`) lets you validate that your theme's template overrides still meet the contract:

```python
from tests.component_test_base import ComponentTestCase

class TestMyThemeButton(ComponentTestCase):
    def test_meets_contract(self):
        html = self.render_component("button", text="Save")
        self.assert_contract(html, "button")

    def test_accessibility(self):
        html = self.render_component("alert", message="Error")
        self.assert_accessible(html, "alert")
```
