from sqlalchemy import select, insert

from backend.database import async_session_maker

class BaseDAO:
    model = None
    
    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=model_id)
            result = await session.execute(query)
            return result.mappings().one_or_none()
    
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()
        
    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def find_all_with_pagination(cls, limit: int, offset: int, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by).order_by(cls.model.id).limit(limit=limit).offset(offset=offset)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def insert(cls, **values):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**values)
            await session.execute(query)
            await session.commit()