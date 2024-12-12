from pydantic import BaseModel
import uuid


class RoomRead(BaseModel):
    """Модель отображения комнаты."""

    uid: uuid.UUID
    name: str
    description: str
    price: float
    quantity: int
    hotel_uid: uuid.UUID


class RoomCreateModel(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

    class Config:
        orm_mode = True

