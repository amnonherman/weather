import requests
api_key = "7f9c3335a0711025a0ab6941bfdb37f2"
def fetch_weather(city_name, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "weather_data": data,
            "location_timezone": data.get("timezone")  # Time zone offset in seconds
        }
    else:
        return None


