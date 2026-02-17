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
    muted_foreground=ColorScale(240, 4, 46),
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
    muted_foreground=ColorScale(240, 5, 65),
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
    muted_foreground=ColorScale(240, 4, 46),
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
    muted_foreground=ColorScale(240, 5, 65),
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
    muted_foreground=ColorScale(215, 16, 47),
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
    muted_foreground=ColorScale(140, 15, 45),
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
    muted_foreground=ColorScale(270, 15, 45),
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
    muted_foreground=ColorScale(20, 15, 45),
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
    muted_foreground=ColorScale(346, 15, 45),
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
