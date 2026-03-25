"""
Theme gallery view -- renders every component in every variant.

Gated by ``DEBUG=True`` or ``is_staff`` for production safety.
"""

from django.conf import settings
from django.http import HttpResponseForbidden
from django.template.loader import render_to_string
from django.http import HttpResponse

from .context import build_gallery_context


def gallery_view(request):
    """Render the theme component gallery page.

    Access control:
    - Always accessible when ``DEBUG=True``
    - When ``DEBUG=False``, requires ``request.user.is_staff``

    Supports ``?preset=<name>`` query parameter to switch color presets.
    """
    # Access control
    if not settings.DEBUG:
        user = getattr(request, "user", None)
        if not user or not getattr(user, "is_staff", False):
            return HttpResponseForbidden(
                "Gallery is only available in DEBUG mode or for staff users."
            )

    # Read preset from query param
    preset_name = request.GET.get("preset", "default")

    ctx = build_gallery_context(preset_name=preset_name)
    ctx["request"] = request

    # Extra context variables consumed directly by template tags in gallery.html
    ctx.update(_template_sample_data())

    html = render_to_string(
        "djust_theming/gallery/gallery.html",
        ctx,
        request=request,
    )
    return HttpResponse(html)


def _template_sample_data() -> dict:
    """Return sample data dicts used by template tags in the gallery template."""
    return {
        "tab_data": [
            {"label": "Tab 1", "content": "Content for tab 1."},
            {"label": "Tab 2", "content": "Content for tab 2."},
            {"label": "Tab 3", "content": "Content for tab 3."},
        ],
        "table_headers": ["Name", "Email", "Role"],
        "table_rows": [
            ["Alice", "alice@example.com", "Admin"],
            ["Bob", "bob@example.com", "Editor"],
            ["Charlie", "charlie@example.com", "Viewer"],
        ],
        "select_options": [
            {"value": "opt1", "label": "Option 1"},
            {"value": "opt2", "label": "Option 2"},
            {"value": "opt3", "label": "Option 3"},
        ],
        "radio_options": [
            {"value": "sm", "label": "Small"},
            {"value": "md", "label": "Medium"},
            {"value": "lg", "label": "Large"},
        ],
        "breadcrumb_items": [
            {"label": "Home", "url": "/"},
            {"label": "Products", "url": "/products/"},
            {"label": "Current Page", "url": ""},
        ],
        "nav_group_items": [
            {"label": "Users", "url": "/admin/users/"},
            {"label": "Settings", "url": "/admin/settings/"},
        ],
        "nav_items": [
            {"label": "Home", "url": "/"},
            {"label": "Docs", "url": "/docs/"},
            {"label": "Gallery", "url": "/gallery/"},
        ],
        "sidebar_sections": [
            {
                "title": "Main",
                "items": [
                    {"label": "Dashboard", "url": "/dash/"},
                    {"label": "Analytics", "url": "/analytics/"},
                ],
            },
            {
                "title": "Settings",
                "items": [
                    {"label": "Profile", "url": "/profile/"},
                    {"label": "Billing", "url": "/billing/"},
                ],
            },
        ],
    }
