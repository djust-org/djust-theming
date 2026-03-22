"""
djust_theming - A shadcn/ui-inspired theming system for Django.

Provides CSS custom properties-based theming with light/dark mode support,
multiple theme presets, and seamless Django/djust integration.
"""

from .cache import clear_css_cache
from .components import ThemeSwitcher
from .css_generator import ThemeCSSGenerator
from .manager import ThemeManager, ThemeState, get_theme_manager
from .mixins import ThemeMixin
from .presets import (
    BLUE_THEME,
    DEFAULT_THEME,
    GREEN_THEME,
    ORANGE_THEME,
    PURPLE_THEME,
    ROSE_THEME,
    THEME_PRESETS,
    ColorScale,
    ThemePreset,
    ThemeTokens,
)

__all__ = [
    # Cache
    "clear_css_cache",
    # Presets
    "ColorScale",
    "ThemeTokens",
    "ThemePreset",
    "THEME_PRESETS",
    "DEFAULT_THEME",
    "BLUE_THEME",
    "GREEN_THEME",
    "PURPLE_THEME",
    "ORANGE_THEME",
    "ROSE_THEME",
    # Core
    "ThemeCSSGenerator",
    "ThemeManager",
    "get_theme_manager",
    "ThemeState",
    "ThemeMixin",
    "ThemeSwitcher",
]

__version__ = "0.1.0"

default_app_config = "djust_theming.apps.DjustThemingConfig"
