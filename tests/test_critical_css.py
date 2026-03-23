"""Tests for I10: Critical CSS Inlining — split CSS into critical and deferred parts."""

import pytest
from unittest.mock import patch

from django.test import RequestFactory, TestCase, override_settings
from django.urls import include, path

# URL config that includes djust_theming URLs with namespace
urlpatterns = [
    path("djust-theming/", include("djust_theming.urls")),
]

from djust_theming.css_generator import ThemeCSSGenerator
from djust_theming.theme_css_generator import CompleteThemeCSSGenerator
from djust_theming.manager import (
    ThemeState,
    generate_critical_css_for_state,
    generate_deferred_css_for_state,
    get_theme_config,
)


# ---------------------------------------------------------------------------
# ThemeCSSGenerator critical/deferred split
# ---------------------------------------------------------------------------

class TestThemeCSSGeneratorCriticalSplit:
    """ThemeCSSGenerator.generate_critical_css() vs generate_deferred_css()."""

    def setup_method(self):
        self.gen = ThemeCSSGenerator(preset_name="default")

    def test_critical_contains_layer_declaration(self):
        css = self.gen.generate_critical_css()
        assert "@layer" in css

    def test_critical_contains_root_variables(self):
        css = self.gen.generate_critical_css()
        assert ":root" in css
        assert "--primary:" in css
        assert "--background:" in css

    def test_critical_contains_dark_mode(self):
        css = self.gen.generate_critical_css()
        assert '[data-theme="dark"]' in css

    def test_critical_contains_system_preference(self):
        css = self.gen.generate_critical_css()
        assert "prefers-color-scheme: dark" in css

    def test_critical_contains_design_tokens(self):
        css = self.gen.generate_critical_css()
        # Design tokens include spacing, typography scale, etc.
        assert "--space-" in css or "--font-" in css or "--radius" in css

    def test_critical_does_not_contain_base_styles(self):
        css = self.gen.generate_critical_css()
        assert "font-feature-settings" not in css
        assert "prefers-reduced-motion" not in css

    def test_critical_does_not_contain_utilities(self):
        css = self.gen.generate_critical_css()
        assert ".bg-background" not in css
        assert ".text-foreground" not in css
        assert ".btn-primary" not in css

    def test_deferred_contains_base_styles(self):
        css = self.gen.generate_deferred_css()
        assert "font-feature-settings" in css

    def test_deferred_contains_utilities(self):
        css = self.gen.generate_deferred_css()
        assert ".bg-background" in css
        assert ".text-foreground" in css

    def test_deferred_does_not_contain_root_variables(self):
        css = self.gen.generate_deferred_css()
        assert ":root" not in css

    def test_deferred_does_not_contain_dark_mode_vars(self):
        css = self.gen.generate_deferred_css()
        assert "--primary:" not in css

    def test_critical_plus_deferred_covers_full(self):
        """Critical + deferred should conceptually cover all the same sections as full CSS."""
        full = self.gen.generate_css()
        critical = self.gen.generate_critical_css()
        deferred = self.gen.generate_deferred_css()
        # Key sections should appear in one or the other
        assert "--primary:" in full
        assert "--primary:" in critical
        assert ".bg-background" in full
        assert ".bg-background" in deferred

    @override_settings(LIVEVIEW_CONFIG={"theme": {"use_css_layers": False}})
    def test_critical_without_layers(self):
        gen = ThemeCSSGenerator(preset_name="default")
        css = gen.generate_critical_css()
        assert ":root" in css
        assert "@layer" not in css

    @override_settings(LIVEVIEW_CONFIG={"theme": {"use_css_layers": False}})
    def test_deferred_without_layers(self):
        gen = ThemeCSSGenerator(preset_name="default")
        css = gen.generate_deferred_css()
        assert ".bg-background" in css


# ---------------------------------------------------------------------------
# CompleteThemeCSSGenerator critical/deferred split
# ---------------------------------------------------------------------------

class TestCompleteThemeCSSGeneratorCriticalSplit:
    """CompleteThemeCSSGenerator.generate_critical_css() vs generate_deferred_css()."""

    def setup_method(self):
        self.gen = CompleteThemeCSSGenerator(theme_name="material")

    def test_critical_contains_theme_vars(self):
        css = self.gen.generate_critical_css()
        # Theme vars include typography, spacing, shadows, etc.
        assert "--font-sans:" in css
        assert "--space-base:" in css

    def test_critical_contains_color_tokens(self):
        css = self.gen.generate_critical_css()
        assert "--primary:" in css

    def test_critical_does_not_contain_component_styles(self):
        css = self.gen.generate_critical_css()
        assert ".btn" not in css

    def test_critical_does_not_contain_typography_classes(self):
        css = self.gen.generate_critical_css()
        assert ".font-sans" not in css
        assert ".text-xs" not in css

    def test_deferred_contains_component_styles(self):
        css = self.gen.generate_deferred_css()
        assert ".btn" in css or ".card" in css

    def test_deferred_contains_typography_classes(self):
        css = self.gen.generate_deferred_css()
        assert ".font-sans" in css

    def test_deferred_does_not_duplicate_tokens(self):
        css = self.gen.generate_deferred_css()
        assert "--primary:" not in css
        assert "--font-sans:" not in css


# ---------------------------------------------------------------------------
# Manager-level functions
# ---------------------------------------------------------------------------

class TestManagerCriticalDeferredFunctions:
    """Test generate_critical_css_for_state / generate_deferred_css_for_state."""

    def setup_method(self):
        self.state = ThemeState(
            theme="material",
            preset="default",
            mode="system",
            resolved_mode="light",
        )

    def test_critical_returns_string(self):
        css = generate_critical_css_for_state(self.state)
        assert isinstance(css, str)
        assert len(css) > 0

    def test_deferred_returns_string(self):
        css = generate_deferred_css_for_state(self.state)
        assert isinstance(css, str)
        assert len(css) > 0

    def test_critical_contains_tokens(self):
        css = generate_critical_css_for_state(self.state)
        assert "--primary:" in css

    def test_deferred_contains_styles(self):
        css = generate_deferred_css_for_state(self.state)
        assert ".btn" in css or ".bg-background" in css or ".font-sans" in css

    def test_critical_with_prefix(self):
        css = generate_critical_css_for_state(self.state, css_prefix="dj-")
        # Critical CSS should still work with prefix
        assert "--primary:" in css


# ---------------------------------------------------------------------------
# Config default
# ---------------------------------------------------------------------------

class TestCriticalCSSConfig:
    """Test critical_css config key exists and defaults to True."""

    def test_default_config_has_critical_css(self):
        config = get_theme_config()
        assert "critical_css" in config

    def test_default_critical_css_is_true(self):
        config = get_theme_config()
        assert config["critical_css"] is True

    @override_settings(LIVEVIEW_CONFIG={"theme": {"critical_css": False}})
    def test_critical_css_can_be_disabled(self):
        config = get_theme_config()
        assert config["critical_css"] is False


# ---------------------------------------------------------------------------
# Deferred CSS view
# ---------------------------------------------------------------------------

@override_settings(ROOT_URLCONF="tests.test_critical_css")
class TestDeferredCSSView(TestCase):
    """Test the deferred CSS view endpoint."""

    def test_deferred_css_view_returns_css(self):
        from django.test import Client
        client = Client()
        response = client.get("/djust-theming/deferred.css")
        assert response.status_code == 200
        assert response["Content-Type"] == "text/css"

    def test_deferred_css_view_has_cache_headers(self):
        from django.test import Client
        client = Client()
        response = client.get("/djust-theming/deferred.css")
        assert "max-age" in response.get("Cache-Control", "")

    def test_deferred_css_contains_styles(self):
        from django.test import Client
        client = Client()
        response = client.get("/djust-theming/deferred.css")
        content = response.content.decode()
        # Should have deferred content (utilities/components), not token vars
        assert ".bg-background" in content or ".btn" in content or ".font-sans" in content


# ---------------------------------------------------------------------------
# Template tag integration
# ---------------------------------------------------------------------------

class TestThemeHeadCriticalCSS(TestCase):
    """Test theme_head tag outputs critical/deferred split when enabled."""

    def _render_theme_head(self, critical_css=True):
        from django.template import Template, Context
        from django.test import RequestFactory

        factory = RequestFactory()
        request = factory.get("/")
        request.session = {}
        request.COOKIES = {}

        with self.settings(
            LIVEVIEW_CONFIG={"theme": {"critical_css": critical_css}},
            ROOT_URLCONF="tests.test_critical_css",
        ):
            tpl = Template("{% load theme_tags %}{% theme_head %}")
            html = tpl.render(Context({"request": request}))
        return html

    def test_critical_css_enabled_has_inline_style(self):
        html = self._render_theme_head(critical_css=True)
        assert "data-djust-theme-critical" in html

    def test_critical_css_enabled_has_preload_link(self):
        html = self._render_theme_head(critical_css=True)
        assert 'rel="preload"' in html
        assert 'as="style"' in html

    def test_critical_css_enabled_has_noscript_fallback(self):
        html = self._render_theme_head(critical_css=True)
        assert "<noscript>" in html

    def test_critical_css_disabled_uses_legacy_style(self):
        html = self._render_theme_head(critical_css=False)
        assert "data-djust-theme" in html
        assert "data-djust-theme-critical" not in html
        assert 'rel="preload"' not in html

    def test_critical_inline_contains_tokens(self):
        html = self._render_theme_head(critical_css=True)
        # The inlined critical CSS should have custom properties
        assert "--primary:" in html

    def test_critical_inline_does_not_contain_utilities(self):
        html = self._render_theme_head(critical_css=True)
        # Utilities should be in the deferred file, not inlined
        assert ".bg-background" not in html
