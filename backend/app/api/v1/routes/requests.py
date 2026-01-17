"""Request routes."""
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.api.deps import get_current_user
from app.schemas.request import RequestCreate, RequestResponse
from app.domain.services import RequestService

router = APIRouter()


@router.post("/", response_model=RequestResponse, status_code=status.HTTP_201_CREATED)
async def create_request(
    request_data: RequestCreate,
    current_user: dict = Depends(get_current_user),
):
    """Create a new request."""
    # TODO: Implement request creation
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Request created successfully"},
    )


@router.get("/{request_id}", response_model=RequestResponse)
async def get_request(
    request_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Get a request by ID."""
    # TODO: Implement request retrieval
    return {"id": request_id, "status": "pending"}


@router.get("/", response_model=list[RequestResponse])
async def list_requests(
    current_user: dict = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
):
    """List all requests."""
    # TODO: Implement request listing
    return []
