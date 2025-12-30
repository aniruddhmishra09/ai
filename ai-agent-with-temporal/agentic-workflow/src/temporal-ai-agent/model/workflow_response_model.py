from dataclasses import dataclass

@dataclass
class WorkFlowRequestModel:
    prompt: str
    data_payload: str