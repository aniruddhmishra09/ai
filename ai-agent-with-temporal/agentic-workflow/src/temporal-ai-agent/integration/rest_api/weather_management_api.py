import requests
import json

from integration.rest_api.model.applicability_check_response_model import ApplicabilityCheckResponseModel
from integration.rest_api.model.applicability_check_request_model  import ApplicabilityCheckRequestModel
from integration.rest_api.model.weather_reporter_response_model import WeatherReporterResponseModel
from integration.rest_api.model.weather_reporter_request_model  import WeatherReporterRequestModel

country_applicability_url = "/country-applicability"
weather_reporter_url = "/weather-reporter"
weather_management_host_url = "http://localhost:8082"
weather_management_api_url = "/api/v1/weather-alert-management"

class WeatherManagementApiClient:
    """REST client for checking weather alert applicability by country"""
    
    def __init__(self, weather_management_host_url: str = "http://localhost:8082"):
        """
        Initialize the REST client.
        
        Args:
            base_url: Base URL of the API server (default: http://localhost:8082)
        """
        self.weather_management_host_url = weather_management_host_url.rstrip('/')
        self.check_country_applicability_endpoint = f"{self.weather_management_host_url}{weather_management_api_url}{country_applicability_url}"
        self.weather_reporter_endpoint = f"{self.weather_management_host_url}{weather_management_api_url}{weather_reporter_url}"

    def fetch_weather_reporter_by_country(self, input: WeatherReporterRequestModel) -> WeatherReporterResponseModel:
        """
        Fetch weather reporter information for a specific country.
        
        Args:
            input: WeatherReporterRequestModel containing country information
        """
        # Build the full URL
        url = f"{self.weather_reporter_endpoint}/{input.country}"
       
        try:
            # Make GET request
            response = requests.get(url, timeout=10)
            
            # Parse response
            if response.status_code == 200:
                data = response.json()
                return WeatherReporterResponseModel(
                    reporter_name=data.get("reporterName", ""),
                    reporter_user_name=data.get("reporterUserName", ""),
                    status_code=response.status_code
                )
            else:
                return WeatherReporterResponseModel(
                    reporter_name="",
                    reporter_user_name="",
                    status_code=response.status_code,
                    error=f"HTTP {response.status_code}: {response.text}"
                )
        
        except requests.exceptions.Timeout:
            return WeatherReporterResponseModel(
                reporter_name="",
                reporter_user_name="",
                status_code=0,
                error="Request timeout"
            )
        
        except requests.exceptions.ConnectionError:
            return WeatherReporterResponseModel(
                reporter_name="",
                reporter_user_name="",
                status_code=0,
                error=f"Connection error: Unable to reach {url}"
            )
        
        except json.JSONDecodeError:
            return WeatherReporterResponseModel(
                reporter_name="",
                reporter_user_name="",
                status_code=response.status_code,
                error="Invalid JSON response"
            )
        
        except Exception as e:
            return WeatherReporterResponseModel(
                reporter_name="",
                reporter_user_name="",
                status_code=0,
                error=f"Unexpected error: {str(e)}"
            )
    
    def check_country_applicability(self, input: ApplicabilityCheckRequestModel) -> ApplicabilityCheckResponseModel:
        """
        Check if weather alerts are applicable for a given country.
        
        Args:
            input: ApplicabilityCheckRequestModel containing country information
            
        Returns:
            ApplicabilityResponse object with applicable status
        """
        # Build the full URL
        
        url = f"{self.check_country_applicability_endpoint}/{input.country}"
        
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
    client = WeatherManagementApiClient(base_url)
    response = client.check_country_applicability(input)
    
    if response.error:
        print(f"Error checking applicability for {input.country}: {response.error}")

    return response

def fetch_weather_reporter_by_country(input: WeatherReporterRequestModel, base_url: str = "http://localhost:8082") -> WeatherReporterResponseModel:
    """
    Fetch weather reporter information for a specific country.
    
    Args:
        country_name: Name of the country to check
        base_url: API server URL (default: http://localhost:8082)
    """
    client = WeatherManagementApiClient(base_url)
    response = client.fetch_weather_reporter_by_country(input)
    
    if response.error:
        print(f"Error fetching weather reporter for {input.country}: {response.error}")

    return response
    



