"""
Citation extraction and formatting service.
"""
from typing import List, Dict
from api.models.schemas import Citation


class CitationService:
    """Service for extracting and formatting citations from search results."""

    @staticmethod
    def extract_citations(search_results: List[Dict]) -> List[Citation]:
        """
        Extract citations from Qdrant search results.

        Args:
            search_results: List of search results from Qdrant

        Returns:
            List of Citation objects
        """
        citations = []

        for result in search_results:
            payload = result['payload']
            score = result['score']

            citation = Citation(
                section=payload.get('heading', 'Unknown Section'),
                url=payload.get('navigation_url', '#'),
                score=score,
                module_id=payload.get('module_id'),
                chapter_id=payload.get('chapter_id')
            )

            citations.append(citation)

        return citations

    @staticmethod
    def format_citations_text(citations: List[Citation]) -> str:
        """
        Format citations as readable text for display.

        Args:
            citations: List of Citation objects

        Returns:
            Formatted citation text
        """
        if not citations:
            return "No citations available"

        citation_lines = []
        for i, citation in enumerate(citations, 1):
            module_text = f"Module: {citation.module_id}" if citation.module_id else ""
            citation_lines.append(
                f"{i}. {citation.section} ({module_text}, Relevance: {citation.score:.2f})"
            )

        return "\n".join(citation_lines)

    @staticmethod
    def calculate_confidence(search_results: List[Dict]) -> float:
        """
        Calculate confidence score based on search results.

        Args:
            search_results: List of search results from Qdrant

        Returns:
            Confidence score (0-1)
        """
        if not search_results:
            return 0.0

        # Use average similarity score of top results as confidence
        scores = [result['score'] for result in search_results[:5]]
        confidence = sum(scores) / len(scores)

        return round(confidence, 2)
