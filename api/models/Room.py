from sqlalchemy import Column, Float, ForeignKey, String, Integer
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
from uuid import uuid4

from api.database.db import Base


class Room(Base):
    """Модель комнаты."""

    __tablename__ = "room"

    uid = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(length=150), nullable=False)
    description = Column(String(length=500), nullable=True)
    price = Column(Integer)
    quantity = Column(Integer, nullable=False)

    hotel_uid = Column(PGUUID(as_uuid=True), ForeignKey("hotels.uid"), nullable=False)

    hotel = relationship("Hotel", back_populates="room")
    # booking = relationship("Booking", back_populates="room")

    def __str__(self):
        return f'Комната: uid - {self.uid}, название - {self.name}'
