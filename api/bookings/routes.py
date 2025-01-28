import uuid
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import parse_obj_as

from typing import List, Union

from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.dependencies import get_current_user
from api.models import User

from .schemas import BookingRead, BookingUserRead, BookingConfirm
from .service import BookingDAO, confirmed_booking
from api.db.data import get_session

from ..errors import DateFromCannotBeAfterDateTo, NotFoundException, NotFoundBooking

from api.tasks.tasks import send_booking_confirmation_email

router = APIRouter()


@router.post('')
async def add_booking(
        room_uid: uuid.UUID,
        date_from: date = Query(
            ..., description=f'Например, {(datetime.now() + timedelta()).date()}'
        ),
        date_to: date = Query(
            ..., description=f'Например, {(datetime.now() + timedelta(days=7)).date()}'
        ),
        user: User = Depends(get_current_user)
):
    """Позволяет добавить бронирование."""
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    booking = await BookingDAO.add_booking_object(
        user_uid=user.uid, room_uid=room_uid,
        date_from=date_from, date_to=date_to
    )

    if booking is None:
        raise NotFoundBooking

    booking_dict = parse_obj_as(BookingRead, booking).dict()
    send_booking_confirmation_email.delay(
        booking=booking_dict, email_to=user.email
    )
    return booking_dict


@router.get("", response_model=Union[List[BookingUserRead], str])
async def get_user_bookings(user: User = Depends(get_current_user)):
    """Возвращает все бронирования текущего пользователя."""
    user_bookings = await BookingDAO.get_user_bookings_object(user_uid=user.uid)

    if not user_bookings:
        return "У вас нет бронирований."
    return await BookingDAO.get_user_bookings_object(user_uid=user.uid)


@router.get("/{booking_uid}", response_model=BookingRead)
async def get_booking(booking_uid: uuid.UUID):
    """Возвращает бронирование по id."""
    booking = await BookingDAO.get_object(uid=booking_uid)

    if not booking:
        raise NotFoundException
    return booking


@router.delete("/{booking_uid}")
async def delete_booking(
    booking_uid: uuid.UUID, user: User = Depends(get_current_user)
):
    """Удаляет конкретное бронирование пользователя."""
    return await BookingDAO.delete_object(
        uid=booking_uid, user_uid=user.uid
    )


@router.post("/confirm_booking")
async def confirm_booking_route(
    booking_data: BookingConfirm, db: AsyncSession = Depends(get_session)
):
    try:
        booking = await confirmed_booking(booking_data, db)
        return {"message": "Бронирование подтверждено", "booking": booking}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
