from datetime import datetime
import uuid
from pydantic import BaseModel

from backend.enums.models import AuthorType, DecisionType, ServiceType, StatusType


class BidSchema(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    status: StatusType
    decision: DecisionType
    tenderId: uuid.UUID
    authorType: AuthorType
    authorId: uuid.UUID
    version: int
    createdAt: datetime
    updatedAt: datetime

class BidCreate(BaseModel):
    name: str
    description: str
    tenderId: uuid.UUID
    authorType: AuthorType
    authorId: uuid.UUID

class BidGet(BaseModel):
    id: uuid.UUID
    name: str
    status: StatusType
    authorType: AuthorType
    authorId: uuid.UUID
    version: int
    createdAt: datetime