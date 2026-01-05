from dataclasses import dataclass

@dataclass
class LLMPromptModel:
    prompt: str
    data_payload: str
    #llm_response_format : str