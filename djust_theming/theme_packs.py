"""
Theme Packs - Complete design systems bundling all styling dimensions.

A ThemePack combines:
- Design theme (typography, spacing, shadows)
- Color preset
- Icon style
- Animation style
- Pattern/texture style
- Interaction style
- Illustration style
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class IconStyle:
    """Icon styling configuration."""
    name: str
    style: str  # "outlined", "filled", "rounded", "sharp", "duotone"
    weight: str  # "thin", "regular", "bold"
    size_scale: float = 1.0  # Multiplier for icon sizes

    # CSS properties
    stroke_width: str = "2"
    corner_rounding: str = "0"  # For rounded style


@dataclass
class AnimationStyle:
    """Animation and motion configuration."""
    name: str

    # Entrance/Exit
    entrance_effect: str = "fade"  # "fade", "slide", "scale", "bounce", "none"
    exit_effect: str = "fade"

    # Hover behaviors
    hover_effect: str = "lift"  # "lift", "scale", "glow", "none"
    hover_scale: float = 1.02
    hover_translate_y: str = "-2px"

    # Click feedback
    click_effect: str = "ripple"  # "ripple", "pulse", "bounce", "none"

    # Loading states
    loading_style: str = "spinner"  # "spinner", "skeleton", "progress", "pulse"

    # Transition characteristics
    transition_style: str = "smooth"  # "smooth", "snappy", "bouncy", "instant"
    duration_fast: str = "0.15s"
    duration_normal: str = "0.3s"
    duration_slow: str = "0.5s"
    easing: str = "cubic-bezier(0.4, 0, 0.2, 1)"


@dataclass
class PatternStyle:
    """Background patterns and textures."""
    name: str

    # Pattern types
    background_pattern: str = "none"  # "dots", "grid", "noise", "gradient", "geometric", "none"
    pattern_opacity: float = 0.05
    pattern_scale: str = "1rem"

    # Surface treatment
    surface_style: str = "flat"  # "flat", "glass", "neumorphic", "elevated"

    # Blur/frosting for glassmorphism
    backdrop_blur: str = "0px"

    # Noise for texture
    noise_intensity: float = 0.0


@dataclass
class InteractionStyle:
    """User interaction feedback."""
    name: str

    # Hover effects
    button_hover: str = "lift"  # "lift", "scale", "glow", "darken", "none"
    link_hover: str = "underline"  # "underline", "color", "background", "none"
    card_hover: str = "lift"  # "lift", "scale", "border", "shadow", "none"

    # Click effects
    button_click: str = "scale"  # "scale", "ripple", "pulse", "none"

    # Focus effects
    focus_style: str = "ring"  # "ring", "outline", "glow", "underline"
    focus_ring_width: str = "2px"
    focus_ring_offset: str = "2px"

    # Cursor
    cursor_style: str = "pointer"  # "pointer", "default", "custom"


@dataclass
class IllustrationStyle:
    """Illustration and imagery treatment."""
    name: str

    # Illustration style
    illustration_type: str = "flat"  # "flat", "isometric", "3d", "line-art", "hand-drawn", "abstract"

    # Image treatment
    image_border_radius: str = "0.5rem"
    image_filter: str = "none"  # "none", "grayscale", "sepia", "vibrant", "duotone"

    # Aspect ratios preference
    preferred_aspect: str = "16:9"  # "1:1", "16:9", "4:3", "3:4"


@dataclass
class ThemePack:
    """
    Complete design system combining all styling dimensions.

    A ThemePack provides a cohesive design experience by bundling:
    - Core design (typography, spacing, shadows)
    - Color palette
    - Icon styling
    - Animation behavior
    - Background patterns
    - Interaction feedback
    - Illustration style
    """
    name: str
    display_name: str
    description: str
    category: str  # "professional", "playful", "minimal", "bold", "elegant", "retro"

    # Core components
    design_theme: str  # Reference to Theme name (e.g., "material", "elegant")
    color_preset: str  # Reference to ColorPreset name (e.g., "blue", "purple")

    # Style dimensions
    icon_style: IconStyle
    animation_style: AnimationStyle
    pattern_style: PatternStyle
    interaction_style: InteractionStyle
    illustration_style: IllustrationStyle


# ============================================
# Icon Style Presets
# ============================================

ICON_OUTLINED = IconStyle(
    name="outlined",
    style="outlined",
    weight="regular",
    stroke_width="2",
    corner_rounding="0",
)

ICON_FILLED = IconStyle(
    name="filled",
    style="filled",
    weight="regular",
    stroke_width="0",
    corner_rounding="0",
)

ICON_ROUNDED = IconStyle(
    name="rounded",
    style="rounded",
    weight="regular",
    stroke_width="2",
    corner_rounding="4px",
)

ICON_SHARP = IconStyle(
    name="sharp",
    style="sharp",
    weight="bold",
    stroke_width="2.5",
    corner_rounding="0",
)

ICON_THIN = IconStyle(
    name="thin",
    style="outlined",
    weight="thin",
    stroke_width="1",
    corner_rounding="0",
)


# ============================================
# Animation Style Presets
# ============================================

ANIM_SMOOTH = AnimationStyle(
    name="smooth",
    entrance_effect="fade",
    exit_effect="fade",
    hover_effect="lift",
    hover_scale=1.02,
    hover_translate_y="-2px",
    click_effect="ripple",
    loading_style="spinner",
    transition_style="smooth",
    duration_fast="0.15s",
    duration_normal="0.3s",
    duration_slow="0.5s",
    easing="cubic-bezier(0.4, 0, 0.2, 1)",
)

ANIM_SNAPPY = AnimationStyle(
    name="snappy",
    entrance_effect="scale",
    exit_effect="scale",
    hover_effect="scale",
    hover_scale=1.05,
    hover_translate_y="0px",
    click_effect="pulse",
    loading_style="progress",
    transition_style="snappy",
    duration_fast="0.08s",
    duration_normal="0.12s",
    duration_slow="0.2s",
    easing="cubic-bezier(0.68, -0.55, 0.265, 1.55)",
)

ANIM_BOUNCY = AnimationStyle(
    name="bouncy",
    entrance_effect="bounce",
    exit_effect="scale",
    hover_effect="scale",
    hover_scale=1.1,
    hover_translate_y="0px",
    click_effect="bounce",
    loading_style="pulse",
    transition_style="bouncy",
    duration_fast="0.2s",
    duration_normal="0.4s",
    duration_slow="0.6s",
    easing="cubic-bezier(0.34, 1.56, 0.64, 1)",
)

ANIM_INSTANT = AnimationStyle(
    name="instant",
    entrance_effect="none",
    exit_effect="none",
    hover_effect="none",
    hover_scale=1.0,
    hover_translate_y="0px",
    click_effect="none",
    loading_style="spinner",
    transition_style="instant",
    duration_fast="0.05s",
    duration_normal="0.1s",
    duration_slow="0.15s",
    easing="linear",
)

ANIM_GENTLE = AnimationStyle(
    name="gentle",
    entrance_effect="fade",
    exit_effect="fade",
    hover_effect="glow",
    hover_scale=1.0,
    hover_translate_y="0px",
    click_effect="none",
    loading_style="skeleton",
    transition_style="smooth",
    duration_fast="0.3s",
    duration_normal="0.5s",
    duration_slow="0.8s",
    easing="cubic-bezier(0.25, 0.46, 0.45, 0.94)",
)


# ============================================
# Pattern Style Presets
# ============================================

PATTERN_MINIMAL = PatternStyle(
    name="minimal",
    background_pattern="none",
    pattern_opacity=0.0,
    pattern_scale="1rem",
    surface_style="flat",
    backdrop_blur="0px",
    noise_intensity=0.0,
)

PATTERN_DOTS = PatternStyle(
    name="dots",
    background_pattern="dots",
    pattern_opacity=0.05,
    pattern_scale="1.5rem",
    surface_style="flat",
    backdrop_blur="0px",
    noise_intensity=0.0,
)

PATTERN_GRID = PatternStyle(
    name="grid",
    background_pattern="grid",
    pattern_opacity=0.03,
    pattern_scale="2rem",
    surface_style="flat",
    backdrop_blur="0px",
    noise_intensity=0.0,
)

PATTERN_NOISE = PatternStyle(
    name="noise",
    background_pattern="noise",
    pattern_opacity=0.02,
    pattern_scale="1rem",
    surface_style="flat",
    backdrop_blur="0px",
    noise_intensity=0.15,
)

PATTERN_GLASS = PatternStyle(
    name="glass",
    background_pattern="none",
    pattern_opacity=0.0,
    pattern_scale="1rem",
    surface_style="glass",
    backdrop_blur="12px",
    noise_intensity=0.0,
)

PATTERN_GRADIENT = PatternStyle(
    name="gradient",
    background_pattern="gradient",
    pattern_opacity=0.1,
    pattern_scale="100%",
    surface_style="flat",
    backdrop_blur="0px",
    noise_intensity=0.0,
)


# ============================================
# Interaction Style Presets
# ============================================

INTERACT_SUBTLE = InteractionStyle(
    name="subtle",
    button_hover="lift",
    link_hover="underline",
    card_hover="shadow",
    button_click="scale",
    focus_style="ring",
    focus_ring_width="2px",
    focus_ring_offset="2px",
    cursor_style="pointer",
)

INTERACT_BOLD = InteractionStyle(
    name="bold",
    button_hover="scale",
    link_hover="background",
    card_hover="lift",
    button_click="pulse",
    focus_style="outline",
    focus_ring_width="3px",
    focus_ring_offset="0px",
    cursor_style="pointer",
)

INTERACT_MINIMAL = InteractionStyle(
    name="minimal",
    button_hover="darken",
    link_hover="color",
    card_hover="border",
    button_click="none",
    focus_style="underline",
    focus_ring_width="1px",
    focus_ring_offset="0px",
    cursor_style="default",
)

INTERACT_PLAYFUL = InteractionStyle(
    name="playful",
    button_hover="glow",
    link_hover="background",
    card_hover="lift",
    button_click="ripple",
    focus_style="glow",
    focus_ring_width="3px",
    focus_ring_offset="3px",
    cursor_style="pointer",
)


# ============================================
# Illustration Style Presets
# ============================================

ILLUST_FLAT = IllustrationStyle(
    name="flat",
    illustration_type="flat",
    image_border_radius="0.5rem",
    image_filter="none",
    preferred_aspect="16:9",
)

ILLUST_3D = IllustrationStyle(
    name="3d",
    illustration_type="3d",
    image_border_radius="1rem",
    image_filter="vibrant",
    preferred_aspect="1:1",
)

ILLUST_LINE = IllustrationStyle(
    name="line-art",
    illustration_type="line-art",
    image_border_radius="0.25rem",
    image_filter="none",
    preferred_aspect="4:3",
)

ILLUST_HAND_DRAWN = IllustrationStyle(
    name="hand-drawn",
    illustration_type="hand-drawn",
    image_border_radius="1.5rem",
    image_filter="none",
    preferred_aspect="16:9",
)

ILLUST_RETRO = IllustrationStyle(
    name="retro",
    illustration_type="flat",
    image_border_radius="0px",
    image_filter="none",
    preferred_aspect="4:3",
)


# ============================================
# Complete Theme Packs
# ============================================

PACK_CORPORATE = ThemePack(
    name="corporate",
    display_name="Corporate Professional",
    description="Clean, professional design for business applications",
    category="professional",
    design_theme="corporate",
    color_preset="blue",
    icon_style=ICON_OUTLINED,
    animation_style=ANIM_SMOOTH,
    pattern_style=PATTERN_GRID,
    interaction_style=INTERACT_SUBTLE,
    illustration_style=ILLUST_LINE,
)

PACK_PLAYFUL = ThemePack(
    name="playful",
    display_name="Playful Startup",
    description="Fun, energetic design with personality",
    category="playful",
    design_theme="playful",
    color_preset="purple",
    icon_style=ICON_ROUNDED,
    animation_style=ANIM_BOUNCY,
    pattern_style=PATTERN_DOTS,
    interaction_style=INTERACT_PLAYFUL,
    illustration_style=ILLUST_3D,
)

PACK_RETRO = ThemePack(
    name="retro",
    display_name="Retro Nostalgia",
    description="Classic 90s web aesthetic with pixel-perfect design",
    category="retro",
    design_theme="retro",
    color_preset="default",
    icon_style=ICON_SHARP,
    animation_style=ANIM_INSTANT,
    pattern_style=PATTERN_NOISE,
    interaction_style=INTERACT_MINIMAL,
    illustration_style=ILLUST_RETRO,
)

PACK_ELEGANT = ThemePack(
    name="elegant",
    display_name="Elegant Luxury",
    description="Sophisticated, premium design with refined details",
    category="elegant",
    design_theme="elegant",
    color_preset="default",
    icon_style=ICON_THIN,
    animation_style=ANIM_GENTLE,
    pattern_style=PATTERN_GRADIENT,
    interaction_style=INTERACT_SUBTLE,
    illustration_style=ILLUST_HAND_DRAWN,
)

PACK_BRUTALIST = ThemePack(
    name="brutalist",
    display_name="Neo-Brutalist Edge",
    description="Bold, dramatic design with high contrast",
    category="bold",
    design_theme="neo_brutalist",
    color_preset="default",
    icon_style=ICON_SHARP,
    animation_style=ANIM_SNAPPY,
    pattern_style=PATTERN_MINIMAL,
    interaction_style=INTERACT_BOLD,
    illustration_style=ILLUST_FLAT,
)

PACK_NATURE = ThemePack(
    name="nature",
    display_name="Nature Organic",
    description="Soft, natural design inspired by organic forms",
    category="playful",
    design_theme="organic",
    color_preset="green",
    icon_style=ICON_ROUNDED,
    animation_style=ANIM_GENTLE,
    pattern_style=PATTERN_DOTS,
    interaction_style=INTERACT_SUBTLE,
    illustration_style=ILLUST_HAND_DRAWN,
)


# Theme Pack Registry
THEME_PACKS: Dict[str, ThemePack] = {
    "corporate": PACK_CORPORATE,
    "playful": PACK_PLAYFUL,
    "retro": PACK_RETRO,
    "elegant": PACK_ELEGANT,
    "brutalist": PACK_BRUTALIST,
    "nature": PACK_NATURE,
}


def get_theme_pack(name: str) -> Optional[ThemePack]:
    """Get a theme pack by name."""
    return THEME_PACKS.get(name)


def get_all_theme_packs() -> Dict[str, ThemePack]:
    """Get all available theme packs."""
    return THEME_PACKS.copy()
