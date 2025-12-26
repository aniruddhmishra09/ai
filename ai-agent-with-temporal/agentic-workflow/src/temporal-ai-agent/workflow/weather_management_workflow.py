import sys
import json
import importlib.util
from pathlib import Path

from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy


# Load load-weather-data.py dynamically because of the hyphenated filename
llm_activity_path = Path(__file__).parent / "activities" / "llm_activity.py"
spec = importlib.util.spec_from_file_location("llm_activity", llm_activity_path)
llm_activity_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(llm_activity_module)
llm_call_activity = llm_activity_module.llm_call_activity

applicability_activity_path = Path(__file__).parent / "activities" / "applicability_activity.py"
spec = importlib.util.spec_from_file_location("applicability_activity", applicability_activity_path)
applicability_activity_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(applicability_activity_module)
applicability_activity = applicability_activity_module.applicability_activity

llm_prompt_model_path = Path(__file__).parent.parent / "model" / "llm_prompt_model.py"
spec = importlib.util.spec_from_file_location("llm_prompt_model", llm_prompt_model_path)
llm_prompt_model_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(llm_prompt_model_module)
LLMPromptModel = llm_prompt_model_module.LLMPromptModel

applicability_check_request_model_path = Path(__file__).parent.parent / "model" / "applicability_check_request_model.py"
spec = importlib.util.spec_from_file_location("applicability_check_request_model", applicability_check_request_model_path)
applicability_check_request_model_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(applicability_check_request_model_module)
ApplicabilityCheckRequestModel = applicability_check_request_model_module.ApplicabilityCheckRequestModel

#with workflow.unsafe.imports_passed_through():
    #from activities.applicability_activity import applicabiilty_check
    #from activities.llm_activity import llm_call_activity
    #from models.llm_prompt_model import LLMPromptModel
    #from models.applicability_check_request_model import ApplicabilityCheckRequestModel
    #from models.applicability_check_response_model import ApplicabilityCheckResponseModel

@workflow.defn
class WeatherManagementWorkerWorkflow:
    @workflow.run
    async def run(self, input: LLMPromptModel) -> str:
        llm_call_input = LLMPromptModel(
            prompt=input.prompt,
            data_payload=input.data_payload
        )
        llm_response = await workflow.execute_activity(
            llm_call_activity,
            llm_call_input,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=2),
                maximum_attempts=3
            )
        )
        return llm_response
          