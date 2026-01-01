from weather_management_workflow import WeatherManagementWorkerWorkflow
from temporalio.client import Client
from litellm import uuid
from model.workflow_request_model import WorkFlowRequestModel
from model.workflow_response_model import WorkFlowResponseModel

async def process_weather_data_with_temporal(workflow_request: WorkFlowRequestModel) -> WorkFlowResponseModel:   
    print("\n" + "=" * 60)
    print("Temporal Workflow Execution - Start")
    client = await Client.connect("localhost:7233")

    handle = await client.start_workflow(
        WeatherManagementWorkerWorkflow,
        workflow_request,
        id=f"generate-weather-workflow-{uuid.uuid4()}",
        task_queue="durable",
    )
    result = await handle.result()
    print("Temporal Workflow Execution - End")
    print("\n" + "=" * 60)
    return result