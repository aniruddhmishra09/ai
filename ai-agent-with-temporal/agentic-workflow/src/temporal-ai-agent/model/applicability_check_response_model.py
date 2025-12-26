from dataclasses import dataclass
from typing import Optional

class ApplicabilityCheckResponseModel:
    """Response model for weather alert applicability check"""
    applicable: bool
    status_code: int = 200
    error: Optional[str] = None