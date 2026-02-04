"""
Demo views showcasing djust-theming features.
"""
from django.shortcuts import render
from djust_theming.presets import THEME_PRESETS
from djust_theming.themes import THEMES
from djust_theming.theme_packs import get_all_theme_packs, get_all_design_systems
from djust_theming.manager import ThemeManager
from djust_theming.inspector import theme_inspector_view, theme_inspector_api, theme_css_api


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


def design_systems(request):
    """Show all available design systems with independent color selection."""
    manager = ThemeManager(request)
    theme_state = manager.get_state()

    design_list = []
    for name, design in get_all_design_systems().items():
        design_list.append({
            'name': name,
            'display_name': design.display_name,
            'description': design.description,
            'category': design.category,
            'typography_name': design.typography.name,
            'layout_name': design.layout.name,
            'surface_name': design.surface.name,
            'icon_style': design.icons.style,
            'animation_name': design.animation.name,
            'interaction_name': design.interaction.name,
        })

    # Get available color presets for selection
    from djust_theming.presets import THEME_PRESETS
    color_list = []
    for name, preset in THEME_PRESETS.items():
        color_list.append({
            'name': name,
            'display_name': preset.display_name,
            'light_primary': preset.light.primary.to_hsl_func(),
            'dark_primary': preset.dark.primary.to_hsl_func(),
        })

    # Get current design system and color from request or defaults
    current_design = request.GET.get('design', 'minimal')
    current_color = request.GET.get('color', 'default')
    
    # Generate CSS for current combination
    from djust_theming.design_system_css import generate_design_system_css
    current_css = generate_design_system_css(current_design, current_color)

    return render(request, 'theme_demo/design_systems.html', {
        'title': 'Design Systems',
        'theme_state': theme_state,
        'designs': design_list,
        'colors': color_list,
        'current_design': current_design,
        'current_color': current_color,
        'current_css': current_css,
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
