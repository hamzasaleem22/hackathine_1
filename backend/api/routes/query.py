"""
Query endpoint for RAG chatbot.
"""
from fastapi import APIRouter, HTTPException
from api.models.schemas import QueryRequest, QueryResponse
from api.services.embedding import EmbeddingService
from api.services.qdrant_search import QdrantSearchService
from api.services.rag_prompt import (
    SYSTEM_PROMPT,
    build_user_prompt,
    detect_ambiguous_question,
    detect_broad_question,
    build_clarification_prompt,
    build_summary_response
)
from api.services.rag_completion import RAGCompletionService
from api.services.rag_citation import CitationService
import uuid
import time
import os
import psycopg
import json
from datetime import datetime

router = APIRouter()

# Initialize services
embedding_service = EmbeddingService()
search_service = QdrantSearchService()
completion_service = RAGCompletionService()
citation_service = CitationService()


@router.post("/api/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Process a RAG query and return an answer with citations.

    Args:
        request: QueryRequest with question, optional context, and session_id

    Returns:
        QueryResponse with answer, citations, and metadata

    Raises:
        HTTPException: If processing fails
    """
    start_time = time.time()

    try:
        # Validate question length
        if len(request.question) > 2000:
            raise HTTPException(
                status_code=400,
                detail="Question must be 2000 characters or less"
            )

        # Check for ambiguous questions
        if detect_ambiguous_question(request.question):
            return QueryResponse(
                answer=build_clarification_prompt(request.question),
                citations=[],
                confidence=0.0,
                message_id=str(uuid.uuid4()),
                response_time_ms=int((time.time() - start_time) * 1000)
            )

        # Generate query embedding
        query_embedding = embedding_service.generate_embedding(request.question)

        # Search Qdrant
        if request.context:
            # Use context boosting for selected text queries (US2)
            search_results = search_service.search_with_context_boost(
                query_vector=query_embedding,
                context_text=request.context,
                boost_factor=2.0,
                top_k=5
            )
        else:
            # Standard search
            search_results = search_service.search(
                query_vector=query_embedding,
                top_k=5,
                threshold=0.7
            )

        # Check for broad questions
        if detect_broad_question(request.question):
            return QueryResponse(
                answer=build_summary_response(request.question, search_results),
                citations=citation_service.extract_citations(search_results),
                confidence=0.5,
                message_id=str(uuid.uuid4()),
                response_time_ms=int((time.time() - start_time) * 1000)
            )

        # Handle no results
        if not search_results:
            return QueryResponse(
                answer="I couldn't find relevant information in the textbook to answer your question. Please try rephrasing or ask about a different topic.",
                citations=[],
                confidence=0.0,
                message_id=str(uuid.uuid4()),
                response_time_ms=int((time.time() - start_time) * 1000)
            )

        # Build RAG prompt with conversation history (T085)
        user_prompt = build_user_prompt(
            question=request.question,
            context_chunks=search_results,
            conversation_history=request.conversation_history
        )

        # Generate completion
        completion_result = completion_service.generate_with_retry(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt
        )

        # Extract citations
        citations = citation_service.extract_citations(search_results)

        # Calculate confidence
        confidence = citation_service.calculate_confidence(search_results)

        # Generate message ID for feedback
        message_id = str(uuid.uuid4())

        # Calculate total response time
        response_time_ms = int((time.time() - start_time) * 1000)

        # Create response
        response = QueryResponse(
            answer=completion_result['answer'],
            citations=citations,
            confidence=confidence,
            message_id=message_id,
            response_time_ms=response_time_ms
        )

        # Log to database (T074)
        try:
            database_url = os.getenv("DATABASE_URL")
            if database_url:
                with psycopg.connect(database_url) as conn:
                    with conn.cursor() as cur:
                        # Convert citations to JSON
                        citations_json = json.dumps([
                            {
                                'section': c.section,
                                'url': c.url,
                                'score': c.score,
                                'module_id': c.module_id,
                                'chapter_id': c.chapter_id
                            }
                            for c in citations
                        ])

                        cur.execute("""
                            INSERT INTO chat_messages
                            (message_id, session_id, question, answer, citations_json, response_time_ms, created_at)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (
                            message_id,
                            request.session_id or 'anonymous',
                            request.question,
                            response.answer,
                            citations_json,
                            response_time_ms,
                            datetime.utcnow()
                        ))
                        conn.commit()
        except Exception as e:
            # Log error but don't fail the request
            print(f"Failed to log query to database: {str(e)}")

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process query: {str(e)}"
        )
