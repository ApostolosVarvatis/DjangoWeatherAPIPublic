from django.shortcuts import render, HttpResponse
from django.utils import timezone

import datetime as dt
import meteomatics.api as api

from base.models import Location, DailyWeather, HourlyWeather

# API username - key
username = 'your_username'
password = 'your_key'


def index(request):
    return render(request, "base/index.html", {})


def load_data(request):

    # Delete all existing daily and hourly weather data
    DailyWeather.objects.all().delete()
    HourlyWeather.objects.all().delete()

    # Locations for weather data
    LOCATIONS = {
        "Thessaloniki" : [(40.64, 22.93)],
        "Athens" : [(37.97, 23.73)],
        "Larnaca" : [(34.92, 33.62)]
    }

    # Daily query parameters
    d_parameters = [
        "t_max_2m_24h:C",
        "t_min_2m_24h:C",

        "wind_gusts_10m_24h:ms",
        "precip_24h:mm",
        "weather_symbol_24h:idx",

        "msl_pressure:hPa",
        "uv:idx",
        "sunrise:sql",
        "sunset:sql"
    ]

    # Hourly query parameters
    h_parameters = [
        "t_2m:C",

        "wind_speed_10m:ms",
        "wind_dir_10m:d",
        "wind_gusts_10m_1h:ms",

        "precip_1h:mm",
        "weather_symbol_1h:idx"
    ]

    # Get request timeframe
    today = timezone.now()
    start_date = today - dt.timedelta(days=1)
    end_date = today + dt.timedelta(days=6)

    start_date = start_date.replace(microsecond=0, second=0, minute=0, hour=0)
    end_date = end_date.replace(microsecond=0, second=0, minute=0, hour=0)

    # Define weather data intervals 
    daily_interval = dt.timedelta(days=1)
    hourly_interval = dt.timedelta(hours=1)

   
    for location_name, coordinates in LOCATIONS.items():

        try:
            location, created = Location.objects.get_or_create(name=location_name)

            # Fetch daily data
            d_data = api.query_time_series(coordinates, start_date, end_date, daily_interval, d_parameters, username, password)

            # Process and store the daily data
            for index, row in d_data.iterrows():
                date = index[2]
                DailyWeather.objects.create(
                    location=location,
                    date=date,
                    temp_max=row['t_max_2m_24h:C'],
                    temp_min=row['t_min_2m_24h:C'],
                    wind_gust=row['wind_gusts_10m_24h:ms'],
                    precipitation=row['precip_24h:mm'],
                    weather_symbol=row['weather_symbol_24h:idx'],
                    sea_pressure=row['msl_pressure:hPa'],
                    uv_index=row['uv:idx'],
                    sunrise=row['sunrise:sql'],
                    sunset=row['sunset:sql']
                )
            

            # Fetch hourly data
            h_data = api.query_time_series(coordinates, start_date, end_date, hourly_interval, h_parameters, username, password)

            # Process and store the hourly data
            for index, row in h_data.iterrows():
                timestamp = index[2]
                HourlyWeather.objects.create(
                    location=location,
                    timestamp=timestamp,
                    temp=row['t_2m:C'],
                    wind_speed=row['wind_speed_10m:ms'],
                    wind_dir=row['wind_dir_10m:d'],
                    wind_gust=row['wind_gusts_10m_1h:ms'],
                    precipitation=row['precip_1h:mm'],
                    weather_symbol=row['weather_symbol_1h:idx'],
                )

        # Error cathcing
        except Exception as e:
            print(f"Failed to load data to database. Error: {e}")
            return HttpResponse(f"Failed to load data to database.")

    return HttpResponse("Data loaded successfully")


