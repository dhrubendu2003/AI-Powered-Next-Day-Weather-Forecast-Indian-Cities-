import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

# 🔍 DEBUG: Show current working directory and file locations
current_dir = Path.cwd()
script_dir = Path(__file__).parent
env_path = script_dir / ".env"

print(f"=== DEBUG INFO ===")
print(f"Current working directory: {current_dir}")
print(f"Script directory: {script_dir}")
print(f"Looking for .env at: {env_path}")
print(f".env file exists: {env_path.exists()}")
print(f"Files in current directory: {list(current_dir.iterdir())}")
print(f"Files in script directory: {list(script_dir.iterdir())}")
print(f"=== END DEBUG ===")

# 🔒 Load .env from the same directory as main.py (works for Streamlit AND CLI)
load_dotenv(dotenv_path=env_path)

# 🔍 DEBUG: Check if keys are loaded after loading
weather_key = os.getenv("OPENWEATHER_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

print(f"OpenWeather key loaded: {'Yes' if weather_key else 'No'}")
print(f"Gemini key loaded: {'Yes' if gemini_key else 'No'}")

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
    
    # 🔍 Debug: Show if API keys are loaded (for development only)
    weather_key = os.getenv("OPENWEATHER_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    st.write(f"**Current directory**: `{Path.cwd()}`")
    st.write(f"**Script directory**: `{Path(__file__).parent}`")
    st.write(f"**Looking for .env at**: `{Path(__file__).parent / '.env'}`")
    st.write(f"**.env exists**: `{(Path(__file__).parent / '.env').exists()}`")
    st.write(f"**OpenWeather key loaded**: `{'Yes' if weather_key else 'No'}`")
    st.write(f"**Gemini key loaded**: `{'Yes' if gemini_key else 'No'}`")
    
    if not weather_key or not gemini_key:
        st.error("⚠️ API keys not loaded! Check if .env file exists in the project root.")
        st.stop()
    
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
    # main()