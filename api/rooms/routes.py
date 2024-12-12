from fastapi import APIRouter, Depends, status, HTTPException
from api.auth.dependencies import AccessTokenBearer, RoleChecker
from api.models.Room import Room
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
    status_code=status.HTTP_201_CREATED,
    response_model=None,
    dependencies=[role_checker],
)
async def create_a_room_info(
    room_data: RoomCreateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> dict:
    room_id = token_details.get("user")["user_uid"]
    new_room = await room_service.create_room(room_data, room_id, session)
    return new_room


@room_routes.delete(
    "/{room_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker]
)
async def delete_room_info(
    room_uid: str,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
):
    room_to_delete = await room_service.delete_room(room_uid, session)

    if room_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Что-то не так(")
    else:
        return {}
