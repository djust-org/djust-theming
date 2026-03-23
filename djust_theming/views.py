from django.http import HttpResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import etag
from django.utils.cache import patch_vary_headers

from .manager import get_theme_config, get_theme_manager
from .theme_css_generator import generate_theme_css
from .pack_css_generator import generate_pack_css


def _generate_css_content(request):
    """Generate the CSS content based on the request."""
    manager = get_theme_manager(request)
    state = manager.get_state()

    # Generate CSS - use pack generator if pack is set, otherwise use theme generator
    if state.pack:
        try:
            return generate_pack_css(pack_name=state.pack)
        except ValueError:
            # Fall back to theme generator if pack not found
            pass

    config = get_theme_config()
    prefix = config.get("css_prefix", "")
    return generate_theme_css(theme_name=state.theme, color_preset=state.preset, css_prefix=prefix)


def _css_etag(request, *args, **kwargs):
    """Generate ETag based on theme state."""
    manager = get_theme_manager(request)
    state = manager.get_state()
    return f"{state.theme}-{state.preset}-{state.mode}-{state.pack}"


@cache_control(max_age=3600, private=True)  # Cache for 1 hour, private (vary by user)
@etag(_css_etag)
def theme_css_view(request):
    """
    Serve dynamic theme CSS.
    
    This view generates the CSS for the current theme configuration.
    It uses ETag and Cache-Control headers to ensure efficient caching
    while respecting user-specific theme settings.
    """
    css = _generate_css_content(request)
    response = HttpResponse(css, content_type="text/css")
    patch_vary_headers(response, ["Cookie"])
    return response
