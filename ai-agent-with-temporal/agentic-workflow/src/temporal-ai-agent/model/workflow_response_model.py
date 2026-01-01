from dataclasses import dataclass
from model.weather_data_model import WeatherDataModel

@dataclass
class WorkFlowRequestModel:
    weather_data_model: WeatherDataModel