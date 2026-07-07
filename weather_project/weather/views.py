from django.shortcuts import render
from .forms import CityForm
from .services import get_weather

def home(request):
    weather_data = None
    form = CityForm()

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            data = get_weather(city)

            # If the service returned a structured error, surface it to the template
            if isinstance(data, dict) and data.get("error"):
                weather_data = {"error": data.get("error")}
            # Some APIs return 'cod' as int or string; normalize and check for 200
            elif data and str(data.get("cod", "200")) == "200":
                weather_data = {
                    "city": data.get("name"),
                    "country": data.get("sys", {}).get("country"),
                    "temperature": data.get("main", {}).get("temp"),
                    "feels_like": data.get("main", {}).get("feels_like"),
                    "humidity": data.get("main", {}).get("humidity"),
                    "pressure": data.get("main", {}).get("pressure"),
                    "description": data.get("weather", [{}])[0].get("description"),
                    "icon": data.get("weather", [{}])[0].get("icon"),
                    "wind": data.get("wind", {}).get("speed"),
                }
            else:
                weather_data = {"error": "City not found or API error."}

    return render(request, 'weather/home.html', {'form': form, 'weather': weather_data})