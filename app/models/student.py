from sqlalchemy import Column, Integer, Boolean, ForeignKey, Enum, Text
from app.models.base import Base
import enum

class GenderEnum(enum.Enum):
    M = "M"
    F = "F"
    OTHER = "OTHER"

class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True)

    gender = Column(Enum( GenderEnum,name="gender_enum"), nullable=False)
    # school_id = Column(Integer, ForeignKey("schools.school_id"), nullable=False)
    onboarding_process_done = Column(Boolean, default=False)
    idea = Column(Text)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True, nullable=False)

