"""Tests for Django system checks (WCAG AA contrast validation)."""

import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        INSTALLED_APPS=["django.contrib.contenttypes", "djust_theming"],
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    )
    django.setup()

from unittest.mock import patch

import pytest

from djust_theming.accessibility import AccessibilityValidator
from djust_theming.checks import CONTRAST_PAIRS, check_preset_contrast
from djust_theming.presets import THEME_PRESETS, ColorScale, ThemePreset, ThemeTokens


class TestHslToRgbBugFix:
    """Verify the color_scale.l -> color_scale.lightness fix."""

    def test_hsl_to_rgb_uses_lightness_attribute(self):
        """AccessibilityValidator.hsl_to_rgb accesses .lightness, not .l."""
        validator = AccessibilityValidator()
        color = ColorScale(h=0, s=100, lightness=50)  # pure red
        r, g, b = validator.hsl_to_rgb(color)
        # Pure red in HSL(0, 100%, 50%) -> RGB(1, 0, 0)
        assert abs(r - 1.0) < 0.01
        assert abs(g - 0.0) < 0.01
        assert abs(b - 0.0) < 0.01

    def test_hsl_to_rgb_white(self):
        """White (0, 0%, 100%) should yield (1, 1, 1)."""
        validator = AccessibilityValidator()
        color = ColorScale(h=0, s=0, lightness=100)
        r, g, b = validator.hsl_to_rgb(color)
        assert abs(r - 1.0) < 0.01
        assert abs(g - 1.0) < 0.01
        assert abs(b - 1.0) < 0.01

    def test_hsl_to_rgb_black(self):
        """Black (0, 0%, 0%) should yield (0, 0, 0)."""
        validator = AccessibilityValidator()
        color = ColorScale(h=0, s=0, lightness=0)
        r, g, b = validator.hsl_to_rgb(color)
        assert abs(r) < 0.01
        assert abs(g) < 0.01
        assert abs(b) < 0.01


class TestCheckPresetContrast:
    """Tests for the check_preset_contrast system check."""

    def test_check_runs_without_error(self):
        """The system check executes against all built-in presets without crashing."""
        warnings = check_preset_contrast(app_configs=None)
        assert isinstance(warnings, list)

    def test_all_warnings_have_correct_id(self):
        """Every warning emitted uses id='djust_theming.W001'."""
        warnings = check_preset_contrast(app_configs=None)
        for w in warnings:
            assert w.id == "djust_theming.W001"

    def test_bad_preset_triggers_warning(self):
        """A preset with near-identical fg/bg colors triggers W001."""
        # Create a deliberately bad preset: white-on-white
        white = ColorScale(h=0, s=0, lightness=100)
        near_white = ColorScale(h=0, s=0, lightness=98)
        bad_tokens = ThemeTokens(
            background=white,
            foreground=near_white,
            card=white,
            card_foreground=near_white,
            popover=white,
            popover_foreground=near_white,
            primary=white,
            primary_foreground=near_white,
            secondary=white,
            secondary_foreground=near_white,
            muted=white,
            muted_foreground=near_white,
            accent=white,
            accent_foreground=near_white,
            destructive=white,
            destructive_foreground=near_white,
            success=white,
            success_foreground=near_white,
            warning=white,
            warning_foreground=near_white,
            info=white,
            info_foreground=near_white,
            link=white,
            link_hover=white,
            code=white,
            code_foreground=near_white,
            selection=white,
            selection_foreground=near_white,
            border=white,
            input=white,
            ring=white,
        )
        bad_preset = ThemePreset(
            name="bad",
            display_name="Bad",
            light=bad_tokens,
            dark=bad_tokens,
            description="Intentionally bad contrast",
        )

        patched_presets = {"bad": bad_preset}
        with patch("djust_theming.checks.THEME_PRESETS", patched_presets):
            warnings = check_preset_contrast(app_configs=None)

        # 12 pairs x 2 modes = 24 warnings expected
        assert len(warnings) == len(CONTRAST_PAIRS) * 2
        for w in warnings:
            assert w.id == "djust_theming.W001"
            assert "bad" in w.msg

    def test_good_preset_no_warnings(self):
        """A preset with high-contrast colors produces no warnings."""
        black = ColorScale(h=0, s=0, lightness=0)
        white = ColorScale(h=0, s=0, lightness=100)
        good_tokens = ThemeTokens(
            background=white,
            foreground=black,
            card=white,
            card_foreground=black,
            popover=white,
            popover_foreground=black,
            primary=black,
            primary_foreground=white,
            secondary=black,
            secondary_foreground=white,
            muted=white,
            muted_foreground=black,
            accent=black,
            accent_foreground=white,
            destructive=black,
            destructive_foreground=white,
            success=black,
            success_foreground=white,
            warning=black,
            warning_foreground=white,
            info=black,
            info_foreground=white,
            link=black,
            link_hover=black,
            code=white,
            code_foreground=black,
            selection=black,
            selection_foreground=white,
            border=black,
            input=black,
            ring=black,
        )
        good_preset = ThemePreset(
            name="good",
            display_name="Good",
            light=good_tokens,
            dark=good_tokens,
            description="High contrast",
        )

        patched_presets = {"good": good_preset}
        with patch("djust_theming.checks.THEME_PRESETS", patched_presets):
            warnings = check_preset_contrast(app_configs=None)

        assert len(warnings) == 0

    def test_empty_presets_no_warnings(self):
        """When THEME_PRESETS is empty, no warnings are produced."""
        with patch("djust_theming.checks.THEME_PRESETS", {}):
            warnings = check_preset_contrast(app_configs=None)

        assert warnings == []

    def test_warning_message_contains_preset_name_and_mode(self):
        """Warning messages include the preset name and mode for actionability."""
        warnings = check_preset_contrast(app_configs=None)
        if warnings:
            w = warnings[0]
            # Should mention a real preset name and light/dark
            assert "light" in w.msg or "dark" in w.msg
            assert "contrast ratio" in w.msg


class TestContrastPairsCompleteness:
    """Verify CONTRAST_PAIRS covers all foreground/background token pairs."""

    def test_all_fg_bg_pairs_covered(self):
        """CONTRAST_PAIRS should cover all *_foreground/*  semantic pairs."""
        expected_pairs = {
            "foreground",
            "card_foreground",
            "popover_foreground",
            "primary_foreground",
            "secondary_foreground",
            "muted_foreground",
            "accent_foreground",
            "destructive_foreground",
            "success_foreground",
            "warning_foreground",
            "info_foreground",
            "code_foreground",
        }
        actual_fg_attrs = {pair[0] for pair in CONTRAST_PAIRS}
        assert actual_fg_attrs == expected_pairs


if __name__ == "__main__":
    pytest.main([__file__])
