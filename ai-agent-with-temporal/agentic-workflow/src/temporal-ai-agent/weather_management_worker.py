import asyncio
import concurrent.futures
import logging
import warnings
#from workflow.activities import llm_call_activity
from temporalio.client import Client
from temporalio.worker import Worker
from weather_management_workflow import WeatherManagementWorkerWorkflow

from temporalio import activity

##LLM Call Activity
from integration.llm.ollama.llm_prompt_handler import llm_call
from integration.llm.model.llm_prompt_model import LLMPromptModel
@activity.defn
def llm_call_activity(input: LLMPromptModel) -> str:
    weather_type = llm_call(input)
    return weather_type


##Applicability Check Activity
from integration.rest_api.model.applicability_check_request_model import ApplicabilityCheckRequestModel
from integration.rest_api.model.applicability_check_response_model import ApplicabilityCheckResponseModel
from integration.rest_api.weather_management_api import check_weather_alert_applicability

@activity.defn
def applicability_check_activity(input: ApplicabilityCheckRequestModel) -> ApplicabilityCheckResponseModel:
    applicability_check = check_weather_alert_applicability(input)
    return applicability_check

##Weather Reporter Activity
from integration.rest_api.model.weather_reporter_request_model import WeatherReporterRequestModel
from integration.rest_api.model.weather_reporter_response_model import WeatherReporterResponseModel
from integration.rest_api.weather_management_api import fetch_weather_reporter_by_country
from temporalio import activity

@activity.defn
def fetch_weather_reporter_activity(input: WeatherReporterRequestModel) -> WeatherReporterResponseModel:
    weather_reporter = fetch_weather_reporter_by_country(input)
    return weather_reporter

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
            activities=[llm_call_activity, applicability_check_activity,fetch_weather_reporter_activity],
            activity_executor=activity_executor,
        )
        logging.info("Starting the worker....")
        await worker.run()

if __name__ == "__main__":
    asyncio.run(weather_management_worker())
