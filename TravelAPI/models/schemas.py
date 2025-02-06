from datetime import date

from pydantic import BaseModel
import uuid


class HotelTravel(BaseModel):
    uid: uuid.UUID
    name: str
    location: str
    price: str
    description: str


class SearchRequest(BaseModel):
    city: str
    # check_in: date
    # check_out: date
    # adults: int


class BookingRequest(BaseModel):
    hotel_uid: uuid.UUID
    user_uid: uuid.UUID
    # check_in: date
    # check_out: date


class GetSentiments(BaseModel):
    hotel_ids: str
