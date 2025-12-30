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
    async def run(self, workflow_request: WorkFlowRequestModel) -> str:
        
        """Workflow to manage weather-related tasks using LLM calls."""
        
        ##Applicability Activity Call
        print("\n" + "=" * 60)
        print("Starting Weather Management Workflow...")
        print("\n" + "=" * 60)
        print("Preparing Applicability Check Request...")
        applicability_check_request = prepare_applicability_check_from_workflow_request(workflow_request)

        print("\n" + "=" * 60)
        print("Executing Applicability Check Activity...")
        applicability_response = await workflow.execute_activity(
            applicability_check_activity,
            applicability_check_request,
            start_to_close_timeout=timedelta(seconds=30),
        )
        print("Applicability Check Completed.")
        print("\n" + "=" * 60)
        print("Applicability Response:", applicability_response)
        if not applicability_response.applicable:
            print("Applicability Check Failed.")
            return f"Weather alert not applicable. Reason: {applicability_response.error}"
        
        print("\n" + "=" * 60)
        print("Applicability Check Passed. Proceeding to LLM Call...")
        print("\n" + "=" * 60)
        print("Preparing LLM Prompt from Workflow Request...")
        ##LLM Call Activity Call
        prompt = prepare_llm_prompt_from_workflow_request(workflow_request)

        print("\n" + "=" * 60)
        print("Executing LLM Call Activity...")
        llm_response = await workflow.execute_activity(
            llm_call_activity,
            prompt,
            start_to_close_timeout=timedelta(seconds=30),
        )
        print("LLM Call Completed.")
        print("\n" + "=" * 60)
        print("LLM Response:", llm_response)
        return llm_response
          