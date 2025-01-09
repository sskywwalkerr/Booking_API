import uuid
from datetime import date

from celery.worker.control import conf
from fastapi import BackgroundTasks
from fastapi_mail import FastMail
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, func, insert, or_, select, update

from sqlalchemy.ext.asyncio import AsyncSession
from api.bookings.schemas import BookingConfirm

from api.dao.base import BaseDAO
from api.db.data import async_session_maker
from api.errors import RoomCantBookedException
from api.logger import logger
from api.models.Bookings import Booking, BookingStatus
from api.models.Room import Room
from api.tasks.email_templates import create_booking_confirmation_template


class BookingDAO(BaseDAO):
    model = Booking

    @classmethod
    async def add_booking_object(
        cls,
        user_uid: uuid.UUID,
        room_uid: uuid.UUID,
        date_from: date,
        date_to: date,
    ):
        """Добавляет объект бронирования в БД."""
        try:
            async with async_session_maker() as session:
                booked_rooms = select(Booking).where(
                    and_(
                        Booking.room_uid == room_uid,
                        or_(
                            and_(
                                Booking.date_from >= date_from,
                                Booking.date_from <= date_to
                            ),
                            and_(
                                Booking.date_from <= date_from,
                                Booking.date_to > date_from
                            )
                        )
                    )
                ).cte('booked_rooms')

                get_available_rooms = (
                        select(
                            (Room.quantity - func.count(booked_rooms.c.room_uid))
                            .label('rooms_available')
                        )
                        .select_from(Room)
                        .join(
                            booked_rooms, booked_rooms.c.room_uid == Room.uid,
                            isouter=True
                        )
                        .where(Room.uid == room_uid)
                        .group_by(Room.quantity, booked_rooms.c.room_uid)
                    )

            rooms_available = await session.execute(get_available_rooms)
            rooms_available = rooms_available.scalar() or 0

            if not rooms_available:
                raise RoomCantBookedException

            # Логика получения цены и добавления бронирования
            get_room_price = select(Room.price).filter_by(uid=room_uid)
            price = await session.execute(get_room_price)
            price = price.scalar()

            add_booking = insert(Booking).values(
                user_uid=user_uid,
                room_uid=room_uid,
                date_from=date_from,
                date_to=date_to,
                price=price
            ).returning(
                Booking.uid, Booking.date_from, Booking.date_to,
                Booking.price, Booking.total_days,
                Booking.total_cost, Booking.room_uid,
                Booking.user_uid
            )

            new_booking = await session.execute(add_booking)
            await session.commit()
            return new_booking.mappings().one()

        except RoomCantBookedException:
            raise RoomCantBookedException

        except (SQLAlchemyError, Exception) as error:
            if isinstance(error, SQLAlchemyError):
                message = 'Database Exception'
            elif isinstance(error, Exception):
                message = 'Unknow Exception'
            message += ': Невозможно добавить бронирование'
            extra = {
                'user_uid': user_uid,
                'room_uid': room_uid,
                'date_from': date_from,
                'date_to': date_to,
            }
            logger.error(message, extra=extra, exc_info=True)

    @classmethod
    async def get_user_bookings_object(cls, user_uid: uuid.UUID):
        """Возвращает все бронирования текущего пользователя."""
        async with async_session_maker() as session:
            get_user_bookings = (
                select(
                    Booking.__table__.columns,
                    Room.__table__.columns
                )
                .join(
                    Room,
                    Booking.room_uid == Room.uid,
                    isouter=True)
                .where(
                    Booking.user_uid == user_uid
                )
            )

            user_bookings = await session.execute(get_user_bookings)
            return user_bookings.mappings().all()


async def confirmed_booking(booking_data: BookingConfirm, db: AsyncSession):
    async with db.begin():
        # Найти бронь по uid
        result = await db.execute(select(Booking).where(Booking.uid == booking_data.uid))
        booking = result.scalar_one_or_none()

    if booking is None:
        raise ValueError("Бронирование не найдено")

    # Обновление поля confirmed
    await db.execute(update(Booking).where(Booking.uid == booking.uid).values(is_confirmed=booking_data.confirmed))
    await db.commit()

    return booking


# async def confirmed_booking(booking_data: BookingConfirm, db: AsyncSession):
#     async with db.begin():
#          # Найти бронь по uid
#
#          result = await db.execute(select(Booking).where(Booking.uid == booking_data.uid))
#          booking = result.scalar_one_or_none()
#
#     if booking is None:
#          raise ValueError("Бронирование не найдено")
#
#     # Обновление статуса на CONFIRMED
#
#     await db.execute(update(Booking).where(Booking.uid == booking.uid).values(status=BookingStatus.CONFIRMED))
#     await db.commit()
#
# async def send_booking_confirmation_email(booking: Booking, email_to: str, background_tasks):
#     message = create_booking_confirmation_template(booking.dict(), email_to)
#     fm = FastMail(conf)
#     background_tasks.add_task(fm.send_message, message)