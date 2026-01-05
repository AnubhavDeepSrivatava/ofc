import enum
from sqlalchemy import Column, Boolean, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class GenderEnum(enum.Enum):
    male = "male"
    female = "female"
    other = "other"
    prefer_not_to_say = "prefer_not_to_say"


class Student(Base):
    __tablename__ = "students"

    user_id = Column(UUID(as_uuid=True), primary_key=True)

    branch_id = Column(UUID(as_uuid=True), nullable=False)
    full_name = Column(Text, nullable=False)

    gender = Column(
        Enum(GenderEnum, name="gender_enum"),
        nullable=True
    )

    is_onboarding_completed = Column(Boolean, default=False)
    idea_description = Column(Text, nullable=True)
