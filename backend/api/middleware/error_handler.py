"""
Error handling middleware for FastAPI application.

Catches all exceptions, logs them with structured logging, and returns
user-friendly JSON error responses.
"""
import logging
import traceback
from typing import Callable
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Configure structured logger
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s", "module": "%(name)s"}'
)
logger = logging.getLogger(__name__)


class ErrorHandlerMiddleware:
    """Middleware to catch and handle all exceptions"""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        try:
            await self.app(scope, receive, send)
        except Exception as exc:
            # Log the exception
            logger.error(
                f"Unhandled exception: {str(exc)}",
                extra={
                    "path": scope.get("path"),
                    "method": scope.get("method"),
                    "exception_type": type(exc).__name__,
                    "traceback": traceback.format_exc()
                }
            )

            # Create error response
            response = JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred. Please try again later.",
                    "request_id": scope.get("headers", {}).get("x-request-id", "unknown")
                }
            )

            await response(scope, receive, send)


# Exception handlers for specific error types
async def validation_error_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors (400 Bad Request)"""
    logger.warning(
        f"Validation error: {exc.errors()}",
        extra={"path": request.url.path, "method": request.method}
    )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Validation Error",
            "message": "The request data is invalid",
            "details": exc.errors()
        }
    )


async def rate_limit_error_handler(request: Request, exc: Exception):
    """Handle rate limit errors (429 Too Many Requests)"""
    logger.warning(
        f"Rate limit exceeded",
        extra={"path": request.url.path, "method": request.method, "ip": request.client.host}
    )

    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "error": "Rate Limit Exceeded",
            "message": "Too many requests. Please try again later.",
            "retry_after": 60  # seconds
        },
        headers={"Retry-After": "60"}
    )


async def openai_error_handler(request: Request, exc: Exception):
    """Handle OpenAI API errors (503 Service Unavailable)"""
    logger.error(
        f"OpenAI API error: {str(exc)}",
        extra={"path": request.url.path, "method": request.method}
    )

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": "AI Service Unavailable",
            "message": "The AI service is temporarily unavailable. Please try again in a few moments."
        },
        headers={"Retry-After": "30"}
    )


async def qdrant_error_handler(request: Request, exc: Exception):
    """Handle Qdrant vector database errors (503 Service Unavailable)"""
    logger.error(
        f"Qdrant error: {str(exc)}",
        extra={"path": request.url.path, "method": request.method}
    )

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": "Search Service Unavailable",
            "message": "The search service is temporarily unavailable. Please try again in a few moments."
        },
        headers={"Retry-After": "30"}
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions"""
    logger.warning(
        f"HTTP exception: {exc.status_code} - {exc.detail}",
        extra={"path": request.url.path, "method": request.method}
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "message": exc.detail
        }
    )


# Custom exception classes
class RateLimitError(Exception):
    """Raised when rate limit is exceeded"""
    pass


class OpenAIError(Exception):
    """Raised when OpenAI API fails"""
    pass


class QdrantError(Exception):
    """Raised when Qdrant operations fail"""
    pass
