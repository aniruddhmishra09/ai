import importlib.util
from pathlib import Path
from temporalio import activity

applicability_check_request_model_path = Path(__file__).parent.parent.parent / "model" / "applicability_check_request_model.py"
spec = importlib.util.spec_from_file_location("applicability_check_request_model", applicability_check_request_model_path)
applicability_check_request_model_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(applicability_check_request_model_module)
ApplicabilityCheckRequestModel = applicability_check_request_model_module.ApplicabilityCheckRequestModel

applicability_check_response_model_path = Path(__file__).parent.parent.parent / "model" / "applicability_check_response_model.py"
spec = importlib.util.spec_from_file_location("applicability_check_response_model", applicability_check_response_model_path)
applicability_check_response_model_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(applicability_check_response_model_module)
ApplicabilityCheckResponseModel = applicability_check_response_model_module.ApplicabilityCheckResponseModel

check_weather_alert_applicability_path = Path(__file__).parent.parent.parent / "integration/applicability" / "check-weather-alert-applicability.py"
spec = importlib.util.spec_from_file_location("check_weather_alert_applicability", check_weather_alert_applicability_path)
check_weather_alert_applicability_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_weather_alert_applicability_module)
check_weather_alert_applicability = check_weather_alert_applicability_module.check_weather_alert_applicability


@activity.defn
def applicability_activity(input: ApplicabilityCheckRequestModel) -> ApplicabilityCheckResponseModel:
    applicability_check = check_weather_alert_applicability(input)
    return applicability_check