from model.workflow_request_model import WorkFlowRequestModel
from integration.llm.model.llm_prompt_model import LLMPromptModel
from integration.llm.manage_llm_prompt import prepare_llm_prompt
from model.weather_data_model import WeatherDataModel
from integration.rest_api.model.applicability_check_request_model import ApplicabilityCheckRequestModel
from integration.rest_api.model.weather_reporter_request_model import WeatherReporterRequestModel

promptQuestion_weatherType = "Categorize the Season if Weather Description is: "
promptQuestion_weatherActivities = "Suggest 5 Outdoor Activities suitable for the Season if Weather Description is: "

def prepare_workflow_request(weather_data_model: WeatherDataModel) -> WorkFlowRequestModel:
    workflow_request = WorkFlowRequestModel(
        weather_record=weather_data_model,
    )
    return workflow_request

def prepare_weather_category_llm_prompt(workflow_request: WorkFlowRequestModel) -> LLMPromptModel:
    llm_prompt = prepare_llm_prompt(promptQuestion_weatherType, workflow_request.weather_record.weather_description)
    return llm_prompt
    
def prepare_applicability_check_request(workflow_request: WorkFlowRequestModel) -> ApplicabilityCheckRequestModel:
    applicability_check = ApplicabilityCheckRequestModel(country=workflow_request.weather_record.country)
    return applicability_check

def prepare_weather_reporter_request(workflow_request: WorkFlowRequestModel) -> WeatherReporterRequestModel:
    weather_reporter_request = WeatherReporterRequestModel(country=workflow_request.weather_record.country)
    return weather_reporter_request

def prepare_weather_outdoor_activities_llm_prompt(workflow_request: WorkFlowRequestModel) -> LLMPromptModel:
    llm_prompt = prepare_llm_prompt(promptQuestion_weatherActivities, workflow_request.weather_record.weather_description)
    return llm_prompt