"""
Semantic Memory Models - SQLAlchemy ORM
Represents concepts learned and their relationships
"""
from sqlalchemy import Column, String, Text, Integer, Date, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.database import Base


class Concept(Base):
    """Concepts learned during internship"""
    __tablename__ = "concepts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False, index=True)
    definition = Column(Text)
    category = Column(String(100))  # 'programming', 'framework', 'algorithm', 'database'
    first_learned_date = Column(Date)
    mastery_level = Column(Integer, default=1)  # 1-5 scale
    times_practiced = Column(Integer, default=0)
    last_reviewed_date = Column(Date)
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    related_from = relationship("ConceptRelation", foreign_keys="ConceptRelation.concept_a_id", back_populates="concept_a")
    related_to = relationship("ConceptRelation", foreign_keys="ConceptRelation.concept_b_id", back_populates="concept_b")


class ConceptRelation(Base):
    """Relationships between concepts"""
    __tablename__ = "concept_relations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    concept_a_id = Column(UUID(as_uuid=True), ForeignKey("concepts.id", ondelete="CASCADE"))
    concept_b_id = Column(UUID(as_uuid=True), ForeignKey("concepts.id", ondelete="CASCADE"))
    relation_type = Column(String(50))  # 'prerequisite', 'related', 'similar', 'part_of'
    strength = Column(Float, default=0.5)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    concept_a = relationship("Concept", foreign_keys=[concept_a_id], back_populates="related_from")
    concept_b = relationship("Concept", foreign_keys=[concept_b_id], back_populates="related_to")


class LogConcept(Base):
    """Link between daily logs and concepts"""
    __tablename__ = "log_concepts"
    
    log_id = Column(UUID(as_uuid=True), ForeignKey("daily_logs.id", ondelete="CASCADE"), primary_key=True)
    concept_id = Column(UUID(as_uuid=True), ForeignKey("concepts.id", ondelete="CASCADE"), primary_key=True)
    context = Column(Text)
