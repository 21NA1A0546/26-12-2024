from django.shortcuts import render
from django.core.cache import cache
from .utils import get_weather_data

# Define a cache timeout period (e.g., 1 hour)
CACHE_TIMEOUT = 3600

def index(request):
    context = {}
    if request.method == 'POST':
        location = request.POST.get('location')
        weather_data = get_cached_weather_data(location)
        if 'error' in weather_data:
            context['error'] = weather_data['error']
        else:
            context['weather_data'] = weather_data['data']['timelines'][0]['intervals'][0]['values']
            context['location'] = location  # Pass the location to the template
    return render(request, 'weather/index.html', context)

def compare(request):
    context = {}
    if request.method == 'POST':
        num_places = int(request.POST.get('num_places'))
        place_names = [request.POST.get(f'place_{i+1}') for i in range(num_places)]
        weather_data = []
        errors = []
        for place in place_names:
            data = get_cached_weather_data(place)
            if 'error' in data:
                errors.append(f"Error for {place}: {data['error']}")
            else:
                weather_data.append({
                    'place': place,
                    'data': data['data']['timelines'][0]['intervals'][0]['values']
                })

        context['weather_data'] = weather_data
        context['errors'] = errors
    return render(request, 'weather/compare.html', context)

def get_cached_weather_data(location):
    # Check if the data is already in the cache
    cache_key = f'weather_data_{location}'
    weather_data = cache.get(cache_key)
    if weather_data is None:
        # If not in cache, fetch the data from the API
        weather_data = get_weather_data(location)
        if 'error' not in weather_data:
            # Store the data in the cache
            cache.set(cache_key, weather_data, CACHE_TIMEOUT)
    return weather_data