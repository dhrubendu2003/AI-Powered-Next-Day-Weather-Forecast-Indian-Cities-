import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def get_weather_data(city):
    """
    Fetches TOMORROW'S weather forecast with accurate min/max temps
    """
    WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    if not WEATHER_API_KEY:
        print("Error: OpenWeatherMap API key not found")
        return None

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city},IN&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        print(f"API Error: {data.get('message', 'Unknown')}")
        return None

    # Calculate tomorrow's date
    tomorrow = (datetime.utcnow() + timedelta(days=1)).strftime('%Y-%m-%d')
    print(f"Looking for forecasts for: {tomorrow}")

    # Collect ALL forecasts for tomorrow
    tomorrow_forecasts = []
    for item in data['list']:
        forecast_date = item['dt_txt'].split(' ')[0]
        if forecast_date == tomorrow:
            tomorrow_forecasts.append(item)

    if not tomorrow_forecasts:
        print("No forecast data found for tomorrow")
        return None

    # Extract all temperatures from tomorrow's forecasts
    temps = [item['main']['temp'] for item in tomorrow_forecasts]
    rain_probs = [item.get('pop', 0) for item in tomorrow_forecasts]

    # Now calculate true min and max
    temp_max = round(max(temps), 1)
    temp_min = round(min(temps), 1)
    avg_rain_prob = round(sum(rain_probs) / len(rain_probs) * 100, 1)

    # Pick one representative entry (e.g., noon) for other details
    target_time = "12:00:00"
    best_forecast = min(
        tomorrow_forecasts,
        key=lambda x: abs(
            datetime.strptime(x['dt_txt'], '%Y-%m-%d %H:%M:%S').timestamp() -
            datetime.strptime(f"{tomorrow} {target_time}", '%Y-%m-%d %H:%M:%S').timestamp()
        )
    )

    weather_info = {
        "city": data['city']['name'],
        "date": best_forecast['dt_txt'],  # Tomorrow at ~12:00 PM
        "temp_max": temp_max,           # True daily max
        "temp_min": temp_min,           # True daily min
        "humidity": best_forecast['main']['humidity'],
        "description": best_forecast['weather'][0]['description'],
        "rain_probability": avg_rain_prob,
        "wind_speed": best_forecast.get('wind', {}).get('speed', 'N/A'),
        "pressure": best_forecast['main']['pressure']
    }
    return weather_info