from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from app.schemas.user import UserResponse


class RequestBase(BaseModel):
  """ Schema for Base request. """

class RequestCreate(RequestBase):
  """ Schema for Creating a request """

class RequestResponse(BaseModel):
  """ Schema for request response """

class RequestBase(BaseModel):
    title: str
    description: str
    is_handled: bool = True
    # rating: Optional[int] = None 

class RequestCreate(RequestBase):
    pass


class Request(RequestBase):
    id: UUID
    created_at: datetime
    owner_id: UUID
    owner: UserResponse

    # class Config:
    #     orm_mode = True # Enable ORM mode to work with SQLAlchemy models with Pydantic v1
    model_config = ConfigDict(from_attributes=True) # Enable ORM mode to work with SQLAlchemy models with Pydantic v2

class RequestOut(BaseModel):
    request: Request
    votes: int

    model_config = ConfigDict(from_attributes=True)