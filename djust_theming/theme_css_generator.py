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

from .themes import Theme, get_theme
from .css_generator import ThemeCSSGenerator as ColorCSSGenerator


class CompleteThemeCSSGenerator:
    """Generate complete theme CSS including colors, typography, spacing, etc."""

    def __init__(self, theme_name: str = "material", color_preset: str = None):
        """
        Initialize complete theme CSS generator.

        Args:
            theme_name: Name of the theme (material, ios, fluent, etc.)
            color_preset: Override color preset (default uses theme's preset)
        """
        self.theme = get_theme(theme_name)
        if not self.theme:
            raise ValueError(f"Theme '{theme_name}' not found")

        # Use provided color preset or theme's default
        self.color_preset = color_preset or self.theme.color_preset

        # Initialize color generator
        self.color_generator = ColorCSSGenerator(preset_name=self.color_preset)

    def generate_css(self) -> str:
        """Generate complete CSS for the theme."""
        # Get full color CSS with light/dark modes
        color_css = self.color_generator.generate_css()

        parts = [
            "/* djust-theming - Complete Theme CSS */",
            "",
            color_css,  # Full color CSS including light/dark modes
            "",
            self._generate_theme_vars(),  # Theme-specific vars (typography, spacing, etc.)
            "",
            self._generate_typography_classes(),
            "",
            self._generate_component_styles(),
        ]
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
body {
  font-family: var(--font-sans);
  font-size: var(--text-base);
  line-height: var(--leading-normal);
}

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

        parts = ["/* Component Styles */"]

        # Button styles based on theme
        if styles.button_style == "solid":
            parts.append("""
.btn {
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  transition: all var(--duration-normal) var(--ease-out);
}
.btn:hover {
  box-shadow: var(--shadow);
  transform: translateY(-1px);
}""")
        elif styles.button_style == "outlined":
            parts.append("""
.btn {
  border-radius: var(--radius);
  border: 2px solid currentColor;
  background: transparent;
  transition: all var(--duration-fast) var(--ease-out);
}
.btn:hover {
  background: currentColor;
  color: var(--background);
}""")
        elif styles.button_style == "ghost":
            parts.append("""
.btn {
  border-radius: var(--radius);
  background: transparent;
  transition: background var(--duration-fast) var(--ease-out);
}
.btn:hover {
  background: hsl(var(--accent) / 0.1);
}""")

        # Card styles
        if styles.card_style == "elevated":
            parts.append("""
.card {
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow);
  transition: box-shadow var(--duration-normal) var(--ease-out);
}
.card:hover {
  box-shadow: var(--shadow-lg);
}""")
        elif styles.card_style == "outlined":
            parts.append("""
.card {
  border-radius: var(--radius-md);
  border: 1px solid hsl(var(--border));
  box-shadow: none;
}""")
        elif styles.card_style == "flat":
            parts.append("""
.card {
  border-radius: var(--radius-sm);
  background: hsl(var(--muted) / 0.3);
  box-shadow: none;
}""")

        # Input styles
        if styles.input_style == "outlined":
            parts.append("""
.form-input {
  border-radius: var(--radius);
  border: 2px solid hsl(var(--input));
  background: transparent;
  transition: border-color var(--duration-fast) var(--ease-out);
}
.form-input:focus {
  border-color: hsl(var(--ring));
  outline: none;
}""")
        elif styles.input_style == "filled":
            parts.append("""
.form-input {
  border-radius: var(--radius) var(--radius) 0 0;
  border: none;
  border-bottom: 2px solid hsl(var(--input));
  background: hsl(var(--muted) / 0.5);
  transition: all var(--duration-fast) var(--ease-out);
}
.form-input:focus {
  border-bottom-color: hsl(var(--ring));
  background: hsl(var(--muted) / 0.7);
  outline: none;
}""")
        elif styles.input_style == "underlined":
            parts.append("""
.form-input {
  border-radius: 0;
  border: none;
  border-bottom: 1px solid hsl(var(--input));
  background: transparent;
  transition: border-color var(--duration-fast) var(--ease-out);
}
.form-input:focus {
  border-bottom-width: 2px;
  border-bottom-color: hsl(var(--ring));
  outline: none;
}""")

        return "\n".join(parts)


def generate_theme_css(theme_name: str, color_preset: str = None) -> str:
    """
    Generate complete CSS for a theme.

    Args:
        theme_name: Name of the theme (material, ios, fluent, etc.)
        color_preset: Optional color preset override

    Returns:
        Complete CSS string for the theme
    """
    generator = CompleteThemeCSSGenerator(theme_name, color_preset)
    return generator.generate_css()
