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
