from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from api.models.Room import Room
from api.rooms.schemas import RoomCreateModel


class RoomService:
    async def create_room(
            self, room_data: RoomCreateModel, hotel_uid: str, session: AsyncSession
    ):
        room_data_dict = room_data.model_dump()

        new_room = Room(**room_data_dict)

        new_room.hotel_uid = hotel_uid

        session.add(new_room)

        await session.commit()

        return new_room

    async def get_room(self, room_uid: str, session: AsyncSession):
        statement = select(Room).where(Room.uid == room_uid)

        result = await session.exec(statement)

        room = result.first()

        return room if room is not None else None

    async def delete_room(self, room_uid: str, session: AsyncSession):
        room_to_delete = await self.get_room(room_uid, session)

        if room_to_delete is not None:
            await session.delete(room_to_delete)

            await session.commit()

            return {}

        else:
            return None
