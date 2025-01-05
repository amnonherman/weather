import streamlit as st
import requests
from datetime import datetime, timedelta
import json
import os

# OpenWeatherMap API key
API_KEY = "7f9c3335a0711025a0ab6941bfdb37f2"

# Path for the settings JSON file
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "settings.json")


def load_settings():
    """
    Load settings from the JSON file. If the file doesn't exist, create default settings.
    Returns:
        dict: The settings dictionary.
    """
    if not os.path.exists(SETTINGS_FILE):
        default_settings = {
            "default_location": None,
            "temperature_unit": "C",  # Default to Celsius
            "favorites": []
        }
        save_settings(default_settings)
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)


def save_settings(settings):
    """
    Save settings to the JSON file.
    Args:
        settings (dict): The settings dictionary to save.
    """
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)


def fetch_weather(city_name, unit="metric"):
    """
    Fetch weather details for the given city using OpenWeatherMap API.
    Args:
        city_name (str): The city name for which to fetch weather details.
        unit (str): Temperature unit ('metric' for Celsius, 'imperial' for Fahrenheit).
    Returns:
        dict: Weather details including temperature, humidity, description, and timezone offset.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units={unit}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "timezone_offset": data["timezone"],  # Offset in seconds from UTC
            "city": data["name"],
            "country": data["sys"]["country"]
        }
    else:
        return None


def get_local_time(timezone_offset):
    """
    Calculate the local time at the destination using the timezone offset.
    Args:
        timezone_offset (int): Offset in seconds from UTC.
    Returns:
        str: Formatted local time at the destination.
    """
    utc_time = datetime.utcnow()
    local_time = utc_time + timedelta(seconds=timezone_offset)
    return local_time.strftime("%A, %B %d, %Y, %I:%M %p")


def weather_app():
    """
    Main function to display the weather app interface.
    """
    # Display the banner using st.image
    st.image(
        "banner.png",  # Ensure this is the correct path
        use_container_width=True
    )

    # Load settings
    settings = load_settings()

    # Display favorite location buttons horizontally
    st.subheader("Your Favorite Locations:")
    if settings["favorites"]:
        cols = st.columns(len(settings["favorites"]))
        for i, favorite in enumerate(settings["favorites"]):
            with cols[i]:
                if st.button(f"{favorite}"):
                    st.session_state["city_name"] = favorite  # Set selected favorite city
                    st.session_state["weather_fetched"] = True

    # Main Weather Interface
    st.title("What's the Weather?")

    # Input box for city name
    city_name = st.text_input("Enter the name of a city:", placeholder="e.g., New York")

    # Button to fetch weather
    if st.button("Get Weather"):
        if city_name:
            st.session_state["city_name"] = city_name
            st.session_state["weather_fetched"] = True

    # Check if weather data should be fetched
    if "weather_fetched" in st.session_state and st.session_state["weather_fetched"]:
        # Determine city to fetch weather for
        city_to_fetch = st.session_state.get("city_name", "")
        if city_to_fetch:
            # Default unit: Celsius
            unit = "metric"
            weather_details = fetch_weather(city_to_fetch, unit=unit)

            if weather_details:
                # Display weather details
                st.success(f"Weather details for {weather_details['city']}, {weather_details['country']}:")

                # Display temperature with unit toggle below it
                selected_unit = st.radio(
                    "Choose temperature unit:",
                    options=["Celsius", "Fahrenheit"],
                    index=0,
                    horizontal=True,
                    key="temp_unit"
                )

                # Update temperature based on the selected unit
                if selected_unit == "Fahrenheit":
                    temperature = round(weather_details["temperature"] * 9 / 5 + 32, 2)
                    st.write(f"**Temperature:** {temperature}°F")
                else:
                    temperature = weather_details["temperature"]
                    st.write(f"**Temperature:** {temperature}°C")

                # Display other weather details
                st.write(f"**Humidity:** {weather_details['humidity']}%")
                st.write(f"**Condition:** {weather_details['description'].capitalize()}")

                # Display local time at the destination
                local_time = get_local_time(weather_details["timezone_offset"])
                st.write(f"**Local Time:** {local_time}")

                # Add to Favorites Button
                if city_to_fetch not in settings["favorites"]:
                    if st.button(f"Add {city_to_fetch} to Favorites"):
                        # Manage up to 5 favorites
                        if len(settings["favorites"]) >= 5:
                            settings["favorites"].pop(0)  # Remove oldest favorite
                        settings["favorites"].append(city_to_fetch)
                        save_settings(settings)
                        st.success(f"{city_to_fetch} added to favorites!")
                        # Reset state to re-render favorites
                        st.session_state["weather_fetched"] = False
                        st.rerun()  # Updated to st.rerun
            else:
                st.error("City not found. Please check the name and try again.")
        else:
            st.warning("Please enter a city name.")
