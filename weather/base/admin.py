from django.contrib import admin
from .models import Location, DailyWeather, HourlyWeather

# Registered the models here for admin usage
admin.site.register(Location)
admin.site.register(DailyWeather)
admin.site.register(HourlyWeather)