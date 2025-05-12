from pydantic import BaseModel
import uuid
from typing import Optional

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
    checkOutDate: str
    roomQuantity: int = 1
    currency: str = "USD"

class HotelSearchRequest(BaseModel):
    city_code: str
    radius: Optional[int] = None  # в метрах
    chain_codes: Optional[str] = None  # коды сетей отелей через запятую
    amenities: Optional[str] = None  # удобства через запятую
    ratings: Optional[str] = None  # рейтинги через запятую (1-5)
    limit: int = 10
    offset: int = 0

class HotelOffersRequest(BaseModel):
    hotel_ids: str  # ID отелей через запятую
    check_in_date: str  # формат YYYY-MM-DD
    check_out_date: str  # формат YYYY-MM-DD
    adults: int = 1
    room_quantity: int = 1
    currency: str = "USD"
    language: str = "en-US"