
from model.workflow_request_model import WorkFlowRequestModel
from model.llm_prompt_model import LLMPromptModel
from integration.llm.manage_llm_prompt import prepare_llm_prompt
from model.weather_data_model import WeatherDataModel
from model.applicability_check_request_model import ApplicabilityCheckRequestModel

def prepare_workflow_request(weather_data_model: WeatherDataModel) -> WorkFlowRequestModel:
    workflow_request = WorkFlowRequestModel(
        weather_record=weather_data_model,
        
    )
    
    return workflow_request

def prepare_llm_prompt_from_workflow_request(workflow_request: WorkFlowRequestModel) -> LLMPromptModel:
    llm_prompt = prepare_llm_prompt(workflow_request.weather_record.weather_description)
    return llm_prompt
    
def prepare_applicability_check_from_workflow_request(workflow_request: WorkFlowRequestModel) -> ApplicabilityCheckRequestModel:
    applicability_check = ApplicabilityCheckRequestModel(country=workflow_request.weather_record.country)
    return applicability_check
