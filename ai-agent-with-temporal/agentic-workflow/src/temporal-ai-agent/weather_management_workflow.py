from datetime import timedelta
from temporalio import workflow


with workflow.unsafe.imports_passed_through():
    ##Activities Imports
    from workflow.activities.applicability_check_activity import applicability_check_activity
    from workflow.activities.llm_call_activity import llm_call_activity
    from workflow.activities.fetch_weather_reporter_activity import fetch_weather_reporter_activity
    ##Model Imports
    from model.workflow_request_model import WorkFlowRequestModel
    ##Response Model Imports
    from model.workflow_response_model import WorkFlowResponseModel
    ##Prepare Request Imports  
    from process.prepare_workflow_request import prepare_weather_category_llm_prompt
    from process.prepare_workflow_request import prepare_applicability_check_request
    from process.prepare_workflow_request import prepare_weather_reporter_request
    ##Prepare Response Imports  
    from process.prepare_workflow_response import prepare_workflow_response
    
    
@workflow.defn
class WeatherManagementWorkerWorkflow:
    
    
    @workflow.run
    async def run(self, workflow_request: WorkFlowRequestModel) -> WorkFlowResponseModel:
        
        """Workflow to manage weather-related tasks using LLM calls."""
        
        
        print("\n" + "=" * 60)
        print("Starting Weather Management Workflow...")
        
        ##Applicability Activity Call - Start
        print("\n" + "=" * 60)
        print("Preparing Applicability Check Request...")
        applicability_check_request = prepare_applicability_check_request(workflow_request)
        print("Executing Applicability Check Activity...")
        applicability_response = await workflow.execute_activity(
            applicability_check_activity,
            applicability_check_request,
            start_to_close_timeout=timedelta(seconds=30),
        )
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
        weather_category = await workflow.execute_activity(
            llm_call_activity,
            weather_category_llm_prompt,
            start_to_close_timeout=timedelta(seconds=30),
        )
        print("LLM Call Completed to identify Weather Category.")
        print("LLM Response for Weather Category:", weather_category)
        print("LLM call passed. Proceeding to fetch Weather Reporter based on Country...")
        ##LLM Call Activity Call to check Weather Category - End


        ##Fetch Weather Reporter Activity Call - Start
        print("\n" + "=" * 60)
        print("Preparing Weather-Reporter-Request to fetch Weather Reporter based on Country...")
        weather_reporter_request = prepare_weather_reporter_request(workflow_request)
        print("Executing Fetch Weather Reporter Activity to fetch Weather Reporter...")
        weather_reporter_response = await workflow.execute_activity(
            fetch_weather_reporter_activity,
            weather_reporter_request,
            start_to_close_timeout=timedelta(seconds=30),
        )
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
        ##Prepare Final Workflow Response - End
        
        print("\n" + "=" * 60)
        print("Workflow Execution Completed.")

        return workflow_response
          