from uuid import UUID
from app.schemas.base import BaseSchema


class SchoolBranchCreate(BaseSchema):
    school_id: UUID
    branch_name: str
    address: str
    branch_head_name: str | None = None
    contact_number: str | None = None


class SchoolBranchResponse(BaseSchema):
    id: UUID
    school_id: UUID
    branch_name: str
    address: str
    branch_head_name: str | None
    contact_number: str | None
    created_at: str
    updated_at: str
    created_by: UUID | None
    updated_by: UUID | None

