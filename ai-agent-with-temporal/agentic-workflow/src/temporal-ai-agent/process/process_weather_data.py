import asyncio
from model.workflow_request_model import WorkFlowRequestModel
from model.workflow_response_model import WorkFlowResponseModel
from process.process_weather_data_synchronously import process_weather_data_synchronously
from process.process_weather_data_with_temporal import process_weather_data_with_temporal

def process(workflow_request: WorkFlowRequestModel, workflow_type: str) -> WorkFlowResponseModel:
    if workflow_type == '1':
        return process_weather_data_synchronously(workflow_request)
    elif workflow_type == '2':
        return asyncio.run(process_weather_data_with_temporal(workflow_request))
    else:
        print("Invalid Workflow Type selected. Please choose 1 or 2.")


