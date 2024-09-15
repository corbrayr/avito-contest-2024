import uuid
from fastapi import APIRouter

from backend.bids.dao import BidDAO
from backend.bids.schemas import BidCreate, BidGet
from backend.employee.dao import EmployeeDAO
from backend.enums.models import StatusType
from backend.exceptions import BidNotFound, PermissionDenied, TenderNotFound, UserNotFound
from backend.tenders.dao import TenderDAO
from backend.tenders.permission import check_user_permission


router = APIRouter(
    prefix="/bids",
    tags=["Bids"]
)

@router.post("/new")
async def create_bid(bid: BidCreate):
    user = await EmployeeDAO.find_by_id(bid.authorId)

    if not user:
        raise UserNotFound

    tender = await TenderDAO.find_by_id(bid.tenderId)

    if not tender:
        raise TenderNotFound

    new_bid = await BidDAO.new_bid(
            bid.name,
            bid.description,
            bid.tenderId,
            bid.authorType,
            bid.authorId
        )
    return new_bid

@router.get("/my", responses={
    401: {
        "description": "Пользователь не существует или некорректен.",
        "content": {"application/json": {"example": {"detail": "Пользователь не существует или некорректен."}}}
    }
})
async def get_my_tenders(username: str, limit: int = 5, offset: int = 0) -> list[BidGet]:
    user = await EmployeeDAO.find_by_username(username=username)

    if not user:
        raise UserNotFound
    
    bids = await BidDAO.get_bids_by_username(
        limit=limit,
        offset=offset,
        username=username
    )
    
    return bids

@router.get("/{tenderId}/list")
async def get_bids(tenderId: uuid.UUID, username: str, limit: int = 5, offset: int = 0) -> list[BidGet]:
    user = await EmployeeDAO.find_by_username(username=username)

    if not user:
        raise UserNotFound

    tender = await TenderDAO.find_by_id(tenderId)

    if not tender:
        raise TenderNotFound

    user_permission = await check_user_permission(user["id"], tender["organizationId"])

    if not user_permission:
        raise PermissionDenied

    bids = await BidDAO.get_bids_by_tender_id(limit, offset, tenderId)

    if not bids:
        raise BidNotFound

    return bids

@router.get("/{bidId}/status", responses={
    401: {
            "description": "Пользователь не существует или некорректен.",
            "content": {"application/json": {"example": {"detail": "Пользователь не существует или некорректен."}}}
        }
})
async def get_bid_status(bidId: uuid.UUID, username: str) -> StatusType:
    user = await EmployeeDAO.find_by_username(username=username)

    if not user:
        raise UserNotFound
    
    bid = await BidDAO.find_by_id(model_id=bidId)
    
    if not bid:
        raise BidNotFound

    tender = await TenderDAO.find_by_id(model_id=bid.tenderId)

    user_permission = await check_user_permission(user["id"], tender["organizationId"])

    if not user_permission:
        raise PermissionDenied

    return bid.status