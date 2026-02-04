# Contributing to djust-theming

Thank you for your interest in contributing to djust-theming! This document provides guidelines and instructions for contributing.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Django 4.2 or higher
- Git

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/djust-org/djust-theming.git
   cd djust-theming
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -e .
   pip install -e ".[dev]"
   ```

4. **Run the example project**
   ```bash
   cd example_project
   pip install -r requirements.txt
   python manage.py runserver
   ```

   Visit http://localhost:8000 to see the demo.

## How to Contribute

### Reporting Bugs

Before creating a bug report:
- Check if the issue already exists
- Test with the latest version
- Collect relevant information (Python version, Django version, browser, etc.)

When filing a bug report, include:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- Screenshots if applicable
- Error messages and stack traces

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:
- Use a clear, descriptive title
- Provide a detailed description of the proposed feature
- Explain why this enhancement would be useful
- Include examples of how it would be used

### Pull Requests

1. **Fork the repository** and create a branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the coding style used in the project
   - Add or update tests as needed
   - Update documentation if necessary

3. **Test your changes**
   ```bash
   # Run example project
   cd example_project
   python manage.py runserver

   # Test all features manually
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**
   - Provide a clear description of the changes
   - Reference any related issues
   - Include screenshots for UI changes

## Coding Standards

### Python

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise

### JavaScript

- Use modern ES6+ syntax
- Add comments for complex logic
- Follow existing code style
- Optimize for performance

### CSS

- Use CSS custom properties for theming
- Follow existing naming conventions
- Keep selectors specific but not overly complex
- Test in multiple browsers

### HTML/Templates

- Use Django template best practices
- Keep templates readable and maintainable
- Use semantic HTML
- Test responsiveness

## Project Structure

```
djust-theming/
├── djust_theming/           # Main package
│   ├── management/          # CLI commands
│   ├── static/              # CSS and JS
│   ├── templates/           # Django templates
│   ├── templatetags/        # Template tags
│   ├── components.py        # UI components
│   ├── css_generator.py     # CSS generation
│   ├── manager.py           # Theme management
│   ├── mixins.py            # LiveView integration
│   ├── presets.py           # Theme presets
│   ├── shadcn.py            # shadcn compatibility
│   └── tailwind.py          # Tailwind integration
├── example_project/         # Demo application
├── README.md
├── CHANGELOG.md
├── LICENSE
└── pyproject.toml
```

## Adding Features

### Adding a New Theme Preset

1. Edit `djust_theming/presets.py`
2. Create a new `ThemePreset` with light and dark tokens
3. Register it in `THEME_PRESETS` dictionary
4. Update documentation

### Adding a New Component

1. Create template in `djust_theming/templates/djust_theming/components/`
2. Add template tag in `djust_theming/templatetags/theme_components.py`
3. Add example in `example_project/theme_demo/templates/theme_demo/components.html`
4. Update documentation

### Adding a New CLI Command

1. Edit `djust_theming/management/commands/djust_theme.py`
2. Add new subcommand to `Command.add_arguments()`
3. Add handler method
4. Update documentation

## Testing

### Manual Testing

1. Run the example project
2. Test all pages (Home, Components, Presets, Tailwind)
3. Test theme switching (all presets)
4. Test light/dark mode
5. Test on multiple browsers
6. Test responsive design

### Browser Testing

Test in:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Android)

## Documentation

When adding or changing features:
- Update README.md if needed
- Update CHANGELOG.md
- Add docstrings to new code
- Update example project if relevant

## Release Process

(For maintainers)

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Commit changes
4. Create git tag: `git tag v1.x.x`
5. Push tag: `git push origin v1.x.x`
6. Build package: `python -m build`
7. Publish to PyPI: `python -m twine upload dist/*`

## Community

- Be respectful and inclusive
- Help others when you can
- Share your use cases and feedback
- Report bugs and suggest improvements

## Questions?

- Open a discussion on GitHub
- Check existing issues and pull requests
- Review the documentation

## License

By contributing to djust-theming, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to djust-theming! 🎨
