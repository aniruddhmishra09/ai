from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities.applicability_activity import applicabiilty_check
    from activities.llm_activity import llm_call_activity
    from models.llm_prompt_model import LLMPromptModel
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
          