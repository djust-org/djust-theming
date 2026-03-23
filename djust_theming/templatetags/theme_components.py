"""
Theme-aware component template tags.

All components automatically use theme CSS variables and adapt to light/dark mode.
Template resolution supports theme-specific overrides via:

    djust_theming/themes/{theme_name}/components/{component}.html

Falling back to:

    djust_theming/components/{component}.html
"""

from django import template
from django.utils.safestring import mark_safe
from typing import Any, Optional, List

from ..manager import get_theme_config
from ..template_resolver import resolve_component_template

register = template.Library()


def _css_prefix() -> str:
    """Return the current css_prefix from theme config."""
    return get_theme_config().get("css_prefix", "")


def _extract_slots(attrs: dict) -> tuple[dict, dict]:
    """Separate slot_* keys from regular attrs.

    Returns:
        (slots_dict, remaining_attrs_dict)
    """
    slots = {}
    remaining = {}
    for k, v in attrs.items():
        if k.startswith("slot_"):
            slots[k] = v
        else:
            remaining[k] = v
    return slots, remaining


@register.simple_tag(takes_context=True)
def theme_button(context, text: str, variant: str = 'primary', size: str = 'md', **attrs):
    """
    Render a themed button.

    Args:
        text: Button text
        variant: 'primary', 'secondary', 'destructive', 'ghost', 'link'
        size: 'sm', 'md', 'lg'
        **attrs: Additional HTML attributes (class, id, onclick, etc.)

    Usage:
        {% theme_button "Click me" variant="primary" size="md" %}
        {% theme_button "Delete" variant="destructive" onclick="confirmDelete()" %}
    """
    request = context.get("request")
    tmpl = resolve_component_template(request, "button")
    ctx = {
        'text': text,
        'variant': variant,
        'size': size,
        'attrs': attrs,
        'css_prefix': _css_prefix(),
    }
    return mark_safe(tmpl.render(ctx))


@register.simple_tag(takes_context=True)
def theme_card(context, title: Optional[str] = None, footer: Optional[str] = None, **attrs):
    """
    Render a themed card container.

    Args:
        title: Optional card title
        footer: Optional card footer content
        **attrs: Additional HTML attributes

    Usage:
        {% theme_card title="Card Title" %}
            <p>Card content goes here</p>
        {% end_theme_card %}
    """
    request = context.get("request")
    tmpl = resolve_component_template(request, "card")
    ctx = {
        'title': title,
        'footer': footer,
        'attrs': attrs,
        'css_prefix': _css_prefix(),
    }
    return mark_safe(tmpl.render(ctx))


@register.simple_tag(takes_context=True)
def theme_badge(context, text: str, variant: str = 'default', **attrs):
    """
    Render a themed badge.

    Args:
        text: Badge text
        variant: 'default', 'secondary', 'success', 'warning', 'destructive'
        **attrs: Additional HTML attributes

    Usage:
        {% theme_badge "New" variant="success" %}
        {% theme_badge "Beta" variant="secondary" %}
    """
    request = context.get("request")
    tmpl = resolve_component_template(request, "badge")
    ctx = {
        'text': text,
        'variant': variant,
        'attrs': attrs,
        'css_prefix': _css_prefix(),
    }
    return mark_safe(tmpl.render(ctx))


@register.simple_tag(takes_context=True)
def theme_alert(context, message: str, title: Optional[str] = None, variant: str = 'default', dismissible: bool = False, **attrs):
    """
    Render a themed alert.

    Args:
        message: Alert message
        title: Optional alert title
        variant: 'default', 'success', 'warning', 'destructive'
        dismissible: Whether alert can be dismissed
        **attrs: Additional HTML attributes

    Usage:
        {% theme_alert "Operation successful!" variant="success" dismissible=True %}
        {% theme_alert "Error occurred" title="Error" variant="destructive" %}
    """
    request = context.get("request")
    tmpl = resolve_component_template(request, "alert")
    ctx = {
        'message': message,
        'title': title,
        'variant': variant,
        'dismissible': dismissible,
        'attrs': attrs,
        'css_prefix': _css_prefix(),
    }
    return mark_safe(tmpl.render(ctx))


@register.simple_tag(takes_context=True)
def theme_input(context, name: str, label: Optional[str] = None, placeholder: str = '', type: str = 'text', **attrs):
    """
    Render a themed input field.

    Args:
        name: Input name attribute
        label: Optional label text
        placeholder: Placeholder text
        type: Input type (text, email, password, etc.)
        **attrs: Additional HTML attributes

    Usage:
        {% theme_input "email" label="Email Address" placeholder="you@example.com" type="email" %}
    """
    request = context.get("request")
    tmpl = resolve_component_template(request, "input")
    ctx = {
        'name': name,
        'label': label,
        'placeholder': placeholder,
        'type': type,
        'attrs': attrs,
        'css_prefix': _css_prefix(),
    }
    return mark_safe(tmpl.render(ctx))


@register.simple_tag(takes_context=True)
def theme_modal(context, id: str, title: Optional[str] = None, size: str = 'md', **attrs):
    """
    Render a themed modal dialog.

    Args:
        id: Unique modal identifier (used for data-theme-modal-open triggers)
        title: Optional modal title
        size: 'sm', 'md', 'lg'
        **attrs: Additional HTML attributes

    Usage:
        {% theme_modal id="confirm" title="Confirm Action" size="md" %}
        <!-- Trigger: <button data-theme-modal-open="confirm">Open</button> -->
    """
    request = context.get("request")
    tmpl = resolve_component_template(request, "modal")
    ctx = {
        'id': id,
        'title': title,
        'size': size,
        'attrs': attrs,
        'css_prefix': _css_prefix(),
    }
    return mark_safe(tmpl.render(ctx))


@register.simple_tag(takes_context=True)
def theme_dropdown(context, id: str, label: str, align: str = 'left', **attrs):
    """
    Render a themed dropdown menu.

    Args:
        id: Unique dropdown identifier
        label: Trigger button text
        align: Menu alignment ('left' or 'right')
        **attrs: Additional HTML attributes

    Usage:
        {% theme_dropdown id="actions" label="Actions" align="right" %}
    """
    request = context.get("request")
    tmpl = resolve_component_template(request, "dropdown")
    ctx = {
        'id': id,
        'label': label,
        'align': align,
        'attrs': attrs,
        'css_prefix': _css_prefix(),
    }
    return mark_safe(tmpl.render(ctx))


@register.simple_tag(takes_context=True)
def theme_tabs(context, id: str, tabs: Any = None, active: int = 0, **attrs):
    """
    Render themed tabs with panels.

    Args:
        id: Unique tabs identifier
        tabs: List of dicts with 'label' and 'content' keys
        active: Zero-based index of the initially active tab
        **attrs: Additional HTML attributes

    Usage:
        {% theme_tabs id="settings" tabs=tab_list active=0 %}
    """
    request = context.get("request")
    tmpl = resolve_component_template(request, "tabs")
    ctx = {
        'id': id,
        'tabs': tabs or [],
        'active': active,
        'attrs': attrs,
        'css_prefix': _css_prefix(),
    }
    return mark_safe(tmpl.render(ctx))


@register.simple_tag(takes_context=True)
def theme_table(context, headers: Any = None, rows: Any = None, variant: str = 'default', caption: Optional[str] = None, **attrs):
    """
    Render a themed responsive table.

    Args:
        headers: List of column header strings
        rows: List of row lists (each row is a list of cell values)
        variant: 'default', 'striped', 'hover'
        caption: Optional table caption
        **attrs: Additional HTML attributes

    Usage:
        {% theme_table headers=headers rows=rows variant="striped" caption="Users" %}
    """
    request = context.get("request")
    tmpl = resolve_component_template(request, "table")
    ctx = {
        'headers': headers or [],
        'rows': rows or [],
        'variant': variant,
        'caption': caption,
        'attrs': attrs,
        'css_prefix': _css_prefix(),
    }
    return mark_safe(tmpl.render(ctx))


@register.simple_tag(takes_context=True)
def theme_pagination(context, current_page: int = 1, total_pages: int = 1, url_pattern: str = '?page={}', show_edges: bool = True, **attrs):
    """
    Render themed pagination controls.

    Args:
        current_page: Current page number (1-based)
        total_pages: Total number of pages
        url_pattern: URL pattern with {} placeholder for page number
        show_edges: Whether to show first/last page links
        **attrs: Additional HTML attributes

    Usage:
        {% theme_pagination current_page=page total_pages=total url_pattern="/items/?page={}" %}
    """
    request = context.get("request")
    tmpl = resolve_component_template(request, "pagination")

    # Build page range (show up to 5 pages around current)
    window = 2
    range_start = max(1, current_page - window)
    range_end = min(total_pages, current_page + window)

    page_range = []
    for p in range(range_start, range_end + 1):
        page_range.append({'number': p, 'url': url_pattern.format(p)})

    # Edge detection
    first_page = 1 if show_edges and range_start > 1 else None
    first_url = url_pattern.format(1) if first_page else None
    first_ellipsis = range_start > 2

    last_page = total_pages if show_edges and range_end < total_pages else None
    last_url = url_pattern.format(total_pages) if last_page else None
    last_ellipsis = range_end < total_pages - 1

    prev_url = url_pattern.format(current_page - 1) if current_page > 1 else None
    next_url = url_pattern.format(current_page + 1) if current_page < total_pages else None

    ctx = {
        'current_page': current_page,
        'total_pages': total_pages,
        'url_pattern': url_pattern,
        'show_edges': show_edges,
        'page_range': page_range,
        'first_page': first_page,
        'first_url': first_url,
        'first_ellipsis': first_ellipsis,
        'last_page': last_page,
        'last_url': last_url,
        'last_ellipsis': last_ellipsis,
        'prev_url': prev_url,
        'next_url': next_url,
        'attrs': attrs,
        'css_prefix': _css_prefix(),
    }
    return mark_safe(tmpl.render(ctx))


@register.simple_tag(takes_context=True)
def theme_select(context, name: str, label: Optional[str] = None, options: Any = None, placeholder: str = '', **attrs):
    """
    Render a themed select dropdown.

    Args:
        name: Select name attribute
        label: Optional label text
        options: List of dicts with 'value' and 'label' keys
        placeholder: Placeholder option text
        **attrs: Additional HTML attributes (required, disabled, etc.)

    Usage:
        {% theme_select "country" label="Country" options=countries placeholder="Choose..." %}
    """
    slots, remaining_attrs = _extract_slots(attrs)
    request = context.get("request")
    tmpl = resolve_component_template(request, "select")
    ctx = {
        'name': name,
        'label': label,
        'options': options or [],
        'placeholder': placeholder,
        'attrs': remaining_attrs,
        'css_prefix': _css_prefix(),
        **slots,
    }
    return mark_safe(tmpl.render(ctx))


@register.simple_tag(takes_context=True)
def theme_textarea(context, name: str, label: Optional[str] = None, placeholder: str = '', rows: int = 4, **attrs):
    """
    Render a themed textarea.

    Args:
        name: Textarea name attribute
        label: Optional label text
        placeholder: Placeholder text
        rows: Number of visible text rows
        **attrs: Additional HTML attributes (required, disabled, readonly, etc.)

    Usage:
        {% theme_textarea "bio" label="Biography" placeholder="Tell us about yourself..." rows=6 %}
    """
    slots, remaining_attrs = _extract_slots(attrs)
    request = context.get("request")
    tmpl = resolve_component_template(request, "textarea")
    ctx = {
        'name': name,
        'label': label,
        'placeholder': placeholder,
        'rows': rows,
        'attrs': remaining_attrs,
        'css_prefix': _css_prefix(),
        **slots,
    }
    return mark_safe(tmpl.render(ctx))


@register.simple_tag(takes_context=True)
def theme_checkbox(context, name: str, label: str = '', description: Optional[str] = None, **attrs):
    """
    Render a themed checkbox.

    Args:
        name: Checkbox name attribute
        label: Label text displayed next to the checkbox
        description: Optional descriptive text below the label
        **attrs: Additional HTML attributes (checked, required, disabled, value, etc.)

    Usage:
        {% theme_checkbox "agree" label="I agree to terms" required=True %}
        {% theme_checkbox "newsletter" label="Subscribe" description="Get weekly updates" %}
    """
    slots, remaining_attrs = _extract_slots(attrs)
    request = context.get("request")
    tmpl = resolve_component_template(request, "checkbox")
    ctx = {
        'name': name,
        'label': label,
        'description': description,
        'attrs': remaining_attrs,
        'css_prefix': _css_prefix(),
        **slots,
    }
    return mark_safe(tmpl.render(ctx))


@register.simple_tag(takes_context=True)
def theme_radio(context, name: str, label: Optional[str] = None, options: Any = None, selected: str = '', **attrs):
    """
    Render a themed radio button group.

    Args:
        name: Radio group name attribute
        label: Optional group label (rendered as fieldset legend)
        options: List of dicts with 'value' and 'label' keys
        selected: Value of the initially selected option
        **attrs: Additional HTML attributes (required, disabled, etc.)

    Usage:
        {% theme_radio "size" label="Size" options=sizes selected="md" %}
    """
    slots, remaining_attrs = _extract_slots(attrs)
    request = context.get("request")
    tmpl = resolve_component_template(request, "radio")
    ctx = {
        'name': name,
        'label': label,
        'options': options or [],
        'selected': selected,
        'attrs': remaining_attrs,
        'css_prefix': _css_prefix(),
        **slots,
    }
    return mark_safe(tmpl.render(ctx))


@register.simple_tag
def theme_icon(name: str, size: int = 20):
    """
    Render an SVG icon (placeholder - integrate with your icon library).

    Args:
        name: Icon name
        size: Icon size in pixels

    Usage:
        {% theme_icon "check" size=16 %}
    """
    # Placeholder SVG icons
    icons = {
        'check': f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>',
        'x': f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>',
        'alert': f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>',
        'info': f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>',
    }
    return mark_safe(icons.get(name, ''))
