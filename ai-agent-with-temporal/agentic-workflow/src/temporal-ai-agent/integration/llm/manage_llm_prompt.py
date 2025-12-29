
from model.llm_prompt_model import LLMPromptModel
from integration.llm.ollama.llm_prompt_handler import llm_call

promptQuestion_weatherType = "Categorize the Season if Weather Description is: "

def prepare_llm_prompt(weather_description):
    llm_prompt = LLMPromptModel(prompt=promptQuestion_weatherType, data_payload=weather_description)
    return llm_prompt

def process_weather_data(llm_prompt: LLMPromptModel):
    weather_type = llm_call(llm_prompt)
    print("\n" + "=" * 60)
    print("Identified Weather Type from LLM:")
    print(weather_type)
    print("\n" + "=" * 60)
    return weather_type