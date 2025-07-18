import sys
import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# from MCPTools.server import mcp
# from MCPTools.loader.loader import *

from ..server import mcp
from ..loader import *
from typing import Dict, Any
import requests
from ..get_weather import *
@mcp.tool()
def get_weather(city: str, current: Any = True, forecast: Any = False, days: Any = 1, forecast_type: str = "daily", day_for_hourly: Any = 0) -> dict[str, Any]:
    """
    Fetches weather data from WeatherAPI.

    Args:
        city (str): City name.
        current (Any): Get current weather. Default is True. Can be boolean or string.
        forecast (Any): Get forecast. Default is False. Can be boolean or string.
        days (Any): Total forecast days (if forecast=True). Must be at least 1. For hourly forecast, must be > day_for_hourly.
        forecast_type (str): Type of forecast to get ("daily" or "hourly"). Only works if forecast=True.
        day_for_hourly (Any): Day for hourly forecast (if forecast_type="hourly"). 0 is today, 1 is tomorrow, etc.
                              Must be less than days parameter.
    Returns:
        dict: Weather data or error.
    """
    try:
        # Convert types more robustly
        def to_bool(value: Any) -> bool:
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                return value.lower() in ('true', 't', 'yes', 'y', '1')
            return bool(value)

        def to_int(value: Any) -> int:
            if isinstance(value, int):
                return value
            if isinstance(value, str):
                return int(float(value))  # handles both "1" and "1.0"
            return int(value)

        # Convert input types
        current = to_bool(current)
        forecast = to_bool(forecast)
        days = to_int(days)
        day_for_hourly = to_int(day_for_hourly)
        forecast_type = str(forecast_type).lower().strip()

        # Validate parameters
        if days < 1:
            return {"error": "Days parameter must be at least 1"}
        
        if forecast_type not in ["daily", "hourly"]:
            return {"error": "forecast_type must be either 'daily' or 'hourly'"}
        
        if forecast_type == "hourly":
            if day_for_hourly >= days:
                # Automatically adjust days if needed
                days = day_for_hourly + 1
                print(f"Adjusted forecast days to {days} to accommodate hourly forecast request")
            elif day_for_hourly < 0:
                return {"error": "day_for_hourly cannot be negative"}

        current_response = None
        forecast_response = None
        if current and not forecast:
            current_response = requests.post(f"https://api.weatherapi.com/v1/current.json",
                             params={"key": weather_api_key,
                                     "q": city,
                                     "aqi": "yes",
                                     "tides": "yes",
                                     "alerts": "yes",
                                     })
            if current_response.status_code != 200:
                return {"error": "Failed to get current weather data"}
            else:
                data = load_data_current(current_response.json())
                return {
                    "current": data
                }
            
        elif forecast and not current:
            forecast_response = requests.post(f"https://api.weatherapi.com/v1/forecast.json",
                             params={"key": weather_api_key,
                                     "q": city,
                                     "aqi": "yes",
                                     "tides": "yes",
                                     "alerts": "yes",
                                     "days": days
                                     })
            if forecast_response.status_code != 200:
                return {"error": "Failed to get forecast weather data"}
            else:
                if forecast_type.lower().strip() == "daily":
                    data = load_daily_data_forecast(forecast_response.json())
                elif forecast_type.lower().strip() == "hourly":
                    if day_for_hourly < days:
                        data = load_hourly_data_forecast(forecast_response.json()['forecast']['forecastday'][day_for_hourly])
                    else:
                        return {"error": "Day for hourly forecast is greater than the number of days"}
                return {
                    "forecast": data
                }
        
        elif current and forecast:
            current_response = requests.post(f"https://api.weatherapi.com/v1/current.json",
                             params={"key": weather_api_key,
                                     "q": city,
                                     "aqi": "yes",
                                     "tides": "yes",
                                     "alerts": "yes",
                                     })
            
            forecast_response = requests.post(f"https://api.weatherapi.com/v1/forecast.json",
                             params={"key": weather_api_key,
                                     "q": city,
                                     "aqi": "yes",
                                     "tides": "yes",
                                     "alerts": "yes",
                                     "days": days
                                     })
            
            if current_response.status_code == 200 and forecast_response.status_code == 200:
                if forecast_type.lower().strip() == "daily":
                    data = load_daily_data_forecast(forecast_response.json())
                elif forecast_type.lower().strip() == "hourly":
                    if day_for_hourly < days:
                        data = load_hourly_data_forecast(forecast_response.json()['forecast']['forecastday'][day_for_hourly])
                    else:
                        return {"error": "Day for hourly forecast is greater than the number of days"}
                return {
                    "current": load_data_current(current_response.json()),
                    "forecast": data
                }
            
            if current_response.status_code != 200 or forecast_response.status_code != 200:
                if current_response.status_code != 200 and forecast_response.status_code == 200:
                    if forecast_type.lower().strip() == "daily":
                        data = load_daily_data_forecast(forecast_response.json())
                    elif forecast_type.lower().strip() == "hourly":
                        if day_for_hourly < days:
                            data = load_hourly_data_forecast(forecast_response.json()['forecast']['forecastday'][day_for_hourly])
                        else:
                            return {"error": "Day for hourly forecast is greater than the number of days"}
                    return {
                        "current": "Failed to get current weather data",
                        "forecast": data
                    }
                elif current_response.status_code == 200 and forecast_response.status_code != 200:
                    data = load_data_current(current_response.json())
                    return {
                        "current": data,
                        "forecast": "Failed to get forecast weather data"
                    }
                else:
                    return {
                        "current": "Failed to get current weather data",
                        "forecast": "Failed to get forecast weather data"
                    }
        else:
            return {"error": "Either current or forecast (or both) must be True"}
    except Exception as e:
        return {"error": str(e)}