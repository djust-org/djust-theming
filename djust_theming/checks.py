"""Django system checks for djust-theming accessibility validation."""

from django.core.checks import Warning, register, Tags

from .presets import THEME_PRESETS
from .accessibility import AccessibilityValidator


# Foreground/background pairs to check (attr_fg, attr_bg, label)
CONTRAST_PAIRS = [
    ("foreground", "background", "text on background"),
    ("card_foreground", "card", "text on card"),
    ("primary_foreground", "primary", "text on primary"),
    ("secondary_foreground", "secondary", "text on secondary"),
    ("muted_foreground", "muted", "text on muted"),
    ("accent_foreground", "accent", "text on accent"),
    ("destructive_foreground", "destructive", "text on destructive"),
    ("success_foreground", "success", "text on success"),
    ("warning_foreground", "warning", "text on warning"),
    ("info_foreground", "info", "text on info"),
    ("popover_foreground", "popover", "text on popover"),
    ("code_foreground", "code", "text on code"),
]


@register(Tags.compatibility)
def check_preset_contrast(app_configs, **kwargs):
    """Validate all registered theme presets meet WCAG AA contrast ratios."""
    warnings = []
    validator = AccessibilityValidator()

    for preset_name, preset in THEME_PRESETS.items():
        for mode_name in ("light", "dark"):
            tokens = getattr(preset, mode_name)
            for fg_attr, bg_attr, label in CONTRAST_PAIRS:
                fg = getattr(tokens, fg_attr)
                bg = getattr(tokens, bg_attr)
                ratio = validator.calculate_contrast_ratio(fg, bg)
                if ratio < validator.AA_NORMAL:
                    warnings.append(
                        Warning(
                            f'Preset "{preset_name}" {mode_name} mode: {label} '
                            f"contrast ratio {ratio:.2f}:1 < {validator.AA_NORMAL}:1 (WCAG AA)",
                            hint=f"Adjust {fg_attr} or {bg_attr} to achieve at least "
                            f"{validator.AA_NORMAL}:1 contrast.",
                            id="djust_theming.W001",
                        )
                    )

    return warnings
