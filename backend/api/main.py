"""
FastAPI application entry point for RAG Chatbot backend.
"""
# CRITICAL: Load environment variables FIRST, before any app imports
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import os

# Import custom middleware and exception handlers
from api.middleware.error_handler import (
    validation_error_handler,
    rate_limit_error_handler,
    openai_error_handler,
    qdrant_error_handler,
    http_exception_handler,
    RateLimitError,
    OpenAIError,
    QdrantError
)
from api.middleware.rate_limit import RateLimitMiddleware

# Import routes (these will now have access to env vars)
from api.routes import health, content_status, query, feedback, report_issue

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="Retrieval-Augmented Generation chatbot for Physical AI Textbook",
    version="1.0.0"
)

# Note: Error handling is done via exception handlers below
# instead of middleware to avoid ASGI compatibility issues

# Register routers
app.include_router(health.router, tags=["health"])
app.include_router(content_status.router, tags=["content"])
app.include_router(query.router, tags=["query"])
app.include_router(feedback.router, tags=["feedback"])
app.include_router(report_issue.router, tags=["issues"])

# Add rate limiting middleware (20 requests per minute per IP)
app.add_middleware(RateLimitMiddleware, requests_per_minute=20)

# Get allowed origins from environment
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "status": "ok",
        "message": "RAG Chatbot API is running",
        "version": "1.0.0"
    }

# OPTIONS handler for CORS preflight
@app.options("/{full_path:path}")
async def options_handler():
    """Handle CORS preflight requests"""
    return {"status": "ok"}


# Register exception handlers
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(RateLimitError, rate_limit_error_handler)
app.add_exception_handler(OpenAIError, openai_error_handler)
app.add_exception_handler(QdrantError, qdrant_error_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
