##Applicability Check Activity
from integration.rest_api.model.weather_reporter_request_model import WeatherReporterRequestModel
from integration.rest_api.model.weather_reporter_response_model import WeatherReporterResponseModel
from integration.rest_api.weather_management_api import fetch_weather_reporter_by_country
from temporalio import activity

@activity.defn
def fetch_weather_reporter_activity(input: WeatherReporterRequestModel) -> WeatherReporterResponseModel:
    weather_reporter_response = fetch_weather_reporter_by_country(input)
    return weather_reporter_response