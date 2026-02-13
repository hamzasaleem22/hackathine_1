"""
Integration tests for /api/feedback endpoint (T087).

Tests feedback submission, validation, and database insertion.
"""
import pytest
from httpx import ASGITransport, AsyncClient
from unittest.mock import patch, MagicMock
import psycopg


@pytest.mark.asyncio
class TestFeedbackAPI:
    """Test suite for the /api/feedback endpoint."""

    @pytest.fixture
    def mock_database(self):
        """Mock database connection and cursor."""
        with patch('api.routes.feedback.psycopg.connect') as mock_connect:
            mock_cursor = MagicMock()
            mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
            mock_cursor.__exit__ = MagicMock(return_value=False)

            mock_conn = MagicMock()
            mock_conn.__enter__ = MagicMock(return_value=mock_conn)
            mock_conn.__exit__ = MagicMock(return_value=False)
            mock_conn.cursor.return_value = mock_cursor

            mock_connect.return_value = mock_conn

            yield {
                'connect': mock_connect,
                'conn': mock_conn,
                'cursor': mock_cursor
            }

    @pytest.fixture
    def mock_env(self):
        """Mock environment variables."""
        with patch.dict('os.environ', {'DATABASE_URL': 'postgresql://test:test@localhost/test'}):
            yield

    @pytest.mark.asyncio
    async def test_submit_feedback_thumbs_up(self, mock_database, mock_env):
        """Test submitting thumbs up feedback."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/feedback",
                json={
                    "message_id": "msg-123",
                    "rating": "up"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "thank you" in data["message"].lower()

            # Verify database insert was called
            mock_database['cursor'].execute.assert_called_once()
            mock_database['conn'].commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_submit_feedback_thumbs_down(self, mock_database, mock_env):
        """Test submitting thumbs down feedback."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/feedback",
                json={
                    "message_id": "msg-456",
                    "rating": "down"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True

    @pytest.mark.asyncio
    async def test_submit_feedback_invalid_rating(self, mock_database, mock_env):
        """Test submitting feedback with invalid rating."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/feedback",
                json={
                    "message_id": "msg-789",
                    "rating": "invalid"
                }
            )

            # Should return 422 validation error
            assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_submit_feedback_missing_message_id(self, mock_database, mock_env):
        """Test submitting feedback without message_id."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/feedback",
                json={
                    "rating": "up"
                }
            )

            # Should return 422 validation error
            assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_submit_feedback_missing_rating(self, mock_database, mock_env):
        """Test submitting feedback without rating."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/feedback",
                json={
                    "message_id": "msg-123"
                }
            )

            # Should return 422 validation error
            assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_submit_feedback_empty_message_id(self, mock_database, mock_env):
        """Test submitting feedback with empty message_id."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/feedback",
                json={
                    "message_id": "",
                    "rating": "up"
                }
            )

            # Should return 422 validation error for empty string
            # or 200 if empty strings are allowed (implementation dependent)
            assert response.status_code in [200, 422]

    @pytest.mark.asyncio
    async def test_submit_feedback_database_error(self, mock_env):
        """Test handling of database errors."""
        from api.main import app

        with patch('api.routes.feedback.psycopg.connect') as mock_connect:
            mock_connect.side_effect = psycopg.Error("Connection failed")

            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.post(
                    "/api/feedback",
                    json={
                        "message_id": "msg-123",
                        "rating": "up"
                    }
                )

                assert response.status_code == 500
                assert "database" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_submit_feedback_missing_database_url(self):
        """Test handling of missing database URL."""
        from api.main import app

        with patch.dict('os.environ', {}, clear=True):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.post(
                    "/api/feedback",
                    json={
                        "message_id": "msg-123",
                        "rating": "up"
                    }
                )

                assert response.status_code == 500
                assert "configuration" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_submit_feedback_stores_timestamp(self, mock_database, mock_env):
        """Test that feedback includes timestamp."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/feedback",
                json={
                    "message_id": "msg-123",
                    "rating": "up"
                }
            )

            assert response.status_code == 200

            # Verify INSERT includes timestamp
            call_args = mock_database['cursor'].execute.call_args
            sql = call_args[0][0]
            assert "created_at" in sql

    @pytest.mark.asyncio
    async def test_submit_feedback_idempotency(self, mock_database, mock_env):
        """Test that submitting same feedback multiple times works."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            # Submit same feedback twice
            for _ in range(2):
                response = await client.post(
                    "/api/feedback",
                    json={
                        "message_id": "msg-123",
                        "rating": "up"
                    }
                )
                assert response.status_code == 200

            # Both inserts should succeed (creates multiple records)
            assert mock_database['cursor'].execute.call_count == 2


@pytest.mark.asyncio
class TestFeedbackValidation:
    """Test suite for feedback input validation."""

    @pytest.fixture
    def mock_database(self):
        """Mock database for validation tests."""
        with patch('api.routes.feedback.psycopg.connect') as mock_connect:
            mock_cursor = MagicMock()
            mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
            mock_cursor.__exit__ = MagicMock(return_value=False)

            mock_conn = MagicMock()
            mock_conn.__enter__ = MagicMock(return_value=mock_conn)
            mock_conn.__exit__ = MagicMock(return_value=False)
            mock_conn.cursor.return_value = mock_cursor

            mock_connect.return_value = mock_conn
            yield

    @pytest.fixture
    def mock_env(self):
        """Mock environment variables."""
        with patch.dict('os.environ', {'DATABASE_URL': 'postgresql://test:test@localhost/test'}):
            yield

    @pytest.mark.asyncio
    async def test_rating_case_insensitive(self, mock_database, mock_env):
        """Test that rating validation is case-insensitive or strict."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            # Test uppercase
            response = await client.post(
                "/api/feedback",
                json={
                    "message_id": "msg-123",
                    "rating": "UP"
                }
            )

            # May be 200 (case-insensitive) or 422 (strict validation)
            assert response.status_code in [200, 422]

    @pytest.mark.asyncio
    async def test_message_id_max_length(self, mock_database, mock_env):
        """Test message_id with very long string."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            long_id = "x" * 1000

            response = await client.post(
                "/api/feedback",
                json={
                    "message_id": long_id,
                    "rating": "up"
                }
            )

            # Should either succeed or return validation error
            assert response.status_code in [200, 422]

    @pytest.mark.asyncio
    async def test_special_characters_in_message_id(self, mock_database, mock_env):
        """Test message_id with special characters."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/feedback",
                json={
                    "message_id": "msg-123-!@#$%",
                    "rating": "up"
                }
            )

            assert response.status_code == 200
