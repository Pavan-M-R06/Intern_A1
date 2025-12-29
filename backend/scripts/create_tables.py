"""
Direct Database Table Creation
Run with: python -m scripts.create_tables
"""
import asyncio

async def create_all_tables():
    from app.database import Base, engine
    from app.models import (
        User, DailyLog, Activity, Assignment, Project,
        Concept, ConceptRelation, LogConcept,
        LearningPattern, PatternInstance
    )
    
    print("Creating all database tables...")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ All tables created successfully!")
    print("\nCreated tables:")
    for table_name in Base.metadata.tables.keys():
        print(f"  ✓ {table_name}")

if __name__ == "__main__":
    asyncio.run(create_all_tables())
