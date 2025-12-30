from datetime import timedelta
from temporalio import workflow


with workflow.unsafe.imports_passed_through():
    from workflow.activities.applicability_check_activity import applicability_check_activity
    from workflow.activities.llm_call_activity import llm_call_activity
    from model.workflow_request_model import WorkFlowRequestModel   
    from process.prepare_workflow_request import prepare_llm_prompt_from_workflow_request
    from process.prepare_workflow_request import prepare_applicability_check_from_workflow_request
    


@workflow.defn
class WeatherManagementWorkerWorkflow:
    @workflow.run
    async def run(self, input: WorkFlowRequestModel) -> str:
        
        """Workflow to manage weather-related tasks using LLM calls."""
        
        ##Applicability Activity Call

        applicability_check_request = prepare_applicability_check_from_workflow_request(input)

        applicability_response = await workflow.execute_activity(
            applicability_check_activity,
            applicability_check_request,
            start_to_close_timeout=timedelta(seconds=30),
        )
        
        if not applicability_response.applicable:
            return f"Weather alert not applicable. Reason: {applicability_response.error}"
        
        ##LLM Call Activity Call
        prompt = prepare_llm_prompt_from_workflow_request(input)

        llm_response = await workflow.execute_activity(
            llm_call_activity,
            prompt,
            start_to_close_timeout=timedelta(seconds=30),
        )
        return llm_response
          