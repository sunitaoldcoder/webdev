import json
from unittest.mock import patch, MagicMock
from urllib.error import URLError
from django.test import SimpleTestCase
from .weather import OpenMeteoWeather, WeatherUnavailable
from .demo import DemoLLM, DemoVision, SampleMarket
from .factory import weather_provider
class ProviderTests(SimpleTestCase):
    def test_live_weather_adapter_uses_external_fields(self):
        payload={'current':{'temperature_2m':31,'relative_humidity_2m':76,'wind_speed_10m':12,'time':'2026-10-06T12:00'},'daily':{'time':['2026-10-06','2026-10-07','2026-10-08','2026-10-09','2026-10-10'],'temperature_2m_max':[32,33,32,31,30],'precipitation_probability_max':[30,85,40,10,20]}}
        mock=MagicMock();mock.__enter__.return_value.read.return_value=json.dumps(payload).encode()
        with patch('providers.weather.urlopen',return_value=mock) as request:
            result=OpenMeteoWeather().get('Lucknow')
        self.assertFalse(result['is_sample']);self.assertEqual(result['temperature'],31)
        self.assertEqual(result['forecast'][1]['rain_probability'],85)
        self.assertIn('सिंचाई टालने',result['advisory'])
        self.assertTrue(request.call_args.args[0].startswith('https://api.open-meteo.com/'))
    def test_weather_failure_never_substitutes_sample(self):
        with patch('providers.weather.urlopen',side_effect=URLError('offline')):
            with self.assertRaises(WeatherUnavailable):OpenMeteoWeather().get('Varanasi')
    def test_replaceable_weather_selection(self):
        with patch.dict('os.environ',{'WEATHER_PROVIDER':'open_meteo'}):
            self.assertIsInstance(weather_provider(),OpenMeteoWeather)
    def test_demo_never_invents_confirmed_diagnosis_or_live_price(self):
        result=DemoVision().analyze(b'valid-image-bytes','Wheat','yellow')
        self.assertTrue(result['is_demo']);self.assertEqual(result['confidence'],'low')
        self.assertTrue(result['expert_required'])
        answer=DemoLLM().answer('What is the mandi price?',{'language':'hi'})
        self.assertIn('Current market price data is unavailable.',answer['answer'])
        self.assertEqual(answer['sources'],[])
