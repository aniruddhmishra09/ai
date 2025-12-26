from typing import Dict
from model.applicability_check_request_model import ApplicabilityCheckRequestModel
from integration.applicability.check_weather_alert_applicability import check_weather_alert_applicability


if __name__ == "__main__":
    # Test the client
    
    
    # Test single country
    print("Testing single country applicability check...")
    #test_country = "United States"
    #input = ApplicabilityCheckRequestModel(country=test_country)
    #result = check_weather_alert_applicability(input)   
    test_countries = ["United States", "United Kingdom", "France", "Germany", "Spain"]
    
    for country in test_countries:
        result = check_weather_alert_applicability(ApplicabilityCheckRequestModel(country=country)) 
        print(f"\n{country}:")
        print(f"  Applicable: {result.applicable}")
        print(f"  Status Code: {result.status_code}")
        if result.error:
            print(f"  Error: {result.error}")