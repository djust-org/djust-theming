# Plan: Phase 7.4 + 7.5 + 7.6 -- Reduced Motion, High Contrast Media Query, Print Stylesheet

## 7.4 Reduced Motion (`@media (prefers-reduced-motion: reduce)`)

### What
Add a `get_reduced_motion_css()` function in `design_tokens.py` that returns a `@media (prefers-reduced-motion: reduce)` block. This block:
- Overrides `--duration-fast`, `--duration-normal`, `--duration-slow`, `--duration-slower` to `0ms`
- Sets `*, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; scroll-behavior: auto !important; }`

Note: `performance.css` and `css_generator._generate_base_styles()` already have partial reduced-motion rules. The new function centralises the token override approach so generated CSS also kills animation tokens at the variable level.

### Where
- `design_tokens.py`: new `get_reduced_motion_css()` function
- `design_tokens.py`: `generate_design_tokens_css()` and `generate_design_tokens_classes_css()` call it at the end
- Tests: `tests/test_a11y_print.py`

## 7.5 High Contrast Media Query (`@media (prefers-contrast: more)`)

### What
Add a `get_high_contrast_css()` function in `design_tokens.py` that returns a `@media (prefers-contrast: more)` block. This block:
- Increases border widths: `--border-width: 2px`
- Enhances focus ring: `--ring-width: 3px; --ring-offset: 3px`
- Forces solid outlines on focus-visible elements
- Increases text contrast by adjusting `--muted-foreground` towards foreground

### Where
- `design_tokens.py`: new `get_high_contrast_css()` function
- `design_tokens.py`: included in `generate_design_tokens_css()` and `generate_design_tokens_classes_css()`
- Tests: `tests/test_a11y_print.py`

## 7.6 Print Stylesheet

### What
Create `djust_theming/static/djust_theming/css/print.css` with `@media print` rules:
- Hide `.sidebar`, `.navbar`, `.theme-switcher`, `.theme-mode-btn`, `.theme-preset-select`, `button[type="button"]`, `.toast`, `.modal-overlay`
- Force white background, black text on body
- Remove shadows, animations, transitions
- Set `a[href]::after { content: " (" attr(href) ")"; }` for URL display
- Page breaks: `h2, h3 { page-break-after: avoid; }`, `img { page-break-inside: avoid; }`

Include in `theme_head.html` via `<link rel="stylesheet" href="{% static 'djust_theming/css/print.css' %}" media="print">`.

### Where
- New file: `djust_theming/static/djust_theming/css/print.css`
- `theme_head.html`: add print stylesheet link
- Tests: `tests/test_a11y_print.py`

## Test Plan (TDD)
1. **test_reduced_motion_css_overrides_duration_tokens** -- verify all duration tokens set to 0ms
2. **test_reduced_motion_css_kills_animations** -- verify animation-duration/transition-duration overrides
3. **test_reduced_motion_in_generated_css** -- verify `generate_design_tokens_css()` includes reduced motion block
4. **test_reduced_motion_in_classes_css** -- verify `generate_design_tokens_classes_css()` includes it
5. **test_high_contrast_css_border_width** -- verify `--border-width` in output
6. **test_high_contrast_css_ring_width** -- verify `--ring-width` in output
7. **test_high_contrast_css_focus_visible** -- verify focus-visible outline rules
8. **test_high_contrast_in_generated_css** -- verify `generate_design_tokens_css()` includes it
9. **test_high_contrast_in_classes_css** -- verify `generate_design_tokens_classes_css()` includes it
10. **test_print_css_file_exists** -- verify file at expected static path
11. **test_print_css_hides_sidebar** -- verify `.sidebar { display: none }` in print.css
12. **test_print_css_hides_navbar** -- verify `.navbar { display: none }` in print.css
13. **test_print_css_hides_interactive** -- verify theme-switcher etc hidden
14. **test_print_css_forces_colors** -- verify white bg, black text
15. **test_print_css_removes_shadows** -- verify box-shadow: none
16. **test_print_css_shows_urls** -- verify `a[href]::after` rule
17. **test_print_css_page_breaks** -- verify page-break rules
18. **test_theme_head_includes_print_link** -- verify `<link ... media="print">` in theme_head output
