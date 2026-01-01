from dataclasses import dataclass
from model.weather_data_model import WeatherDataModel
from model.weather_reporter_model import WeatherReporterModel

@dataclass
class WorkFlowResponseModel:
    weather_data: WeatherDataModel
    weather_category: str
    weather_reporter: WeatherReporterModel