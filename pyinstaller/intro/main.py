import matplotlib.pyplot as plt
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

latitude = 41.902782
longitude = 12.496366
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": latitude,
    "longitude": longitude,
    "hourly": "temperature_2m"
}

responses = openmeteo.weather_api(url, params=params)
response = responses[0]

hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

hourly_data = {"Data": pd.date_range(
    start=pd.to_datetime(hourly.Time(), unit="s"),
    periods=len(hourly_temperature_2m),
    freq=pd.Timedelta(seconds=hourly.Interval()),
    inclusive="left"
), "Temperatura a 2 metri": hourly_temperature_2m}

hourly_dataframe = pd.DataFrame(data=hourly_data)

plt.figure(figsize=(10, 6))
plt.plot(hourly_dataframe["Data"], hourly_dataframe["Temperatura a 2 metri"], marker='o')
plt.title('Andamento della Temperatura a 2 Metri')
plt.xlabel('Data e Ora')
plt.ylabel('Temperatura (°C)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()
