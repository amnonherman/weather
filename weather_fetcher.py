import requests
from get_coordinates import get_coordinates

API_KEY = st.secrets["openweathermap"]["api_key"]

def fetch_weather(city_name, unit="metric"):
    """
    Fetch weather details for the given city using OpenWeatherMap API.
    Args:
        city_name (str): The city name for which to fetch weather details.
        unit (str): Temperature unit ('metric' for Celsius, 'imperial' for Fahrenheit).
    Returns:
        dict: Weather details including temperature, humidity, description, coordinates, etc.
    """
    # Get coordinates for the city
    coordinates = get_coordinates(city_name)
    if not coordinates:
        return None  # Return None if city is not found

    # Use coordinates to fetch weather details
    lat, lon = coordinates["lat"], coordinates["lon"]
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units={unit}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_data = {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "timezone_offset": data["timezone"],
            "city": data["name"],
            "country": data["sys"]["country"],
            "icon": data["weather"][0]["icon"]  # Get the icon code
        }
        weather_data["coord"] = coordinates
        return weather_data
    else:
        return None