"""
CSS Generator for Theme Packs.

Generates complete CSS including icons, animations, patterns, interactions,
and all other styling dimensions from a ThemePack.
"""

from .theme_packs import ThemePack, get_theme_pack
from .theme_css_generator import CompleteThemeCSSGenerator


class ThemePackCSSGenerator:
    """Generates CSS for complete theme packs."""

    def __init__(self, pack_name: str):
        """Initialize with a theme pack name."""
        self.pack = get_theme_pack(pack_name)
        if not self.pack:
            raise ValueError(f"Theme pack '{pack_name}' not found")

        # Initialize base theme generator
        self.theme_generator = CompleteThemeCSSGenerator(
            theme_name=self.pack.design_theme,
            color_preset=self.pack.color_preset
        )

    def generate_css(self) -> str:
        """Generate complete CSS for the theme pack."""
        parts = [
            f"/* Theme Pack: {self.pack.display_name} */",
            f"/* {self.pack.description} */",
            "",
            "/* Base Theme CSS */",
            self.theme_generator.generate_css(),
            "",
            "/* Icon Styles */",
            self._generate_icon_css(),
            "",
            "/* Animation Styles */",
            self._generate_animation_css(),
            "",
            "/* Pattern Styles */",
            self._generate_pattern_css(),
            "",
            "/* Interaction Styles */",
            self._generate_interaction_css(),
            "",
            "/* Illustration Styles */",
            self._generate_illustration_css(),
        ]
        return "\n".join(parts)

    def _generate_icon_css(self) -> str:
        """Generate CSS for icon styling."""
        icon = self.pack.icon_style

        # Base icon CSS that applies to all SVGs
        base_css = f"""
:root {{
  --icon-stroke-width: {icon.stroke_width};
  --icon-corner-rounding: {icon.corner_rounding};
  --icon-size-scale: {icon.size_scale};
}}

/* Apply icon styles to all SVG icons */
svg {{
  stroke-width: {icon.stroke_width};
}}
"""

        # Style-specific CSS modifications with !important to override inline SVG attributes
        style_css = ""
        if icon.style == "filled":
            style_css = """
/* Filled icon style */
svg {
  fill: currentColor !important;
  stroke: none !important;
}
svg path, svg circle, svg rect, svg polygon, svg line {
  fill: currentColor !important;
  stroke: none !important;
}
"""
        elif icon.style == "outlined":
            style_css = f"""
/* Outlined icon style */
svg {{
  fill: none !important;
  stroke: currentColor !important;
  stroke-width: {icon.stroke_width} !important;
  stroke-linecap: round !important;
  stroke-linejoin: round !important;
}}
svg path, svg circle, svg rect, svg polygon, svg line {{
  fill: none !important;
  stroke: currentColor !important;
}}
"""
        elif icon.style == "rounded":
            style_css = f"""
/* Rounded icon style */
svg {{
  fill: currentColor !important;
  stroke: none !important;
  stroke-width: {icon.stroke_width} !important;
  stroke-linecap: round !important;
  stroke-linejoin: round !important;
}}
svg path, svg circle, svg rect, svg polygon, svg line {{
  fill: currentColor !important;
  stroke: none !important;
}}
/* Add slight rounding to shapes */
svg rect {{
  rx: 2 !important;
}}
"""
        elif icon.style == "sharp":
            style_css = f"""
/* Sharp icon style */
svg {{
  fill: currentColor !important;
  stroke: currentColor !important;
  stroke-width: {icon.stroke_width} !important;
  stroke-linecap: square !important;
  stroke-linejoin: miter !important;
}}
svg path, svg circle, svg rect, svg polygon, svg line {{
  fill: currentColor !important;
  stroke: currentColor !important;
  stroke-width: {icon.stroke_width} !important;
}}
"""
        elif icon.style == "thin":
            style_css = f"""
/* Thin icon style */
svg {{
  fill: none !important;
  stroke: currentColor !important;
  stroke-width: {icon.stroke_width} !important;
  stroke-linecap: round !important;
  stroke-linejoin: round !important;
}}
svg path, svg circle, svg rect, svg polygon, svg line {{
  fill: none !important;
  stroke: currentColor !important;
  stroke-width: {icon.stroke_width} !important;
}}
"""

        return base_css + style_css

    def _generate_animation_css(self) -> str:
        """Generate CSS for animations and transitions."""
        anim = self.pack.animation_style

        hover_css = ""
        if anim.hover_effect == "lift":
            hover_css = f"""
.btn:hover, .card:hover {{
  transform: translateY({anim.hover_translate_y});
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
}}
"""
        elif anim.hover_effect == "scale":
            hover_css = f"""
.btn:hover, .card:hover {{
  transform: scale({anim.hover_scale});
}}
"""
        elif anim.hover_effect == "glow":
            hover_css = """
.btn:hover, .card:hover {
  box-shadow: 0 0 20px hsla(var(--primary), 0.5);
}
"""

        click_css = ""
        if anim.click_effect == "ripple":
            click_css = """
.btn:active {
  position: relative;
  overflow: hidden;
}

.btn:active::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle, hsla(var(--primary-foreground), 0.3) 0%, transparent 70%);
  animation: ripple 0.6s ease-out;
}

@keyframes ripple {
  to {
    transform: scale(2);
    opacity: 0;
  }
}
"""
        elif anim.click_effect == "pulse":
            click_css = """
.btn:active {
  animation: pulse 0.3s ease-out;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(0.95); }
}
"""
        elif anim.click_effect == "bounce":
            click_css = """
.btn:active {
  animation: bounce 0.4s ease-out;
}

@keyframes bounce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(0.9); }
  75% { transform: scale(1.05); }
}
"""

        entrance_css = ""
        if anim.entrance_effect == "fade":
            entrance_css = """
@keyframes entrance-fade {{
  from {{ opacity: 0; }}
  to {{ opacity: 1; }}
}}

.animate-in {{
  animation: entrance-fade {duration_fast} {easing};
}}
""".format(duration_fast=anim.duration_fast, easing=anim.easing)
        elif anim.entrance_effect == "slide":
            entrance_css = """
@keyframes entrance-slide {{
  from {{
    opacity: 0;
    transform: translateY(20px);
  }}
  to {{
    opacity: 1;
    transform: translateY(0);
  }}
}}

.animate-in {{
  animation: entrance-slide {duration_normal} {easing};
}}
""".format(duration_normal=anim.duration_normal, easing=anim.easing)
        elif anim.entrance_effect == "scale":
            entrance_css = """
@keyframes entrance-scale {{
  from {{
    opacity: 0;
    transform: scale(0.9);
  }}
  to {{
    opacity: 1;
    transform: scale(1);
  }}
}}

.animate-in {{
  animation: entrance-scale {duration_fast} {easing};
}}
""".format(duration_fast=anim.duration_fast, easing=anim.easing)

        return f"""
:root {{
  --anim-duration-fast: {anim.duration_fast};
  --anim-duration-normal: {anim.duration_normal};
  --anim-duration-slow: {anim.duration_slow};
  --anim-easing: {anim.easing};
}}

* {{
  transition-duration: var(--anim-duration-fast);
  transition-timing-function: var(--anim-easing);
}}

{hover_css}

{click_css}

{entrance_css}

/* Loading states */
.loading-spinner {{
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border: 2px solid hsla(var(--primary), 0.3);
  border-top-color: hsl(var(--primary));
  border-radius: 50%;
  animation: spin {anim.duration_normal} linear infinite;
}}

@keyframes spin {{
  to {{ transform: rotate(360deg); }}
}}
"""

    def _generate_pattern_css(self) -> str:
        """Generate CSS for background patterns."""
        pattern = self.pack.pattern_style

        pattern_bg = ""
        if pattern.background_pattern == "dots":
            pattern_bg = f"""
body::before {{
  content: '';
  position: fixed;
  inset: 0;
  background-image: radial-gradient(circle, hsl(var(--foreground)) 1px, transparent 1px);
  background-size: {pattern.pattern_scale} {pattern.pattern_scale};
  opacity: {pattern.pattern_opacity};
  pointer-events: none;
  z-index: -1;
}}
"""
        elif pattern.background_pattern == "grid":
            pattern_bg = f"""
body::before {{
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(hsla(var(--foreground), {pattern.pattern_opacity}) 1px, transparent 1px),
    linear-gradient(90deg, hsla(var(--foreground), {pattern.pattern_opacity}) 1px, transparent 1px);
  background-size: {pattern.pattern_scale} {pattern.pattern_scale};
  pointer-events: none;
  z-index: -1;
}}
"""
        elif pattern.background_pattern == "noise":
            pattern_bg = f"""
body::before {{
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  opacity: {pattern.pattern_opacity};
  pointer-events: none;
  z-index: -1;
}}
"""
        elif pattern.background_pattern == "gradient":
            pattern_bg = f"""
body::before {{
  content: '';
  position: fixed;
  inset: 0;
  background: linear-gradient(135deg,
    hsla(var(--primary), {pattern.pattern_opacity}) 0%,
    hsla(var(--secondary), {pattern.pattern_opacity}) 100%);
  pointer-events: none;
  z-index: -1;
}}
"""

        surface_css = ""
        if pattern.surface_style == "glass":
            surface_css = f"""
.card, .modal, .dropdown {{
  background: hsla(var(--card), 0.8);
  backdrop-filter: blur({pattern.backdrop_blur});
  -webkit-backdrop-filter: blur({pattern.backdrop_blur});
}}
"""
        elif pattern.surface_style == "neumorphic":
            surface_css = """
.card {
  background: hsl(var(--background));
  box-shadow:
    8px 8px 16px hsla(var(--foreground), 0.1),
    -8px -8px 16px hsla(var(--background), 1);
}
"""

        return f"""
{pattern_bg}

{surface_css}
"""

    def _generate_interaction_css(self) -> str:
        """Generate CSS for user interactions."""
        interact = self.pack.interaction_style

        button_hover = ""
        if interact.button_hover == "lift":
            button_hover = "transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.1);"
        elif interact.button_hover == "scale":
            button_hover = "transform: scale(1.05);"
        elif interact.button_hover == "glow":
            button_hover = "box-shadow: 0 0 16px hsla(var(--primary), 0.5);"
        elif interact.button_hover == "darken":
            button_hover = "filter: brightness(0.9);"

        link_hover = ""
        if interact.link_hover == "underline":
            link_hover = "text-decoration: underline;"
        elif interact.link_hover == "color":
            link_hover = "color: hsl(var(--primary));"
        elif interact.link_hover == "background":
            link_hover = "background-color: hsla(var(--primary), 0.1);"

        card_hover = ""
        if interact.card_hover == "lift":
            card_hover = "transform: translateY(-4px); box-shadow: 0 8px 16px rgba(0,0,0,0.1);"
        elif interact.card_hover == "scale":
            card_hover = "transform: scale(1.02);"
        elif interact.card_hover == "border":
            card_hover = "border-color: hsl(var(--primary));"
        elif interact.card_hover == "shadow":
            card_hover = "box-shadow: 0 4px 12px rgba(0,0,0,0.1);"

        focus_css = ""
        if interact.focus_style == "ring":
            focus_css = f"""
*:focus-visible {{
  outline: none;
  box-shadow: 0 0 0 {interact.focus_ring_offset} hsl(var(--background)),
              0 0 0 calc({interact.focus_ring_offset} + {interact.focus_ring_width}) hsl(var(--ring));
}}
"""
        elif interact.focus_style == "outline":
            focus_css = f"""
*:focus-visible {{
  outline: {interact.focus_ring_width} solid hsl(var(--ring));
  outline-offset: {interact.focus_ring_offset};
}}
"""
        elif interact.focus_style == "glow":
            focus_css = """
*:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px hsla(var(--ring), 0.3);
}
"""
        elif interact.focus_style == "underline":
            focus_css = """
*:focus-visible {
  outline: none;
  text-decoration: underline;
  text-decoration-color: hsl(var(--ring));
  text-decoration-thickness: 2px;
  text-underline-offset: 4px;
}
"""

        return f"""
.btn:hover {{
  {button_hover}
}}

a:hover {{
  {link_hover}
}}

.card:hover {{
  {card_hover}
}}

{focus_css}

* {{
  cursor: {interact.cursor_style};
}}

button, a, .clickable {{
  cursor: {interact.cursor_style};
}}
"""

    def _generate_illustration_css(self) -> str:
        """Generate CSS for illustrations and images."""
        illust = self.pack.illustration_style

        filter_css = ""
        if illust.image_filter == "grayscale":
            filter_css = "filter: grayscale(100%);"
        elif illust.image_filter == "sepia":
            filter_css = "filter: sepia(60%);"
        elif illust.image_filter == "vibrant":
            filter_css = "filter: saturate(1.3) contrast(1.1);"
        elif illust.image_filter == "duotone":
            filter_css = "filter: grayscale(100%) contrast(1.2) brightness(0.9);"

        return f"""
img, .illustration {{
  border-radius: {illust.image_border_radius};
  {filter_css}
}}

.aspect-preferred {{
  aspect-ratio: {illust.preferred_aspect.replace(':', ' / ')};
}}

.illustration-{illust.illustration_type} {{
  /* Style hint for illustration type: {illust.illustration_type} */
}}
"""
