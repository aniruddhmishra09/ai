from weather_management_workflow import WeatherManagementWorkerWorkflow
from temporalio.client import Client
from litellm import uuid
from workflow_response_model import WorkFlowRequestModel

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