"""
Unit tests for embedding service.

Tests embedding generation, batching, error handling, and edge cases.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from api.services.embedding import EmbeddingService


class TestEmbeddingService:
    """Test suite for EmbeddingService."""

    @pytest.fixture
    def embedding_service(self):
        """Create embedding service instance for testing."""
        with patch('api.services.embedding.OpenAI'):
            service = EmbeddingService()
            return service

    @pytest.fixture
    def mock_embedding_response(self):
        """Mock OpenAI embedding API response."""
        mock_response = Mock()
        mock_response.data = [
            Mock(embedding=[0.1] * 1536)
        ]
        return mock_response

    @pytest.fixture
    def mock_batch_embedding_response(self):
        """Mock OpenAI batch embedding API response."""
        mock_response = Mock()
        mock_response.data = [
            Mock(embedding=[0.1] * 1536),
            Mock(embedding=[0.2] * 1536),
            Mock(embedding=[0.3] * 1536),
        ]
        return mock_response

    def test_generate_embedding_success(self, embedding_service, mock_embedding_response):
        """Test successful single embedding generation."""
        # Arrange
        test_text = "What is reinforcement learning?"
        embedding_service.client.embeddings.create = Mock(return_value=mock_embedding_response)

        # Act
        result = embedding_service.generate_embedding(test_text)

        # Assert
        assert len(result) == 1536
        assert all(isinstance(x, float) for x in result)
        embedding_service.client.embeddings.create.assert_called_once_with(
            model="text-embedding-3-small",
            input=test_text
        )

    def test_generate_embedding_empty_text(self, embedding_service, mock_embedding_response):
        """Test embedding generation with empty text."""
        # Arrange
        embedding_service.client.embeddings.create = Mock(return_value=mock_embedding_response)

        # Act
        result = embedding_service.generate_embedding("")

        # Assert
        assert len(result) == 1536
        embedding_service.client.embeddings.create.assert_called_once()

    def test_generate_embedding_api_error(self, embedding_service):
        """Test handling of OpenAI API errors."""
        # Arrange
        embedding_service.client.embeddings.create = Mock(
            side_effect=Exception("API rate limit exceeded")
        )

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            embedding_service.generate_embedding("test text")

        assert "Failed to generate embedding" in str(exc_info.value)
        assert "API rate limit exceeded" in str(exc_info.value)

    def test_generate_embeddings_batch_success(self, embedding_service, mock_batch_embedding_response):
        """Test successful batch embedding generation."""
        # Arrange
        test_texts = [
            "What is reinforcement learning?",
            "Explain neural networks",
            "How do transformers work?"
        ]
        embedding_service.client.embeddings.create = Mock(return_value=mock_batch_embedding_response)

        # Act
        result = embedding_service.generate_embeddings_batch(test_texts)

        # Assert
        assert len(result) == 3
        assert all(len(emb) == 1536 for emb in result)
        assert all(isinstance(emb, list) for emb in result)
        embedding_service.client.embeddings.create.assert_called_once_with(
            model="text-embedding-3-small",
            input=test_texts
        )

    def test_generate_embeddings_batch_max_size(self, embedding_service):
        """Test batch size validation (max 100 texts)."""
        # Arrange
        test_texts = [f"Text {i}" for i in range(101)]

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            embedding_service.generate_embeddings_batch(test_texts)

        assert "Maximum 100 texts per batch" in str(exc_info.value)

    def test_generate_embeddings_batch_single_text(self, embedding_service, mock_embedding_response):
        """Test batch generation with single text."""
        # Arrange
        test_texts = ["Single text"]
        embedding_service.client.embeddings.create = Mock(return_value=mock_embedding_response)

        # Act
        result = embedding_service.generate_embeddings_batch(test_texts)

        # Assert
        assert len(result) == 1
        assert len(result[0]) == 1536

    def test_generate_embeddings_batch_api_error(self, embedding_service):
        """Test handling of API errors in batch generation."""
        # Arrange
        test_texts = ["Text 1", "Text 2"]
        embedding_service.client.embeddings.create = Mock(
            side_effect=Exception("Network timeout")
        )

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            embedding_service.generate_embeddings_batch(test_texts)

        assert "Failed to generate embeddings batch" in str(exc_info.value)
        assert "Network timeout" in str(exc_info.value)

    def test_model_configuration(self, embedding_service):
        """Test that service uses correct model and dimensions."""
        # Assert
        assert embedding_service.model == "text-embedding-3-small"
        assert embedding_service.dimensions == 1536

    def test_generate_embedding_long_text(self, embedding_service, mock_embedding_response):
        """Test embedding generation with very long text."""
        # Arrange
        long_text = "word " * 2000  # ~2000 words
        embedding_service.client.embeddings.create = Mock(return_value=mock_embedding_response)

        # Act
        result = embedding_service.generate_embedding(long_text)

        # Assert
        assert len(result) == 1536
        embedding_service.client.embeddings.create.assert_called_once()

    def test_generate_embedding_special_characters(self, embedding_service, mock_embedding_response):
        """Test embedding generation with special characters."""
        # Arrange
        special_text = "What is α + β = γ? And ∫∂Ω = ∮?"
        embedding_service.client.embeddings.create = Mock(return_value=mock_embedding_response)

        # Act
        result = embedding_service.generate_embedding(special_text)

        # Assert
        assert len(result) == 1536
        embedding_service.client.embeddings.create.assert_called_once_with(
            model="text-embedding-3-small",
            input=special_text
        )
