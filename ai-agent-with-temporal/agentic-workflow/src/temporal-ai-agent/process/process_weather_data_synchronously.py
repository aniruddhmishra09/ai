##Process Weather Data Synchronously
from model.workflow_request_model import WorkFlowRequestModel
from integration.rest_api.weather_management_api import check_weather_alert_applicability
from process.prepare_workflow_request import prepare_weather_category_llm_prompt
from process.prepare_workflow_request import prepare_applicability_check_request
from process.prepare_workflow_request import prepare_weather_reporter_request
from integration.llm.manage_llm_prompt import process_llm_prompt
from integration.rest_api.weather_management_api import fetch_weather_reporter_by_country
from model.workflow_response_model import WorkFlowResponseModel

##Prepare Response Imports  
from process.prepare_workflow_response import prepare_workflow_response

def process_weather_data_synchronously(workflow_request: WorkFlowRequestModel) -> WorkFlowResponseModel:   
    
    print("\n" + "=" * 60)
    print("Synchronously - Starting Weather Management Workflow...")
   
     ##Applicability Activity Call - Start
    print("\n" + "=" * 60)
    print("Preparing Applicability Check Request...")
    applicability_check_request = prepare_applicability_check_request(workflow_request)
    print("Executing Applicability Check Activity...")
    applicability_response = check_weather_alert_applicability(applicability_check_request)

    print("Applicability Check Completed.")
    print("Applicability Response:", applicability_response)
    if not applicability_response.applicable:
        print("Applicability Check Failed.")
        return f"Weather alert not applicable. Reason: {applicability_response.error}"
        
    
    print("Applicability Check Passed. Proceeding to LLM Call to identify Weather Category...")
    print("\n" + "=" * 60)
    ##Applicability Activity Call - End


    ##LLM Call Activity Call to check Weather Category - Start
    print("\n" + "=" * 60)
    print("Preparing LLM Prompt from Workflow Request...")
    weather_category_llm_prompt = prepare_weather_category_llm_prompt(workflow_request)
    print("Executing LLM Call Activity to identify Weather Category...")
    weather_category = process_llm_prompt(weather_category_llm_prompt)
    print("LLM Call Completed to identify Weather Category.")
    print("LLM Response for Weather Category:", weather_category)
    print("LLM call passed. Proceeding to fetch Weather Reporter based on Country...")
    ##LLM Call Activity Call to check Weather Category - End


    ##Fetch Weather Reporter Activity Call - Start
    print("\n" + "=" * 60)
    print("Preparing Weather-Reporter-Request to fetch Weather Reporter based on Country...")
    weather_reporter_request = prepare_weather_reporter_request(workflow_request)
    print("Executing Fetch Weather Reporter Activity to fetch Weather Reporter...")
    weather_reporter_response = fetch_weather_reporter_by_country(weather_reporter_request)
    print("Fetch Weather Reporter Activity Completed.")
    print("Weather Reporter Response:", weather_reporter_response)
    ###Fetch Weather Reporter Activity Call - End

    ##Prepare Final Workflow Response - Start
    print("\n" + "=" * 60)
    print("Preparing Final Workflow Response..." )
    workflow_response = prepare_workflow_response(
        weather_category=weather_category,
        workflow_request=workflow_request,
        weather_reporter=weather_reporter_response,
        )
      
    print("Final Workflow Response Prepared Successfully." )
    ##print("Workflow Response:", workflow_response)
    ##Prepare Final Workflow Response - End


    print("\n" + "=" * 60)
    print("Workflow Execution Completed.")

    return workflow_response