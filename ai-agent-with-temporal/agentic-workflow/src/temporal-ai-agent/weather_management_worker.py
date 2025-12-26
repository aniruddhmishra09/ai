import asyncio
import concurrent.futures
import logging
import warnings
#from workflow.activities import llm_call_activity
from temporalio.client import Client
from temporalio.worker import Worker
from weather_management_workflow import WeatherManagementWorkerWorkflow

from temporalio import activity
from integration.ollama.llm_prompt_handler import llm_call
from model.llm_prompt_model import LLMPromptModel

@activity.defn
def llm_call_activity(input: LLMPromptModel) -> str:
    weather_type = llm_call(input)
    return weather_type

async def weather_management_worker() -> None:
    logging.basicConfig(level=logging.INFO)

    # Reduce noise from various libraries
    #logging.getLogger("LiteLLM").setLevel(logging.WARNING)
    logging.getLogger("temporalio").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    # Suppress Pydantic converter warning
    warnings.filterwarnings("ignore", category=UserWarning, module="temporalio.converter")

    client = await Client.connect("localhost:7233", namespace="default")

    # Run the Worker
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as activity_executor:
        worker: Worker = Worker(
            client,
            task_queue="durable",
            workflows=[WeatherManagementWorkerWorkflow],
            activities=[llm_call_activity],
            activity_executor=activity_executor,
        )
        logging.info("Starting the worker....")
        await worker.run()

if __name__ == "__main__":
    asyncio.run(weather_management_worker())
