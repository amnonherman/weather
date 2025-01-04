import streamlit as st
from weather_fetcher import fetch_weather
from date_time_utils import get_date_time_for_timezones

def weather_app():
    st.title("Weather Checker Application")
    api_key = "7f9c3335a0711025a0ab6941bfdb37f2"

    city_name = st.text_input("Enter city name:")
    user_timezone = "Europe/London"  # Replace this with your local timezone

    if st.button("Get Weather"):
        if city_name:
            result = fetch_weather(city_name, api_key)
            if result:
                weather_data = result["weather_data"]
                location_timezone_offset = result["location_timezone"]

                # Convert the timezone offset to a pytz-compatible timezone string
                location_timezone = f"Etc/GMT{int(-location_timezone_offset/3600)}"

                # Get local and location-specific times
                time_info = get_date_time_for_timezones(user_timezone, location_timezone)

                if "error" in time_info:
                    st.error(f"Time zone error: {time_info['error']}")
                else:
                    st.success(f"Weather data for {city_name.capitalize()}:")
                    st.write(f"Temperature: {weather_data['main']['temp']}°C")
                    st.write(f"Humidity: {weather_data['main']['humidity']}%")
                    st.write(f"Condition: {weather_data['weather'][0]['description'].capitalize()}")
                    st.write(f"Your Local Time: {time_info['user_time']}")
                    st.write(f"{city_name.capitalize()} Time: {time_info['location_time']}")
            else:
                st.error("City not found. Please check the name and try again.")
        else:
            st.warning("Please enter a city name.")
