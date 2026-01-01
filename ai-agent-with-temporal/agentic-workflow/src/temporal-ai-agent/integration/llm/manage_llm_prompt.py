
from integration.llm.model.llm_prompt_model import LLMPromptModel
from integration.llm.ollama.llm_prompt_handler import llm_call

def prepare_llm_prompt(prompt_question, data_payload):
    llm_prompt = LLMPromptModel(prompt=prompt_question, data_payload=data_payload)
    return llm_prompt

def process_llm_prompt(llm_prompt: LLMPromptModel):
    llm_response = llm_call(llm_prompt)
    return llm_response