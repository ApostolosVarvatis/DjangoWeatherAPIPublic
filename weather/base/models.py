from django.db import models

# Model for Location defined in base/views.load_data
class Location(models.Model):
    name = models.CharField(max_length=255)

# Model for Daily Weather attributes regardless of time
class DailyWeather(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date = models.DateTimeField()

    temp_max = models.FloatField()
    temp_min = models.FloatField()

    wind_gust = models.FloatField()
    precipitation = models.FloatField()
    weather_symbol = models.IntegerField()

    sea_pressure = models.FloatField()
    uv_index = models.FloatField()
    sunrise = models.DateTimeField()
    sunset = models.DateTimeField()

# Model for Hourly Weather attributes
class HourlyWeather(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()

    temp = models.FloatField()

    wind_speed = models.FloatField()
    wind_dir = models.FloatField()
    wind_gust = models.FloatField()

    precipitation = models.FloatField()
    weather_symbol = models.IntegerField()
