"""Authentication routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core import get_current_user, hash_password, verify_access_token, verify_password
from app.schemas import UserCreate, UserLogin, UserResponse, UserCreateResponse
from app.models import User
from app.core import get_db, create_access_token
# from app.domain.services import RequestService

router = APIRouter()

@router.post("/register", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
def register_user(new_user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""

    if db.query(User).filter(User.email == new_user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    new_user.password = hash_password(new_user.password)

    user = User(**new_user.dict())  # Unpacking the dictionary
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
    """Run migrations in 'online' mode."""


@router.post("/login", status_code=status.HTTP_200_OK)
def login(credentials: UserLogin, db: Session =  Depends(get_db)):
   
   user = db.query(User).filter(User.email == credentials.email).first()
   if not user:
      raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
   # Verify that the passwords are the same
   if not verify_password(credentials.password, user.password):
      raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
   access_token = create_access_token(data={"user_id": str(user.id)})
   return {"access_token": access_token, "token_type": "bearer"} 

@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_current_authenticated_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/protected", status_code=status.HTTP_200_OK)
def protected_route(token: str = Depends(verify_access_token)):
    return {"message": "You have access to this protected route."}

