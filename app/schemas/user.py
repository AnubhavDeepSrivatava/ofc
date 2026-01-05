from uuid import UUID
from pydantic import EmailStr
from app.schemas.base import BaseSchema
from enum import Enum

class UserTypeEnum(str, Enum):
    student = "student"
    jury = "jury"
    admin = "admin"
    staff = "staff"
    platform_admin = "platform_admin"

class UserCreate(BaseSchema):
    username: str
    email: EmailStr
    password: str
    user_type: UserTypeEnum
    is_enabled: bool = True
    should_send_welcome_email: bool = True
    image_url: str | None = None


class UserResponse(BaseSchema):
    id: UUID
    username: str
    email: str
    user_type: UserTypeEnum
    is_enabled: bool
    should_send_welcome_email: bool
    image_url: str | None
    created_at: str
    updated_at: str
    created_by: UUID | None
    updated_by: UUID | None
