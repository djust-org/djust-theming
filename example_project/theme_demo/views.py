"""
Demo views showcasing djust-theming features across Phases 1-9.
"""
from django import forms
from django.shortcuts import render
from djust_theming.presets import THEME_PRESETS
from djust_theming.theme_packs import get_all_theme_packs, get_all_design_systems
from djust_theming.manager import ThemeManager, get_theme_manager
from djust_theming.inspector import theme_inspector_view, theme_inspector_api, theme_css_api


def index(request):
    """Homepage with overview of features."""
    return render(request, 'theme_demo/index.html', {
        'title': 'djust-theming Demo',
    })


def components(request):
    """Showcase all 24 theme components."""
    # Data for table component
    table_headers = ['Name', 'Role', 'Status', 'Actions']
    table_rows = [
        ['Alice Johnson', 'Admin', 'Active', 'Edit'],
        ['Bob Smith', 'Editor', 'Active', 'Edit'],
        ['Carol White', 'Viewer', 'Inactive', 'Edit'],
    ]

    # Data for tabs component
    tab_list = [
        {'label': 'Overview', 'content': 'This is the overview tab content. It shows general information about the item.'},
        {'label': 'Details', 'content': 'Detailed information goes here. Specifications, metadata, and technical details.'},
        {'label': 'History', 'content': 'Activity history and changelog for this item.'},
    ]

    # Data for select component
    country_options = [
        {'value': 'us', 'label': 'United States'},
        {'value': 'uk', 'label': 'United Kingdom'},
        {'value': 'de', 'label': 'Germany'},
        {'value': 'fr', 'label': 'France'},
        {'value': 'jp', 'label': 'Japan'},
    ]

    # Data for radio component
    size_options = [
        {'value': 'sm', 'label': 'Small'},
        {'value': 'md', 'label': 'Medium'},
        {'value': 'lg', 'label': 'Large'},
    ]

    # Data for breadcrumb component
    breadcrumb_items = [
        {'label': 'Home', 'url': '/'},
        {'label': 'Components', 'url': '/components/'},
        {'label': 'Breadcrumb', 'url': ''},
    ]

    # Data for nav component
    nav_items = [
        {'label': 'Dashboard', 'url': '/dashboard/', 'icon': 'D'},
        {'label': 'Projects', 'url': '/projects/', 'icon': 'P', 'badge': '3'},
        {'label': 'Settings', 'url': '/settings/', 'icon': 'S'},
    ]

    # Data for sidebar_nav component
    sidebar_sections = [
        {
            'title': 'Main',
            'items': [
                {'label': 'Dashboard', 'url': '/', 'icon': 'D'},
                {'label': 'Projects', 'url': '/projects/', 'icon': 'P', 'badge': '5'},
            ],
        },
        {
            'title': 'Settings',
            'items': [
                {'label': 'Profile', 'url': '/profile/', 'icon': 'U'},
                {'label': 'Billing', 'url': '/billing/', 'icon': 'B'},
            ],
        },
    ]

    return render(request, 'theme_demo/components.html', {
        'title': 'Component Library',
        'table_headers': table_headers,
        'table_rows': table_rows,
        'tab_list': tab_list,
        'country_options': country_options,
        'size_options': size_options,
        'breadcrumb_items': breadcrumb_items,
        'nav_items': nav_items,
        'sidebar_sections': sidebar_sections,
    })


def presets(request):
    """Show all 19 available theme presets."""
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


def design_systems(request):
    """Show all available design systems with independent color selection."""
    manager = get_theme_manager(request)
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
    color_list = []
    for name, preset in THEME_PRESETS.items():
        color_list.append({
            'name': name,
            'display_name': preset.display_name,
            'light_primary': preset.light.primary.to_hsl_func(),
            'dark_primary': preset.dark.primary.to_hsl_func(),
        })

    # Get current design system and color from request or defaults
    current_design = request.GET.get('design', 'minimalist')
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
    manager = get_theme_manager(request)
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


# ---------------------------------------------------------------------------
# Phase 6: Django form integration demo
# ---------------------------------------------------------------------------

class ContactForm(forms.Form):
    """Sample form for demonstrating theme_form integration."""
    name = forms.CharField(
        max_length=100,
        help_text='Your full name',
    )
    email = forms.EmailField(
        help_text='We will never share your email',
    )
    subject = forms.ChoiceField(
        choices=[
            ('', 'Select a subject...'),
            ('general', 'General Inquiry'),
            ('support', 'Technical Support'),
            ('feedback', 'Feedback'),
            ('other', 'Other'),
        ],
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text='Describe your inquiry in detail',
    )
    subscribe = forms.BooleanField(
        required=False,
        label='Subscribe to newsletter',
        help_text='Get weekly updates on new features',
    )
    priority = forms.ChoiceField(
        choices=[('low', 'Low'), ('normal', 'Normal'), ('high', 'High')],
        widget=forms.RadioSelect,
        initial='normal',
    )


class LoginForm(forms.Form):
    """Sample login form."""
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False, label='Remember me')


def forms_demo(request):
    """Demonstrate Django form integration with theme_form tags."""
    contact_form = ContactForm()
    login_form = LoginForm()

    # Create a form with errors for demonstration
    error_form = ContactForm(data={'name': '', 'email': 'invalid', 'message': ''})
    error_form.is_valid()  # Trigger validation

    return render(request, 'theme_demo/forms.html', {
        'title': 'Form Integration',
        'contact_form': contact_form,
        'login_form': login_form,
        'error_form': error_form,
    })


# ---------------------------------------------------------------------------
# Phase 3: Layout templates demo
# ---------------------------------------------------------------------------

def layouts_demo(request):
    """Showcase layout templates from Phase 3."""
    layouts = [
        {
            'name': 'topbar',
            'display_name': 'Topbar',
            'description': 'Header navigation bar with main content area below. Best for marketing sites and simple apps.',
            'template': 'djust_theming/layouts/topbar.html',
        },
        {
            'name': 'sidebar',
            'display_name': 'Sidebar',
            'description': 'Fixed sidebar navigation with scrollable content area. Ideal for dashboards and admin panels.',
            'template': 'djust_theming/layouts/sidebar.html',
        },
        {
            'name': 'sidebar_topbar',
            'display_name': 'Sidebar + Topbar',
            'description': 'Combined sidebar and topbar layout. Perfect for complex applications with multiple navigation levels.',
            'template': 'djust_theming/layouts/sidebar_topbar.html',
        },
        {
            'name': 'centered',
            'display_name': 'Centered',
            'description': 'Centered content with max-width constraint. Great for auth pages, landing pages, and forms.',
            'template': 'djust_theming/layouts/centered.html',
        },
        {
            'name': 'dashboard',
            'display_name': 'Dashboard',
            'description': 'Multi-panel dashboard layout with grid-based content areas. Built for data-heavy interfaces.',
            'template': 'djust_theming/layouts/dashboard.html',
        },
        {
            'name': 'split',
            'display_name': 'Split',
            'description': 'Two-column split layout with equal or weighted halves. Useful for auth flows and comparison views.',
            'template': 'djust_theming/layouts/split.html',
        },
    ]

    return render(request, 'theme_demo/layouts.html', {
        'title': 'Layout Templates',
        'layouts': layouts,
    })


# ---------------------------------------------------------------------------
# Phase 5: Page template demos
# ---------------------------------------------------------------------------

def pages_demo(request):
    """Showcase page template tags (auth, error, utility pages)."""
    return render(request, 'theme_demo/pages.html', {
        'title': 'Page Templates',
    })


def landing(request):
    """Landing page showcasing djust-theming capabilities."""
    return render(request, 'theme_demo/landing.html', {
        'title': 'djust-theming Landing Page',
    })
