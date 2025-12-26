import requests
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass


from model.applicability_check_response_model import ApplicabilityCheckResponseModel
from model.applicability_check_request_model  import ApplicabilityCheckRequestModel

class WeatherAlertApplicabilityClient:
    """REST client for checking weather alert applicability by country"""
    
    def __init__(self, base_url: str = "http://localhost:8082"):
        """
        Initialize the REST client.
        
        Args:
            base_url: Base URL of the API server (default: http://localhost:8082)
        """
        self.base_url = base_url.rstrip('/')
        self.endpoint = "/api/v1/weather-alert-management/country-applicability"
    
    def check_country_applicability(self, country: str) -> ApplicabilityResponseModel:
        """
        Check if weather alerts are applicable for a given country.
        
        Args:
            country: Country name to check applicability for
            
        Returns:
            ApplicabilityResponse object with applicable status
        """
        # Build the full URL
        url = f"{self.base_url}{self.endpoint}/{country}"
        
        try:
            # Make GET request
            response = requests.get(url, timeout=10)
            
            # Parse response
            if response.status_code == 200:
                data = response.json()
                return ApplicabilityResponseModel(
                    applicable=data.get("applicable", False),
                    status_code=response.status_code
                )
            else:
                return ApplicabilityResponseModel(
                    applicable=False,
                    status_code=response.status_code,
                    error=f"HTTP {response.status_code}: {response.text}"
                )
        
        except requests.exceptions.Timeout:
            return ApplicabilityResponseModel(
                applicable=False,
                status_code=0,
                error="Request timeout"
            )
        
        except requests.exceptions.ConnectionError:
            return ApplicabilityResponseModel(
                applicable=False,
                status_code=0,
                error=f"Connection error: Unable to reach {url}"
            )
        
        except json.JSONDecodeError:
            return ApplicabilityResponseModel(
                applicable=False,
                status_code=response.status_code,
                error="Invalid JSON response"
            )
        
        except Exception as e:
            return ApplicabilityResponseModel(
                applicable=False,
                status_code=0,
                error=f"Unexpected error: {str(e)}"
            )
    
    def check_multiple_countries(self, countries: list) -> Dict[str, ApplicabilityResponseModel]:
        """
        Check applicability for multiple countries.
        
        Args:
            countries: List of country names to check
            
        Returns:
            Dictionary mapping country names to ApplicabilityResponse objects
        """
        results = {}
        for country in countries:
            results[country] = self.check_country_applicability(country)
        return results


# Helper function for quick access
def check_weather_alert_applicability(input: ApplicabilityCheckRequestModel, base_url: str = "http://localhost:8082") -> ApplicabilityResponseModel:
    """
    Quick function to check if weather alerts are applicable for a country.
    
    Args:
        country: Country name to check
        base_url: API server URL (default: http://localhost:8082)
        
    Returns:
        Boolean indicating if weather alerts are applicable
    """
    client = WeatherAlertApplicabilityClient(base_url)
    response = client.check_country_applicability(input.country)
    
    if response.error:
        print(f"Error checking applicability for {input.country}: {response.error}")

    return response


if __name__ == "__main__":
    # Test the client
    client = WeatherAlertApplicabilityClient()
    
    # Test single country
    print("Testing single country applicability check...")
    test_countries = ["United States", "United Kingdom", "France", "Germany", "Spain"]
    
    for country in test_countries:
        result = client.check_country_applicability(country)
        print(f"\n{country}:")
        print(f"  Applicable: {result.applicable}")
        print(f"  Status Code: {result.status_code}")
        if result.error:
            print(f"  Error: {result.error}")
