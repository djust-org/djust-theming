"""
Tailwind CSS integration for djust-theming.

Provides utilities to:
- Generate tailwind.config.js with theme CSS variable mappings
- Export presets as Tailwind color configs
- Enable @apply with theme colors
"""

from typing import Dict, Any, Optional
from .presets import THEME_PRESETS, ThemePreset, ThemeTokens


def generate_tailwind_config(
    preset_name: str = "default",
    extend_colors: bool = True,
    include_all_presets: bool = False,
) -> str:
    """
    Generate a tailwind.config.js file that uses djust-theming CSS variables.

    Args:
        preset_name: Name of the preset to use for color generation
        extend_colors: If True, extends Tailwind's default colors (recommended)
        include_all_presets: If True, includes all presets as separate color scales

    Returns:
        Complete tailwind.config.js file content as a string

    Example:
        >>> from djust_theming.tailwind import generate_tailwind_config
        >>> config = generate_tailwind_config('blue')
        >>> with open('tailwind.config.js', 'w') as f:
        ...     f.write(config)
    """
    preset = THEME_PRESETS.get(preset_name)
    if not preset:
        raise ValueError(f"Unknown preset: {preset_name}")

    # Generate color mappings for CSS variables
    colors_config = _generate_color_config(preset, extend_colors)

    # Optionally include all presets
    if include_all_presets:
        all_presets_config = _generate_all_presets_config()
        colors_config.update(all_presets_config)

    # Generate the full config
    config_content = f"""/** @type {{import('tailwindcss').Config}} */
module.exports = {{
  content: [
    './templates/**/*.html',
    './static/**/*.js',
    './**/*.py',  // For class names in Python code
  ],
  theme: {{
    {'extend: {' if extend_colors else '{'}
      colors: {{
{_format_colors_config(colors_config, indent=8)}
      }},
      borderRadius: {{
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      }},
    }},
  }},
  plugins: [],
}}
"""
    return config_content


def _generate_color_config(preset: ThemePreset, extend: bool = True) -> Dict[str, Any]:
    """Generate Tailwind color config from a preset."""
    colors = {
        "border": "hsl(var(--border))",
        "input": "hsl(var(--input))",
        "ring": "hsl(var(--ring))",
        "background": "hsl(var(--background))",
        "foreground": "hsl(var(--foreground))",
        "primary": {
            "DEFAULT": "hsl(var(--primary))",
            "foreground": "hsl(var(--primary-foreground))",
        },
        "secondary": {
            "DEFAULT": "hsl(var(--secondary))",
            "foreground": "hsl(var(--secondary-foreground))",
        },
        "destructive": {
            "DEFAULT": "hsl(var(--destructive))",
            "foreground": "hsl(var(--destructive-foreground))",
        },
        "muted": {
            "DEFAULT": "hsl(var(--muted))",
            "foreground": "hsl(var(--muted-foreground))",
        },
        "accent": {
            "DEFAULT": "hsl(var(--accent))",
            "foreground": "hsl(var(--accent-foreground))",
        },
        "popover": {
            "DEFAULT": "hsl(var(--popover))",
            "foreground": "hsl(var(--popover-foreground))",
        },
        "card": {
            "DEFAULT": "hsl(var(--card))",
            "foreground": "hsl(var(--card-foreground))",
        },
        "success": {
            "DEFAULT": "hsl(var(--success))",
            "foreground": "hsl(var(--success-foreground))",
        },
        "warning": {
            "DEFAULT": "hsl(var(--warning))",
            "foreground": "hsl(var(--warning-foreground))",
        },
    }

    return colors


def _generate_all_presets_config() -> Dict[str, Any]:
    """Generate Tailwind configs for all presets with preset-prefixed names."""
    all_configs = {}

    for name, preset in THEME_PRESETS.items():
        # Create direct color values for each preset (not CSS variables)
        # These are useful for static generation or preset-specific colors
        all_configs[f"preset-{name}"] = {
            "primary": preset.light.primary.to_hsl_func(),
            "secondary": preset.light.secondary.to_hsl_func(),
            "accent": preset.light.accent.to_hsl_func(),
            "muted": preset.light.muted.to_hsl_func(),
        }

    return all_configs


def _format_colors_config(colors: Dict[str, Any], indent: int = 8) -> str:
    """Format the colors config dict as JavaScript object notation."""
    lines = []
    indent_str = " " * indent

    for key, value in colors.items():
        if isinstance(value, dict):
            lines.append(f"{indent_str}{key}: {{")
            for sub_key, sub_value in value.items():
                # Handle DEFAULT specially (no quotes needed)
                if sub_key == "DEFAULT":
                    lines.append(f"{indent_str}  DEFAULT: '{sub_value}',")
                else:
                    lines.append(f"{indent_str}  {sub_key}: '{sub_value}',")
            lines.append(f"{indent_str}}},")
        else:
            lines.append(f"{indent_str}{key}: '{value}',")

    return "\n".join(lines)


def export_preset_as_tailwind_colors(preset_name: str = "default") -> Dict[str, str]:
    """
    Export a preset's colors in Tailwind-compatible format.

    This generates static color values (not CSS variables) that can be
    used directly in Tailwind config or for generating color palettes.

    Args:
        preset_name: Name of the preset to export

    Returns:
        Dictionary of color names to HSL values

    Example:
        >>> from djust_theming.tailwind import export_preset_as_tailwind_colors
        >>> colors = export_preset_as_tailwind_colors('blue')
        >>> colors['primary']
        'hsl(221, 83%, 53%)'
    """
    preset = THEME_PRESETS.get(preset_name)
    if not preset:
        raise ValueError(f"Unknown preset: {preset_name}")

    light = preset.light
    dark = preset.dark

    return {
        # Light mode colors
        "light-background": light.background.to_hsl_func(),
        "light-foreground": light.foreground.to_hsl_func(),
        "light-primary": light.primary.to_hsl_func(),
        "light-primary-foreground": light.primary_foreground.to_hsl_func(),
        "light-secondary": light.secondary.to_hsl_func(),
        "light-muted": light.muted.to_hsl_func(),
        "light-accent": light.accent.to_hsl_func(),
        "light-destructive": light.destructive.to_hsl_func(),
        "light-border": light.border.to_hsl_func(),
        # Dark mode colors
        "dark-background": dark.background.to_hsl_func(),
        "dark-foreground": dark.foreground.to_hsl_func(),
        "dark-primary": dark.primary.to_hsl_func(),
        "dark-primary-foreground": dark.primary_foreground.to_hsl_func(),
        "dark-secondary": dark.secondary.to_hsl_func(),
        "dark-muted": dark.muted.to_hsl_func(),
        "dark-accent": dark.accent.to_hsl_func(),
        "dark-destructive": dark.destructive.to_hsl_func(),
        "dark-border": dark.border.to_hsl_func(),
    }


def generate_tailwind_apply_examples() -> str:
    """
    Generate example CSS showing how to use @apply with theme colors.

    Returns:
        CSS code with @apply examples

    Example:
        >>> from djust_theming.tailwind import generate_tailwind_apply_examples
        >>> print(generate_tailwind_apply_examples())
    """
    return """/* Using @apply with djust-theming colors */

/* Button styles */
.btn-primary {
  @apply bg-primary text-primary-foreground px-4 py-2 rounded-md;
  @apply hover:opacity-90 transition-opacity;
}

.btn-secondary {
  @apply bg-secondary text-secondary-foreground px-4 py-2 rounded-md;
  @apply hover:bg-secondary/80;
}

.btn-destructive {
  @apply bg-destructive text-destructive-foreground px-4 py-2 rounded-md;
  @apply hover:bg-destructive/90;
}

/* Card styles */
.card {
  @apply bg-card text-card-foreground rounded-lg border border-border;
  @apply shadow-sm p-6;
}

/* Input styles */
.input {
  @apply bg-background border border-input rounded-md px-3 py-2;
  @apply text-foreground placeholder:text-muted-foreground;
  @apply focus:outline-none focus:ring-2 focus:ring-ring;
}

/* Muted text */
.text-muted {
  @apply text-muted-foreground;
}

/* Alert variants */
.alert-success {
  @apply bg-success/10 text-success border border-success/20;
  @apply rounded-md p-4;
}

.alert-warning {
  @apply bg-warning/10 text-warning border border-warning/20;
  @apply rounded-md p-4;
}

.alert-destructive {
  @apply bg-destructive/10 text-destructive border border-destructive/20;
  @apply rounded-md p-4;
}
"""
