import requests
import os
from typing import Any
from dotenv import load_dotenv
import pandas as pd
import json

load_dotenv()

        

def clean_forecast_data(forecast_data: dict[str, Any]) -> pd.DataFrame:
    """
    Cleans the forecast data from the WeatherAPI.
    """
    # Access the first day's hourly forecast
    data = forecast_data["forecast"]['forecastday']
    daily_data = []
    for day in data:
        day_data = {
            "date": day["date"],
            "max_temp": day["day"]["maxtemp_c"],
            "min_temp": day["day"]["mintemp_c"],
            "max_wind": day["day"]["maxwind_kph"],
        }
        daily_data.append(day_data)
    
    return pd.DataFrame(daily_data)

def air_quality(so2, no2, pm10, pm2_5, o3, co):
    """
    Determines air quality based on pollutant levels.
    Returns 'Good', 'Fair', 'Moderate', 'Poor', or 'Very Poor'.
    """
    # Handle None or negative values
    values = [so2, no2, pm10, pm2_5, o3, co]
    if any(v is None or v < 0 for v in values):
        return "Invalid Data"

    # Define the ranges for each pollutant
    thresholds = {
        "Good": {
            "SO2": (0, 20), "NO2": (0, 40), "PM10": (0, 20), "PM2.5": (0, 10), "O3": (0, 60), "CO": (0, 4400)
        },
        "Fair": {
            "SO2": (20, 80), "NO2": (40, 70), "PM10": (20, 50), "PM2.5": (10, 25), "O3": (60, 100), "CO": (4400, 9400)
        },
        "Moderate": {
            "SO2": (80, 250), "NO2": (70, 150), "PM10": (50, 100), "PM2.5": (25, 50), "O3": (100, 140), "CO": (9400, 12400)
        },
        "Poor": {
            "SO2": (250, 350), "NO2": (150, 200), "PM10": (100, 200), "PM2.5": (50, 75), "O3": (140, 180), "CO": (12400, 15400)
        },
        "Very Poor": {
            "SO2": (350, float('inf')), "NO2": (200, float('inf')), "PM10": (200, float('inf')), "PM2.5": (75, float('inf')), 
            "O3": (180, float('inf')), "CO": (15400, float('inf'))
        }
    }

    # Find the worst quality level that matches all pollutants
    worst_quality = "Good"
    pollutant_values = {"SO2": so2, "NO2": no2, "PM10": pm10, "PM2.5": pm2_5, "O3": o3, "CO": co}
    
    quality_levels = ["Good", "Fair", "Moderate", "Poor", "Very Poor"]
    
    for pollutant, value in pollutant_values.items():
        for quality in quality_levels:
            min_val, max_val = thresholds[quality][pollutant]
            if min_val <= value < max_val:
                # Update to worse quality if found
                current_index = quality_levels.index(quality)
                worst_index = quality_levels.index(worst_quality)
                if current_index > worst_index:
                    worst_quality = quality
                break
        else:
            # If no range matched for any pollutant
            return "Data out of range"
            
    return worst_quality

def get_air_quality(request: dict[str, Any]) -> dict[str, Any]:
    """
    Fetches air quality data from the AirQualityAPI.
    """
    data = request['air_quality']
    so2 = round(data['so2'], 3)
    no2 = round(data['no2'], 3)
    pm10 = round(data['pm10'], 3)
    pm2_5 = round(data['pm2_5'], 3)
    o3 = round(data['o3'], 3)
    co = round(data['co'], 3)
    # print(f"Air Quality Values - SO2: {so2}, NO2: {no2}, PM10: {pm10}, PM2.5: {pm2_5}, O3: {o3}, CO: {co}")
    return air_quality(so2, no2, pm10, pm2_5, o3, co)


def load_daily_data_forecast(data: dict[str, Any]):
    """
    Loads the daily forecast data from the WeatherAPI.
    Returns a string of the daily forecast data.
    The data is in the format of a csv file.
    """
    data = data['forecast']['forecastday']
    daily_data = []
    header = "date, avg_temp_c, max_temp_c, min_temp_c, max_wind_kph, avg_humidity, avg_visibility, daily_chance_of_rain, uv, condition, precipitation_mm, snow_cm, air_quality"
    daily_data.append(header)
    for day in data:
        day_data = day["day"]
        daily_data.append(
            f"{day['date']}, {day_data['avgtemp_c']}, {day_data['maxtemp_c']}, "
            f"{day_data['mintemp_c']}, {day_data['maxwind_kph']}, "
            f"{day_data['avghumidity']}, {day_data['avgvis_km']}, "
            f"{day_data['daily_chance_of_rain']}, {day_data['uv']}, "
            f"{day_data['condition']['text']}, {day_data['totalprecip_mm']}, "
            f"{day_data['totalsnow_cm']}, {get_air_quality(day_data)}"
        )
        # day_data = {
        #     "date": day["date"],
        #     "avg_temp, max_temp, min_temp, max_wind": str(day["day"]["avgtemp_c"]) + str(day["day"]["maxtemp_c"]) + str(day["day"]["mintemp_c"]) + str(day["day"]["maxwind_kph"]),
        #     "avg_humidity": day["day"]["avghumidity"],
        #     "avg_visibility": day["day"]["avgvis_km"],
        #     "daily_chance_of_rain": day["day"]["daily_chance_of_rain"],
        #     "uv": day["day"]["uv"],
        #     "condition": day["day"]["condition"]["text"],
        #     "precipitation": day["day"]["totalprecip_mm"],
        #     "snow": day["day"]["totalsnow_cm"],
        # }
        # daily_data.append(day_data)
    
        # "max_temp": str(day["day"]["maxtemp_c"]),
        # "min_temp": str(day["day"]["mintemp_c"]),
        # "max_wind": str(day["day"]["maxwind_kph"]),
        # "avg_wind": day["day"]["avgwind_kph"],
        
        # "avg_pressure": day["day"]["avgpressure_mb"],
        
        
        # "avg_cloud": day["day"]["avghumidity"],
    return "\n".join(daily_data)

# def load_hourly_data_forecast(data: dict[str, Any]):
#     data = data['hour']
#     hourly_data = []
#     header = "date, hour, temp, wind, humidity, visibility, precipitation, snow, air_quality"
#     hourly_data.append(header)
#     for hour in data:
#         try:
#             air_quality_data = hour.get('air_quality', {})
#             air_quality_result = "N/A"
#             # if air_quality_data:
#             #     so2 = round(air_quality_data.get('so2', 0), 3)
#             #     no2 = round(air_quality_data.get('no2', 0), 3)
#             #     pm10 = round(air_quality_data.get('pm10', 0), 3)
#             #     pm2_5 = round(air_quality_data.get('pm2_5', 0), 3)
#             #     o3 = round(air_quality_data.get('o3', 0), 3)
#             #     co = round(air_quality_data.get('co', 0), 3)
#             #     air_quality_result = air_quality(so2, no2, pm10, pm2_5, o3, co)
            
#             hourly_data.append(
#                 f"{hour['time'].split()[0]}, {hour['time'].split()[1]}, "
#                 f"{hour['temp_c']}, {hour['wind_kph']}, {hour['humidity']}, "
#                 f"{hour['vis_km']}, {hour['precip_mm']}, {hour['snow_cm']}, "
#                 f"{get_air_quality(hour)}"
#             )
#         except KeyError as e:
#             print(f"Warning: Missing data for hour {hour.get('time', 'unknown')}: {str(e)}")
#             continue
#     return "\n".join(hourly_data)


def load_hourly_data_forecast(data: dict[str, Any]):
    data = data['hour']
    hourly_data = []
    header = "date, hour, temp_c, wind_kph, humidity, visibility_km, precipitation_mm, uv, condition, will_it_rain, will_it_snow, snow_cm, air_quality"
    hourly_data.append(header)
    for hour in data:
        hourly_data.append(
            f"{hour['time'].split(' ')[0]}, {hour['time'].split(' ')[1]}, "
            f"{hour['temp_c']}, {hour['wind_kph']}, {hour['humidity']}, {hour['vis_km']}, "
            f"{hour['precip_mm']}, {hour['uv']}, {hour['condition']['text']}, {hour['will_it_rain']}, {hour['will_it_snow']}, "
            # f"{hour['precip_mm']}, {hour['condition']['text']}, {hour['snow_cm']}, "
            f"{hour['snow_cm']}, {get_air_quality(hour)}"
        )
    return "\n".join(hourly_data)

def load_data_current(data: dict[str, Any]):
    data = data['current']
    header = "last_updated, temp_c, wind_kph, pressure_in, humidity, visibility_km, precipitation_mm, uv, condition, air_quality"
    current_data = []
    current_data.append(header)
    current_data.append(
        f"{data['last_updated'].split(' ')[1]}, {data['temp_c']}, {data['wind_kph']}, {data['pressure_in']}, {data['humidity']}, {data['vis_km']}, {data['precip_mm']}, {data['uv']}, {data['condition']['text']}, {get_air_quality(data)}"
    )
    return "\n".join(current_data)
    

def get_weather(city: str, current: bool = True, forecast:bool = False, days: int = 1) -> dict[str, Any]:
    """
    Fetches weather data from WeatherAPI.

    Args:
        city (str): City name.
        current (bool): Get current weather. Default is True.
        forecast (bool): Get forecast. Default is False.
        days (int): Forecast days (if forecast=True).

    Returns:
        dict: Weather data or error.
    """
    try:
        current_response = None
        forecast_response = None
        if current and not forecast:
            current_response = requests.post(f"https://api.weatherapi.com/v1/current.json",
                             params={"key": os.getenv("WEATHER_API_KEY"),
                                     "q": city,
                                     "aqi": "yes",
                                     "tides": "yes",
                                     "alerts": "yes",
                                     })
            if current_response.status_code != 200:
                return {"error": "Failed to get current weather data"}
            else:
                return {
                    "current": current_response.json()
                }
            
        elif forecast and not current:
            print("Fetching forecast data...")
            forecast_response = requests.post(f"https://api.weatherapi.com/v1/forecast.json",
                             params={"key": os.getenv("WEATHER_API_KEY"),
                                     "q": city,
                                     "aqi": "yes",
                                     "tides": "yes",
                                     "alerts": "yes",
                                     "days": days
                                     })
            if forecast_response.status_code != 200:
                return {"error": "Failed to get forecast weather data"}
            else:
                print("Forecast data fetched successfully")
                print(load_daily_data_forecast(forecast_response.json()))
                print("--------------------------------")
                print(load_hourly_data_forecast(forecast_response.json()['forecast']['forecastday'][1]))
                print("--------------------------------")
                print(load_hourly_data_forecast(forecast_response.json()['forecast']['forecastday'][2]))
                print("--------------------------------")
                print(load_data_current(forecast_response.json()))
                print("--------------------------------")
                air_quality = get_air_quality(forecast_response.json()['current'])
                print(f"Air quality is: {air_quality}")
                df = clean_forecast_data(forecast_response.json())
                df.to_csv("forecast.csv", index=False)
                return {
                    "forecast": forecast_response.json(),
                    "forecast_df": df.to_dict('records')
                }
        
        elif current and forecast:
            current_response = requests.post(f"https://api.weatherapi.com/v1/current.json",
                             params={"key": os.getenv("WEATHER_API_KEY"),
                                     "q": city,
                                     "aqi": "yes",
                                     "tides": "yes",
                                     "alerts": "yes",
                                     })
            
            forecast_response = requests.post(f"https://api.weatherapi.com/v1/forecast.json",
                             params={"key": os.getenv("WEATHER_API_KEY"),
                                     "q": city,
                                     "aqi": "yes",
                                     "tides": "yes",
                                     "alerts": "yes",
                                     "days": days
                                     })
            
            result = {}
            
            if current_response.status_code == 200:
                result["current"] = current_response.json()
            else:
                result["current"] = "Failed to get current weather data"
                
            if forecast_response.status_code == 200:
                result["forecast"] = forecast_response.json()
                df = clean_forecast_data(forecast_response.json())
                result["forecast_df"] = df.to_dict('records')
            else:
                result["forecast"] = "Failed to get forecast weather data"
                
            return result
            
    except Exception as e:
        return {"error": str(e)}
    


if __name__ == "__main__":
    g = get_weather("Pune", current=False, forecast=True, days=4)
    print(g)