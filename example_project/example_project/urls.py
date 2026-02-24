"""
URL configuration for example_project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('theming/', include('djust_theming.urls')),
    path('', include('theme_demo.urls')),
]
