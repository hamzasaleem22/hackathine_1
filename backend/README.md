# RAG Chatbot Backend

Backend API for the Physical AI Textbook RAG Chatbot.

## Tech Stack

- **Framework**: FastAPI 0.109.0
- **Python**: 3.10+
- **Vector Database**: Qdrant Cloud
- **Relational Database**: Neon Serverless Postgres
- **AI**: OpenAI GPT-4o-mini + text-embedding-3-small

## Project Structure

```
backend/
├── api/
│   ├── main.py              # FastAPI app entry point
│   ├── routes/              # API endpoints
│   ├── services/            # Business logic
│   ├── models/              # Pydantic models
│   └── middleware/          # Custom middleware
├── scripts/                 # Indexing and utility scripts
├── tests/                   # Test suite
├── db/                      # Database schemas and migrations
├── alembic/                 # Alembic migrations
├── requirements.txt         # Python dependencies
└── .env.example            # Environment variables template
```

## Setup

1. Create virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Run development server:
```bash
uvicorn api.main:app --reload
```

## API Endpoints

### Core Endpoints
- `GET /` - Health check
- `GET /health` - System health status
- `POST /api/query` - RAG query endpoint
- `GET /api/content-status` - Content indexing status
- `POST /api/feedback` - Submit feedback
- `POST /api/report-issue` - Report issues

### Admin Endpoints
- `POST /api/cache/clear` - Clear query cache
- `GET /api/metrics` - Performance metrics

## Testing

Run tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=api --cov-report=html
```

## Environment Variables

See `.env.example` for required configuration.

## Deployment

This backend is deployed to Vercel Serverless Functions.

See [deployment guide](../docs/DEPLOYMENT.md) for details.
