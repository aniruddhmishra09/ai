from dataclasses import dataclass

@dataclass
class WeatherDataModel:
    id: int
    country: str
    city: str
    weather_description: str
    wikipedia_url: str
