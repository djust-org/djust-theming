# Phase 4: Page Templates + theme_pages Tag Library

## Overview

Add 9 page templates (auth, error, utility) and a `theme_pages` template tag library.
Pages compose existing components (card, input, button, checkbox, alert) within the
centered layout. Each page template lives at `djust_theming/templates/djust_theming/pages/`.
Each tag in `theme_pages.py` renders a page's inner content as a standalone fragment
(not a full HTML document) so users can include it in their own templates or extend
the centered layout themselves.

## Architecture

### Template Resolution

Add `_get_page_candidates()` and `resolve_page_template()` to `template_resolver.py`,
following the same pattern as components and layouts:

1. `djust_theming/themes/{theme_name}/pages/{page}.html`
2. `djust_theming/pages/{page}.html`

### Tag Library

New file: `djust_theming/templatetags/theme_pages.py`

Each tag is a `@register.simple_tag(takes_context=True)` that:
- Resolves the page template via `resolve_page_template()`
- Passes context variables (configurable headings, descriptions, URLs, etc.)
- Returns `mark_safe(tmpl.render(ctx))`
- Uses `css_prefix` from theme config

### CSS

Page-specific CSS goes in `djust_theming/static/djust_theming/css/pages.css` wrapped
in `@layer components`. Included via the page templates or documented for manual inclusion.

## 9 Page Templates

### Auth Pages (4)

All compose: card, input, button components via `css_prefix`-prefixed classes.

#### 1. login.html
- Card wrapper with optional title slot
- Email input (type=email, required)
- Password input (type=password, required)
- "Remember me" checkbox
- Submit button (primary, full width)
- "Forgot password?" link
- Social login slot (`slot_social`)
- Footer slot (`slot_footer`) for "Don't have an account? Register"

Tag: `{% theme_login_page %}`
Params: `action=""`, `title="Sign in"`, `forgot_password_url=""`, `register_url=""`, `**attrs`

#### 2. register.html
- Card wrapper with optional title slot
- Name input (type=text)
- Email input (type=email, required)
- Password input (type=password, required)
- Confirm password input (type=password, required)
- Terms checkbox with slot_label for custom terms link
- Submit button (primary, full width)
- Footer slot for "Already have an account? Sign in"

Tag: `{% theme_register_page %}`
Params: `action=""`, `title="Create account"`, `login_url=""`, `terms_url=""`, `**attrs`

#### 3. password_reset.html
- Card wrapper
- Heading + description text
- Email input (type=email, required)
- Submit button (primary, full width)
- "Back to login" link

Tag: `{% theme_password_reset_page %}`
Params: `action=""`, `title="Reset password"`, `description="..."`, `login_url=""`, `**attrs`

#### 4. password_confirm.html
- Card wrapper
- Heading + description text
- New password input (type=password, required)
- Confirm password input (type=password, required)
- Submit button (primary, full width)

Tag: `{% theme_password_confirm_page %}`
Params: `action=""`, `title="Set new password"`, `description="..."`, `**attrs`

### Error Pages (3)

#### 5. 404.html
- Illustration slot (`slot_illustration`)
- Large "404" display text
- "Page not found" heading
- Description text
- "Go home" button (primary)

Tag: `{% theme_404_page %}`
Params: `title="Page not found"`, `description="..."`, `home_url="/"`, `**attrs`

#### 6. 500.html
- Large "500" display text
- "Something went wrong" heading
- Description text
- "Try again" button (primary) + "Go home" button (secondary)

Tag: `{% theme_500_page %}`
Params: `title="Something went wrong"`, `description="..."`, `home_url="/"`, `retry_url=""`, `**attrs`

#### 7. 403.html
- Large "403" display text
- "Access denied" heading
- Description text
- "Go back" button (primary)

Tag: `{% theme_403_page %}`
Params: `title="Access denied"`, `description="..."`, `back_url="/"`, `**attrs`

### Utility Pages (2)

#### 8. maintenance.html
- Icon/illustration slot
- "Under maintenance" heading
- Description text
- Estimated return time slot (`slot_eta`)
- Progress bar slot (`slot_progress`)

Tag: `{% theme_maintenance_page %}`
Params: `title="Under maintenance"`, `description="..."`, `**attrs`

#### 9. empty_state.html
- Icon/illustration slot (`slot_icon`)
- Heading
- Description text
- CTA button with configurable text and URL

Tag: `{% theme_empty_state_page %}`
Params: `title="No items yet"`, `description="..."`, `cta_text=""`, `cta_url=""`, `**attrs`

## Files to Create

1. `djust_theming/templates/djust_theming/pages/login.html`
2. `djust_theming/templates/djust_theming/pages/register.html`
3. `djust_theming/templates/djust_theming/pages/password_reset.html`
4. `djust_theming/templates/djust_theming/pages/password_confirm.html`
5. `djust_theming/templates/djust_theming/pages/404.html`
6. `djust_theming/templates/djust_theming/pages/500.html`
7. `djust_theming/templates/djust_theming/pages/403.html`
8. `djust_theming/templates/djust_theming/pages/maintenance.html`
9. `djust_theming/templates/djust_theming/pages/empty_state.html`
10. `djust_theming/templatetags/theme_pages.py`
11. `djust_theming/static/djust_theming/css/pages.css`

## Files to Modify

1. `djust_theming/template_resolver.py` — add `_get_page_candidates()` + `resolve_page_template()`

## Test Plan

File: `tests/test_page_templates.py`

### Template Existence Tests
- All 9 page templates loadable via `get_template()`

### Template Resolution Tests
- `_get_page_candidates()` returns correct fallback chain
- `resolve_page_template()` falls back to default

### Tag Rendering Tests (per page)
For each of the 9 tags:
- Renders without error with defaults
- Contains expected CSS classes (card, btn, input classes)
- Contains expected text (headings, descriptions)
- Custom params override defaults
- Slot passthrough works (slot_social on login, slot_illustration on 404, etc.)

### Structure Tests
- Auth pages contain `<form>` element
- Auth pages have `method="post"` on form
- Error pages contain error code display
- Error pages contain action buttons
- Empty state contains CTA when provided, omits when not

### Accessibility Tests
- Forms have associated labels
- Buttons have type attributes
- Error pages have proper heading hierarchy

Estimated: ~80-100 tests
