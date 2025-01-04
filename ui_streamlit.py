import streamlit as st
from weather_fetcher import fetch_weather

def weather_app():
    """Streamlit application for checking weather."""
    st.title("Weather Checker Application")
    api_key = "7f9c3335a0711025a0ab6941bfdb37f2"

    city_name = st.text_input("Enter city name:")

    if st.button("Get Weather"):
        if city_name:
            weather_data = fetch_weather(city_name, api_key)
            if weather_data:
                st.success(f"Weather data for {city_name.capitalize()}:")
                st.write(f"Temperature: {weather_data['main']['temp']}°C")
                st.write(f"Humidity: {weather_data['main']['humidity']}%")
                st.write(f"Condition: {weather_data['weather'][0]['description'].capitalize()}")
            else:
                st.error("City not found. Please check the name and try again.")
        else:
            st.warning("Please enter a city name.")
