import os
from dotenv import load_dotenv
from ollama import Client
from integration.llm.model.llm_prompt_model import LLMPromptModel
from pydantic import BaseModel, Field
import instructor

class WeatherActivities(BaseModel):
    activityName: str = Field(description="The name of the activity based on the weather description.")
    suitableTime: str = Field(description="The suitable time to perform the activity based on the weather description..")
    recommendedGear: list[str] = Field(description="A list of recommended gear for the activity based on the weather description..")
    

class WeatherResponse(BaseModel):
    weatherSeason: str = Field(description="The season of the weather based on the weather description.")
    activities: list[WeatherActivities] = Field(description="A list of activities suitable for the weather description.")



load_dotenv(override=True)

# Ollama configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")  # Change to your available model
ollama_client = None


def get_ollama_client():
    """Get or create ollama client instance."""
    global ollama_client
    if ollama_client is None:
        print(f"Connecting to Ollama at {OLLAMA_HOST}")
        ollama_client = Client(host=OLLAMA_HOST)
    return ollama_client


def llm_call(input: LLMPromptModel) -> str:
    """Call ollama model and return response text."""
    client = get_ollama_client()
    print(f"Using LLM to Process Request. LLM-Model: {OLLAMA_MODEL}")
    llm_input = input.prompt + input.data_payload
    print(f"\nPrompt:\n{llm_input}\n")
    response = client.generate(model=OLLAMA_MODEL, prompt=llm_input, stream=False , format=WeatherActivities.model_json_schema())
    return response.get("response", "")

