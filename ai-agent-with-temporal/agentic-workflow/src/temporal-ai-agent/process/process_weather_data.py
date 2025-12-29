from model.llm_prompt_model import LLMPromptModel
from weather_management_workflow import WeatherManagementWorkerWorkflow
import asyncio
from temporalio.client import Client
from litellm import uuid
from integration.llm.manage_llm_prompt import process_weather_data

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