from sqlalchemy import Column, Enum, Integer, String, Boolean, TIMESTAMP, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import text
import uuid

from app.core.db_base import Base
from app.enum import RequestType, RequestCategory, DurationType


class Request(Base):
    __tablename__ = "requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subject_id = Column(ForeignKey("subject_profiles.id", ondelete="CASCADE"), nullable=False)
    # subject_id = Column(
    #     UUID(as_uuid=True),
    #     ForeignKey("subject_profiles.id", ondelete="CASCADE"),
    #     nullable=False
    # )
    owner_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    care_type = Column(Enum(RequestType), nullable=False, default=RequestType.NON_MEDICAL)
    category = Column(Enum(RequestCategory), nullable=False, default=RequestCategory.ELDERLY)
    duration = Column(Enum(DurationType), nullable=False, default=DurationType.HOURLY)  # duration in hours
    description = Column(String, nullable=False)
    is_handled = Column(Boolean, default=False)
    created_at = Column( 
        TIMESTAMP(timezone=True), 
        nullable=False, server_default=text('now()')
    )    
    """ Relationships with other models """

    subject = relationship(
        "SubjectProfile",
        back_populates="requests"
    )

    owner = relationship(
        "User",
        back_populates="requests"
    )

