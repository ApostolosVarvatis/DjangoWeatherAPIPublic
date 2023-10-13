from rest_framework import serializers
from base.models import Location, DailyWeather, HourlyWeather

# Serializers for all models in base.models

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class DailyWeatherSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = DailyWeather
        fields = '__all__'

class HourlyWeatherSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = HourlyWeather
        fields = '__all__'
