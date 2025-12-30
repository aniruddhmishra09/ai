from weather_management_workflow import WeatherManagementWorkerWorkflow
import asyncio
from temporalio.client import Client
from litellm import uuid
from integration.llm.manage_llm_prompt import process_weather_data
from model.workflow_request_model import WorkFlowRequestModel
from process.prepare_workflow_request import prepare_llm_prompt_from_workflow_request
from process.prepare_workflow_request import prepare_applicability_check_from_workflow_request
from integration.applicability.check_weather_alert_applicability import check_weather_alert_applicability
from model.applicability_check_response_model import ApplicabilityCheckResponseModel

async def process_weather_data_with_temporal(workflow_request: WorkFlowRequestModel):   
    print("\n" + "=" * 60)
    print("Starting Temporal Workflow Execution...")
    client = await Client.connect("localhost:7233")

    handle = await client.start_workflow(
        WeatherManagementWorkerWorkflow,
        workflow_request,
        id=f"generate-weather-workflow-{uuid.uuid4()}",
        task_queue="durable",
    )
    result = await handle.result()

    
    print("\n" + "=" * 60)
    print("Workflow Execution Result:")
    print(result)
    
def process_weather_data_synchronously(workflow_request: WorkFlowRequestModel):   
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

    
def process(workflow_request: WorkFlowRequestModel, workflow_type: str):   
    if workflow_type == '1':
        process_weather_data_synchronously(workflow_request)
    elif workflow_type == '2':
        asyncio.run(process_weather_data_with_temporal(workflow_request))
    else:
        print("Invalid Workflow Type selected. Please choose 1 or 2.")


