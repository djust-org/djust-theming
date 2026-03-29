from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'theme_demo'

urlpatterns = [
    # Primary pages
    path('', views.index, name='index'),
    path('components/', views.components, name='components'),
    path('themes/', views.themes, name='themes'),
    path('packs/', views.packs, name='packs'),

    # Documentation
    path('docs/', views.docs, name='docs'),
    path('integration/', views.integration, name='integration'),

    # Tools
    path('inspector/', views.theme_inspector_view, name='inspector'),
    path('landing/', views.landing, name='landing'),

    # API endpoints (used by inspector)
    path('theme-inspector-api/', views.theme_inspector_api, name='inspector_api'),
    path('theme-css-api/', views.theme_css_api, name='css_api'),

    # Redirects for old URLs
    path('design-systems/', RedirectView.as_view(pattern_name='theme_demo:themes', permanent=True)),
    path('presets/', RedirectView.as_view(pattern_name='theme_demo:themes', permanent=True)),
    path('tailwind/', RedirectView.as_view(pattern_name='theme_demo:index', permanent=True)),
    path('forms/', RedirectView.as_view(pattern_name='theme_demo:components', permanent=True)),
    path('layouts/', RedirectView.as_view(pattern_name='theme_demo:docs', permanent=True)),
    path('pages/', RedirectView.as_view(pattern_name='theme_demo:docs', permanent=True)),
    path('djust-components/', RedirectView.as_view(pattern_name='theme_demo:components', permanent=True)),
]
