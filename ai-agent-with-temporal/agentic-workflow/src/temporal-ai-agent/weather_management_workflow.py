import importlib.util
from pathlib import Path
from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from workflow.activities.applicability_activity import applicability_activity
    from workflow.activities.llm_call_activity import llm_call_activity
    from model.llm_prompt_model import LLMPromptModel
    


@workflow.defn
class WeatherManagementWorkerWorkflow:
    @workflow.run
    async def run(self, input: LLMPromptModel) -> str:
        
        """Workflow to manage weather-related tasks using LLM calls."""
        ##Applicability Activity Call

        applicability_response = await workflow.execute_activity(
            applicability_activity,
            input,
            start_to_close_timeout=timedelta(seconds=30),
        )

        if not applicability_response.applicable:
            return f"Weather alert not applicable. Reason: {applicability_response.error}"
        
        ##LLM Call Activity Call

        llm_response = await workflow.execute_activity(
            llm_call_activity,
            input,
            start_to_close_timeout=timedelta(seconds=30),
        )
        return llm_response
          