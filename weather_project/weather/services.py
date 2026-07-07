import requests
import os
from typing import Any, Optional, Dict
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

API_KEY = os.environ.get('API_KEY')


def get_weather_data(city: str) -> Optional[Dict[str, Any]]:
    """Call OpenWeatherMap and return parsed JSON or a dict with an `error` key.

    Returns:
        dict: API response JSON on success, or {'error': ...} on failure.
    """
    if not API_KEY:
        return {"error": "Missing API key. Set the API_KEY environment variable."}

    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    try:
        response = requests.get(url, timeout=10)
    except requests.RequestException as exc:
        return {"error": f"Network error when contacting weather API: {exc}"}

    # Try to parse JSON error message when the status is not 200
    try:
        payload = response.json()
    except ValueError:
        return {"error": f"Unexpected non-JSON response (status {response.status_code})."}

    if response.status_code == 200:
        return payload

    # API returned an error payload (e.g., invalid API key, city not found)
    message = payload.get("message") or payload.get("error") or f"HTTP {response.status_code}"
    return {"error": message, "code": payload.get("cod", response.status_code)}


def get_weather(city: str) -> Optional[Dict[str, Any]]:
    """Compatibility wrapper used by views."""
    return get_weather_data(city)