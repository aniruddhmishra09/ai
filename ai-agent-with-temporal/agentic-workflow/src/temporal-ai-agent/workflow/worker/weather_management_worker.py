import asyncio
import concurrent.futures
import logging
import warnings

from activities import llm_activity
from temporalio.client import Client
from temporalio.worker import Worker
from workflow.weather_management_workflow import WeatherManagementWorkerWorkflow

async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    # Reduce noise from various libraries
    logging.getLogger("LiteLLM").setLevel(logging.WARNING)
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
            activities=[llm_activity],
            activity_executor=activity_executor,
        )
        logging.info("Starting the worker....")
        await worker.run()


if __name__ == "__main__":
    asyncio.run(main())