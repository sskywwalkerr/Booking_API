from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
from uuid import uuid4

from api.database.db import Base


class Room(Base):
    __tablename__ = "room"

    uid = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    hotel_uid = Column(PGUUID(as_uuid=True), ForeignKey("hotels.uid"))
    price = Column(Float)
    room_type = Column(String)

    # hotel = relationship("Hotel", foreign_keys="Room.hotel_uid")

    def __repr__(self):
        return f"<room {self.uid}>"
