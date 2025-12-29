# Database Migration & Initialization Script

**Note**: Alembic migrations are configured but pending PostgreSQL credentials verification.

## Manual Database Setup (Alternative)

If you prefer to set up tables manually or fix PostgreSQL connection issues:

### Option 1: Using Python

```python
# Run this script to create all tables
import asyncio
from app.database import init_db

async def setup_db():
    print("Creating database tables...")
    await init_db()
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(setup_db())
```

Save as `scripts/init_db.py` and run:

```bash
python scripts/init_db.py
```

### Option 2: Using Alembic (Recommended)

Once PostgreSQL credentials are verified:

```bash
# Generate initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

### Current Status

- ✅ Alembic configured
- ✅ Models defined
- ⏳ Awaiting PostgreSQL connection verification

**Error encountered**: Authentication failed for user "postgres"

**To fix**:

1. Verify PostgreSQL is running: `pg_isready`
2. Check password in `.env` file
3. Try connecting manually: `psql -U postgres -d intern_ai`
4. If needed, reset password or create new user

### Qdrant Setup

Qdrant collections are initialized automatically on first API call.

To manually initialize:

```python
from app.core.vector_store import vector_store
vector_store.initialize_collections()
```
