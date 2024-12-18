import uuid
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import parse_obj_as

from typing import List, Union

from api.auth.dependencies import get_current_user
from api.models import User
from .service import BookingDAO
from .schemas import BookingRead, BookingUserRead
from api.celery_tasks import send_email, send_booking_confirmation_email
from ..errors import DateFromCannotBeAfterDateTo, NotFoundException

router = APIRouter(
    prefix='/bookings',
    tags=['bookings']
)


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
        raise HTTPException(status_code=500, detail="Не удалось создать бронирование")

    booking_dict = parse_obj_as(BookingRead, booking).dict()
    send_booking_confirmation_email.delay(
        booking=booking_dict, email_to=user.email
    )
    return booking_dict


@router.get("", response_model=Union[List[BookingRead], str])
async def get_user_bookins(user: User = Depends(get_current_user)):
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
