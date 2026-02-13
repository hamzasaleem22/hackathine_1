"""
Vercel serverless function entry point for FastAPI.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.middleware.rate_limit import RateLimitMiddleware
import os

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="Retrieval-Augmented Generation chatbot for Physical AI Textbook",
    version="1.0.0"
)

# Add rate limiting middleware (20 requests per minute per IP)
app.add_middleware(RateLimitMiddleware, requests_per_minute=20)

# Get allowed origins from environment
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else ["*"]

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
