from pydantic import BaseModel
from datetime import date, datetime
import uuid


class Hotel(BaseModel):
    uid: uuid.UUID
    name: str
    location: str
    description: str
    rating: float
    published_date: date
    rooms: str
    added_at: datetime
    update_at: datetime


class HotelCreateModel(BaseModel):
    name: str
    location: str
    description: str
    rating: float
    rooms: str
    published_date: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "string",
                "location": "string",
                "description": "string",
                "rating": 0,
                "rooms": "string",
                "published_date": "2023-01-01"
            }
        }


class HotelUpdateModel(BaseModel):
    name: str
    location: str
    description: str
    rating: float
    rooms: str
