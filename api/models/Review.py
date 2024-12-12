from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship

from sqlalchemy.sql import func
from uuid import uuid4

from api.database.db import Base


class Review(Base):
    """Модель отзывов."""

    __tablename__ = "reviews"

    uid = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    rating = Column(Integer, nullable=False)
    review_text = Column(String, nullable=False)
    user_uid = Column(PGUUID(as_uuid=True), ForeignKey("users.uid"))
    hotel_uid = Column(PGUUID(as_uuid=True), ForeignKey("hotels.uid"))
    created_at = Column(DateTime, default=func.now())
    update_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="reviews")
    hotel = relationship("Hotel", back_populates="reviews")

    def __repr__(self):
        return f"<Review for hotel {self.hotel_uid} by user {self.user_uid}>"
