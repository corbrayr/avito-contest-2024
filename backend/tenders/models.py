import enum
import uuid
from datetime import datetime
from sqlalchemy import ForeignKey, Integer, String, DateTime, func, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ENUM
from backend.database import Base
from backend.enums.models import ServiceType, StatusType, status_type, service_type

class Tender(Base):
    __tablename__ = "tender"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[StatusType] = mapped_column(status_type, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    description: Mapped[str] = mapped_column(Text)
    serviceType: Mapped[ServiceType] = mapped_column(service_type, nullable=False)
    organizationId: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("organization.id"))
    creatorUsername: Mapped[str] = mapped_column(String, ForeignKey("employee.username"))
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updatedAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # organization = relationship("Organization", back_populates="tender")
    # employee = relationship("Employee", back_populates="tender")

class TenderHistory(Base):
    __tablename__ = "tender_history"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    tender_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    serviceType: Mapped[ServiceType] = mapped_column(type_=ENUM(ServiceType, create_type=False), nullable=False, default=ServiceType.CONSTRUCTION)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
