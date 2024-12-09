from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.dependencies import RoleChecker, get_current_user
from api.db.data import get_session
from api.db.models import User
from api.reviews.schemas import ReviewCreateModel
from api.reviews.service import ReviewService

review_service = ReviewService()
review_router = APIRouter()
admin_role_checker = Depends(RoleChecker(["admin"]))
user_role_checker = Depends(RoleChecker(["user", "admin"]))


@review_router.get("/", dependencies=[admin_role_checker])
async def get_all_reviews(session: AsyncSession = Depends(get_session)):
    hotel = await review_service.get_all_reviews(session)

    return hotel


@review_router.get("/{review_uid}", dependencies=[user_role_checker])
async def get_review(review_uid: str, session: AsyncSession = Depends(get_session)):
    hotel = await review_service.get_review(review_uid, session)

    if not hotel:
        raise


@review_router.post("/{hotel_uid}", dependencies=[user_role_checker])
async def add_review_to_hotel(
    hotel_uid: str,
    review_data: ReviewCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    new_review = await review_service.add_review_to_hotel(
        user_email=current_user.email,
        review_data=review_data,
        hotel_uid=hotel_uid,
        session=session,
    )

    return new_review


@review_router.delete(
    "/{review_uid}",
    dependencies=[user_role_checker],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_review(
    review_uid: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    await review_service.delete_review_to_from_hotel(
        review_uid=review_uid, user_email=current_user.email, session=session
    )

    return None
