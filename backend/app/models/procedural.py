"""
Procedural Memory Models - SQLAlchemy ORM
Represents learning patterns, mistakes, and preferences
"""
from sqlalchemy import Column, String, Text, Integer, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.sql import func
import uuid

from app.database import Base


class LearningPattern(Base):
    """Patterns in learning behavior - mistakes, preferences, strengths"""
    __tablename__ = "learning_patterns"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    pattern_type = Column(String(50))  # 'mistake', 'preference', 'strength', 'weakness'
    category = Column(String(100))
    description = Column(Text, nullable=False)
    first_observed_date = Column(Date)
    occurrences = Column(Integer, default=1)
    last_observed_date = Column(Date)
    severity = Column(String(20))  # 'low', 'medium', 'high'
    resolution_notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())


class PatternInstance(Base):
    """Links specific pattern occurrences to daily logs"""
    __tablename__ = "pattern_instances"
    
    pattern_id = Column(UUID(as_uuid=True), ForeignKey("learning_patterns.id", ondelete="CASCADE"), primary_key=True)
    log_id = Column(UUID(as_uuid=True), ForeignKey("daily_logs.id", ondelete="CASCADE"), primary_key=True)
    notes = Column(Text)
