"""
Theme preset definitions using HSL color tokens.

Based on shadcn/ui theming system with CSS custom properties.
Each preset includes both light and dark mode token sets.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class ColorScale:
    """HSL color representation for CSS custom properties."""

    h: int  # Hue 0-360
    s: int  # Saturation 0-100
    l: int  # Lightness 0-100

    def to_hsl(self) -> str:
        """Return HSL values for CSS variable (without hsl() wrapper)."""
        return f"{self.h} {self.s}% {self.l}%"

    def to_hsl_func(self) -> str:
        """Return complete hsl() function."""
        return f"hsl({self.h}, {self.s}%, {self.l}%)"

    def with_lightness(self, l: int) -> "ColorScale":
        """Return a new ColorScale with modified lightness."""
        return ColorScale(self.h, self.s, l)

    def with_saturation(self, s: int) -> "ColorScale":
        """Return a new ColorScale with modified saturation."""
        return ColorScale(self.h, s, self.l)


@dataclass
class ThemeTokens:
    """
    Complete token set for a theme mode.

    Follows shadcn/ui naming conventions with extensions for
    success and warning states.
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
    muted_foreground=ColorScale(215, 20, 65),
    accent=ColorScale(217, 33, 17),
    accent_foreground=ColorScale(210, 40, 98),
    destructive=ColorScale(0, 62, 30),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 69, 28),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 40),
    warning_foreground=ColorScale(0, 0, 98),
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
    muted_foreground=ColorScale(140, 20, 60),
    accent=ColorScale(140, 30, 16),
    accent_foreground=ColorScale(138, 76, 97),
    destructive=ColorScale(0, 62, 30),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 69, 28),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 40),
    warning_foreground=ColorScale(0, 0, 98),
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
    muted_foreground=ColorScale(270, 20, 60),
    accent=ColorScale(270, 30, 16),
    accent_foreground=ColorScale(270, 80, 98),
    destructive=ColorScale(0, 62, 30),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 69, 28),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 40),
    warning_foreground=ColorScale(0, 0, 98),
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
    muted_foreground=ColorScale(20, 20, 60),
    accent=ColorScale(20, 30, 16),
    accent_foreground=ColorScale(24, 100, 98),
    destructive=ColorScale(0, 62, 30),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 69, 28),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 40),
    warning_foreground=ColorScale(0, 0, 98),
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
    muted_foreground=ColorScale(346, 20, 60),
    accent=ColorScale(346, 30, 16),
    accent_foreground=ColorScale(346, 100, 98),
    destructive=ColorScale(0, 62, 30),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 69, 28),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 40),
    warning_foreground=ColorScale(0, 0, 98),
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
# Cyberpunk Theme (Futuristic Neon)
# =============================================================================

_CYBERPUNK_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 100),
    foreground=ColorScale(270, 95, 10),
    card=ColorScale(0, 0, 100),
    card_foreground=ColorScale(270, 95, 10),
    popover=ColorScale(0, 0, 100),
    popover_foreground=ColorScale(270, 95, 10),
    primary=ColorScale(120, 100, 50),
    primary_foreground=ColorScale(0, 0, 0),
    secondary=ColorScale(300, 100, 25),
    secondary_foreground=ColorScale(0, 0, 100),
    muted=ColorScale(270, 20, 96),
    muted_foreground=ColorScale(270, 15, 45),
    accent=ColorScale(300, 100, 70),
    accent_foreground=ColorScale(0, 0, 0),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(120, 100, 40),
    success_foreground=ColorScale(0, 0, 0),
    warning=ColorScale(60, 100, 50),
    warning_foreground=ColorScale(0, 0, 0),
    border=ColorScale(270, 30, 88),
    input=ColorScale(270, 30, 88),
    ring=ColorScale(120, 100, 50),
    radius=0.5,
)

_CYBERPUNK_DARK = ThemeTokens(
    background=ColorScale(270, 95, 5),
    foreground=ColorScale(120, 100, 80),
    card=ColorScale(270, 95, 8),
    card_foreground=ColorScale(120, 100, 80),
    popover=ColorScale(270, 95, 8),
    popover_foreground=ColorScale(120, 100, 80),
    primary=ColorScale(120, 100, 60),
    primary_foreground=ColorScale(270, 95, 5),
    secondary=ColorScale(300, 100, 15),
    secondary_foreground=ColorScale(120, 100, 80),
    muted=ColorScale(270, 50, 12),
    muted_foreground=ColorScale(270, 30, 60),
    accent=ColorScale(300, 100, 60),
    accent_foreground=ColorScale(270, 95, 5),
    destructive=ColorScale(0, 84, 50),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(120, 100, 50),
    success_foreground=ColorScale(270, 95, 5),
    warning=ColorScale(60, 100, 60),
    warning_foreground=ColorScale(270, 95, 5),
    border=ColorScale(270, 50, 12),
    input=ColorScale(270, 50, 12),
    ring=ColorScale(120, 100, 60),
    radius=0.5,
)

CYBERPUNK_THEME = ThemePreset(
    name="cyberpunk",
    display_name="Cyberpunk",
    description="A futuristic theme with neon greens and purples",
    light=_CYBERPUNK_LIGHT,
    dark=_CYBERPUNK_DARK,
)

# =============================================================================
# Sunset Theme (Warm Colors)  
# =============================================================================

_SUNSET_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 100),
    foreground=ColorScale(15, 80, 15),
    card=ColorScale(0, 0, 100),
    card_foreground=ColorScale(15, 80, 15),
    popover=ColorScale(0, 0, 100),
    popover_foreground=ColorScale(15, 80, 15),
    primary=ColorScale(25, 95, 55),
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(45, 100, 85),
    secondary_foreground=ColorScale(15, 80, 15),
    muted=ColorScale(25, 20, 96),
    muted_foreground=ColorScale(25, 15, 45),
    accent=ColorScale(15, 100, 70),
    accent_foreground=ColorScale(0, 0, 100),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 76, 36),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 50),
    warning_foreground=ColorScale(0, 0, 98),
    border=ColorScale(25, 25, 88),
    input=ColorScale(25, 25, 88),
    ring=ColorScale(25, 95, 55),
    radius=0.5,
)

_SUNSET_DARK = ThemeTokens(
    background=ColorScale(15, 80, 5),
    foreground=ColorScale(45, 100, 85),
    card=ColorScale(15, 80, 8),
    card_foreground=ColorScale(45, 100, 85),
    popover=ColorScale(15, 80, 8),
    popover_foreground=ColorScale(45, 100, 85),
    primary=ColorScale(25, 95, 65),
    primary_foreground=ColorScale(15, 80, 5),
    secondary=ColorScale(15, 50, 16),
    secondary_foreground=ColorScale(45, 100, 85),
    muted=ColorScale(15, 50, 16),
    muted_foreground=ColorScale(25, 30, 60),
    accent=ColorScale(45, 100, 70),
    accent_foreground=ColorScale(15, 80, 5),
    destructive=ColorScale(0, 84, 50),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 76, 40),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 60),
    warning_foreground=ColorScale(15, 80, 5),
    border=ColorScale(15, 50, 16),
    input=ColorScale(15, 50, 16),
    ring=ColorScale(25, 95, 65),
    radius=0.5,
)

SUNSET_THEME = ThemePreset(
    name="sunset",
    display_name="Sunset",
    description="A warm theme with oranges, reds, and yellows",
    light=_SUNSET_LIGHT,
    dark=_SUNSET_DARK,
)

# =============================================================================
# Forest Theme (Nature Green)
# =============================================================================

_FOREST_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 100),
    foreground=ColorScale(130, 60, 15),
    card=ColorScale(0, 0, 100),
    card_foreground=ColorScale(130, 60, 15),
    popover=ColorScale(0, 0, 100),
    popover_foreground=ColorScale(130, 60, 15),
    primary=ColorScale(130, 75, 40),
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(80, 40, 90),
    secondary_foreground=ColorScale(130, 60, 15),
    muted=ColorScale(130, 20, 96),
    muted_foreground=ColorScale(130, 15, 45),
    accent=ColorScale(100, 60, 60),
    accent_foreground=ColorScale(0, 0, 100),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(130, 75, 40),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 50),
    warning_foreground=ColorScale(0, 0, 98),
    border=ColorScale(130, 25, 88),
    input=ColorScale(130, 25, 88),
    ring=ColorScale(130, 75, 40),
    radius=0.5,
)

_FOREST_DARK = ThemeTokens(
    background=ColorScale(130, 60, 8),
    foreground=ColorScale(100, 60, 85),
    card=ColorScale(130, 60, 10),
    card_foreground=ColorScale(100, 60, 85),
    popover=ColorScale(130, 60, 10),
    popover_foreground=ColorScale(100, 60, 85),
    primary=ColorScale(130, 75, 50),
    primary_foreground=ColorScale(130, 60, 8),
    secondary=ColorScale(130, 40, 16),
    secondary_foreground=ColorScale(100, 60, 85),
    muted=ColorScale(130, 40, 16),
    muted_foreground=ColorScale(130, 20, 60),
    accent=ColorScale(100, 60, 70),
    accent_foreground=ColorScale(130, 60, 8),
    destructive=ColorScale(0, 84, 50),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(130, 75, 45),
    success_foreground=ColorScale(130, 60, 8),
    warning=ColorScale(38, 92, 60),
    warning_foreground=ColorScale(130, 60, 8),
    border=ColorScale(130, 40, 16),
    input=ColorScale(130, 40, 16),
    ring=ColorScale(130, 75, 50),
    radius=0.5,
)

FOREST_THEME = ThemePreset(
    name="forest",
    display_name="Forest",
    description="A nature-inspired theme with earth tones and greens",
    light=_FOREST_LIGHT,
    dark=_FOREST_DARK,
)

# =============================================================================
# Ocean Theme (Blue/Teal)
# =============================================================================

_OCEAN_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 100),
    foreground=ColorScale(200, 80, 15),
    card=ColorScale(0, 0, 100),
    card_foreground=ColorScale(200, 80, 15),
    popover=ColorScale(0, 0, 100),
    popover_foreground=ColorScale(200, 80, 15),
    primary=ColorScale(200, 85, 50),
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(180, 60, 85),
    secondary_foreground=ColorScale(200, 80, 15),
    muted=ColorScale(200, 20, 96),
    muted_foreground=ColorScale(200, 15, 45),
    accent=ColorScale(180, 70, 60),
    accent_foreground=ColorScale(0, 0, 100),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 76, 36),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 50),
    warning_foreground=ColorScale(0, 0, 98),
    border=ColorScale(200, 25, 88),
    input=ColorScale(200, 25, 88),
    ring=ColorScale(200, 85, 50),
    radius=0.5,
)

_OCEAN_DARK = ThemeTokens(
    background=ColorScale(200, 80, 8),
    foreground=ColorScale(180, 70, 85),
    card=ColorScale(200, 80, 10),
    card_foreground=ColorScale(180, 70, 85),
    popover=ColorScale(200, 80, 10),
    popover_foreground=ColorScale(180, 70, 85),
    primary=ColorScale(200, 85, 60),
    primary_foreground=ColorScale(200, 80, 8),
    secondary=ColorScale(200, 40, 16),
    secondary_foreground=ColorScale(180, 70, 85),
    muted=ColorScale(200, 40, 16),
    muted_foreground=ColorScale(200, 20, 60),
    accent=ColorScale(180, 70, 70),
    accent_foreground=ColorScale(200, 80, 8),
    destructive=ColorScale(0, 84, 50),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 76, 40),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 60),
    warning_foreground=ColorScale(200, 80, 8),
    border=ColorScale(200, 40, 16),
    input=ColorScale(200, 40, 16),
    ring=ColorScale(200, 85, 60),
    radius=0.5,
)

OCEAN_THEME = ThemePreset(
    name="ocean",
    display_name="Ocean",
    description="A calming theme with blues and teals",
    light=_OCEAN_LIGHT,
    dark=_OCEAN_DARK,
)

# =============================================================================
# Metallic Theme (Silver/Gray)
# =============================================================================

_METALLIC_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 100),
    foreground=ColorScale(220, 15, 20),
    card=ColorScale(0, 0, 100),
    card_foreground=ColorScale(220, 15, 20),
    popover=ColorScale(0, 0, 100),
    popover_foreground=ColorScale(220, 15, 20),
    primary=ColorScale(220, 25, 45),
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(220, 10, 90),
    secondary_foreground=ColorScale(220, 15, 20),
    muted=ColorScale(220, 10, 96),
    muted_foreground=ColorScale(220, 8, 45),
    accent=ColorScale(220, 30, 65),
    accent_foreground=ColorScale(0, 0, 100),
    destructive=ColorScale(0, 84, 60),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 76, 36),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 50),
    warning_foreground=ColorScale(0, 0, 98),
    border=ColorScale(220, 15, 85),
    input=ColorScale(220, 15, 85),
    ring=ColorScale(220, 25, 45),
    radius=0.5,
)

_METALLIC_DARK = ThemeTokens(
    background=ColorScale(220, 15, 8),
    foreground=ColorScale(220, 30, 85),
    card=ColorScale(220, 15, 10),
    card_foreground=ColorScale(220, 30, 85),
    popover=ColorScale(220, 15, 10),
    popover_foreground=ColorScale(220, 30, 85),
    primary=ColorScale(220, 25, 55),
    primary_foreground=ColorScale(220, 15, 8),
    secondary=ColorScale(220, 15, 16),
    secondary_foreground=ColorScale(220, 30, 85),
    muted=ColorScale(220, 15, 16),
    muted_foreground=ColorScale(220, 10, 60),
    accent=ColorScale(220, 30, 70),
    accent_foreground=ColorScale(220, 15, 8),
    destructive=ColorScale(0, 84, 50),
    destructive_foreground=ColorScale(0, 0, 98),
    success=ColorScale(142, 76, 40),
    success_foreground=ColorScale(0, 0, 98),
    warning=ColorScale(38, 92, 60),
    warning_foreground=ColorScale(220, 15, 8),
    border=ColorScale(220, 15, 16),
    input=ColorScale(220, 15, 16),
    ring=ColorScale(220, 25, 55),
    radius=0.5,
)

METALLIC_THEME = ThemePreset(
    name="metallic",
    display_name="Metallic",
    description="A sleek and modern theme with silver tones",
    light=_METALLIC_LIGHT,
    dark=_METALLIC_DARK,
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
    "cyberpunk": CYBERPUNK_THEME,
    "sunset": SUNSET_THEME,
    "forest": FOREST_THEME,
    "ocean": OCEAN_THEME,
    "metallic": METALLIC_THEME,
}


def get_preset(name: str) -> ThemePreset:
    """Get a theme preset by name (regular + high contrast)."""
    # Check regular presets first
    if name in THEME_PRESETS:
        return THEME_PRESETS[name]
    
    # Check high contrast presets
    try:
        from .high_contrast import get_all_high_contrast_presets
        hc_presets = get_all_high_contrast_presets()
        if name in hc_presets:
            return hc_presets[name]
    except ImportError:
        pass
    
    # Fallback to default
    return THEME_PRESETS.get("default", DEFAULT_THEME)


def get_all_presets() -> Dict[str, ThemePreset]:
    """Get all available theme presets (regular + high contrast)."""
    all_presets = THEME_PRESETS.copy()
    
    try:
        from .high_contrast import get_all_high_contrast_presets
        hc_presets = get_all_high_contrast_presets()
        all_presets.update(hc_presets)
    except ImportError:
        pass
        
    return all_presets


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
