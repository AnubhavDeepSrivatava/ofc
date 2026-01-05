from sqlalchemy import Column, Integer, String, Boolean
from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)

    # Core fields
    user_name = Column(String(100), nullable=False)
    user_email = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    # Flags / checks
    is_enabled = Column(Boolean, default=True)
    send_welcome_email = Column(Boolean, default=False)

    user_image = Column(String(255), nullable=True)
