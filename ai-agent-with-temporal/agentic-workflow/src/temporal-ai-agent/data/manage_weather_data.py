import json
import os
from pathlib import Path
from typing import Dict, List, Any
from model.weather_data_model import WeatherDataModel


def load_weather_data() -> Dict[str, Any]:
    """
    Load weather alerts data from the JSON file.
    
    Returns:
        Dict containing the JSON response with weather data.
    """
    # Get the path to weather-alerts.json
    weather_file = Path("/Users/apple/Aniruddh/Work/Study/Workspace/ai/ai-agent-with-temporal/data/weather-alerts.json")
    
    try:
        with open(weather_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return {
            "status": "success",
            "data": data,
            "count": len(data),
            "message": f"Successfully loaded {len(data)} weather records"
        }
    
    except FileNotFoundError:
        return {
            "status": "error",
            "message": f"Weather data file not found at {weather_file}",
            "data": None
        }
    
    except json.JSONDecodeError as e:
        return {
            "status": "error",
            "message": f"Error parsing JSON file: {str(e)}",
            "data": None
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Unexpected error loading weather data: {str(e)}",
            "data": None
        }


def get_weather_by_city(city_name: str) -> Dict[str, Any]:
    """
    Get weather data for a specific city.
    
    Args:
        city_name: Name of the city to search for
        
    Returns:
        Dict containing weather data for the specified city
    """
    response = load_weather_data()
    
    if response["status"] != "success":
        return response
    
    weather_records = response["data"]
    city_data = [record for record in weather_records if record.get("city").lower() == city_name.lower()]
    
    if city_data:
        return {
            "status": "success",
            "data": city_data[0],
            "message": f"Found weather data for {city_name}"
        }
    else:
        return {
            "status": "not_found",
            "data": None,
            "message": f"No weather data found for city: {city_name}"
        }


def get_weather_by_country(country_name: str) -> Dict[str, Any]:
    """
    Get weather data for all cities in a specific country.
    
    Args:
        country_name: Name of the country to search for
        
    Returns:
        Dict containing weather data for all cities in the country
    """
    response = load_weather_data()
    
    if response["status"] != "success":
        return response
    
    weather_records = response["data"]
    country_data = [record for record in weather_records if record.get("country").lower() == country_name.lower()]
    
    if country_data:
        return {
            "status": "success",
            "data": country_data,
            "count": len(country_data),
            "message": f"Found {len(country_data)} weather records for {country_name}"
        }
    else:
        return {
            "status": "not_found",
            "data": [],
            "count": 0,
            "message": f"No weather data found for country: {country_name}"
        }

from typing import Optional, Dict, Any


def weather_record_by_id(weather_alerts_response: Dict[str, Any], record_id: int) -> Optional[Dict[str, Any]]:
	"""
	Return a single weather record matching `record_id` from the
	`weather_alerts_response` returned by the application's loader.

	Args:
		weather_alerts_response: dict returned by `load_weather_data()` with keys
			like `status` and `data`.
		record_id: numeric id of the weather record to find.

	Returns:
		The matching record dict if found, otherwise None.
	"""
	
	if not weather_alerts_response or not weather_alerts_response.get("data"):
		return None

	data = weather_alerts_response.get("data", [])
	for rec in data:
		if rec is None:
			continue
		if str(rec.get("id")) == str(record_id):
			return rec

	return None


def prepare_data():
    print("\n" + "=" * 60)
    print("\nFetching weather alerts data...")
    # Store the response in a variable
    weather_alerts_data = load_weather_data()
    
    print(f"Weather alert Fetch Status: {weather_alerts_data['message']}")
    return weather_alerts_data
    
def fetch_weather_record(weather_alerts_response, record_id) -> WeatherDataModel:
    # Pass the full loader response and numeric id
    weather_record = weather_record_by_id(weather_alerts_response, record_id)
    if weather_record is None: 
        print(f"No weather record found with ID: {record_id}")
        return None 
    
    weather_data_model = WeatherDataModel(id=weather_record['id'],
        country=weather_record['country'],
        city=weather_record['city'],
        weather_description=weather_record['weather_description'],
        wikipedia_url=weather_record['wikipedia_url'])
    
    print("\n" + "=" * 60)
    print("Weather Record: \n\n", weather_data_model)

    return weather_data_model