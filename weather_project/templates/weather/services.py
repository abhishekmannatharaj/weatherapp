import requests
import os

API_KEY = os.environ.get('API_KEY')

def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_weather(city):
    """Compatibility wrapper used by views: returns the same as get_weather_data."""
    return get_weather_data(city)