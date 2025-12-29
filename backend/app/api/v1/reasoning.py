"""
Reasoning API Endpoints
Handle AI-powered queries, summaries, and explanations
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import Dict, Any
from datetime import date, timedelta
import uuid

from app.database import get_db
from app.schemas.common import (
    SummarizeRequest, SummarizeResponse,
    ExplainConceptRequest, ExplainConceptResponse,
    SearchRequest, SearchResponse, SearchResult
)
from app.models import DailyLog, Concept
from app.services.llm_service import llm_service
from app.core.embeddings import embedding_generator
from app.core.vector_store import vector_store

router = APIRouter()

TEMP_USER_ID = "00000000-0000-0000-0000-000000000001"


@router.post("/reasoning/summarize", response_model=SummarizeResponse)
async def generate_summary(
    request: SummarizeRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Generate VTU diary summary for specified date range
    Modes: daily, weekly, monthly
    """
    # Calculate end date if not provided
    end_date = request.end_date
    if not end_date:
        if request.mode == "daily":
            end_date = request.start_date
        elif request.mode == "weekly":
            end_date = request.start_date + timedelta(days=6)
        elif request.mode == "monthly":
            end_date = request.start_date + timedelta(days=29)
    
    # Fetch logs in date range
    result = await db.execute(
        select(DailyLog).where(
            and_(
                DailyLog.user_id == uuid.UUID(TEMP_USER_ID),
                DailyLog.log_date >= request.start_date,
                DailyLog.log_date <= end_date
            )
        ).order_by(DailyLog.log_date)
    )
    logs = result.scalars().all()
    
    if not logs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No logs found between {request.start_date} and {end_date}"
        )
    
    # Prepare data for LLM
    summary_data = {
        "date_range": {
            "start": str(request.start_date),
            "end": str(end_date)
        },
        "total_days": len(logs),
        "logs": [
            {
                "date": str(log.log_date),
                "raw_text": log.raw_text,
                "structured_data": log.structured_data,
                "mood": log.mood,
                "difficulty": log.difficulty_level
            }
            for log in logs
        ]
    }
    
    # Generate summary using LLM
    try:
        summary_text = llm_service.generate_summary(summary_data, mode=request.mode)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate summary: {str(e)}"
        )
    
    return SummarizeResponse(
        summary=summary_text,
        mode=request.mode,
        date_range={"start": str(request.start_date), "end": str(end_date)},
        metadata={
            "total_days": len(logs),
            "avg_difficulty": "medium"  # TODO: Calculate from logs
        }
    )


@router.post("/reasoning/explain", response_model=ExplainConceptResponse)
async def explain_concept(
    request: ExplainConceptRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Explain a concept with identity-aware personalization
    Uses user's learning history for context
    """
    # Get user's learned concepts
    result = await db.execute(
        select(Concept.name).where(
            Concept.user_id == uuid.UUID(TEMP_USER_ID)
        )
    )
    learned_concepts = [row[0] for row in result.all()]
    
    # TODO: Get past mistakes from learning_patterns table
    past_mistakes = []
    
    # Build user context
    user_context = {
        "learned_concepts": learned_concepts,
        "past_mistakes": past_mistakes,
        "current_level": "intermediate"  # TODO: Calculate based on mastery levels
    }
    
    # Generate personalized explanation
    try:
        explanation = llm_service.explain_concept(request.concept_name, user_context)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate explanation: {str(e)}"
        )
    
    return ExplainConceptResponse(
        concept_name=request.concept_name,
        explanation=explanation,
        personalized=True
    )


@router.post("/reasoning/search", response_model=SearchResponse)
async def semantic_search(
    request: SearchRequest
):
    """
    Semantic search across concepts or logs using vector similarity
    """
    # Generate query embedding
    try:
        query_embedding = embedding_generator.generate(request.query)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate embedding: {str(e)}"
        )
    
    # Search in appropriate collection
    try:
        if request.search_type == "concepts":
            results = vector_store.search_similar_concepts(query_embedding, limit=request.limit)
        elif request.search_type == "logs":
            results = vector_store.search_similar_logs(query_embedding, limit=request.limit)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="search_type must be 'concepts' or 'logs'"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )
    
    # Format results
    search_results = [
        SearchResult(score=r["score"], content=r)
        for r in results
    ]
    
    return SearchResponse(
        query=request.query,
        results=search_results
    )


@router.get("/reasoning/guidance")
async def get_learning_guidance(
    db: AsyncSession = Depends(get_db)
):
    """
    Get personalized learning guidance based on history
    """
    # Fetch user's learning history
    logs_result = await db.execute(
        select(DailyLog).where(
            DailyLog.user_id == uuid.UUID(TEMP_USER_ID)
        ).order_by(DailyLog.log_date.desc()).limit(10)
    )
    recent_logs = logs_result.scalars().all()
    
    concepts_result = await db.execute(
        select(Concept).where(
            Concept.user_id == uuid.UUID(TEMP_USER_ID)
        ).order_by(Concept.mastery_level.desc())
    )
    concepts = concepts_result.scalars().all()
    
    # Prepare history data
    user_history = {
        "total_days": len(recent_logs),
        "recent_concepts": [c.name for c in concepts[:10]],
        "mastery_levels": {c.name: c.mastery_level for c in concepts},
        "recent_activities": [
            log.structured_data.get("activities", []) 
            for log in recent_logs 
            if log.structured_data
        ]
    }
    
    # Generate guidance
    try:
        guidance = llm_service.generate_guidance(user_history)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate guidance: {str(e)}"
        )
    
    return {
        "guidance": guidance,
        "context": {
            "total_concepts_learned": len(concepts),
            "days_logged": len(recent_logs)
        }
    }
