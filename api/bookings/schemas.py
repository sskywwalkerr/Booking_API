from datetime import date
from typing import List

from pydantic import BaseModel


class BookingRead(BaseModel):
    """Модель отображения бронирования."""

    uid: int
    date_from: date
    date_to: date
    price: int
    total_days: int
    total_cost: int
    room_uid: int
    user_uid: int


class BookingUserRead(BaseModel):
    """Модель отображения бронирования пользователя."""

    uid: int
    date_from: date
    date_to: date
    price: int
    total_days: int
    total_cost: int
    user_uid: int
    room_uid: int
    name: str
    description: str
