import uuid
from datetime import date, datetime
from typing import List

from pydantic import BaseModel


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

# class HotelDetailModel(BaseModel):


class HotelCreateModel(BaseModel):
    name: str
    location: str
    description: str
    rating: float
    rooms: str
    published_date: str


class HotelUpdateModel(BaseModel):
    name: str
    location: str
    description: str
    rating: float
    rooms: str
