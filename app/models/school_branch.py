import uuid
from sqlalchemy import Column, String, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.models.base import Base


class SchoolBranch(Base):
    __tablename__ = "school_branches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    school_id = Column(UUID(as_uuid=True), nullable=False)
    branch_name = Column(String, nullable=False)
    address = Column(Text, nullable=False)
    branch_head_name = Column(String, nullable=True)
    contact_number = Column(String, nullable=True)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))

