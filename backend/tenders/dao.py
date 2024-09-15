

from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import and_, insert, select, join, update
from backend.dao.base import BaseDAO
from backend.tenders.models import Tender, StatusType, ServiceType, TenderHistory
from backend.employee.models import Employee
from backend.organization.models import Organization, OrganizationResponsible
from backend.database import async_session_maker
from backend.tenders.schemas import TenderGet, TenderPatch, TenderSchema

class TenderDAO(BaseDAO):
    model = Tender

    @classmethod
    async def get_tenders_by_service_type(
        cls,
        limit: int,
        offset: int,
        service_type: list[ServiceType]
    ):
        async with async_session_maker() as session:
            get_tenders = select(
                    Tender.id,
                    Tender.name,
                    Tender.description,
                    Tender.status,
                    Tender.serviceType,
                    Tender.version,
                    Tender.createdAt
                )
            if service_type:
                get_tenders = get_tenders.where(Tender.serviceType.in_(service_type))
            
            get_tenders = get_tenders.order_by(Tender.name).offset(offset).limit(limit)
        
            tenders = await session.execute(get_tenders)
            
            return tenders.mappings().all()
    
    @classmethod
    async def get_tenders_by_username(
        cls,
        limit: int,
        offset: int,
        username: str
    ):
        async with async_session_maker() as session:
            get_tenders = select(
                    Tender.id,
                    Tender.name,
                    Tender.description,
                    Tender.status,
                    Tender.serviceType,
                    Tender.version,
                    Tender.createdAt
                ).where(
                    Tender.creatorUsername == username
                ).order_by(
                    Tender.name
                ).offset(offset=offset).limit(limit=limit)
        
            tenders = await session.execute(get_tenders)
            
            return tenders.mappings().all()

    @classmethod
    async def check_new_tender(
        cls,
        organizationId: uuid.UUID,
        creatorUsername: str
    ):
        async with async_session_maker() as session:
            get_responsible_info = (
                select(
                    OrganizationResponsible
                ).join(
                    Employee, Employee.id == OrganizationResponsible.user_id
                ).where(
                    and_(
                        Employee.username == creatorUsername,
                        OrganizationResponsible.organization_id == organizationId
                    )
                )
            )

            responsible_info = await session.execute(get_responsible_info)
            return responsible_info.mappings().one_or_none()

    @classmethod
    async def new_tender(
        cls,
        name: str,
        description: str,
        serviceType: ServiceType,
        organizationId: uuid.UUID,
        creatorUsername: str
    ):
        async with async_session_maker() as session:
            add_new_tender = (
                insert(Tender).values(
                    name=name,
                    description=description,
                    serviceType=serviceType,
                    organizationId=organizationId,
                    creatorUsername=creatorUsername,
                    status=StatusType.CREATED
                )
            ).returning(
                Tender.id,
                Tender.name,
                Tender.description,
                Tender.status,
                Tender.serviceType,
                Tender.version,
                Tender.createdAt
            )
            
            new_tender = await session.execute(add_new_tender)
            
            await session.commit()
            
            return new_tender.mappings().one()

    @classmethod
    async def change_tender_status(
        cls,
        tender_id: uuid.UUID,
        status: StatusType
    ):
        async with async_session_maker() as session:
            update_tender_status = update(Tender).where(Tender.id == tender_id).values(status=status)
            await session.execute(update_tender_status)
            await session.commit()


    @classmethod
    async def change_tender_params(
        cls,
        tenderId: uuid.UUID,
        tender_patch_info: TenderPatch
    ):
        async with async_session_maker() as session:
            update_tender = update(
                Tender
            ).where(
                Tender.id == tenderId
            ).values(
                version= (Tender.version + 1),
                **tender_patch_info.model_dump(exclude_none=True)
            ).returning(
                Tender.id,
                Tender.name,
                Tender.description,
                Tender.status,
                Tender.serviceType,
                Tender.version,
                Tender.createdAt
            )

            result_tender = await session.execute(update_tender)
            await session.commit()

        return result_tender.mappings().one()
    
class TenderHistoryDAO(BaseDAO):
    model = TenderHistory
