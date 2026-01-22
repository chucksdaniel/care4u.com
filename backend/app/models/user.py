from sqlalchemy import Column, Enum, Integer, String, Boolean, TIMESTAMP, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import text
from app.core.db_base import Base
import uuid

from app.enum import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False,)
    role = Column(Enum(UserRole), default=UserRole.USER) # Role column to define user roles I:Many relationship
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(
        TIMESTAMP(timezone=True), 
        nullable=False, server_default=text('now()')
    )

    """ Relationships with profile models """
    profile = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    care_giver_profile = relationship(
        "CareGiverProfile",
        back_populates="user",
        uselist=False
    )

    """ Relationships with other models """
    created_subjects = relationship(
        "SubjectProfile",
        back_populates="created_by",
        foreign_keys="[SubjectProfile.created_by_id]"
    )
    assigned_subjects = relationship(
        "SubjectProfile",
        back_populates="assigned_care_giver",
        foreign_keys="[SubjectProfile.assigned_care_giver_id]"
    )
    

""" Role and UserRole association for many-to-many relationship implementation """
# class Role(Base):
#     __tablename__ = "roles"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     name = Column(String, unique=True)
# class UserRole(Base):
#     __tablename__ = "user_roles"

#     user_id = Column(ForeignKey("users.id"), primary_key=True)
#     role_id = Column(ForeignKey("roles.id"), primary_key=True)
   
#     User.roles = relationship("Role", secondary="user_roles")
