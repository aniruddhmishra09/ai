def select_weather_record():
    weather_record_id = input("Enter your Weather Record ID: ").strip()
    print(f"\nProcessing Weather Record ID: {weather_record_id}")

    # convert input to integer ID
    try:
        record_id = int(weather_record_id)
        return record_id
    except ValueError:
        print("Invalid ID provided. Please enter a numeric weather record ID.")
        return None
    
def select_workflow_type():
    workflow_type = input("Enter your Workflow Type 1: Sync or 2: Temporal. Please enter 1 or 2: ").strip()
    print(f"\nProcessing Workflow Type: {workflow_type}")
    return workflow_type