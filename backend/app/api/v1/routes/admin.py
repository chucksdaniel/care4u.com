from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core import get_current_user, get_current_admin_user, hash_password
from app.schemas import UserCreate, UserLogin, UserResponse, UserCreateResponse, SubjectCreate, CareGiverProfileResponse
from app.models import User, SubjectProfile
from app.core import get_db, create_access_token
from app.enum import UserRole

router = APIRouter()

""" Get users by admin. """
@router.get("/users", response_model=List[UserResponse])
def get_users_by_admin(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role == UserRole.SUPER_ADMIN:
        # superadmin sees everyone
        return db.query(User).all()

    # admin sees only users + caregivers
    return db.query(User).filter(
        User.role.in_([UserRole.USER, UserRole.CARE_GIVER])
    ).all()

""" Register a new admin user. """
@router.post("/register", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
def register_admin(new_admin: UserCreate, db: Session = Depends(get_db)):
    """Register a new admin user."""

    if db.query(User).filter(User.email == new_admin.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    new_admin.password = hash_password(new_admin.password)
    user_data = new_admin.dict(exclude={"role"})
    
    user = User(**user_data, role = UserRole.ADMIN)  # Unpacking the dictionary
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
    """Run migrations in 'online' mode."""

""" Activate a user by admin. """
# @router.put("/users/{user_id}/activate", status_code=status.HTTP_204_NO_CONTENT)
# def activate_user_by_admin(user_id: int, db: Session = Depends(get_db), 
#                          current_user: User = Depends(get_current_admin_user)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     user.is_active = True
#     db.commit()
#     return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})

""" Reset a user's password by admin. """
# @router.put("/users/{user_id}/reset-password", status_code=status.HTTP_204_NO_CONTENT)
# def reset_user_password_by_admin(user_id: int, db: Session = Depends(get_db), 
#                          current_user: User = Depends(get_current_admin_user)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     user.password = hash_password("default_password")
#     db.commit()
#     return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})



""" Deactivate a user by admin. """
@router.put("/users/{user_id}/deactivate", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_caregiver_by_admin(user_id: int, db: Session = Depends(get_db), 
                         current_user: User = Depends(get_current_admin_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    db.commit()
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})

""" Delete a user by admin. """
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_admin(user_id: int, db: Session = Depends(get_db), 
                         current_user: User = Depends(get_current_admin_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})


""" Admin get all patient profiles. """
@router.get("/patients", response_model=List[SubjectCreate], status_code=status.HTTP_200_OK)
def get_all_patient_profiles(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_admin_user)
):
    patients = db.query(SubjectProfile).all()
    return patients

