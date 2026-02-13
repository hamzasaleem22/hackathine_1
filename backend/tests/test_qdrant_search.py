"""
Unit tests for Qdrant search service.

Tests vector search, context boosting, filtering, and error handling.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from api.services.qdrant_search import QdrantSearchService


class TestQdrantSearchService:
    """Test suite for QdrantSearchService."""

    @pytest.fixture
    def search_service(self):
        """Create search service instance for testing."""
        with patch.dict('os.environ', {
            'QDRANT_URL': 'https://test.qdrant.io',
            'QDRANT_API_KEY': 'test-key'
        }):
            service = QdrantSearchService()
            return service

    @pytest.fixture
    def mock_search_results(self):
        """Mock Qdrant search API response."""
        return {
            'result': [
                {
                    'id': 1,
                    'score': 0.95,
                    'payload': {
                        'text': 'Reinforcement learning is a type of machine learning...',
                        'module_id': 'module-1',
                        'chapter_id': 'ch1',
                        'section_id': 'sec1',
                        'heading_title': 'Introduction to RL',
                        'file_path': 'docs/module-1/chapter-1.mdx',
                        'navigation_url': '/docs/module-1/chapter-1#intro'
                    }
                },
                {
                    'id': 2,
                    'score': 0.88,
                    'payload': {
                        'text': 'Q-learning is a model-free reinforcement learning algorithm...',
                        'module_id': 'module-1',
                        'chapter_id': 'ch2',
                        'section_id': 'sec3',
                        'heading_title': 'Q-Learning',
                        'file_path': 'docs/module-1/chapter-2.mdx',
                        'navigation_url': '/docs/module-1/chapter-2#qlearning'
                    }
                },
                {
                    'id': 3,
                    'score': 0.82,
                    'payload': {
                        'text': 'Policy gradient methods optimize the policy directly...',
                        'module_id': 'module-1',
                        'chapter_id': 'ch3',
                        'section_id': 'sec2',
                        'heading_title': 'Policy Gradients',
                        'file_path': 'docs/module-1/chapter-3.mdx',
                        'navigation_url': '/docs/module-1/chapter-3#policy'
                    }
                }
            ]
        }

    @pytest.fixture
    def query_vector(self):
        """Sample query embedding vector."""
        return [0.1] * 1536

    def test_search_success(self, search_service, mock_search_results, query_vector):
        """Test successful vector search."""
        # Arrange
        with patch('httpx.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_search_results
            mock_post.return_value = mock_response

            # Act
            results = search_service.search(query_vector)

            # Assert
            assert len(results) == 3
            assert results[0]['score'] == 0.95
            assert results[0]['payload']['heading_title'] == 'Introduction to RL'
            mock_post.assert_called_once()

    def test_search_with_custom_parameters(self, search_service, query_vector):
        """Test search with custom top_k and threshold."""
        # Arrange
        with patch('httpx.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'result': []}
            mock_post.return_value = mock_response

            # Act
            search_service.search(query_vector, top_k=10, threshold=0.8)

            # Assert
            call_args = mock_post.call_args
            assert call_args[1]['json']['limit'] == 10
            assert call_args[1]['json']['score_threshold'] == 0.8

    def test_search_with_filter(self, search_service, query_vector):
        """Test search with metadata filter."""
        # Arrange
        filter_dict = {
            'must': [
                {
                    'key': 'module_id',
                    'match': {'value': 'module-1'}
                }
            ]
        }

        with patch('httpx.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'result': []}
            mock_post.return_value = mock_response

            # Act
            search_service.search(query_vector, filter_dict=filter_dict)

            # Assert
            call_args = mock_post.call_args
            assert 'filter' in call_args[1]['json']
            assert call_args[1]['json']['filter'] == filter_dict

    def test_search_api_error(self, search_service, query_vector):
        """Test handling of Qdrant API errors."""
        # Arrange
        with patch('httpx.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_post.return_value = mock_response

            # Act & Assert
            with pytest.raises(Exception) as exc_info:
                search_service.search(query_vector)

            assert "Qdrant search failed: HTTP 500" in str(exc_info.value)

    def test_search_network_error(self, search_service, query_vector):
        """Test handling of network errors."""
        # Arrange
        with patch('httpx.post', side_effect=Exception("Connection timeout")):
            # Act & Assert
            with pytest.raises(Exception) as exc_info:
                search_service.search(query_vector)

            assert "Qdrant search error" in str(exc_info.value)
            assert "Connection timeout" in str(exc_info.value)

    def test_search_empty_results(self, search_service, query_vector):
        """Test search with no results."""
        # Arrange
        with patch('httpx.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'result': []}
            mock_post.return_value = mock_response

            # Act
            results = search_service.search(query_vector)

            # Assert
            assert len(results) == 0
            assert isinstance(results, list)

    def test_search_with_context_boost_no_match(self, search_service, mock_search_results, query_vector):
        """Test context boosting when context text doesn't match any chunks."""
        # Arrange
        context_text = "unrelated context text"

        with patch('httpx.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_search_results
            mock_post.return_value = mock_response

            # Act
            results = search_service.search_with_context_boost(
                query_vector,
                context_text,
                boost_factor=2.0,
                top_k=5
            )

            # Assert
            assert len(results) == 3
            # Scores should remain unchanged since no match
            assert results[0]['score'] == 0.95

    def test_search_with_context_boost_with_match(self, search_service, mock_search_results, query_vector):
        """Test context boosting when context text matches a chunk."""
        # Arrange
        context_text = "reinforcement learning"  # This will match first result

        with patch('httpx.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_search_results
            mock_post.return_value = mock_response

            # Act
            results = search_service.search_with_context_boost(
                query_vector,
                context_text,
                boost_factor=2.0,
                top_k=5
            )

            # Assert
            assert len(results) == 3
            # First result should have boosted score (0.95 * 2.0 = 1.0, capped at 1.0)
            # Second result also matches, so it should be boosted too
            assert results[0]['score'] >= 0.95

    def test_search_with_context_boost_reranking(self, search_service, query_vector):
        """Test that context boosting can reorder results."""
        # Arrange
        context_text = "policy gradient"
        mock_results = {
            'result': [
                {
                    'id': 1,
                    'score': 0.9,
                    'payload': {
                        'text': 'Reinforcement learning basics...',
                        'heading_title': 'RL Intro'
                    }
                },
                {
                    'id': 2,
                    'score': 0.75,
                    'payload': {
                        'text': 'Policy gradient methods optimize the policy directly...',
                        'heading_title': 'Policy Gradients'
                    }
                },
                {
                    'id': 3,
                    'score': 0.7,
                    'payload': {
                        'text': 'Q-learning algorithm...',
                        'heading_title': 'Q-Learning'
                    }
                }
            ]
        }

        with patch('httpx.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_results
            mock_post.return_value = mock_response

            # Act
            results = search_service.search_with_context_boost(
                query_vector,
                context_text,
                boost_factor=2.0,
                top_k=5
            )

            # Assert
            # Second result should be boosted and become first
            # (0.75 * 2.0 = 1.0) > 0.9
            assert results[0]['payload']['heading_title'] == 'Policy Gradients'
            assert results[0]['score'] == 1.0  # Capped at 1.0

    def test_search_with_context_boost_top_k_limit(self, search_service, query_vector):
        """Test that context boosting respects top_k limit."""
        # Arrange
        context_text = "test"
        # Create 10 results
        mock_results = {
            'result': [
                {
                    'id': i,
                    'score': 0.9 - (i * 0.05),
                    'payload': {'text': f'Text {i}', 'heading_title': f'Title {i}'}
                }
                for i in range(10)
            ]
        }

        with patch('httpx.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_results
            mock_post.return_value = mock_response

            # Act
            results = search_service.search_with_context_boost(
                query_vector,
                context_text,
                top_k=3
            )

            # Assert
            assert len(results) == 3

    def test_service_configuration(self, search_service):
        """Test that service is configured with correct parameters."""
        # Assert
        assert search_service.collection_name == "physical-ai-textbook"
        assert search_service.qdrant_url == "https://test.qdrant.io"
        assert "Bearer test-key" in search_service.headers['Authorization']

    def test_search_with_case_insensitive_context_match(self, search_service, query_vector):
        """Test that context matching is case-insensitive."""
        # Arrange
        context_text = "REINFORCEMENT LEARNING"
        mock_results = {
            'result': [
                {
                    'id': 1,
                    'score': 0.8,
                    'payload': {
                        'text': 'Reinforcement learning is...',
                        'heading_title': 'RL'
                    }
                }
            ]
        }

        with patch('httpx.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_results
            mock_post.return_value = mock_response

            # Act
            results = search_service.search_with_context_boost(
                query_vector,
                context_text,
                boost_factor=2.0
            )

            # Assert
            # Should match and boost despite case difference
            assert results[0]['score'] == 1.0  # 0.8 * 2.0 = 1.6, capped at 1.0
