from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from typing import Annotated, Optional

from app.enum import UserRole

class UserBase(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.USER

class ProfileBase(BaseModel):
    first_name: str
    last_name: str
    address: str
    state: str
    country: str
    phone: Optional[str] = None
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserProfileCreate(ProfileBase):
    pass

class CareGiverProfileCreate(ProfileBase):
    license_number: str
    specialization: Optional[str] = None
    years_of_experience: Optional[int] = None
    certification_url: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole
    is_active: bool
    is_verified: Optional[bool] = False
    created_at: datetime

class UserProfileResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    address: str
    state: str
    country: str
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
class CareGiverProfileResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    address: str
    state: str
    country: str
    license_number: str
    specialization: Optional[str] = None
    years_of_experience: Optional[int] = None
    certification_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class UserCreateResponse(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Subject(BaseModel):
    id: UUID
    full_name: str
    age: int
    medical_history: str
    allergies: Optional[str] = None
    eating_schedule_enabled: bool = False
    eating_schedule_details: Optional[str] = None
    created_at: datetime
    created_by: UUID

    @field_validator("eating_schedule_details")
    @classmethod
    def validate_details(cls, v, info):
        enabled = info.data.get("eating_schedule_enabled")
        if enabled and not v:
            raise ValueError(
                "eating_schedule_details is required when eating_schedule_enabled is True"
            )
        return v

class SubjectCreate(BaseModel):
    full_name: str
    age: int
    medical_history: str
    medications: Optional[str] = None
    allergies: Optional[str] = None
    eating_schedule_enabled: bool = False
    eating_schedule_details: Optional[str] = None

    @field_validator("eating_schedule_details")
    @classmethod
    def validate_details(cls, v, info):
        enabled = info.data.get("eating_schedule_enabled")
        if enabled and not v:
            raise ValueError(
                "eating_schedule_details is required when eating_schedule_enabled is True"
            )
        return v
    
class SubjectResponse(BaseModel):
    id: UUID
    full_name: str
    age: int
    medical_history: str
    allergies: Optional[str] = None
    eating_schedule_enabled: bool = False
    eating_schedule_details: Optional[str] = None
    created_at: datetime
    created_by: UserBase

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[UUID] = None # Optional field to handle cases where token might not have id why did he use str before?

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]  # 1 = upvote, 0 = remove
    # dir : conint(le=1)  # 1 for upvote, 0 for remove vote