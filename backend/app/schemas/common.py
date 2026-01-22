"""Common schemas."""
from typing import Optional, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response schema."""
    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int


class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str
    version: Optional[str] = None
    timestamp: Optional[str] = None