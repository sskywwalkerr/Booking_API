from sqlalchemy import select

from api.db.data import async_session_maker


class BaseDAO:
    """Класс для работы с объектами БД"""

    model = None

    @classmethod
    async def get_all_objects(cls, **kwargs):
        """Возвращает все объекты модели."""
        async with (async_session_maker() as session):
            query = (select(cls.model.__table__.columns).filter_by(**kwargs)
                     ).order_by(cls.model.uid)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def get_object(cls, **kwargs):
        """Возвращает объект модели."""
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**kwargs)
            result = await session.execute(query)
            return result.mappings().one_or_none()
