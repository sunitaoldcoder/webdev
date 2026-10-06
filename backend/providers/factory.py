"""Composition root: swap implementations without changing endpoint contracts."""
import os
from .interfaces import WeatherProvider, MarketPriceProvider, LLMProvider, VisionProvider
from .demo import SampleWeather, SampleMarket, DemoLLM, DemoVision
from .weather import OpenMeteoWeather

def weather_provider() -> WeatherProvider:
    return OpenMeteoWeather() if os.environ.get('WEATHER_PROVIDER')=='open_meteo' else SampleWeather()
def market_provider() -> MarketPriceProvider:
    return SampleMarket()
def llm_provider() -> LLMProvider:
    return DemoLLM()
def vision_provider() -> VisionProvider:
    return DemoVision()
