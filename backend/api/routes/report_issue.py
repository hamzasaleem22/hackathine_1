"""
Report Issue endpoint for User Story 3.

Allows users to report problems with chatbot responses (incorrect, incomplete, harmful).
"""
from fastapi import APIRouter, HTTPException
from api.models.schemas import ReportIssueRequest, ReportIssueResponse
import psycopg
import os
from datetime import datetime

router = APIRouter()


@router.post("/api/report-issue", response_model=ReportIssueResponse)
async def report_issue(request: ReportIssueRequest):
    """
    Report an issue with a chatbot response.

    Args:
        request: ReportIssueRequest with message_id, issue_type, and description

    Returns:
        ReportIssueResponse confirming submission

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

        # Determine severity based on issue type
        severity_map = {
            "incorrect": "medium",
            "incomplete": "low",
            "harmful": "high",
        }
        severity = severity_map.get(request.issue_type, "medium")

        # Connect to database
        with psycopg.connect(database_url) as conn:
            with conn.cursor() as cur:
                # Insert issue report
                cur.execute(
                    """
                    INSERT INTO issue_reports
                    (message_id, issue_type, description, severity, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        request.message_id,
                        request.issue_type,
                        request.description,
                        severity,
                        datetime.utcnow()
                    )
                )
                conn.commit()

        return ReportIssueResponse(
            success=True,
            message="Issue report submitted. We'll review it shortly."
        )

    except psycopg.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to submit issue report: {str(e)}"
        )
