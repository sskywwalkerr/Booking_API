import uuid
from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BookingRead(BaseModel):
    """Модель отображения бронирования."""

    uid: uuid.UUID
    date_from: date
    date_to: date
    price: int
    total_days: int
    total_cost: int
    room_uid: Optional[uuid.UUID]
    user_uid: Optional[uuid.UUID]

    class Config:
        orm_mode = True


class BookingUserRead(BaseModel):
    """Модель отображения бронирования пользователя."""

    uid: uuid.UUID
    date_from: date
    date_to: date
    price: int
    total_days: int
    total_cost: int
    user_uid: Optional[uuid.UUID]
    room_uid: Optional[uuid.UUID]
    name: str
    description: str

    class Config:
        orm_mode = True
