from typing import Optional, Union
import uuid
from fastapi import APIRouter, Path, Query
from backend.employee.dao import EmployeeDAO
from backend.tenders.dao import TenderDAO, TenderHistoryDAO
from backend.tenders.models import ServiceType, StatusType
from backend.tenders.permission import check_user_permission
from backend.tenders.schemas import TenderCreate, TenderGet, TenderPatch
from backend.exceptions import TenderNotFound, TenderVersionNotFound, UserNotFound, PermissionDenied

router = APIRouter(
    prefix="/tenders",
    tags=["Tenders"]
)
@router.get("/")
async def get_tenders(limit: int = 5, offset: int = 0, service_type: list[ServiceType] = Query(None)) -> list[TenderGet]:
    tenders = await TenderDAO.get_tenders_by_service_type(limit, offset, service_type)
    return tenders

@router.post("/new")
async def create_tender(tender: TenderCreate):
    user = await EmployeeDAO.find_by_username(tender.creatorUsername)
    
    if not user:
        raise UserNotFound
    
    tender_info = await TenderDAO.check_new_tender(
        tender.organizationId,
        tender.creatorUsername
    )

    if not tender_info:
        raise PermissionDenied

    new_tender = await TenderDAO.new_tender(
            tender.name,
            tender.description,
            tender.serviceType,
            tender.organizationId,
            tender.creatorUsername
        )
    return new_tender

@router.get("/my", responses={
    401: {
        "description": "Пользователь не существует или некорректен.",
        "content": {"application/json": {"example": {"detail": "Пользователь не существует или некорректен."}}}
    }
})
async def get_my_tenders(username: str, limit: int = 5, offset: int = 0) -> list[TenderGet]:
    user = await EmployeeDAO.find_by_username(username=username)

    if not user:
        raise UserNotFound
    
    tenders = await TenderDAO.get_tenders_by_username(
        limit=limit,
        offset=offset,
        username=username
    )
    
    return tenders

@router.get("/{tenderId}/status", responses={
    401: {
            "description": "Пользователь не существует или некорректен.",
            "content": {"application/json": {"example": {"detail": "Пользователь не существует или некорректен."}}}
        }
})
async def get_tender_status(tenderId: uuid.UUID, username: str) -> StatusType:
    user = await EmployeeDAO.find_by_username(username=username)

    if not user:
        raise UserNotFound

    tender = await TenderDAO.find_by_id(model_id=tenderId)

    if not tender:
        raise TenderNotFound

    if tender["status"] == StatusType.CREATED or tender["status"] == StatusType.CLOSED:
        user_permission = await check_user_permission(user["id"], tender["organizationId"])

        if not user_permission:
            raise PermissionDenied

    return tender.status

@router.put("/{tenderId}/status", responses={
    401: {
            "description": "Пользователь не существует или некорректен.",
            "content": {"application/json": {"example": {"detail": "Пользователь не существует или некорректен."}}}
        }
})
async def change_tender_status(tenderId: uuid.UUID, status: StatusType, username: str) -> TenderGet:
    user = await EmployeeDAO.find_by_username(username=username)

    if not user:
        raise UserNotFound

    tender = await TenderDAO.find_by_id(model_id=tenderId)

    if not tender:
        raise TenderNotFound

    user_permission = await check_user_permission(user["id"], tender["organizationId"])

    if not user_permission:
        raise PermissionDenied

    await TenderDAO.change_tender_status(tender_id=tenderId, status=status)

    tender = await TenderDAO.find_by_id(model_id=tenderId)
    
    return tender

@router.patch("/{tenderId}/edit", responses={
    401: {
            "description": "Пользователь не существует или некорректен.",
            "content": {"application/json": {"example": {"detail": "Пользователь не существует или некорректен."}}}
        }
})
async def edit_tender(tenderId: uuid.UUID, username: str, tender_patch_info: TenderPatch):
    user = await EmployeeDAO.find_by_username(username=username)

    if not user:
        raise UserNotFound

    tender = await TenderDAO.find_by_id(model_id=tenderId)

    if not tender:
        raise TenderNotFound

    user_permission = await check_user_permission(user["id"], tender["organizationId"])

    if not user_permission:
        raise PermissionDenied

    await TenderHistoryDAO.insert(
        tender_id=tender["id"],
        name=tender["name"],
        description=tender["description"],
        serviceType=tender["serviceType"],
        version=tender["version"]
    )

    tender = await TenderDAO.change_tender_params(
        tenderId=tenderId,
        tender_patch_info=tender_patch_info
    )

    return tender

@router.put("/{tenderId}/rollback/{version}", responses={
    401: {
            "description": "Пользователь не существует или некорректен.",
            "content": {"application/json": {"example": {"detail": "Пользователь не существует или некорректен."}}}
        }
})
async def rollback_tender(tenderId: uuid.UUID, username: str, version: int = Path(ge=1)):
    user = await EmployeeDAO.find_by_username(username=username)

    if not user:
        raise UserNotFound

    tender = await TenderDAO.find_by_id(model_id=tenderId)

    if not tender:
        raise TenderNotFound
    
    user_permission = await check_user_permission(user["id"], tender["organizationId"])

    if not user_permission:
        raise PermissionDenied
    
    tender_history = await TenderHistoryDAO.find_one_or_none(
        tender_id=tenderId,
        version=version
    )
    
    if not tender_history:
        raise TenderVersionNotFound
    
    await TenderHistoryDAO.insert(
        tender_id=tender["id"],
        name=tender["name"],
        description=tender["description"],
        serviceType=tender["serviceType"],
        version=tender["version"]
    )

    tender_patch_info = TenderPatch(**{
        "name": tender_history["name"],
        "description": tender_history["description"],
        "serviceType": tender_history["serviceType"],
    })

    tender = await TenderDAO.change_tender_params(
        tenderId=tenderId,
        tender_patch_info=tender_patch_info
    )

    return tender