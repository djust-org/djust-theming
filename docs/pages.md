# Page Templates

djust-theming ships 9 ready-to-use page templates covering authentication, error handling, and common utility screens. Each page is available as a template tag that renders a styled fragment you can drop into any layout.

## Quick start

```html
{% extends "djust_theming/layouts/centered.html" %}
{% load theme_pages %}

{% block centered_content %}
    {% theme_login_page action="/auth/login/" forgot_password_url="/reset/" register_url="/register/" %}
{% endblock %}
```

Load the `theme_pages` tag library, then call the tag for the page you need. Every tag renders a self-contained HTML fragment (not a full document), so you control the surrounding layout.

## Available pages

### Authentication pages

| Tag | Default title | Description |
|-----|---------------|-------------|
| `{% theme_login_page %}` | Sign in | Email + password form with remember-me, social login slot, forgot-password link |
| `{% theme_register_page %}` | Create account | Name, email, password, confirm-password, optional terms checkbox |
| `{% theme_password_reset_page %}` | Reset password | Email-only form with back-to-login link |
| `{% theme_password_confirm_page %}` | Set new password | New password + confirmation form |

All authentication forms include a CSRF token automatically when rendered inside a Django request context.

### Error pages

| Tag | Default title | Description |
|-----|---------------|-------------|
| `{% theme_404_page %}` | Page not found | Large 404 code, description, "Go home" button, illustration slot |
| `{% theme_500_page %}` | Something went wrong | Large 500 code, "Try again" + "Go home" buttons |
| `{% theme_403_page %}` | Access denied | Large 403 code, description, "Go back" button |

### Utility pages

| Tag | Default title | Description |
|-----|---------------|-------------|
| `{% theme_maintenance_page %}` | Under maintenance | Illustration, ETA, and progress-bar slots |
| `{% theme_empty_state_page %}` | No items yet | Icon slot, optional CTA button |

## Tag reference

### theme_login_page

```html
{% theme_login_page
    action="/auth/login/"
    title="Sign in"
    forgot_password_url="/reset/"
    register_url="/register/"
    slot_social='<button class="google-btn">Sign in with Google</button>'
    slot_footer='<p>Custom footer HTML</p>'
%}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `action` | string | `""` | Form action URL |
| `title` | string | `"Sign in"` | Page heading text |
| `forgot_password_url` | string | `""` | URL for "Forgot password?" link (hidden if empty) |
| `register_url` | string | `""` | URL for "Register" link in footer (hidden if empty) |
| `slot_social` | HTML | — | Raw HTML for social login buttons |
| `slot_footer` | HTML | — | Raw HTML to replace the default footer |

### theme_register_page

```html
{% theme_register_page
    action="/auth/register/"
    title="Create account"
    login_url="/login/"
    terms_url="/terms/"
    slot_footer='<p>Custom footer</p>'
%}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `action` | string | `""` | Form action URL |
| `title` | string | `"Create account"` | Page heading text |
| `login_url` | string | `""` | URL for "Already have an account?" link |
| `terms_url` | string | `""` | URL for terms-of-service checkbox (hidden if empty) |
| `slot_footer` | HTML | — | Raw HTML to replace the default footer |

### theme_password_reset_page

```html
{% theme_password_reset_page
    action="/auth/reset/"
    title="Reset password"
    description="Enter your email and we'll send a reset link."
    login_url="/login/"
%}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `action` | string | `""` | Form action URL |
| `title` | string | `"Reset password"` | Page heading |
| `description` | string | *(email prompt)* | Help text below heading |
| `login_url` | string | `""` | URL for "Back to login" link |

### theme_password_confirm_page

```html
{% theme_password_confirm_page
    action="/auth/confirm/uidb64/token/"
    title="Set new password"
    description="Choose a strong password."
%}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `action` | string | `""` | Form action URL |
| `title` | string | `"Set new password"` | Page heading |
| `description` | string | `"Choose a strong password for your account."` | Help text |

### theme_404_page

```html
{% theme_404_page
    title="Page not found"
    description="The page you're looking for doesn't exist."
    home_url="/"
    slot_illustration='<img src="/static/lost.svg" alt="" />'
%}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | string | `"Page not found"` | Page heading |
| `description` | string | *(default message)* | Description text |
| `home_url` | string | `"/"` | URL for "Go home" button |
| `slot_illustration` | HTML | — | Custom illustration above the error code |

### theme_500_page

```html
{% theme_500_page
    title="Something went wrong"
    home_url="/"
    retry_url="/dashboard/"
%}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | string | `"Something went wrong"` | Page heading |
| `description` | string | *(default message)* | Description text |
| `home_url` | string | `"/"` | URL for "Go home" button |
| `retry_url` | string | `""` | URL for "Try again" button (hidden if empty) |

### theme_403_page

```html
{% theme_403_page
    title="Access denied"
    back_url="/dashboard/"
%}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | string | `"Access denied"` | Page heading |
| `description` | string | *(default message)* | Description text |
| `back_url` | string | `"/"` | URL for "Go back" button |

### theme_maintenance_page

```html
{% theme_maintenance_page
    title="Scheduled maintenance"
    description="We'll be back shortly."
    slot_eta="<p>Estimated return: 2:00 PM UTC</p>"
    slot_progress='<div class="progress-bar" style="width:60%"></div>'
    slot_illustration='<svg>...</svg>'
%}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | string | `"Under maintenance"` | Page heading |
| `description` | string | *(default message)* | Description text |
| `slot_illustration` | HTML | — | Custom illustration |
| `slot_eta` | HTML | — | Estimated return time content |
| `slot_progress` | HTML | — | Progress indicator content |

### theme_empty_state_page

```html
{% theme_empty_state_page
    title="No projects yet"
    description="Create your first project to get started."
    cta_text="New project"
    cta_url="/projects/new/"
    slot_icon='<svg class="inbox-icon">...</svg>'
%}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | string | `"No items yet"` | Page heading |
| `description` | string | `"Get started by creating your first item."` | Description text |
| `cta_text` | string | `""` | Call-to-action button text (hidden if empty) |
| `cta_url` | string | `""` | Call-to-action button URL |
| `slot_icon` | HTML | — | Custom icon/illustration |

## How to override a page template

djust-theming resolves page templates using a fallback chain:

1. **Theme-specific**: `djust_theming/themes/{theme_name}/pages/{page}.html`
2. **Default**: `djust_theming/pages/{page}.html`

To override the login page for a theme called `corporate`:

```
your_app/
  templates/
    djust_theming/
      themes/
        corporate/
          pages/
            login.html    <-- your custom login template
```

Your custom template receives the same context variables as the default. See the default templates in `djust_theming/templates/djust_theming/pages/` for the full variable list.

## CSS

Page styles live in `djust_theming/static/djust_theming/css/pages.css` inside a CSS `@layer`. All class names respect the `css_prefix` setting from your theme configuration.

Key CSS classes used across pages:

- `.page-login`, `.page-register`, `.page-password-reset`, `.page-password-confirm` -- auth pages
- `.page-error`, `.page-404`, `.page-500`, `.page-403` -- error pages
- `.page-utility`, `.page-maintenance`, `.page-empty-state` -- utility pages
- `.page-title`, `.page-description`, `.page-actions` -- shared structural classes
