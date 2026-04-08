"""
Theme preset definitions using HSL color tokens.

Based on shadcn/ui theming system with CSS custom properties.
Each preset includes both light and dark mode token sets.
"""

from dataclasses import dataclass
from typing import Tuple


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

    def to_hex(self) -> str:
        """Return hex color string, e.g. '#3b82f6'."""
        from .colors import hsl_to_hex

        return hsl_to_hex(self.h, self.s, self.lightness)

    def to_rgb(self) -> Tuple[int, int, int]:
        """Return RGB tuple (0-255 each)."""
        from .colors import hsl_to_rgb

        return hsl_to_rgb(self.h, self.s, self.lightness)

    def to_rgb_func(self) -> str:
        """Return complete rgb() CSS function string, e.g. 'rgb(59, 130, 246)'."""
        r, g, b = self.to_rgb()
        return f"rgb({r}, {g}, {b})"

    @classmethod
    def from_hex(cls, hex_str: str) -> "ColorScale":
        """Create ColorScale from hex string (#RRGGBB or #RGB)."""
        from .colors import hex_to_hsl

        h, s, l = hex_to_hsl(hex_str)
        return cls(h, s, l)

    @classmethod
    def from_rgb(cls, r: int, g: int, b: int) -> "ColorScale":
        """Create ColorScale from RGB values (0-255 each)."""
        from .colors import rgb_to_hsl

        h, s, l = rgb_to_hsl(r, g, b)
        return cls(h, s, l)

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

    # Surface levels for complex dark layouts (e.g., landing pages)
    # surface_1: darkest (ultra-dark background)
    # surface_2: mid-level (panels, navbar)
    # surface_3: elevated (cards, elevated elements)
    surface_1: ColorScale
    surface_2: ColorScale
    surface_3: ColorScale


@dataclass
class SurfaceTreatment:
    """Surface styling treatments for glass panels, gradients, and noise effects."""

    style: str = "glass"  # "glass" | "gradient" | "noise"

    # Glass surface properties
    glass_background: str = "rgba(21, 27, 43, 0.7)"
    glass_border: str = "rgba(255, 255, 255, 0.1)"
    glass_blur: str = "12px"
    surface_radius: str | None = None  # None means use --radius

    # Gradient surface properties
    gradient_direction: str = "180deg"
    gradient_from: str = "#1e293b"
    gradient_to: str = "#0f172a"

    # Noise surface properties
    noise_opacity: float = 0.03



@dataclass
class ThemePreset:
    """A complete theme with light and dark mode tokens."""

    name: str
    display_name: str
    light: ThemeTokens
    dark: ThemeTokens
    description: str = ""
    radius: float = 0.5  # Border radius multiplier (output as --radius: {val}rem)

    # Which mode is the default (emitted in :root)?
    # "light" = :root gets light tokens (standard shadcn behavior)
    # "dark" = :root gets dark tokens (for dark-first themes like djust.org)
    default_mode: str = "light"

    # Extra CSS custom properties beyond the standard shadcn set.
    # Use this for brand-specific variables like --color-brand-rust,
    # --background-image-grid-pattern, --animation-pulse-slow, etc.
    # These are emitted in the base :root block.
    extra_css_vars: dict | None = None

    # Per-mode brand CSS variables for light and dark modes.
    # Use these for brand surface colors that need to differ between modes
    # (e.g., --color-brand-dark: #0B0F19 in dark, #f8fafc in light).
    # If None, extra_css_vars is used for both modes.
    extra_css_vars_light: dict | None = None
    extra_css_vars_dark: dict | None = None

    # Surface treatment for glass panels, gradients, etc.
    surface: SurfaceTreatment | None = None


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
    surface_1=ColorScale(0, 0, 99),
    surface_2=ColorScale(0, 0, 97),
    surface_3=ColorScale(0, 0, 95),
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
    surface_1=ColorScale(240, 4, 8),
    surface_2=ColorScale(240, 4, 12),
    surface_3=ColorScale(240, 4, 16),
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
    surface_1=ColorScale(0, 0, 99),
    surface_2=ColorScale(0, 0, 97),
    surface_3=ColorScale(0, 0, 95),
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
    surface_1=ColorScale(240, 4, 8),
    surface_2=ColorScale(240, 4, 12),
    surface_3=ColorScale(240, 4, 16),
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
    surface_1=ColorScale(0, 0, 99),
    surface_2=ColorScale(0, 0, 97),
    surface_3=ColorScale(0, 0, 95),
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
    surface_1=ColorScale(240, 4, 8),
    surface_2=ColorScale(240, 4, 12),
    surface_3=ColorScale(240, 4, 16),
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
    surface_1=ColorScale(0, 0, 99),
    surface_2=ColorScale(0, 0, 97),
    surface_3=ColorScale(0, 0, 95),
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
    surface_1=ColorScale(240, 4, 8),
    surface_2=ColorScale(240, 4, 12),
    surface_3=ColorScale(240, 4, 16),
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
    surface_1=ColorScale(0, 0, 99),
    surface_2=ColorScale(0, 0, 97),
    surface_3=ColorScale(0, 0, 95),
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
    surface_1=ColorScale(240, 4, 8),
    surface_2=ColorScale(240, 4, 12),
    surface_3=ColorScale(240, 4, 16),
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
    surface_1=ColorScale(0, 0, 99),
    surface_2=ColorScale(0, 0, 97),
    surface_3=ColorScale(0, 0, 95),
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
    surface_1=ColorScale(240, 4, 8),
    surface_2=ColorScale(240, 4, 12),
    surface_3=ColorScale(240, 4, 16),
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
    surface_1=ColorScale(0, 0, 99),
    surface_2=ColorScale(0, 0, 97),
    surface_3=ColorScale(0, 0, 95),
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
    surface_1=ColorScale(240, 4, 8),
    surface_2=ColorScale(240, 4, 12),
    surface_3=ColorScale(240, 4, 16),
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
    surface_1=ColorScale(0, 0, 99),
    surface_2=ColorScale(0, 0, 97),
    surface_3=ColorScale(0, 0, 95),
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
    surface_1=ColorScale(240, 4, 8),
    surface_2=ColorScale(240, 4, 12),
    surface_3=ColorScale(240, 4, 16),
)

NATURAL20_THEME = ThemePreset(
    name="natural20",
    display_name="Natural 20",
    description="Dark-first Bloomberg Terminal-inspired theme with cyan accents",
    light=_NATURAL20_LIGHT,
    dark=_NATURAL20_DARK,
    radius=0.75,
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
    surface_1=ColorScale(0, 0, 99),
    surface_2=ColorScale(0, 0, 97),
    surface_3=ColorScale(0, 0, 95),
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
    # Gentle animations for pastel theme
    surface_1=ColorScale(240, 4, 8),
    surface_2=ColorScale(240, 4, 12),
    surface_3=ColorScale(240, 4, 16),
)

CATPPUCCIN_THEME = ThemePreset(
    name="catppuccin",
    display_name="Catppuccin Mocha",
    description="Soothing pastel theme with warm, muted colors",
    light=_CATPPUCCIN_LIGHT,
    dark=_CATPPUCCIN_DARK,
    radius=0.75,
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
    surface_1=ColorScale(0, 0, 99),
    surface_2=ColorScale(0, 0, 97),
    surface_3=ColorScale(0, 0, 95),
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
    # Gentle animations for pastel theme
    surface_1=ColorScale(240, 4, 8),
    surface_2=ColorScale(240, 4, 12),
    surface_3=ColorScale(240, 4, 16),
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
    surface_1=ColorScale(0, 0, 99),
    surface_2=ColorScale(0, 0, 97),
    surface_3=ColorScale(0, 0, 95),
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
    # Moderate animations for vibrant pastel theme
    surface_1=ColorScale(240, 4, 8),
    surface_2=ColorScale(240, 4, 12),
    surface_3=ColorScale(240, 4, 16),
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
    surface_1=ColorScale(0, 0, 99),
    surface_2=ColorScale(0, 0, 97),
    surface_3=ColorScale(0, 0, 95),
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
    # Gentle animations for pastel theme
    surface_1=ColorScale(240, 4, 8),
    surface_2=ColorScale(240, 4, 12),
    surface_3=ColorScale(240, 4, 16),
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
    surface_1=ColorScale(0, 0, 99),
    surface_2=ColorScale(0, 0, 97),
    surface_3=ColorScale(0, 0, 95),
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
    # Dramatic animations for neon theme
    surface_1=ColorScale(240, 4, 8),
    surface_2=ColorScale(240, 4, 12),
    surface_3=ColorScale(240, 4, 16),
)

SYNTHWAVE_THEME = ThemePreset(
    name="synthwave",
    display_name="Synthwave '84",
    description="Iconic 1980s synthwave with glowing neon pink and cyan",
    light=_SYNTHWAVE_LIGHT,
    dark=_SYNTHWAVE_DARK,
    radius=0.75,
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
    surface_1=ColorScale(0, 0, 99),
    surface_2=ColorScale(0, 0, 97),
    surface_3=ColorScale(0, 0, 95),
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
    # Dramatic animations for neon theme
    surface_1=ColorScale(240, 4, 8),
    surface_2=ColorScale(240, 4, 12),
    surface_3=ColorScale(240, 4, 16),
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
    surface_1=ColorScale(0, 0, 99),
    surface_2=ColorScale(0, 0, 97),
    surface_3=ColorScale(0, 0, 95),
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
    # Dramatic animations for neon theme
    surface_1=ColorScale(240, 4, 8),
    surface_2=ColorScale(240, 4, 12),
    surface_3=ColorScale(240, 4, 16),
)

OUTRUN_THEME = ThemePreset(
    name="outrun",
    display_name="Outrun",
    description="80s retro racing with hot pink, purple, and sunset gradients",
    light=_OUTRUN_LIGHT,
    dark=_OUTRUN_DARK,
    radius=0.75,
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
    surface_1=ColorScale(0, 0, 99),
    surface_2=ColorScale(0, 0, 97),
    surface_3=ColorScale(0, 0, 95),
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
    # Gentle animations for nature theme
    surface_1=ColorScale(240, 4, 8),
    surface_2=ColorScale(240, 4, 12),
    surface_3=ColorScale(240, 4, 16),
)

FOREST_THEME = ThemePreset(
    name="forest",
    display_name="Forest",
    description="Deep emerald greens with warm earth tones",
    light=_FOREST_LIGHT,
    dark=_FOREST_DARK,
    radius=0.75,
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
    surface_1=ColorScale(0, 0, 99),
    surface_2=ColorScale(0, 0, 97),
    surface_3=ColorScale(0, 0, 95),
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
    # Gentle animations for warm theme
    surface_1=ColorScale(240, 4, 8),
    surface_2=ColorScale(240, 4, 12),
    surface_3=ColorScale(240, 4, 16),
)

AMBER_THEME = ThemePreset(
    name="amber",
    display_name="Amber",
    description="Warm amber & gold — like a control room at midnight",
    light=_AMBER_LIGHT,
    dark=_AMBER_DARK,
    radius=0.75,
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
    surface_1=ColorScale(0, 0, 99),
    surface_2=ColorScale(0, 0, 97),
    surface_3=ColorScale(0, 0, 95),
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
    # Subtle animations for focus mode
    surface_1=ColorScale(240, 4, 8),
    surface_2=ColorScale(240, 4, 12),
    surface_3=ColorScale(240, 4, 16),
)

SLATE_THEME = ThemePreset(
    name="slate",
    display_name="Slate",
    description="Minimal monochrome — pure focus, no color noise",
    light=_SLATE_LIGHT,
    dark=_SLATE_DARK,
    radius=0.75,
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
    surface_1=ColorScale(0, 0, 99),
    surface_2=ColorScale(0, 0, 97),
    surface_3=ColorScale(0, 0, 95),
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
    # Moderate animations for space theme
    surface_1=ColorScale(240, 4, 8),
    surface_2=ColorScale(240, 4, 12),
    surface_3=ColorScale(240, 4, 16),
)

NEBULA_THEME = ThemePreset(
    name="nebula",
    display_name="Nebula",
    description="Deep space — dark slate & violet",
    light=_NEBULA_LIGHT,
    dark=_NEBULA_DARK,
    radius=0.75,
)


# =============================================================================
# djust.org Theme (Dark-focused brand theme)
# =============================================================================

_DJUST_LIGHT = ThemeTokens(
    background=ColorScale(220, 10, 98),  # Near white
    foreground=ColorScale(220, 10, 4),    # Near black
    card=ColorScale(220, 10, 100),
    card_foreground=ColorScale(220, 10, 4),
    popover=ColorScale(220, 10, 100),
    popover_foreground=ColorScale(220, 10, 4),
    primary=ColorScale(28, 80, 53),        # djust rust orange
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(154, 48, 39),    # djust django green
    secondary_foreground=ColorScale(0, 0, 100),
    muted=ColorScale(215, 14, 93),        # Light muted gray
    muted_foreground=ColorScale(215, 10, 45),
    accent=ColorScale(157, 46, 39),          # django green (darker for light bg)
    accent_foreground=ColorScale(0, 0, 100),
    destructive=ColorScale(350, 89, 60),
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(160, 84, 39),
    success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(38, 92, 50),
    warning_foreground=ColorScale(0, 0, 100),
    info=ColorScale(199, 89, 48),
    info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(28, 80, 53),
    link_hover=ColorScale(28, 80, 45),
    code=ColorScale(215, 14, 93),
    code_foreground=ColorScale(215, 10, 20),
    selection=ColorScale(28, 80, 53),
    selection_foreground=ColorScale(0, 0, 100),
    border=ColorScale(215, 14, 88),
    input=ColorScale(215, 14, 88),
    ring=ColorScale(28, 80, 53),
    surface_1=ColorScale(220, 10, 98),
    surface_2=ColorScale(220, 10, 95),
    surface_3=ColorScale(220, 10, 92),
)

_DJUST_DARK = ThemeTokens(
    background=ColorScale(223, 39, 7),    # #0B0F19 — djust brand dark
    foreground=ColorScale(214, 32, 91),  # #E2E8F0 — djust brand text
    card=ColorScale(224, 34, 13),         # #151B2B — djust panel
    card_foreground=ColorScale(214, 32, 91),
    popover=ColorScale(224, 34, 13),
    popover_foreground=ColorScale(214, 32, 91),
    primary=ColorScale(28, 80, 55),        # djust rust orange
    primary_foreground=ColorScale(0, 0, 100),  # white text on orange
    secondary=ColorScale(154, 48, 53),   # djust django green
    secondary_foreground=ColorScale(0, 0, 100),
    muted=ColorScale(224, 30, 16),        # djust muted
    muted_foreground=ColorScale(215, 20, 65),
    accent=ColorScale(157, 46, 49),          # django green (#44B78B)
    accent_foreground=ColorScale(0, 0, 100),
    destructive=ColorScale(350, 89, 60),
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(160, 84, 39),
    success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(38, 92, 50),
    warning_foreground=ColorScale(0, 0, 100),
    info=ColorScale(199, 89, 48),
    info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(28, 80, 55),
    link_hover=ColorScale(28, 80, 65),
    code=ColorScale(224, 34, 13),           # matches card/panel
    code_foreground=ColorScale(214, 32, 91),
    selection=ColorScale(28, 80, 55),
    selection_foreground=ColorScale(0, 0, 100),
    border=ColorScale(215, 25, 18),         # #1E293B — brand border
    input=ColorScale(215, 25, 18),
    ring=ColorScale(28, 80, 55),
    surface_1=ColorScale(223, 39, 7),       # #0B0F19 — matches background
    surface_2=ColorScale(224, 34, 13),      # #151B2B — matches panel
    surface_3=ColorScale(215, 25, 18),      # #1E293B — matches border
)

DJUST_THEME = ThemePreset(
    name="djust",
    display_name="djust.org",
    description="djust.org brand — dark with rust orange and Django green accents",
    light=_DJUST_LIGHT,
    dark=_DJUST_DARK,
    default_mode="dark",  # djust.org is dark-first
    radius=0.5,
    extra_css_vars={
        # Brand colors (djust.org specific)
        "color-brand-dark": "#0B0F19",
        "color-brand-panel": "#151B2B",
        "color-brand-rust": "#E57324",
        "color-brand-django": "#44B78B",
        "color-brand-text": "#E2E8F0",
        "color-brand-muted": "#94A3B8",
        "color-brand-border": "#1E293B",
        "color-brand-danger": "#F43F5E",
        "color-brand-success": "#10B981",
        # Background patterns
        "background-image-grid-pattern": "linear-gradient(to right, #1e293b 1px, transparent 1px), linear-gradient(to bottom, #1e293b 1px, transparent 1px)",
        "background-image-gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        # Animations
        "animation-pulse-slow": "pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite",
    },
    extra_css_vars_light={
        # Light-mode brand surfaces (surfaces change, accents stay)
        "color-brand-dark": "#f8fafc",
        "color-brand-panel": "#f1f5f9",
        "color-brand-text": "#0f172a",
        "color-brand-muted": "#64748b",
        "color-brand-border": "#e2e8f0",
    },
    surface=SurfaceTreatment(
        style='glass',
        glass_background='rgba(21, 27, 43, 0.7)',
        glass_border='rgba(255, 255, 255, 0.1)',
        glass_blur='12px',
    ),
)


# =============================================================================
# Theme Presets Registry
# =============================================================================

# =============================================================================
# Dracula Theme
# =============================================================================

# Alucard light mode — official warm cream palette
_DRACULA_LIGHT = ThemeTokens(
    background=ColorScale(45, 100, 96),           # #FFFBEB — Alucard Background
    foreground=ColorScale(0, 0, 12),              # #1F1F1F — Alucard Foreground
    card=ColorScale(45, 60, 93),                  # Warm cream card
    card_foreground=ColorScale(0, 0, 12),
    popover=ColorScale(45, 80, 95),               # Slightly brighter cream
    popover_foreground=ColorScale(0, 0, 12),
    primary=ColorScale(265, 89, 55),              # Darkened Purple for AA on cream
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(45, 30, 90),             # Warm secondary
    secondary_foreground=ColorScale(0, 0, 12),
    muted=ColorScale(45, 30, 88),                 # Warm muted
    muted_foreground=ColorScale(0, 0, 40),
    accent=ColorScale(326, 100, 45),              # Darkened Pink for cream contrast
    accent_foreground=ColorScale(0, 0, 100),
    destructive=ColorScale(0, 100, 50),           # Darkened Red
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(135, 80, 35),              # Darkened Green
    success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(31, 100, 50),              # Darkened Orange
    warning_foreground=ColorScale(0, 0, 100),
    info=ColorScale(191, 97, 40),                 # Darkened Cyan
    info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(326, 100, 40),                # Darkened Pink links
    link_hover=ColorScale(265, 89, 45),           # Purple on hover
    code=ColorScale(45, 40, 90),                  # Warm cream code bg
    code_foreground=ColorScale(265, 89, 40),      # Purple code text
    border=ColorScale(240, 15, 82),               # Soft blue-gray border
    input=ColorScale(240, 15, 85),
    ring=ColorScale(265, 89, 55),                 # Purple focus ring
    selection=ColorScale(240, 20, 84),            # #CFCFDE — Alucard Selection
    selection_foreground=ColorScale(0, 0, 12),
    surface_1=ColorScale(45, 60, 97),             # Lightest warm cream
    surface_2=ColorScale(45, 40, 94),             # Mid warm cream
    surface_3=ColorScale(45, 30, 91),             # Deepest warm cream
)
# Dark mode — pixel-perfect official Dracula spec
_DRACULA_DARK = ThemeTokens(
    background=ColorScale(231, 15, 18),           # #282A36 — Official Background
    foreground=ColorScale(60, 30, 96),            # #F8F8F2 — Official Foreground
    card=ColorScale(232, 15, 15),                 # #21222C — Official "Dark" bg level
    card_foreground=ColorScale(60, 30, 96),
    popover=ColorScale(231, 15, 24),              # #343746 — Official "Light" bg level
    popover_foreground=ColorScale(60, 30, 96),
    primary=ColorScale(265, 89, 78),              # #BD93F9 — Official Purple
    primary_foreground=ColorScale(231, 15, 18),
    secondary=ColorScale(231, 8, 29),             # #424450 — Official "Lighter" bg
    secondary_foreground=ColorScale(60, 30, 96),
    muted=ColorScale(232, 14, 31),                # #44475A — Official Selection
    muted_foreground=ColorScale(225, 27, 51),     # #6272A4 — Official Comment
    accent=ColorScale(326, 100, 74),              # #FF79C6 — Official Pink (signature!)
    accent_foreground=ColorScale(231, 15, 18),
    destructive=ColorScale(0, 100, 67),           # #FF5555 — Official Red
    destructive_foreground=ColorScale(60, 30, 96),
    success=ColorScale(135, 94, 65),              # #50FA7B — Official Green
    success_foreground=ColorScale(0, 0, 10),
    warning=ColorScale(31, 100, 71),              # #FFB86C — Official Orange
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(191, 97, 77),                 # #8BE9FD — Official Cyan
    info_foreground=ColorScale(0, 0, 10),
    link=ColorScale(326, 100, 74),                # #FF79C6 — Pink links (most distinctive)
    link_hover=ColorScale(265, 89, 78),           # Purple on hover (complementary)
    code=ColorScale(230, 15, 11),                 # #191A21 — Official "Darker" bg
    code_foreground=ColorScale(191, 97, 77),      # Cyan for code identifiers
    border=ColorScale(225, 27, 51),               # #6272A4 — Comment color (visible borders)
    input=ColorScale(232, 14, 31),                # #44475A — Selection (subtler inputs)
    ring=ColorScale(265, 89, 78),                 # Purple focus ring
    selection=ColorScale(232, 14, 31),            # #44475A — Official Selection
    selection_foreground=ColorScale(60, 30, 96),  # #F8F8F2
    surface_1=ColorScale(230, 15, 11),            # #191A21 — Official "Darker"
    surface_2=ColorScale(232, 15, 15),            # #21222C — Official "Dark"
    surface_3=ColorScale(231, 15, 24),            # #343746 — Official "Light"
)
DRACULA_THEME = ThemePreset(name="dracula",
    display_name="Dracula",
    description="Pixel-perfect official palette with Alucard light mode",
    light=_DRACULA_LIGHT, dark=_DRACULA_DARK, default_mode="dark")

# =============================================================================
# Gruvbox Theme
# =============================================================================

_GRUVBOX_LIGHT = ThemeTokens(
    background=ColorScale(44, 87, 94), foreground=ColorScale(0, 0, 16),
    card=ColorScale(47, 80, 90), card_foreground=ColorScale(0, 0, 16),
    popover=ColorScale(47, 80, 90), popover_foreground=ColorScale(0, 0, 16),
    primary=ColorScale(27, 99, 55), primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(44, 70, 85), secondary_foreground=ColorScale(0, 0, 16),
    muted=ColorScale(44, 70, 85), muted_foreground=ColorScale(24, 12, 45),
    accent=ColorScale(175, 42, 52), accent_foreground=ColorScale(0, 0, 100),
    destructive=ColorScale(6, 96, 59), destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(106, 33, 51), success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(40, 73, 49), warning_foreground=ColorScale(0, 0, 100),
    info=ColorScale(175, 42, 52), info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(27, 99, 55), link_hover=ColorScale(27, 99, 45),
    code=ColorScale(44, 70, 85), code_foreground=ColorScale(6, 96, 59),
    border=ColorScale(40, 30, 75), input=ColorScale(40, 30, 75),
    ring=ColorScale(27, 99, 55),
    selection=ColorScale(27, 80, 85),
    selection_foreground=ColorScale(27, 10, 15),
    surface_1=ColorScale(27, 5, 96),
    surface_2=ColorScale(27, 5, 93),
    surface_3=ColorScale(27, 5, 90))
_GRUVBOX_DARK = ThemeTokens(
    background=ColorScale(0, 0, 16), foreground=ColorScale(42, 46, 82),
    card=ColorScale(20, 5, 20), card_foreground=ColorScale(42, 46, 82),
    popover=ColorScale(20, 5, 20), popover_foreground=ColorScale(42, 46, 82),
    primary=ColorScale(27, 99, 55), primary_foreground=ColorScale(0, 0, 16),
    secondary=ColorScale(20, 5, 24), secondary_foreground=ColorScale(42, 46, 82),
    muted=ColorScale(20, 5, 24), muted_foreground=ColorScale(30, 12, 55),
    accent=ColorScale(175, 42, 63), accent_foreground=ColorScale(0, 0, 16),
    destructive=ColorScale(6, 96, 59), destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(106, 33, 62), success_foreground=ColorScale(0, 0, 16),
    warning=ColorScale(40, 73, 49), warning_foreground=ColorScale(0, 0, 16),
    info=ColorScale(175, 42, 63), info_foreground=ColorScale(0, 0, 16),
    link=ColorScale(27, 99, 55), link_hover=ColorScale(40, 73, 60),
    code=ColorScale(20, 5, 22), code_foreground=ColorScale(106, 33, 62),
    border=ColorScale(20, 5, 28), input=ColorScale(20, 5, 28),
    ring=ColorScale(27, 99, 55),
    selection=ColorScale(27, 80, 25),
    selection_foreground=ColorScale(27, 10, 90),
    surface_1=ColorScale(27, 5, 6),
    surface_2=ColorScale(27, 5, 10),
    surface_3=ColorScale(27, 5, 14))
GRUVBOX_THEME = ThemePreset(name="gruvbox", display_name="Gruvbox",
    description="Retro-warm earthy palette beloved by vim users",
    light=_GRUVBOX_LIGHT, dark=_GRUVBOX_DARK)

# =============================================================================
# Solarized Theme
# =============================================================================

_SOLARIZED_LIGHT = ThemeTokens(
    background=ColorScale(44, 87, 94), foreground=ColorScale(194, 14, 40),
    card=ColorScale(46, 42, 88), card_foreground=ColorScale(194, 14, 40),
    popover=ColorScale(46, 42, 88), popover_foreground=ColorScale(194, 14, 40),
    primary=ColorScale(205, 82, 33), primary_foreground=ColorScale(44, 87, 94),
    secondary=ColorScale(46, 42, 88), secondary_foreground=ColorScale(194, 14, 40),
    muted=ColorScale(46, 42, 88), muted_foreground=ColorScale(196, 13, 55),
    accent=ColorScale(175, 59, 40), accent_foreground=ColorScale(44, 87, 94),
    destructive=ColorScale(1, 71, 52), destructive_foreground=ColorScale(44, 87, 94),
    success=ColorScale(68, 100, 30), success_foreground=ColorScale(44, 87, 94),
    warning=ColorScale(45, 100, 35), warning_foreground=ColorScale(194, 14, 40),
    info=ColorScale(175, 59, 40), info_foreground=ColorScale(44, 87, 94),
    link=ColorScale(205, 82, 33), link_hover=ColorScale(237, 45, 52),
    code=ColorScale(46, 42, 85), code_foreground=ColorScale(1, 71, 52),
    border=ColorScale(44, 20, 78), input=ColorScale(44, 20, 78),
    ring=ColorScale(205, 82, 33),
    selection=ColorScale(205, 80, 85),
    selection_foreground=ColorScale(205, 10, 15),
    surface_1=ColorScale(205, 5, 96),
    surface_2=ColorScale(205, 5, 93),
    surface_3=ColorScale(205, 5, 90))
_SOLARIZED_DARK = ThemeTokens(
    background=ColorScale(192, 100, 11), foreground=ColorScale(44, 87, 94),
    card=ColorScale(192, 81, 14), card_foreground=ColorScale(44, 87, 94),
    popover=ColorScale(192, 81, 14), popover_foreground=ColorScale(44, 87, 94),
    primary=ColorScale(205, 82, 33), primary_foreground=ColorScale(44, 87, 94),
    secondary=ColorScale(192, 81, 18), secondary_foreground=ColorScale(44, 87, 94),
    muted=ColorScale(192, 81, 18), muted_foreground=ColorScale(180, 9, 63),
    accent=ColorScale(175, 59, 40), accent_foreground=ColorScale(44, 87, 94),
    destructive=ColorScale(1, 71, 52), destructive_foreground=ColorScale(44, 87, 94),
    success=ColorScale(68, 100, 30), success_foreground=ColorScale(44, 87, 94),
    warning=ColorScale(45, 100, 35), warning_foreground=ColorScale(192, 100, 11),
    info=ColorScale(175, 59, 40), info_foreground=ColorScale(44, 87, 94),
    link=ColorScale(205, 82, 33), link_hover=ColorScale(237, 45, 52),
    code=ColorScale(192, 81, 16), code_foreground=ColorScale(68, 100, 30),
    border=ColorScale(192, 81, 20), input=ColorScale(192, 81, 20),
    ring=ColorScale(205, 82, 33),
    selection=ColorScale(205, 80, 25),
    selection_foreground=ColorScale(205, 10, 90),
    surface_1=ColorScale(205, 5, 6),
    surface_2=ColorScale(205, 5, 10),
    surface_3=ColorScale(205, 5, 14))
SOLARIZED_THEME = ThemePreset(name="solarized", display_name="Solarized",
    description="The OG scientifically designed contrast palette",
    light=_SOLARIZED_LIGHT, dark=_SOLARIZED_DARK)

# =============================================================================
# High Contrast Theme (Accessibility)
# =============================================================================

_HIGH_CONTRAST_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 100), foreground=ColorScale(0, 0, 0),
    card=ColorScale(0, 0, 100), card_foreground=ColorScale(0, 0, 0),
    popover=ColorScale(0, 0, 100), popover_foreground=ColorScale(0, 0, 0),
    primary=ColorScale(220, 100, 40), primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(0, 0, 95), secondary_foreground=ColorScale(0, 0, 0),
    muted=ColorScale(0, 0, 95), muted_foreground=ColorScale(0, 0, 30),
    accent=ColorScale(0, 0, 90), accent_foreground=ColorScale(0, 0, 0),
    destructive=ColorScale(0, 100, 40), destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(120, 100, 25), success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(40, 100, 40), warning_foreground=ColorScale(0, 0, 0),
    info=ColorScale(220, 100, 40), info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(220, 100, 35), link_hover=ColorScale(220, 100, 25),
    code=ColorScale(0, 0, 93), code_foreground=ColorScale(0, 100, 40),
    border=ColorScale(0, 0, 0), input=ColorScale(0, 0, 0),
    ring=ColorScale(220, 100, 40),
    selection=ColorScale(220, 80, 85),
    selection_foreground=ColorScale(220, 10, 15),
    surface_1=ColorScale(220, 5, 96),
    surface_2=ColorScale(220, 5, 93),
    surface_3=ColorScale(220, 5, 90))
_HIGH_CONTRAST_DARK = ThemeTokens(
    background=ColorScale(0, 0, 0), foreground=ColorScale(0, 0, 100),
    card=ColorScale(0, 0, 5), card_foreground=ColorScale(0, 0, 100),
    popover=ColorScale(0, 0, 5), popover_foreground=ColorScale(0, 0, 100),
    primary=ColorScale(210, 100, 60), primary_foreground=ColorScale(0, 0, 0),
    secondary=ColorScale(0, 0, 12), secondary_foreground=ColorScale(0, 0, 100),
    muted=ColorScale(0, 0, 12), muted_foreground=ColorScale(0, 0, 70),
    accent=ColorScale(0, 0, 15), accent_foreground=ColorScale(0, 0, 100),
    destructive=ColorScale(0, 100, 55), destructive_foreground=ColorScale(0, 0, 0),
    success=ColorScale(120, 100, 45), success_foreground=ColorScale(0, 0, 0),
    warning=ColorScale(45, 100, 50), warning_foreground=ColorScale(0, 0, 0),
    info=ColorScale(210, 100, 60), info_foreground=ColorScale(0, 0, 0),
    link=ColorScale(210, 100, 65), link_hover=ColorScale(210, 100, 80),
    code=ColorScale(0, 0, 10), code_foreground=ColorScale(120, 100, 50),
    border=ColorScale(0, 0, 100), input=ColorScale(0, 0, 100),
    ring=ColorScale(210, 100, 60),
    selection=ColorScale(210, 80, 25),
    selection_foreground=ColorScale(210, 10, 90),
    surface_1=ColorScale(210, 5, 6),
    surface_2=ColorScale(210, 5, 10),
    surface_3=ColorScale(210, 5, 14))
HIGH_CONTRAST_THEME = ThemePreset(name="high_contrast", display_name="High Contrast",
    description="Accessibility-first with maximum contrast ratios",
    light=_HIGH_CONTRAST_LIGHT, dark=_HIGH_CONTRAST_DARK)

# =============================================================================
# Mono Theme (Pure Grayscale)
# =============================================================================

_MONO_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 100), foreground=ColorScale(0, 0, 10),
    card=ColorScale(0, 0, 98), card_foreground=ColorScale(0, 0, 10),
    popover=ColorScale(0, 0, 98), popover_foreground=ColorScale(0, 0, 10),
    primary=ColorScale(0, 0, 15), primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(0, 0, 93), secondary_foreground=ColorScale(0, 0, 15),
    muted=ColorScale(0, 0, 93), muted_foreground=ColorScale(0, 0, 45),
    accent=ColorScale(0, 0, 90), accent_foreground=ColorScale(0, 0, 10),
    destructive=ColorScale(0, 0, 30), destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(0, 0, 35), success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(0, 0, 40), warning_foreground=ColorScale(0, 0, 100),
    info=ColorScale(0, 0, 35), info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(0, 0, 20), link_hover=ColorScale(0, 0, 10),
    code=ColorScale(0, 0, 94), code_foreground=ColorScale(0, 0, 25),
    border=ColorScale(0, 0, 82), input=ColorScale(0, 0, 82),
    ring=ColorScale(0, 0, 15),
    selection=ColorScale(0, 0, 85),
    selection_foreground=ColorScale(0, 10, 15),
    surface_1=ColorScale(0, 5, 96),
    surface_2=ColorScale(0, 5, 93),
    surface_3=ColorScale(0, 5, 90))
_MONO_DARK = ThemeTokens(
    background=ColorScale(0, 0, 7), foreground=ColorScale(0, 0, 90),
    card=ColorScale(0, 0, 10), card_foreground=ColorScale(0, 0, 90),
    popover=ColorScale(0, 0, 10), popover_foreground=ColorScale(0, 0, 90),
    primary=ColorScale(0, 0, 85), primary_foreground=ColorScale(0, 0, 7),
    secondary=ColorScale(0, 0, 15), secondary_foreground=ColorScale(0, 0, 85),
    muted=ColorScale(0, 0, 15), muted_foreground=ColorScale(0, 0, 55),
    accent=ColorScale(0, 0, 18), accent_foreground=ColorScale(0, 0, 90),
    destructive=ColorScale(0, 0, 70), destructive_foreground=ColorScale(0, 0, 7),
    success=ColorScale(0, 0, 65), success_foreground=ColorScale(0, 0, 7),
    warning=ColorScale(0, 0, 60), warning_foreground=ColorScale(0, 0, 7),
    info=ColorScale(0, 0, 65), info_foreground=ColorScale(0, 0, 7),
    link=ColorScale(0, 0, 80), link_hover=ColorScale(0, 0, 95),
    code=ColorScale(0, 0, 13), code_foreground=ColorScale(0, 0, 70),
    border=ColorScale(0, 0, 20), input=ColorScale(0, 0, 20),
    ring=ColorScale(0, 0, 85),
    selection=ColorScale(0, 0, 25),
    selection_foreground=ColorScale(0, 10, 90),
    surface_1=ColorScale(0, 5, 6),
    surface_2=ColorScale(0, 5, 10),
    surface_3=ColorScale(0, 5, 14))
MONO_THEME = ThemePreset(name="mono", display_name="Mono",
    description="Pure grayscale — zero chroma, maximum discipline",
    light=_MONO_LIGHT, dark=_MONO_DARK)

# =============================================================================
# Ember Theme (Warm Coal)
# =============================================================================

_EMBER_LIGHT = ThemeTokens(
    background=ColorScale(30, 20, 97), foreground=ColorScale(15, 20, 15),
    card=ColorScale(30, 18, 94), card_foreground=ColorScale(15, 20, 15),
    popover=ColorScale(30, 18, 94), popover_foreground=ColorScale(15, 20, 15),
    primary=ColorScale(35, 95, 55), primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(30, 15, 88), secondary_foreground=ColorScale(15, 20, 15),
    muted=ColorScale(30, 15, 88), muted_foreground=ColorScale(15, 10, 45),
    accent=ColorScale(15, 80, 55), accent_foreground=ColorScale(0, 0, 100),
    destructive=ColorScale(0, 72, 51), destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(85, 45, 45), success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(35, 95, 55), warning_foreground=ColorScale(15, 20, 15),
    info=ColorScale(200, 40, 50), info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(15, 80, 50), link_hover=ColorScale(15, 80, 40),
    code=ColorScale(30, 15, 90), code_foreground=ColorScale(15, 80, 45),
    border=ColorScale(30, 12, 80), input=ColorScale(30, 12, 80),
    ring=ColorScale(35, 95, 55),
    selection=ColorScale(35, 80, 85),
    selection_foreground=ColorScale(35, 10, 15),
    surface_1=ColorScale(35, 5, 96),
    surface_2=ColorScale(35, 5, 93),
    surface_3=ColorScale(35, 5, 90))
_EMBER_DARK = ThemeTokens(
    background=ColorScale(15, 15, 10), foreground=ColorScale(35, 30, 88),
    card=ColorScale(15, 12, 14), card_foreground=ColorScale(35, 30, 88),
    popover=ColorScale(15, 12, 14), popover_foreground=ColorScale(35, 30, 88),
    primary=ColorScale(35, 95, 55), primary_foreground=ColorScale(15, 15, 10),
    secondary=ColorScale(15, 12, 18), secondary_foreground=ColorScale(35, 30, 88),
    muted=ColorScale(15, 12, 18), muted_foreground=ColorScale(25, 15, 55),
    accent=ColorScale(15, 80, 55), accent_foreground=ColorScale(15, 15, 10),
    destructive=ColorScale(0, 72, 55), destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(85, 45, 55), success_foreground=ColorScale(15, 15, 10),
    warning=ColorScale(35, 95, 55), warning_foreground=ColorScale(15, 15, 10),
    info=ColorScale(200, 40, 60), info_foreground=ColorScale(15, 15, 10),
    link=ColorScale(35, 95, 55), link_hover=ColorScale(35, 95, 70),
    code=ColorScale(15, 12, 16), code_foreground=ColorScale(35, 95, 65),
    border=ColorScale(15, 12, 22), input=ColorScale(15, 12, 22),
    ring=ColorScale(35, 95, 55),
    selection=ColorScale(35, 80, 25),
    selection_foreground=ColorScale(35, 10, 90),
    surface_1=ColorScale(35, 5, 6),
    surface_2=ColorScale(35, 5, 10),
    surface_3=ColorScale(35, 5, 14))
EMBER_THEME = ThemePreset(name="ember", display_name="Ember",
    description="Warm coal and fireplace — cozy dark theme",
    light=_EMBER_LIGHT, dark=_EMBER_DARK, default_mode="dark")

# =============================================================================
# Aurora Theme (Northern Lights)
# =============================================================================

_AURORA_LIGHT = ThemeTokens(
    background=ColorScale(210, 20, 98), foreground=ColorScale(220, 25, 15),
    card=ColorScale(210, 18, 95), card_foreground=ColorScale(220, 25, 15),
    popover=ColorScale(210, 18, 95), popover_foreground=ColorScale(220, 25, 15),
    primary=ColorScale(160, 84, 39), primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(210, 15, 90), secondary_foreground=ColorScale(220, 25, 15),
    muted=ColorScale(210, 15, 90), muted_foreground=ColorScale(220, 15, 45),
    accent=ColorScale(270, 60, 60), accent_foreground=ColorScale(0, 0, 100),
    destructive=ColorScale(0, 72, 55), destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(160, 84, 39), success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(45, 90, 55), warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(200, 80, 55), info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(160, 84, 39), link_hover=ColorScale(270, 60, 55),
    code=ColorScale(210, 15, 92), code_foreground=ColorScale(160, 84, 35),
    border=ColorScale(210, 15, 82), input=ColorScale(210, 15, 82),
    ring=ColorScale(160, 84, 39),
    selection=ColorScale(160, 80, 85),
    selection_foreground=ColorScale(160, 10, 15),
    surface_1=ColorScale(160, 5, 96),
    surface_2=ColorScale(160, 5, 93),
    surface_3=ColorScale(160, 5, 90))
_AURORA_DARK = ThemeTokens(
    background=ColorScale(230, 25, 10), foreground=ColorScale(180, 20, 90),
    card=ColorScale(230, 22, 14), card_foreground=ColorScale(180, 20, 90),
    popover=ColorScale(230, 22, 14), popover_foreground=ColorScale(180, 20, 90),
    primary=ColorScale(160, 84, 52), primary_foreground=ColorScale(230, 25, 10),
    secondary=ColorScale(230, 22, 18), secondary_foreground=ColorScale(180, 20, 90),
    muted=ColorScale(230, 22, 18), muted_foreground=ColorScale(200, 15, 55),
    accent=ColorScale(270, 60, 65), accent_foreground=ColorScale(0, 0, 100),
    destructive=ColorScale(0, 72, 55), destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(160, 84, 52), success_foreground=ColorScale(230, 25, 10),
    warning=ColorScale(45, 90, 60), warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(200, 80, 60), info_foreground=ColorScale(230, 25, 10),
    link=ColorScale(160, 84, 52), link_hover=ColorScale(270, 60, 70),
    code=ColorScale(230, 22, 16), code_foreground=ColorScale(160, 84, 60),
    border=ColorScale(230, 22, 22), input=ColorScale(230, 22, 22),
    ring=ColorScale(160, 84, 52),
    selection=ColorScale(160, 80, 25),
    selection_foreground=ColorScale(160, 10, 90),
    surface_1=ColorScale(160, 5, 6),
    surface_2=ColorScale(160, 5, 10),
    surface_3=ColorScale(160, 5, 14))
AURORA_THEME = ThemePreset(name="aurora", display_name="Aurora",
    description="Northern lights — shifting green-to-violet feel",
    light=_AURORA_LIGHT, dark=_AURORA_DARK, default_mode="dark")

# =============================================================================
# Ink Theme (Japanese Calligraphy Minimalism)
# =============================================================================

_INK_LIGHT = ThemeTokens(
    background=ColorScale(40, 15, 97), foreground=ColorScale(220, 15, 12),
    card=ColorScale(40, 12, 94), card_foreground=ColorScale(220, 15, 12),
    popover=ColorScale(40, 12, 94), popover_foreground=ColorScale(220, 15, 12),
    primary=ColorScale(4, 80, 52), primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(40, 10, 90), secondary_foreground=ColorScale(220, 15, 12),
    muted=ColorScale(40, 10, 90), muted_foreground=ColorScale(220, 10, 45),
    accent=ColorScale(40, 10, 88), accent_foreground=ColorScale(220, 15, 12),
    destructive=ColorScale(4, 80, 52), destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(150, 30, 40), success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(40, 60, 50), warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(210, 30, 50), info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(4, 80, 48), link_hover=ColorScale(4, 80, 38),
    code=ColorScale(40, 10, 92), code_foreground=ColorScale(220, 15, 20),
    border=ColorScale(220, 8, 82), input=ColorScale(220, 8, 82),
    ring=ColorScale(4, 80, 52),
    selection=ColorScale(4, 80, 85),
    selection_foreground=ColorScale(4, 10, 15),
    surface_1=ColorScale(4, 5, 96),
    surface_2=ColorScale(4, 5, 93),
    surface_3=ColorScale(4, 5, 90))
_INK_DARK = ThemeTokens(
    background=ColorScale(220, 15, 8), foreground=ColorScale(40, 15, 85),
    card=ColorScale(220, 12, 12), card_foreground=ColorScale(40, 15, 85),
    popover=ColorScale(220, 12, 12), popover_foreground=ColorScale(40, 15, 85),
    primary=ColorScale(4, 80, 58), primary_foreground=ColorScale(220, 15, 8),
    secondary=ColorScale(220, 12, 15), secondary_foreground=ColorScale(40, 15, 85),
    muted=ColorScale(220, 12, 15), muted_foreground=ColorScale(40, 10, 55),
    accent=ColorScale(220, 12, 18), accent_foreground=ColorScale(40, 15, 85),
    destructive=ColorScale(4, 80, 58), destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(150, 30, 50), success_foreground=ColorScale(220, 15, 8),
    warning=ColorScale(40, 60, 55), warning_foreground=ColorScale(220, 15, 8),
    info=ColorScale(210, 30, 60), info_foreground=ColorScale(220, 15, 8),
    link=ColorScale(4, 80, 58), link_hover=ColorScale(4, 80, 70),
    code=ColorScale(220, 12, 14), code_foreground=ColorScale(4, 80, 65),
    border=ColorScale(220, 12, 18), input=ColorScale(220, 12, 18),
    ring=ColorScale(4, 80, 58),
    selection=ColorScale(4, 80, 25),
    selection_foreground=ColorScale(4, 10, 90),
    surface_1=ColorScale(4, 5, 6),
    surface_2=ColorScale(4, 5, 10),
    surface_3=ColorScale(4, 5, 14))
INK_THEME = ThemePreset(name="ink", display_name="Ink",
    description="Japanese calligraphy minimalism — sharp edges, single vermillion accent",
    light=_INK_LIGHT, dark=_INK_DARK)

# =============================================================================
# Solarpunk Theme
# =============================================================================

_SOLARPUNK_LIGHT = ThemeTokens(
    background=ColorScale(45, 40, 96), foreground=ColorScale(145, 30, 15),
    card=ColorScale(45, 35, 93), card_foreground=ColorScale(145, 30, 15),
    popover=ColorScale(45, 35, 93), popover_foreground=ColorScale(145, 30, 15),
    primary=ColorScale(145, 63, 42), primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(45, 30, 88), secondary_foreground=ColorScale(145, 30, 15),
    muted=ColorScale(45, 30, 88), muted_foreground=ColorScale(145, 15, 40),
    accent=ColorScale(35, 80, 55), accent_foreground=ColorScale(0, 0, 10),
    destructive=ColorScale(0, 65, 50), destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(145, 63, 42), success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(35, 80, 55), warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(190, 55, 45), info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(145, 63, 38), link_hover=ColorScale(145, 63, 30),
    code=ColorScale(45, 30, 90), code_foreground=ColorScale(145, 63, 35),
    border=ColorScale(45, 20, 78), input=ColorScale(45, 20, 78),
    ring=ColorScale(145, 63, 42),
    selection=ColorScale(145, 63, 85),
    selection_foreground=ColorScale(145, 10, 15),
    surface_1=ColorScale(145, 5, 96),
    surface_2=ColorScale(145, 5, 93),
    surface_3=ColorScale(145, 5, 90))
_SOLARPUNK_DARK = ThemeTokens(
    background=ColorScale(150, 30, 10), foreground=ColorScale(45, 40, 90),
    card=ColorScale(150, 25, 14), card_foreground=ColorScale(45, 40, 90),
    popover=ColorScale(150, 25, 14), popover_foreground=ColorScale(45, 40, 90),
    primary=ColorScale(145, 63, 52), primary_foreground=ColorScale(150, 30, 10),
    secondary=ColorScale(150, 25, 18), secondary_foreground=ColorScale(45, 40, 90),
    muted=ColorScale(150, 25, 18), muted_foreground=ColorScale(120, 15, 55),
    accent=ColorScale(35, 80, 60), accent_foreground=ColorScale(0, 0, 10),
    destructive=ColorScale(0, 65, 55), destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(145, 63, 52), success_foreground=ColorScale(150, 30, 10),
    warning=ColorScale(35, 80, 60), warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(190, 55, 55), info_foreground=ColorScale(150, 30, 10),
    link=ColorScale(145, 63, 52), link_hover=ColorScale(80, 60, 65),
    code=ColorScale(150, 25, 16), code_foreground=ColorScale(80, 60, 60),
    border=ColorScale(150, 25, 22), input=ColorScale(150, 25, 22),
    ring=ColorScale(145, 63, 52),
    selection=ColorScale(145, 63, 25),
    selection_foreground=ColorScale(145, 10, 90),
    surface_1=ColorScale(145, 5, 6),
    surface_2=ColorScale(145, 5, 10),
    surface_3=ColorScale(145, 5, 14))
SOLARPUNK_THEME = ThemePreset(name="solarpunk", display_name="Solarpunk",
    description="Optimistic nature — lush greens and warm amber, organic shapes",
    light=_SOLARPUNK_LIGHT, dark=_SOLARPUNK_DARK)

# =============================================================================
# Bauhaus Theme (Geometric Modernist)
# =============================================================================

_BAUHAUS_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 100), foreground=ColorScale(0, 0, 8),
    card=ColorScale(0, 0, 98), card_foreground=ColorScale(0, 0, 8),
    popover=ColorScale(0, 0, 98), popover_foreground=ColorScale(0, 0, 8),
    primary=ColorScale(4, 86, 58), primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(0, 0, 94), secondary_foreground=ColorScale(0, 0, 8),
    muted=ColorScale(0, 0, 94), muted_foreground=ColorScale(0, 0, 40),
    accent=ColorScale(220, 80, 55), accent_foreground=ColorScale(0, 0, 100),
    destructive=ColorScale(4, 86, 58), destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(120, 50, 40), success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(48, 100, 50), warning_foreground=ColorScale(0, 0, 8),
    info=ColorScale(220, 80, 55), info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(220, 80, 50), link_hover=ColorScale(4, 86, 55),
    code=ColorScale(0, 0, 95), code_foreground=ColorScale(4, 86, 50),
    border=ColorScale(0, 0, 8), input=ColorScale(0, 0, 8),
    ring=ColorScale(4, 86, 58),
    selection=ColorScale(4, 80, 85),
    selection_foreground=ColorScale(4, 10, 15),
    surface_1=ColorScale(4, 5, 96),
    surface_2=ColorScale(4, 5, 93),
    surface_3=ColorScale(4, 5, 90))
_BAUHAUS_DARK = ThemeTokens(
    background=ColorScale(0, 0, 5), foreground=ColorScale(0, 0, 95),
    card=ColorScale(0, 0, 9), card_foreground=ColorScale(0, 0, 95),
    popover=ColorScale(0, 0, 9), popover_foreground=ColorScale(0, 0, 95),
    primary=ColorScale(4, 86, 58), primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(0, 0, 14), secondary_foreground=ColorScale(0, 0, 95),
    muted=ColorScale(0, 0, 14), muted_foreground=ColorScale(0, 0, 55),
    accent=ColorScale(220, 80, 60), accent_foreground=ColorScale(0, 0, 100),
    destructive=ColorScale(4, 86, 58), destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(120, 50, 50), success_foreground=ColorScale(0, 0, 5),
    warning=ColorScale(48, 100, 55), warning_foreground=ColorScale(0, 0, 5),
    info=ColorScale(220, 80, 60), info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(220, 80, 60), link_hover=ColorScale(4, 86, 65),
    code=ColorScale(0, 0, 12), code_foreground=ColorScale(48, 100, 60),
    border=ColorScale(0, 0, 95), input=ColorScale(0, 0, 95),
    ring=ColorScale(4, 86, 58),
    selection=ColorScale(4, 80, 25),
    selection_foreground=ColorScale(4, 10, 90),
    surface_1=ColorScale(4, 5, 6),
    surface_2=ColorScale(4, 5, 10),
    surface_3=ColorScale(4, 5, 14))
BAUHAUS_THEME = ThemePreset(name="bauhaus", display_name="Bauhaus",
    description="Geometric modernist — bold primary colors, sharp edges",
    light=_BAUHAUS_LIGHT, dark=_BAUHAUS_DARK)

# =============================================================================
# Cyberdeck Theme (Terminal Hacker)
# =============================================================================

_CYBERDECK_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 97), foreground=ColorScale(120, 10, 15),
    card=ColorScale(120, 5, 94), card_foreground=ColorScale(120, 10, 15),
    popover=ColorScale(120, 5, 94), popover_foreground=ColorScale(120, 10, 15),
    primary=ColorScale(120, 100, 35), primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(120, 5, 90), secondary_foreground=ColorScale(120, 10, 15),
    muted=ColorScale(120, 5, 90), muted_foreground=ColorScale(120, 5, 45),
    accent=ColorScale(120, 100, 90), accent_foreground=ColorScale(120, 10, 15),
    destructive=ColorScale(0, 80, 55), destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(120, 100, 35), success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(60, 80, 45), warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(180, 80, 40), info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(120, 100, 30), link_hover=ColorScale(120, 100, 22),
    code=ColorScale(120, 5, 92), code_foreground=ColorScale(120, 100, 30),
    border=ColorScale(120, 10, 80), input=ColorScale(120, 10, 80),
    ring=ColorScale(120, 100, 35),
    selection=ColorScale(120, 80, 85),
    selection_foreground=ColorScale(120, 10, 15),
    surface_1=ColorScale(120, 5, 96),
    surface_2=ColorScale(120, 5, 93),
    surface_3=ColorScale(120, 5, 90))
_CYBERDECK_DARK = ThemeTokens(
    background=ColorScale(0, 0, 2), foreground=ColorScale(120, 100, 50),
    card=ColorScale(120, 10, 5), card_foreground=ColorScale(120, 100, 50),
    popover=ColorScale(120, 10, 5), popover_foreground=ColorScale(120, 100, 50),
    primary=ColorScale(120, 100, 50), primary_foreground=ColorScale(0, 0, 2),
    secondary=ColorScale(120, 10, 8), secondary_foreground=ColorScale(120, 100, 50),
    muted=ColorScale(120, 10, 8), muted_foreground=ColorScale(120, 50, 35),
    accent=ColorScale(120, 100, 12), accent_foreground=ColorScale(120, 100, 50),
    destructive=ColorScale(0, 100, 50), destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(120, 100, 50), success_foreground=ColorScale(0, 0, 2),
    warning=ColorScale(60, 100, 50), warning_foreground=ColorScale(0, 0, 2),
    info=ColorScale(180, 100, 45), info_foreground=ColorScale(0, 0, 2),
    link=ColorScale(120, 100, 50), link_hover=ColorScale(120, 100, 65),
    code=ColorScale(120, 10, 7), code_foreground=ColorScale(120, 100, 55),
    border=ColorScale(120, 100, 18), input=ColorScale(120, 100, 18),
    ring=ColorScale(120, 100, 50),
    selection=ColorScale(120, 80, 25),
    selection_foreground=ColorScale(120, 10, 90),
    surface_1=ColorScale(120, 5, 6),
    surface_2=ColorScale(120, 5, 10),
    surface_3=ColorScale(120, 5, 14))
CYBERDECK_THEME = ThemePreset(name="cyberdeck", display_name="Cyberdeck",
    description="Terminal hacker — matrix green on true black, CRT vibes",
    light=_CYBERDECK_LIGHT, dark=_CYBERDECK_DARK, default_mode="dark")

# =============================================================================
# Paper Theme (Reading-Optimized Warm)
# =============================================================================

_PAPER_LIGHT = ThemeTokens(
    background=ColorScale(40, 33, 96), foreground=ColorScale(25, 15, 20),
    card=ColorScale(40, 28, 93), card_foreground=ColorScale(25, 15, 20),
    popover=ColorScale(40, 28, 93), popover_foreground=ColorScale(25, 15, 20),
    primary=ColorScale(30, 40, 45), primary_foreground=ColorScale(40, 33, 96),
    secondary=ColorScale(40, 22, 88), secondary_foreground=ColorScale(25, 15, 20),
    muted=ColorScale(40, 22, 88), muted_foreground=ColorScale(25, 10, 45),
    accent=ColorScale(40, 22, 85), accent_foreground=ColorScale(25, 15, 20),
    destructive=ColorScale(0, 55, 50), destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(100, 35, 42), success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(35, 65, 50), warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(210, 35, 50), info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(210, 45, 45), link_hover=ColorScale(210, 45, 35),
    code=ColorScale(40, 22, 90), code_foreground=ColorScale(25, 15, 30),
    border=ColorScale(35, 15, 80), input=ColorScale(35, 15, 80),
    ring=ColorScale(30, 40, 45),
    selection=ColorScale(30, 40, 85),
    selection_foreground=ColorScale(30, 10, 15),
    surface_1=ColorScale(30, 5, 96),
    surface_2=ColorScale(30, 5, 93),
    surface_3=ColorScale(30, 5, 90))
_PAPER_DARK = ThemeTokens(
    background=ColorScale(25, 12, 14), foreground=ColorScale(40, 25, 85),
    card=ColorScale(25, 10, 18), card_foreground=ColorScale(40, 25, 85),
    popover=ColorScale(25, 10, 18), popover_foreground=ColorScale(40, 25, 85),
    primary=ColorScale(30, 40, 60), primary_foreground=ColorScale(25, 12, 14),
    secondary=ColorScale(25, 10, 22), secondary_foreground=ColorScale(40, 25, 85),
    muted=ColorScale(25, 10, 22), muted_foreground=ColorScale(30, 10, 55),
    accent=ColorScale(25, 10, 25), accent_foreground=ColorScale(40, 25, 85),
    destructive=ColorScale(0, 55, 55), destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(100, 35, 52), success_foreground=ColorScale(25, 12, 14),
    warning=ColorScale(35, 65, 55), warning_foreground=ColorScale(25, 12, 14),
    info=ColorScale(210, 35, 60), info_foreground=ColorScale(25, 12, 14),
    link=ColorScale(210, 45, 60), link_hover=ColorScale(210, 45, 72),
    code=ColorScale(25, 10, 20), code_foreground=ColorScale(30, 40, 65),
    border=ColorScale(25, 10, 25), input=ColorScale(25, 10, 25),
    ring=ColorScale(30, 40, 60),
    selection=ColorScale(30, 40, 25),
    selection_foreground=ColorScale(30, 10, 90),
    surface_1=ColorScale(30, 5, 6),
    surface_2=ColorScale(30, 5, 10),
    surface_3=ColorScale(30, 5, 14))
PAPER_THEME = ThemePreset(name="paper", display_name="Paper",
    description="Reading-optimized warm — like sunlit paper, large radius",
    light=_PAPER_LIGHT, dark=_PAPER_DARK)

# =============================================================================
# Neon Noir Theme (Film Noir + Neon)
# =============================================================================

_NEON_NOIR_LIGHT = ThemeTokens(
    background=ColorScale(0, 0, 98), foreground=ColorScale(300, 10, 15),
    card=ColorScale(300, 5, 95), card_foreground=ColorScale(300, 10, 15),
    popover=ColorScale(300, 5, 95), popover_foreground=ColorScale(300, 10, 15),
    primary=ColorScale(330, 100, 60), primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(300, 5, 90), secondary_foreground=ColorScale(300, 10, 15),
    muted=ColorScale(300, 5, 90), muted_foreground=ColorScale(300, 5, 45),
    accent=ColorScale(300, 5, 88), accent_foreground=ColorScale(300, 10, 15),
    destructive=ColorScale(0, 85, 55), destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(160, 60, 45), success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(45, 85, 55), warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(210, 70, 55), info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(330, 100, 55), link_hover=ColorScale(330, 100, 45),
    code=ColorScale(300, 5, 92), code_foreground=ColorScale(330, 100, 50),
    border=ColorScale(300, 5, 82), input=ColorScale(300, 5, 82),
    ring=ColorScale(330, 100, 60),
    selection=ColorScale(330, 80, 85),
    selection_foreground=ColorScale(330, 10, 15),
    surface_1=ColorScale(330, 5, 96),
    surface_2=ColorScale(330, 5, 93),
    surface_3=ColorScale(330, 5, 90))
_NEON_NOIR_DARK = ThemeTokens(
    background=ColorScale(0, 0, 3), foreground=ColorScale(0, 0, 85),
    card=ColorScale(300, 5, 6), card_foreground=ColorScale(0, 0, 85),
    popover=ColorScale(300, 5, 6), popover_foreground=ColorScale(0, 0, 85),
    primary=ColorScale(330, 100, 60), primary_foreground=ColorScale(0, 0, 3),
    secondary=ColorScale(300, 5, 10), secondary_foreground=ColorScale(0, 0, 85),
    muted=ColorScale(300, 5, 10), muted_foreground=ColorScale(0, 0, 45),
    accent=ColorScale(300, 5, 12), accent_foreground=ColorScale(0, 0, 85),
    destructive=ColorScale(0, 85, 55), destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(160, 60, 50), success_foreground=ColorScale(0, 0, 3),
    warning=ColorScale(45, 85, 55), warning_foreground=ColorScale(0, 0, 3),
    info=ColorScale(210, 70, 60), info_foreground=ColorScale(0, 0, 3),
    link=ColorScale(330, 100, 60), link_hover=ColorScale(330, 100, 75),
    code=ColorScale(300, 5, 8), code_foreground=ColorScale(330, 100, 65),
    border=ColorScale(300, 5, 12), input=ColorScale(300, 5, 12),
    ring=ColorScale(330, 100, 60),
    selection=ColorScale(330, 80, 25),
    selection_foreground=ColorScale(330, 10, 90),
    surface_1=ColorScale(330, 5, 6),
    surface_2=ColorScale(330, 5, 10),
    surface_3=ColorScale(330, 5, 14))
NEON_NOIR_THEME = ThemePreset(name="neon_noir", display_name="Neon Noir",
    description="Film noir meets neon — piercing hot pink on true black",
    light=_NEON_NOIR_LIGHT, dark=_NEON_NOIR_DARK, default_mode="dark")

# =============================================================================
# Ocean Theme (Deep Sea)
# =============================================================================

_OCEAN_LIGHT = ThemeTokens(
    background=ColorScale(200, 25, 97), foreground=ColorScale(210, 40, 15),
    card=ColorScale(200, 22, 94), card_foreground=ColorScale(210, 40, 15),
    popover=ColorScale(200, 22, 94), popover_foreground=ColorScale(210, 40, 15),
    primary=ColorScale(200, 80, 45), primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(200, 18, 88), secondary_foreground=ColorScale(210, 40, 15),
    muted=ColorScale(200, 18, 88), muted_foreground=ColorScale(210, 20, 45),
    accent=ColorScale(180, 50, 45), accent_foreground=ColorScale(0, 0, 100),
    destructive=ColorScale(0, 70, 55), destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(160, 60, 42), success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(40, 80, 55), warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(200, 80, 45), info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(200, 80, 40), link_hover=ColorScale(200, 80, 32),
    code=ColorScale(200, 18, 91), code_foreground=ColorScale(200, 80, 35),
    border=ColorScale(200, 15, 80), input=ColorScale(200, 15, 80),
    ring=ColorScale(200, 80, 45),
    selection=ColorScale(200, 80, 85),
    selection_foreground=ColorScale(200, 10, 15),
    surface_1=ColorScale(200, 5, 96),
    surface_2=ColorScale(200, 5, 93),
    surface_3=ColorScale(200, 5, 90))
_OCEAN_DARK = ThemeTokens(
    background=ColorScale(210, 60, 8), foreground=ColorScale(195, 30, 88),
    card=ColorScale(210, 50, 12), card_foreground=ColorScale(195, 30, 88),
    popover=ColorScale(210, 50, 12), popover_foreground=ColorScale(195, 30, 88),
    primary=ColorScale(200, 80, 55), primary_foreground=ColorScale(210, 60, 8),
    secondary=ColorScale(210, 50, 16), secondary_foreground=ColorScale(195, 30, 88),
    muted=ColorScale(210, 50, 16), muted_foreground=ColorScale(200, 20, 55),
    accent=ColorScale(180, 50, 50), accent_foreground=ColorScale(210, 60, 8),
    destructive=ColorScale(0, 70, 55), destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(160, 60, 50), success_foreground=ColorScale(210, 60, 8),
    warning=ColorScale(40, 80, 60), warning_foreground=ColorScale(210, 60, 8),
    info=ColorScale(200, 80, 55), info_foreground=ColorScale(210, 60, 8),
    link=ColorScale(200, 80, 55), link_hover=ColorScale(180, 50, 65),
    code=ColorScale(210, 50, 14), code_foreground=ColorScale(180, 50, 60),
    border=ColorScale(210, 50, 20), input=ColorScale(210, 50, 20),
    ring=ColorScale(200, 80, 55),
    selection=ColorScale(200, 80, 25),
    selection_foreground=ColorScale(200, 10, 90),
    surface_1=ColorScale(200, 5, 6),
    surface_2=ColorScale(200, 5, 10),
    surface_3=ColorScale(200, 5, 14))
OCEAN_THEME = ThemePreset(name="ocean", display_name="Ocean",
    description="Deep sea gradient depth — coastal sky to ocean floor",
    light=_OCEAN_LIGHT, dark=_OCEAN_DARK, default_mode="dark")


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
    "djust": DJUST_THEME,
    "dracula": DRACULA_THEME,
    "gruvbox": GRUVBOX_THEME,
    "solarized": SOLARIZED_THEME,
    "high_contrast": HIGH_CONTRAST_THEME,
    "mono": MONO_THEME,
    "ember": EMBER_THEME,
    "aurora": AURORA_THEME,
    "ink": INK_THEME,
    "solarpunk": SOLARPUNK_THEME,
    "bauhaus": BAUHAUS_THEME,
    "cyberdeck": CYBERDECK_THEME,
    "paper": PAPER_THEME,
    "neon_noir": NEON_NOIR_THEME,
    "ocean_deep": OCEAN_THEME,
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
