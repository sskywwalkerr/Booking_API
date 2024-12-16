import uuid
from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from api.auth.dependencies import AccessTokenBearer, RoleChecker
from api.rooms.schemas import RoomCreateModel
from api.rooms.service import RoomService, RoomDAO
from sqlalchemy.ext.asyncio import AsyncSession
from api.db.data import get_session
from .schemas import RoomRead
room_routes = APIRouter()
room_service = RoomService()
access_token_bearer = AccessTokenBearer()

admin_role_checker = Depends(RoleChecker(["admin"]))
user_role_checker = Depends(RoleChecker(["user", "admin"]))


@room_routes.post(
    "/",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
    dependencies=[admin_role_checker],
)
async def create_a_room_info(
    room_data: RoomCreateModel,
    hotel_uid: str,  # Предполагаем, что hotel_uid передается в запросе
    session: AsyncSession = Depends(get_session),
):
    new_room = await room_service.create_room(room_data, hotel_uid, session)
    return new_room


@room_routes.delete(
    "/{room_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[admin_role_checker],
)
async def delete_room_info(
    room_uid: str,
    session: AsyncSession = Depends(get_session),
):
    await room_service.delete_room(room_uid, session)
    return {}


@room_routes.get('', response_model=List[RoomRead])
async def get_all_rooms():
    """Возвращает все комнаты"""
    rooms = await RoomDAO.get_all_objects()

    if not rooms:
        raise HTTPException(status_code=404, detail="Данные не найдены")
    return rooms


@room_routes.get('/{room_uid}', response_model=RoomRead)
async def get_room(room_uid: uuid.UUID):
    """Возвращает конкретный тип комнаты."""
    room = await RoomDAO.get_object(uid=room_uid)

    if not room:
        raise HTTPException(status_code=404, detail="Данные не найдены")
    return room
