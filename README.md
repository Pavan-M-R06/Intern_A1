# Intern_AI - AI-Powered Learning Companion

A memory-first, identity-aware AI system that tracks your internship learning journey, generates VTU diary entries, and provides personalized teaching.

## 🚀 Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: Next.js 14 (React, TypeScript)
- **Database**: PostgreSQL 16
- **Vector DB**: Qdrant
- **AI**: Google Gemini API (primary), OpenAI/Claude (fallback)

## 📂 Project Structure

```
Intern_AI/
├── backend/          # FastAPI backend
├── frontend/         # Next.js frontend
├── docs/             # Documentation
└── README.md
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 16
- Docker (for Qdrant)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## 📝 Core Features

1. **Daily Log Tracking** - Record what you learned each day
2. **Structured Memory** - Episodic, semantic, and procedural memory storage
3. **VTU Diary Generator** - Automated diary entry generation
4. **AI Mentor** - Personalized concept explanations and guidance
5. **Interview Prep** - DSA and theory preparation assistance

## 🏗️ Development Status

Currently in Phase 1: Project Setup & Core Infrastructure

See [task.md](docs/task.md) for detailed progress.

## 📖 Documentation

- [Implementation Plan](docs/implementation_plan.md)
- [Architecture Overview](docs/architecture.md) (Coming soon)
- [API Documentation](docs/api.md) (Coming soon)

## 🔐 Environment Variables

Create `.env` files in both backend and frontend directories:

**Backend (.env)**:

```
DATABASE_URL=postgresql://user:password@localhost:5432/intern_ai
QDRANT_URL=http://localhost:6333
GEMINI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
CLAUDE_API_KEY=your_key_here
```

**Frontend (.env.local)**:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📄 License

Private project for personal use during VTU internship (Jan 2026 - Apr 2026).
