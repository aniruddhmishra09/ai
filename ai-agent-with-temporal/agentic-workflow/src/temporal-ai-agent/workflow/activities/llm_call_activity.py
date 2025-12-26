from temporalio import activity
from integration.ollama.llm_prompt_handler import llm_call
from model.llm_prompt_model import LLMPromptModel

@activity.defn
def llm_call_activity(input: LLMPromptModel) -> str:
    weather_type = llm_call(input)
    return weather_type