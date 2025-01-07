import streamlit as st
import requests
from datetime import datetime, timedelta
import json
import os
import folium
from streamlit_folium import folium_static
from weather_fetcher import fetch_weather
from get_coordinates import get_coordinates

# OpenWeatherMap API key
API_KEY = st.secrets["openweathermap"]["api_key"]

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
        city_to_fetch = st.session_state.get("city_name", "")
        if city_to_fetch:
            weather_details = fetch_weather(city_to_fetch)

            # Debugging: Display weather details
            # st.write("Debugging Weather Details:", weather_details) # Removed Debug Output

            if weather_details:
                # Display weather details
                st.success(f"Weather details for {weather_details['city']}, {weather_details['country']}:")

                # Display the weather condition and icon in a box
                with st.container():
                    col1, col2 = st.columns([1, 3])  # Create two columns, first for the icon and the second for description

                    with col1:
                        icon_code = weather_details["icon"]
                        icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
                        st.image(icon_url, width=80)  # Adjust width for better appearance
                    with col2:
                        st.subheader(f"{weather_details['description'].capitalize()}")

                # Allow the user to toggle between Celsius and Fahrenheit
                selected_unit = st.radio(
                    "Choose temperature unit:",
                    options=["Celsius", "Fahrenheit"],
                    index=0,
                    horizontal=True,
                    key="temp_unit"
                )

                # Update temperature based on selected unit
                temperature = weather_details["temperature"]
                if selected_unit == "Fahrenheit":
                    temperature = round(weather_details["temperature"] * 9 / 5 + 32, 2)
                    st.write(f"**Temperature:** {temperature}°F")
                else:
                    st.write(f"**Temperature:** {temperature}°C")

                # Display other weather details
                st.write(f"**Humidity:** {weather_details['humidity']}%")

                # Display local time at the destination
                local_time = get_local_time(weather_details["timezone_offset"])
                st.write(f"**Local Time:** {local_time}")

                # Add to Favorites Button
                if city_to_fetch not in settings["favorites"]:
                    if st.button(f"Add {city_to_fetch} to Favorites"):
                        # Manage up to 5 favorites
                        if len(settings["favorites"]) >= 5:
                            settings["favorites"].pop(0)  # Remove the oldest favorite
                        settings["favorites"].append(city_to_fetch)
                        save_settings(settings)
                        st.success(f"{city_to_fetch} added to favorites!")
                        st.session_state["weather_fetched"] = False
                        st.rerun()

                # Display interactive map if coordinates are available
                coordinates = get_coordinates(city_to_fetch)
                if coordinates and weather_details:  # Ensure weather_details also exists
                    latitude = coordinates["lat"]
                    longitude = coordinates["lon"]
                    icon_code = weather_details["icon"]
                    icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
                    popup_content = f"""
                        <div style="display: flex; flex-direction: column; align-items: center;">
                            <img src="{icon_url}" alt="Weather Icon" style="width: 50px; height: 50px;">
                            <p style="margin: 0; font-weight: bold;"></p>
                        </div>
                    """
                    location_map = folium.Map(location=[latitude, longitude], zoom_start=10)
                    folium.Marker(
                        [latitude, longitude],
                        popup=popup_content,
                        icon=folium.DivIcon(html=popup_content, icon_size=(60, 60), icon_anchor = (30, 55)), # Reduced icon size and anchor
                    ).add_to(location_map)
                    folium_static(location_map)
                else:
                    st.error("Unable to fetch coordinates for this location.")
            else:
                st.error("City not found. Please check the name and try again.")
        else:
            st.warning("Please enter a city name.")