from temporalio import activity
from integration.llm.ollama.llm_prompt_handler import llm_call
from integration.llm.model.llm_prompt_model import LLMPromptModel

@activity.defn
def llm_call_activity(input: LLMPromptModel) -> str:
    llm_response = llm_call(input)
    return llm_response