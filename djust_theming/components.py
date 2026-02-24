"""
Theme UI components for djust.

Provides reusable components for theme switching.
"""

from dataclasses import dataclass

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from .manager import ThemeManager


@dataclass
class ThemeSwitcherConfig:
    """Configuration for ThemeSwitcher component."""

    show_presets: bool = True
    show_mode_toggle: bool = True
    show_labels: bool = True
    dropdown_position: str = "bottom-end"  # bottom-start, bottom-end, top-start, top-end
    button_class: str = ""
    dropdown_class: str = ""


class ThemeSwitcher:
    """
    Theme switcher component.

    Renders a dropdown or button group for switching themes and modes.
    """

    def __init__(
        self,
        theme_manager: ThemeManager | None = None,
        config: ThemeSwitcherConfig | None = None,
    ):
        """
        Initialize ThemeSwitcher.

        Args:
            theme_manager: ThemeManager instance (will create one if not provided)
            config: Configuration options
        """
        self.manager = theme_manager or ThemeManager()
        self.config = config or ThemeSwitcherConfig()

    def get_context(self) -> dict:
        """Get context for template rendering."""
        state = self.manager.get_state()
        presets = self.manager.get_available_presets()

        return {
            "theme_state": state,
            "theme_preset": state.preset,
            "theme_mode": state.mode,
            "theme_resolved_mode": state.resolved_mode,
            "presets": presets,
            "show_presets": self.config.show_presets,
            "show_mode_toggle": self.config.show_mode_toggle,
            "show_labels": self.config.show_labels,
            "dropdown_position": self.config.dropdown_position,
            "button_class": self.config.button_class,
            "dropdown_class": self.config.dropdown_class,
        }

    def render(self) -> str:
        """Render the theme switcher component."""
        context = self.get_context()
        html = render_to_string("djust_theming/theme_switcher.html", context)
        return mark_safe(html)

    def __str__(self) -> str:
        """Allow using component directly in templates."""
        return self.render()


class ThemeModeButton:
    """Simple theme mode toggle button component."""

    def __init__(
        self,
        theme_manager: ThemeManager | None = None,
        button_class: str = "",
        show_label: bool = False,
    ):
        self.manager = theme_manager or ThemeManager()
        self.button_class = button_class
        self.show_label = show_label

    def get_context(self) -> dict:
        state = self.manager.get_state()
        return {
            "theme_mode": state.mode,
            "theme_resolved_mode": state.resolved_mode,
            "button_class": self.button_class,
            "show_label": self.show_label,
        }

    def render(self) -> str:
        """Render the mode toggle button."""
        context = self.get_context()

        # Inline template for simple button
        icon = self._get_mode_icon(context["theme_resolved_mode"])
        label = f" {context['theme_mode'].title()}" if self.show_label else ""
        classes = f"theme-mode-toggle {self.button_class}".strip()

        html = f'''
        <button type="button"
                class="{classes}"
                data-djust-event="toggle_theme_mode"
                aria-label="Toggle theme mode"
                title="Toggle theme mode">
            {icon}{label}
        </button>
        '''
        return mark_safe(html)

    def _get_mode_icon(self, mode: str) -> str:
        """Get SVG icon for mode."""
        if mode == "dark":
            return """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>"""
        else:
            return """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>"""

    def __str__(self) -> str:
        return self.render()


class PresetSelector:
    """Theme preset selector component."""

    def __init__(
        self,
        theme_manager: ThemeManager | None = None,
        show_descriptions: bool = True,
        layout: str = "dropdown",  # dropdown, grid, list
        dropdown_class: str = "",
    ):
        self.manager = theme_manager or ThemeManager()
        self.show_descriptions = show_descriptions
        self.layout = layout
        self.dropdown_class = dropdown_class

    def get_context(self) -> dict:
        state = self.manager.get_state()
        return {
            "current_preset": state.preset,
            "presets": self.manager.get_available_presets(),
            "show_descriptions": self.show_descriptions,
            "layout": self.layout,
            "dropdown_class": self.dropdown_class,
        }

    def render(self) -> str:
        """Render the preset selector."""
        context = self.get_context()

        if self.layout == "dropdown":
            return self._render_dropdown(context)
        elif self.layout == "grid":
            return self._render_grid(context)
        else:
            return self._render_list(context)

    def _render_dropdown(self, context: dict) -> str:
        """Render as dropdown select."""
        options = []
        for preset in context["presets"]:
            selected = "selected" if preset["is_active"] else ""
            options.append(
                f'<option value="{preset["name"]}" {selected}>{preset["display_name"]}</option>'
            )

        html = f"""
        <select class="theme-preset-select {self.dropdown_class}"
                data-djust-event="set_theme_preset"
                data-djust-value-key="preset">
            {"".join(options)}
        </select>
        """
        return mark_safe(html)

    def _render_grid(self, context: dict) -> str:
        """Render as grid of buttons."""
        buttons = []
        for preset in context["presets"]:
            active_class = "active" if preset["is_active"] else ""
            buttons.append(f'''
            <button type="button"
                    class="theme-preset-btn {active_class}"
                    data-djust-event="set_theme_preset"
                    data-djust-params='{{"preset": "{preset["name"]}"}}'>
                {preset["display_name"]}
            </button>
            ''')

        html = f"""
        <div class="theme-preset-grid">
            {"".join(buttons)}
        </div>
        """
        return mark_safe(html)

    def _render_list(self, context: dict) -> str:
        """Render as list of radio buttons."""
        items = []
        for preset in context["presets"]:
            checked = "checked" if preset["is_active"] else ""
            description = (
                f"<small>{preset['description']}</small>" if self.show_descriptions else ""
            )
            items.append(f'''
            <label class="theme-preset-item">
                <input type="radio" name="theme-preset" value="{preset["name"]}" {checked}
                       data-djust-event="set_theme_preset"
                       data-djust-params='{{"preset": "{preset["name"]}"}}'>
                <span>{preset["display_name"]}</span>
                {description}
            </label>
            ''')

        html = f"""
        <div class="theme-preset-list">
            {"".join(items)}
        </div>
        """
        return mark_safe(html)

    def __str__(self) -> str:
        return self.render()
