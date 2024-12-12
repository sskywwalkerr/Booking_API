# import uuid
# from datetime import date, datetime
# from typing import List, Optional
#
# import sqlalchemy.dialects.postgresql as pg
# from sqlmodel import Column, Field, Relationship, SQLModel
#
#
# class User(SQLModel, table=True):
#     __tablename__ = "users"
#     uid: uuid.UUID = Field(
#         sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
#     )
#     username: str
#     email: str
#     first_name: str
#     last_name: str
#     role: str = Field(
#         sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
#     )
#     is_verified: bool = Field(default=False)
#     password_hash: str = Field(
#         sa_column=Column(pg.VARCHAR, nullable=False), exclude=True
#     )
#     created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
#     update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
#     hotels: List["Hotel"] = Relationship(
#         back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
#     )
#     reviews: List["Review"] = Relationship(
#         back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
#     )
#
#     def __repr__(self):
#         return f"<User {self.username}>"
#
#
# class Hotel(SQLModel, table=True):
#     __tablename__ = "hotels"
#     uid: uuid.UUID = Field(
#         sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
#     )
#     name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
#     location: str
#     description: str
#     rating: float
#     rooms: str
#     published_date: date
#     user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
#     added_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
#     update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
#     user: Optional[User] = Relationship(back_populates="hotels")
#     reviews: List["Review"] = Relationship(
#         back_populates="hotel", sa_relationship_kwargs={"lazy": "selectin"}
#     )
#
#     def __repr__(self):
#         return f"<hotel {self.name}>"
#
#
# class Review(SQLModel, table=True):
#     __tablename__ = "reviews"
#     uid: uuid.UUID = Field(
#         sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
#     )
#     rating: int = Field(lt=5)
#     review_text: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
#     user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
#     hotel_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="hotels.uid")
#     created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
#     update_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
#     user: Optional[User] = Relationship(back_populates="reviews")
#     hotel: Optional[Hotel] = Relationship(back_populates="reviews")
#
#     def __repr__(self):
#         return f"<Review for hotel {self.hotel_uid} by user {self.user_uid}>"
#
#
# class Room(SQLModel, table=True):
#     __tablename__ = "room"
#     uid: uuid.UUID = Field(
#         sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
#     )
#     hotel_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="hotels.uid")
#     price: float
#     room_type: str
#
#     def __repr__(self):
#         return f"<room {self.uid}>"
#
#
# class Reservation(SQLModel, table=True):
#     __tablename__ = "reservation"
#     uid: uuid.UUID = Field(
#         sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
#     )
#     user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
#     room_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="room.uid")
#     start_date: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
#     end_date: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime))
#     status: str
#
#     def __repr__(self):
#         return f"<Reservation {self.uid}>"