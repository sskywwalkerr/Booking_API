from pydantic import BaseModel
from typing import List, Optional


class FlightDestination(BaseModel):
    id: str
    name: str
    type: str
    country: str


class FlightDestinationResponse(BaseModel):
    results: List[FlightDestination]