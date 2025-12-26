import requests
import json
from typing import Dict, Any, Optional

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
    
    def check_country_applicability(self, country: str) -> ApplicabilityCheckResponseModel:
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
                return ApplicabilityCheckResponseModel(
                    applicable=data.get("applicable", False),
                    status_code=response.status_code
                )
            else:
                return ApplicabilityCheckResponseModel(
                    applicable=False,
                    status_code=response.status_code,
                    error=f"HTTP {response.status_code}: {response.text}"
                )
        
        except requests.exceptions.Timeout:
            return ApplicabilityCheckResponseModel(
                applicable=False,
                status_code=0,
                error="Request timeout"
            )
        
        except requests.exceptions.ConnectionError:
            return ApplicabilityCheckResponseModel(
                applicable=False,
                status_code=0,
                error=f"Connection error: Unable to reach {url}"
            )
        
        except json.JSONDecodeError:
            return ApplicabilityCheckResponseModel(
                applicable=False,
                status_code=response.status_code,
                error="Invalid JSON response"
            )
        
        except Exception as e:
            return ApplicabilityCheckResponseModel(
                applicable=False,
                status_code=0,
                error=f"Unexpected error: {str(e)}"
            )
    
    def check_multiple_countries(self, countries: list) -> Dict[str, ApplicabilityCheckResponseModel]:
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
def check_weather_alert_applicability(input: ApplicabilityCheckRequestModel, base_url: str = "http://localhost:8082") -> ApplicabilityCheckResponseModel:
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



