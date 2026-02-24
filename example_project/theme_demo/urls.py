from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'theme_demo'

urlpatterns = [
    path('', views.index, name='index'),
    path('components/', views.components, name='components'),
    path('presets/', views.presets, name='presets'),
    # Redirect old themes URL to design-systems
    path('themes/', RedirectView.as_view(pattern_name='theme_demo:design_systems', permanent=True), name='themes'),
    path('packs/', views.packs, name='packs'),
    path('design-systems/', views.design_systems, name='design_systems'),
    path('inspector/', views.theme_inspector_view, name='inspector'),
    path('theme-inspector-api/', views.theme_inspector_api, name='inspector_api'),
    path('theme-css-api/', views.theme_css_api, name='css_api'),
    path('tailwind/', views.tailwind_demo, name='tailwind'),
]
