from backend.dao.base import BaseDAO
from backend.organization.models import Organization, OrganizationResponsible


class OrganizationDAO(BaseDAO):
    model = Organization
    
class OrganizationResponsibleDAO(BaseDAO):
    model = OrganizationResponsible