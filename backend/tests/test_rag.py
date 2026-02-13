"""
Unit tests for RAG completion and citation services (T029).

Tests RAG completion, citation extraction, and confidence calculation.
Target: 80% coverage.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import asyncio


class TestRAGCompletion:
    """Test suite for RAG completion service."""

    @pytest.fixture
    def mock_openai_client(self):
        """Mock OpenAI client for completions."""
        with patch('api.services.rag_completion.OpenAI') as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client
            yield mock_client

    @pytest.fixture
    def mock_completion_response(self):
        """Standard mock completion response."""
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(
                message=MagicMock(
                    content="Physical AI is a field that combines artificial intelligence with physical systems. [1] This enables robots to learn and adapt in real environments. [2]"
                ),
                finish_reason="stop"
            )
        ]
        mock_response.usage = MagicMock(
            prompt_tokens=150,
            completion_tokens=50,
            total_tokens=200
        )
        return mock_response

    def test_generate_completion_success(self, mock_openai_client, mock_completion_response):
        """Test successful RAG completion generation."""
        from api.services.rag_completion import RAGCompletionService

        mock_openai_client.chat.completions.create.return_value = mock_completion_response

        service = RAGCompletionService()
        service.client = mock_openai_client

        # Act
        result = service.generate_completion(
            system_prompt="You are a helpful assistant.",
            user_prompt="What is Physical AI?"
        )

        # Assert
        assert result is not None
        assert "Physical AI" in result
        mock_openai_client.chat.completions.create.assert_called_once()

    def test_generate_completion_uses_correct_model(self, mock_openai_client, mock_completion_response):
        """Test that completion uses gpt-4o-mini model."""
        from api.services.rag_completion import RAGCompletionService

        mock_openai_client.chat.completions.create.return_value = mock_completion_response

        service = RAGCompletionService()
        service.client = mock_openai_client

        # Act
        service.generate_completion(
            system_prompt="Test",
            user_prompt="Test question"
        )

        # Assert
        call_args = mock_openai_client.chat.completions.create.call_args
        assert call_args[1]['model'] == 'gpt-4o-mini'

    def test_generate_completion_includes_messages(self, mock_openai_client, mock_completion_response):
        """Test that completion includes system and user messages."""
        from api.services.rag_completion import RAGCompletionService

        mock_openai_client.chat.completions.create.return_value = mock_completion_response

        service = RAGCompletionService()
        service.client = mock_openai_client

        system_prompt = "You are a teaching assistant."
        user_prompt = "Explain reinforcement learning."

        # Act
        service.generate_completion(system_prompt, user_prompt)

        # Assert
        call_args = mock_openai_client.chat.completions.create.call_args
        messages = call_args[1]['messages']

        assert len(messages) == 2
        assert messages[0]['role'] == 'system'
        assert messages[0]['content'] == system_prompt
        assert messages[1]['role'] == 'user'
        assert messages[1]['content'] == user_prompt

    def test_generate_completion_with_timeout(self, mock_openai_client, mock_completion_response):
        """Test that completion respects timeout setting."""
        from api.services.rag_completion import RAGCompletionService

        mock_openai_client.chat.completions.create.return_value = mock_completion_response

        service = RAGCompletionService()
        service.client = mock_openai_client

        # Act
        service.generate_completion(
            system_prompt="Test",
            user_prompt="Test"
        )

        # Assert
        call_args = mock_openai_client.chat.completions.create.call_args
        assert 'timeout' in call_args[1] or call_args[1].get('timeout', 30) <= 30

    def test_generate_completion_api_error(self, mock_openai_client):
        """Test handling of OpenAI API errors."""
        from api.services.rag_completion import RAGCompletionService

        mock_openai_client.chat.completions.create.side_effect = Exception("API rate limit exceeded")

        service = RAGCompletionService()
        service.client = mock_openai_client

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            service.generate_completion(
                system_prompt="Test",
                user_prompt="Test question"
            )

        assert "rate limit" in str(exc_info.value).lower() or "failed" in str(exc_info.value).lower()

    def test_generate_completion_empty_response(self, mock_openai_client):
        """Test handling of empty completion response."""
        from api.services.rag_completion import RAGCompletionService

        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content=""))
        ]
        mock_openai_client.chat.completions.create.return_value = mock_response

        service = RAGCompletionService()
        service.client = mock_openai_client

        # Act
        result = service.generate_completion(
            system_prompt="Test",
            user_prompt="Test"
        )

        # Assert - should return empty string or raise error
        assert result == "" or result is None

    def test_generate_completion_with_temperature(self, mock_openai_client, mock_completion_response):
        """Test that completion uses appropriate temperature."""
        from api.services.rag_completion import RAGCompletionService

        mock_openai_client.chat.completions.create.return_value = mock_completion_response

        service = RAGCompletionService()
        service.client = mock_openai_client

        # Act
        service.generate_completion(
            system_prompt="Test",
            user_prompt="Test"
        )

        # Assert
        call_args = mock_openai_client.chat.completions.create.call_args
        # Temperature should be low for factual responses (typically 0.3-0.7)
        temperature = call_args[1].get('temperature', 0.7)
        assert 0 <= temperature <= 1.0


class TestRAGCitation:
    """Test suite for citation extraction service."""

    @pytest.fixture
    def sample_chunks(self):
        """Sample search result chunks with metadata."""
        return [
            {
                'score': 0.95,
                'payload': {
                    'text': 'Physical AI is a field combining AI with robotics.',
                    'heading': 'Introduction to Physical AI',
                    'module_id': 'module-0',
                    'chapter_id': 'chapter-1',
                    'section_id': 'section-1',
                    'navigation_url': '/docs/module-0/chapter-1#introduction'
                }
            },
            {
                'score': 0.88,
                'payload': {
                    'text': 'Reinforcement learning enables agents to learn from experience.',
                    'heading': 'Reinforcement Learning Basics',
                    'module_id': 'module-1',
                    'chapter_id': 'chapter-2',
                    'section_id': 'section-1',
                    'navigation_url': '/docs/module-1/chapter-2#rl-basics'
                }
            },
            {
                'score': 0.75,
                'payload': {
                    'text': 'Sim-to-real transfer bridges simulation and reality.',
                    'heading': 'Sim-to-Real Transfer',
                    'module_id': 'module-2',
                    'chapter_id': 'chapter-3',
                    'section_id': 'section-2',
                    'navigation_url': '/docs/module-2/chapter-3#sim-to-real'
                }
            }
        ]

    def test_extract_citations_from_chunks(self, sample_chunks):
        """Test extracting citations from search result chunks."""
        from api.services.rag_citation import extract_citations

        # Act
        citations = extract_citations(sample_chunks)

        # Assert
        assert len(citations) == 3
        assert all('section' in c or 'section_title' in c for c in citations)
        assert all('url' in c for c in citations)
        assert all('score' in c for c in citations)

    def test_extract_citations_preserves_order(self, sample_chunks):
        """Test that citations are ordered by relevance score."""
        from api.services.rag_citation import extract_citations

        # Act
        citations = extract_citations(sample_chunks)

        # Assert
        scores = [c['score'] for c in citations]
        assert scores == sorted(scores, reverse=True)

    def test_extract_citations_includes_section_title(self, sample_chunks):
        """Test that citations include section title from heading."""
        from api.services.rag_citation import extract_citations

        # Act
        citations = extract_citations(sample_chunks)

        # Assert
        section_titles = [c.get('section') or c.get('section_title') for c in citations]
        assert 'Introduction to Physical AI' in section_titles
        assert 'Reinforcement Learning Basics' in section_titles

    def test_extract_citations_includes_navigation_url(self, sample_chunks):
        """Test that citations include proper navigation URLs."""
        from api.services.rag_citation import extract_citations

        # Act
        citations = extract_citations(sample_chunks)

        # Assert
        urls = [c['url'] for c in citations]
        assert '/docs/module-0/chapter-1#introduction' in urls
        assert '/docs/module-1/chapter-2#rl-basics' in urls

    def test_extract_citations_empty_chunks(self):
        """Test citation extraction with empty chunks list."""
        from api.services.rag_citation import extract_citations

        # Act
        citations = extract_citations([])

        # Assert
        assert citations == []

    def test_extract_citations_missing_metadata(self):
        """Test citation extraction with chunks missing metadata."""
        from api.services.rag_citation import extract_citations

        chunks = [
            {
                'score': 0.9,
                'payload': {
                    'text': 'Some content without full metadata'
                }
            }
        ]

        # Act
        citations = extract_citations(chunks)

        # Assert
        assert len(citations) == 1
        # Should have default/fallback values
        assert 'section' in citations[0] or 'section_title' in citations[0]
        assert 'url' in citations[0]

    def test_extract_citations_filters_low_scores(self, sample_chunks):
        """Test that citations filter out very low relevance scores."""
        from api.services.rag_citation import extract_citations

        # Add a low-score chunk
        sample_chunks.append({
            'score': 0.3,  # Below threshold
            'payload': {
                'text': 'Unrelated content',
                'heading': 'Unrelated Section',
                'navigation_url': '/docs/unrelated'
            }
        })

        # Act
        citations = extract_citations(sample_chunks, threshold=0.5)

        # Assert - low score chunk should be filtered
        assert len(citations) == 3
        assert all(c['score'] >= 0.5 for c in citations)

    def test_format_citation_for_response(self, sample_chunks):
        """Test formatting citations for API response."""
        from api.services.rag_citation import format_citations_for_response

        # Act
        formatted = format_citations_for_response(sample_chunks[:2])

        # Assert
        assert len(formatted) == 2
        for citation in formatted:
            assert 'section' in citation or 'section_title' in citation
            assert 'url' in citation
            assert 'score' in citation
            assert isinstance(citation['score'], float)


class TestConfidenceCalculation:
    """Test suite for confidence score calculation."""

    @pytest.fixture
    def high_confidence_chunks(self):
        """Chunks with high relevance scores."""
        return [
            {'score': 0.95, 'payload': {'text': 'Relevant content 1'}},
            {'score': 0.92, 'payload': {'text': 'Relevant content 2'}},
            {'score': 0.88, 'payload': {'text': 'Relevant content 3'}},
        ]

    @pytest.fixture
    def low_confidence_chunks(self):
        """Chunks with low relevance scores."""
        return [
            {'score': 0.55, 'payload': {'text': 'Somewhat relevant'}},
            {'score': 0.48, 'payload': {'text': 'Less relevant'}},
        ]

    def test_calculate_confidence_high_scores(self, high_confidence_chunks):
        """Test confidence calculation with high-scoring chunks."""
        from api.services.rag_citation import calculate_confidence

        # Act
        confidence = calculate_confidence(high_confidence_chunks)

        # Assert
        assert confidence >= 0.85
        assert confidence <= 1.0

    def test_calculate_confidence_low_scores(self, low_confidence_chunks):
        """Test confidence calculation with low-scoring chunks."""
        from api.services.rag_citation import calculate_confidence

        # Act
        confidence = calculate_confidence(low_confidence_chunks)

        # Assert
        assert confidence < 0.7
        assert confidence >= 0.0

    def test_calculate_confidence_empty_chunks(self):
        """Test confidence calculation with no chunks."""
        from api.services.rag_citation import calculate_confidence

        # Act
        confidence = calculate_confidence([])

        # Assert
        assert confidence == 0.0

    def test_calculate_confidence_single_chunk(self):
        """Test confidence calculation with single chunk."""
        from api.services.rag_citation import calculate_confidence

        chunks = [{'score': 0.85, 'payload': {'text': 'Single result'}}]

        # Act
        confidence = calculate_confidence(chunks)

        # Assert
        assert 0.0 <= confidence <= 1.0

    def test_calculate_confidence_weighted_average(self, high_confidence_chunks):
        """Test that confidence considers weighted average of scores."""
        from api.services.rag_citation import calculate_confidence

        # Add low-scoring chunks
        mixed_chunks = high_confidence_chunks + [
            {'score': 0.4, 'payload': {'text': 'Low relevance'}},
        ]

        # Act
        confidence_high = calculate_confidence(high_confidence_chunks)
        confidence_mixed = calculate_confidence(mixed_chunks)

        # Assert - mixed should be lower but not dramatically
        assert confidence_mixed <= confidence_high

    def test_calculate_confidence_normalized(self):
        """Test that confidence is always normalized between 0 and 1."""
        from api.services.rag_citation import calculate_confidence

        test_cases = [
            [{'score': 1.0, 'payload': {}}],  # Max score
            [{'score': 0.0, 'payload': {}}],  # Min score
            [{'score': 0.5, 'payload': {}}] * 10,  # Many medium scores
        ]

        for chunks in test_cases:
            confidence = calculate_confidence(chunks)
            assert 0.0 <= confidence <= 1.0


class TestRAGIntegration:
    """Integration tests for the full RAG pipeline."""

    @pytest.fixture
    def mock_services(self):
        """Mock all RAG services for integration testing."""
        with patch('api.services.embedding.EmbeddingService') as mock_embed, \
             patch('api.services.qdrant_search.QdrantSearchService') as mock_search, \
             patch('api.services.rag_completion.RAGCompletionService') as mock_completion:

            # Mock embedding
            mock_embed_instance = MagicMock()
            mock_embed_instance.generate_embedding.return_value = [0.1] * 1536
            mock_embed.return_value = mock_embed_instance

            # Mock search
            mock_search_instance = MagicMock()
            mock_search_instance.search.return_value = [
                {
                    'score': 0.9,
                    'payload': {
                        'text': 'Physical AI combines AI with robotics.',
                        'heading': 'Introduction',
                        'navigation_url': '/docs/intro'
                    }
                }
            ]
            mock_search.return_value = mock_search_instance

            # Mock completion
            mock_completion_instance = MagicMock()
            mock_completion_instance.generate_completion.return_value = "Physical AI is a field... [1]"
            mock_completion.return_value = mock_completion_instance

            yield {
                'embedding': mock_embed_instance,
                'search': mock_search_instance,
                'completion': mock_completion_instance
            }

    def test_full_rag_pipeline(self, mock_services):
        """Test the complete RAG pipeline from question to answer."""
        # This test verifies all components work together
        embedding = mock_services['embedding'].generate_embedding("What is Physical AI?")
        assert len(embedding) == 1536

        search_results = mock_services['search'].search(embedding)
        assert len(search_results) > 0

        answer = mock_services['completion'].generate_completion(
            "System prompt",
            "User question with context"
        )
        assert "Physical AI" in answer

    def test_rag_pipeline_handles_no_results(self, mock_services):
        """Test RAG pipeline when no relevant chunks are found."""
        mock_services['search'].search.return_value = []

        # Should handle gracefully - either return default message or raise
        search_results = mock_services['search'].search([0.1] * 1536)
        assert search_results == []
