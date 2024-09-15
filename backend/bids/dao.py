

import uuid

from sqlalchemy import insert, select
from backend.bids.models import Bid
from backend.dao.base import BaseDAO
from backend.employee.models import Employee
from backend.enums.models import AuthorType, DecisionType, StatusType
from backend.database import async_session_maker


class BidDAO(BaseDAO):
    model = Bid
    
    @classmethod
    async def new_bid(
        cls,
        name: str,
        description: str,
        tenderId: uuid.UUID,
        authorType: AuthorType,
        authorId: uuid.UUID
    ):
        async with async_session_maker() as session:
            add_new_bid = (
                insert(Bid).values(
                    name=name,
                    description=description,
                    tenderId=tenderId,
                    authorType=authorType,
                    authorId=authorId,
                    status=StatusType.CREATED,
                    decision=DecisionType.REVIEW
                )
            ).returning(
                Bid.id,
                Bid.name,
                Bid.status,
                Bid.authorType,
                Bid.authorId,
                Bid.version,
                Bid.createdAt,
            )
            
            new_bid = await session.execute(add_new_bid)
            
            await session.commit()
            
            return new_bid.mappings().one()
    
    @classmethod
    async def get_bids_by_username(
        cls,
        limit: int,
        offset: int,
        username: str
    ):
        async with async_session_maker() as session:
            get_bids = select(
                    Bid.id,
                    Bid.name,
                    Bid.status,
                    Bid.authorType,
                    Bid.authorId,
                    Bid.version,
                    Bid.createdAt
                ).join(
                    Employee, Employee.id == Bid.authorId
                ).where(
                    Employee.username == username
                ).order_by(
                    Bid.name
                ).offset(offset=offset).limit(limit=limit)

            bids = await session.execute(get_bids)

            return bids.mappings().all()

    @classmethod
    async def get_bids_by_tender_id(
        cls,
        limit: int,
        offset: int,
        tenderId: uuid.UUID
    ):
        async with async_session_maker() as session:
            get_bids = select(
                Bid.id,
                Bid.name,
                Bid.status,
                Bid.authorType,
                Bid.authorId,
                Bid.version,
                Bid.createdAt
            ).where(
                Bid.tenderId == tenderId
            ).order_by(
                Bid.name
            ).offset(offset=offset).limit(limit=limit)

            bids = await session.execute(get_bids)

            return bids.mappings().all()