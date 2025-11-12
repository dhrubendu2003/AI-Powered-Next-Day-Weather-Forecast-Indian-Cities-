import google.generativeai as genai
import os
from dotenv import load_dotenv

# 🔧 Load environment variables
load_dotenv()

def generate_ai_forecast(weather_info):
    """
    Uses Gemini to generate a conversational weather forecast
    """
    # 🔧 Get API key directly in this function
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    if not GEMINI_API_KEY:
        return "Error: Gemini API key not found. Please check your environment variables."
    
    try:
        # 🔧 Configure Gemini API dynamically
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
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

        Generate a short, helpful, and conversational 2-sentence weather forecast for tomorrow.
        Be friendly and add a tip if relevant (e.g., carry an umbrella, wear light clothes).
        Keep the tone casual and useful for daily planning.
        """

        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"Error in Gemini API call: {str(e)}")  # This will help debug
        return f"Sorry, I couldn't generate a forecast. API Error: {str(e)}"

if __name__ == "__main__":
    # Test the function with sample data
    sample_weather = {
        "city": "Mumbai",
        "date": "2025-11-13 12:00:00",
        "temp_max": 28.6,
        "temp_min": 24.7,
        "humidity": 54,
        "description": "clear sky",
        "rain_probability": 0.0,
        "wind_speed": 5.18,
        "pressure": 1012
    }
    
    forecast = generate_ai_forecast(sample_weather)
    print("Sample AI Forecast:")
    print(forecast)