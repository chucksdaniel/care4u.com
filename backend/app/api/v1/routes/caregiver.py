"""Authentication routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core import get_current_user, hash_password, verify_access_token, verify_password
from app.schemas import UserCreate, UserLogin, UserResponse, UserCreateResponse, CareGiverProfileCreate ,CareGiverProfileResponse
from app.models import User, CareGiverProfile
from app.enum import UserRole
from app.core import get_db, create_access_token
# from app.domain.services import RequestService

router = APIRouter()

""" Register a new caregiver user. """
@router.post("/register", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
def register_user(new_user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""

    if db.query(User).filter(User.email == new_user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    new_user.password = hash_password(new_user.password)
    new_user.role = UserRole.CARE_GIVER
    user = User(**new_user.dict())  # Unpacking the dictionary
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
    """Run migrations in 'online' mode."""

""" Create caregiver profile for an existing user """
@router.post("/profiles", response_model=CareGiverProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_caregiver_profile(
    profile_data: CareGiverProfileCreate, db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
  ):
    """Create a caregiver profile for an existing user."""
    if current_user.role != UserRole.CARE_GIVER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only caregivers can create a caregiver profile",
        )
    exiting_profile = db.query(CareGiverProfile).filter(CareGiverProfile.user_id == current_user.id).first()
    
    if exiting_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Caregiver profile already exists for this user",
        )
    
    caregiver_profile = CareGiverProfile(**profile_data.dict(), user_id=current_user.id)
    db.add(caregiver_profile)
    db.commit()
    db.refresh(caregiver_profile)
    return caregiver_profile

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
   access_token = create_access_token(data={"user_id": user.id})
   return {"access_token": access_token, "token_type": "bearer"} 

""" Update current authenticated user """
@router.put("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_current_authenticated_user(
    user_update: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = db.query(User).filter(User.id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    for var, value in vars(user_update).items():
        setattr(profile, var, value) if value else None
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_current_authenticated_user(current_user: User = Depends(get_current_user)):
    return current_user

""" Get caregiver profile of the current authenticated user """
@router.get("/me/profiles", response_model=CareGiverProfileResponse, status_code=status.HTTP_200_OK)
def get_current_user_caregiver_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(CareGiverProfile).filter(CareGiverProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Caregiver profile not found"
        )
    return profile

@router.get("/protected", status_code=status.HTTP_200_OK)
def protected_route(token: str = Depends(verify_access_token)):
    return {"message": "You have access to this protected route."}

