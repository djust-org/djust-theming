"""
ASGI config for example_project.
"""

import os
from djust.asgi import get_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'example_project.settings')

application = get_application()