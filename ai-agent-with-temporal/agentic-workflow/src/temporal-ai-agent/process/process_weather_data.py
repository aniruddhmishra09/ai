from weather_management_workflow import WeatherManagementWorkerWorkflow
import asyncio
from temporalio.client import Client
from litellm import uuid
from integration.llm.manage_llm_prompt import process_weather_data
from model.workflow_request_model import WorkFlowRequestModel
from process.prepare_workflow_request import prepare_llm_prompt_from_workflow_request

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
    print("\n" + "=" * 60)
    print("Starting Synchronous LLM Processing...")
    prompt = prepare_llm_prompt_from_workflow_request(workflow_request)
    result = process_weather_data(prompt)
    print("\n" + "=" * 60)
    print("Workflow Execution Result:")
    print(result)    
    
def process(workflow_request: WorkFlowRequestModel, workflow_type: str):   
    if workflow_type == '1':
        process_weather_data_synchronously(workflow_request)
    elif workflow_type == '2':
        asyncio.run(process_weather_data_with_temporal(workflow_request))
    else:
        print("Invalid Workflow Type selected. Please choose 1 or 2.")


