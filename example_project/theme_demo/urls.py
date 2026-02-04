from django.urls import path
from . import views

app_name = 'theme_demo'

urlpatterns = [
    path('', views.index, name='index'),
    path('components/', views.components, name='components'),
    path('presets/', views.presets, name='presets'),
    path('themes/', views.themes, name='themes'),
    path('packs/', views.packs, name='packs'),
    path('tailwind/', views.tailwind_demo, name='tailwind'),
]
