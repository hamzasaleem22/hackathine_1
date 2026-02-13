"""
Pydantic models for request/response validation.
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime


# ====================================
# Request Models
# ====================================

class QueryRequest(BaseModel):
    """Request model for /api/query endpoint."""
    question: str = Field(..., min_length=1, max_length=2000, description="User's question")
    session_id: Optional[str] = Field(None, description="Session ID for conversation tracking")
    context: Optional[str] = Field(None, max_length=2000, description="Selected text context (for US2)")
    conversation_history: Optional[List[dict]] = Field(None, description="Previous Q&A pairs for context")

    @validator('question')
    def question_not_empty(cls, v):
        """Ensure question is not just whitespace."""
        if not v.strip():
            raise ValueError('Question cannot be empty')
        return v.strip()

    @validator('context')
    def context_length(cls, v):
        """Validate context length."""
        if v and len(v) > 2000:
            raise ValueError('Context must be 2000 characters or less')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is embodied intelligence?",
                "session_id": "abc123",
                "context": None
            }
        }


class FeedbackRequest(BaseModel):
    """Request model for /api/feedback endpoint."""
    message_id: str = Field(..., description="ID of the message being rated")
    rating: str = Field(..., pattern="^(up|down)$", description="Rating: 'up' or 'down'")

    class Config:
        json_schema_extra = {
            "example": {
                "message_id": "550e8400-e29b-41d4-a716-446655440000",
                "rating": "up"
            }
        }


class ReportIssueRequest(BaseModel):
    """Request model for /api/report-issue endpoint."""
    message_id: str = Field(..., description="ID of the message with an issue")
    issue_type: str = Field(..., pattern="^(incorrect|incomplete|harmful|other)$", description="Type of issue")
    description: Optional[str] = Field(None, max_length=1000, description="Detailed description of the issue")

    class Config:
        json_schema_extra = {
            "example": {
                "message_id": "550e8400-e29b-41d4-a716-446655440000",
                "issue_type": "incorrect",
                "description": "The answer contains outdated information"
            }
        }


# ====================================
# Response Models
# ====================================

class Citation(BaseModel):
    """Citation model for answer references."""
    section: str = Field(..., description="Section title")
    url: str = Field(..., description="Navigation URL to the section")
    score: float = Field(..., ge=0, le=1, description="Relevance score (0-1)")
    module_id: Optional[str] = Field(None, description="Module identifier")
    chapter_id: Optional[str] = Field(None, description="Chapter identifier")

    class Config:
        json_schema_extra = {
            "example": {
                "section": "Embodied Intelligence",
                "url": "/module-0/embodied-intelligence",
                "score": 0.85,
                "module_id": "module-0",
                "chapter_id": "ch-01"
            }
        }


class QueryResponse(BaseModel):
    """Response model for /api/query endpoint."""
    answer: str = Field(..., description="AI-generated answer")
    citations: List[Citation] = Field(..., description="List of source citations")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score (0-1)")
    message_id: str = Field(..., description="Unique message ID for feedback")
    response_time_ms: int = Field(..., description="Response time in milliseconds")

    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Embodied intelligence refers to...",
                "citations": [
                    {
                        "section": "Embodied Intelligence",
                        "url": "/module-0/embodied-intelligence",
                        "score": 0.85,
                        "module_id": "module-0",
                        "chapter_id": None
                    }
                ],
                "confidence": 0.9,
                "message_id": "550e8400-e29b-41d4-a716-446655440000",
                "response_time_ms": 2340
            }
        }


class HealthResponse(BaseModel):
    """Response model for /health endpoint."""
    status: str = Field(..., description="Overall health status")
    qdrant: str = Field(..., description="Qdrant connection status")
    database: str = Field(..., description="PostgreSQL connection status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Health check timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "qdrant": "connected",
                "database": "connected",
                "timestamp": "2026-02-12T10:30:00Z"
            }
        }


class ContentStatusResponse(BaseModel):
    """Response model for /api/content-status endpoint."""
    last_updated: str = Field(..., description="Last content update date (YYYY-MM-DD)")
    content_version: str = Field(..., description="Content version identifier")
    indexed_modules: List[str] = Field(..., description="List of indexed module IDs")
    total_chunks: int = Field(..., description="Total number of indexed chunks")
    indexing_complete: bool = Field(..., description="Whether indexing is complete")

    class Config:
        json_schema_extra = {
            "example": {
                "last_updated": "2026-02-12",
                "content_version": "v1.0.0",
                "indexed_modules": ["module-0"],
                "total_chunks": 141,
                "indexing_complete": True
            }
        }


class FeedbackResponse(BaseModel):
    """Response model for /api/feedback endpoint."""
    success: bool = Field(..., description="Whether feedback was recorded")
    message: str = Field(..., description="Success/error message")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Feedback recorded successfully"
            }
        }


class ReportIssueResponse(BaseModel):
    """Response model for /api/report-issue endpoint."""
    success: bool = Field(..., description="Whether issue was reported")
    issue_id: str = Field(..., description="Issue report ID")
    message: str = Field(..., description="Success/error message")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "issue_id": "550e8400-e29b-41d4-a716-446655440001",
                "message": "Issue reported successfully"
            }
        }
