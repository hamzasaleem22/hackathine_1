"""
Context Boosting Service for User Story 2.

Implements context-aware search that prioritizes chunks matching selected text
while still searching the entire book.
"""
from typing import List, Dict, Any, Optional
from api.services.embedding import EmbeddingService
from api.services.qdrant_search import QdrantSearchService


class ContextBoostService:
    """Service for boosting search results based on selected text context."""

    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.search_service = QdrantSearchService()

    def search_with_context(
        self,
        question: str,
        context: str,
        top_k: int = 5,
        boost_factor: float = 2.0
    ) -> List[Dict[str, Any]]:
        """
        Search with context boosting.

        Algorithm:
        1. Embed the question
        2. Retrieve top-10 candidates from full index
        3. Apply 2x similarity boost to chunks that contain substring match with context
        4. Re-rank and return top-5

        Args:
            question: User's question
            context: Selected text context
            top_k: Number of results to return (default: 5)
            boost_factor: Multiplier for context matches (default: 2.0)

        Returns:
            List of search results with boosted scores
        """
        # Step 1: Get more candidates initially (top-10)
        initial_results = self.search_service.search(
            question=question,
            top_k=10,
            threshold=0.5  # Lower threshold to get more candidates
        )

        if not initial_results:
            return []

        # Step 2: Apply context boost
        boosted_results = []
        context_lower = context.lower() if context else ""

        for result in initial_results:
            chunk_text = result.get('chunk_text', '').lower()
            original_score = result.get('score', 0.0)

            # Check for context match (case-insensitive substring)
            has_context_match = self._has_context_match(chunk_text, context_lower)

            # Apply boost if match found
            if has_context_match:
                boosted_score = original_score * boost_factor
                result['score'] = boosted_score
                result['context_boost_applied'] = True
            else:
                result['context_boost_applied'] = False

            boosted_results.append(result)

        # Step 3: Re-rank by boosted scores
        boosted_results.sort(key=lambda x: x['score'], reverse=True)

        # Step 4: Return top-k
        return boosted_results[:top_k]

    def _has_context_match(self, chunk_text: str, context: str) -> bool:
        """
        Check if chunk contains context as a substring.

        Uses flexible matching:
        - Case-insensitive
        - Checks for significant phrases (>10 characters)
        - Can split context into phrases and check for any match

        Args:
            chunk_text: Text from the chunk (lowercase)
            context: Selected context (lowercase)

        Returns:
            True if match found, False otherwise
        """
        if not context or len(context) < 10:
            return False

        # Direct substring match
        if context in chunk_text:
            return True

        # Try matching significant phrases (>20 chars)
        if len(context) > 50:
            # Split context into sentences/phrases
            phrases = [p.strip() for p in context.split('.') if len(p.strip()) > 20]
            for phrase in phrases:
                if phrase in chunk_text:
                    return True

        return False

    def get_context_summary(self, context: str, max_length: int = 100) -> str:
        """
        Generate a summary of the context for display.

        Args:
            context: Full selected text
            max_length: Maximum length of summary

        Returns:
            Truncated context with ellipsis if needed
        """
        if not context:
            return ""

        if len(context) <= max_length:
            return context

        # Truncate and add ellipsis
        return context[:max_length].rsplit(' ', 1)[0] + "..."
