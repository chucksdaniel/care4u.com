"""Response schemas."""
from typing import Optional, Dict, Any, List
from uuid import UUID
from pydantic import BaseModel


class FieldResponse(BaseModel):
    """Schema for field response."""
    id: UUID
    name: str
    label: str
    field_type: str
    required: bool
    options: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


class WorkflowResponse(BaseModel):
    """Schema for workflow response."""
    id: UUID
    name: str
    description: Optional[str]
    steps: List[Dict[str, Any]]
    active: bool

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str
    detail: Optional[str] = None