"""
Django management command to build static theme files.
"""

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os

try:
    from djust_theming.build_themes import build_themes
except ImportError:
    # Fallback if djust_theming not in path
    import sys
    sys.path.insert(0, '/Users/tip/Dropbox/online_projects/ai/djust_project/djust-theming')
    from djust_theming.build_themes import build_themes


class Command(BaseCommand):
    help = 'Build static theme CSS files for production deployment'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output-dir',
            type=str,
            default='static/themes',
            help='Output directory for generated theme files'
        )
        parser.add_argument(
            '--no-minify',
            action='store_true',
            help='Skip CSS minification'
        )
        parser.add_argument(
            '--source-maps',
            action='store_true',
            help='Generate CSS source maps for debugging'
        )
        parser.add_argument(
            '--no-manifest',
            action='store_true',
            help='Skip manifest.json generation'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Verbose output'
        )

    def handle(self, *args, **options):
        """Execute the build command."""
        
        # Get options
        output_dir = options['output_dir']
        minify = not options['no_minify']
        source_maps = options['source_maps']
        manifest = not options['no_manifest']
        verbose = options['verbose']

        # Make output directory relative to Django project if not absolute
        if not os.path.isabs(output_dir):
            base_dir = getattr(settings, 'BASE_DIR', os.getcwd())
            output_dir = os.path.join(base_dir, output_dir)

        if verbose:
            self.stdout.write(f"Building themes to: {output_dir}")
            self.stdout.write(f"Minify: {minify}")
            self.stdout.write(f"Source maps: {source_maps}")
            self.stdout.write(f"Manifest: {manifest}")

        try:
            # Run the build process
            artifacts = build_themes(
                output_dir=output_dir,
                minify=minify,
                source_maps=source_maps,
                manifest=manifest
            )

            # Report results
            self.stdout.write(
                self.style.SUCCESS(f"✅ Theme build completed successfully!")
            )
            
            if verbose:
                self.stdout.write("Generated artifacts:")
                for artifact_type, paths in artifacts.items():
                    if isinstance(paths, list):
                        self.stdout.write(f"  {artifact_type}: {len(paths)} files")
                    else:
                        self.stdout.write(f"  {artifact_type}: {os.path.basename(paths)}")

            # Usage instructions
            self.stdout.write("\n📖 Usage Instructions:")
            self.stdout.write("1. Include the bundle in your HTML:")
            self.stdout.write('   <link rel="stylesheet" href="/static/themes/djust-theming-bundle.min.css">')
            self.stdout.write('   <script src="/static/themes/djust-theme-switcher.min.js"></script>')
            self.stdout.write("\n2. Switch themes with JavaScript:")
            self.stdout.write("   djustTheme.setTheme('brutalist', 'ocean')")
            self.stdout.write("   djustTheme.setThemeByName('elegant-sunset')")
            
        except Exception as e:
            raise CommandError(f"Theme build failed: {str(e)}")

        return artifacts