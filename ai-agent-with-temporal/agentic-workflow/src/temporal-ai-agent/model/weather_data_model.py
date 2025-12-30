from dataclasses import dataclass


@dataclass
class WeatherDataModel:
    id: str
    country: str
    country: str
    city: str
    weather_description: str
    wikipedia_url: str