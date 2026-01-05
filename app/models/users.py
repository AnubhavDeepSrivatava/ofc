# app/models/users.py
from sqlalchemy import Column, String, Boolean, Enum, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.models.base import Base
from app.schemas.user import UserTypeEnum
from uuid7 import uuid7
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid7)

    username = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)

    user_type = Column(Enum(UserTypeEnum, name="user_type_enum"), nullable=False)

    is_enabled = Column(Boolean, default=True)
    should_send_welcome_email = Column(Boolean, default=True)

    image_url = Column(String(512))
    
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))

