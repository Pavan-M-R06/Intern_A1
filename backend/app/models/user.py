"""
User Model - SQLAlchemy ORM
Represents users in the system
"""
from sqlalchemy import Column, String, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.database import Base


class User(Base):
    """User model for authentication and profile"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255))
    internship_start_date = Column(Date)
    internship_end_date = Column(Date)
    company_name = Column(String(255))
    created_at = Column(Date, server_default=func.now())
