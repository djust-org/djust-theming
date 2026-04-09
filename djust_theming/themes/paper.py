"""Paper -- Reading-optimized warm — like sunlit paper, large radius."""

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
    PATTERN_NOISE,
)

# --- Color Preset ---

LIGHT = ThemeTokens(
    background=ColorScale(40, 33, 96),
    foreground=ColorScale(25, 15, 20),
    card=ColorScale(40, 28, 93),
    card_foreground=ColorScale(25, 15, 20),
    popover=ColorScale(40, 28, 93),
    popover_foreground=ColorScale(25, 15, 20),
    primary=ColorScale(30, 40, 45),
    primary_foreground=ColorScale(40, 33, 96),
    secondary=ColorScale(40, 22, 88),
    secondary_foreground=ColorScale(25, 15, 20),
    muted=ColorScale(40, 22, 88),
    muted_foreground=ColorScale(25, 10, 45),
    accent=ColorScale(40, 22, 85),
    accent_foreground=ColorScale(25, 15, 20),
    destructive=ColorScale(0, 55, 50),
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(100, 35, 42),
    success_foreground=ColorScale(0, 0, 100),
    warning=ColorScale(35, 65, 50),
    warning_foreground=ColorScale(0, 0, 10),
    info=ColorScale(210, 35, 50),
    info_foreground=ColorScale(0, 0, 100),
    link=ColorScale(210, 45, 45),
    link_hover=ColorScale(210, 45, 35),
    code=ColorScale(40, 22, 90),
    code_foreground=ColorScale(25, 15, 30),
    selection=ColorScale(30, 40, 85),
    selection_foreground=ColorScale(30, 10, 15),
    brand=ColorScale(30, 40, 45),
    brand_foreground=ColorScale(40, 33, 96),
    border=ColorScale(35, 15, 80),
    input=ColorScale(35, 15, 80),
    ring=ColorScale(30, 40, 45),
    surface_1=ColorScale(30, 5, 96),
    surface_2=ColorScale(30, 5, 93),
    surface_3=ColorScale(30, 5, 90),
)

DARK = ThemeTokens(
    background=ColorScale(25, 12, 14),
    foreground=ColorScale(40, 25, 85),
    card=ColorScale(25, 10, 18),
    card_foreground=ColorScale(40, 25, 85),
    popover=ColorScale(25, 10, 18),
    popover_foreground=ColorScale(40, 25, 85),
    primary=ColorScale(30, 40, 60),
    primary_foreground=ColorScale(25, 12, 14),
    secondary=ColorScale(25, 10, 22),
    secondary_foreground=ColorScale(40, 25, 85),
    muted=ColorScale(25, 10, 22),
    muted_foreground=ColorScale(30, 10, 55),
    accent=ColorScale(25, 10, 25),
    accent_foreground=ColorScale(40, 25, 85),
    destructive=ColorScale(0, 55, 55),
    destructive_foreground=ColorScale(0, 0, 100),
    success=ColorScale(100, 35, 52),
    success_foreground=ColorScale(25, 12, 14),
    warning=ColorScale(35, 65, 55),
    warning_foreground=ColorScale(25, 12, 14),
    info=ColorScale(210, 35, 60),
    info_foreground=ColorScale(25, 12, 14),
    link=ColorScale(210, 45, 60),
    link_hover=ColorScale(210, 45, 72),
    code=ColorScale(25, 10, 20),
    code_foreground=ColorScale(30, 40, 65),
    selection=ColorScale(30, 40, 25),
    selection_foreground=ColorScale(30, 10, 90),
    brand=ColorScale(30, 40, 60),
    brand_foreground=ColorScale(25, 12, 14),
    border=ColorScale(25, 10, 25),
    input=ColorScale(25, 10, 25),
    ring=ColorScale(30, 40, 60),
    surface_1=ColorScale(30, 5, 6),
    surface_2=ColorScale(30, 5, 10),
    surface_3=ColorScale(30, 5, 14),
)

PRESET = ThemePreset(
    name="paper",
    display_name="Paper",
    description="Reading-optimized warm — like sunlit paper, large radius",
    light=LIGHT,
    dark=DARK,
)


# =============================================================================
# Design System
# =============================================================================

TYPOGRAPHY = TypographyStyle(
    name="paper",
    heading_font="Georgia, serif",
    body_font="system-ui, sans-serif",
    base_size="16px",
    heading_scale=1.25,
    line_height="1.6",
    body_line_height="1.8",
    heading_weight="600",
    section_heading_weight="600",
    body_weight="400",
    letter_spacing="normal",
    prose_max_width="38rem",
    badge_radius="9999px",
)

LAYOUT = LayoutStyle(
    name="paper",
    space_unit="1rem",
    space_scale=1.5,
    border_radius_sm="2px",
    border_radius_md="4px",
    border_radius_lg="6px",
    button_shape="rounded",
    card_shape="rounded",
    input_shape="rounded",
    container_width="900px",
    grid_gap="1.5rem",
    section_spacing="4rem",
    hero_padding_top="7rem",
    hero_padding_bottom="4rem",
    hero_line_height="1.2",
    hero_max_width="42rem",
)

SURFACE = SurfaceStyle(
    name="paper",
    shadow_sm="0 1px 3px rgba(80, 60, 40, 0.06)",
    shadow_md="0 3px 8px rgba(80, 60, 40, 0.08)",
    shadow_lg="0 6px 16px rgba(80, 60, 40, 0.1)",
    border_width="1px",
    border_style="solid",
    surface_treatment="noise",
    backdrop_blur="0px",
    noise_opacity=0.03,
)

ICON = IconStyle(
    name="paper",
    style="outlined",
    weight="regular",
    size_scale=1.0,
    stroke_width="1.5",
    corner_rounding="2px",
)

ANIMATION = AnimationStyle(
    name="paper",
    entrance_effect="fade",
    exit_effect="fade",
    hover_effect="lift",
    hover_scale=1.0,
    hover_translate_y="-1px",
    click_effect="none",
    loading_style="pulse",
    transition_style="smooth",
    duration_fast="0.15s",
    duration_normal="0.25s",
    duration_slow="0.4s",
    easing="cubic-bezier(0.25, 0.1, 0.25, 1)",
)

INTERACTION = InteractionStyle(
    name="paper",
    button_hover="lift",
    link_hover="underline",
    card_hover="shadow",
    focus_style="ring",
    focus_ring_width="2px",
)

DESIGN_SYSTEM = DesignSystem(
    name="paper",
    display_name="Paper",
    description="Reading-optimized warm -- sunlit paper, serif headings, book-like",
    category="elegant",
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
    name="paper",
    display_name="Paper",
    description="Reading-optimized warm -- sunlit paper, serif headings, book-like",
    category="elegant",
    design_theme="paper",
    color_preset="paper",
    icon_style=ICON,
    animation_style=ANIMATION,
    pattern_style=PATTERN_NOISE,
    interaction_style=INTERACTION,
    illustration_style=ILLUST_LINE,
)
