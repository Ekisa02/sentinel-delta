from pydantic import BaseModel, Field
from typing import List, Dict, Any


class Event(BaseModel):
    contract: str
    nonce: int
    value: float
    gas_used: int
    timestamp: int


class PredictRequest(BaseModel):
    events: List[Event]


class PredictResponse(BaseModel):
    anomalies: List[float]
    meta: Dict[str, Any] = Field(default_factory=dict)


class TrainRequest(BaseModel):
    epochs: int = 5
    lr: float = 1e-3

