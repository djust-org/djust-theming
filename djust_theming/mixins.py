"""
ThemeMixin for djust LiveViews.

Provides theme-aware context, event handlers, and reactive theme switching.
Works with both Django templates (via context processors) and LiveView 
(via instance attributes and push_event).
"""

try:
    from djust.decorators import event_handler

    DJUST_AVAILABLE = True
except ImportError:
    DJUST_AVAILABLE = False

    def event_handler(*args, **kwargs):
        """Dummy decorator when djust is not available."""
        def decorator(func):
            return func
        if args and callable(args[0]):
            return args[0]
        return decorator


from .theme_css_generator import CompleteThemeCSSGenerator
from .manager import ThemeManager
from .presets import THEME_PRESETS


class ThemeMixin:
    """
    Mixin to add theme support to LiveViews.

    Provides:
    - Theme manager initialization in mount()
    - Event handlers for theme switching
    - Template context with theme state (as instance attributes)
    - Reactive theme switching via push_event (no page reload)

    Usage:
        class MyView(ThemeMixin, LiveView):
            template_name = 'my_template.html'
            
            def mount(self, request, **kwargs):
                super().mount(request, **kwargs)
                # Your mount code here

        In template, use these instance variables:
            {{ theme_head }}      - CSS + anti-FOUC script + JS
            {{ theme_switcher }}  - Theme mode and preset controls
            {{ theme_css }}       - Just the CSS variables
            {{ theme_preset }}    - Current preset name
            {{ theme_mode }}      - Current mode (light/dark/system)
            
    For reactive theme changes (no page reload):
        - Use dj-click="set_theme_mode" with data-dj-mode="dark"
        - Use dj-click="set_theme_preset" with data-dj-preset="blue"
        - The mixin will push CSS updates to the client via push_event
    """

    # Internal state (prefixed to avoid serialization)
    _theme_manager: ThemeManager = None
    _theme_state = None

    def mount(self, request, **kwargs):
        """Initialize theme manager and add theme context as instance attributes."""
        # Call parent mount if it exists
        if hasattr(super(), "mount"):
            super().mount(request, **kwargs)

        # Initialize theme manager (underscore prefix to avoid serialization)
        self._theme_manager = ThemeManager(request=request)
        self._theme_state = self._theme_manager.get_state()

        # Add theme context as instance attributes
        # These get picked up by get_context_data() in LiveView
        self._setup_theme_context()

    def _setup_theme_context(self):
        """Set up theme context variables as instance attributes."""
        if not self._theme_manager or not self._theme_state:
            return
            
        state = self._theme_state
        presets = self._theme_manager.get_available_presets()

        # Generate CSS using the complete generator
        generator = CompleteThemeCSSGenerator(theme_name=state.theme, color_preset=state.preset)
        css = generator.generate_css()

        # Anti-FOUC script - runs before page renders
        anti_fouc = """<script>
(function() {
    var storageKey = 'djust-theme-mode';
    var storedMode = localStorage.getItem(storageKey);
    var mode = storedMode || 'system';
    var resolvedMode = mode;
    if (mode === 'system') {
        resolvedMode = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    document.documentElement.setAttribute('data-theme', resolvedMode);
    document.documentElement.setAttribute('data-theme-mode', mode);
})();
</script>"""

        # Set theme_head - complete head content for theming
        # Use link_css=True logic similar to context processor for consistency
        from django.urls import reverse, NoReverseMatch
        try:
            url = reverse("djust_theming:theme_css")
            cache_buster = f"t={state.theme}&p={state.preset}&m={state.mode}"
            if state.pack:
                cache_buster += f"&pk={state.pack}"
            css_include = f'<link rel="stylesheet" href="{url}?{cache_buster}" data-djust-theme id="djust-theme-css">'
        except NoReverseMatch:
            css_include = f'<style id="djust-theme-css" data-djust-theme>{css}</style>'

        self.theme_head = f"""{anti_fouc}
{css_include}
<script src="/static/djust_theming/js/theme.js?v=3" defer></script>"""

        # Set theme_css - just the CSS (for cases where you want more control)
        self.theme_css = css_include
        
        # Raw CSS content (for push_event updates)
        self._theme_css_raw = css

        # Set theme_switcher - complete UI component
        self.theme_switcher = self._render_theme_switcher(state, presets)

        # Individual state values (useful for conditional logic in templates)
        self.theme_preset = state.preset
        self.theme_mode = state.mode
        self.theme_resolved_mode = state.resolved_mode
        self.theme_presets = presets

    def _render_theme_switcher(self, state, presets):
        """Render the theme switcher HTML component."""
        icons = {
            "light": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>',
            "dark": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>',
            "system": '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>',
        }

        # Build mode buttons with djust event handlers
        mode_buttons = ""
        for mode in ["light", "dark", "system"]:
            active = "active" if state.mode == mode else ""
            mode_buttons += f'''
            <button type="button" class="theme-mode-btn {active}"
                    dj-click="set_theme_mode"
                    data-dj-mode="{mode}"
                    title="{mode.title()} mode">{icons[mode]}</button>'''

        # Build preset options
        preset_options = ""
        for preset in presets:
            selected = "selected" if preset["is_active"] else ""
            preset_options += (
                f'<option value="{preset["name"]}" {selected}>{preset["display_name"]}</option>'
            )

        return f"""<div class="theme-switcher">
    <div class="theme-mode-controls">{mode_buttons}
    </div>
    <select class="theme-preset-select"
            dj-change="set_theme_preset"
            aria-label="Select theme preset">{preset_options}</select>
</div>
<style>
.theme-switcher {{ display: flex; align-items: center; gap: 0.75rem; }}
.theme-mode-controls {{ display: flex; background-color: hsl(var(--muted)); border-radius: var(--radius); padding: 0.25rem; gap: 0.125rem; }}
.theme-mode-btn {{ display: inline-flex; align-items: center; justify-content: center; padding: 0.375rem 0.5rem; border: none; background: transparent; color: hsl(var(--muted-foreground)); border-radius: calc(var(--radius) - 0.125rem); cursor: pointer; transition: all 0.15s ease; }}
.theme-mode-btn:hover {{ color: hsl(var(--foreground)); background-color: hsl(var(--background)); }}
.theme-mode-btn.active {{ color: hsl(var(--foreground)); background-color: hsl(var(--background)); box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); }}
.theme-preset-select {{ padding: 0.375rem 2rem 0.375rem 0.75rem; border: 1px solid hsl(var(--border)); border-radius: var(--radius); background-color: hsl(var(--background)); color: hsl(var(--foreground)); font-size: 0.875rem; cursor: pointer; appearance: none; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E"); background-repeat: no-repeat; background-position: right 0.5rem center; }}
.theme-preset-select:hover {{ border-color: hsl(var(--ring)); }}
.theme-preset-select:focus {{ outline: none; border-color: hsl(var(--ring)); box-shadow: 0 0 0 2px hsl(var(--ring) / 0.2); }}
</style>"""

    def _push_theme_update(self, mode: str = None, preset: str = None, css: str = None):
        """
        Push theme update to client via push_event.

        This allows reactive theme changes without full page reload.
        The client JS will update the CSS and DOM attributes.

        The event name 'theme_update' will be dispatched by djust as
        'djust:push_event' with detail { event: 'theme_update', payload: {...} }
        """
        if hasattr(self, 'push_event'):
            payload = {}
            if mode is not None:
                payload['mode'] = mode
            if preset is not None:
                payload['preset'] = preset
            if css is not None:
                payload['css'] = css

            self.push_event('theme_update', payload)
            # Theme changes are purely client-side (CSS variables) — skip the
            # server render to avoid a full HTML update that mangles the page
            # when theme state is outside <div data-djust-root> (DJE-053).
            self._skip_render = True

    # Event handlers - only define if djust is available
    if DJUST_AVAILABLE:
        @event_handler()
        def set_theme_mode(self, mode: str = "", value: str = "", **kwargs):
            """
            Set theme mode to light, dark, or system.

            Usage in template:
                <button dj-click="set_theme_mode" data-dj-mode="dark">Dark Mode</button>
            """
            # Support both data-dj-mode (dj-click) and value (dj-change)
            mode = mode or value or "system"
            if mode not in ("light", "dark", "system"):
                return
                
            success = self._theme_manager.set_mode(mode)
            if success:
                self._theme_state = self._theme_manager.get_state()
                self._setup_theme_context()  # Refresh context
                
                # Push update to client (mode only - CSS doesn't change)
                self._push_theme_update(mode=mode)

        @event_handler()
        def set_theme_preset(self, preset: str = "", value: str = "", **kwargs):
            """
            Set theme preset.

            Usage in template (button):
                <button dj-click="set_theme_preset" data-dj-preset="blue">Blue</button>

            Usage in template (select):
                <select dj-change="set_theme_preset">
                    <option value="default">Default</option>
                    <option value="blue">Blue</option>
                </select>
            """
            # Support both data-dj-preset (dj-click) and value (dj-change)
            preset = preset or value or "default"
            if preset not in THEME_PRESETS:
                return
                
            success = self._theme_manager.set_preset(preset)
            if success:
                self._theme_state = self._theme_manager.get_state()
                self._setup_theme_context()  # Refresh context with new CSS
                
                # Push update to client with new CSS
                self._push_theme_update(preset=preset, css=self._theme_css_raw)

        @event_handler()
        def toggle_theme_mode(self, **kwargs):
            """
            Toggle between light and dark mode.
            
            Usage in template:
                <button dj-click="toggle_theme_mode">Toggle Theme</button>
            """
            new_mode = self._theme_manager.toggle_mode()
            self._theme_state = self._theme_manager.get_state()
            self._setup_theme_context()
            
            # Push update to client
            self._push_theme_update(mode=new_mode)

        @event_handler()
        def cycle_theme_preset(self, **kwargs):
            """
            Cycle through available theme presets.
            
            Usage in template:
                <button dj-click="cycle_theme_preset">Next Theme</button>
            """
            current = self._theme_state.preset
            presets = list(THEME_PRESETS.keys())
            current_index = presets.index(current) if current in presets else 0
            next_index = (current_index + 1) % len(presets)
            next_preset = presets[next_index]

            self._theme_manager.set_preset(next_preset)
            self._theme_state = self._theme_manager.get_state()
            self._setup_theme_context()
            
            # Push update to client with new CSS
            self._push_theme_update(preset=next_preset, css=self._theme_css_raw)
