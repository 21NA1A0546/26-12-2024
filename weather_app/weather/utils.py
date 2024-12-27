# weather/utils.py
import requests

API_KEY = 'aoGOJCzkTDP9IN6oc3aRgqW1QecbrbBe'  # Replace with your actual Tomorrow.io API key
BASE_URL = 'https://api.tomorrow.io/v4/timelines'

def get_weather_data(location):
    try:
        params = {
            'apikey': API_KEY,
            'location': location,
            'fields': [
                'temperature', 'temperatureApparent', 'pressureSurfaceLevel', 'pressureSeaLevel',
                'precipitationIntensity', 'humidity', 'windSpeed', 'windDirection',
                'rainIntensity', 'snowIntensity'
            ],
            'timesteps': ['1h', '1d'],
            'units': 'metric',
            'timezone': 'auto',
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}