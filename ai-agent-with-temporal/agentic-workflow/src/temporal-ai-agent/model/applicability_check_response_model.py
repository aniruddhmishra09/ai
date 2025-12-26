from dataclasses import dataclass
from typing import Optional

@dataclass
class ApplicabilityCheckResponseModel:
    applicable: bool
    status_code: int = 200
    error: Optional[str] = None