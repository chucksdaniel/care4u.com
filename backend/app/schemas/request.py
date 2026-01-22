from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from app.schemas.user import UserResponse, SubjectResponse, SubjectCreate
from app.enum import RequestType, RequestCategory, DurationType


class RequestBase(BaseModel):
    care_type: RequestType
    category: RequestCategory
    duration: DurationType
    description: str
    is_handled: bool = True
    # rating: Optional[int] = None 

""" Schema for Creating a request """
class RequestCreate(RequestBase):
    subject_id: UUID
    pass

""" Schema for request response """
class RequestResponse(BaseModel):
    id: UUID
    owner_id: UUID
    owner: UserResponse
    subject_id: UUID
    subject: SubjectResponse
    created_at: datetime

    # class Config:
    #     orm_mode = True # Enable ORM mode to work with SQLAlchemy models with Pydantic v1
    model_config = ConfigDict(from_attributes=True) # Enable ORM mode to work with SQLAlchemy models with Pydantic v2

class CreateCareRequest():
    subject: SubjectCreate
    request: RequestCreate

class SubjectOut(BaseModel):
    id: UUID
    full_name: str
    age: int
    medical_notes: str | None

    model_config = ConfigDict(from_attributes=True)


class RequestOut(BaseModel):
    id: UUID
    subject_id: UUID
    requester_id: UUID
    care_type: RequestType
    # service_type: ServiceType
    duration: DurationType
    description: str
    status: str

    model_config = ConfigDict(from_attributes=True)

class CareRequestOut(BaseModel):
    subject: SubjectOut
    request: RequestOut


# class CareRequestResponse():
#     SubjectCreate: SubjectCreate
#     RequestCreate: RequestCreate

class RequestOut(BaseModel):
    request: RequestResponse
    votes: int

    model_config = ConfigDict(from_attributes=True)