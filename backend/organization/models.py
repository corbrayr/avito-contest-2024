import enum
import uuid
from datetime import datetime
from sqlalchemy import ForeignKey, Integer, String, DateTime, func, Text, Enum, text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base
from backend.enums.models import OrganizationType, organization_type

class Organization(Base):
    __tablename__ = "organization"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    type: Mapped[OrganizationType] = mapped_column(organization_type)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

class OrganizationResponsible(Base):
    __tablename__ = "organization_responsible"
    
    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, nullable=False, server_default=func.uuid_generate_v4())
    organization_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("organization.id", ondelete="CASCADE"))
    user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("employee.id", ondelete="CASCADE"))
    
    # organization = relationship("Organization", back_populates="organization_responsible")
    # employee = relationship("Employee", back_populates="organization_responsible")
