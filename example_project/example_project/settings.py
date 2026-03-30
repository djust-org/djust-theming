"""
Django settings for example_project.

Demonstrates djust-theming integration.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-example-key-change-in-production')

DEBUG = os.environ.get('DJANGO_DEBUG', 'true').lower() not in ('false', '0', 'no')

_allowed = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
# Include pod IP for k8s kubelet health probes
_pod_ip = os.environ.get('POD_IP', '')
ALLOWED_HOSTS = [h.strip() for h in _allowed if h.strip()] + ([_pod_ip] if _pod_ip else [])

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get('CSRF_TRUSTED_ORIGINS', 'https://theming.djust.org').split(',')
    if origin.strip()
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # djust-theming (required)
    'djust_theming',

    # djust-components
    'djust_components',

    # Demo app
    'theme_demo',
]

# Optional: uncomment for djust LiveView support
# INSTALLED_APPS = ['daphne', 'channels', 'djust'] + INSTALLED_APPS
# ASGI_APPLICATION = 'example_project.asgi.application'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'example_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # djust-theming context processor
                'djust_theming.context_processors.theme_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'example_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'djust_theming': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# djust-theming configuration
LIVEVIEW_CONFIG = {
    'theme': {
        'preset': 'djust',  # Default preset (19 available)
        'default_mode': 'system',  # light, dark, or system
        'persist_in_session': True,
        'enable_dark_mode': True,
        'css_prefix': '',  # Optional CSS class prefix for isolation
        'critical_css': True,  # Split CSS into critical/deferred
        'use_css_layers': True,  # Enable CSS cascade layers
        'direction': 'ltr',  # Text direction: 'ltr' or 'rtl'
        'themes_dir': '',  # Custom themes directory
    }
}
