from datetime import datetime
from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    # These fields will exist in EVERY table
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)