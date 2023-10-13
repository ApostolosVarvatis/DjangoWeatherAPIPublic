from django.urls import path

from . import views

# Urls for API endpoints
urlpatterns = [
    path("getLocations", views.getLocations, name="getLocations"),
    path("getLatestForecast", views.getLatestForecast, name="getLatestForecast"),
    path("getAverageTemp", views.getAverageTemp, name="getAverageTemp"),
    path("getTopN", views.getTopN, name="getTopN")
]