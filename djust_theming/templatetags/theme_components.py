"""
Theme-aware component template tags.

All components automatically use theme CSS variables and adapt to light/dark mode.
"""

from django import template
from django.utils.safestring import mark_safe
from typing import Optional, List

register = template.Library()


@register.inclusion_tag('djust_theming/components/button.html')
def theme_button(text: str, variant: str = 'primary', size: str = 'md', **attrs):
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
    return {
        'text': text,
        'variant': variant,
        'size': size,
        'attrs': attrs,
    }


@register.inclusion_tag('djust_theming/components/card.html')
def theme_card(title: Optional[str] = None, footer: Optional[str] = None, **attrs):
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
    return {
        'title': title,
        'footer': footer,
        'attrs': attrs,
    }


@register.inclusion_tag('djust_theming/components/badge.html')
def theme_badge(text: str, variant: str = 'default', **attrs):
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
    return {
        'text': text,
        'variant': variant,
        'attrs': attrs,
    }


@register.inclusion_tag('djust_theming/components/alert.html')
def theme_alert(message: str, title: Optional[str] = None, variant: str = 'default', dismissible: bool = False, **attrs):
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
    return {
        'message': message,
        'title': title,
        'variant': variant,
        'dismissible': dismissible,
        'attrs': attrs,
    }


@register.inclusion_tag('djust_theming/components/input.html')
def theme_input(name: str, label: Optional[str] = None, placeholder: str = '', type: str = 'text', **attrs):
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
    return {
        'name': name,
        'label': label,
        'placeholder': placeholder,
        'type': type,
        'attrs': attrs,
    }


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
