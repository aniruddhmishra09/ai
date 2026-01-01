from dataclasses import dataclass
from typing import Optional

@dataclass
class WeatherReporterResponseModel:
    reporter_name: str
    reporter_user_name: str
    status_code: int = 200
    error: Optional[str] = None