"""
Health check endpoint.
"""
from fastapi import APIRouter, HTTPException
from api.models.schemas import HealthResponse
import os
import httpx
import psycopg
from datetime import datetime

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint that verifies Qdrant and PostgreSQL connections.

    Returns:
        HealthResponse with connection status for all services
    """
    qdrant_status = "unknown"
    db_status = "unknown"

    # Check Qdrant
    try:
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_key = os.getenv("QDRANT_API_KEY")

        response = httpx.get(
            f"{qdrant_url}/collections/physical-ai-textbook",
            headers={"Authorization": f"Bearer {qdrant_key}"},
            timeout=5.0
        )

        if response.status_code == 200:
            qdrant_status = "connected"
        else:
            qdrant_status = f"error: HTTP {response.status_code}"

    except Exception as e:
        qdrant_status = f"error: {str(e)[:50]}"

    # Check PostgreSQL
    try:
        db_url = os.getenv("DATABASE_URL")

        with psycopg.connect(db_url, connect_timeout=5) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
                db_status = "connected"

    except Exception as e:
        db_status = f"error: {str(e)[:50]}"

    # Determine overall status
    overall_status = "healthy" if (qdrant_status == "connected" and db_status == "connected") else "degraded"

    return HealthResponse(
        status=overall_status,
        qdrant=qdrant_status,
        database=db_status,
        timestamp=datetime.utcnow()
    )
