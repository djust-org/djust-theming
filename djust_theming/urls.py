from django.urls import path

from . import views

app_name = "djust_theming"

urlpatterns = [
    path("theme.css", views.theme_css_view, name="theme_css"),
]
