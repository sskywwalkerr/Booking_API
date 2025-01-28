import uuid
from datetime import date


from pydantic import BaseModel


class BookingRead(BaseModel):
    """Модель отображения бронирования."""

    uid: uuid.UUID
    date_from: date
    date_to: date
    price: int
    total_days: int
    total_cost: int
    room_uid: uuid.UUID
    user_uid: uuid.UUID

    class Config:
        from_attributes = True


class BookingUserRead(BaseModel):
    """Модель отображения бронирования пользователя."""

    uid: uuid.UUID
    date_from: date
    date_to: date
    price: int
    total_days: int
    total_cost: int
    user_uid: uuid.UUID
    room_uid: uuid.UUID
    name: str
    description: str

    class Config:
        from_attributes = True


class BookingConfirm(BaseModel):
    uid: uuid.UUID
    confirmed: bool

    class Config:
        from_attributes = True
