from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from api.models.Hotel import Hotel
from api.models.Room import Room
from api.rooms.schemas import RoomCreateModel


class RoomService:
    async def create_room(
            self, room_data: RoomCreateModel, hotel_uid: str, session: AsyncSession
    ):
        # Проверяем, существует ли отель
        hotel_exists = await session.execute(select(Hotel).where(Hotel.uid == hotel_uid))
        if not hotel_exists.scalar():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found.")

        # Создаем новую комнату
        new_room = Room(**room_data.dict(), hotel_uid=hotel_uid)
        session.add(new_room)
        await session.commit()
        await session.refresh(new_room)  # Обновляем объект, чтобы получить значения по умолчанию
        return new_room

    async def delete_room(self, room_uid: str, session: AsyncSession):
        # Получаем комнату для удаления
        room_to_delete = await session.execute(select(Room).where(Room.uid == room_uid))
        room = room_to_delete.scalar_one_or_none()

        if room is not None:
            await session.delete(room)
            await session.commit()
            return {}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found.")
