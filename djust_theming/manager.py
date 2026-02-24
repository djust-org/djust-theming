"""
Theme state management for djust.

Manages theme preset and mode preferences, with session persistence.
"""

from dataclasses import dataclass
from typing import Literal

from django.conf import settings
from django.http import HttpRequest

from .presets import THEME_PRESETS, ThemePreset, get_preset

ThemeMode = Literal["light", "dark", "system"]

# Default configuration
DEFAULT_CONFIG = {
    "theme": "material",  # Design system theme
    "preset": "default",  # Color preset
    "default_mode": "system",
    "persist_in_session": True,
    "session_key": "djust_theme",
    "enable_dark_mode": True,
}


def get_theme_config() -> dict:
    """Get theme configuration from Django settings."""
    liveview_config = getattr(settings, "LIVEVIEW_CONFIG", {})
    theme_config = liveview_config.get("theme", {})
    return {**DEFAULT_CONFIG, **theme_config}


@dataclass
class ThemeState:
    """Current theme state."""

    theme: str  # Design system theme (material, ios, fluent, etc.)
    preset: str  # Color preset
    mode: ThemeMode
    resolved_mode: str  # 'light' or 'dark' (system resolved to actual)
    pack: str = None  # Theme pack name (optional, overrides theme + preset)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "theme": self.theme,
            "preset": self.preset,
            "mode": self.mode,
            "resolved_mode": self.resolved_mode,
            "pack": self.pack,
        }


class ThemeManager:
    """
    Manages theme state for a session.

    Handles preset selection, mode switching, and session persistence.
    """

    VALID_MODES = ("light", "dark", "system")

    def __init__(self, request: HttpRequest | None = None):
        """
        Initialize theme manager.

        Args:
            request: Django HTTP request (for session access)
        """
        self.request = request
        self.config = get_theme_config()
        self._session_key = self.config["session_key"]

    @property
    def session(self):
        """Get session if available."""
        if self.request and hasattr(self.request, "session"):
            return self.request.session
        return None

    def _get_session_data(self) -> dict:
        """Get theme data from session."""
        if not self.session:
            return {}
        return self.session.get(self._session_key, {})

    def _set_session_data(self, data: dict) -> None:
        """Save theme data to session."""
        if self.session and self.config["persist_in_session"]:
            self.session[self._session_key] = data

    def get_state(self) -> ThemeState:
        """
        Get current theme state.

        Returns:
            ThemeState with current theme, preset and mode
        """
        from .themes import THEMES
        import logging
        logger = logging.getLogger(__name__)

        session_data = self._get_session_data()

        # Check cookies for theme, preset, and pack (set by JavaScript)
        theme = None
        preset = None
        pack = None
        if self.request:
            theme = self.request.COOKIES.get("djust_theme")
            preset = self.request.COOKIES.get("djust_theme_preset")
            pack = self.request.COOKIES.get("djust_theme_pack")
            logger.debug("Cookies: theme=%s, preset=%s, pack=%s", theme, preset, pack)

        # Fall back to session, then config default
        if not theme:
            theme = session_data.get("theme", self.config["theme"])
        if not preset:
            preset = session_data.get("preset", self.config["preset"])
        if not pack:
            pack = session_data.get("pack")

        mode = session_data.get("mode", self.config["default_mode"])
        
        logger.debug("Resolved before validation: theme=%s, preset=%s, pack=%s, mode=%s", theme, preset, pack, mode)

        # If pack is set, override theme and preset from pack
        if pack:
            from .theme_packs import get_theme_pack
            theme_pack = get_theme_pack(pack)
            if theme_pack:
                theme = theme_pack.design_theme
                preset = theme_pack.color_preset

        # Validate theme
        if theme not in THEMES:
            theme = "material"

        # Validate preset
        if preset not in THEME_PRESETS:
            preset = "default"

        # Validate mode
        if mode not in self.VALID_MODES:
            mode = "system"

        # Resolve system mode (default to light for server-side)
        resolved_mode = mode if mode != "system" else "light"

        return ThemeState(
            theme=theme,
            preset=preset,
            mode=mode,
            resolved_mode=resolved_mode,
            pack=pack,
        )

    def set_theme(self, theme_name: str) -> bool:
        """
        Set design system theme.

        Args:
            theme_name: Name of theme to use (material, ios, fluent, etc.)

        Returns:
            True if theme was valid and set
        """
        from .themes import THEMES

        if theme_name not in THEMES:
            return False

        session_data = self._get_session_data()
        session_data["theme"] = theme_name
        self._set_session_data(session_data)
        return True

    def set_preset(self, preset_name: str) -> bool:
        """
        Set color preset.

        Args:
            preset_name: Name of color preset to use

        Returns:
            True if preset was valid and set
        """
        if preset_name not in THEME_PRESETS:
            return False

        session_data = self._get_session_data()
        session_data["preset"] = preset_name
        self._set_session_data(session_data)
        return True

    def set_mode(self, mode: str) -> bool:
        """
        Set theme mode.

        Args:
            mode: 'light', 'dark', or 'system'

        Returns:
            True if mode was valid and set
        """
        if mode not in self.VALID_MODES:
            return False

        if mode == "dark" and not self.config["enable_dark_mode"]:
            return False

        session_data = self._get_session_data()
        session_data["mode"] = mode
        self._set_session_data(session_data)
        return True

    def toggle_mode(self) -> str:
        """
        Toggle between light and dark mode.

        If currently in system mode, switches to opposite of system preference.

        Returns:
            New mode ('light' or 'dark')
        """
        state = self.get_state()

        # Toggle based on resolved mode
        new_mode = "light" if state.resolved_mode == "dark" else "dark"
        self.set_mode(new_mode)
        return new_mode

    def get_preset(self) -> ThemePreset:
        """Get current theme preset object."""
        state = self.get_state()
        return get_preset(state.preset)

    def get_available_presets(self) -> list[dict]:
        """Get list of available preset metadata."""
        return [
            {
                "name": preset.name,
                "display_name": preset.display_name,
                "description": preset.description,
                "is_active": preset.name == self.get_state().preset,
                "primary_hsl": preset.dark.primary.to_hsl(),
                "primary_hsl_light": preset.light.primary.to_hsl(),
            }
            for preset in THEME_PRESETS.values()
        ]

    def get_context(self) -> dict:
        """
        Get template context for theme rendering.

        Returns:
            Dict with theme state and presets for templates
        """
        state = self.get_state()
        return {
            "theme_preset": state.preset,
            "theme_mode": state.mode,
            "theme_resolved_mode": state.resolved_mode,
            "theme_presets": self.get_available_presets(),
            "dark_mode_enabled": self.config["enable_dark_mode"],
        }
