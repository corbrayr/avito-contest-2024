from datetime import datetime
import uuid
from typing import Literal, Optional
from pydantic import BaseModel

from backend.tenders.models import ServiceType, StatusType

class TenderSchema(BaseModel):
    id: uuid.UUID
    name: str
    status: StatusType
    version: int
    description: str
    serviceType: ServiceType
    organizationId: uuid.UUID
    creatorUsername: str
    createdAt: datetime
    updatedAt: datetime
    
class TenderCreate(BaseModel):
    name: str
    description: str
    serviceType: ServiceType
    organizationId: uuid.UUID
    creatorUsername: str

class TenderGet(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    status: StatusType
    serviceType: ServiceType
    version: int
    createdAt: datetime

class TenderPatch(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    serviceType: Optional[ServiceType] = None
