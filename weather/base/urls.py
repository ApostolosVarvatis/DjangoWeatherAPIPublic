from django.urls import path

from . import views

urlpatterns = [
    # Index view
    path("", views.index, name="index"),

    # Load data route for AJAX request
    path("load_data/", views.load_data, name="load_data"),
]