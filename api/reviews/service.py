import logging

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession

from api.auth.service import UserService
from api.models.Review import Review
from api.hotel.service import HotelService

from .schemas import ReviewCreateModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging
logger = logging.getLogger(__name__)

hotel_service = HotelService()
user_service = UserService()


class ReviewService:
    async def add_review_to_hotels(
        self,
        user_email: str,
        hotel_uid: str,
        review_data: ReviewCreateModel,
        session: AsyncSession,
    ):
        try:
            hotel = await hotel_service.get_hotel(hotel_uid=hotel_uid, session=session)
            user = await user_service.get_user_by_email(
                email=user_email, session=session
            )
            review_data_dict = review_data.model_dump()
            if not hotel:
                raise HTTPException(
                    detail="Hotel not found", status_code=status.HTTP_404_NOT_FOUND
                )

            if not user:
                raise HTTPException(
                    detail="User not found", status_code=status.HTTP_404_NOT_FOUND
                )

            new_review = Review(**review_data_dict, user=user, hotel=hotel)

            session.add(new_review)

            await session.commit()

            return new_review

        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                detail="something went wrong",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def get_review(self, review_uid: str, session: AsyncSession):
        statement = select(Review).where(Review.uid == review_uid)

        result = await session.exec(statement)

        return result.first()

    async def get_all_reviews(self, session: AsyncSession):
        statement = select(Review).order_by(desc(Review.created_at))

        result = await session.exec(statement)

        return result.all()

    async def delete_review_to_from_hotel(
        self, review_uid: str, user_email: str, session: AsyncSession
    ):
        user = await user_service.get_user_by_email(user_email, session)

        review = await self.get_review(review_uid, session)

        if not review:
            raise HTTPException(
                detail="Review not found",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if review.user_uid != user.uid:
            raise HTTPException(
                detail="Cannot delete this review",
                status_code=status.HTTP_403_FORBIDDEN,
            )

        # if not review or (review.user != user):
        #     raise HTTPException(
        #         detail="Cannot delete this review",
        #         status_code=status.HTTP_403_FORBIDDEN,
        #     )

        await session.delete(review)
        await session.commit()
    # async def delete_review_to_from_hotel(
    #         self, review_uid: str, user_email: str, session: AsyncSession
    # ):
    #     try:
    #         user = await user_service.get_user_by_email(user_email, session)
    #         review = await self.get_review(review_uid, session)
    #
    #         if not review or (review.user != user):
    #             raise HTTPException(
    #                 detail="You do not have permission to delete this review.",
    #                 status_code=status.HTTP_403_FORBIDDEN,
    #             )
    #
    #         await session.delete(review)
    #         await session.commit()
    #     except IntegrityError as e:
    #         await session.rollback()
    #         logger.exception(
    #             f"Database integrity error (review deletion): {e}, review_uid={review_uid}, user_email={user_email}")
    #         raise HTTPException(status_code=409, detail="Cannot delete this review. It may be in use.") from e
    #     except SQLAlchemyError as e:
    #         await session.rollback()
    #         logger.exception(
    #             f"SQLAlchemy error (review deletion): {e}, review_uid={review_uid}, user_email={user_email}")
    #         raise HTTPException(status_code=500, detail="An unexpected database error occurred.") from e
    #     except HTTPException as e:
    #         raise e
    #     except Exception as e:
    #         logger.exception(
    #             f"Unexpected error (review deletion): {e}, review_uid={review_uid}, user_email={user_email}")
    #         raise HTTPException(status_code=500, detail="Internal server error. Please contact support.") from e

