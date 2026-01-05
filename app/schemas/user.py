from pydantic import EmailStr
from app.schemas.base import BaseSchema


class UserCreate(BaseSchema):
    user_name: str
    user_email: EmailStr
    password: str
    is_enabled: bool = True
    send_welcome_email: bool = False
    user_image: str | None = None


class UserResponse(BaseSchema):
    user_id: int
    user_name: str
    user_email: str
    is_enabled: bool
    send_welcome_email: bool
    user_image: str | None
    created_at: str
    updated_at: str
    created_by: str | None
    updated_by: str | None
