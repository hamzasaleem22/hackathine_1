"""
Pytest configuration and shared fixtures for backend tests.
"""
import os
import json
import pytest
from pathlib import Path
from typing import Dict, List
from unittest.mock import Mock, AsyncMock

# Set mock environment variables before any application imports
os.environ["OPENAI_API_KEY"] = "test-api-key"
os.environ["QDRANT_URL"] = "https://test-qdrant.example.com"
os.environ["QDRANT_API_KEY"] = "test-qdrant-key"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["ALLOWED_ORIGINS"] = "http://localhost:3000,https://test.example.com"

# Test fixtures directory
FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_questions() -> List[Dict]:
    """Load sample questions for testing."""
    with open(FIXTURES_DIR / "sample_questions.json", 'r') as f:
        data = json.load(f)
    return data['questions']


@pytest.fixture
def expected_answers() -> List[Dict]:
    """Load expected answers for validation."""
    with open(FIXTURES_DIR / "expected_answers.json", 'r') as f:
        data = json.load(f)
    return data['answers']


@pytest.fixture
def mock_embeddings() -> Dict[str, List[float]]:
    """Load pre-computed mock embeddings."""
    with open(FIXTURES_DIR / "mock_embeddings.json", 'r') as f:
        return json.load(f)


@pytest.fixture
def mock_openai_embedding_response():
    """Mock OpenAI embedding API response."""
    return {
        "object": "list",
        "data": [
            {
                "object": "embedding",
                "index": 0,
                "embedding": [0.1] * 1536
            }
        ],
        "model": "text-embedding-3-small",
        "usage": {
            "prompt_tokens": 10,
            "total_tokens": 10
        }
    }


@pytest.fixture
def mock_openai_completion_response():
    """Mock OpenAI completion API response."""
    return {
        "id": "chatcmpl-test",
        "object": "chat.completion",
        "created": 1234567890,
        "model": "gpt-4o-mini",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "This is a test answer based on the provided context."
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 50,
            "completion_tokens": 20,
            "total_tokens": 70
        }
    }


@pytest.fixture
def mock_qdrant_search_results():
    """Mock Qdrant search results."""
    return [
        {
            "id": "chunk-001",
            "score": 0.85,
            "payload": {
                "text": "Physical AI refers to artificial intelligence systems that interact with the physical world.",
                "heading": "Introduction to Physical AI",
                "module_id": "module-0",
                "chapter_id": "chapter-1",
                "section_id": "introduction",
                "navigation_url": "/docs/module-0/chapter-1#introduction",
                "file_path": "docs/module-0/chapter-1.mdx"
            }
        },
        {
            "id": "chunk-002",
            "score": 0.78,
            "payload": {
                "text": "These systems use sensors to perceive their environment and actuators to act upon it.",
                "heading": "Components of Physical AI",
                "module_id": "module-0",
                "chapter_id": "chapter-1",
                "section_id": "components",
                "navigation_url": "/docs/module-0/chapter-1#components",
                "file_path": "docs/module-0/chapter-1.mdx"
            }
        }
    ]


@pytest.fixture
def sample_query_request():
    """Sample query request for testing."""
    return {
        "question": "What is Physical AI?",
        "session_id": "test-session-123",
        "context": None
    }


@pytest.fixture
def sample_query_response():
    """Sample query response for testing."""
    return {
        "answer": "Physical AI refers to artificial intelligence systems that interact with the physical world through sensors and actuators.",
        "citations": [
            {
                "section": "Introduction to Physical AI",
                "url": "/docs/module-0/chapter-1#introduction",
                "score": 0.85,
                "module_id": "module-0",
                "chapter_id": "chapter-1"
            }
        ],
        "confidence": 0.85,
        "message_id": "msg-test-123",
        "response_time_ms": 1500
    }


@pytest.fixture
def mock_embedding_service():
    """Mock embedding service."""
    service = Mock()
    service.generate_embedding = Mock(return_value=[0.1] * 1536)
    service.generate_embeddings_batch = Mock(return_value=[[0.1] * 1536])
    return service


@pytest.fixture
def mock_qdrant_service():
    """Mock Qdrant search service."""
    service = Mock()
    service.search = Mock(return_value=[
        {
            "id": "test-chunk",
            "score": 0.85,
            "payload": {
                "text": "Test content",
                "heading": "Test Section",
                "module_id": "module-0",
                "navigation_url": "/test"
            }
        }
    ])
    return service


@pytest.fixture
def mock_completion_service():
    """Mock RAG completion service."""
    service = Mock()
    service.generate_with_retry = Mock(return_value={
        "answer": "Test answer",
        "model": "gpt-4o-mini",
        "response_time_ms": 1000,
        "tokens_used": 100
    })
    return service


@pytest.fixture
def test_database_url():
    """Test database URL (uses SQLite for testing)."""
    return "sqlite:///./test.db"


@pytest.fixture
async def async_client():
    """Async HTTP client for testing FastAPI endpoints."""
    from httpx import AsyncClient
    from api.main import app

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
