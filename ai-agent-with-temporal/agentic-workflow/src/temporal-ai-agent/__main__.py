from data.manage_weather_data import prepare_data, fetch_weather_record
from process.process_weather_data import process
from data.user_input import select_weather_record
from data.user_input import select_workflow_type
from process.prepare_workflow_request import prepare_workflow_request
import json
from model.workflow_response_model import WorkFlowResponseModel

if __name__ == "__main__":
    
    print("\n" + "=" * 60)
    print("Welcome to the Weather Management AI Agent!")
    weather_data = prepare_data()
    record_id = select_weather_record()
    if record_id is not None:
        weather_record = fetch_weather_record(weather_data, record_id)
        workflow_request = prepare_workflow_request(weather_record)
        workflow_type = select_workflow_type()
        workflow_response = process(workflow_request, workflow_type)
        print("Weather Management Workflow Completed Successfully. Preparing Response:")
        print("Workflow Response:\n\n", json.dumps(workflow_response, default=vars , indent=4))
    else:
        print("No valid weather record selected.")

    print("\n" + "=" * 60)
    print("Exiting to the Weather Management AI Agent!")
    print("\n" + "=" * 60)
