import uuid
from backend.organization.dao import OrganizationResponsibleDAO
from backend.tenders.models import StatusType


async def check_user_permission(user_id: uuid.UUID, organization_id: uuid.UUID) -> bool:
    responsible = await OrganizationResponsibleDAO.find_one_or_none(organization_id=organization_id, user_id=user_id)

    if not responsible:
        return False

    return True