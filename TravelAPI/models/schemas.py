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


class BookingRequest(BaseModel):
    hotel_uid: uuid.UUID
    user_uid: uuid.UUID


class GetSentiments(BaseModel):
    hotel_ids: str


class GetPrices(BaseModel):
    hotel_ids: str
    adults: int = 1
    checkInDate: str
    roomQuantity: int = 1
