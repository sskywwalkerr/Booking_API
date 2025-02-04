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
    # check_in: str
    # check_out: str
    # adults: int


class BookingRequest(BaseModel):
    hotel_uid: uuid.UUID
    user_uid: uuid.UUID
    check_in: str
    check_out: str
