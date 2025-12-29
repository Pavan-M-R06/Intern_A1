"""
Episodic Memory Models - SQLAlchemy ORM
Represents daily logs, activities, assignments, and projects
"""
from sqlalchemy import Column, String, Text, Integer, Date, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.database import Base


class DailyLog(Base):
    """Daily log entries with raw and structured data"""
    __tablename__ = "daily_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    log_date = Column(Date, nullable=False, index=True)
    raw_text = Column(Text, nullable=False)
    structured_data = Column(JSONB)
    mood = Column(String(50))
    difficulty_level = Column(String(20))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    activities = relationship("Activity", back_populates="log", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="log")


class Activity(Base):
    """Activities performed during internship"""
    __tablename__ = "activities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    log_id = Column(UUID(as_uuid=True), ForeignKey("daily_logs.id", ondelete="CASCADE"))
    activity_type = Column(String(50))  # 'coding', 'debugging', 'learning', 'meeting'
    description = Column(Text, nullable=False)
    duration_minutes = Column(Integer)
    status = Column(String(20), default='completed')
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    log = relationship("DailyLog", back_populates="activities")


class Assignment(Base):
    """Tasks and assignments"""
    __tablename__ = "assignments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    log_id = Column(UUID(as_uuid=True), ForeignKey("daily_logs.id", ondelete="SET NULL"))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    assigned_date = Column(Date)
    due_date = Column(Date)
    status = Column(String(20), default='pending')
    completion_notes = Column(Text)
    completed_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    log = relationship("DailyLog", back_populates="assignments")


class Project(Base):
    """Projects worked on during internship"""
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    tech_stack = Column(ARRAY(Text))
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(20), default='active')
    repo_url = Column(String(500))
    created_at = Column(TIMESTAMP, server_default=func.now())
