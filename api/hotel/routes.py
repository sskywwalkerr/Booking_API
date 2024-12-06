from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.dependencies import AccessTokenBearer, RoleChecker
from api.db.data import get_session
from api.hotel.schemas import Hotel, HotelUpdateModel
from api.hotel.service import HotelService

from .schemas import HotelCreateModel
from ..errors import HotelNotFound

hotel_router = APIRouter()
hotel_service = HotelService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "user"]))


@hotel_router.get("/", response_model=List[Hotel], dependencies=[role_checker])
async def get_all_hotels_info(
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
):
    hotels = await hotel_service.get_all_hotels(session)
    return hotels


@hotel_router.get(
    "/user/{user_uid}", response_model=List[Hotel], dependencies=[role_checker]
)
async def get_user_hotel_info(
        user_uid: str,
        session: AsyncSession = Depends(get_session),
        _: dict = Depends(access_token_bearer),
):
    hotels = await hotel_service.get_user_hotels_reviews(user_uid, session)
    return hotels


@hotel_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Hotel,
    dependencies=[role_checker],
)
async def create_a_hotel_info(
    hotel_data: HotelCreateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> dict:
    hotel_id = token_details.get("user")["user_uid"]
    new_hotel = await hotel_service.create_hotel(hotel_data, hotel_id, session)
    return new_hotel


@hotel_router.patch("/{hotel_uid}", response_model=Hotel, dependencies=[role_checker])
async def update_hotel_info(
    hotel_uid: str,
    hotel_update_data: HotelUpdateModel,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
) -> dict:
    updated_hotel = await hotel_service.update_hotel_info(hotel_uid, hotel_update_data, session)

    if updated_hotel is None:
        raise HotelNotFound()
    else:
        return updated_hotel


@hotel_router.delete(
    "/{hotel_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker]
)
async def delete_hotel_info(
    hotel_uid: str,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(access_token_bearer),
):
    hotel_to_delete = await hotel_service.delete_hotel(hotel_uid, session)

    if hotel_to_delete is None:
        raise HotelNotFound()
    else:
        return {}

