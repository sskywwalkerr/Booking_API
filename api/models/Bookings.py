from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Computed, Date
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from uuid import uuid4

from api.database.db import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from api.models import User, Room


class Booking(Base):
    """Модель бронирования."""

    __tablename__ = "bookings"

    uid = Column(PGUUID, primary_key=True, default=uuid4)
    date_from: Mapped[datetime] = mapped_column(Date, nullable=False)
    date_to: Mapped[datetime] = mapped_column(Date, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    total_days: Mapped[int] = mapped_column(
        Integer, Computed('date_to - date_from'), nullable=False
    )
    total_cost: Mapped[int] = mapped_column(
        Integer, Computed('(date_to - date_from) * price'),
        nullable=False
    )

    room_uid = Column(PGUUID(as_uuid=True), ForeignKey("room.uid"))
    user_uid = Column(PGUUID(as_uuid=True), ForeignKey("users.uid"))

    # user = relationship("User", back_populates="bookings")
    # room = relationship("Room", back_populates="booking")
    user: Mapped["User"] = relationship(back_populates="bookings")
    room: Mapped["Room"] = relationship(back_populates="booking")

    def __str__(self):
        return f'Бронирование: uid - {self.uid}, c {self.date_from} по {self.date_to}'
