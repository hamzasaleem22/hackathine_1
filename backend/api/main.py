"""
FastAPI application entry point for RAG Chatbot backend.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from dotenv import load_dotenv
import os

# Import custom middleware and exception handlers
from api.middleware.error_handler import (
    ErrorHandlerMiddleware,
    validation_error_handler,
    rate_limit_error_handler,
    openai_error_handler,
    qdrant_error_handler,
    http_exception_handler,
    RateLimitError,
    OpenAIError,
    QdrantError
)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="Retrieval-Augmented Generation chatbot for Physical AI Textbook",
    version="1.0.0"
)

# Add error handling middleware
app.middleware("http")(ErrorHandlerMiddleware(app))

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
