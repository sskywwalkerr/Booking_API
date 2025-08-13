from pydantic import BaseModel


class Segment(BaseModel):
    origin: str
    destination: str
    date: str


class Passengers(BaseModel):
    adults: int = 1
    children: int = 0
    infants: int = 0


class SearchRequest(BaseModel):
    trip_class: str = "Y"
    locale: str = "ru"
    passengers: Passengers
    segments: list[Segment]
    user_ip: str


class SearchResponse(BaseModel):
    search_id: str


class BookingRequest(BaseModel):
    search_id: str
    url_code: int
    user_ip: str
