from uuid import UUID
from app.schemas.base import BaseSchema
from app.models.student import GenderEnum


class StudentCreate(BaseSchema):
    user_id: UUID
    branch_id: UUID
    full_name: str
    gender: GenderEnum | None = None
    is_onboarding_completed: bool = False
    idea_description: str | None = None


class StudentResponse(BaseSchema):
    user_id: UUID
    branch_id: UUID
    full_name: str
    gender: GenderEnum | None
    is_onboarding_completed: bool
    idea_description: str | None
    created_at: str
    updated_at: str
    created_by: UUID | None
    updated_by: UUID | None
