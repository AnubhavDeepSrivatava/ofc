from app.schemas.base import BaseSchema
from app.models.student import GenderEnum


class StudentCreate(BaseSchema):
    user_id: int
    gender: GenderEnum
    onboarding_process_done: bool = False
    idea: str | None = None


class StudentResponse(BaseSchema):
    student_id: int
    user_id: int
    gender: str
    onboarding_process_done: bool
    idea: str | None
    created_at: str
    updated_at: str
    created_by: str | None
    updated_by: str | None
