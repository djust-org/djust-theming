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
