from pydantic import BaseModel
from typing import Optional
import uuid


class RoomRead(BaseModel):
    """Модель отображения комнаты."""

    uid: uuid.UUID
    name: str
    description: str
    price: float
    quantity: int
    hotel_uid: Optional[uuid.UUID]


class RoomCreateModel(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

