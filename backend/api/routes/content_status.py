"""
Content status endpoint.
"""
from fastapi import APIRouter
from api.models.schemas import ContentStatusResponse
import os
import httpx

router = APIRouter()


@router.get("/api/content-status", response_model=ContentStatusResponse)
async def get_content_status():
    """
    Get content indexing status.

    Returns:
        ContentStatusResponse with indexing metadata
    """
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_key = os.getenv("QDRANT_API_KEY")
    collection_name = "physical-ai-textbook"

    try:
        # Get collection info from Qdrant
        response = httpx.get(
            f"{qdrant_url}/collections/{collection_name}",
            headers={"Authorization": f"Bearer {qdrant_key}"},
            timeout=5.0
        )

        if response.status_code == 200:
            info = response.json()['result']
            total_chunks = info['points_count']
            indexing_complete = total_chunks > 0

            # For now, hardcode indexed modules
            # In production, this could be stored in database or config
            indexed_modules = ["module-0"] if total_chunks > 0 else []

            return ContentStatusResponse(
                last_updated="2026-02-12",
                content_version="v1.0.0",
                indexed_modules=indexed_modules,
                total_chunks=total_chunks,
                indexing_complete=indexing_complete
            )
        else:
            raise Exception(f"Failed to get collection info: HTTP {response.status_code}")

    except Exception as e:
        # Return default values if Qdrant is unavailable
        return ContentStatusResponse(
            last_updated="2026-02-12",
            content_version="v1.0.0",
            indexed_modules=[],
            total_chunks=0,
            indexing_complete=False
        )
