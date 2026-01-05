import os
from dotenv import load_dotenv
import ollama 
from pydantic import BaseModel, Field
import instructor

weather_description = "Clear and sunny skies dominate New York today with brilliant blue heavens stretching across the entire metropolitan area. The temperature is pleasant and comfortable, making it an ideal day for outdoor activities and sightseeing. The sun shines brightly, casting sharp shadows and illuminating the iconic skyscrapers of Manhattan with golden light. There is minimal cloud cover, and the air is crisp with excellent visibility extending for miles. The gentle breeze provides relief from any potential heat buildup, creating perfect conditions for walking through Central Park or exploring the bustling streets. The ultraviolet index is moderate, so sun protection is still recommended for extended outdoor exposure."
promptQuestion_weatherType = "Categorize the Season if Weather Description is: "
promptQuestion_weatherActivities = "Suggest 5 Outdoor Activities suitable for the Season if Weather Description is: "
prompt_response_json_format = '{"weatherCategory":"Clear","activities":[{"activityName":"Hiking","suitableTime":"Morning","recommendedGear":["Hiking boots", "Sunscreen", "Water bottle"]}]}'

class WeatherActivities(BaseModel):
    activityName: str = Field(description="The name of the activity based on the weather description.")
    suitableTime: str = Field(description="The suitable time to perform the activity based on the weather description..")
    recommendedGear: list[str] = Field(description="A list of recommended gear for the activity based on the weather description..")
    

class WeatherResponse(BaseModel):
    weatherSeason: str = Field(description="The season of the weather based on the weather description.")
    activities: list[WeatherActivities] = Field(description="A list of activities suitable for the weather description.")

WeatherResponse.model_json_schema()

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
        ollama_client = ollama.Client(host=OLLAMA_HOST)
    return ollama_client

def get_client():
   client = instructor.from_ollama(
        client=ollama.Client(host=OLLAMA_HOST),
        model=OLLAMA_MODEL, # Use a capable model
        mode=instructor.Mode.JSON,)
   return client


def llm_call(prompt_question: str, data_payload: str) -> str:
    """Call ollama model and return response text."""
    client = get_ollama_client()
    #client = get_client()

    print(f"Using LLM to Process Request. LLM-Model: {OLLAMA_MODEL}")
    llm_input = prompt_question + data_payload
    print(f"\nPrompt:\n{llm_input}\n")
    response = client.generate(model=OLLAMA_MODEL, prompt=llm_input, stream=False , format=WeatherResponse.model_json_schema())
    return response.get("response", "")

if __name__ == "__main__":
    
    # Call the LLM
    llm_response = llm_call(promptQuestion_weatherType, weather_description)
    
    # Print the response
    print("LLM Response:\n", llm_response)