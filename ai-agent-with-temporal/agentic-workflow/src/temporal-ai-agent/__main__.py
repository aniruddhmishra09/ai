import sys
import json
import importlib.util
from pathlib import Path

from model.llm_prompt_model import LLMPromptModel
from data.load_weather_data import load_weather_data
from data.weather_record_by_id import weather_record_by_id
from integration.ollama.llm_prompt_handler import llm_call


promptQuestion = "Categorize the Season if Weather Description is: "

def main():
    """
    Main entry point for the temporal AI agent application.
    """
    
    # Fetch weather alerts data
    print("\n" + "=" * 60)
    print("\nFetching weather alerts data...")
    # Store the response in a variable
    weather_alerts_response = load_weather_data()
    
    print(f"Weather alert Fetch Status: {weather_alerts_response['message']}")
   
    
    # Check if data was loaded successfully
    if weather_alerts_response['status'] == 'success':
        # Store the JSON response
        weather_data = weather_alerts_response['data']
        
        
        print("\n" + "=" * 60)
        weather_record_id = input("Enter your Weather Record ID: ").strip()
        print(f"\nProcessing Weather Record ID: {weather_record_id}")

        # convert input to integer ID
        try:
            record_id = int(weather_record_id)
        except ValueError:
            print("Invalid ID provided. Please enter a numeric weather record ID.")
            return weather_alerts_response

        

        # Pass the full loader response and numeric id
        weather_record = weather_record_by_id(weather_alerts_response, record_id)
        print("\n" + "=" * 60)
        
        print("Weather Record: \n\n", weather_record)
        weather_description = weather_record.get("weather_description", "No description available.")

        llm_prompt = LLMPromptModel(prompt=promptQuestion, data_payload=weather_description)
        
        weather_type = llm_call(llm_prompt)

        print("\n" + "=" * 60)
        print("Identified Weather Type from LLM:")
        print(weather_type)
        print("\n" + "=" * 60)


        return weather_alerts_response
    
    else:
        print(f"Error: {weather_alerts_response['message']}")
        return weather_alerts_response
    
    


if __name__ == "__main__":
    
    print("\n" + "=" * 60)
    print("Welcome to the Weather Management AI Agent!")
    result = main()
    print("\n" + "=" * 60)
