"""
Qdrant vector search service.
"""
import os
import httpx
from typing import List, Dict, Optional


class QdrantSearchService:
    """Service for semantic search using Qdrant vector database."""

    def __init__(self):
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_key = os.getenv("QDRANT_API_KEY")
        self.collection_name = "physical-ai-textbook"
        self.headers = {"Authorization": f"Bearer {self.qdrant_key}"}

    def search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        threshold: float = 0.7,
        filter_dict: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search for similar vectors in Qdrant.

        Args:
            query_vector: The query embedding vector
            top_k: Number of results to return (default: 5)
            threshold: Minimum similarity score (default: 0.7)
            filter_dict: Optional filter conditions

        Returns:
            List of search results with payload and score

        Raises:
            Exception: If Qdrant API call fails
        """
        try:
            search_payload = {
                "vector": query_vector,
                "limit": top_k,
                "with_payload": True,
                "score_threshold": threshold
            }

            if filter_dict:
                search_payload["filter"] = filter_dict

            response = httpx.post(
                f"{self.qdrant_url}/collections/{self.collection_name}/points/search",
                json=search_payload,
                headers=self.headers,
                timeout=10.0
            )

            if response.status_code == 200:
                results = response.json()['result']
                return results
            else:
                raise Exception(f"Qdrant search failed: HTTP {response.status_code}")

        except Exception as e:
            raise Exception(f"Qdrant search error: {str(e)}")

    def search_with_context_boost(
        self,
        query_vector: List[float],
        context_text: str,
        boost_factor: float = 2.0,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Search with context boosting for selected text queries (US2).

        Args:
            query_vector: The query embedding vector
            context_text: Selected text for context
            boost_factor: Similarity boost for matching chunks (default: 2.0)
            top_k: Number of final results (default: 5)

        Returns:
            List of search results with boosted scores
        """
        # Retrieve more candidates for re-ranking
        candidates = self.search(query_vector, top_k=10, threshold=0.6)

        # Re-rank with context boost
        for result in candidates:
            chunk_text = result['payload'].get('text', '')

            # Check if context substring exists in chunk
            if context_text.lower() in chunk_text.lower():
                result['score'] = min(result['score'] * boost_factor, 1.0)

        # Sort by boosted score and return top_k
        candidates.sort(key=lambda x: x['score'], reverse=True)
        return candidates[:top_k]
