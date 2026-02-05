# djust-theming - Simple Usage Guide

## 🚀 Quick Start (5 minutes)

### 1. View the Demo
**URL**: http://localhost:8001

**What to try**:
1. Open the homepage
2. Click the theme switcher (top-right corner) 
3. Try different presets: Default, Blue, Green, Purple, etc.
4. Toggle light/dark mode (moon/sun icon)
5. Visit `/components/` to see themed components

### 2. Add to Your Django Project

**Step 1**: Install
```bash
pip install djust-theming
```

**Step 2**: Add to settings.py
```python
INSTALLED_APPS = [
    # ... your apps
    'djust_theming',
]
```

**Step 3**: Add to your base template
```html
<!-- In your <head> -->
{% load theme_tags %}
{% theme_head %}

<!-- Theme switcher anywhere in your page -->
{% theme_switcher %}
```

**Step 4**: Use themed components
```html
{% load theme_components %}

{% button text="Click me" variant="primary" %}
{% card title="My Card" %}
    <p>Card content here</p>
{% endcard %}
```

### 3. CLI Commands
```bash
# List available themes
python manage.py djust_theme list-presets

# Generate Tailwind config
python manage.py djust_theme tailwind-config

# Export colors for shadcn/ui
python manage.py djust_theme shadcn-export
```

## 🎨 What You Get

- **7 color presets**: Default, Shadcn, Blue, Green, Purple, Orange, Rose
- **Light/Dark/System modes** with smooth transitions
- **6 components**: Button, Card, Badge, Alert, Input, Icon
- **Automatic persistence** (saves user preference)
- **Fast switching** (no page reload needed)

## 🔧 Integration Examples

### With Tailwind
```css
/* Use theme colors in your CSS */
.my-button {
  background: hsl(var(--primary));
  color: hsl(var(--primary-foreground));
}
```

### With djust LiveView
```python
from djust_theming.mixins import ThemeMixin

class MyLiveView(ThemeMixin, LiveView):
    template_name = "my_template.html"
    
    def handle_event(self, event, data):
        if event == "change_theme":
            self.set_theme(data["preset"])
```

## 📁 File Structure
```
your_project/
├── settings.py          # Add 'djust_theming'
├── templates/
│   └── base.html        # Add {% theme_head %} and {% theme_switcher %}
└── static/
    └── css/
        └── styles.css   # Use CSS variables like --primary
```

## ❓ Common Issues

**Theme not changing?**
- Make sure `{% theme_head %}` is in your `<head>`
- Check browser console for JS errors

**Styles not loading?**
- Run `python manage.py collectstatic`
- Make sure `STATIC_URL` is configured

**Components not showing?**
- Load the template tags: `{% load theme_components %}`
- Check that djust_theming is in INSTALLED_APPS

## 🎯 Next Steps

1. **Test the demo**: http://localhost:8001
2. **Add to your project**: Follow the 4 steps above
3. **Customize**: Use the CLI commands to export/modify themes
4. **Deploy**: Works with any Django deployment

The system is designed to be drop-in simple - add it to INSTALLED_APPS, include the template tags, and you're done!