from sqlalchemy import Column, Enum, Float, Integer, String, Boolean, TIMESTAMP, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import text
from app.core.db_base import Base
import uuid

""" Caregiver profile model for storing caregiver-specific information """
class CareGiverProfile(Base):
    __tablename__ = "care_giver_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(ForeignKey("users.id"), unique=True, nullable=False)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)

    license_number = Column(String, nullable=False)
    specialization = Column(String)
    years_of_experience = Column(Integer)

    certification_url = Column(String, nullable=True)
    certification_verified = Column(Boolean, default=False)

    rating = Column(Float, default=0.0)
    empathy_score = Column(Float, default=0.0)

    created_at = Column(
        TIMESTAMP(timezone=True), 
        nullable=False, server_default=text("now()")
    )
    user = relationship("User", back_populates="care_giver_profile")


""" User profile model for additional user information """
class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    address = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), 
        nullable=False, server_default=text('now()')
    )
    user = relationship("User", back_populates="profile")


""" Subject model representing subjects in the system """
class SubjectProfile(Base):
    __tablename__ = "subject_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    created_by_id = Column(ForeignKey("users.id"), nullable=False)  # Normal user
    assigned_care_giver_id = Column(ForeignKey("users.id"), nullable=True)

    full_name = Column(String, nullable=False)
    age = Column(Integer)
    medical_history = Column(Text)
    medications = Column(Text)
    allergies = Column(Text, nullable=True)
    eating_schedule_enabled = Column(Boolean, default=False)
    eating_schedule_details = Column(Text)
    created_at = Column(
        TIMESTAMP(timezone=True), 
        nullable=False, server_default=text('now()')
    )
    assigned_care_giver = relationship("User", foreign_keys=[assigned_care_giver_id])

    created_by = relationship(
        "User",
        back_populates="subject_profiles",
        foreign_keys=[created_by_id]
    )

    # created_by = relationship(
    #     "User", 
    #     backref="subject_profiles", 
    #     foreign_keys=[created_by_id]
    # )

    requests = relationship(
        "Request",
        back_populates="subject",
        cascade="all, delete-orphan"
    )
