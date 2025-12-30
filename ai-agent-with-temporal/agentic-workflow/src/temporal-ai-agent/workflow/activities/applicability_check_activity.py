##Applicability Check Activity
from model.applicability_check_request_model import ApplicabilityCheckRequestModel
from model.applicability_check_response_model import ApplicabilityCheckResponseModel
from integration.applicability.check_weather_alert_applicability import check_weather_alert_applicability
from temporalio import activity

@activity.defn
def applicability_check_activity(input: ApplicabilityCheckRequestModel) -> ApplicabilityCheckResponseModel:
    
    applicability_check = check_weather_alert_applicability(input)
    return applicability_check