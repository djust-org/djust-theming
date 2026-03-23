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
from typing import Optional, List

from ..manager import get_theme_config
from ..template_resolver import resolve_component_template

register = template.Library()


def _css_prefix() -> str:
    """Return the current css_prefix from theme config."""
    return get_theme_config().get("css_prefix", "")


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
