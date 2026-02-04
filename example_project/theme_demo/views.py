"""
Demo views showcasing djust-theming features.
"""
from django.shortcuts import render
from djust_theming.presets import THEME_PRESETS
from djust_theming.themes import THEMES
from djust_theming.theme_packs import get_all_theme_packs
from djust_theming.manager import ThemeManager


def index(request):
    """Homepage with overview of features."""
    return render(request, 'theme_demo/index.html', {
        'title': 'djust-theming Demo',
    })


def components(request):
    """Showcase all theme components."""
    return render(request, 'theme_demo/components.html', {
        'title': 'Component Library',
    })


def presets(request):
    """Show all available theme presets."""
    preset_list = []
    for name, preset in THEME_PRESETS.items():
        preset_list.append({
            'name': name,
            'display_name': preset.display_name,
            'light_primary': preset.light.primary.to_hsl_func(),
            'dark_primary': preset.dark.primary.to_hsl_func(),
        })

    return render(request, 'theme_demo/presets.html', {
        'title': 'Theme Presets',
        'presets': preset_list,
    })


def tailwind_demo(request):
    """Demonstrate Tailwind CSS integration."""
    return render(request, 'theme_demo/tailwind.html', {
        'title': 'Tailwind Integration',
    })


def themes(request):
    """Show all available design system themes."""
    manager = ThemeManager(request)
    theme_state = manager.get_state()

    theme_list = []
    for name, theme in THEMES.items():
        theme_list.append({
            'name': name,
            'display_name': theme.display_name,
            'description': theme.description,
        })

    return render(request, 'theme_demo/themes.html', {
        'title': 'Design System Themes',
        'theme_state': theme_state,
        'themes': theme_list,
    })


def packs(request):
    """Show all available theme packs."""
    manager = ThemeManager(request)
    theme_state = manager.get_state()

    pack_list = []
    for name, pack in get_all_theme_packs().items():
        pack_list.append({
            'name': name,
            'display_name': pack.display_name,
            'description': pack.description,
            'category': pack.category,
            'design_theme': pack.design_theme,
            'color_preset': pack.color_preset,
            'icon_style': pack.icon_style.style,
            'animation_style': pack.animation_style.name,
            'pattern_style': pack.pattern_style.background_pattern,
            'surface_style': pack.pattern_style.surface_style,
        })

    return render(request, 'theme_demo/packs.html', {
        'title': 'Theme Packs',
        'theme_state': theme_state,
        'packs': pack_list,
    })
