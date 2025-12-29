"""
Database Initialization Script
Run this to create all tables manually (bypasses Alembic)
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import init_db, engine, Base
from app.models import *  # Import all models
from app.core.vector_store import vector_store


async def setup_database():
    """Initialize database tables and Qdrant collections"""
    print("=" * 60)
    print("🚀 Intern_AI - Database Initialization")
    print("=" * 60)
    
    # Initialize PostgreSQL tables
    print("\n📦 Creating PostgreSQL tables...")
    try:
        await init_db()
        print("✅ PostgreSQL tables created successfully!")
        
        # List created tables
        print("\n📋 Created tables:")
        print("  - users")
        print("  - daily_logs")
        print("  - activities")
        print("  - assignments")
        print("  - projects")
        print("  - concepts")
        print("  - concept_relations")
        print("  - log_concepts")
        print("  - learning_patterns")
        print("  - pattern_instances")
        
    except Exception as e:
        print(f"❌ Failed to create PostgreSQL tables: {e}")
        print(f"\n⚠️  Error details: {str(e)}")
        return False
    
    # Initialize Qdrant collections
    print("\n📦 Creating Qdrant collections...")
    try:
        vector_store.initialize_collections()
        print("✅ Qdrant collections created successfully!")
        
        print("\n📋 Created collections:")
        print("  - concept_embeddings (384 dim)")
        print("  - log_embeddings (384 dim)")
        
    except Exception as e:
        print(f"❌ Failed to create Qdrant collections: {e}")
        print(f"\n⚠️  Error details: {str(e)}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ Database initialization complete!")
    print("=" * 60)
    print("\n🎉 You're ready to start using Intern_AI!")
    print("   Run: uvicorn app.main:app --reload")
    print("   Then visit: http://localhost:8000/docs")
    
    return True


async def test_connection():
    """Test database connection before initialization"""
    print("\n🔍 Testing database connection...")
    try:
        from app.config import settings
        from sqlalchemy import text
        print(f"   Database URL: {settings.database_url[:30]}...") 
        
        # Try to connect and run a simple query
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            result.fetchone()
        
        print("✅ Database connection successful!")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Check if PostgreSQL is running:")
        print("      Get-Service postgresql*")
        print("   2. Verify credentials in .env file")
        print("   3. Check if database 'intern_ai' exists:")
        print("      psql -U postgres -c '\\l'")
        print("   4. Try creating the database:")
        print("      psql -U postgres -c 'CREATE DATABASE intern_ai;'")
        return False


if __name__ == "__main__":
    print("\n🔧 Checking prerequisites...")
    
    # Test connection first
    connection_ok = asyncio.run(test_connection())
    
    if not connection_ok:
        print("\n⚠️  Please fix the database connection before continuing.")
        sys.exit(1)
    
    # Proceed with initialization
    print("\n" + "=" * 60)
    response = input("Proceed with database initialization? (yes/no): ")
    
    if response.lower() in ['yes', 'y']:
        success = asyncio.run(setup_database())
        sys.exit(0 if success else 1)
    else:
        print("❌ Initialization cancelled.")
        sys.exit(0)
