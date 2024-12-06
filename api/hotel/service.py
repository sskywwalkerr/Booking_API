from datetime import datetime

from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from api.db.models import Hotel

from .schemas import HotelCreateModel, HotelUpdateModel


class HotelService:
    async def get_all_hotels(self, session: AsyncSession):
        statement = select(Hotel).order_by(desc(Hotel.added_at))

        result = await session.exec(statement)

        return result.all()

    async def get_user_hotels_reviews(self, user_uid: str, session: AsyncSession):
        statement = (
            select(Hotel)
            .where(Hotel.user_uid == user_uid)
            .order_by(desc(Hotel.added_at))
        )
        result = await session.exec(statement)
        return result.all()

    async def get_hotel(self, hotel_uid: str, session: AsyncSession):
        statement = select(Hotel).where(Hotel.uid == hotel_uid)

        result = await session.exec(statement)

        hotel = result.first()

        return hotel if hotel is not None else None

    async def create_hotel(
            self, hotel_data: HotelCreateModel, user_uid: str, session: AsyncSession
    ):
        hotel_data_dict = hotel_data.model_dump()

        new_hotel = Hotel(**hotel_data_dict)

        new_hotel.published_date = datetime.strptime(
            hotel_data_dict["published_date"], "%Y-%m-%d"
        )

        new_hotel.user_uid = user_uid

        session.add(new_hotel)

        await session.commit()

        return new_hotel

    async def update_hotel_info(
            self, hotel_uid: str, update_data: HotelUpdateModel, session: AsyncSession
    ):
        hotel_to_update = await self.get_hotel(hotel_uid, session)

        if hotel_to_update is not None:
            update_data_dict = update_data.model_dump()

            for k, v in update_data_dict.items():
                setattr(hotel_to_update, k, v)

            await session.commit()

            return hotel_to_update
        else:
            return None

    async def delete_hotel(self, hotel_uid: str, session: AsyncSession):
        hotel_to_delete = await self.get_hotel(hotel_uid, session)

        if hotel_to_delete is not None:
            await session.delete(hotel_to_delete)

            await session.commit()

            return {}

        else:
            return None
