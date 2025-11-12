import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('models/gemini-2.0-flash-001')
else:
    print("Error: Gemini API key not found in .env file")
    model = None

def generate_ai_forecast(weather_info):
    """
    Uses Gemini to generate a conversational weather forecast
    """
    if not model:
        return "Error: Gemini API not configured. Please check your API key."
    
    # Handle wind_speed: convert 'N/A' to 'not available' or a number
    wind_speed = weather_info['wind_speed']
    if wind_speed == 'N/A':
        wind_speed_str = 'not available'
    else:
        wind_speed_str = f"{wind_speed} m/s"
    
    prompt = f"""
You are a friendly weather assistant for India. Based on the following forecast data for {weather_info['city']} for **TOMORROW** ({weather_info['date']}):
- Max Temperature: {weather_info['temp_max']}°C
- Min Temperature: {weather_info['temp_min']}°C
- Humidity: {weather_info['humidity']}%
- Rain Probability: {weather_info['rain_probability']}%
- Weather: {weather_info['description']}
- Wind Speed: {wind_speed_str}
- Pressure: {weather_info['pressure']} hPa

Generate a short, helpful, and conversational 2-sentence weather forecast **for tomorrow**.
Be friendly and add a tip if relevant (e.g., carry an umbrella, wear light clothes).
Keep the tone casual and useful for daily planning.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating AI forecast: {str(e)}")
        # Try a simpler prompt as fallback
        fallback_prompt = f"""
        You are a friendly weather assistant. The weather for {weather_info['city']} on {weather_info['date']} will be {weather_info['description']} with max temperature {weather_info['temp_max']}°C and rain probability {weather_info['rain_probability']}%. Generate a short 2-sentence forecast.
        """
        try:
            response = model.generate_content(fallback_prompt)
            return response.text
        except Exception as fallback_error:
            print(f"Fallback also failed: {str(fallback_error)}")
            return "Sorry, I couldn't generate a forecast at the moment. Please try again."

if __name__ == "__main__":
    # Test the function with sample data
    sample_weather = {
        "city": "Mumbai",
        "date": "2025-11-06 12:00:00",
        "temp_max": 32.5,
        "temp_min": 24.1,
        "humidity": 75,
        "description": "clear sky",
        "rain_probability": 0.0,
        "wind_speed": 3.5,
        "pressure": 1012
    }
    
    forecast = generate_ai_forecast(sample_weather)
    print("Sample AI Forecast:")
    print(forecast)