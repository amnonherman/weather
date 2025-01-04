import requests
api_key = "7f9c3335a0711025a0ab6941bfdb37f2"
def fetch_weather(city_name, api_key):
    """Fetch weather data for a given city using OpenWeatherMap API."""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
