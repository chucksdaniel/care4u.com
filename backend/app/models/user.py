from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import text
from sqlalchemy.ext.declarative import declarative_base
from app.core.db_base import Base
import uuid


class User(Base):
    __tablename__ = "users"

    id =  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False,)
    created_at = Column(
        TIMESTAMP(timezone=True), 
        nullable=False, server_default=text('now()')
    )