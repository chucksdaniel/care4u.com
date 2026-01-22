from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core import get_current_user, hash_password, verify_access_token, verify_password
from app.schemas import UserUpdate, UserResponse, UserProfileCreate, UserProfileResponse, SubjectCreate, SubjectResponse
from app.models import User, SubjectProfile, UserProfile
from app.core import get_db
from app.enum import UserRole

router = APIRouter()

""" Edit user profile. """
@router.put("/profiles", response_model=UserProfileResponse, status_code=status.HTTP_200_OK)
def edit_user_profile(
    user: UserUpdate, db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    db_user = db.query(User).filter(User.id == current_user.id).first()
    if not db_user:
        raise HTTPException(status_code=409, detail="You are not authorized to perform this action")

    hashed_password = hash_password(user.password)
    db_user.email = user.email
    db_user.hashed_password = hashed_password
    db_user.full_name = user.full_name
    db_user.age = user.age
    db_user.medical_history = user.medical_history

    db.commit()
    db.refresh(db_user)

    return db_user

""" Create user profile. """
@router.post("/profiles", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
def create_user_profile(
    user: UserProfileCreate, db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only users can create a user profile",
        )
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    if profile:
        raise HTTPException(status_code=400, detail="Profile already exists")

    new_profile = UserProfile(
        user_id=current_user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        address=user.address,
        state=user.state,
        country=user.country,
        phone=user.phone,
        avatar_url=user.avatar_url
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

""" Endpoint for users to create profiles for subjects. """
@router.post("/subjects", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
def create_subject_profile(
    subject: SubjectCreate, db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only users can create a user profile",
        )
    """ Check if subject profile already exists for the user. What will be the unique identifier? Todo: phone number"""
    # db_patient = db.query(PatientProfile).filter(PatientProfile.created_by_id == current_user.id).first()
    # if db_patient:
    #     raise HTTPException(status_code=400, detail="Patient profile already exists")
    # patient = PatientCreate(**patient.dict(), created_by_id=current_user.id)

    patient = SubjectProfile(
        created_by_id=current_user.id,
        full_name=subject.full_name,
        age=subject.age,
        medical_history=subject.medical_history,
        medications=subject.medications,
        allergies=subject.allergies,
        eating_schedule_enabled=subject.eating_schedule_enabled,
        eating_schedule_details=subject.eating_schedule_details
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

""" Get profiles created by the user. """
@router.get("/subjects", response_model=List[SubjectCreate], status_code=status.HTTP_200_OK)
def get_subject_profiles(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    subjects = db.query(SubjectProfile).filter(SubjectProfile.created_by_id == current_user.id).all()
    return subjects

""" Delete a subject profile. """
@router.delete("/subjects/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subject_profile(
    subject_id: str, db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    subject = db.query(SubjectProfile).filter(
        SubjectProfile.id == subject_id,
        SubjectProfile.created_by_id == current_user.id
    ).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject profile not found")
    db.delete(subject)
    db.commit()
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})

