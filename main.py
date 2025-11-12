import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

# Load .env file
load_dotenv()

from src.weather_api import get_weather_data
from src.gemini_api import generate_ai_forecast

def main():
    """Main function for command-line interface"""
    print("AI-Powered Weather Forecast for Indian Cities")
    city = input("Enter an Indian city name: ")
    
    weather_data = get_weather_data(city)
    
    if weather_data:
        print("\nRaw Weather Data:")
        print(weather_data)
        
        print("\nAI-Generated Forecast:")
        ai_forecast = generate_ai_forecast(weather_data)
        print(ai_forecast)
    else:
        print("Could not retrieve weather data.")

def streamlit_app():
    """Streamlit web interface for the weather forecast app"""
    st.title("🌤️ AI-Powered Weather Forecast for Indian Cities")
    st.markdown("Get conversational weather forecasts powered by Gemini AI!")
    
    city = st.text_input("Enter an Indian City Name:", "Mumbai")
    
    if st.button("Get Forecast"):
        with st.spinner(f"Fetching weather data for {city}..."):
            weather_data = get_weather_data(city)
        
        if weather_data:
            st.subheader(f"📊 Weather for {weather_data['city']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Max Temp", f"{weather_data['temp_max']}°C")
                st.metric("Humidity", f"{weather_data['humidity']}%")
            with col2:
                st.metric("Min Temp", f"{weather_data['temp_min']}°C")
                st.metric("Rain Probability", f"{weather_data['rain_probability']}%")
            
            st.write(f"**Weather Condition**: {weather_data['description'].title()}")
            st.write(f"**Forecast Date**: {weather_data['date']}")
            
            with st.spinner("Generating AI forecast..."):
                ai_forecast = generate_ai_forecast(weather_data)
            
            st.subheader("🤖 AI Forecast:")
            st.info(ai_forecast)
        else:
            st.error("Could not retrieve weather data. Please check the city name and try again.")

if __name__ == "__main__":
    # For Streamlit deployment
    streamlit_app()
    
    # For command-line interface:
    main()