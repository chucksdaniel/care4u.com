from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Annotated, Optional

class UserBase(BaseModel):
    first_name: str
    last_name: str
    address: str
    state: str
    country: str
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class RequestBase(BaseModel):
    title: str
    description: str
    is_handled: bool = True
    # rating: Optional[int] = None 

class RequestCreate(RequestBase):
    pass


class Request(RequestBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    # class Config:
    #     orm_mode = True # Enable ORM mode to work with SQLAlchemy models with Pydantic v1
    model_config = ConfigDict(from_attributes=True) # Enable ORM mode to work with SQLAlchemy models with Pydantic v2

class RequestOut(BaseModel):
    request: Request
    votes: int

    model_config = ConfigDict(from_attributes=True)
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None # Optional field to handle cases where token might not have id why did he use str before?

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]  # 1 = upvote, 0 = remove
    # dir : conint(le=1)  # 1 for upvote, 0 for remove vote