from data.manage_weather_data import prepare_data, fetch_weather_record
from process.process_weather_data import process
from data.user_input import select_weather_record
from data.user_input import select_workflow_type
from process.prepare_workflow_request import prepare_workflow_request

if __name__ == "__main__":
    
    print("\n" + "=" * 60)
    print("Welcome to the Weather Management AI Agent!")
    weather_data = prepare_data()
    record_id = select_weather_record()
    if record_id is not None:
        weather_record = fetch_weather_record(weather_data, record_id)
        workflow_request = prepare_workflow_request(weather_record)
        workflow_type = select_workflow_type()
        process(workflow_request, workflow_type)
        
        
    print("\n" + "=" * 60)
