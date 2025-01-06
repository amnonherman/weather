import requests
API_KEY = "7f9c3335a0711025a0ab6941bfdb37f2"
def get_coordinates(city_name):
    """
    Get geographical coordinates for a city using OpenWeatherMap's Geocoding API.
    """
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print("Geocoding API Response:", data)  # Debugging line
        if len(data) > 0:
            return {"lat": data[0]["lat"], "lon": data[0]["lon"]}
    print(f"Failed to get coordinates for city: {city_name}")
    return None
