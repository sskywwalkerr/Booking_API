from fastapi import APIRouter, Depends, status, HTTPException
from api.auth.dependencies import AccessTokenBearer, RoleChecker
from api.rooms.schemas import RoomCreateModel
from api.rooms.service import RoomService
from sqlalchemy.ext.asyncio import AsyncSession
from api.db.data import get_session

room_routes = APIRouter()
room_service = RoomService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "user"]))


@room_routes.post(
    "/",
    response_model=None,
    status_code=status.HTTP_201_CREATED,
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
)
async def delete_room_info(
    room_uid: str,
    session: AsyncSession = Depends(get_session),
):
    await room_service.delete_room(room_uid, session)
    return {}
