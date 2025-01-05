import streamlit as st
import requests
from datetime import datetime, timedelta
import os

# OpenWeatherMap API key
API_KEY = "7f9c3335a0711025a0ab6941bfdb37f2"

# Get the absolute path of the banner image
BANNER_PATH = os.path.join(os.path.dirname(__file__), "banner.png")


def fetch_weather(city_name):
    """
    Fetch weather details for the given city using OpenWeatherMap API.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
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
    """
    utc_time = datetime.utcnow()
    local_time = utc_time + timedelta(seconds=timezone_offset)
    return local_time.strftime("%A, %B %d, %Y, %I:%M %p")


def weather_app():
    """
    Main function to display the weather app interface.
    """
    # Display the banner image using HTML and CSS for full-width
    st.markdown(
        f"""
        <style>
        .full-width-banner {{
            width: 100%;
            height: auto;
            margin-bottom: 20px;
        }}
        </style>
        <div style="text-align: center;">
            <img src="data:image/png;base64,{get_image_as_base64(BANNER_PATH)}" class="full-width-banner" alt="Weather Banner">
        </div>
        """,
        unsafe_allow_html=True
    )

    # Title and input
    st.title("What's the Weather?")
    city_name = st.text_input(
        "Enter the name of a city:",
        placeholder="e.g., New York, Tokyo, London"
    )

    # Fetch weather details when the user submits
    if st.button("Get Weather"):
        if city_name:
            weather_details = fetch_weather(city_name)
            if weather_details:
                # Display weather details
                st.success(f"Weather details for {weather_details['city']}, {weather_details['country']}:")
                st.write(f"**Temperature:** {weather_details['temperature']}°C")
                st.write(f"**Humidity:** {weather_details['humidity']}%")
                st.write(f"**Condition:** {weather_details['description'].capitalize()}")

                # Display local time at the destination
                local_time = get_local_time(weather_details["timezone_offset"])
                st.write(f"**Local Time:** {local_time}")
            else:
                st.error("City not found. Please check the name and try again.")
        else:
            st.warning("Please enter a city name.")


def get_image_as_base64(image_path):
    """
    Convert the image at the given path to a base64 string for embedding in HTML.
    """
    import base64
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")
