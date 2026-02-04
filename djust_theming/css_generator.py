"""
CSS generator for theme presets.

Generates CSS custom properties from theme tokens, supporting both
light and dark modes with system preference detection.
"""

from .presets import ThemeTokens, get_preset


class ThemeCSSGenerator:
    """Generate CSS from theme tokens."""

    def __init__(
        self,
        preset_name: str = "default",
        custom_tokens: dict | None = None,
        include_base_styles: bool = True,
        include_utilities: bool = True,
    ):
        """
        Initialize CSS generator.

        Args:
            preset_name: Name of the theme preset to use
            custom_tokens: Optional dict of token overrides
            include_base_styles: Include base body/element styles
            include_utilities: Include utility classes
        """
        self.preset = get_preset(preset_name)
        self.custom_tokens = custom_tokens or {}
        self.include_base_styles = include_base_styles
        self.include_utilities = include_utilities

    def _tokens_to_css_vars(self, tokens: ThemeTokens, indent: str = "  ") -> str:
        """Convert ThemeTokens to CSS custom property declarations."""
        lines = []

        # Color tokens
        color_mappings = [
            ("background", tokens.background),
            ("foreground", tokens.foreground),
            ("card", tokens.card),
            ("card-foreground", tokens.card_foreground),
            ("popover", tokens.popover),
            ("popover-foreground", tokens.popover_foreground),
            ("primary", tokens.primary),
            ("primary-foreground", tokens.primary_foreground),
            ("secondary", tokens.secondary),
            ("secondary-foreground", tokens.secondary_foreground),
            ("muted", tokens.muted),
            ("muted-foreground", tokens.muted_foreground),
            ("accent", tokens.accent),
            ("accent-foreground", tokens.accent_foreground),
            ("destructive", tokens.destructive),
            ("destructive-foreground", tokens.destructive_foreground),
            ("success", tokens.success),
            ("success-foreground", tokens.success_foreground),
            ("warning", tokens.warning),
            ("warning-foreground", tokens.warning_foreground),
            ("border", tokens.border),
            ("input", tokens.input),
            ("ring", tokens.ring),
        ]

        for name, color in color_mappings:
            lines.append(f"{indent}--{name}: {color.to_hsl()};")

        # shadcn/ui compatibility aliases (extended tokens)
        shadcn_mappings = [
            ("sidebar-background", tokens.background),
            ("sidebar-foreground", tokens.foreground),
            ("sidebar-primary", tokens.primary),
            ("sidebar-primary-foreground", tokens.primary_foreground),
            ("sidebar-accent", tokens.accent),
            ("sidebar-accent-foreground", tokens.accent_foreground),
            ("sidebar-border", tokens.border),
            ("sidebar-ring", tokens.ring),
            ("chart-1", tokens.primary),
            ("chart-2", tokens.secondary),
            ("chart-3", tokens.accent),
            ("chart-4", tokens.success),
            ("chart-5", tokens.warning),
        ]

        for name, color in shadcn_mappings:
            lines.append(f"{indent}--{name}: {color.to_hsl()};")

        # Radius
        lines.append(f"{indent}--radius: {tokens.radius}rem;")

        return "\n".join(lines)

    def _generate_light_mode(self) -> str:
        """Generate :root light mode variables."""
        return f""":root {{
{self._tokens_to_css_vars(self.preset.light)}
}}"""

    def _generate_dark_mode(self) -> str:
        """Generate dark mode variables for explicit .dark class and data attribute."""
        return f""".dark,
[data-theme="dark"] {{
{self._tokens_to_css_vars(self.preset.dark)}
}}"""

    def _generate_system_preference(self) -> str:
        """Generate system preference media query for auto dark mode."""
        return f"""@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
{self._tokens_to_css_vars(self.preset.dark, indent="    ")}
  }}
}}"""

    def _generate_base_styles(self) -> str:
        """Generate base element styles using CSS variables."""
        return """/* Base styles */
* {
  border-color: hsl(var(--border));
}

body {
  background-color: hsl(var(--background));
  color: hsl(var(--foreground));
  font-feature-settings: "rlig" 1, "calt" 1;
}

/* Smooth theme transitions */
*,
*::before,
*::after {
  transition: background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease;
}

/* Reduce motion for users who prefer it */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    transition: none;
  }
}"""

    def _generate_utilities(self) -> str:
        """Generate utility classes for theme colors."""
        return """/* Theme utility classes */

/* Backgrounds */
.bg-background { background-color: hsl(var(--background)); }
.bg-foreground { background-color: hsl(var(--foreground)); }
.bg-card { background-color: hsl(var(--card)); }
.bg-popover { background-color: hsl(var(--popover)); }
.bg-primary { background-color: hsl(var(--primary)); }
.bg-secondary { background-color: hsl(var(--secondary)); }
.bg-muted { background-color: hsl(var(--muted)); }
.bg-accent { background-color: hsl(var(--accent)); }
.bg-destructive { background-color: hsl(var(--destructive)); }
.bg-success { background-color: hsl(var(--success)); }
.bg-warning { background-color: hsl(var(--warning)); }

/* Text colors */
.text-foreground { color: hsl(var(--foreground)); }
.text-card-foreground { color: hsl(var(--card-foreground)); }
.text-popover-foreground { color: hsl(var(--popover-foreground)); }
.text-primary { color: hsl(var(--primary)); }
.text-primary-foreground { color: hsl(var(--primary-foreground)); }
.text-secondary-foreground { color: hsl(var(--secondary-foreground)); }
.text-muted-foreground { color: hsl(var(--muted-foreground)); }
.text-accent-foreground { color: hsl(var(--accent-foreground)); }
.text-destructive { color: hsl(var(--destructive)); }
.text-destructive-foreground { color: hsl(var(--destructive-foreground)); }
.text-success { color: hsl(var(--success)); }
.text-success-foreground { color: hsl(var(--success-foreground)); }
.text-warning { color: hsl(var(--warning)); }
.text-warning-foreground { color: hsl(var(--warning-foreground)); }

/* Borders */
.border-border { border-color: hsl(var(--border)); }
.border-input { border-color: hsl(var(--input)); }
.border-primary { border-color: hsl(var(--primary)); }
.border-secondary { border-color: hsl(var(--secondary)); }
.border-destructive { border-color: hsl(var(--destructive)); }
.border-success { border-color: hsl(var(--success)); }
.border-warning { border-color: hsl(var(--warning)); }

/* Ring (focus) */
.ring-ring { --tw-ring-color: hsl(var(--ring)); }

/* Rounded corners using theme radius */
.rounded-theme { border-radius: var(--radius); }
.rounded-theme-sm { border-radius: calc(var(--radius) - 0.25rem); }
.rounded-theme-md { border-radius: calc(var(--radius) + 0.25rem); }
.rounded-theme-lg { border-radius: calc(var(--radius) + 0.5rem); }

/* Common component patterns */
.card-theme {
  background-color: hsl(var(--card));
  color: hsl(var(--card-foreground));
  border: 1px solid hsl(var(--border));
  border-radius: var(--radius);
}

.btn-primary {
  background-color: hsl(var(--primary));
  color: hsl(var(--primary-foreground));
  border-radius: var(--radius);
}

.btn-primary:hover {
  background-color: hsl(var(--primary) / 0.9);
}

.btn-secondary {
  background-color: hsl(var(--secondary));
  color: hsl(var(--secondary-foreground));
  border-radius: var(--radius);
}

.btn-secondary:hover {
  background-color: hsl(var(--secondary) / 0.8);
}

.btn-destructive {
  background-color: hsl(var(--destructive));
  color: hsl(var(--destructive-foreground));
  border-radius: var(--radius);
}

.btn-destructive:hover {
  background-color: hsl(var(--destructive) / 0.9);
}

.input-theme {
  background-color: transparent;
  border: 1px solid hsl(var(--input));
  border-radius: var(--radius);
}

.input-theme:focus {
  outline: none;
  box-shadow: 0 0 0 2px hsl(var(--ring) / 0.5);
}

/* Badge variants */
.badge-primary {
  background-color: hsl(var(--primary));
  color: hsl(var(--primary-foreground));
}

.badge-secondary {
  background-color: hsl(var(--secondary));
  color: hsl(var(--secondary-foreground));
}

.badge-destructive {
  background-color: hsl(var(--destructive));
  color: hsl(var(--destructive-foreground));
}

.badge-success {
  background-color: hsl(var(--success));
  color: hsl(var(--success-foreground));
}

.badge-warning {
  background-color: hsl(var(--warning));
  color: hsl(var(--warning-foreground));
}"""

    def generate_css(self) -> str:
        """Generate complete CSS for the theme."""
        sections = [
            "/* djust_theming - Auto-generated CSS */",
            "",
            self._generate_light_mode(),
            "",
            self._generate_dark_mode(),
            "",
            self._generate_system_preference(),
        ]

        if self.include_base_styles:
            sections.extend(["", self._generate_base_styles()])

        if self.include_utilities:
            sections.extend(["", self._generate_utilities()])

        return "\n".join(sections)

    def generate_variables_only(self) -> str:
        """Generate only the CSS custom property declarations."""
        sections = [
            self._generate_light_mode(),
            "",
            self._generate_dark_mode(),
            "",
            self._generate_system_preference(),
        ]
        return "\n".join(sections)

    def generate_for_preset(self, preset_name: str) -> str:
        """Generate CSS for a specific preset."""
        old_preset = self.preset
        self.preset = get_preset(preset_name)
        css = self.generate_css()
        self.preset = old_preset
        return css


def generate_theme_css(
    preset_name: str = "default",
    include_base_styles: bool = True,
    include_utilities: bool = True,
) -> str:
    """
    Convenience function to generate CSS for a theme.

    Args:
        preset_name: Name of the theme preset
        include_base_styles: Include base body/element styles
        include_utilities: Include utility classes

    Returns:
        Complete CSS string
    """
    generator = ThemeCSSGenerator(
        preset_name=preset_name,
        include_base_styles=include_base_styles,
        include_utilities=include_utilities,
    )
    return generator.generate_css()
