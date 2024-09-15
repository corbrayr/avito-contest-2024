import enum
import uuid
from datetime import datetime
from sqlalchemy import ForeignKey, Integer, String, DateTime, func, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ENUM
from backend.database import Base
from backend.enums.models import AuthorType, DecisionType, StatusType, status_type

class Bid(Base):
    __tablename__ = "bid"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500))
    status: Mapped[StatusType] = mapped_column(type_=ENUM(StatusType, create_type=False), nullable=False)
    decision: Mapped[DecisionType] = mapped_column(type_=ENUM(DecisionType, create_type=False), nullable=False)
    tenderId: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("tender.id"), nullable=False)
    authorType: Mapped[AuthorType] = mapped_column(type_=ENUM(AuthorType, create_type=False), nullable=False)
    authorId: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("employee.id"), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    updatedAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

# class BidFeedback(Base):
#     __tablename__ = "bid_feedback"
    
#     id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     bidId: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("bid.id"), nullable=False)
#     bidFeedback: Mapped[uuid.UUID] = mapped_column(Text)
#     username: Mapped[str] = mapped_column(String(100), nullable=False)
#     createdAt: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())