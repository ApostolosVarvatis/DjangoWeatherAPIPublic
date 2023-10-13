from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Avg

from base.models import Location, DailyWeather, HourlyWeather
from base.views import load_data
from .serializers import LocationSerializer

from django.utils import timezone
from datetime import timedelta


@api_view(['GET'])
def getLocations(request):
    locations = Location.objects.all()
    seriliazer = LocationSerializer(locations, many=True)
    return Response(seriliazer.data)


@api_view(['GET'])
def getLatestForecast(request):

    # Reload the data on each call to the api
    # If you want to keep previously fetched data comment next line out
    load_data(request)

    current_time = timezone.now()
    locations = Location.objects.all()

    combined_data_all_locations = []

    for location in locations:
        # Looping through all days in the database and extracting data
        for day in range(-1, 6):
            day_start = current_time + timedelta(days=day)
            day_start = day_start.replace(hour=current_time.hour, minute=0, second=0, microsecond=0)

            # Get the latest hourly forecast for the current hour for the day_start day
            latest_hourly_weather = HourlyWeather.objects.filter(
                location=location,
                timestamp__date=day_start.date(),
                timestamp__hour=current_time.hour
            ).order_by('-timestamp').first()

            # Get the daily weather for the day_start date
            daily_weather = DailyWeather.objects.filter(location=location, date=day_start.date()).first()

            # Combine the relevant information for the location
            combined_data_location = {
                'location_id': location.id,
                'location_name': location.name,
                'current_date': day_start.date(),
                'current_hour': current_time.hour,
                'latest_hourly_weather': {
                    'timestamp': latest_hourly_weather.timestamp,
                    'temprature': latest_hourly_weather.temp,
                    'wind_speed': latest_hourly_weather.wind_speed,
                    'wind_direction': latest_hourly_weather.wind_dir,
                    'hourly_wind_gust': latest_hourly_weather.wind_gust,
                    'hourly_precipitation': latest_hourly_weather.precipitation,
                    'hourly_weather_symbol': latest_hourly_weather.weather_symbol,
                },
                'daily_weather': {
                    'temp_max': daily_weather.temp_max,
                    'temp_min': daily_weather.temp_min,
                    'daily_wind_gust': daily_weather.wind_gust,
                    'daily_precipitation': daily_weather.precipitation,
                    'daily_weather_symbol': daily_weather.weather_symbol,
                    'sea_pressure': daily_weather.sea_pressure,
                    'uv_index': daily_weather.uv_index,
                    'sunrise': daily_weather.sunrise,
                    'sunset': daily_weather.sunset,
                }
            }

            combined_data_all_locations.append(combined_data_location)

    return Response(combined_data_all_locations)


@api_view(['GET'])
def getAverageTemp(request):

    # Reload the data on each call to the api
    # If you want to keep previously fetched data comment next line out
    load_data(request)

    result = []
    locations = Location.objects.all()

    today = timezone.now()

    for location in locations:
        # Looping through all days in the database and extracting data
        for day in range(-1, 6):
            # Defining timeframe for average temprature
            day_start = today + timedelta(days=day)
            day_start = day_start.replace(hour=today.hour, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(hours=23, minutes=59, seconds=59)

            # Limiting results to the last 3 forecasts / last 3 hours
            last_3_forecasts = HourlyWeather.objects.filter(
                location=location,
                timestamp__gte=day_start,
                timestamp__lte=day_end
            ).order_by('-timestamp')[:3]

            avg_temp = last_3_forecasts.aggregate(Avg('temp'))['temp__avg']

            result.append({
                'location_id': location.id,
                'location_name': location.name,
                'timestamp': day_start,
                'average_temp_last_3_forecasts': avg_temp
            })

    return Response(result)


@api_view(['GET'])
def getTopN(request):

    # Reload the data on each call to the api
    # If you want to keep previously fetched data comment next line out
    load_data(request)

    # Validating user input
    n = request.query_params.get('n', 3)
    try:
        n = int(n)
    except ValueError:
        return Response({'error': 'Invalid value for parameter n'}, status=400)

    if int(n) > 3:
        return Response({'error': 'Invalid value for parameter n'}, status=422)

    # Metrics to consider
    metrics = ['temp_max', 'temp_min', 'wind_gust', 'precipitation', 'weather_symbol', 'sea_pressure', 'uv_index']

    top_locations = {}

    for metric in metrics:
        # Calculate the average value for the metric for each location
        avg_values = DailyWeather.objects.values('location__id', 'location__name').annotate(
            avg_metric=Avg(metric)
        ).order_by('-avg_metric')[:n]

        # Add the results to the top_locations dictionary
        top_locations[metric] = list(avg_values)

    return Response(top_locations)