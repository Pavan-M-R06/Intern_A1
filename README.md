# Intern_AI

A personal learning companion that helps students track their internship journey, generate diary entries, and get personalized study assistance.

## What is this?

During my 8th semester CS engineering internship, I needed a way to keep track of everything I learned daily and generate proper diary entries for university submission. Instead of maintaining manual notes and struggling to recall what I did weeks ago, I built this tool to:

- Record daily learning activities, concepts, and projects
- Extract structured data from free-form text using LLMs
- Generate professional VTU diary entries automatically
- Get personalized explanations based on what I've already learned
- Search through my learning history semantically

Think of it as a memory system that actually understands what you're learning, rather than just storing text.

## Features

### Daily Logging

Write what you learned in plain text. The system extracts:

- Concepts and technologies
- Activities and their duration
- Assignments and deadlines
- Your mood and difficulty level
- Project work

### VTU Diary Generation

Generate properly formatted diary entries for daily, weekly, or monthly reports. No more struggling to remember what you did two weeks ago when the submission deadline arrives.

### Personalized Teaching

Ask questions and get explanations tailored to your level. The system knows what you've already learned and what you struggled with, so it can explain new concepts in context.

### Semantic Search

Find concepts or logs using natural language. Instead of keyword matching, it understands meaning—search for "authentication" and find related entries about JWT, OAuth, and sessions.

## Tech Stack

**Backend:**

- FastAPI (Python 3.11+)
- PostgreSQL 16 (structured data)
- Qdrant (vector database for semantic search)
- SQLAlchemy 2.0 + Alembic (ORM and migrations)

**Frontend:**

- Next.js 14 (React + TypeScript)
- TailwindCSS (styling)
- Lucide React (icons)

**AI Integration:**

- Google Gemini (primary LLM)
- OpenAI & Claude (fallback)
- Sentence Transformers (embeddings)

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 16
- Qdrant (can run via Docker)

### Backend Setup

1. **Clone and navigate:**

   ```bash
   git clone <repository-url>
   cd Intern_AI/backend
   ```

2. **Create virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   Create a `.env` file in the backend directory:

   ```env
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/intern_ai
   QDRANT_URL=http://localhost:6333
   GEMINI_API_KEY=your_gemini_api_key
   OPENAI_API_KEY=your_openai_key  # optional
   CLAUDE_API_KEY=your_claude_key  # optional
   SECRET_KEY=your-secret-key-here
   ALLOWED_ORIGINS=http://localhost:3000
   ```

5. **Setup database:**

   First, verify your PostgreSQL password:

   ```bash
   python scripts/verify_password.py
   ```

   Then create tables:

   ```bash
   python -m scripts.create_tables
   ```

6. **Start Qdrant (using Docker):**

   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```

7. **Run the server:**

   ```bash
   uvicorn app.main:app --reload
   ```

   Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate and install:**

   ```bash
   cd ../frontend
   npm install
   ```

2. **Configure environment:**
   Create `.env.local`:

   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. **Run development server:**

   ```bash
   npm run dev
   ```

   Frontend will be available at `http://localhost:3000`

## Usage

### Adding Daily Logs

1. Go to `/log` page
2. Select the date
3. Write about your day in plain text:
   ```
   Today I learned FastAPI routing and created 2 REST endpoints.
   Mentor assigned JWT authentication implementation.
   Struggled with async/await but figured it out after 2 hours.
   ```
4. Submit and watch the system extract structured data automatically

### Generating Diary Entries

1. Go to `/diary` page
2. Select summary type (daily/weekly/monthly)
3. Pick the date range
4. Click generate
5. Copy or export the professional diary entry

### Asking Questions

1. Go to `/query` page
2. Ask anything: "Explain JWT authentication"
3. Get a personalized response based on your learning history

### Searching Your Memory

1. Go to `/search` page
2. Toggle between concepts or logs
3. Enter your query
4. See semantically similar results ranked by relevance

## Project Structure

```
Intern_AI/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # API endpoints
│   │   ├── core/            # Vector store, embeddings
│   │   ├── models/          # SQLAlchemy models
│   │   ├── services/        # LLM service
│   │   ├── config.py        # Configuration
│   │   ├── database.py      # Database setup
│   │   └── main.py          # FastAPI app
│   ├── alembic/             # Database migrations
│   ├── scripts/             # Utility scripts
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── app/            # Next.js pages
│   │   │   ├── log/        # Daily log page
│   │   │   ├── diary/      # VTU diary generator
│   │   │   ├── query/      # AI query interface
│   │   │   └── search/     # Semantic search
│   │   └── lib/
│   │       └── api.ts      # API client
│   ├── tailwind.config.ts
│   └── package.json
│
└── docs/                    # Documentation
```

## Database Schema

The system uses three types of memory:

**Episodic Memory** (what happened):

- Daily logs with structured data
- Activities, assignments, projects
- Temporal information

**Semantic Memory** (what you know):

- Concepts learned
- Relationships between concepts
- Mastery levels

**Procedural Memory** (patterns):

- Learning patterns
- Common mistakes
- Progress tracking

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

Key endpoints:

- `POST /api/v1/logs/daily` - Create daily log
- `GET /api/v1/logs/daily/{date}` - Retrieve log
- `POST /api/v1/reasoning/summarize` - Generate VTU diary
- `POST /api/v1/reasoning/explain` - Get concept explanation
- `POST /api/v1/reasoning/search` - Semantic search

## Troubleshooting

### PostgreSQL Connection Issues

If you get authentication errors, run:

```bash
python scripts/verify_password.py
```

This will test different connection scenarios and tell you the correct credentials.

### Frontend Build Errors

If you see Tailwind CSS errors, clear the cache:

```bash
rm -rf .next
npm run dev
```

### Qdrant Connection

Make sure Qdrant is running:

```bash
docker ps | grep qdrant
```

## Future Enhancements

- [ ] Analytics dashboard for learning progress
- [ ] Concept relationship visualization
- [ ] Interview preparation mode
- [ ] Voice input support
- [ ] Multi-user support with authentication
- [ ] Mobile app
- [ ] Export to PDF functionality

## Contributing

This is a personal project built for my internship needs, but feel free to fork and adapt it for your use case.

## License

MIT

---

Built during my 3-month internship period to solve a real problem I was facing. Hope it helps other students too.
