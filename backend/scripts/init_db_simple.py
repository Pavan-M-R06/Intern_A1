"""
Simple Database Initialization Script
Creates PostgreSQL tables only (Qdrant will auto-initialize on first API call)
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


async def initialize_database():
    """Initialize PostgreSQL database tables"""
    from app.database import Base, engine
    from sqlalchemy import text
    from app.models import *  # Import all models
    
    print("=" * 60)
    print("🚀 Intern_AI - Database Initialization")
    print("=" * 60)
    
    # Test connection
    print("\n🔍 Testing database connection...")
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            result.fetchone()
        print("✅ Database connection successful!")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False
    
    # Create tables
    print("\n📦 Creating PostgreSQL tables...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        print("✅ All tables created successfully!")
        
        # List created tables
        print("\n📋 Created tables:")
        tables = [
            "users", "daily_logs", "activities", "assignments",
            "projects", "concepts", "concept_relations", "log_concepts",
            "learning_patterns", "pattern_instances"
        ]
        for table in tables:
            print(f"   ✓ {table}")
        
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False
    
    # Note about Qdrant
    print("\n📦 Qdrant Vector Store:")
    print("   ℹ️  Collections will be created automatically on first use")
    print("   ℹ️  No manual initialization needed")
    
    print("\n" + "=" * 60)
    print("✅ Database initialization complete!")
    print("=" * 60)
    print("\n🎉 You're ready to start using Intern_AI!")
    print("\n📝 Next steps:")
    print("   1. Start backend: uvicorn app.main:app --reload")
    print("   2. Visit API docs: http://localhost:8000/docs")
    print("   3. Test endpoints in the interactive documentation")
    
    return True


if __name__ == "__main__":
    print("\n🚀 Starting database initialization...\n")
    
    success = asyncio.run(initialize_database())
    
    if success:
        print("\n✅ SUCCESS! Database is ready.")
        sys.exit(0)
    else:
        print("\n❌ FAILED! Please check errors above.")
        sys.exit(1)
