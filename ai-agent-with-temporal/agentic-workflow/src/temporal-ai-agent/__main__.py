from data.manage_weather_data import prepare_data, fetch_weather_record
from process.process_weather_data import process
from data.user_input import select_weather_record
from data.user_input import select_workflow_type
from integration.llm.manage_llm_prompt import prepare_llm_prompt


if __name__ == "__main__":
    
    print("\n" + "=" * 60)
    print("Welcome to the Weather Management AI Agent!")
    weather_data = prepare_data()
    record_id = select_weather_record()
    if record_id is not None:
        weather_description = fetch_weather_record(weather_data, record_id)
        llm_prompt = prepare_llm_prompt(weather_description)
        workflow_type = select_workflow_type()
        process(llm_prompt, workflow_type)
        
        
    print("\n" + "=" * 60)
