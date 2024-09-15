import enum

from sqlalchemy import Enum

class OrganizationType(enum.Enum):
    IE = "IE"
    LLC = "LLC"
    JSC = "JSC"

organization_type = Enum(OrganizationType, name="organization_type", create_type=True)

class ServiceType(enum.Enum):
    CONSTRUCTION = "Construction"
    DELIVERY = "Delivery"
    MANUFACTURE = "Manufacture"

service_type = Enum(ServiceType, name="service_type", create_type=True)

class StatusType(enum.Enum):
    CREATED = "Created"
    PUBLISHED = "Published"
    CLOSED = "Closed"

status_type = Enum(StatusType, name="status_type", create_type=True)

class AuthorType(enum.Enum):
    ORGANIZATION = "Organization"
    USER = "User"
    
author_type = Enum(AuthorType, name="author_type", create_type=True)

class DecisionType(enum.Enum):
    REVIEW = "Review"
    APPROVED = "Approved"
    REJECTED = "Rejected"

decision_type = Enum(DecisionType, name="decision_type", create_type=True)