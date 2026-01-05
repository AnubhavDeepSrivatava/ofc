from uuid import UUID
from app.schemas.base import BaseSchema


class SchoolCreate(BaseSchema):
    name: str
    logo_url: str | None = None
    ceo_name: str | None = None
    ceo_mobile: str | None = None


class SchoolResponse(BaseSchema):
    id: UUID
    name: str
    logo_url: str | None
    ceo_name: str | None
    ceo_mobile: str | None
    created_at: str
    updated_at: str
    created_by: UUID | None
    updated_by: UUID | None

