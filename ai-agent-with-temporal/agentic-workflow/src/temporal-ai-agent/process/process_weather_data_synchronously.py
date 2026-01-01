##Process Weather Data Synchronously
from integration.llm.manage_llm_prompt import process_weather_data
from model.workflow_request_model import WorkFlowRequestModel
from process.prepare_workflow_request import prepare_llm_prompt_from_workflow_request
from process.prepare_workflow_request import prepare_applicability_check_from_workflow_request
from integration.rest_api.weather_management_api import check_weather_alert_applicability

def process_weather_data_synchronously(workflow_request: WorkFlowRequestModel) -> str:   
    ##Applicability Activity Call
    print("\n" + "=" * 60)
    print("Synchronously - Starting Weather Management Workflow...")
    print("\n" + "=" * 60)
    print("Preparing Applicability Check Request...")
    applicability_check_request = prepare_applicability_check_from_workflow_request(workflow_request)

    print("\n" + "=" * 60)
    print("Executing Applicability Check Activity...")
    applicability_response = check_weather_alert_applicability(applicability_check_request)

    print("Applicability Check Completed.")
    print("\n" + "=" * 60)
    print("Applicability Response:", applicability_response)
    if not applicability_response.applicable:
        print("Applicability Check Failed.")
        return f"Weather alert not applicable. Reason: {applicability_response.error}"
        
    print("\n" + "=" * 60)
    print("Applicability Check Passed. Proceeding to LLM Call...")
    print("\n" + "=" * 60)
    print("Preparing LLM Prompt from Workflow Request...")
    ##LLM Call Activity Call
    prompt = prepare_llm_prompt_from_workflow_request(workflow_request)
    llm_response = process_weather_data(prompt)
    
    
    print("LLM Call Completed.")
    print("\n" + "=" * 60)
    print("LLM Response:", llm_response)




    return llm_response