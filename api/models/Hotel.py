from sqlalchemy import Column, DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

from api.database.db import Base


class Hotel(Base):
    """Модель отеля."""

    __tablename__ = "hotels"

    uid = Column(PGUUID, primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    location = Column(String)
    description = Column(String)
    rating = Column(Float)
    rooms = Column(String)
    published_date = Column(DateTime)
    user_uid = Column(PGUUID(as_uuid=True), ForeignKey("users.uid"))
    added_at = Column(DateTime, default=func.now())
    update_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="hotels")
    reviews = relationship("Review", back_populates="hotel")
    room = relationship("Room", back_populates="hotel")

    def __repr__(self):
        return f"<hotel {self.name}>"
