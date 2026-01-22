"""Request routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, selectinload

from app.core import get_current_user, get_db
from app.schemas.request import RequestCreate, RequestResponse, CreateCareRequest, CareRequestOut
from app.models import User, SubjectProfile, Request
from app.enum import UserRole
# from app.domain.services import RequestService

router = APIRouter()


@router.post("/", response_model=RequestResponse, status_code=status.HTTP_201_CREATED)
async def create_request(
    request_data: RequestCreate, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed! Only client is allowed to create a request",
        )
    """Check if the subject exist"""
    subject = db.query(SubjectProfile).filter(SubjectProfile.id == request_data.subject_id).first()
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No profile found for the patient",
        )
    """ Check if the subject belong to the user """
    if subject.created_by_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorize to perform this action",
        )
    """Create a new request."""
    request = Request(
        subject_id=subject.id,
        owner_id=current_user.id,
        care_type=request_data.care_type,
        category=request_data.category,
        duration=request_data.duration,
        description=request_data.description
    )
    db.add(request)
    db.commit()
    db.refresh(request) 

    return request


# """ Create care request transaction-based """
# @router.post('/care-requests', response_model=CareRequestOut, status_code=status.HTTP_201_CREATED)
# def create_care_request(
#     care_request: CreateCareRequest, db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     # ONLY normal users can create care requests
#     if current_user.role != "user":
#         raise HTTPException(status_code=403, detail="Not allowed")
#     try:
#         subject = SubjectProfile(
#             created_by_id= get_current_user.id,
#             full_name=care_request.subject.full_name,
#             age=care_request.subject.age,
#             medical_history= care_request.subject.medical_history,
#             medications=care_request.subject.medications,
#             allergies=care_request.subject.allergies,
#             eating_schedule_enabled=care_request.subject.eating_schedule_enabled,
#             eating_schedule_details=care_request.subject.eating_schedule_details
#         )
#         db.add(subject)
#         db.flush()  # important to get subject.id

#         request = Request(
#             subject_id=subject.id,
#             owner_id=current_user.id,
#             care_type=care_request.request.care_type,
#             category=care_request.request.category,
#             duration=care_request.request.duration,
#             description=care_request.request.description
#         )

#     except Exception as e:
#         db.rollback()
#         raise HTTPException(500, str(e))

#     return {subject, request}

@router.get("/{request_id}", response_model=RequestResponse)
async def get_request(
    request_id: str, db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # request = db.query(Request).filter(Request.id == request_id).first()
    request = (
    db.query(Request)
    .options(
        selectinload(Request.owner),
        selectinload(Request.subject)
    )
    .filter(Request.id == request_id)
    .first()
)
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found"
        )
    return request


@router.get("/", response_model=list[RequestResponse])
async def list_requests(
    current_user: dict = Depends(get_current_user),
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db),
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed!",
        )
    """List all requests."""
    requests = (
    db.query(Request)
    .options(
        selectinload(Request.owner),
        selectinload(Request.subject)
    ))

    return requests
