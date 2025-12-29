# Intern_AI - Local Development Setup Guide

This guide will walk you through setting up Intern_AI for local development.

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] Python 3.11 or higher
- [ ] Node.js 18 or higher
- [ ] PostgreSQL 16 installed
- [ ] Docker Desktop (for Qdrant)
- [ ] Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))

---

## Step 1: Database Setup

### PostgreSQL Setup

1. **Install PostgreSQL 16** (if not already installed):

   - Windows: Download from [postgresql.org](https://www.postgresql.org/download/windows/)
   - Mac: `brew install postgresql@16`
   - Linux: `sudo apt install postgresql-16`

2. **Start PostgreSQL service**:

   ```bash
   # Windows (PowerShell as Admin)
   net start postgresql-x64-16

   # Mac
   brew services start postgresql@16

   # Linux
   sudo systemctl start postgresql
   ```

3. **Create database**:

   ```bash
   # Connect to PostgreSQL
   psql -U postgres

   # Create database
   CREATE DATABASE intern_ai;

   # Create user (optional, for production-like setup)
   CREATE USER intern_ai_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE intern_ai TO intern_ai_user;

   # Exit
   \q
   ```

### Qdrant Setup (Vector Database)

1. **Start Qdrant using Docker**:

   ```bash
   docker run -d -p 6333:6333 -p 6334:6334 \
     -v qdrant_storage:/qdrant/storage \
     --name qdrant \
     qdrant/qdrant
   ```

2. **Verify Qdrant is running**:
   - Open browser: `http://localhost:6333/dashboard`
   - You should see the Qdrant dashboard

---

## Step 2: Backend Setup

1. **Navigate to backend directory**:

   ```bash
   cd backend
   ```

2. **Create virtual environment**:

   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**:

   ```bash
   # Windows
   .\venv\Scripts\activate

   # Mac/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Create `.env` file**:

   ```bash
   cp .env.example .env
   ```

6. **Edit `.env` with your settings**:

   ```env
   DATABASE_URL=postgresql://postgres:your_postgres_password@localhost:5432/intern_ai
   QDRANT_URL=http://localhost:6333
   GEMINI_API_KEY=your_gemini_api_key_here
   SECRET_KEY=your-secret-key-here
   ```

7. **Initialize database** (create tables):

   ```bash
   # We'll use Alembic migrations (to be setup next)
   # For now, tables will be created automatically on first run
   ```

8. **Run backend server**:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

9. **Verify backend is running**:
   - Open browser: `http://localhost:8000`
   - You should see: `{"message": "Welcome to Intern_AI API", ...}`
   - API docs: `http://localhost:8000/docs`

---

## Step 3: Frontend Setup

1. **Open new terminal and navigate to frontend**:

   ```bash
   cd frontend
   ```

2. **Create `.env.local` file**:

   ```bash
   # Create the file manually
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
   ```

3. **Install dependencies** (if not already done):

   ```bash
   npm install
   ```

4. **Run development server**:

   ```bash
   npm run dev
   ```

5. **Verify frontend is running**:
   - Open browser: `http://localhost:3000`

---

## Step 4: Verify Everything Works

### Backend Health Check

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{ "status": "healthy", "app": "Intern_AI", "version": "1.0.0" }
```

### Database Connection

```bash
# Inside backend venv
python -c "from app.database import engine; print('Database connected!')"
```

### Qdrant Connection

```bash
curl http://localhost:6333/collections
```

---

## Next Steps

Now that everything is set up, you can:

1. **Start development** on Phase 2: Database Schemas
2. **Test API endpoints** using Swagger docs at `http://localhost:8000/docs`
3. **Begin building** the ingestion pipeline

---

## Troubleshooting

### PostgreSQL Connection Error

- Ensure PostgreSQL service is running
- Check DATABASE_URL in `.env`
- Verify database exists: `psql -U postgres -l`

### Qdrant Connection Error

- Check Docker container is running: `docker ps`
- Restart Qdrant: `docker restart qdrant`

### Python Dependencies Error

- Ensure you're in virtual environment: `which python` (should show venv path)
- Upgrade pip: `pip install --upgrade pip`
- Try installing dependencies one by one

### Node Modules Error

- Delete `node_modules` and `package-lock.json`
- Run `npm install` again

---

## Development Workflow

**Terminal 1 - Backend**:

```bash
cd backend
venv\Scripts\activate  # Windows
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend**:

```bash
cd frontend
npm run dev
```

**Terminal 3 - Database/Tools**:

```bash
# For running migrations, database queries, etc.
```

---

## API Key Setup

### Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the key
4. Paste in `backend/.env` → `GEMINI_API_KEY=your_key_here`

### Optional: OpenAI & Claude (Fallback)

- OpenAI: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- Claude: [console.anthropic.com](https://console.anthropic.com/)

---

## Ready to Build! 🚀

Your development environment is ready. Check `task.md` for the next phase of development.
