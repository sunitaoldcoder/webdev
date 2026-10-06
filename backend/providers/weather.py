"""Credential-free weather API adapter. Never substitutes samples for failed live data."""
import json
from urllib.request import urlopen
from urllib.parse import urlencode
from django.utils.timezone import now
LOCATIONS = {'Lucknow':(26.85,80.95),'Rae Bareli':(26.23,81.23),'Gorakhpur':(26.76,83.37),'Varanasi':(25.32,82.97)}
class WeatherUnavailable(Exception):
    pass
class OpenMeteoWeather:
    def get(self, district: str) -> dict:
        lat,lon=LOCATIONS[district]
        query=urlencode({'latitude':lat,'longitude':lon,'current':'temperature_2m,relative_humidity_2m,wind_speed_10m','daily':'temperature_2m_max,precipitation_probability_max','forecast_days':5,'timezone':'Asia/Kolkata'})
        try:
            with urlopen('https://api.open-meteo.com/v1/forecast?'+query,timeout=12) as response:
                raw=json.load(response)
            current=raw['current'];daily=raw['daily'];rain=daily['precipitation_probability_max']
            forecast=[{'date':d,'temperature':daily['temperature_2m_max'][i],'rain_probability':rain[i]} for i,d in enumerate(daily['time'])]
            advice='कल बारिश की संभावना अधिक है। सिंचाई टालने पर विचार करें और स्थानीय पूर्वानुमान जाँचें।' if rain[1] is not None and rain[1]>=60 else 'सिंचाई का निर्णय मिट्टी की नमी, फसल और स्थानीय पूर्वानुमान देखकर लें।'
            return {'district':district,'temperature':current['temperature_2m'],'humidity':current['relative_humidity_2m'],'wind_kmh':current['wind_speed_10m'],'rain_probability':rain[0],'forecast':forecast,'source':'Open-Meteo API','is_sample':False,'updated_at':now().isoformat(),'observed_at':current['time'],'advisory':advice,'advisory_category':'rule_based_suggestion'}
        except (OSError,ValueError,KeyError,IndexError,TypeError) as exc:
            raise WeatherUnavailable('Live weather unavailable. Try again later.') from exc
