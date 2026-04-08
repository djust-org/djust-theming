"""
CSS generator for complete themes.

Generates CSS custom properties for all aspects of a theme:
- Typography
- Spacing
- Border radius
- Shadows
- Animations
- Component styles
"""

from functools import lru_cache

from .manager import get_theme_config
from .themes import Theme, get_theme
from .css_generator import ThemeCSSGenerator as ColorCSSGenerator


class CompleteThemeCSSGenerator:
    """Generate complete theme CSS including colors, typography, spacing, etc."""

    def __init__(self, theme_name: str = "material", color_preset: str = None, css_prefix: str = ""):
        """
        Initialize complete theme CSS generator.

        Args:
            theme_name: Name of the theme (material, ios, fluent, etc.)
            color_preset: Override color preset (default uses theme's preset)
            css_prefix: Namespace prefix for component CSS classes (e.g. "dj-")
        """
        self.theme = get_theme(theme_name)
        if not self.theme:
            raise ValueError(f"Theme '{theme_name}' not found")

        # Use provided color preset or theme's default
        self.color_preset = color_preset or self.theme.color_preset
        self.css_prefix = css_prefix

        # Initialize color generator
        self.color_generator = ColorCSSGenerator(preset_name=self.color_preset)

    def generate_css(self) -> str:
        """Generate complete CSS for the theme.

        Produces a single @layer tokens block containing both color tokens
        and theme vars, avoiding duplicate layer declarations.
        """
        config = get_theme_config()
        use_layers = config.get("use_css_layers", True)
        layer_order = config.get("css_layer_order", "base, tokens, components, theme")

        # Build raw color token parts (unwrapped — we'll wrap once)
        color_parts = [
            self.color_generator._generate_light_mode(),
            "",
            self.color_generator._generate_dark_mode(),
            "",
            self.color_generator._generate_system_preference(),
        ]

        if self.color_generator.include_design_tokens:
            from .design_tokens import generate_design_tokens_css
            color_parts.extend(["", "", generate_design_tokens_css()])

        color_tokens_css = "\n".join(color_parts)

        theme_vars = self._generate_theme_vars()
        typography_css = self._generate_typography_classes()
        component_css = self._generate_component_styles()

        base_css = self.color_generator._generate_base_styles() if self.color_generator.include_base_styles else ""
        utilities_css = self.color_generator._generate_utilities() if self.color_generator.include_utilities else ""
        surface_css = self.color_generator._generate_surface_styles()

        parts = [
            "/* djust-theming - Complete Theme CSS */",
            "",
        ]

        if use_layers:
            parts.append(f"@layer {layer_order};")
            parts.append("")
            # Color tokens go in @layer tokens (light, dark, system preference)
            parts.append(f"@layer tokens {{\n{color_tokens_css}\n}}")
            # Design system theme vars (font, shadow, spacing, radius, duration)
            # emitted OUTSIDE @layer so they override base.css static defaults
            parts.extend(["", theme_vars])
            if base_css:
                parts.extend(["", f"@layer base {{\n{base_css}\n}}"])
            if utilities_css:
                parts.extend(["", f"@layer components {{\n{utilities_css}\n}}"])
            if surface_css:
                parts.extend(["", f"@layer components {{\n{surface_css}\n}}"])
            parts.extend([
                "",
                f"@layer components {{\n{typography_css}\n}}",
                "",
                f"@layer components {{\n{component_css}\n}}",
            ])
        else:
            all_tokens = color_tokens_css + "\n\n" + theme_vars
            parts.append(all_tokens)
            if base_css:
                parts.extend(["", base_css])
            if utilities_css:
                parts.extend(["", utilities_css])
            if surface_css:
                parts.extend(["", surface_css])
            parts.extend([
                "",
                typography_css,
                "",
                component_css,
            ])

        return "\n".join(parts)

    def generate_critical_css(self) -> str:
        """Generate critical CSS for inline delivery.

        Includes color tokens (from ColorCSSGenerator) and theme-specific
        :root variables (typography, spacing, shadows, etc.). These are
        needed for first paint to avoid FOUC.

        Produces a single @layer tokens block containing both color tokens
        and theme vars, avoiding duplicate layer declarations.

        Returns:
            CSS string suitable for inlining in a <style> tag.
        """
        config = get_theme_config()
        use_layers = config.get("use_css_layers", True)
        layer_order = config.get("css_layer_order", "base, tokens, components, theme")

        # Build raw color token CSS (light/dark/system + design token root vars)
        color_parts = [
            self.color_generator._generate_light_mode(),
            "",
            self.color_generator._generate_dark_mode(),
            "",
            self.color_generator._generate_system_preference(),
        ]

        if self.color_generator.include_design_tokens:
            from .design_tokens import generate_design_tokens_root_css
            color_parts.extend(["", "", generate_design_tokens_root_css()])

        # Theme vars (:root with typography, spacing, shadows, etc.)
        theme_vars = self._generate_theme_vars()

        # Base element styles (body bg/color, * border-color, transitions)
        # Must be in critical CSS to prevent layout shift when deferred CSS loads.
        base_css = self.color_generator._generate_base_styles() if self.color_generator.include_base_styles else ""

        # Combine all token CSS
        all_tokens = "\n".join(color_parts) + "\n\n" + theme_vars

        parts = [
            "/* djust-theming - Critical CSS (inline) */",
            "",
            # CSS variables are NOT wrapped in @layer — they must have
            # highest priority since all other styles depend on them.
            all_tokens,
        ]

        if base_css:
            parts.extend(["", base_css])

        return "\n".join(parts)

    def generate_deferred_css(self) -> str:
        """Generate deferred CSS for async loading.

        Includes base styles, utility classes, design token classes,
        typography classes, and component styles. Not needed for first paint.

        Returns:
            CSS string suitable for serving from a <link> tag.
        """
        config = get_theme_config()
        use_layers = config.get("use_css_layers", True)

        # Build deferred parts directly (avoiding duplicate comment headers)
        # Note: base_css (body/border-color/transitions) is now in critical CSS
        utilities_css = self.color_generator._generate_utilities() if self.color_generator.include_utilities else ""

        # Design token classes (typography hierarchy, interactive, layout, animations)
        design_classes = ""
        if self.color_generator.include_design_tokens:
            from .design_tokens import generate_design_tokens_classes_css
            design_classes = generate_design_tokens_classes_css()

        typography_css = self._generate_typography_classes()
        component_css = self._generate_component_styles()

        parts = [
            "/* djust-theming - Deferred CSS */",
        ]

        if use_layers:
            if utilities_css:
                parts.extend(["", f"@layer components {{\n{utilities_css}\n}}"])
            if design_classes:
                parts.extend(["", f"@layer components {{\n{design_classes}\n}}"])
            parts.extend([
                "",
                f"@layer components {{\n{typography_css}\n}}",
                "",
                f"@layer components {{\n{component_css}\n}}",
            ])
        else:
            if utilities_css:
                parts.extend(["", utilities_css])
            if design_classes:
                parts.extend(["", design_classes])
            parts.extend([
                "",
                typography_css,
                "",
                component_css,
            ])

        return "\n".join(parts)

    def _generate_theme_vars(self) -> str:
        """Generate theme-specific CSS custom properties (typography, spacing, etc.)."""
        theme = self.theme

        parts = [
            ":root {",
            "  /* ========================================",
            f"     Theme: {theme.display_name}",
            f"     {theme.description}",
            "     ======================================== */",
            "",
        ]

        # Typography
        parts.extend([
            "  /* Typography */",
            f"  --font-sans: {theme.typography.font_sans};",
            f"  --font-mono: {theme.typography.font_mono};",
        ])
        if theme.typography.font_display:
            parts.append(f"  --font-display: {theme.typography.font_display};")

        parts.extend([
            "",
            "  /* Font Sizes */",
            f"  --text-xs: {theme.typography.text_xs};",
            f"  --text-sm: {theme.typography.text_sm};",
            f"  --text-base: {theme.typography.text_base};",
            f"  --text-lg: {theme.typography.text_lg};",
            f"  --text-xl: {theme.typography.text_xl};",
            f"  --text-2xl: {theme.typography.text_2xl};",
            f"  --text-3xl: {theme.typography.text_3xl};",
            f"  --text-4xl: {theme.typography.text_4xl};",
            f"  --text-5xl: {theme.typography.text_5xl};",
            "",
            "  /* Font Weights */",
            f"  --font-normal: {theme.typography.font_normal};",
            f"  --font-medium: {theme.typography.font_medium};",
            f"  --font-semibold: {theme.typography.font_semibold};",
            f"  --font-bold: {theme.typography.font_bold};",
            "",
            "  /* Line Heights */",
            f"  --leading-tight: {theme.typography.leading_tight};",
            f"  --leading-normal: {theme.typography.leading_normal};",
            f"  --leading-relaxed: {theme.typography.leading_relaxed};",
        ])

        if hasattr(theme.typography, 'leading_loose'):
            parts.append(f"  --leading-loose: {theme.typography.leading_loose};")

        # Spacing
        base = theme.spacing.base
        parts.extend([
            "",
            "  /* Spacing */",
            f"  --space-base: {base}rem;",
            f"  --space-0: 0;",
            f"  --space-1: {base * theme.spacing.space_1}rem;",
            f"  --space-2: {base * theme.spacing.space_2}rem;",
            f"  --space-3: {base * theme.spacing.space_3}rem;",
            f"  --space-4: {base * theme.spacing.space_4}rem;",
            f"  --space-5: {base * theme.spacing.space_5}rem;",
            f"  --space-6: {base * theme.spacing.space_6}rem;",
            f"  --space-8: {base * theme.spacing.space_8}rem;",
            f"  --space-10: {base * theme.spacing.space_10}rem;",
            f"  --space-12: {base * theme.spacing.space_12}rem;",
            f"  --space-16: {base * theme.spacing.space_16}rem;",
            f"  --space-20: {base * theme.spacing.space_20}rem;",
            f"  --space-24: {base * theme.spacing.space_24}rem;",
        ])

        # Border Radius
        parts.extend([
            "",
            "  /* Border Radius */",
            f"  --radius-sm: {theme.border_radius.radius_sm};",
            f"  --radius: {theme.border_radius.radius};",
            f"  --radius-md: {theme.border_radius.radius_md};",
            f"  --radius-lg: {theme.border_radius.radius_lg};",
            f"  --radius-xl: {theme.border_radius.radius_xl};",
            f"  --radius-2xl: {theme.border_radius.radius_2xl};",
            f"  --radius-3xl: {theme.border_radius.radius_3xl};",
            f"  --radius-full: {theme.border_radius.radius_full};",
        ])

        # Shadows
        parts.extend([
            "",
            "  /* Shadows */",
            f"  --shadow-xs: {theme.shadows.shadow_xs};",
            f"  --shadow-sm: {theme.shadows.shadow_sm};",
            f"  --shadow: {theme.shadows.shadow};",
            f"  --shadow-md: {theme.shadows.shadow_md};",
            f"  --shadow-lg: {theme.shadows.shadow_lg};",
            f"  --shadow-xl: {theme.shadows.shadow_xl};",
            f"  --shadow-2xl: {theme.shadows.shadow_2xl};",
            f"  --shadow-inner: {theme.shadows.shadow_inner};",
        ])

        # Animations
        parts.extend([
            "",
            "  /* Animations */",
            f"  --duration-fast: {theme.animations.duration_fast};",
            f"  --duration-normal: {theme.animations.duration_normal};",
            f"  --duration-slow: {theme.animations.duration_slow};",
            f"  --ease-in: {theme.animations.ease_in};",
            f"  --ease-out: {theme.animations.ease_out};",
            f"  --ease-in-out: {theme.animations.ease_in_out};",
        ])

        if hasattr(theme.animations, 'ease_bounce'):
            parts.append(f"  --ease-bounce: {theme.animations.ease_bounce};")

        parts.append("}")

        return "\n".join(parts)

    def _generate_typography_classes(self) -> str:
        """Generate utility classes for typography."""
        return """/* Typography Utilities */
/* Note: body font-family/size/line-height is set in critical CSS base styles
   to prevent layout shift when deferred CSS loads. */

.font-sans { font-family: var(--font-sans); }
.font-mono { font-family: var(--font-mono); }
.font-display { font-family: var(--font-display, var(--font-sans)); }

.text-xs { font-size: var(--text-xs); }
.text-sm { font-size: var(--text-sm); }
.text-base { font-size: var(--text-base); }
.text-lg { font-size: var(--text-lg); }
.text-xl { font-size: var(--text-xl); }
.text-2xl { font-size: var(--text-2xl); }
.text-3xl { font-size: var(--text-3xl); }
.text-4xl { font-size: var(--text-4xl); }
.text-5xl { font-size: var(--text-5xl); }

.font-normal { font-weight: var(--font-normal); }
.font-medium { font-weight: var(--font-medium); }
.font-semibold { font-weight: var(--font-semibold); }
.font-bold { font-weight: var(--font-bold); }

.leading-tight { line-height: var(--leading-tight); }
.leading-normal { line-height: var(--leading-normal); }
.leading-relaxed { line-height: var(--leading-relaxed); }"""

    def _generate_component_styles(self) -> str:
        """Generate component styles based on theme."""
        theme = self.theme
        styles = theme.component_styles
        p = self.css_prefix  # shorthand for prefix

        parts = ["/* Component Styles */"]

        # Button styles based on theme
        if styles.button_style == "solid":
            parts.append(f"""
.{p}btn {{
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  transition: all var(--duration-normal) var(--ease-out);
}}
.{p}btn:hover {{
  box-shadow: var(--shadow);
  transform: translateY(-1px);
}}""")
        elif styles.button_style == "outlined":
            parts.append(f"""
.{p}btn {{
  border-radius: var(--radius);
  border: 2px solid currentColor;
  background: transparent;
  transition: all var(--duration-fast) var(--ease-out);
}}
.{p}btn:hover {{
  background: currentColor;
  color: var(--background);
}}""")
        elif styles.button_style == "ghost":
            parts.append(f"""
.{p}btn {{
  border-radius: var(--radius);
  background: transparent;
  transition: background var(--duration-fast) var(--ease-out);
}}
.{p}btn:hover {{
  background: hsl(var(--accent) / 0.1);
}}""")

        # Card styles
        if styles.card_style == "elevated":
            parts.append(f"""
.{p}card {{
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  transition: box-shadow var(--duration-normal) var(--ease-out);
}}
.{p}card:hover {{
  box-shadow: var(--shadow-lg);
}}""")
        elif styles.card_style == "outlined":
            parts.append(f"""
.{p}card {{
  border-radius: var(--radius-md);
  border: 1px solid hsl(var(--border));
  box-shadow: none;
}}""")
        elif styles.card_style == "flat":
            parts.append(f"""
.{p}card {{
  border-radius: var(--radius-sm);
  background: hsl(var(--muted) / 0.3);
  box-shadow: none;
}}""")

        # Input styles
        if styles.input_style == "outlined":
            parts.append(f"""
.{p}form-input {{
  border-radius: var(--radius);
  border: 2px solid hsl(var(--input));
  background: transparent;
  transition: border-color var(--duration-fast) var(--ease-out);
}}
.{p}form-input:focus {{
  border-color: hsl(var(--ring));
  outline: none;
}}""")
        elif styles.input_style == "filled":
            parts.append(f"""
.{p}form-input {{
  border-radius: var(--radius) var(--radius) 0 0;
  border: none;
  border-bottom: 2px solid hsl(var(--input));
  background: hsl(var(--muted) / 0.5);
  transition: all var(--duration-fast) var(--ease-out);
}}
.{p}form-input:focus {{
  border-bottom-color: hsl(var(--ring));
  background: hsl(var(--muted) / 0.7);
  outline: none;
}}""")
        elif styles.input_style == "underlined":
            parts.append(f"""
.{p}form-input {{
  border-radius: 0;
  border: none;
  border-bottom: 1px solid hsl(var(--input));
  background: transparent;
  transition: border-color var(--duration-fast) var(--ease-out);
}}
.{p}form-input:focus {{
  border-bottom-width: 2px;
  border-bottom-color: hsl(var(--ring));
  outline: none;
}}""")

        return "\n".join(parts)


@lru_cache(maxsize=256)
def generate_theme_css(theme_name: str, color_preset: str = None, css_prefix: str = "") -> str:
    """
    Generate complete CSS for a theme (cached).

    Results are cached by (theme_name, color_preset, css_prefix). Use
    ``clear_css_cache()`` to invalidate during development.

    Args:
        theme_name: Name of the theme (material, ios, fluent, etc.)
        color_preset: Optional color preset override
        css_prefix: CSS class prefix for component styles (e.g. "dj-")

    Returns:
        Complete CSS string for the theme
    """
    # Normalize None preset to the theme's default so that
    # generate_theme_css("material") and generate_theme_css("material", "default")
    # share the same cache entry.
    if color_preset is None:
        theme = get_theme(theme_name)
        if theme:
            color_preset = theme.color_preset

    generator = CompleteThemeCSSGenerator(theme_name, color_preset, css_prefix=css_prefix)
    return generator.generate_css()
