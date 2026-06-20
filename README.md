# DB-GPT: Local AI Data Assistant

Connect databases or upload CSV/Excel files, ask questions in plain English, and get instant analysis with charts, summaries, and shareable reports.

## Architecture

- **Frontend**: Next.js 15 (App Router) + TypeScript + shadcn/ui + Recharts
- **Backend**: FastAPI + SQLAlchemy 2.0 (async) + PostgreSQL
- **AI**: Google Gemini + Ollama (local LLMs) via LangChain

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL 16 (or Docker)

### 1. Clone & Setup

```bash
git clone <repo-url> db-gpt
cd db-gpt
```

### 2. Environment Variables

```bash
cp .env.example .env
# Edit .env with your API keys:
# - GEMINI_API_KEY: Get from https://aistudio.google.com/apikey
# - OLLAMA_BASE_URL: http://localhost:11434 (if using local Ollama)
```

### 3. Start PostgreSQL

```bash
docker compose up -d db
```

Or use a local PostgreSQL instance and update `DATABASE_URL` in `.env`.

### 4. Backend

```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### 5. Frontend

```bash
cd frontend
npm install
npm run dev
```

### 6. Open

Visit **http://localhost:3000** and register with your email.

Default seed credentials (if seeded):
- Email: `mzoraofficila@gmail.com`
- Password: `zabi12345`

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://postgres:postgres@localhost:5432/dbgpt` |
| `SECRET_KEY` | JWT signing key | (required) |
| `GEMINI_API_KEY` | Google Gemini API key | (optional) |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | Ollama model name | `llama3.2` |

## Features

- **Natural Language Queries**: Ask questions in English → AI generates SQL or Python
- **Multi-Source Data**: Connect PostgreSQL, MySQL, SQLite, MSSQL or upload CSV/Excel
- **Charts & Visualizations**: Bar, line, pie, scatter charts — interactive
- **Dashboards**: Drag-and-drop widget grid to create custom dashboards
- **HTML Reports**: Export analysis as shareable HTML reports with embedded charts
- **Reusable Skills**: Save analysis patterns as skills with parameters
- **AI Planning**: Complex questions are broken into steps automatically
- **Safe Execution**: SQL is read-only validated; Python runs in a sandbox
- **Multi-Model**: Use Gemini (cloud) or Ollama (local) — switch per chat
