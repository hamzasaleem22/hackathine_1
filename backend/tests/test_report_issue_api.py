"""
Integration tests for /api/report-issue endpoint (T088).

Tests issue reporting, validation, severity mapping, and database logging.
"""
import pytest
from httpx import ASGITransport, AsyncClient
from unittest.mock import patch, MagicMock
import psycopg


@pytest.mark.asyncio
class TestReportIssueAPI:
    """Test suite for the /api/report-issue endpoint."""

    @pytest.fixture
    def mock_database(self):
        """Mock database connection and cursor."""
        with patch('api.routes.report_issue.psycopg.connect') as mock_connect:
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
    async def test_report_incorrect_issue(self, mock_database, mock_env):
        """Test reporting an incorrect answer issue."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/report-issue",
                json={
                    "message_id": "msg-123",
                    "issue_type": "incorrect",
                    "description": "The answer stated X but the correct answer is Y."
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "submitted" in data["message"].lower()

            # Verify database insert
            mock_database['cursor'].execute.assert_called_once()
            mock_database['conn'].commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_report_incomplete_issue(self, mock_database, mock_env):
        """Test reporting an incomplete answer issue."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/report-issue",
                json={
                    "message_id": "msg-456",
                    "issue_type": "incomplete",
                    "description": "The answer only covered part of the topic."
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True

    @pytest.mark.asyncio
    async def test_report_harmful_issue(self, mock_database, mock_env):
        """Test reporting a harmful content issue."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/report-issue",
                json={
                    "message_id": "msg-789",
                    "issue_type": "harmful",
                    "description": "The answer contained inappropriate content."
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True

    @pytest.mark.asyncio
    async def test_severity_mapping_incorrect(self, mock_database, mock_env):
        """Test that 'incorrect' issues are mapped to 'medium' severity."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/report-issue",
                json={
                    "message_id": "msg-123",
                    "issue_type": "incorrect",
                    "description": "Test description"
                }
            )

            assert response.status_code == 200

            # Check severity in INSERT statement
            call_args = mock_database['cursor'].execute.call_args
            params = call_args[0][1]
            assert "medium" in params

    @pytest.mark.asyncio
    async def test_severity_mapping_incomplete(self, mock_database, mock_env):
        """Test that 'incomplete' issues are mapped to 'low' severity."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/report-issue",
                json={
                    "message_id": "msg-123",
                    "issue_type": "incomplete",
                    "description": "Test description"
                }
            )

            assert response.status_code == 200

            call_args = mock_database['cursor'].execute.call_args
            params = call_args[0][1]
            assert "low" in params

    @pytest.mark.asyncio
    async def test_severity_mapping_harmful(self, mock_database, mock_env):
        """Test that 'harmful' issues are mapped to 'high' severity."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/report-issue",
                json={
                    "message_id": "msg-123",
                    "issue_type": "harmful",
                    "description": "Test description"
                }
            )

            assert response.status_code == 200

            call_args = mock_database['cursor'].execute.call_args
            params = call_args[0][1]
            assert "high" in params

    @pytest.mark.asyncio
    async def test_invalid_issue_type(self, mock_database, mock_env):
        """Test submitting an invalid issue type."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/report-issue",
                json={
                    "message_id": "msg-123",
                    "issue_type": "invalid_type",
                    "description": "Test"
                }
            )

            # Should return 422 validation error
            assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_missing_message_id(self, mock_database, mock_env):
        """Test submitting report without message_id."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/report-issue",
                json={
                    "issue_type": "incorrect",
                    "description": "Test"
                }
            )

            assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_missing_issue_type(self, mock_database, mock_env):
        """Test submitting report without issue_type."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/report-issue",
                json={
                    "message_id": "msg-123",
                    "description": "Test"
                }
            )

            assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_missing_description(self, mock_database, mock_env):
        """Test submitting report without description."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/report-issue",
                json={
                    "message_id": "msg-123",
                    "issue_type": "incorrect"
                }
            )

            # May return 422 if description is required, or 200 if optional
            assert response.status_code in [200, 422]

    @pytest.mark.asyncio
    async def test_empty_description(self, mock_database, mock_env):
        """Test submitting report with empty description."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/report-issue",
                json={
                    "message_id": "msg-123",
                    "issue_type": "incorrect",
                    "description": ""
                }
            )

            # Implementation may accept or reject empty description
            assert response.status_code in [200, 422]

    @pytest.mark.asyncio
    async def test_database_error(self, mock_env):
        """Test handling of database errors."""
        from api.main import app

        with patch('api.routes.report_issue.psycopg.connect') as mock_connect:
            mock_connect.side_effect = psycopg.Error("Connection failed")

            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.post(
                    "/api/report-issue",
                    json={
                        "message_id": "msg-123",
                        "issue_type": "incorrect",
                        "description": "Test"
                    }
                )

                assert response.status_code == 500
                assert "database" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_missing_database_url(self):
        """Test handling of missing database URL."""
        from api.main import app

        with patch.dict('os.environ', {}, clear=True):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.post(
                    "/api/report-issue",
                    json={
                        "message_id": "msg-123",
                        "issue_type": "incorrect",
                        "description": "Test"
                    }
                )

                assert response.status_code == 500
                assert "configuration" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_stores_all_fields(self, mock_database, mock_env):
        """Test that all fields are stored in database."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/report-issue",
                json={
                    "message_id": "msg-123",
                    "issue_type": "incorrect",
                    "description": "Detailed description here"
                }
            )

            assert response.status_code == 200

            # Verify INSERT includes all fields
            call_args = mock_database['cursor'].execute.call_args
            sql = call_args[0][0]
            params = call_args[0][1]

            assert "message_id" in sql
            assert "issue_type" in sql
            assert "description" in sql
            assert "severity" in sql
            assert "created_at" in sql

            # Verify values
            assert "msg-123" in params
            assert "incorrect" in params
            assert "Detailed description here" in params

    @pytest.mark.asyncio
    async def test_long_description(self, mock_database, mock_env):
        """Test submitting report with very long description."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            long_description = "A" * 5000  # 5000 characters

            response = await client.post(
                "/api/report-issue",
                json={
                    "message_id": "msg-123",
                    "issue_type": "incorrect",
                    "description": long_description
                }
            )

            # Should either succeed or return validation error for too long
            assert response.status_code in [200, 422]


@pytest.mark.asyncio
class TestReportIssueValidation:
    """Additional validation tests for report-issue endpoint."""

    @pytest.fixture
    def mock_database(self):
        """Mock database for validation tests."""
        with patch('api.routes.report_issue.psycopg.connect') as mock_connect:
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
    async def test_description_with_special_characters(self, mock_database, mock_env):
        """Test description containing special characters."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/report-issue",
                json={
                    "message_id": "msg-123",
                    "issue_type": "incorrect",
                    "description": "Test with special chars: <script>alert('xss')</script>"
                }
            )

            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_description_with_unicode(self, mock_database, mock_env):
        """Test description containing unicode characters."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(
                "/api/report-issue",
                json={
                    "message_id": "msg-123",
                    "issue_type": "incorrect",
                    "description": "Test with unicode: 日本語 emoji 🎉 and math α + β = γ"
                }
            )

            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_multiple_reports_same_message(self, mock_database, mock_env):
        """Test that multiple reports can be submitted for same message."""
        from api.main import app

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            # Submit multiple reports
            for i in range(3):
                response = await client.post(
                    "/api/report-issue",
                    json={
                        "message_id": "msg-123",
                        "issue_type": "incorrect",
                        "description": f"Report number {i + 1}"
                    }
                )
                assert response.status_code == 200

            # All three inserts should have been called
            assert mock_database['cursor'].execute.call_count == 3
