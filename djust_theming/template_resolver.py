"""
Template resolution with theme-specific override support.

Provides helpers that build a fallback chain of template candidates:

    1. ``djust_theming/themes/{theme_name}/components/{component}.html``
    2. ``djust_theming/components/{component}.html``

The first template found by ``django.template.loader.select_template``
wins. If no theme-specific override exists, the default ships with the
package and is always available.
"""

from django.template.loader import select_template

from .manager import get_theme_manager


def _get_component_candidates(theme_name: str, component_name: str) -> list[str]:
    """
    Build the ordered list of template candidates for a component.

    Args:
        theme_name: Active design system theme (e.g. "material")
        component_name: Component name (e.g. "button", "card")

    Returns:
        List of template paths, theme-specific first.
    """
    return [
        f"djust_theming/themes/{theme_name}/components/{component_name}.html",
        f"djust_theming/components/{component_name}.html",
    ]


def _get_theme_template_candidates(theme_name: str, template_name: str) -> list[str]:
    """
    Build the ordered list of template candidates for a top-level theme template.

    Args:
        theme_name: Active design system theme (e.g. "material")
        template_name: Template name (e.g. "theme_switcher", "theme_head")

    Returns:
        List of template paths, theme-specific first.
    """
    return [
        f"djust_theming/themes/{theme_name}/{template_name}.html",
        f"djust_theming/{template_name}.html",
    ]


def resolve_component_template(request, component_name: str):
    """
    Resolve the template for a component, checking theme-specific override first.

    Args:
        request: Django HttpRequest (for theme state)
        component_name: e.g. "button", "card", "alert"

    Returns:
        Template object from ``select_template()``.
    """
    manager = get_theme_manager(request)
    state = manager.get_state()
    candidates = _get_component_candidates(state.theme, component_name)
    return select_template(candidates)


def resolve_theme_template(request, template_name: str):
    """
    Resolve a top-level theme template, checking theme-specific override first.

    Args:
        request: Django HttpRequest (for theme state)
        template_name: e.g. "theme_switcher"

    Returns:
        Template object from ``select_template()``.
    """
    manager = get_theme_manager(request)
    state = manager.get_state()
    candidates = _get_theme_template_candidates(state.theme, template_name)
    return select_template(candidates)
