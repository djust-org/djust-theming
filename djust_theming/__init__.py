"""
djust_theming - A shadcn/ui-inspired theming system for Django.

Provides CSS custom properties-based theming with light/dark mode support,
multiple theme presets, and seamless Django/djust integration.
"""

from .cache import clear_css_cache
from .colors import hex_to_hsl, hex_to_rgb, hsl_to_hex, hsl_to_rgb, rgb_to_hex, rgb_to_hsl
from .components import ThemeSwitcher
from .css_generator import ThemeCSSGenerator
from .manager import ThemeManager, ThemeState, get_theme_manager
from .mixins import ThemeMixin
from .palette import PaletteGenerator
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
    # Color utilities
    "hsl_to_rgb",
    "rgb_to_hsl",
    "hex_to_rgb",
    "rgb_to_hex",
    "hex_to_hsl",
    "hsl_to_hex",
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
    # Palette generator
    "PaletteGenerator",
]

__version__ = "0.1.0"

default_app_config = "djust_theming.apps.DjustThemingConfig"
