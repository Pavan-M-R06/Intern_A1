"""
Pydantic Schemas for API Request/Response Validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from uuid import UUID


# ===== Daily Log Schemas =====

class ActivityCreate(BaseModel):
    """Activity creation schema"""
    activity_type: str = Field(..., description="Type: coding, debugging, learning, meeting")
    description: str
    duration_minutes: Optional[int] = None


class AssignmentCreate(BaseModel):
    """Assignment creation schema"""
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None


class DailyLogCreate(BaseModel):
    """Daily log creation request"""
    log_date: date
    raw_text: str = Field(..., min_length=10, description="Raw daily log text")
    
    class Config:
        json_schema_extra = {
            "example": {
                "log_date": "2026-01-22",
                "raw_text": "Today I learned FastAPI routing and created 2 REST endpoints. Mentor assigned JWT authentication implementation. Struggled with async/await concepts."
            }
        }


class DailyLogResponse(BaseModel):
    """Daily log response"""
    id: UUID
    user_id: UUID
    log_date: date
    raw_text: str
    structured_data: Optional[Dict[str, Any]] = None
    mood: Optional[str] = None
    difficulty_level: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ===== Concept Schemas =====

class ConceptCreate(BaseModel):
    """Concept creation schema"""
    name: str
    definition: Optional[str] = None
    category: Optional[str] = None


class ConceptResponse(BaseModel):
    """Concept response"""
    id: UUID
    name: str
    definition: Optional[str] = None
    category: Optional[str] = None
    mastery_level: int
    times_practiced: int
    first_learned_date: Optional[date] = None
    
    class Config:
        from_attributes = True


# ===== Query/Reasoning Schemas =====

class SummarizeRequest(BaseModel):
    """Request for generating summary"""
    mode: str = Field(..., description="daily, weekly, or monthly")
    start_date: date
    end_date: Optional[date] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "mode": "weekly",
                "start_date": "2026-01-22",
                "end_date": "2026-01-28"
            }
        }


class SummarizeResponse(BaseModel):
    """Summary response"""
    summary: str
    mode: str
    date_range: Dict[str, str]
    metadata: Dict[str, Any]


class ExplainConceptRequest(BaseModel):
    """Request to explain a concept"""
    concept_name: str


class ExplainConceptResponse(BaseModel):
    """Concept explanation response"""
    concept_name: str
    explanation: str
    personalized: bool = True


class SearchRequest(BaseModel):
    """Semantic search request"""
    query: str
    limit: int = Field(default=5, ge=1, le=20)
    search_type: str = Field(default="concepts", description="concepts or logs")


class SearchResult(BaseModel):
    """Search result item"""
    score: float
    content: Dict[str, Any]


class SearchResponse(BaseModel):
    """Search response"""
    query: str
    results: List[SearchResult]


# ===== Analytics Schemas =====

class AnalyticsResponse(BaseModel):
    """Learning analytics response"""
    total_days_logged: int
    total_concepts_learned: int
    total_activities: int
    total_assignments: int
    learning_streak: int
    most_common_difficulties: List[str]
    top_concepts: List[Dict[str, Any]]
