"""
Django management command for djust-theming Tailwind integration.

Usage:
    python manage.py djust_theme tailwind-config [--preset blue] [--output tailwind.config.js]
    python manage.py djust_theme export-colors [--preset blue] [--format json]
    python manage.py djust_theme list-presets
    python manage.py djust_theme generate-examples
"""

from django.core.management.base import BaseCommand, CommandError
from djust_theming.presets import THEME_PRESETS
from djust_theming.tailwind import (
    generate_tailwind_config,
    export_preset_as_tailwind_colors,
    generate_tailwind_apply_examples,
)
from djust_theming.shadcn import (
    import_shadcn_theme_from_file,
    export_shadcn_theme_to_file,
    export_to_shadcn_format,
)
import json


class Command(BaseCommand):
    help = 'djust-theming utilities for Tailwind CSS integration'

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest='subcommand', help='Subcommand to run')

        # tailwind-config subcommand
        tailwind_parser = subparsers.add_parser(
            'tailwind-config',
            help='Generate tailwind.config.js with theme CSS variables'
        )
        tailwind_parser.add_argument(
            '--preset',
            type=str,
            default='default',
            help='Preset name to use (default: default)'
        )
        tailwind_parser.add_argument(
            '--output',
            type=str,
            default='tailwind.config.js',
            help='Output file path (default: tailwind.config.js)'
        )
        tailwind_parser.add_argument(
            '--extend',
            action='store_true',
            default=True,
            help='Extend Tailwind default colors (default: true)'
        )
        tailwind_parser.add_argument(
            '--no-extend',
            action='store_false',
            dest='extend',
            help='Replace Tailwind default colors instead of extending'
        )
        tailwind_parser.add_argument(
            '--all-presets',
            action='store_true',
            help='Include all presets as additional color scales'
        )

        # export-colors subcommand
        export_parser = subparsers.add_parser(
            'export-colors',
            help='Export preset colors in various formats'
        )
        export_parser.add_argument(
            '--preset',
            type=str,
            default='default',
            help='Preset name to export (default: default)'
        )
        export_parser.add_argument(
            '--format',
            type=str,
            choices=['json', 'python'],
            default='json',
            help='Output format (default: json)'
        )
        export_parser.add_argument(
            '--output',
            type=str,
            help='Output file path (default: stdout)'
        )

        # list-presets subcommand
        subparsers.add_parser(
            'list-presets',
            help='List all available theme presets'
        )

        # generate-examples subcommand
        examples_parser = subparsers.add_parser(
            'generate-examples',
            help='Generate CSS examples showing @apply usage'
        )
        examples_parser.add_argument(
            '--output',
            type=str,
            default='theme-examples.css',
            help='Output file path (default: theme-examples.css)'
        )

        # shadcn-import subcommand
        import_parser = subparsers.add_parser(
            'shadcn-import',
            help='Import a shadcn/ui theme JSON file'
        )
        import_parser.add_argument(
            'input_file',
            type=str,
            help='Path to shadcn theme JSON file'
        )
        import_parser.add_argument(
            '--register',
            action='store_true',
            help='Register the imported theme in THEME_PRESETS'
        )

        # shadcn-export subcommand
        shadcn_export_parser = subparsers.add_parser(
            'shadcn-export',
            help='Export a preset to shadcn/ui theme JSON format'
        )
        shadcn_export_parser.add_argument(
            '--preset',
            type=str,
            default='default',
            help='Preset name to export (default: default)'
        )
        shadcn_export_parser.add_argument(
            '--output',
            type=str,
            required=True,
            help='Output JSON file path'
        )

        # init subcommand
        init_parser = subparsers.add_parser(
            'init',
            help='Initialize djust-theming in your project'
        )
        init_parser.add_argument(
            '--preset',
            type=str,
            default='default',
            help='Initial preset to use (default: default)'
        )
        init_parser.add_argument(
            '--with-tailwind',
            action='store_true',
            help='Also generate Tailwind config'
        )
        init_parser.add_argument(
            '--with-examples',
            action='store_true',
            help='Generate example templates'
        )

    def handle(self, *args, **options):
        subcommand = options.get('subcommand')

        if not subcommand:
            self.print_help('manage.py', 'djust_theme')
            return

        if subcommand == 'tailwind-config':
            self.handle_tailwind_config(options)
        elif subcommand == 'export-colors':
            self.handle_export_colors(options)
        elif subcommand == 'list-presets':
            self.handle_list_presets()
        elif subcommand == 'generate-examples':
            self.handle_generate_examples(options)
        elif subcommand == 'shadcn-import':
            self.handle_shadcn_import(options)
        elif subcommand == 'shadcn-export':
            self.handle_shadcn_export(options)
        elif subcommand == 'init':
            self.handle_init(options)
        else:
            raise CommandError(f"Unknown subcommand: {subcommand}")

    def handle_tailwind_config(self, options):
        """Generate tailwind.config.js file."""
        preset = options['preset']
        output = options['output']
        extend = options['extend']
        all_presets = options['all_presets']

        if preset not in THEME_PRESETS:
            raise CommandError(
                f"Unknown preset: {preset}. "
                f"Available: {', '.join(THEME_PRESETS.keys())}"
            )

        self.stdout.write(f"Generating Tailwind config for preset '{preset}'...")

        try:
            config_content = generate_tailwind_config(
                preset_name=preset,
                extend_colors=extend,
                include_all_presets=all_presets,
            )

            with open(output, 'w') as f:
                f.write(config_content)

            self.stdout.write(
                self.style.SUCCESS(f"✓ Generated {output}")
            )

            self.stdout.write("\nNext steps:")
            self.stdout.write("  1. Install Tailwind CSS if you haven't:")
            self.stdout.write("     npm install -D tailwindcss")
            self.stdout.write("")
            self.stdout.write("  2. Add theme CSS to your base template:")
            self.stdout.write("     {{ theme_head }}")
            self.stdout.write("")
            self.stdout.write("  3. Use theme colors in your templates:")
            self.stdout.write('     <button class="bg-primary text-primary-foreground">Click me</button>')
            self.stdout.write("")
            self.stdout.write("  4. Or use @apply in your CSS:")
            self.stdout.write("     python manage.py djust_theme generate-examples")

        except Exception as e:
            raise CommandError(f"Failed to generate config: {e}")

    def handle_export_colors(self, options):
        """Export preset colors."""
        preset = options['preset']
        format_type = options['format']
        output = options.get('output')

        if preset not in THEME_PRESETS:
            raise CommandError(
                f"Unknown preset: {preset}. "
                f"Available: {', '.join(THEME_PRESETS.keys())}"
            )

        try:
            colors = export_preset_as_tailwind_colors(preset)

            if format_type == 'json':
                content = json.dumps(colors, indent=2)
            elif format_type == 'python':
                content = f"# Colors for preset: {preset}\n\n"
                content += "COLORS = {\n"
                for key, value in colors.items():
                    content += f"    '{key}': '{value}',\n"
                content += "}\n"
            else:
                raise CommandError(f"Unknown format: {format_type}")

            if output:
                with open(output, 'w') as f:
                    f.write(content)
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Exported colors to {output}")
                )
            else:
                self.stdout.write(content)

        except Exception as e:
            raise CommandError(f"Failed to export colors: {e}")

    def handle_list_presets(self):
        """List all available presets."""
        self.stdout.write(self.style.SUCCESS("Available theme presets:\n"))

        for name, preset in THEME_PRESETS.items():
            self.stdout.write(
                f"  • {name:12} - {preset.display_name}"
            )
            if hasattr(preset, 'description'):
                self.stdout.write(f"               {preset.description}")

        self.stdout.write(
            f"\nTotal: {len(THEME_PRESETS)} presets"
        )

    def handle_generate_examples(self, options):
        """Generate @apply examples."""
        output = options['output']

        try:
            examples = generate_tailwind_apply_examples()

            with open(output, 'w') as f:
                f.write(examples)

            self.stdout.write(
                self.style.SUCCESS(f"✓ Generated {output}")
            )
            self.stdout.write("\nThis file shows how to use @apply with theme colors.")
            self.stdout.write("You can copy these examples into your own CSS files.")

        except Exception as e:
            raise CommandError(f"Failed to generate examples: {e}")

    def handle_shadcn_import(self, options):
        """Import a shadcn theme from JSON file."""
        input_file = options['input_file']
        register = options['register']

        try:
            preset = import_shadcn_theme_from_file(input_file)

            self.stdout.write(
                self.style.SUCCESS(f"✓ Imported theme: {preset.name}")
            )
            self.stdout.write(f"  Display name: {preset.display_name}")

            if register:
                THEME_PRESETS[preset.name] = preset
                self.stdout.write(
                    self.style.SUCCESS(
                        f"\n✓ Registered '{preset.name}' in THEME_PRESETS"
                    )
                )
                self.stdout.write(
                    "\nTo make this permanent, add the theme to "
                    "djust_theming/presets.py"
                )
            else:
                self.stdout.write(
                    "\nTo register this theme, re-run with --register flag"
                )

        except FileNotFoundError:
            raise CommandError(f"File not found: {input_file}")
        except json.JSONDecodeError as e:
            raise CommandError(f"Invalid JSON: {e}")
        except Exception as e:
            raise CommandError(f"Failed to import theme: {e}")

    def handle_shadcn_export(self, options):
        """Export a preset to shadcn theme JSON format."""
        preset = options['preset']
        output = options['output']

        if preset not in THEME_PRESETS:
            raise CommandError(
                f"Unknown preset: {preset}. "
                f"Available: {', '.join(THEME_PRESETS.keys())}"
            )

        try:
            export_shadcn_theme_to_file(preset, output)

            self.stdout.write(
                self.style.SUCCESS(f"✓ Exported {preset} to {output}")
            )
            self.stdout.write(
                "\nThis file can be imported into shadcn/ui-based projects "
                "or uploaded to themes.shadcn.com"
            )

        except Exception as e:
            raise CommandError(f"Failed to export theme: {e}")

    def handle_init(self, options):
        """Initialize djust-theming in the project."""
        preset = options['preset']
        with_tailwind = options['with_tailwind']
        with_examples = options['with_examples']

        if preset not in THEME_PRESETS:
            raise CommandError(
                f"Unknown preset: {preset}. "
                f"Available: {', '.join(THEME_PRESETS.keys())}"
            )

        self.stdout.write(self.style.SUCCESS("\n🎨 Initializing djust-theming...\n"))

        # Check if djust_theming is in INSTALLED_APPS
        try:
            import django.conf
            if 'djust_theming' not in django.conf.settings.INSTALLED_APPS:
                self.stdout.write(
                    self.style.WARNING(
                        "⚠  djust_theming not found in INSTALLED_APPS"
                    )
                )
                self.stdout.write(
                    "\nPlease add to settings.py:\n"
                    "INSTALLED_APPS = [\n"
                    "    ...\n"
                    "    'djust_theming',\n"
                    "]\n"
                )
        except Exception:
            pass

        # Generate tailwind config if requested
        if with_tailwind:
            try:
                config_content = generate_tailwind_config(preset_name=preset)
                with open('tailwind.config.js', 'w') as f:
                    f.write(config_content)
                self.stdout.write(
                    self.style.SUCCESS("✓ Generated tailwind.config.js")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"✗ Failed to generate Tailwind config: {e}")
                )

        # Generate example templates if requested
        if with_examples:
            import os
            os.makedirs('templates/examples', exist_ok=True)

            example_template = """{% load theme_tags theme_components %}
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>djust-theming Example</title>
    {% theme_head %}
    {% if tailwind %}
    <link href="https://cdn.tailwindcss.com" rel="stylesheet">
    {% endif %}
</head>
<body class="bg-background text-foreground min-h-screen p-8">
    <div class="max-w-4xl mx-auto">
        <div class="flex items-center justify-between mb-8">
            <h1 class="text-3xl font-bold">djust-theming Example</h1>
            {% theme_switcher %}
        </div>

        {% theme_card title="Welcome" %}
            <p class="mb-4">This is an example using djust-theming components.</p>
            {% theme_button "Click me" variant="primary" %}
            {% theme_button "Secondary" variant="secondary" %}
        {% end_theme_card %}

        <div class="mt-4">
            {% theme_alert "This is a success message!" variant="success" dismissible=True %}
        </div>

        <div class="mt-4 flex gap-2">
            {% theme_badge "New" variant="success" %}
            {% theme_badge "Beta" variant="secondary" %}
            {% theme_badge "Popular" variant="default" %}
        </div>
    </div>
</body>
</html>
"""
            with open('templates/examples/theme_example.html', 'w') as f:
                f.write(example_template)

            self.stdout.write(
                self.style.SUCCESS("✓ Generated templates/examples/theme_example.html")
            )

        # Print next steps
        self.stdout.write(
            self.style.SUCCESS("\n✓ Initialization complete!\n")
        )
        self.stdout.write("Next steps:\n")
        self.stdout.write("  1. Add djust_theming to INSTALLED_APPS (if not already)")
        self.stdout.write("  2. Add theme context processor to settings.py:")
        self.stdout.write("     'djust_theming.context_processors.theme_context'")
        self.stdout.write("  3. Use {{ theme_head }} in your base template")
        self.stdout.write("  4. Use {% load theme_components %} to access components\n")

        if with_examples:
            self.stdout.write(
                "  5. Check templates/examples/theme_example.html for usage examples\n"
            )

        self.stdout.write(f"\n📚 Preset: {preset}")
        self.stdout.write(f"🎨 Theme switcher: {{ theme_switcher }}")
        self.stdout.write(f"🌓 Mode toggle: {{ theme_mode_toggle }}\n")
