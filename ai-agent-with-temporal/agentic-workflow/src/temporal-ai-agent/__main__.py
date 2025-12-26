from pathlib import Path
from temporalio.client import Client
from litellm import uuid
from model.llm_prompt_model import LLMPromptModel
from data.load_weather_data import load_weather_data
from data.weather_record_by_id import weather_record_by_id
from integration.ollama.llm_prompt_handler import llm_call
from weather_management_workflow import WeatherManagementWorkerWorkflow
from weather_management_worker import weather_management_worker
import asyncio

promptQuestion = "Categorize the Season if Weather Description is: "

def prepare_data():
    print("\n" + "=" * 60)
    print("\nFetching weather alerts data...")
    # Store the response in a variable
    weather_alerts_data = load_weather_data()
    
    print(f"Weather alert Fetch Status: {weather_alerts_data['message']}")
    return weather_alerts_data

def get_user_input():
    print("\n" + "=" * 60)
    weather_record_id = input("Enter your Weather Record ID: ").strip()
    print(f"\nProcessing Weather Record ID: {weather_record_id}")

    # convert input to integer ID
    try:
        record_id = int(weather_record_id)
        return record_id
    except ValueError:
        print("Invalid ID provided. Please enter a numeric weather record ID.")
        return None

def fetch_weather_record(weather_alerts_response, record_id):
    # Pass the full loader response and numeric id
    weather_record = weather_record_by_id(weather_alerts_response, record_id)
    print("\n" + "=" * 60)
    
    print("Weather Record: \n\n", weather_record)
    weather_description = weather_record.get("weather_description", "No description available.")

    return weather_description

def prepare_llm_prompt(weather_description):
    llm_prompt = LLMPromptModel(prompt=promptQuestion, data_payload=weather_description)
    return llm_prompt

def process_weather_data(llm_prompt: LLMPromptModel):
    weather_type = llm_call(llm_prompt)
    print("\n" + "=" * 60)
    print("Identified Weather Type from LLM:")
    print(weather_type)
    print("\n" + "=" * 60)
    return weather_type


def get_workflow_type():
    print("\n" + "=" * 60)
    workflow_type = input("Enter your Workflow Type 1: Sync or 2: Temporal").strip()
    print(f"\nProcessing Workflow Type: {workflow_type}")
    return workflow_type

async def process_weather_data_with_temporal(llm_prompt: LLMPromptModel):   
    print("\n" + "=" * 60)
    print("Starting Temporal Workflow Execution...")
    client = await Client.connect("localhost:7233")

    handle = await client.start_workflow(
        WeatherManagementWorkerWorkflow,
        llm_prompt,
        id=f"generate-weather-workflow-{uuid.uuid4()}",
        task_queue="durable",
    )
    result = await handle.result()

    
    print("\n" + "=" * 60)
    print("Workflow Execution Result:")
    print(result)
    
def process_weather_data_synchronously(llm_prompt: LLMPromptModel):   
    print("\n" + "=" * 60)
    print("Starting Synchronous LLM Processing...")
    result = process_weather_data(llm_prompt)
    print("\n" + "=" * 60)
    print("Workflow Execution Result:")
    print(result)    
    
def process(llm_prompt: LLMPromptModel, workflow_type: str):   
    if workflow_type == '1':
        process_weather_data_synchronously(llm_prompt)
    elif workflow_type == '2':
        asyncio.run(process_weather_data_with_temporal(llm_prompt))
    else:
        print("Invalid Workflow Type selected. Please choose 1 or 2.")

if __name__ == "__main__":
    
    print("\n" + "=" * 60)
    print("Welcome to the Weather Management AI Agent!")
    weather_data = prepare_data()
    record_id = get_user_input()
    if record_id is not None:
        weather_description = fetch_weather_record(weather_data, record_id)
        llm_prompt = prepare_llm_prompt(weather_description)
        workflow_type = get_workflow_type()
        process(llm_prompt, workflow_type)
        
        
    print("\n" + "=" * 60)
