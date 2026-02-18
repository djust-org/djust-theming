"""
Theme preset definitions using HSL color tokens.

Based on shadcn/ui theming system with CSS custom properties.
Each preset includes both light and dark mode token sets.
"""

from dataclasses import dataclass


@dataclass
class ColorScale:
    """HSL color representation for CSS custom properties."""

    h: int  # Hue 0-360
    s: int  # Saturation 0-100
    lightness: int  # Lightness 0-100

    def to_hsl(self) -> str:
        """Return HSL values for CSS variable (without hsl() wrapper)."""
        return f"{self.h} {self.s}% {self.lightness}%"

    def to_hsl_func(self) -> str:
        """Return complete hsl() function."""
        return f"hsl({self.h}, {self.s}%, {self.lightness}%)"

    def with_lightness(self, new_lightness: int) -> "ColorScale":
        """Return a new ColorScale with modified lightness."""
        return ColorScale(self.h, self.s, new_lightness)

    def with_saturation(self, new_saturation: int) -> "ColorScale":
        """Return a new ColorScale with modified saturation."""
        return ColorScale(self.h, new_saturation, self.lightness)


@dataclass
class ThemeTokens:
    """
    Complete token set for a theme mode.

    Follows shadcn/ui naming conventions with extensions for
    success, warning, info, and additional semantic states.
    """

    # Backgrounds
    background: ColorScale
    foreground: ColorScale

    # Card surfaces
    card: ColorScale
    card_foreground: ColorScale

    # Popover surfaces
    popover: ColorScale
    popover_foreground: ColorScale

    # Primary action color
    primary: ColorScale
    primary_foreground: ColorScale

    # Secondary/muted action
    secondary: ColorScale
    secondary_foreground: ColorScale

    # Muted backgrounds
    muted: ColorScale
    muted_foreground: ColorScale

    # Accent for highlights
    accent: ColorScale
    accent_foreground: ColorScale

    # Destructive/error
    destructive: ColorScale
    destructive_foreground: ColorScale

    # Success state (extension)
    success: ColorScale
    success_foreground: ColorScale

    # Warning state (extension)
    warning: ColorScale
    warning_foreground: ColorScale

    # Info state (extension)
    info: ColorScale
    info_foreground: ColorScale

    # Link color (extension)
    link: ColorScale
    link_hover: ColorScale

    # Code/mono background (extension)
    code: ColorScale
    code_foreground: ColorScale

    # Selection/highlight (extension)
    selection: ColorScale
    selection_foreground: ColorScale

    # UI elements
    border: ColorScale
    input: ColorScale
    ring: ColorScale

    # Border radius multiplier
    radius: float = 0.5


@dataclass
class ThemePreset:
    """A complete theme with light and dark mode tokens."""

    name: str
    display_name: str
    light: ThemeTokens
    dark: ThemeTokens
    description: str = ""


# =============================================================================
# Default Theme (Neutral Zinc)
# =============================================================================

_DEFAULT_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 100),
    foreground=ColorScale(240, 10, 4),
    card=ColorScale(0, 0, 100),
    card_foreground=ColorScale(240, 10, 4),
    popover=ColorScale(0, 0, 100),
    popover_foreground=ColorScale(240, 10, 4),
    primary=ColorScale(240, 6, 10),
    primary_foreground=ColorScale(0, 0, 98),
    secondary=ColorScale(240, 5, 96),
    secondary_foreground=ColorScale(240, 6, 10),
    muted=ColorScale(240, 5, 96),
    muted_foreground=ColorScale(240, 5, 40),  # Changed from 46 to 40 for better contrast
    accent=ColorScale(240, 5, 96),
    accent_foreground=ColorScale(240, 6, 10),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 76, 36),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 50),
    warning_foreground=ColorScale(0, 0, 98),
    info=ColorScale(199, 89, 48),
    info_foreground=ColorScale(0, 0, 98),
    link=ColorScale(221, 83, 53),
    link_hover=ColorScale(221, 83, 45),
    code=ColorScale(240, 5, 94),
    code_foreground=ColorScale(240, 10, 20),
    selection=ColorScale(240, 100, 80),
    selection_foreground=ColorScale(240, 10, 4),
    border=ColorScale(240, 6, 90),
    input=ColorScale(240, 6, 90),
    ring=ColorScale(240, 6, 10),
    radius=0.5,
)

_DEFAULT_DARK = ThemeTokens(
    background=ColorScale(240, 10, 4),
    foreground=ColorScale(0, 0, 98),
    card=ColorScale(240, 10, 4),
    card_foreground=ColorScale(0, 0, 98),
    popover=ColorScale(240, 10, 4),
    popover_foreground=ColorScale(0, 0, 98),
    primary=ColorScale(0, 0, 98),
    primary_foreground=ColorScale(240, 6, 10),
    secondary=ColorScale(240, 4, 16),
    secondary_foreground=ColorScale(0, 0, 98),
    muted=ColorScale(240, 4, 16),
    muted_foreground=ColorScale(240, 5, 75),  # Changed from 65 to 75 for better contrast on dark bg
    accent=ColorScale(240, 4, 16),
    accent_foreground=ColorScale(0, 0, 98),
    destructive=ColorScale(0, 62, 30),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 69, 28),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 40),
    warning_foreground=ColorScale(0, 0, 98),
    info=ColorScale(199, 89, 60),
    info_foreground=ColorScale(0, 0, 98),
    link=ColorScale(221, 83, 65),
    link_hover=ColorScale(221, 83, 75),
    code=ColorScale(240, 4, 12),
    code_foreground=ColorScale(240, 5, 80),
    selection=ColorScale(240, 100, 30),
    selection_foreground=ColorScale(0, 0, 98),
    border=ColorScale(240, 4, 16),
    input=ColorScale(240, 4, 16),
    ring=ColorScale(240, 5, 84),
    radius=0.5,
)

DEFAULT_THEME = ThemePreset(
    name="default",
    display_name="Default",
    description="Neutral zinc theme with professional aesthetics",
    light=_DEFAULT_LIGHT,
    dark=_DEFAULT_DARK,
)


# =============================================================================
# Shadcn Theme (Neutral Zinc Compatibility)
# =============================================================================

_SHADCN_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 100),
    foreground=ColorScale(240, 10, 4),
    card=ColorScale(0, 0, 100),
    card_foreground=ColorScale(240, 10, 4),
    popover=ColorScale(0, 0, 100),
    popover_foreground=ColorScale(240, 10, 4),
    primary=ColorScale(240, 6, 10),
    primary_foreground=ColorScale(0, 0, 98),
    secondary=ColorScale(240, 5, 96),
    secondary_foreground=ColorScale(240, 6, 10),
    muted=ColorScale(240, 5, 96),
    muted_foreground=ColorScale(240, 5, 40),
    accent=ColorScale(240, 5, 96),
    accent_foreground=ColorScale(240, 6, 10),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 76, 36),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 50),
    warning_foreground=ColorScale(0, 0, 98),
    info=ColorScale(199, 89, 48),
    info_foreground=ColorScale(0, 0, 98),
    link=ColorScale(221, 83, 53),
    link_hover=ColorScale(221, 83, 45),
    code=ColorScale(240, 5, 94),
    code_foreground=ColorScale(240, 10, 20),
    selection=ColorScale(240, 100, 80),
    selection_foreground=ColorScale(240, 10, 4),
    border=ColorScale(240, 6, 90),
    input=ColorScale(240, 6, 90),
    ring=ColorScale(240, 6, 10),
    radius=0.5,
)

_SHADCN_DARK = ThemeTokens(
    background=ColorScale(240, 10, 4),
    foreground=ColorScale(0, 0, 98),
    card=ColorScale(240, 10, 4),
    card_foreground=ColorScale(0, 0, 98),
    popover=ColorScale(240, 10, 4),
    popover_foreground=ColorScale(0, 0, 98),
    primary=ColorScale(0, 0, 98),
    primary_foreground=ColorScale(240, 6, 10),
    secondary=ColorScale(240, 4, 16),
    secondary_foreground=ColorScale(0, 0, 98),
    muted=ColorScale(240, 4, 16),
    muted_foreground=ColorScale(240, 5, 75),
    accent=ColorScale(240, 4, 16),
    accent_foreground=ColorScale(0, 0, 98),
    destructive=ColorScale(0, 62, 30),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 69, 28),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 40),
    warning_foreground=ColorScale(0, 0, 98),
    info=ColorScale(199, 89, 60),
    info_foreground=ColorScale(0, 0, 98),
    link=ColorScale(221, 83, 65),
    link_hover=ColorScale(221, 83, 75),
    code=ColorScale(240, 4, 12),
    code_foreground=ColorScale(240, 5, 80),
    selection=ColorScale(240, 100, 30),
    selection_foreground=ColorScale(0, 0, 98),
    border=ColorScale(240, 4, 16),
    input=ColorScale(240, 4, 16),
    ring=ColorScale(240, 5, 84),
    radius=0.5,
)

SHADCN_THEME = ThemePreset(
    name="shadcn",
    display_name="Shadcn",
    description="Shadcn-compatible neutral theme",
    light=_SHADCN_LIGHT,
    dark=_SHADCN_DARK,
)


# =============================================================================
# Blue Theme (Professional/Corporate)
# =============================================================================

_BLUE_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 100),
    foreground=ColorScale(222, 47, 11),
    card=ColorScale(0, 0, 100),
    card_foreground=ColorScale(222, 47, 11),
    popover=ColorScale(0, 0, 100),
    popover_foreground=ColorScale(222, 47, 11),
    primary=ColorScale(221, 83, 53),
    primary_foreground=ColorScale(210, 40, 98),
    secondary=ColorScale(210, 40, 96),
    secondary_foreground=ColorScale(222, 47, 11),
    muted=ColorScale(210, 40, 96),
    muted_foreground=ColorScale(215, 16, 38),
    accent=ColorScale(210, 40, 96),
    accent_foreground=ColorScale(222, 47, 11),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 76, 36),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 50),
    warning_foreground=ColorScale(0, 0, 98),
    info=ColorScale(199, 89, 48),
    info_foreground=ColorScale(0, 0, 98),
    link=ColorScale(221, 83, 53),
    link_hover=ColorScale(221, 83, 45),
    code=ColorScale(221, 95, 94),
    code_foreground=ColorScale(240, 10, 20),
    selection=ColorScale(221, 100, 80),
    selection_foreground=ColorScale(240, 10, 4),
    border=ColorScale(214, 32, 91),
    input=ColorScale(214, 32, 91),
    ring=ColorScale(221, 83, 53),
    radius=0.5,
)

_BLUE_DARK = ThemeTokens(
    background=ColorScale(222, 47, 11),
    foreground=ColorScale(210, 40, 98),
    card=ColorScale(222, 47, 11),
    card_foreground=ColorScale(210, 40, 98),
    popover=ColorScale(222, 47, 11),
    popover_foreground=ColorScale(210, 40, 98),
    primary=ColorScale(217, 91, 60),
    primary_foreground=ColorScale(222, 47, 11),
    secondary=ColorScale(217, 33, 17),
    secondary_foreground=ColorScale(210, 40, 98),
    muted=ColorScale(217, 33, 17),
    muted_foreground=ColorScale(215, 15, 85),  # Increased from 65% to 85% for better contrast
    accent=ColorScale(217, 33, 17),
    accent_foreground=ColorScale(210, 40, 98),
    destructive=ColorScale(0, 62, 30),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 69, 28),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 40),
    warning_foreground=ColorScale(0, 0, 98),
    info=ColorScale(199, 89, 60),
    info_foreground=ColorScale(0, 0, 98),
    link=ColorScale(221, 83, 65),
    link_hover=ColorScale(221, 83, 75),
    code=ColorScale(221, 30, 12),
    code_foreground=ColorScale(240, 5, 80),
    selection=ColorScale(221, 100, 30),
    selection_foreground=ColorScale(0, 0, 98),
    border=ColorScale(217, 33, 17),
    input=ColorScale(217, 33, 17),
    ring=ColorScale(224, 76, 48),
    radius=0.5,
)

BLUE_THEME = ThemePreset(
    name="blue",
    display_name="Blue",
    description="Professional blue theme for corporate applications",
    light=_BLUE_LIGHT,
    dark=_BLUE_DARK,
)


# =============================================================================
# Green Theme (Nature/Growth)
# =============================================================================

_GREEN_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 100),
    foreground=ColorScale(140, 40, 10),
    card=ColorScale(0, 0, 100),
    card_foreground=ColorScale(140, 40, 10),
    popover=ColorScale(0, 0, 100),
    popover_foreground=ColorScale(140, 40, 10),
    primary=ColorScale(142, 76, 36),
    primary_foreground=ColorScale(138, 76, 97),
    secondary=ColorScale(138, 30, 95),
    secondary_foreground=ColorScale(140, 40, 10),
    muted=ColorScale(138, 30, 95),
    muted_foreground=ColorScale(140, 15, 38),  # Changed from 45 to 38 for better contrast
    accent=ColorScale(138, 30, 95),
    accent_foreground=ColorScale(140, 40, 10),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 76, 36),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 50),
    warning_foreground=ColorScale(0, 0, 98),
    info=ColorScale(199, 89, 48),
    info_foreground=ColorScale(0, 0, 98),
    link=ColorScale(142, 76, 40),
    link_hover=ColorScale(142, 76, 32),
    code=ColorScale(142, 20, 94),
    code_foreground=ColorScale(240, 10, 20),
    selection=ColorScale(142, 100, 80),
    selection_foreground=ColorScale(240, 10, 4),
    border=ColorScale(140, 20, 88),
    input=ColorScale(140, 20, 88),
    ring=ColorScale(142, 76, 36),
    radius=0.5,
)

_GREEN_DARK = ThemeTokens(
    background=ColorScale(140, 40, 8),
    foreground=ColorScale(138, 76, 97),
    card=ColorScale(140, 40, 8),
    card_foreground=ColorScale(138, 76, 97),
    popover=ColorScale(140, 40, 8),
    popover_foreground=ColorScale(138, 76, 97),
    primary=ColorScale(142, 69, 45),
    primary_foreground=ColorScale(140, 40, 8),
    secondary=ColorScale(140, 30, 16),
    secondary_foreground=ColorScale(138, 76, 97),
    muted=ColorScale(140, 30, 16),
    muted_foreground=ColorScale(140, 15, 85),  # Increased from 60% to 85% for better contrast
    accent=ColorScale(140, 30, 16),
    accent_foreground=ColorScale(138, 76, 97),
    destructive=ColorScale(0, 62, 30),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 69, 28),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 40),
    warning_foreground=ColorScale(0, 0, 98),
    info=ColorScale(199, 89, 60),
    info_foreground=ColorScale(0, 0, 98),
    link=ColorScale(142, 69, 45),
    link_hover=ColorScale(142, 69, 55),
    code=ColorScale(142, 30, 12),
    code_foreground=ColorScale(240, 5, 80),
    selection=ColorScale(142, 100, 30),
    selection_foreground=ColorScale(0, 0, 98),
    border=ColorScale(140, 30, 16),
    input=ColorScale(140, 30, 16),
    ring=ColorScale(142, 69, 45),
    radius=0.5,
)

GREEN_THEME = ThemePreset(
    name="green",
    display_name="Green",
    description="Nature-inspired green theme for growth and sustainability",
    light=_GREEN_LIGHT,
    dark=_GREEN_DARK,
)


# =============================================================================
# Purple Theme (Creative/Premium)
# =============================================================================

_PURPLE_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 100),
    foreground=ColorScale(270, 50, 11),
    card=ColorScale(0, 0, 100),
    card_foreground=ColorScale(270, 50, 11),
    popover=ColorScale(0, 0, 100),
    popover_foreground=ColorScale(270, 50, 11),
    primary=ColorScale(270, 50, 50),
    primary_foreground=ColorScale(270, 80, 98),
    secondary=ColorScale(270, 30, 96),
    secondary_foreground=ColorScale(270, 50, 11),
    muted=ColorScale(270, 30, 96),
    muted_foreground=ColorScale(270, 15, 38),
    accent=ColorScale(270, 30, 96),
    accent_foreground=ColorScale(270, 50, 11),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 76, 36),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 50),
    warning_foreground=ColorScale(0, 0, 98),
    info=ColorScale(199, 89, 48),
    info_foreground=ColorScale(0, 0, 98),
    link=ColorScale(271, 81, 56),
    link_hover=ColorScale(271, 81, 48),
    code=ColorScale(271, 20, 94),
    code_foreground=ColorScale(240, 10, 20),
    selection=ColorScale(271, 100, 80),
    selection_foreground=ColorScale(240, 10, 4),
    border=ColorScale(270, 20, 90),
    input=ColorScale(270, 20, 90),
    ring=ColorScale(270, 50, 50),
    radius=0.5,
)

_PURPLE_DARK = ThemeTokens(
    background=ColorScale(270, 50, 8),
    foreground=ColorScale(270, 80, 98),
    card=ColorScale(270, 50, 8),
    card_foreground=ColorScale(270, 80, 98),
    popover=ColorScale(270, 50, 8),
    popover_foreground=ColorScale(270, 80, 98),
    primary=ColorScale(270, 60, 60),
    primary_foreground=ColorScale(270, 50, 8),
    secondary=ColorScale(270, 30, 16),
    secondary_foreground=ColorScale(270, 80, 98),
    muted=ColorScale(270, 30, 16),
    muted_foreground=ColorScale(270, 15, 85),  # Increased from 60% to 85% for better contrast
    accent=ColorScale(270, 30, 16),
    accent_foreground=ColorScale(270, 80, 98),
    destructive=ColorScale(0, 62, 30),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 69, 28),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 40),
    warning_foreground=ColorScale(0, 0, 98),
    info=ColorScale(199, 89, 60),
    info_foreground=ColorScale(0, 0, 98),
    link=ColorScale(271, 91, 65),
    link_hover=ColorScale(271, 91, 75),
    code=ColorScale(271, 30, 12),
    code_foreground=ColorScale(240, 5, 80),
    selection=ColorScale(271, 100, 30),
    selection_foreground=ColorScale(0, 0, 98),
    border=ColorScale(270, 30, 16),
    input=ColorScale(270, 30, 16),
    ring=ColorScale(270, 60, 60),
    radius=0.5,
)

PURPLE_THEME = ThemePreset(
    name="purple",
    display_name="Purple",
    description="Creative purple theme for premium applications",
    light=_PURPLE_LIGHT,
    dark=_PURPLE_DARK,
)


# =============================================================================
# Orange Theme (Energetic/Warm)
# =============================================================================

_ORANGE_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 100),
    foreground=ColorScale(20, 50, 10),
    card=ColorScale(0, 0, 100),
    card_foreground=ColorScale(20, 50, 10),
    popover=ColorScale(0, 0, 100),
    popover_foreground=ColorScale(20, 50, 10),
    primary=ColorScale(24, 95, 53),
    primary_foreground=ColorScale(24, 100, 98),
    secondary=ColorScale(24, 30, 95),
    secondary_foreground=ColorScale(20, 50, 10),
    muted=ColorScale(24, 30, 95),
    muted_foreground=ColorScale(20, 15, 38),
    accent=ColorScale(24, 30, 95),
    accent_foreground=ColorScale(20, 50, 10),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 76, 36),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 50),
    warning_foreground=ColorScale(0, 0, 98),
    info=ColorScale(199, 89, 48),
    info_foreground=ColorScale(0, 0, 98),
    link=ColorScale(25, 95, 53),
    link_hover=ColorScale(25, 95, 45),
    code=ColorScale(25, 20, 94),
    code_foreground=ColorScale(240, 10, 20),
    selection=ColorScale(25, 100, 80),
    selection_foreground=ColorScale(240, 10, 4),
    border=ColorScale(24, 25, 88),
    input=ColorScale(24, 25, 88),
    ring=ColorScale(24, 95, 53),
    radius=0.5,
)

_ORANGE_DARK = ThemeTokens(
    background=ColorScale(20, 50, 8),
    foreground=ColorScale(24, 100, 98),
    card=ColorScale(20, 50, 8),
    card_foreground=ColorScale(24, 100, 98),
    popover=ColorScale(20, 50, 8),
    popover_foreground=ColorScale(24, 100, 98),
    primary=ColorScale(24, 95, 55),
    primary_foreground=ColorScale(20, 50, 8),
    secondary=ColorScale(20, 30, 16),
    secondary_foreground=ColorScale(24, 100, 98),
    muted=ColorScale(20, 30, 16),
    muted_foreground=ColorScale(20, 15, 85),  # Increased from 60% to 85% for better contrast
    accent=ColorScale(20, 30, 16),
    accent_foreground=ColorScale(24, 100, 98),
    destructive=ColorScale(0, 62, 30),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 69, 28),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 40),
    warning_foreground=ColorScale(0, 0, 98),
    info=ColorScale(199, 89, 60),
    info_foreground=ColorScale(0, 0, 98),
    link=ColorScale(25, 95, 55),
    link_hover=ColorScale(25, 95, 65),
    code=ColorScale(25, 30, 12),
    code_foreground=ColorScale(240, 5, 80),
    selection=ColorScale(25, 100, 30),
    selection_foreground=ColorScale(0, 0, 98),
    border=ColorScale(20, 30, 16),
    input=ColorScale(20, 30, 16),
    ring=ColorScale(24, 95, 55),
    radius=0.5,
)

ORANGE_THEME = ThemePreset(
    name="orange",
    display_name="Orange",
    description="Energetic orange theme for warm, engaging interfaces",
    light=_ORANGE_LIGHT,
    dark=_ORANGE_DARK,
)


# =============================================================================
# Rose Theme (Friendly/Modern)
# =============================================================================

_ROSE_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 100),
    foreground=ColorScale(346, 40, 11),
    card=ColorScale(0, 0, 100),
    card_foreground=ColorScale(346, 40, 11),
    popover=ColorScale(0, 0, 100),
    popover_foreground=ColorScale(346, 40, 11),
    primary=ColorScale(346, 77, 50),
    primary_foreground=ColorScale(346, 100, 98),
    secondary=ColorScale(346, 30, 96),
    secondary_foreground=ColorScale(346, 40, 11),
    muted=ColorScale(346, 30, 96),
    muted_foreground=ColorScale(346, 15, 38),
    accent=ColorScale(346, 30, 96),
    accent_foreground=ColorScale(346, 40, 11),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 76, 36),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 50),
    warning_foreground=ColorScale(0, 0, 98),
    info=ColorScale(199, 89, 48),
    info_foreground=ColorScale(0, 0, 98),
    link=ColorScale(347, 77, 50),
    link_hover=ColorScale(347, 77, 42),
    code=ColorScale(347, 20, 94),
    code_foreground=ColorScale(240, 10, 20),
    selection=ColorScale(347, 100, 80),
    selection_foreground=ColorScale(240, 10, 4),
    border=ColorScale(346, 20, 90),
    input=ColorScale(346, 20, 90),
    ring=ColorScale(346, 77, 50),
    radius=0.5,
)

_ROSE_DARK = ThemeTokens(
    background=ColorScale(346, 40, 8),
    foreground=ColorScale(346, 100, 98),
    card=ColorScale(346, 40, 8),
    card_foreground=ColorScale(346, 100, 98),
    popover=ColorScale(346, 40, 8),
    popover_foreground=ColorScale(346, 100, 98),
    primary=ColorScale(346, 77, 55),
    primary_foreground=ColorScale(346, 40, 8),
    secondary=ColorScale(346, 30, 16),
    secondary_foreground=ColorScale(346, 100, 98),
    muted=ColorScale(346, 30, 16),
    muted_foreground=ColorScale(346, 15, 85),  # Increased from 60% to 85% for better contrast
    accent=ColorScale(346, 30, 16),
    accent_foreground=ColorScale(346, 100, 98),
    destructive=ColorScale(0, 62, 30),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 69, 28),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 40),
    warning_foreground=ColorScale(0, 0, 98),
    info=ColorScale(199, 89, 60),
    info_foreground=ColorScale(0, 0, 98),
    link=ColorScale(347, 77, 60),
    link_hover=ColorScale(347, 77, 70),
    code=ColorScale(347, 30, 12),
    code_foreground=ColorScale(240, 5, 80),
    selection=ColorScale(347, 100, 30),
    selection_foreground=ColorScale(0, 0, 98),
    border=ColorScale(346, 30, 16),
    input=ColorScale(346, 30, 16),
    ring=ColorScale(346, 77, 55),
    radius=0.5,
)

ROSE_THEME = ThemePreset(
    name="rose",
    display_name="Rose",
    description="Friendly rose theme for modern, approachable interfaces",
    light=_ROSE_LIGHT,
    dark=_ROSE_DARK,
)


# =============================================================================
# Natural 20 Theme (Dark-first Bloomberg Terminal style)
# =============================================================================

_NATURAL20_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 98),
    foreground=ColorScale(240, 10, 10),
    card=ColorScale(0, 0, 100),
    card_foreground=ColorScale(240, 10, 10),
    popover=ColorScale(0, 0, 100),
    popover_foreground=ColorScale(240, 10, 10),
    primary=ColorScale(211, 100, 65),  # Cyan accent
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(240, 5, 96),
    secondary_foreground=ColorScale(240, 10, 10),
    muted=ColorScale(240, 5, 96),
    muted_foreground=ColorScale(0, 0, 53),
    accent=ColorScale(211, 100, 96),
    accent_foreground=ColorScale(211, 100, 30),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(142, 76, 36),
    success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(38, 92, 50),
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(211, 100, 65),
    info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(211, 100, 55),
    link_hover=ColorScale(211, 100, 45),
    code=ColorScale(240, 5, 96),
    code_foreground=ColorScale(240, 10, 20),
    selection=ColorScale(211, 100, 85),
    selection_foreground=ColorScale(240, 10, 10),
    border=ColorScale(240, 5, 90),
    input=ColorScale(0, 0, 100),
    ring=ColorScale(211, 100, 65),
    radius=0.5,
)

_NATURAL20_DARK = ThemeTokens(
    background=ColorScale(240, 13, 3),  # #08080d - deep near-black
    foreground=ColorScale(0, 0, 100),  # Pure white
    card=ColorScale(240, 15, 6),  # #0d0d12 - card background
    card_foreground=ColorScale(0, 0, 100),
    popover=ColorScale(240, 15, 6),
    popover_foreground=ColorScale(0, 0, 100),
    primary=ColorScale(211, 100, 65),  # #4a9eff - cyan accent
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(240, 10, 10),
    secondary_foreground=ColorScale(0, 0, 88),
    muted=ColorScale(240, 9, 13),  # #1f1f23 - border color
    muted_foreground=ColorScale(0, 0, 53),  # #888 - muted text
    accent=ColorScale(240, 9, 13),
    accent_foreground=ColorScale(211, 100, 65),
    destructive=ColorScale(0, 84, 53),  # Red gradient start
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(160, 84, 39),  # Green (#34d399)
    success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(38, 100, 59),  # Amber/gold (#fbbf24)
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(211, 100, 65),  # Same as primary cyan
    info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(211, 100, 65),
    link_hover=ColorScale(211, 100, 75),
    code=ColorScale(240, 10, 8),  # Slightly lighter than background
    code_foreground=ColorScale(0, 0, 88),
    selection=ColorScale(211, 100, 30),
    selection_foreground=ColorScale(0, 0, 100),
    border=ColorScale(240, 9, 13),  # #1f1f23
    input=ColorScale(240, 15, 6),
    ring=ColorScale(211, 100, 65),
    radius=0.75,  # Slightly more rounded
)

NATURAL20_THEME = ThemePreset(
    name="natural20",
    display_name="Natural 20",
    description="Dark-first Bloomberg Terminal-inspired theme with cyan accents",
    light=_NATURAL20_LIGHT,
    dark=_NATURAL20_DARK,
)


# =============================================================================
# Catppuccin Mocha Theme (Most Popular Pastel Theme)
# =============================================================================

_CATPPUCCIN_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 100),
    foreground=ColorScale(240, 23, 15),
    card=ColorScale(220, 23, 97),
    card_foreground=ColorScale(240, 23, 15),
    popover=ColorScale(220, 23, 97),
    popover_foreground=ColorScale(240, 23, 15),
    primary=ColorScale(217, 92, 76),  # Blue
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(220, 17, 93),
    secondary_foreground=ColorScale(240, 23, 15),
    muted=ColorScale(220, 17, 93),
    muted_foreground=ColorScale(233, 16, 49),
    accent=ColorScale(220, 17, 93),
    accent_foreground=ColorScale(217, 92, 76),
    destructive=ColorScale(343, 81, 75),  # Red
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(115, 54, 76),  # Green
    success_foreground=ColorScale(0, 0, 10),
    warning=ColorScale(35, 77, 49),  # Yellow
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(189, 100, 74),  # Sky
    info_foreground=ColorScale(0, 0, 10),
    link=ColorScale(267, 84, 81),  # Mauve
    link_hover=ColorScale(267, 84, 71),
    code=ColorScale(220, 23, 97),
    code_foreground=ColorScale(240, 23, 15),
    selection=ColorScale(217, 92, 86),
    selection_foreground=ColorScale(240, 23, 15),
    border=ColorScale(220, 17, 93),
    input=ColorScale(0, 0, 100),
    ring=ColorScale(217, 92, 76),
    radius=0.75,
)

_CATPPUCCIN_DARK = ThemeTokens(
    background=ColorScale(240, 21, 15),  # Base #1e1e2e
    foreground=ColorScale(226, 64, 88),  # Text #cdd6f4
    card=ColorScale(240, 21, 19),  # Surface0 #313244
    card_foreground=ColorScale(226, 64, 88),
    popover=ColorScale(240, 21, 19),
    popover_foreground=ColorScale(226, 64, 88),
    primary=ColorScale(217, 92, 76),  # Blue #89b4fa
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(240, 21, 26),  # Surface1
    secondary_foreground=ColorScale(226, 64, 88),
    muted=ColorScale(240, 21, 26),
    muted_foreground=ColorScale(227, 27, 72),  # Overlay0
    accent=ColorScale(240, 21, 26),
    accent_foreground=ColorScale(267, 84, 81),  # Mauve
    destructive=ColorScale(343, 81, 75),  # Red #f38ba8
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(115, 54, 76),  # Green #a6e3a1
    success_foreground=ColorScale(0, 0, 10),
    warning=ColorScale(23, 92, 75),  # Peach #fab387
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(189, 100, 74),  # Sky #89dceb
    info_foreground=ColorScale(0, 0, 10),
    link=ColorScale(267, 84, 81),  # Mauve #cba6f7
    link_hover=ColorScale(267, 84, 71),
    code=ColorScale(240, 21, 12),  # Mantle
    code_foreground=ColorScale(226, 64, 88),
    selection=ColorScale(267, 84, 81),
    selection_foreground=ColorScale(0, 0, 100),
    border=ColorScale(240, 21, 26),
    input=ColorScale(240, 21, 19),
    ring=ColorScale(217, 92, 76),
    radius=0.75,
)

CATPPUCCIN_THEME = ThemePreset(
    name="catppuccin",
    display_name="Catppuccin Mocha",
    description="Soothing pastel theme with warm, muted colors",
    light=_CATPPUCCIN_LIGHT,
    dark=_CATPPUCCIN_DARK,
)


# =============================================================================
# Rosé Pine Theme (Elegant Nature-Inspired Pastels)
# =============================================================================

_ROSE_PINE_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 100),
    foreground=ColorScale(248, 25, 18),
    card=ColorScale(245, 50, 97),
    card_foreground=ColorScale(248, 25, 18),
    popover=ColorScale(245, 50, 97),
    popover_foreground=ColorScale(248, 25, 18),
    primary=ColorScale(343, 76, 68),  # Love (rose)
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(245, 22, 91),
    secondary_foreground=ColorScale(248, 25, 18),
    muted=ColorScale(245, 22, 91),
    muted_foreground=ColorScale(257, 9, 48),
    accent=ColorScale(245, 22, 91),
    accent_foreground=ColorScale(267, 57, 78),  # Iris
    destructive=ColorScale(343, 76, 68),
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(197, 49, 38),  # Pine
    success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(35, 88, 72),  # Gold
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(189, 43, 73),  # Foam
    info_foreground=ColorScale(0, 0, 10),
    link=ColorScale(267, 57, 78),  # Iris
    link_hover=ColorScale(267, 57, 68),
    code=ColorScale(245, 50, 97),
    code_foreground=ColorScale(248, 25, 18),
    selection=ColorScale(343, 76, 88),
    selection_foreground=ColorScale(248, 25, 18),
    border=ColorScale(245, 22, 91),
    input=ColorScale(0, 0, 100),
    ring=ColorScale(343, 76, 68),
    radius=0.5,
)

_ROSE_PINE_DARK = ThemeTokens(
    background=ColorScale(249, 22, 12),  # Base #191724
    foreground=ColorScale(245, 50, 91),  # Text #e0def4
    card=ColorScale(250, 23, 17),  # Surface #1f1d2e
    card_foreground=ColorScale(245, 50, 91),
    popover=ColorScale(250, 23, 17),
    popover_foreground=ColorScale(245, 50, 91),
    primary=ColorScale(343, 76, 68),  # Love #eb6f92
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(247, 23, 20),  # Overlay
    secondary_foreground=ColorScale(245, 50, 91),
    muted=ColorScale(247, 23, 20),
    muted_foreground=ColorScale(249, 15, 56),  # Muted
    accent=ColorScale(247, 23, 20),
    accent_foreground=ColorScale(267, 57, 78),  # Iris
    destructive=ColorScale(343, 76, 68),  # Love
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(197, 49, 38),  # Pine #31748f
    success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(35, 88, 72),  # Gold #f6c177
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(189, 43, 73),  # Foam #9ccfd8
    info_foreground=ColorScale(0, 0, 10),
    link=ColorScale(267, 57, 78),  # Iris #c4a7e7
    link_hover=ColorScale(267, 57, 88),
    code=ColorScale(248, 24, 10),  # Highlight Low
    code_foreground=ColorScale(245, 50, 91),
    selection=ColorScale(267, 57, 78),
    selection_foreground=ColorScale(0, 0, 100),
    border=ColorScale(247, 23, 20),
    input=ColorScale(250, 23, 17),
    ring=ColorScale(343, 76, 68),
    radius=0.5,
)

ROSE_PINE_THEME = ThemePreset(
    name="rose_pine",
    display_name="Rosé Pine",
    description="Elegant, muted pastels inspired by natural pine forests",
    light=_ROSE_PINE_LIGHT,
    dark=_ROSE_PINE_DARK,
)


# =============================================================================
# Tokyo Night Theme (Vibrant Neon Pastels)
# =============================================================================

_TOKYO_NIGHT_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 100),
    foreground=ColorScale(224, 18, 20),
    card=ColorScale(219, 28, 97),
    card_foreground=ColorScale(224, 18, 20),
    popover=ColorScale(219, 28, 97),
    popover_foreground=ColorScale(224, 18, 20),
    primary=ColorScale(217, 89, 72),  # Blue
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(219, 20, 92),
    secondary_foreground=ColorScale(224, 18, 20),
    muted=ColorScale(219, 20, 92),
    muted_foreground=ColorScale(224, 18, 45),
    accent=ColorScale(219, 20, 92),
    accent_foreground=ColorScale(267, 85, 78),  # Magenta
    destructive=ColorScale(355, 89, 72),  # Red
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(89, 59, 64),  # Green
    success_foreground=ColorScale(0, 0, 10),
    warning=ColorScale(41, 70, 65),  # Yellow
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(189, 100, 74),  # Cyan
    info_foreground=ColorScale(0, 0, 10),
    link=ColorScale(267, 85, 78),  # Magenta
    link_hover=ColorScale(267, 85, 68),
    code=ColorScale(219, 28, 97),
    code_foreground=ColorScale(224, 18, 20),
    selection=ColorScale(217, 89, 82),
    selection_foreground=ColorScale(224, 18, 20),
    border=ColorScale(219, 20, 92),
    input=ColorScale(0, 0, 100),
    ring=ColorScale(217, 89, 72),
    radius=0.5,
)

_TOKYO_NIGHT_DARK = ThemeTokens(
    background=ColorScale(234, 16, 13),  # Background #1a1b26
    foreground=ColorScale(219, 72, 85),  # Foreground #c0caf5
    card=ColorScale(233, 15, 18),  # Slightly lighter
    card_foreground=ColorScale(219, 72, 85),
    popover=ColorScale(233, 15, 18),
    popover_foreground=ColorScale(219, 72, 85),
    primary=ColorScale(217, 89, 72),  # Blue #7aa2f7
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(234, 13, 20),
    secondary_foreground=ColorScale(219, 72, 85),
    muted=ColorScale(234, 13, 20),
    muted_foreground=ColorScale(225, 12, 68),
    accent=ColorScale(234, 13, 20),
    accent_foreground=ColorScale(267, 85, 78),  # Magenta
    destructive=ColorScale(355, 89, 72),  # Red #f7768e
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(89, 59, 64),  # Green #9ece6a
    success_foreground=ColorScale(0, 0, 10),
    warning=ColorScale(41, 70, 65),  # Yellow #e0af68
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(189, 100, 74),  # Cyan #7dcfff
    info_foreground=ColorScale(0, 0, 10),
    link=ColorScale(267, 85, 78),  # Magenta #bb9af7
    link_hover=ColorScale(267, 85, 88),
    code=ColorScale(233, 17, 10),
    code_foreground=ColorScale(219, 72, 85),
    selection=ColorScale(267, 85, 78),
    selection_foreground=ColorScale(0, 0, 100),
    border=ColorScale(234, 13, 20),
    input=ColorScale(233, 15, 18),
    ring=ColorScale(217, 89, 72),
    radius=0.5,
)

TOKYO_NIGHT_THEME = ThemePreset(
    name="tokyo_night",
    display_name="Tokyo Night",
    description="Vibrant yet soft neon colors inspired by Tokyo at night",
    light=_TOKYO_NIGHT_LIGHT,
    dark=_TOKYO_NIGHT_DARK,
)


# =============================================================================
# Nord Theme (Arctic-Inspired Cool Pastels)
# =============================================================================

_NORD_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 100),
    foreground=ColorScale(220, 16, 22),
    card=ColorScale(219, 28, 97),
    card_foreground=ColorScale(220, 16, 22),
    popover=ColorScale(219, 28, 97),
    popover_foreground=ColorScale(220, 16, 22),
    primary=ColorScale(193, 43, 67),  # Nord8 frost
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(219, 20, 92),
    secondary_foreground=ColorScale(220, 16, 22),
    muted=ColorScale(219, 20, 92),
    muted_foreground=ColorScale(220, 16, 45),
    accent=ColorScale(219, 20, 92),
    accent_foreground=ColorScale(210, 34, 63),  # Nord9
    destructive=ColorScale(354, 42, 56),  # Nord11 aurora red
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(92, 28, 65),  # Nord14 aurora green
    success_foreground=ColorScale(0, 0, 10),
    warning=ColorScale(40, 71, 73),  # Nord13 aurora yellow
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(210, 34, 63),  # Nord9 frost
    info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(213, 32, 52),  # Nord10 frost
    link_hover=ColorScale(213, 32, 42),
    code=ColorScale(219, 28, 97),
    code_foreground=ColorScale(220, 16, 22),
    selection=ColorScale(193, 43, 77),
    selection_foreground=ColorScale(220, 16, 22),
    border=ColorScale(219, 20, 92),
    input=ColorScale(0, 0, 100),
    ring=ColorScale(193, 43, 67),
    radius=0.5,
)

_NORD_DARK = ThemeTokens(
    background=ColorScale(220, 16, 22),  # Nord0 #2e3440
    foreground=ColorScale(219, 28, 88),  # Nord4 #d8dee9
    card=ColorScale(220, 16, 28),  # Nord1 #3b4252
    card_foreground=ColorScale(219, 28, 88),
    popover=ColorScale(220, 16, 28),
    popover_foreground=ColorScale(219, 28, 88),
    primary=ColorScale(193, 43, 67),  # Nord8 #88c0d0
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(220, 16, 32),  # Nord2
    secondary_foreground=ColorScale(219, 28, 88),
    muted=ColorScale(220, 16, 32),
    muted_foreground=ColorScale(219, 14, 62),
    accent=ColorScale(220, 16, 32),
    accent_foreground=ColorScale(210, 34, 63),  # Nord9
    destructive=ColorScale(354, 42, 56),  # Nord11 #bf616a
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(92, 28, 65),  # Nord14 #a3be8c
    success_foreground=ColorScale(0, 0, 10),
    warning=ColorScale(40, 71, 73),  # Nord13 #ebcb8b
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(210, 34, 63),  # Nord9 #81a1c1
    info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(213, 32, 52),  # Nord10 #5e81ac
    link_hover=ColorScale(213, 32, 62),
    code=ColorScale(220, 17, 18),  # Darker than background
    code_foreground=ColorScale(219, 28, 88),
    selection=ColorScale(210, 34, 63),
    selection_foreground=ColorScale(0, 0, 100),
    border=ColorScale(220, 16, 32),
    input=ColorScale(220, 16, 28),
    ring=ColorScale(193, 43, 67),
    radius=0.5,
)

NORD_THEME = ThemePreset(
    name="nord",
    display_name="Nord",
    description="Cool, arctic-inspired blue/gray pastels",
    light=_NORD_LIGHT,
    dark=_NORD_DARK,
)


# =============================================================================
# Theme Presets Registry
# =============================================================================

THEME_PRESETS: dict[str, ThemePreset] = {
    "default": DEFAULT_THEME,
    "shadcn": SHADCN_THEME,
    "blue": BLUE_THEME,
    "green": GREEN_THEME,
    "purple": PURPLE_THEME,
    "orange": ORANGE_THEME,
    "rose": ROSE_THEME,
    "natural20": NATURAL20_THEME,
    "catppuccin": CATPPUCCIN_THEME,
    "rose_pine": ROSE_PINE_THEME,
    "tokyo_night": TOKYO_NIGHT_THEME,
    "nord": NORD_THEME,
}


def get_preset(name: str) -> ThemePreset:
    """Get a theme preset by name, with fallback to default."""
    return THEME_PRESETS.get(name, DEFAULT_THEME)


def list_presets() -> list[dict]:
    """Return list of available presets with metadata."""
    return [
        {
            "name": preset.name,
            "display_name": preset.display_name,
            "description": preset.description,
        }
        for preset in THEME_PRESETS.values()
    ]
