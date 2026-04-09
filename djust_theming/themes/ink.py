"""Ink -- Japanese calligraphy minimalism — sharp edges, single vermillion accent."""

from ._base import (
    AnimationStyle,
    ColorScale,
    DesignSystem,
    IconStyle,
    InteractionStyle,
    LayoutStyle,
    SurfaceStyle,
    ThemePack,
    ThemePreset,
    ThemeTokens,
    TypographyStyle,
    ILLUST_LINE,
    PATTERN_DOTS,
    PATTERN_MINIMAL,
)

# --- Color Preset ---

LIGHT = ThemeTokens(
    background=ColorScale(40, 15, 97),
    foreground=ColorScale(220, 15, 12),
    card=ColorScale(40, 12, 94),
    card_foreground=ColorScale(220, 15, 12),
    popover=ColorScale(40, 12, 94),
    popover_foreground=ColorScale(220, 15, 12),
    primary=ColorScale(4, 80, 52),
    primary_foreground=ColorScale(0, 0, 100),
    secondary=ColorScale(40, 10, 90),
    secondary_foreground=ColorScale(220, 15, 12),
    muted=ColorScale(40, 10, 90),
    muted_foreground=ColorScale(220, 10, 45),
    accent=ColorScale(40, 10, 88),
    accent_foreground=ColorScale(220, 15, 12),
    destructive=ColorScale(4, 80, 52),
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(150, 30, 40),
    success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(40, 60, 50),
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(210, 30, 50),
    info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(4, 80, 48),
    link_hover=ColorScale(4, 80, 38),
    code=ColorScale(40, 10, 92),
    code_foreground=ColorScale(220, 15, 20),
    selection=ColorScale(4, 80, 85),
    selection_foreground=ColorScale(4, 10, 15),
    brand=ColorScale(4, 80, 52),
    brand_foreground=ColorScale(0, 0, 100),
    border=ColorScale(220, 8, 82),
    input=ColorScale(220, 8, 82),
    ring=ColorScale(4, 80, 52),
    surface_1=ColorScale(4, 5, 96),
    surface_2=ColorScale(4, 5, 93),
    surface_3=ColorScale(4, 5, 90),
)

DARK = ThemeTokens(
    background=ColorScale(220, 15, 8),
    foreground=ColorScale(40, 15, 85),
    card=ColorScale(220, 12, 12),
    card_foreground=ColorScale(40, 15, 85),
    popover=ColorScale(220, 12, 12),
    popover_foreground=ColorScale(40, 15, 85),
    primary=ColorScale(4, 80, 58),
    primary_foreground=ColorScale(220, 15, 8),
    secondary=ColorScale(220, 12, 15),
    secondary_foreground=ColorScale(40, 15, 85),
    muted=ColorScale(220, 12, 15),
    muted_foreground=ColorScale(40, 10, 55),
    accent=ColorScale(220, 12, 18),
    accent_foreground=ColorScale(40, 15, 85),
    destructive=ColorScale(4, 80, 58),
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(150, 30, 50),
    success_foreground=ColorScale(220, 15, 8),
    warning=ColorScale(40, 60, 55),
    warning_foreground=ColorScale(220, 15, 8),
    info=ColorScale(210, 30, 60),
    info_foreground=ColorScale(220, 15, 8),
    link=ColorScale(4, 80, 58),
    link_hover=ColorScale(4, 80, 70),
    code=ColorScale(220, 12, 14),
    code_foreground=ColorScale(4, 80, 65),
    selection=ColorScale(4, 80, 25),
    selection_foreground=ColorScale(4, 10, 90),
    brand=ColorScale(4, 80, 58),
    brand_foreground=ColorScale(220, 15, 8),
    border=ColorScale(220, 12, 18),
    input=ColorScale(220, 12, 18),
    ring=ColorScale(4, 80, 58),
    surface_1=ColorScale(4, 5, 6),
    surface_2=ColorScale(4, 5, 10),
    surface_3=ColorScale(4, 5, 14),
)

PRESET = ThemePreset(
    name="ink",
    display_name="Ink",
    description="Japanese calligraphy minimalism — sharp edges, single vermillion accent",
    light=LIGHT,
    dark=DARK,
)


# =============================================================================
# Design System
# =============================================================================

TYPOGRAPHY = TypographyStyle(
    name="ink",
    heading_font='"Noto Serif JP", Georgia, serif',
    body_font="system-ui, sans-serif",
    base_size="16px",
    heading_scale=1.2,
    line_height="1.7",
    body_line_height="1.8",
    heading_weight="400",
    section_heading_weight="400",
    body_weight="400",
    letter_spacing="0.02em",
    prose_max_width="36rem",
    badge_radius="0px",
)

LAYOUT = LayoutStyle(
    name="ink",
    space_unit="1rem",
    space_scale=1.5,
    border_radius_sm="0px",
    border_radius_md="0px",
    border_radius_lg="0px",
    button_shape="sharp",
    card_shape="sharp",
    input_shape="sharp",
    container_width="900px",
    grid_gap="1.5rem",
    section_spacing="4rem",
    hero_padding_top="8rem",
    hero_padding_bottom="4rem",
    hero_line_height="1.0",
    hero_max_width="40rem",
)

SURFACE = SurfaceStyle(
    name="ink",
    shadow_sm="none",
    shadow_md="none",
    shadow_lg="none",
    border_width="1px",
    border_style="solid",
    surface_treatment="flat",
    backdrop_blur="0px",
    noise_opacity=0.0,
)

ICON = IconStyle(
    name="ink",
    style="outlined",
    weight="thin",
    size_scale=1.0,
    stroke_width="1",
    corner_rounding="0px",
)

ANIMATION = AnimationStyle(
    name="ink",
    entrance_effect="none",
    exit_effect="none",
    hover_effect="none",
    hover_scale=1.0,
    hover_translate_y="0px",
    click_effect="none",
    loading_style="spinner",
    transition_style="instant",
    duration_fast="0s",
    duration_normal="0s",
    duration_slow="0.1s",
    easing="linear",
)

INTERACTION = InteractionStyle(
    name="ink",
    button_hover="darken",
    link_hover="underline",
    card_hover="border",
    focus_style="outline",
    focus_ring_width="1px",
)

DESIGN_SYSTEM = DesignSystem(
    name="ink",
    display_name="Ink",
    description="Japanese calligraphy -- sharp edges, single vermillion accent, poster-like",
    category="minimal",
    typography=TYPOGRAPHY,
    layout=LAYOUT,
    surface=SURFACE,
    icons=ICON,
    animation=ANIMATION,
    interaction=INTERACTION,
)


# =============================================================================
# Theme Pack
# =============================================================================

PACK = ThemePack(
    name="ink",
    display_name="Ink",
    description="Japanese calligraphy -- sharp edges, single vermillion accent, poster-like",
    category="minimal",
    design_theme="ink",
    color_preset="ink",
    icon_style=ICON,
    animation_style=ANIMATION,
    pattern_style=PATTERN_MINIMAL,
    interaction_style=INTERACTION,
    illustration_style=ILLUST_LINE,
)
