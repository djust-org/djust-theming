"""
Design Systems - Pure visual design without color dependency.

A DesignSystem defines the non-color aspects of UI:
- Typography (fonts, sizes, spacing)
- Layout (grid systems, component shapes) 
- Visual patterns (borders, shadows, textures)
- Animation behaviors
- Interaction feedback
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class TypographyStyle:
    """Typography configuration."""
    name: str
    
    # Font families
    heading_font: str = "system-ui"  # "system-ui", "serif", "mono", "display"
    body_font: str = "system-ui"
    
    # Scale and sizing
    base_size: str = "16px"
    heading_scale: float = 1.25  # Multiplier between heading levels
    line_height: str = "1.5"
    
    # Weight and style
    heading_weight: str = "600"  # "300", "400", "500", "600", "700", "800", "900"
    body_weight: str = "400"
    letter_spacing: str = "normal"  # "tight", "normal", "wide"


@dataclass 
class LayoutStyle:
    """Layout and spacing configuration."""
    name: str
    
    # Spacing system
    space_unit: str = "1rem"  # Base unit for spacing
    space_scale: float = 1.5  # Ratio between spacing levels
    
    # Border radius system
    border_radius_sm: str = "0.25rem"
    border_radius_md: str = "0.5rem" 
    border_radius_lg: str = "1rem"
    
    # Component shapes
    button_shape: str = "rounded"  # "sharp", "rounded", "pill", "organic"
    card_shape: str = "rounded"
    input_shape: str = "rounded"
    
    # Grid and layout
    container_width: str = "1200px"
    grid_gap: str = "1.5rem"
    section_spacing: str = "3rem"


@dataclass
class SurfaceStyle:
    """Surface treatments and visual depth."""
    name: str
    
    # Shadow system
    shadow_sm: str = "0 1px 2px rgba(0,0,0,0.1)"
    shadow_md: str = "0 4px 6px rgba(0,0,0,0.1)" 
    shadow_lg: str = "0 10px 15px rgba(0,0,0,0.1)"
    
    # Border system
    border_width: str = "1px"
    border_style: str = "solid"  # "solid", "dashed", "dotted", "none"
    
    # Background treatments
    surface_treatment: str = "flat"  # "flat", "glass", "textured", "gradient"
    backdrop_blur: str = "0px"
    noise_opacity: float = 0.0


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
class InteractionStyle:
    """User interaction feedback.""" 
    name: str

    # Hover effects
    button_hover: str = "lift"  # "lift", "scale", "glow", "darken", "none"
    link_hover: str = "underline"  # "underline", "color", "background", "none"
    card_hover: str = "lift"  # "lift", "scale", "border", "shadow", "none"

    # Focus effects
    focus_style: str = "ring"  # "ring", "outline", "glow", "underline"
    focus_ring_width: str = "2px"


@dataclass 
class DesignSystem:
    """
    Complete design system - all visual aspects EXCEPT colors.
    
    This allows any design system to be combined with any color preset.
    """
    name: str
    display_name: str
    description: str
    category: str  # "minimal", "bold", "elegant", "playful", "industrial"
    
    # Core styling components
    typography: TypographyStyle
    layout: LayoutStyle  
    surface: SurfaceStyle
    icons: IconStyle
    animation: AnimationStyle
    interaction: InteractionStyle


# =============================================================================
# Typography Presets
# =============================================================================

TYPO_MATERIAL = TypographyStyle(
    name="material",
    heading_font="system-ui",
    body_font="system-ui",
    base_size="16px",
    heading_scale=1.25,
    line_height="1.5",
    heading_weight="500",
    body_weight="400",
    letter_spacing="normal"
)

TYPO_IOS = TypographyStyle(
    name="ios",
    heading_font="system-ui",
    body_font="system-ui",
    base_size="17px",
    heading_scale=1.3,
    line_height="1.4",
    heading_weight="600",
    body_weight="400",
    letter_spacing="tight"
)

TYPO_FLUENT = TypographyStyle(
    name="fluent",
    heading_font="system-ui",
    body_font="system-ui",
    base_size="14px",
    heading_scale=1.25,
    line_height="1.5",
    heading_weight="600",
    body_weight="400",
    letter_spacing="normal"
)

TYPO_PLAYFUL = TypographyStyle(
    name="playful",
    heading_font="display",
    body_font="system-ui",
    base_size="16px",
    heading_scale=1.3,
    line_height="1.75",
    heading_weight="700",
    body_weight="400",
    letter_spacing="normal"
)

TYPO_CORPORATE = TypographyStyle(
    name="corporate",
    heading_font="system-ui",
    body_font="system-ui",
    base_size="16px",
    heading_scale=1.2,
    line_height="1.6",
    heading_weight="600",
    body_weight="400",
    letter_spacing="normal"
)

TYPO_DENSE = TypographyStyle(
    name="dense",
    heading_font="system-ui",
    body_font="system-ui",
    base_size="13px",
    heading_scale=1.15,
    line_height="1.35",
    heading_weight="600",
    body_weight="400",
    letter_spacing="tight"
)

TYPO_MINIMAL = TypographyStyle(
    name="minimal",
    heading_font="system-ui",
    body_font="system-ui",
    base_size="16px",
    heading_scale=1.2,  # Subtle scale
    line_height="1.6",
    heading_weight="500",  # Lighter weight
    body_weight="400",
    letter_spacing="normal"
)

TYPO_BRUTALIST = TypographyStyle(
    name="brutalist", 
    heading_font="system-ui",
    body_font="system-ui",
    base_size="18px",  # Larger base
    heading_scale=1.4,  # Aggressive scale
    line_height="1.3",  # Tighter line height
    heading_weight="900",  # Black weight
    body_weight="500",
    letter_spacing="tight"
)

TYPO_ELEGANT = TypographyStyle(
    name="elegant",
    heading_font="serif",  # Serif headings
    body_font="system-ui",
    base_size="16px",
    heading_scale=1.3,
    line_height="1.7",  # Generous line height
    heading_weight="400",  # Light serif
    body_weight="400",
    letter_spacing="wide"  # Spaced out
)

TYPO_RETRO = TypographyStyle(
    name="retro",
    heading_font="mono",  # Monospace
    body_font="system-ui", 
    base_size="14px",  # Smaller, pixel-like
    heading_scale=1.1,  # Minimal scale
    line_height="1.4",
    heading_weight="700",
    body_weight="400",
    letter_spacing="normal"
)

TYPO_ORGANIC = TypographyStyle(
    name="organic",
    heading_font="system-ui",
    body_font="system-ui",
    base_size="16px", 
    heading_scale=1.25,
    line_height="1.6",
    heading_weight="600",
    body_weight="400",
    letter_spacing="normal"
)


# =============================================================================
# Layout Presets
# =============================================================================

LAYOUT_MATERIAL = LayoutStyle(
    name="material",
    space_unit="1rem",
    space_scale=2.0,
    border_radius_sm="4px",
    border_radius_md="8px",
    border_radius_lg="12px",
    button_shape="rounded",
    card_shape="rounded",
    input_shape="rounded",
    container_width="1200px",
    grid_gap="1.5rem",
    section_spacing="3rem"
)

LAYOUT_IOS = LayoutStyle(
    name="ios",
    space_unit="1rem",
    space_scale=1.5,
    border_radius_sm="8px",
    border_radius_md="12px",
    border_radius_lg="16px",
    button_shape="rounded",
    card_shape="rounded",
    input_shape="rounded",
    container_width="1100px",
    grid_gap="1.5rem",
    section_spacing="3rem"
)

LAYOUT_FLUENT = LayoutStyle(
    name="fluent",
    space_unit="1rem",
    space_scale=1.5,
    border_radius_sm="2px",
    border_radius_md="4px",
    border_radius_lg="8px",
    button_shape="rounded",
    card_shape="rounded",
    input_shape="rounded",
    container_width="1200px",
    grid_gap="1.5rem",
    section_spacing="3rem"
)

LAYOUT_PLAYFUL = LayoutStyle(
    name="playful",
    space_unit="1rem",
    space_scale=1.5,
    border_radius_sm="8px",
    border_radius_md="16px",
    border_radius_lg="24px",
    button_shape="pill",
    card_shape="rounded",
    input_shape="pill",
    container_width="1200px",
    grid_gap="2rem",
    section_spacing="4rem"
)

LAYOUT_CORPORATE = LayoutStyle(
    name="corporate",
    space_unit="1rem",
    space_scale=1.5,
    border_radius_sm="2px",
    border_radius_md="4px",
    border_radius_lg="8px",
    button_shape="rounded",
    card_shape="rounded",
    input_shape="rounded",
    container_width="1200px",
    grid_gap="1.5rem",
    section_spacing="3rem"
)

LAYOUT_DENSE = LayoutStyle(
    name="dense",
    space_unit="0.5rem",
    space_scale=1.5,
    border_radius_sm="2px",
    border_radius_md="2px",
    border_radius_lg="4px",
    button_shape="rounded",
    card_shape="sharp",
    input_shape="rounded",
    container_width="1400px",
    grid_gap="1rem",
    section_spacing="2rem"
)

LAYOUT_MINIMAL = LayoutStyle(
    name="minimal",
    space_unit="1rem",
    space_scale=1.5,
    border_radius_sm="2px",  # Subtle radius
    border_radius_md="4px",
    border_radius_lg="8px",
    button_shape="rounded",
    card_shape="rounded",
    input_shape="rounded",
    container_width="1000px",  # Narrower
    grid_gap="2rem",  # More space
    section_spacing="4rem"
)

LAYOUT_BRUTALIST = LayoutStyle(
    name="brutalist",
    space_unit="1rem", 
    space_scale=2.0,  # Bigger jumps
    border_radius_sm="0px",  # No radius
    border_radius_md="0px",
    border_radius_lg="0px", 
    button_shape="sharp",
    card_shape="sharp",
    input_shape="sharp",
    container_width="1400px",  # Wide
    grid_gap="1rem",  # Tight spacing
    section_spacing="2rem"
)

LAYOUT_ELEGANT = LayoutStyle(
    name="elegant",
    space_unit="1rem",
    space_scale=1.618,  # Golden ratio
    border_radius_sm="6px",
    border_radius_md="12px",
    border_radius_lg="20px",
    button_shape="rounded", 
    card_shape="rounded",
    input_shape="rounded",
    container_width="900px",  # Conservative width
    grid_gap="3rem",  # Generous spacing
    section_spacing="5rem"
)

LAYOUT_RETRO = LayoutStyle(
    name="retro",
    space_unit="8px",  # Pixel-based
    space_scale=2.0,
    border_radius_sm="0px",  # Sharp pixels
    border_radius_md="0px",
    border_radius_lg="0px",
    button_shape="sharp",
    card_shape="sharp", 
    input_shape="sharp",
    container_width="1024px",  # Old screen size
    grid_gap="16px",
    section_spacing="32px"
)

LAYOUT_ORGANIC = LayoutStyle(
    name="organic",
    space_unit="1rem",
    space_scale=1.4,
    border_radius_sm="12px",  # Very rounded
    border_radius_md="20px",
    border_radius_lg="32px", 
    button_shape="pill",  # Pill shapes
    card_shape="organic",
    input_shape="pill",
    container_width="1100px",
    grid_gap="1.5rem",
    section_spacing="3rem"
)


# =============================================================================
# Surface Presets
# =============================================================================

SURFACE_MATERIAL = SurfaceStyle(
    name="material",
    shadow_sm="0 2px 4px rgba(0,0,0,0.14), 0 3px 4px rgba(0,0,0,0.12)",
    shadow_md="0 4px 8px rgba(0,0,0,0.14), 0 6px 10px rgba(0,0,0,0.12)",
    shadow_lg="0 12px 17px rgba(0,0,0,0.14), 0 5px 22px rgba(0,0,0,0.12)",
    border_width="1px",
    border_style="solid",
    surface_treatment="flat",
    backdrop_blur="0px",
    noise_opacity=0.0
)

SURFACE_IOS = SurfaceStyle(
    name="ios",
    shadow_sm="0 2px 4px rgba(0,0,0,0.06)",
    shadow_md="0 4px 8px rgba(0,0,0,0.08)",
    shadow_lg="0 8px 16px rgba(0,0,0,0.1)",
    border_width="1px",
    border_style="solid",
    surface_treatment="flat",
    backdrop_blur="0px",
    noise_opacity=0.0
)

SURFACE_FLUENT = SurfaceStyle(
    name="fluent",
    shadow_sm="0 1.6px 3.6px rgba(0,0,0,0.13), 0 0.3px 0.9px rgba(0,0,0,0.11)",
    shadow_md="0 3.2px 7.2px rgba(0,0,0,0.13), 0 0.6px 1.8px rgba(0,0,0,0.11)",
    shadow_lg="0 6.4px 14.4px rgba(0,0,0,0.13), 0 1.2px 3.6px rgba(0,0,0,0.11)",
    border_width="1px",
    border_style="solid",
    surface_treatment="flat",
    backdrop_blur="0px",
    noise_opacity=0.0
)

SURFACE_PLAYFUL = SurfaceStyle(
    name="playful",
    shadow_sm="0 2px 8px rgba(0,0,0,0.08)",
    shadow_md="0 4px 16px rgba(0,0,0,0.1)",
    shadow_lg="0 8px 32px rgba(0,0,0,0.12)",
    border_width="0px",
    border_style="none",
    surface_treatment="flat",
    backdrop_blur="0px",
    noise_opacity=0.0
)

SURFACE_CORPORATE = SurfaceStyle(
    name="corporate",
    shadow_sm="0 1px 3px rgba(0,0,0,0.08)",
    shadow_md="0 2px 6px rgba(0,0,0,0.1)",
    shadow_lg="0 4px 12px rgba(0,0,0,0.12)",
    border_width="1px",
    border_style="solid",
    surface_treatment="flat",
    backdrop_blur="0px",
    noise_opacity=0.0
)

SURFACE_DENSE = SurfaceStyle(
    name="dense",
    shadow_sm="0 1px 2px rgba(0,0,0,0.06)",
    shadow_md="0 1px 3px rgba(0,0,0,0.08)",
    shadow_lg="0 2px 6px rgba(0,0,0,0.1)",
    border_width="1px",
    border_style="solid",
    surface_treatment="flat",
    backdrop_blur="0px",
    noise_opacity=0.0
)

SURFACE_MINIMAL = SurfaceStyle(
    name="minimal",
    shadow_sm="0 1px 2px rgba(0,0,0,0.05)",  # Very subtle
    shadow_md="0 2px 4px rgba(0,0,0,0.08)",
    shadow_lg="0 4px 8px rgba(0,0,0,0.12)",
    border_width="1px",
    border_style="solid",
    surface_treatment="flat",
    backdrop_blur="0px",
    noise_opacity=0.0
)

SURFACE_BRUTALIST = SurfaceStyle(
    name="brutalist", 
    shadow_sm="4px 4px 0px rgba(0,0,0,1)",  # Hard shadows
    shadow_md="8px 8px 0px rgba(0,0,0,1)",
    shadow_lg="12px 12px 0px rgba(0,0,0,1)",
    border_width="3px",  # Thick borders
    border_style="solid",
    surface_treatment="flat",
    backdrop_blur="0px",
    noise_opacity=0.0
)

SURFACE_ELEGANT = SurfaceStyle(
    name="elegant",
    shadow_sm="0 2px 8px rgba(0,0,0,0.08)", 
    shadow_md="0 8px 24px rgba(0,0,0,0.12)",
    shadow_lg="0 16px 40px rgba(0,0,0,0.16)",  # Soft, large shadows
    border_width="1px",
    border_style="solid", 
    surface_treatment="gradient",  # Subtle gradients
    backdrop_blur="0px",
    noise_opacity=0.02  # Subtle texture
)

SURFACE_RETRO = SurfaceStyle(
    name="retro",
    shadow_sm="2px 2px 0px rgba(0,0,0,0.8)",  # Pixel shadows
    shadow_md="4px 4px 0px rgba(0,0,0,0.8)",
    shadow_lg="6px 6px 0px rgba(0,0,0,0.8)", 
    border_width="2px",
    border_style="solid",
    surface_treatment="textured",  # Dithered texture
    backdrop_blur="0px",
    noise_opacity=0.15
)

SURFACE_ORGANIC = SurfaceStyle(
    name="organic",
    shadow_sm="0 3px 6px rgba(0,0,0,0.1)",
    shadow_md="0 6px 12px rgba(0,0,0,0.15)", 
    shadow_lg="0 12px 24px rgba(0,0,0,0.2)",
    border_width="0px",  # No borders
    border_style="none",
    surface_treatment="glass",  # Soft glass effect
    backdrop_blur="8px",
    noise_opacity=0.0
)


# =============================================================================
# Icon Style Presets
# =============================================================================

ICON_MATERIAL = IconStyle(
    name="material",
    style="filled",
    weight="regular",
    size_scale=1.0,
    stroke_width="2",
    corner_rounding="0px"
)

ICON_IOS = IconStyle(
    name="ios",
    style="outlined",
    weight="thin",
    size_scale=1.0,
    stroke_width="1.5",
    corner_rounding="4px"
)

ICON_FLUENT = IconStyle(
    name="fluent",
    style="outlined",
    weight="regular",
    size_scale=1.0,
    stroke_width="2",
    corner_rounding="0px"
)

ICON_PLAYFUL = IconStyle(
    name="playful",
    style="rounded",
    weight="regular",
    size_scale=1.1,
    stroke_width="2",
    corner_rounding="8px"
)

ICON_CORPORATE = IconStyle(
    name="corporate",
    style="outlined",
    weight="regular",
    size_scale=1.0,
    stroke_width="2",
    corner_rounding="0px"
)

ICON_DENSE = IconStyle(
    name="dense",
    style="outlined",
    weight="thin",
    size_scale=0.85,
    stroke_width="1.5",
    corner_rounding="0px"
)

ICON_MINIMAL = IconStyle(
    name="minimal",
    style="outlined",
    weight="thin",
    size_scale=0.9,  # Smaller icons
    stroke_width="1.5",
    corner_rounding="2px"
)

ICON_BRUTALIST = IconStyle(
    name="brutalist", 
    style="filled",
    weight="bold",
    size_scale=1.2,  # Larger, bold icons
    stroke_width="3",
    corner_rounding="0px"
)

ICON_ELEGANT = IconStyle(
    name="elegant",
    style="outlined", 
    weight="thin",
    size_scale=1.0,
    stroke_width="1",  # Very thin strokes
    corner_rounding="4px"
)

ICON_RETRO = IconStyle(
    name="retro",
    style="filled",
    weight="regular", 
    size_scale=1.0,
    stroke_width="2",
    corner_rounding="0px"  # Sharp pixels
)

ICON_ORGANIC = IconStyle(
    name="organic",
    style="rounded",
    weight="regular",
    size_scale=1.1,
    stroke_width="2",
    corner_rounding="8px"  # Very rounded
)


# =============================================================================
# Animation Style Presets
# =============================================================================

ANIM_MATERIAL = AnimationStyle(
    name="material",
    entrance_effect="fade",
    exit_effect="fade",
    hover_effect="lift",
    hover_scale=1.02,
    hover_translate_y="-2px",
    click_effect="ripple",
    loading_style="spinner",
    transition_style="smooth",
    duration_fast="0.1s",
    duration_normal="0.2s",
    duration_slow="0.3s",
    easing="cubic-bezier(0.4, 0, 0.2, 1)"
)

ANIM_IOS = AnimationStyle(
    name="ios",
    entrance_effect="fade",
    exit_effect="fade",
    hover_effect="scale",
    hover_scale=1.05,
    hover_translate_y="0px",
    click_effect="none",
    loading_style="spinner",
    transition_style="snappy",
    duration_fast="0.15s",
    duration_normal="0.25s",
    duration_slow="0.35s",
    easing="cubic-bezier(0.42, 0, 0.58, 1)"
)

ANIM_FLUENT = AnimationStyle(
    name="fluent",
    entrance_effect="fade",
    exit_effect="fade",
    hover_effect="lift",
    hover_scale=1.02,
    hover_translate_y="-2px",
    click_effect="ripple",
    loading_style="progress",
    transition_style="smooth",
    duration_fast="0.167s",
    duration_normal="0.25s",
    duration_slow="0.367s",
    easing="cubic-bezier(0.1, 0.9, 0.2, 1)"
)

ANIM_PLAYFUL = AnimationStyle(
    name="playful",
    entrance_effect="bounce",
    exit_effect="scale",
    hover_effect="scale",
    hover_scale=1.05,
    hover_translate_y="0px",
    click_effect="bounce",
    loading_style="pulse",
    transition_style="bouncy",
    duration_fast="0.2s",
    duration_normal="0.3s",
    duration_slow="0.5s",
    easing="cubic-bezier(0.68, -0.55, 0.265, 1.55)"
)

ANIM_CORPORATE = AnimationStyle(
    name="corporate",
    entrance_effect="fade",
    exit_effect="fade",
    hover_effect="lift",
    hover_scale=1.01,
    hover_translate_y="-1px",
    click_effect="none",
    loading_style="progress",
    transition_style="smooth",
    duration_fast="0.15s",
    duration_normal="0.2s",
    duration_slow="0.3s",
    easing="cubic-bezier(0.4, 0, 0.2, 1)"
)

ANIM_DENSE = AnimationStyle(
    name="dense",
    entrance_effect="fade",
    exit_effect="fade",
    hover_effect="none",
    hover_scale=1.0,
    hover_translate_y="0px",
    click_effect="none",
    loading_style="progress",
    transition_style="instant",
    duration_fast="0.05s",
    duration_normal="0.1s",
    duration_slow="0.15s",
    easing="linear"
)

ANIM_MINIMAL = AnimationStyle(
    name="minimal",
    entrance_effect="fade",
    exit_effect="fade",
    hover_effect="none",  # No hover effects
    hover_scale=1.0,
    hover_translate_y="0px",
    click_effect="none",
    loading_style="progress",
    transition_style="smooth",
    duration_fast="0.2s",
    duration_normal="0.3s",
    duration_slow="0.4s",
    easing="ease-out"
)

ANIM_BRUTALIST = AnimationStyle(
    name="brutalist",
    entrance_effect="none",  # Instant appearance
    exit_effect="none",
    hover_effect="scale",
    hover_scale=1.05,  # Bold scale
    hover_translate_y="0px",
    click_effect="pulse",
    loading_style="spinner",
    transition_style="instant",
    duration_fast="0.05s",  # Very fast
    duration_normal="0.1s",
    duration_slow="0.15s",
    easing="linear"  # No easing curves
)

ANIM_ELEGANT = AnimationStyle(
    name="elegant", 
    entrance_effect="fade",
    exit_effect="fade",
    hover_effect="lift",
    hover_scale=1.02,  # Subtle
    hover_translate_y="-4px",  # Gentle lift
    click_effect="none",  # No aggressive feedback
    loading_style="skeleton",
    transition_style="smooth",
    duration_fast="0.4s",  # Slower, more graceful
    duration_normal="0.6s",
    duration_slow="0.8s",
    easing="cubic-bezier(0.25, 0.46, 0.45, 0.94)"  # Elegant curve
)

ANIM_RETRO = AnimationStyle(
    name="retro",
    entrance_effect="slide",  # Old-school slide
    exit_effect="slide",
    hover_effect="glow",
    hover_scale=1.0,  # No scaling
    hover_translate_y="0px", 
    click_effect="bounce",  # Arcade-style
    loading_style="progress",
    transition_style="snappy",
    duration_fast="0.1s",
    duration_normal="0.2s",
    duration_slow="0.3s", 
    easing="cubic-bezier(0.68, -0.55, 0.265, 1.55)"  # Bouncy
)

ANIM_ORGANIC = AnimationStyle(
    name="organic",
    entrance_effect="scale",  # Organic growth
    exit_effect="scale", 
    hover_effect="glow",
    hover_scale=1.03,
    hover_translate_y="-2px",
    click_effect="ripple",  # Natural ripple
    loading_style="pulse",
    transition_style="bouncy",
    duration_fast="0.3s", 
    duration_normal="0.5s",
    duration_slow="0.8s",
    easing="cubic-bezier(0.34, 1.56, 0.64, 1)"  # Organic bounce
)


# =============================================================================
# Interaction Style Presets
# =============================================================================

INTERACT_MATERIAL = InteractionStyle(
    name="material",
    button_hover="lift",
    link_hover="underline",
    card_hover="lift",
    focus_style="ring",
    focus_ring_width="2px"
)

INTERACT_IOS = InteractionStyle(
    name="ios",
    button_hover="scale",
    link_hover="color",
    card_hover="shadow",
    focus_style="ring",
    focus_ring_width="2px"
)

INTERACT_FLUENT = InteractionStyle(
    name="fluent",
    button_hover="lift",
    link_hover="underline",
    card_hover="shadow",
    focus_style="ring",
    focus_ring_width="2px"
)

INTERACT_PLAYFUL = InteractionStyle(
    name="playful",
    button_hover="glow",
    link_hover="background",
    card_hover="lift",
    focus_style="glow",
    focus_ring_width="3px"
)

INTERACT_CORPORATE = InteractionStyle(
    name="corporate",
    button_hover="darken",
    link_hover="underline",
    card_hover="border",
    focus_style="ring",
    focus_ring_width="2px"
)

INTERACT_DENSE = InteractionStyle(
    name="dense",
    button_hover="darken",
    link_hover="underline",
    card_hover="none",
    focus_style="outline",
    focus_ring_width="1px"
)

INTERACT_MINIMAL = InteractionStyle(
    name="minimal",
    button_hover="darken",  # Subtle color change
    link_hover="underline",
    card_hover="none",  # No card hover
    focus_style="underline",
    focus_ring_width="1px"
)

INTERACT_BRUTALIST = InteractionStyle(
    name="brutalist",
    button_hover="glow",  # Bold glow effect
    link_hover="background", 
    card_hover="shadow",  # Hard shadow change
    focus_style="outline",
    focus_ring_width="4px"  # Thick focus ring
)

INTERACT_ELEGANT = InteractionStyle(
    name="elegant",
    button_hover="lift", 
    link_hover="color",  # Subtle color shift
    card_hover="shadow",  # Soft shadow lift
    focus_style="glow",
    focus_ring_width="2px"
)

INTERACT_RETRO = InteractionStyle(
    name="retro", 
    button_hover="scale",  # Arcade-style scale
    link_hover="background",
    card_hover="border",  # Pixel border change
    focus_style="outline",
    focus_ring_width="2px"
)

INTERACT_ORGANIC = InteractionStyle(
    name="organic",
    button_hover="glow",  # Soft organic glow
    link_hover="color",
    card_hover="lift",  # Natural lift
    focus_style="glow", 
    focus_ring_width="3px"
)


# =============================================================================
# Complete Design Systems (Color-Independent)
# =============================================================================

DESIGN_MATERIAL = DesignSystem(
    name="material",
    display_name="Material Design",
    description="Google's Material Design with elevation-based hierarchy",
    category="professional",
    typography=TYPO_MATERIAL,
    layout=LAYOUT_MATERIAL,
    surface=SURFACE_MATERIAL,
    icons=ICON_MATERIAL,
    animation=ANIM_MATERIAL,
    interaction=INTERACT_MATERIAL
)

DESIGN_IOS = DesignSystem(
    name="ios",
    display_name="iOS",
    description="Apple's iOS design language with fluid animations",
    category="elegant",
    typography=TYPO_IOS,
    layout=LAYOUT_IOS,
    surface=SURFACE_IOS,
    icons=ICON_IOS,
    animation=ANIM_IOS,
    interaction=INTERACT_IOS
)

DESIGN_FLUENT = DesignSystem(
    name="fluent",
    display_name="Fluent Design",
    description="Microsoft's Fluent Design System with depth and motion",
    category="professional",
    typography=TYPO_FLUENT,
    layout=LAYOUT_FLUENT,
    surface=SURFACE_FLUENT,
    icons=ICON_FLUENT,
    animation=ANIM_FLUENT,
    interaction=INTERACT_FLUENT
)

DESIGN_PLAYFUL = DesignSystem(
    name="playful",
    display_name="Playful",
    description="Fun, energetic design with bouncy animations and rounded shapes",
    category="playful",
    typography=TYPO_PLAYFUL,
    layout=LAYOUT_PLAYFUL,
    surface=SURFACE_PLAYFUL,
    icons=ICON_PLAYFUL,
    animation=ANIM_PLAYFUL,
    interaction=INTERACT_PLAYFUL
)

DESIGN_CORPORATE = DesignSystem(
    name="corporate",
    display_name="Corporate",
    description="Professional, clean design for business applications",
    category="professional",
    typography=TYPO_CORPORATE,
    layout=LAYOUT_CORPORATE,
    surface=SURFACE_CORPORATE,
    icons=ICON_CORPORATE,
    animation=ANIM_CORPORATE,
    interaction=INTERACT_CORPORATE
)

DESIGN_DENSE = DesignSystem(
    name="dense",
    display_name="Dense",
    description="Compact, information-dense design for data-heavy interfaces",
    category="minimal",
    typography=TYPO_DENSE,
    layout=LAYOUT_DENSE,
    surface=SURFACE_DENSE,
    icons=ICON_DENSE,
    animation=ANIM_DENSE,
    interaction=INTERACT_DENSE
)

DESIGN_MINIMAL = DesignSystem(
    name="minimal",
    display_name="Minimal Clean",
    description="Pure, distraction-free design with maximum content focus",
    category="minimal",
    typography=TYPO_MINIMAL,
    layout=LAYOUT_MINIMAL,
    surface=SURFACE_MINIMAL,
    icons=ICON_MINIMAL,
    animation=ANIM_MINIMAL,
    interaction=INTERACT_MINIMAL
)

DESIGN_BRUTALIST = DesignSystem(
    name="brutalist",
    display_name="Neo-Brutalist",
    description="Bold, aggressive design with sharp edges and high contrast", 
    category="bold",
    typography=TYPO_BRUTALIST,
    layout=LAYOUT_BRUTALIST,
    surface=SURFACE_BRUTALIST,
    icons=ICON_BRUTALIST,
    animation=ANIM_BRUTALIST,
    interaction=INTERACT_BRUTALIST
)

DESIGN_ELEGANT = DesignSystem(
    name="elegant",
    display_name="Refined Elegance", 
    description="Sophisticated typography with generous spacing and subtle details",
    category="elegant",
    typography=TYPO_ELEGANT,
    layout=LAYOUT_ELEGANT,
    surface=SURFACE_ELEGANT,
    icons=ICON_ELEGANT,
    animation=ANIM_ELEGANT,
    interaction=INTERACT_ELEGANT
)

DESIGN_RETRO = DesignSystem(
    name="retro", 
    display_name="Pixel Perfect",
    description="Nostalgic pixel-art aesthetic with sharp edges and chunky shadows",
    category="retro",
    typography=TYPO_RETRO,
    layout=LAYOUT_RETRO,
    surface=SURFACE_RETRO,
    icons=ICON_RETRO,
    animation=ANIM_RETRO,
    interaction=INTERACT_RETRO
)

DESIGN_ORGANIC = DesignSystem(
    name="organic",
    display_name="Natural Flow",
    description="Soft, rounded design inspired by natural forms and gentle motion", 
    category="playful",
    typography=TYPO_ORGANIC,
    layout=LAYOUT_ORGANIC,
    surface=SURFACE_ORGANIC,
    icons=ICON_ORGANIC,
    animation=ANIM_ORGANIC,
    interaction=INTERACT_ORGANIC
)


# Design System Registry
DESIGN_SYSTEMS: Dict[str, DesignSystem] = {
    "material": DESIGN_MATERIAL,
    "ios": DESIGN_IOS,
    "fluent": DESIGN_FLUENT,
    "playful": DESIGN_PLAYFUL,
    "corporate": DESIGN_CORPORATE,
    "dense": DESIGN_DENSE,
    "minimalist": DESIGN_MINIMAL,
    "neo_brutalist": DESIGN_BRUTALIST,
    "elegant": DESIGN_ELEGANT,
    "retro": DESIGN_RETRO,
    "organic": DESIGN_ORGANIC,
}


def get_design_system(name: str) -> Optional[DesignSystem]:
    """Get a design system by name."""
    return DESIGN_SYSTEMS.get(name)


def get_all_design_systems() -> Dict[str, DesignSystem]:
    """Get all available design systems."""
    return DESIGN_SYSTEMS.copy()


# =============================================================================
# Legacy Theme Packs (for backward compatibility)
# =============================================================================


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

# ============================================
# Qwen-Generated Theme Packs
# ============================================

PACK_CYBERPUNK = ThemePack(
    name="cyberpunk",
    display_name="Cyberpunk Future",
    description="Futuristic interface with neon highlights and dark aesthetics",
    category="bold",
    design_theme="neo_brutalist",
    color_preset="cyberpunk",
    icon_style=ICON_SHARP,
    animation_style=ANIM_SNAPPY,
    pattern_style=PATTERN_GRID,
    interaction_style=INTERACT_BOLD,
    illustration_style=ILLUST_FLAT,
)

PACK_SUNSET = ThemePack(
    name="sunset",
    display_name="Golden Sunset",
    description="Warm, inviting design with golden hour color palette",
    category="elegant",
    design_theme="elegant",
    color_preset="sunset",
    icon_style=ICON_ROUNDED,
    animation_style=ANIM_GENTLE,
    pattern_style=PATTERN_GRADIENT,
    interaction_style=INTERACT_SUBTLE,
    illustration_style=ILLUST_HAND_DRAWN,
)

PACK_FOREST = ThemePack(
    name="forest",
    display_name="Forest Explorer",
    description="Natural, earthy design inspired by woodland environments",
    category="playful",
    design_theme="organic",
    color_preset="forest",
    icon_style=ICON_ROUNDED,
    animation_style=ANIM_SMOOTH,
    pattern_style=PATTERN_DOTS,
    interaction_style=INTERACT_SUBTLE,
    illustration_style=ILLUST_HAND_DRAWN,
)

PACK_OCEAN = ThemePack(
    name="ocean",
    display_name="Ocean Depths",
    description="Calming, fluid design with deep blue and teal tones",
    category="minimal",
    design_theme="material",
    color_preset="ocean",
    icon_style=ICON_FILLED,
    animation_style=ANIM_SMOOTH,
    pattern_style=PATTERN_MINIMAL,
    interaction_style=INTERACT_SUBTLE,
    illustration_style=ILLUST_FLAT,
)

PACK_METALLIC = ThemePack(
    name="metallic",
    display_name="Metallic Industrial",
    description="Sleek, modern design with industrial metallic aesthetics",
    category="professional",
    design_theme="corporate",
    color_preset="metallic",
    icon_style=ICON_OUTLINED,
    animation_style=ANIM_SMOOTH,
    pattern_style=PATTERN_NOISE,
    interaction_style=INTERACT_MINIMAL,
    illustration_style=ILLUST_LINE,
)


# Theme Pack Registry
THEME_PACKS: Dict[str, ThemePack] = {
    "corporate": PACK_CORPORATE,
    "playful": PACK_PLAYFUL,
    "retro": PACK_RETRO,
    "elegant": PACK_ELEGANT,
    "brutalist": PACK_BRUTALIST,
    "nature": PACK_NATURE,
    "cyberpunk": PACK_CYBERPUNK,
    "sunset": PACK_SUNSET,
    "forest": PACK_FOREST,
    "ocean": PACK_OCEAN,
    "metallic": PACK_METALLIC,
}


def get_theme_pack(name: str) -> Optional[ThemePack]:
    """Get a theme pack by name."""
    return THEME_PACKS.get(name)


def get_all_theme_packs() -> Dict[str, ThemePack]:
    """Get all available theme packs."""
    return THEME_PACKS.copy()
