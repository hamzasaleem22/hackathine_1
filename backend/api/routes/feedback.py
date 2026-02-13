"""
Feedback endpoint for User Story 3.

Allows users to provide thumbs up/down feedback on chatbot responses.
"""
from fastapi import APIRouter, HTTPException
from api.models.schemas import FeedbackRequest, FeedbackResponse
import psycopg
import os
from datetime import datetime

router = APIRouter()


@router.post("/api/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest):
    """
    Submit feedback (thumbs up/down) for a chatbot response.

    Args:
        request: FeedbackRequest with message_id and rating

    Returns:
        FeedbackResponse confirming submission

    Raises:
        HTTPException: If database operation fails
    """
    try:
        # Get database URL
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise HTTPException(
                status_code=500,
                detail="Database configuration missing"
            )

        # Connect to database
        with psycopg.connect(database_url) as conn:
            with conn.cursor() as cur:
                # Insert feedback
                cur.execute(
                    """
                    INSERT INTO feedback_events (message_id, rating, created_at)
                    VALUES (%s, %s, %s)
                    """,
                    (request.message_id, request.rating, datetime.utcnow())
                )
                conn.commit()

        return FeedbackResponse(
            success=True,
            message="Feedback received. Thank you!"
        )

    except psycopg.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to submit feedback: {str(e)}"
        )
