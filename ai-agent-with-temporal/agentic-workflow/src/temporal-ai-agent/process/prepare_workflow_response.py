from model.workflow_response_model import WorkFlowResponseModel
from model.weather_data_model import WeatherDataModel
from integration.rest_api.model.weather_reporter_response_model import WeatherReporterResponseModel
from model.workflow_request_model import WorkFlowRequestModel
from model.weather_reporter_model import WeatherReporterModel

def prepare_workflow_response(
                            weather_category: str,
                            workflow_request: WorkFlowRequestModel,
                            weather_reporter: WeatherReporterResponseModel
                            ) -> WorkFlowResponseModel:
    
    weather_reporter = WeatherReporterModel(
        reporter_name=weather_reporter.reporter_name,
        reporter_user_name=weather_reporter.reporter_user_name
    )

    workflow_response = WorkFlowResponseModel(

        weather_data=workflow_request.weather_record,
        weather_category=weather_category,
        weather_reporter=weather_reporter
    )
    return workflow_response