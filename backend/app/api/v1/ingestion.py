"""
Daily Log Ingestion API Endpoints
Handle creation and retrieval of daily logs
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import date
import uuid

from app.database import get_db
from app.schemas.common import DailyLogCreate, DailyLogResponse
from app.models import DailyLog, User
from app.services.llm_service import llm_service
from app.core.embeddings import embedding_generator
from app.core.vector_store import vector_store

router = APIRouter()

# Temporary: For single-user MVP, use a fixed user ID
# TODO: Replace with proper authentication
TEMP_USER_ID = "00000000-0000-0000-0000-000000000001"


async def get_or_create_temp_user(db: AsyncSession) -> str:
    """Get or create temporary user for MVP"""
    result = await db.execute(
        select(User).where(User.id == uuid.UUID(TEMP_USER_ID))
    )
    user = result.scalar_one_or_none()
    
    if not user:
        user = User(
            id=uuid.UUID(TEMP_USER_ID),
            email="temp@intern-ai.com",
            full_name="Test User"
        )
        db.add(user)
        await db.commit()
    
    return TEMP_USER_ID


@router.post("/logs/daily", response_model=DailyLogResponse, status_code=status.HTTP_201_CREATED)
async def create_daily_log(
    log_data: DailyLogCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new daily log entry
    
    - Extracts structured data using Gemini
    - Stores in PostgreSQL
    - Generates and stores embeddings in Qdrant
    """
    user_id = await get_or_create_temp_user(db)
    
    # Check if log for this date already exists
    result = await db.execute(
        select(DailyLog).where(
            DailyLog.user_id == uuid.UUID(user_id),
            DailyLog.log_date == log_data.log_date
        )
    )
    existing_log = result.scalar_one_or_none()
    
    if existing_log:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Log for {log_data.log_date} already exists. Use PUT to update."
        )
    
    # Extract structured data using LLM
    print(f"🤖 Extracting structured data from log...")
    try:
        structured_data = llm_service.extract_structured_data(log_data.raw_text)
    except Exception as e:
        print(f"⚠️ LLM extraction failed: {e}")
        structured_data = {}
    
    # Create daily log
    daily_log = DailyLog(
        user_id=uuid.UUID(user_id),
        log_date=log_data.log_date,
        raw_text=log_data.raw_text,
        structured_data=structured_data,
        mood=structured_data.get("mood"),
        difficulty_level=structured_data.get("difficulty_level")
    )
    
    db.add(daily_log)
    await db.commit()
    await db.refresh(daily_log)
    
    # Generate and store embedding (async task in production)
    try:
        embedding = embedding_generator.generate_log_embedding(log_data.raw_text)
        concepts = structured_data.get("concepts", [])
        
        vector_store.add_log_embedding(
            log_id=str(daily_log.id),
            embedding=embedding,
            log_date=str(log_data.log_date),
            summary=log_data.raw_text[:200],  # First 200 chars as summary
            concepts=concepts
        )
        print(f"✅ Stored embedding in Qdrant")
    except Exception as e:
        print(f"⚠️ Failed to store embedding: {e}")
    
    return daily_log


@router.get("/logs/daily/{log_date}", response_model=DailyLogResponse)
async def get_daily_log(
    log_date: date,
    db: AsyncSession = Depends(get_db)
):
    """Get daily log by date"""
    user_id = await get_or_create_temp_user(db)
    
    result = await db.execute(
        select(DailyLog).where(
            DailyLog.user_id == uuid.UUID(user_id),
            DailyLog.log_date == log_date
        )
    )
    log = result.scalar_one_or_none()
    
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No log found for {log_date}"
        )
    
    return log


@router.get("/logs/daily", response_model=List[DailyLogResponse])
async def list_daily_logs(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """List all daily logs with pagination"""
    user_id = await get_or_create_temp_user(db)
    
    result = await db.execute(
        select(DailyLog)
        .where(DailyLog.user_id == uuid.UUID(user_id))
        .order_by(DailyLog.log_date.desc())
        .offset(skip)
        .limit(limit)
    )
    logs = result.scalars().all()
    
    return logs


@router.put("/logs/daily/{log_date}", response_model=DailyLogResponse)
async def update_daily_log(
    log_date: date,
    log_data: DailyLogCreate,
    db: AsyncSession = Depends(get_db)
):
    """Update an existing daily log"""
    user_id = await get_or_create_temp_user(db)
    
    result = await db.execute(
        select(DailyLog).where(
            DailyLog.user_id == uuid.UUID(user_id),
            DailyLog.log_date == log_date
        )
    )
    log = result.scalar_one_or_none()
    
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No log found for {log_date}"
        )
    
    # Re-extract structured data
    try:
        structured_data = llm_service.extract_structured_data(log_data.raw_text)
    except Exception as e:
        print(f"⚠️ LLM extraction failed: {e}")
        structured_data = log.structured_data or {}
    
    # Update log
    log.raw_text = log_data.raw_text
    log.structured_data = structured_data
    log.mood = structured_data.get("mood")
    log.difficulty_level = structured_data.get("difficulty_level")
    
    await db.commit()
    await db.refresh(log)
    
    return log
