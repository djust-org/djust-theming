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

    # Animation properties
    card_lift_distance: float = 1.0  # pixels - how much cards lift on hover
    card_glow_opacity: float = 0.3  # 0-1 - strength of border glow effect
    transition_speed: int = 150  # milliseconds - base transition duration
    animation_intensity: str = "subtle"  # subtle, moderate, dramatic


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
    # Gentle animations for pastel theme
    card_lift_distance=1.0,
    card_glow_opacity=0.2,
    transition_speed=150,
    animation_intensity="subtle",
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
    # Gentle animations for pastel theme
    card_lift_distance=1.0,
    card_glow_opacity=0.2,
    transition_speed=150,
    animation_intensity="subtle",
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
    # Moderate animations for vibrant pastel theme
    card_lift_distance=2.0,
    card_glow_opacity=0.35,
    transition_speed=175,
    animation_intensity="moderate",
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
    # Gentle animations for pastel theme
    card_lift_distance=1.0,
    card_glow_opacity=0.2,
    transition_speed=150,
    animation_intensity="subtle",
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

# =============================================================================
# Synthwave '84 Theme (Most Iconic Neon Theme)
# =============================================================================

_SYNTHWAVE_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 98),
    foreground=ColorScale(255, 26, 25),
    card=ColorScale(255, 26, 95),
    card_foreground=ColorScale(255, 26, 25),
    popover=ColorScale(255, 26, 95),
    popover_foreground=ColorScale(255, 26, 25),
    primary=ColorScale(320, 100, 74),  # Hot pink
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(255, 26, 88),
    secondary_foreground=ColorScale(255, 26, 25),
    muted=ColorScale(255, 26, 88),
    muted_foreground=ColorScale(255, 26, 45),
    accent=ColorScale(154, 83, 70),  # Electric cyan
    accent_foreground=ColorScale(0, 0, 10),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(154, 83, 70),  # Cyan
    success_foreground=ColorScale(0, 0, 10),
    warning=ColorScale(45, 100, 70),  # Sunset orange
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(267, 41, 69),  # Neon purple
    info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(320, 100, 74),  # Hot pink
    link_hover=ColorScale(320, 100, 64),
    code=ColorScale(255, 26, 95),
    code_foreground=ColorScale(255, 26, 25),
    selection=ColorScale(320, 100, 84),
    selection_foreground=ColorScale(255, 26, 25),
    border=ColorScale(255, 26, 88),
    input=ColorScale(0, 0, 100),
    ring=ColorScale(320, 100, 74),
    radius=0.75,
)

_SYNTHWAVE_DARK = ThemeTokens(
    background=ColorScale(255, 26, 17),  # #262335 dark purple-gray
    foreground=ColorScale(320, 100, 95),  # Light pink-white
    card=ColorScale(255, 26, 22),  # Slightly lighter
    card_foreground=ColorScale(320, 100, 95),
    popover=ColorScale(255, 26, 22),
    popover_foreground=ColorScale(320, 100, 95),
    primary=ColorScale(320, 100, 74),  # #ff7edb hot pink
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(255, 26, 30),
    secondary_foreground=ColorScale(320, 100, 95),
    muted=ColorScale(255, 26, 30),
    muted_foreground=ColorScale(267, 41, 69),  # Neon purple
    accent=ColorScale(154, 83, 70),  # #72f1b8 electric cyan
    accent_foreground=ColorScale(0, 0, 10),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(154, 83, 70),  # Electric cyan
    success_foreground=ColorScale(0, 0, 10),
    warning=ColorScale(45, 100, 70),  # #ffd866 sunset orange
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(267, 41, 69),  # #b893ce neon purple
    info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(320, 100, 74),  # Hot pink
    link_hover=ColorScale(320, 100, 84),
    code=ColorScale(255, 26, 14),
    code_foreground=ColorScale(320, 100, 95),
    selection=ColorScale(320, 100, 74),
    selection_foreground=ColorScale(0, 0, 100),
    border=ColorScale(255, 26, 30),
    input=ColorScale(255, 26, 22),
    ring=ColorScale(320, 100, 74),
    radius=0.75,
    # Dramatic animations for neon theme
    card_lift_distance=3.0,
    card_glow_opacity=0.5,
    transition_speed=200,
    animation_intensity="dramatic",
)

SYNTHWAVE_THEME = ThemePreset(
    name="synthwave",
    display_name="Synthwave '84",
    description="Iconic 1980s synthwave with glowing neon pink and cyan",
    light=_SYNTHWAVE_LIGHT,
    dark=_SYNTHWAVE_DARK,
)


# =============================================================================
# Cyberpunk Theme (Dystopian Future Neon)
# =============================================================================

_CYBERPUNK_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 98),
    foreground=ColorScale(219, 100, 15),
    card=ColorScale(219, 50, 95),
    card_foreground=ColorScale(219, 100, 15),
    popover=ColorScale(219, 50, 95),
    popover_foreground=ColorScale(219, 100, 15),
    primary=ColorScale(54, 70, 68),  # Neon yellow
    primary_foreground=ColorScale(0, 0, 10),
    secondary=ColorScale(219, 50, 88),
    secondary_foreground=ColorScale(219, 100, 15),
    muted=ColorScale(219, 50, 88),
    muted_foreground=ColorScale(219, 50, 45),
    accent=ColorScale(330, 100, 50),  # Hot magenta
    accent_foreground=ColorScale(0, 0, 100),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(135, 94, 65),  # Neon green
    success_foreground=ColorScale(0, 0, 10),
    warning=ColorScale(54, 70, 68),  # Neon yellow
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(180, 100, 50),  # Electric cyan
    info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(330, 100, 50),  # Hot magenta
    link_hover=ColorScale(330, 100, 40),
    code=ColorScale(219, 50, 95),
    code_foreground=ColorScale(219, 100, 15),
    selection=ColorScale(54, 70, 78),
    selection_foreground=ColorScale(0, 0, 10),
    border=ColorScale(219, 50, 88),
    input=ColorScale(0, 0, 100),
    ring=ColorScale(54, 70, 68),
    radius=0.5,
)

_CYBERPUNK_DARK = ThemeTokens(
    background=ColorScale(219, 100, 6),  # #000b1e near black with blue tint
    foreground=ColorScale(54, 70, 95),  # Light yellow-white
    card=ColorScale(219, 100, 10),  # Slightly lighter
    card_foreground=ColorScale(54, 70, 95),
    popover=ColorScale(219, 100, 10),
    popover_foreground=ColorScale(54, 70, 95),
    primary=ColorScale(54, 70, 68),  # #e6db74 neon yellow
    primary_foreground=ColorScale(0, 0, 10),
    secondary=ColorScale(219, 100, 15),
    secondary_foreground=ColorScale(54, 70, 95),
    muted=ColorScale(219, 100, 15),
    muted_foreground=ColorScale(180, 100, 70),  # Cyan
    accent=ColorScale(330, 100, 50),  # #ff0080 hot magenta
    accent_foreground=ColorScale(0, 0, 100),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(135, 94, 65),  # #50fa7b neon green
    success_foreground=ColorScale(0, 0, 10),
    warning=ColorScale(54, 70, 68),  # Neon yellow
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(180, 100, 50),  # #00ffff electric cyan
    info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(330, 100, 50),  # Hot magenta
    link_hover=ColorScale(330, 100, 60),
    code=ColorScale(219, 100, 8),
    code_foreground=ColorScale(54, 70, 95),
    selection=ColorScale(330, 100, 50),
    selection_foreground=ColorScale(0, 0, 100),
    border=ColorScale(219, 100, 15),
    input=ColorScale(219, 100, 10),
    ring=ColorScale(54, 70, 68),
    radius=0.5,
    # Dramatic animations for neon theme
    card_lift_distance=3.0,
    card_glow_opacity=0.5,
    transition_speed=200,
    animation_intensity="dramatic",
)

CYBERPUNK_THEME = ThemePreset(
    name="cyberpunk",
    display_name="Cyberpunk",
    description="Dystopian future with neon yellow, magenta, and cyan",
    light=_CYBERPUNK_LIGHT,
    dark=_CYBERPUNK_DARK,
)


# =============================================================================
# Outrun Theme (80s Retro Racing Aesthetic)
# =============================================================================

_OUTRUN_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 98),
    foreground=ColorScale(240, 100, 15),
    card=ColorScale(240, 50, 95),
    card_foreground=ColorScale(240, 100, 15),
    popover=ColorScale(240, 50, 95),
    popover_foreground=ColorScale(240, 100, 15),
    primary=ColorScale(329, 100, 71),  # Hot pink
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(240, 50, 88),
    secondary_foreground=ColorScale(240, 100, 15),
    muted=ColorScale(240, 50, 88),
    muted_foreground=ColorScale(240, 50, 45),
    accent=ColorScale(285, 61, 66),  # Neon purple
    accent_foreground=ColorScale(0, 0, 100),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(187, 47, 55),  # Electric cyan
    success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(48, 100, 50),  # Sunset orange
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(187, 47, 55),  # Electric cyan
    info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(329, 100, 71),  # Hot pink
    link_hover=ColorScale(329, 100, 61),
    code=ColorScale(240, 50, 95),
    code_foreground=ColorScale(240, 100, 15),
    selection=ColorScale(329, 100, 81),
    selection_foreground=ColorScale(240, 100, 15),
    border=ColorScale(240, 50, 88),
    input=ColorScale(0, 0, 100),
    ring=ColorScale(329, 100, 71),
    radius=0.75,
)

_OUTRUN_DARK = ThemeTokens(
    background=ColorScale(240, 100, 8),  # #00002a deep blue-black
    foreground=ColorScale(329, 100, 95),  # Light pink-white
    card=ColorScale(240, 100, 12),  # Slightly lighter
    card_foreground=ColorScale(329, 100, 95),
    popover=ColorScale(240, 100, 12),
    popover_foreground=ColorScale(329, 100, 95),
    primary=ColorScale(329, 100, 71),  # #ff6ac1 hot pink
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(240, 100, 18),
    secondary_foreground=ColorScale(329, 100, 95),
    muted=ColorScale(240, 100, 18),
    muted_foreground=ColorScale(285, 61, 66),  # Neon purple
    accent=ColorScale(285, 61, 66),  # #c574dd neon purple
    accent_foreground=ColorScale(0, 0, 100),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(187, 47, 55),  # #56b6c2 electric cyan
    success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(48, 100, 50),  # #ffcc00 sunset orange
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(187, 47, 55),  # Electric cyan
    info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(329, 100, 71),  # Hot pink
    link_hover=ColorScale(329, 100, 81),
    code=ColorScale(240, 100, 6),
    code_foreground=ColorScale(329, 100, 95),
    selection=ColorScale(329, 100, 71),
    selection_foreground=ColorScale(0, 0, 100),
    border=ColorScale(240, 100, 18),
    input=ColorScale(240, 100, 12),
    ring=ColorScale(329, 100, 71),
    radius=0.75,
    # Dramatic animations for neon theme
    card_lift_distance=3.0,
    card_glow_opacity=0.5,
    transition_speed=200,
    animation_intensity="dramatic",
)

OUTRUN_THEME = ThemePreset(
    name="outrun",
    display_name="Outrun",
    description="80s retro racing with hot pink, purple, and sunset gradients",
    light=_OUTRUN_LIGHT,
    dark=_OUTRUN_DARK,
)


# =============================================================================
# Forest Theme (Emerald Green Earth Tones)
# =============================================================================

_FOREST_LIGHT = ThemeTokens(
    background=ColorScale(150, 30, 98),  # Very light mint
    foreground=ColorScale(150, 80, 15),  # Deep forest green
    card=ColorScale(150, 25, 95),
    card_foreground=ColorScale(150, 80, 15),
    popover=ColorScale(150, 25, 95),
    popover_foreground=ColorScale(150, 80, 15),
    primary=ColorScale(142, 71, 45),  # #22c55e emerald
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(150, 20, 90),
    secondary_foreground=ColorScale(150, 80, 20),
    muted=ColorScale(150, 20, 92),
    muted_foreground=ColorScale(150, 30, 40),
    accent=ColorScale(150, 25, 90),
    accent_foreground=ColorScale(150, 80, 20),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(142, 71, 45),
    success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(38, 92, 50),
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(158, 64, 52),  # Teal
    info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(142, 71, 40),
    link_hover=ColorScale(142, 71, 30),
    code=ColorScale(150, 30, 94),
    code_foreground=ColorScale(150, 80, 15),
    selection=ColorScale(142, 71, 45),
    selection_foreground=ColorScale(0, 0, 100),
    border=ColorScale(150, 20, 85),
    input=ColorScale(0, 0, 100),
    ring=ColorScale(142, 71, 45),
    radius=0.75,
)

_FOREST_DARK = ThemeTokens(
    background=ColorScale(150, 51, 8),  # #0a1f14 deep forest
    foreground=ColorScale(150, 50, 95),  # Light mint
    card=ColorScale(150, 48, 12),  # Slightly lighter
    card_foreground=ColorScale(150, 50, 95),
    popover=ColorScale(150, 48, 12),
    popover_foreground=ColorScale(150, 50, 95),
    primary=ColorScale(142, 71, 45),  # #22c55e emerald
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(150, 45, 18),
    secondary_foreground=ColorScale(150, 50, 95),
    muted=ColorScale(150, 45, 18),
    muted_foreground=ColorScale(150, 40, 65),
    accent=ColorScale(150, 45, 18),
    accent_foreground=ColorScale(142, 65, 75),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(142, 71, 45),  # Emerald
    success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(38, 92, 50),  # Amber
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(158, 64, 52),  # Teal
    info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(142, 71, 50),
    link_hover=ColorScale(142, 71, 60),
    code=ColorScale(150, 48, 10),
    code_foreground=ColorScale(150, 50, 95),
    selection=ColorScale(142, 71, 45),
    selection_foreground=ColorScale(0, 0, 100),
    border=ColorScale(150, 45, 18),
    input=ColorScale(150, 48, 12),
    ring=ColorScale(142, 71, 45),
    radius=0.75,
    # Gentle animations for nature theme
    card_lift_distance=1.0,
    card_glow_opacity=0.2,
    transition_speed=150,
    animation_intensity="subtle",
)

FOREST_THEME = ThemePreset(
    name="forest",
    display_name="Forest",
    description="Deep emerald greens with warm earth tones",
    light=_FOREST_LIGHT,
    dark=_FOREST_DARK,
)


# =============================================================================
# Amber Theme (Control Room Gold)
# =============================================================================

_AMBER_LIGHT = ThemeTokens(
    background=ColorScale(38, 40, 98),  # Very light cream
    foreground=ColorScale(34, 100, 15),  # Deep brown
    card=ColorScale(38, 35, 94),
    card_foreground=ColorScale(34, 100, 15),
    popover=ColorScale(38, 35, 94),
    popover_foreground=ColorScale(34, 100, 15),
    primary=ColorScale(38, 92, 50),  # #f59e0b amber
    primary_foreground=ColorScale(0, 0, 10),
    secondary=ColorScale(38, 30, 88),
    secondary_foreground=ColorScale(34, 100, 20),
    muted=ColorScale(38, 30, 90),
    muted_foreground=ColorScale(34, 50, 40),
    accent=ColorScale(38, 30, 88),
    accent_foreground=ColorScale(34, 100, 20),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(142, 71, 45),
    success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(45, 100, 60),  # Brighter yellow
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(38, 92, 50),
    info_foreground=ColorScale(0, 0, 10),
    link=ColorScale(38, 92, 45),
    link_hover=ColorScale(38, 92, 35),
    code=ColorScale(38, 35, 92),
    code_foreground=ColorScale(34, 100, 15),
    selection=ColorScale(38, 92, 50),
    selection_foreground=ColorScale(0, 0, 10),
    border=ColorScale(38, 30, 82),
    input=ColorScale(0, 0, 100),
    ring=ColorScale(38, 92, 50),
    radius=0.75,
)

_AMBER_DARK = ThemeTokens(
    background=ColorScale(34, 100, 5),  # #1c1000 deep brown-black
    foreground=ColorScale(45, 100, 95),  # Light golden
    card=ColorScale(36, 100, 8),  # Slightly lighter
    card_foreground=ColorScale(45, 100, 95),
    popover=ColorScale(36, 100, 8),
    popover_foreground=ColorScale(45, 100, 95),
    primary=ColorScale(38, 92, 50),  # #f59e0b amber
    primary_foreground=ColorScale(0, 0, 10),
    secondary=ColorScale(34, 100, 10),
    secondary_foreground=ColorScale(45, 100, 95),
    muted=ColorScale(34, 100, 10),
    muted_foreground=ColorScale(45, 80, 65),
    accent=ColorScale(34, 100, 10),
    accent_foreground=ColorScale(45, 100, 75),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(142, 71, 45),
    success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(45, 100, 60),  # Bright yellow
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(38, 92, 50),
    info_foreground=ColorScale(0, 0, 10),
    link=ColorScale(38, 92, 50),
    link_hover=ColorScale(38, 92, 60),
    code=ColorScale(34, 100, 6),
    code_foreground=ColorScale(45, 100, 95),
    selection=ColorScale(38, 92, 50),
    selection_foreground=ColorScale(0, 0, 10),
    border=ColorScale(34, 100, 10),
    input=ColorScale(36, 100, 8),
    ring=ColorScale(38, 92, 50),
    radius=0.75,
    # Gentle animations for warm theme
    card_lift_distance=1.0,
    card_glow_opacity=0.25,
    transition_speed=150,
    animation_intensity="subtle",
)

AMBER_THEME = ThemePreset(
    name="amber",
    display_name="Amber",
    description="Warm amber & gold — like a control room at midnight",
    light=_AMBER_LIGHT,
    dark=_AMBER_DARK,
)


# =============================================================================
# Slate Theme (Pure Monochrome)
# =============================================================================

_SLATE_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 100),  # Pure white
    foreground=ColorScale(215, 25, 10),  # Deep slate
    card=ColorScale(0, 0, 98),
    card_foreground=ColorScale(215, 25, 10),
    popover=ColorScale(0, 0, 98),
    popover_foreground=ColorScale(215, 25, 10),
    primary=ColorScale(214, 16, 46),  # #64748b slate
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(0, 0, 94),
    secondary_foreground=ColorScale(215, 25, 15),
    muted=ColorScale(0, 0, 94),
    muted_foreground=ColorScale(215, 15, 45),
    accent=ColorScale(0, 0, 94),
    accent_foreground=ColorScale(215, 25, 15),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(142, 71, 45),
    success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(38, 92, 50),
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(214, 16, 46),
    info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(214, 16, 40),
    link_hover=ColorScale(214, 16, 30),
    code=ColorScale(0, 0, 96),
    code_foreground=ColorScale(215, 25, 10),
    selection=ColorScale(214, 16, 46),
    selection_foreground=ColorScale(0, 0, 100),
    border=ColorScale(0, 0, 88),
    input=ColorScale(0, 0, 100),
    ring=ColorScale(214, 16, 46),
    radius=0.75,
)

_SLATE_DARK = ThemeTokens(
    background=ColorScale(240, 20, 5),  # #0a0a0f near black
    foreground=ColorScale(0, 0, 92),  # Light gray
    card=ColorScale(240, 18, 8),  # Slightly lighter
    card_foreground=ColorScale(0, 0, 92),
    popover=ColorScale(240, 18, 8),
    popover_foreground=ColorScale(0, 0, 92),
    primary=ColorScale(214, 16, 66),  # #94a3b8 slate
    primary_foreground=ColorScale(0, 0, 10),
    secondary=ColorScale(240, 15, 12),
    secondary_foreground=ColorScale(0, 0, 92),
    muted=ColorScale(240, 15, 12),
    muted_foreground=ColorScale(0, 0, 55),
    accent=ColorScale(240, 15, 12),
    accent_foreground=ColorScale(214, 16, 80),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(142, 71, 45),
    success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(38, 92, 50),
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(214, 16, 66),
    info_foreground=ColorScale(0, 0, 10),
    link=ColorScale(214, 16, 66),
    link_hover=ColorScale(214, 16, 76),
    code=ColorScale(240, 18, 6),
    code_foreground=ColorScale(0, 0, 92),
    selection=ColorScale(214, 16, 66),
    selection_foreground=ColorScale(0, 0, 10),
    border=ColorScale(240, 15, 12),
    input=ColorScale(240, 18, 8),
    ring=ColorScale(214, 16, 66),
    radius=0.75,
    # Subtle animations for focus mode
    card_lift_distance=1.0,
    card_glow_opacity=0.15,
    transition_speed=150,
    animation_intensity="subtle",
)

SLATE_THEME = ThemePreset(
    name="slate",
    display_name="Slate",
    description="Minimal monochrome — pure focus, no color noise",
    light=_SLATE_LIGHT,
    dark=_SLATE_DARK,
)


# =============================================================================
# Nebula Theme (Deep Space Violet)
# =============================================================================

_NEBULA_LIGHT = ThemeTokens(
    background=ColorScale(239, 50, 98),  # Very light lavender
    foreground=ColorScale(218, 47, 15),  # Deep navy
    card=ColorScale(239, 45, 95),
    card_foreground=ColorScale(218, 47, 15),
    popover=ColorScale(239, 45, 95),
    popover_foreground=ColorScale(218, 47, 15),
    primary=ColorScale(239, 84, 67),  # #6366f1 indigo
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(239, 40, 90),
    secondary_foreground=ColorScale(218, 47, 20),
    muted=ColorScale(239, 40, 92),
    muted_foreground=ColorScale(218, 30, 45),
    accent=ColorScale(239, 40, 90),
    accent_foreground=ColorScale(218, 47, 20),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(142, 71, 45),
    success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(38, 92, 50),
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(239, 84, 67),
    info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(239, 84, 62),
    link_hover=ColorScale(239, 84, 52),
    code=ColorScale(239, 45, 93),
    code_foreground=ColorScale(218, 47, 15),
    selection=ColorScale(239, 84, 67),
    selection_foreground=ColorScale(0, 0, 100),
    border=ColorScale(239, 40, 85),
    input=ColorScale(0, 0, 100),
    ring=ColorScale(239, 84, 67),
    radius=0.75,
)

_NEBULA_DARK = ThemeTokens(
    background=ColorScale(218, 47, 11),  # #0f172a deep slate-blue
    foreground=ColorScale(239, 50, 95),  # Light violet
    card=ColorScale(220, 45, 15),  # Slightly lighter
    card_foreground=ColorScale(239, 50, 95),
    popover=ColorScale(220, 45, 15),
    popover_foreground=ColorScale(239, 50, 95),
    primary=ColorScale(239, 84, 67),  # #6366f1 indigo
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(218, 45, 18),
    secondary_foreground=ColorScale(239, 50, 95),
    muted=ColorScale(218, 45, 18),
    muted_foreground=ColorScale(239, 30, 70),
    accent=ColorScale(218, 45, 18),
    accent_foreground=ColorScale(239, 84, 80),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(142, 71, 45),
    success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(38, 92, 50),
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(239, 84, 67),
    info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(239, 84, 67),
    link_hover=ColorScale(239, 84, 77),
    code=ColorScale(218, 45, 9),
    code_foreground=ColorScale(239, 50, 95),
    selection=ColorScale(239, 84, 67),
    selection_foreground=ColorScale(0, 0, 100),
    border=ColorScale(218, 45, 18),
    input=ColorScale(220, 45, 15),
    ring=ColorScale(239, 84, 67),
    radius=0.75,
    # Moderate animations for space theme
    card_lift_distance=2.0,
    card_glow_opacity=0.3,
    transition_speed=175,
    animation_intensity="moderate",
)

NEBULA_THEME = ThemePreset(
    name="nebula",
    display_name="Nebula",
    description="Deep space — dark slate & violet",
    light=_NEBULA_LIGHT,
    dark=_NEBULA_DARK,
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
    "synthwave": SYNTHWAVE_THEME,
    "cyberpunk": CYBERPUNK_THEME,
    "outrun": OUTRUN_THEME,
    "forest": FOREST_THEME,
    "amber": AMBER_THEME,
    "slate": SLATE_THEME,
    "nebula": NEBULA_THEME,
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
