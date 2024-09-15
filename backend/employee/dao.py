from sqlalchemy import select
from backend.dao.base import BaseDAO
from backend.employee.models import Employee
from backend.database import async_session_maker


class EmployeeDAO(BaseDAO):
    model = Employee
    
    @classmethod
    async def find_by_username(cls, username: str):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(username=username)
            result = await session.execute(query)
            return result.mappings().one_or_none()
