"""
Template tags for djust_theming.

Usage:
    {% load theme_tags %}

    <!-- In <head> -->
    {% theme_head %}

    <!-- Theme switcher component -->
    {% theme_switcher %}

    <!-- Simple mode toggle -->
    {% theme_mode_toggle %}

    <!-- Preset selector -->
    {% theme_preset_selector layout="dropdown" %}
"""

from django import template
from django.utils.safestring import mark_safe

from ..components import PresetSelector, ThemeModeButton, ThemeSwitcher, ThemeSwitcherConfig
from ..theme_css_generator import CompleteThemeCSSGenerator
from ..manager import ThemeManager, get_theme_config

register = template.Library()


@register.simple_tag(takes_context=True)
def theme_head(context, include_js: bool = True):
    """
    Render theme CSS and anti-FOUC script in the <head>.

    Usage:
        {% theme_head %}
        {% theme_head include_js=False %}

    This renders:
    - Anti-flash script (runs before page render to set correct theme)
    - Theme CSS custom properties
    - Optionally, the theme.js script tag
    """
    request = context.get("request")
    config = get_theme_config()

    # Get current theme state
    manager = ThemeManager(request=request)
    state = manager.get_state()

    # Generate CSS for current theme and preset
    generator = CompleteThemeCSSGenerator(theme_name=state.theme, color_preset=state.preset)
    css = generator.generate_css()

    # Anti-FOUC script - runs immediately to set theme before render
    anti_fouc_script = """
    <script>
        (function() {
            // Set loading class to prevent transitions on page load
            document.documentElement.classList.add('loading');

            var storageKey = 'djust-theme-mode';
            var storedMode = localStorage.getItem(storageKey);
            var mode = storedMode || 'system';

            var resolvedMode = mode;
            if (mode === 'system') {
                resolvedMode = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
            }

            document.documentElement.setAttribute('data-theme', resolvedMode);
            document.documentElement.setAttribute('data-theme-mode', mode);
        })();
    </script>
    """

    # CSS styles
    css_block = f"<style data-djust-theme>{css}</style>"

    # Optional JS include
    js_include = ""
    if include_js:
        js_include = '<script src="/static/djust_theming/js/theme.js?v=2" defer></script>'

    return mark_safe(f"{anti_fouc_script}\n{css_block}\n{js_include}")


@register.simple_tag(takes_context=True)
def theme_css(context):
    """
    Render only the theme CSS (no scripts).

    Useful when you want more control over script placement.

    Usage:
        {% theme_css %}
    """
    request = context.get("request")
    manager = ThemeManager(request=request)
    state = manager.get_state()

    generator = CompleteThemeCSSGenerator(theme_name=state.theme, color_preset=state.preset)
    css = generator.generate_css()

    return mark_safe(f"<style data-djust-theme>{css}</style>")


@register.inclusion_tag("djust_theming/theme_switcher.html", takes_context=True)
def theme_switcher(
    context,
    show_presets: bool = True,
    show_mode_toggle: bool = True,
    show_labels: bool = True,
    dropdown_position: str = "bottom-end",
    button_class: str = "",
    dropdown_class: str = "",
):
    """
    Render the full theme switcher component.

    Usage:
        {% theme_switcher %}
        {% theme_switcher show_presets=False %}
        {% theme_switcher show_labels=False button_class="btn btn-sm" %}
    """
    request = context.get("request")
    manager = ThemeManager(request=request)

    config = ThemeSwitcherConfig(
        show_presets=show_presets,
        show_mode_toggle=show_mode_toggle,
        show_labels=show_labels,
        dropdown_position=dropdown_position,
        button_class=button_class,
        dropdown_class=dropdown_class,
    )

    switcher = ThemeSwitcher(theme_manager=manager, config=config)
    return switcher.get_context()


@register.simple_tag(takes_context=True)
def theme_mode_toggle(context, button_class: str = "", show_label: bool = False):
    """
    Render a simple theme mode toggle button.

    Usage:
        {% theme_mode_toggle %}
        {% theme_mode_toggle button_class="btn btn-outline-secondary" %}
        {% theme_mode_toggle show_label=True %}
    """
    request = context.get("request")
    manager = ThemeManager(request=request)

    button = ThemeModeButton(
        theme_manager=manager,
        button_class=button_class,
        show_label=show_label,
    )
    return mark_safe(button.render())


@register.simple_tag(takes_context=True)
def theme_preset_selector(
    context,
    layout: str = "dropdown",
    show_descriptions: bool = True,
    dropdown_class: str = "",
):
    """
    Render theme preset selector.

    Usage:
        {% theme_preset_selector %}
        {% theme_preset_selector layout="grid" %}
        {% theme_preset_selector layout="list" show_descriptions=True %}
    """
    request = context.get("request")
    manager = ThemeManager(request=request)

    selector = PresetSelector(
        theme_manager=manager,
        show_descriptions=show_descriptions,
        layout=layout,
        dropdown_class=dropdown_class,
    )
    return mark_safe(selector.render())


@register.simple_tag(takes_context=True)
def theme_preset(context):
    """
    Get current theme preset name.

    Usage:
        <body class="theme-{% theme_preset %}">
    """
    request = context.get("request")
    manager = ThemeManager(request=request)
    return manager.get_state().preset


@register.simple_tag(takes_context=True)
def theme_mode(context):
    """
    Get current theme mode setting.

    Returns 'light', 'dark', or 'system'.

    Usage:
        <body data-theme-setting="{% theme_mode %}">
    """
    request = context.get("request")
    manager = ThemeManager(request=request)
    return manager.get_state().mode


@register.simple_tag(takes_context=True)
def theme_resolved_mode(context):
    """
    Get resolved theme mode (always 'light' or 'dark').

    Usage:
        <body class="{% theme_resolved_mode %}">
    """
    request = context.get("request")
    manager = ThemeManager(request=request)
    return manager.get_state().resolved_mode
