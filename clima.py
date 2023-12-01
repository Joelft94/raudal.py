import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": -25.30317112685815,
	"longitude": -57.587873470793625,
	"current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation", "rain", "showers", "weather_code", "wind_speed_10m"],
	"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "precipitation_probability_max"],
	"timezone": "auto"
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
""" print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s") """

# Current values. The order of variables needs to be the same as requested.
current = response.Current()
current_temperature_2m = current.Variables(0).Value()
current_relative_humidity_2m = current.Variables(1).Value()
current_apparent_temperature = current.Variables(2).Value()
current_is_day = current.Variables(3).Value()
current_precipitation = current.Variables(4).Value()
current_rain = current.Variables(5).Value()
current_showers = current.Variables(6).Value()
current_weather_code = current.Variables(7).Value()
current_wind_speed_10m = current.Variables(8).Value()

# print(f"Current time {current.Time()}")
# print(f"Current temperature_2m {current_temperature_2m}")
# print(f"Current relative_humidity_2m {current_relative_humidity_2m}")
# print(f"Current apparent_temperature {current_apparent_temperature}")
# print(f"Current is_day {current_is_day}")
# print(f"Current precipitation {current_precipitation}")
# print(f"Current rain {current_rain}")
# print(f"Current showers {current_showers}")
# print(f"Current weather_code {current_weather_code}")
# print(f"Current wind_speed_10m {current_wind_speed_10m}")

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_weather_code = daily.Variables(0).ValuesAsNumpy()
daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
daily_precipitation_probability_max = daily.Variables(3).ValuesAsNumpy()

daily_data = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s"),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s"),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}



daily_data["weather_code"] = daily_weather_code
daily_data["temperature_2m_max"] = daily_temperature_2m_max
daily_data["temperature_2m_min"] = daily_temperature_2m_min
daily_data["precipitation_probability_max"] = daily_precipitation_probability_max

daily_dataframe = pd.DataFrame(data = daily_data)
print(daily_dataframe)


# daily_temperature_2m_max[1] tira en forma de lista los valores de dataframe de arriba para abajo empezando por 0
# daily_temperature_2m_max promediamos con daily_temperature_2m_min y mandamos al html
