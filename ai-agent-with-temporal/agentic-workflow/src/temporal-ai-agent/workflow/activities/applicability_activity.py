import importlib.util
from pathlib import Path
from temporalio import activity
from model.applicability_check_request_model import ApplicabilityCheckRequestModel
from model.applicability_check_response_model import ApplicabilityCheckResponseModel
from integration.applicability.check_weather_alert_applicability import check_weather_alert_applicability

@activity.defn
def applicabiilty_check(input: ApplicabilityCheckRequestModel) -> ApplicabilityCheckResponseModel:
    applicabiilty_check = check_weather_alert_applicability(input)
    return applicabiilty_check