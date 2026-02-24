from django.http import HttpResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import etag
from django.utils.cache import patch_vary_headers

from .manager import ThemeManager
from .theme_css_generator import CompleteThemeCSSGenerator
from .pack_css_generator import ThemePackCSSGenerator


def _generate_css_content(request):
    """Generate the CSS content based on the request."""
    manager = ThemeManager(request=request)
    state = manager.get_state()

    # Generate CSS - use pack generator if pack is set, otherwise use theme generator
    if state.pack:
        try:
            generator = ThemePackCSSGenerator(pack_name=state.pack)
            return generator.generate_css()
        except ValueError:
            # Fall back to theme generator if pack not found
            pass
            
    generator = CompleteThemeCSSGenerator(theme_name=state.theme, color_preset=state.preset)
    return generator.generate_css()


def _css_etag(request, *args, **kwargs):
    """Generate ETag based on theme state."""
    manager = ThemeManager(request=request)
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
