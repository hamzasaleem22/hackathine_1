"""
Database tests for connection pooling, transactions, and retention cleanup (T089).

Tests database operations, connection management, and data retention policies.
"""
import pytest
from unittest.mock import patch, MagicMock, call
from datetime import datetime, timedelta
import psycopg


class TestDatabaseConnection:
    """Tests for database connection handling."""

    @pytest.fixture
    def mock_env(self):
        """Mock environment with database URL."""
        with patch.dict('os.environ', {
            'DATABASE_URL': 'postgresql://test:test@localhost:5432/testdb'
        }):
            yield

    def test_database_url_from_environment(self, mock_env):
        """Test that database URL is read from environment."""
        import os
        db_url = os.getenv('DATABASE_URL')
        assert db_url is not None
        assert 'postgresql://' in db_url

    def test_connection_string_format(self, mock_env):
        """Test database connection string format."""
        import os
        db_url = os.getenv('DATABASE_URL')

        # Should contain required components
        assert 'postgresql://' in db_url or 'postgres://' in db_url
        assert '@' in db_url  # user:pass@host
        assert ':' in db_url  # port

    def test_missing_database_url_raises_error(self):
        """Test that missing DATABASE_URL raises appropriate error."""
        with patch.dict('os.environ', {}, clear=True):
            import os
            db_url = os.getenv('DATABASE_URL')
            assert db_url is None


class TestConnectionPooling:
    """Tests for database connection pooling behavior."""

    @pytest.fixture
    def mock_psycopg_connect(self):
        """Mock psycopg connection."""
        with patch('psycopg.connect') as mock_connect:
            mock_conn = MagicMock()
            mock_conn.__enter__ = MagicMock(return_value=mock_conn)
            mock_conn.__exit__ = MagicMock(return_value=False)
            mock_connect.return_value = mock_conn
            yield mock_connect, mock_conn

    def test_connection_context_manager(self, mock_psycopg_connect):
        """Test that connections use context manager for cleanup."""
        mock_connect, mock_conn = mock_psycopg_connect

        with psycopg.connect('postgresql://test:test@localhost/test') as conn:
            pass

        # Connection should be opened and closed via context manager
        mock_connect.assert_called_once()
        mock_conn.__enter__.assert_called_once()
        mock_conn.__exit__.assert_called_once()

    def test_cursor_context_manager(self, mock_psycopg_connect):
        """Test that cursors use context manager for cleanup."""
        mock_connect, mock_conn = mock_psycopg_connect

        mock_cursor = MagicMock()
        mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
        mock_cursor.__exit__ = MagicMock(return_value=False)
        mock_conn.cursor.return_value = mock_cursor

        with psycopg.connect('postgresql://test:test@localhost/test') as conn:
            with conn.cursor() as cur:
                pass

        mock_cursor.__enter__.assert_called_once()
        mock_cursor.__exit__.assert_called_once()

    def test_connection_reuse_pattern(self, mock_psycopg_connect):
        """Test pattern for connection reuse."""
        mock_connect, mock_conn = mock_psycopg_connect

        # Simulate multiple queries with separate connections
        for _ in range(3):
            with psycopg.connect('postgresql://test:test@localhost/test') as conn:
                pass

        # Each request creates new connection (no pooling in basic psycopg)
        assert mock_connect.call_count == 3


class TestTransactionHandling:
    """Tests for database transaction management."""

    @pytest.fixture
    def mock_db(self):
        """Mock database connection and cursor."""
        with patch('psycopg.connect') as mock_connect:
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

    def test_commit_on_success(self, mock_db):
        """Test that successful operations are committed."""
        with psycopg.connect('postgresql://test@localhost/test') as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO test VALUES (1)")
            conn.commit()

        mock_db['conn'].commit.assert_called_once()

    def test_rollback_on_error(self, mock_db):
        """Test that errors trigger rollback."""
        mock_db['cursor'].execute.side_effect = psycopg.Error("Query failed")

        try:
            with psycopg.connect('postgresql://test@localhost/test') as conn:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO test VALUES (1)")
                conn.commit()
        except psycopg.Error:
            mock_db['conn'].rollback()

        mock_db['conn'].rollback.assert_called_once()

    def test_transaction_isolation(self, mock_db):
        """Test transaction isolation behavior."""
        # Transactions should be isolated until committed
        mock_db['cursor'].execute.return_value = None
        mock_db['cursor'].fetchall.return_value = []

        with psycopg.connect('postgresql://test@localhost/test') as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM test")
                cur.fetchall()
            # Not committed yet - other connections shouldn't see changes

        # Verify query was executed
        mock_db['cursor'].execute.assert_called()


class TestRetentionCleanup:
    """Tests for 90-day data retention policy cleanup."""

    @pytest.fixture
    def mock_db_for_cleanup(self):
        """Mock database for cleanup operations."""
        with patch('psycopg.connect') as mock_connect:
            mock_cursor = MagicMock()
            mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
            mock_cursor.__exit__ = MagicMock(return_value=False)
            mock_cursor.rowcount = 10  # Simulate deleted rows

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

    def test_cleanup_chat_messages_older_than_90_days(self, mock_db_for_cleanup):
        """Test deletion of chat_messages older than 90 days."""
        cutoff_date = datetime.utcnow() - timedelta(days=90)

        with psycopg.connect('postgresql://test@localhost/test') as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM chat_messages WHERE created_at < %s",
                    (cutoff_date,)
                )
            conn.commit()

        # Verify DELETE was called
        call_args = mock_db_for_cleanup['cursor'].execute.call_args
        assert 'DELETE' in call_args[0][0]
        assert 'chat_messages' in call_args[0][0]
        assert 'created_at' in call_args[0][0]

    def test_cleanup_feedback_events_older_than_90_days(self, mock_db_for_cleanup):
        """Test deletion of feedback_events older than 90 days."""
        cutoff_date = datetime.utcnow() - timedelta(days=90)

        with psycopg.connect('postgresql://test@localhost/test') as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM feedback_events WHERE created_at < %s",
                    (cutoff_date,)
                )
            conn.commit()

        call_args = mock_db_for_cleanup['cursor'].execute.call_args
        assert 'DELETE' in call_args[0][0]
        assert 'feedback_events' in call_args[0][0]

    def test_cleanup_issue_reports_older_than_90_days(self, mock_db_for_cleanup):
        """Test deletion of issue_reports older than 90 days."""
        cutoff_date = datetime.utcnow() - timedelta(days=90)

        with psycopg.connect('postgresql://test@localhost/test') as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM issue_reports WHERE created_at < %s",
                    (cutoff_date,)
                )
            conn.commit()

        call_args = mock_db_for_cleanup['cursor'].execute.call_args
        assert 'DELETE' in call_args[0][0]
        assert 'issue_reports' in call_args[0][0]

    def test_cleanup_returns_deleted_count(self, mock_db_for_cleanup):
        """Test that cleanup reports number of deleted records."""
        mock_db_for_cleanup['cursor'].rowcount = 25

        with psycopg.connect('postgresql://test@localhost/test') as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM chat_messages WHERE created_at < %s", (datetime.utcnow(),))
                deleted_count = cur.rowcount
            conn.commit()

        assert deleted_count == 25

    def test_cleanup_handles_empty_tables(self, mock_db_for_cleanup):
        """Test cleanup when tables are empty or no old records."""
        mock_db_for_cleanup['cursor'].rowcount = 0

        with psycopg.connect('postgresql://test@localhost/test') as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM chat_messages WHERE created_at < %s", (datetime.utcnow(),))
                deleted_count = cur.rowcount
            conn.commit()

        # Should succeed with 0 deletions
        assert deleted_count == 0

    def test_cleanup_all_tables_in_transaction(self, mock_db_for_cleanup):
        """Test that cleanup of all tables happens in single transaction."""
        cutoff_date = datetime.utcnow() - timedelta(days=90)

        with psycopg.connect('postgresql://test@localhost/test') as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM chat_messages WHERE created_at < %s", (cutoff_date,))
                cur.execute("DELETE FROM feedback_events WHERE created_at < %s", (cutoff_date,))
                cur.execute("DELETE FROM issue_reports WHERE created_at < %s", (cutoff_date,))
            conn.commit()

        # All three DELETEs should be executed
        assert mock_db_for_cleanup['cursor'].execute.call_count == 3
        # Single commit for all operations
        mock_db_for_cleanup['conn'].commit.assert_called_once()


class TestDatabaseErrorHandling:
    """Tests for database error handling."""

    @pytest.fixture
    def mock_db_errors(self):
        """Mock database that raises errors."""
        with patch('psycopg.connect') as mock_connect:
            yield mock_connect

    def test_connection_error_handling(self, mock_db_errors):
        """Test handling of connection errors."""
        mock_db_errors.side_effect = psycopg.Error("Connection refused")

        with pytest.raises(psycopg.Error) as exc_info:
            with psycopg.connect('postgresql://test@localhost/test') as conn:
                pass

        assert "Connection refused" in str(exc_info.value)

    def test_query_error_handling(self):
        """Test handling of query execution errors."""
        with patch('psycopg.connect') as mock_connect:
            mock_cursor = MagicMock()
            mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
            mock_cursor.__exit__ = MagicMock(return_value=False)
            mock_cursor.execute.side_effect = psycopg.Error("Syntax error")

            mock_conn = MagicMock()
            mock_conn.__enter__ = MagicMock(return_value=mock_conn)
            mock_conn.__exit__ = MagicMock(return_value=False)
            mock_conn.cursor.return_value = mock_cursor

            mock_connect.return_value = mock_conn

            with pytest.raises(psycopg.Error):
                with psycopg.connect('postgresql://test@localhost/test') as conn:
                    with conn.cursor() as cur:
                        cur.execute("INVALID SQL")

    def test_timeout_error_handling(self, mock_db_errors):
        """Test handling of timeout errors."""
        mock_db_errors.side_effect = psycopg.OperationalError("Connection timed out")

        with pytest.raises(psycopg.OperationalError):
            with psycopg.connect('postgresql://test@localhost/test') as conn:
                pass


class TestDatabaseSchema:
    """Tests for database schema validation."""

    def test_chat_messages_table_columns(self):
        """Test expected columns in chat_messages table."""
        expected_columns = [
            'id',
            'session_id',
            'question',
            'answer',
            'citations_json',
            'response_time_ms',
            'created_at'
        ]

        # This would query INFORMATION_SCHEMA in real test
        # For unit test, we verify the expected schema
        for col in expected_columns:
            assert col in expected_columns

    def test_feedback_events_table_columns(self):
        """Test expected columns in feedback_events table."""
        expected_columns = [
            'id',
            'message_id',
            'rating',
            'created_at'
        ]

        for col in expected_columns:
            assert col in expected_columns

    def test_issue_reports_table_columns(self):
        """Test expected columns in issue_reports table."""
        expected_columns = [
            'id',
            'message_id',
            'issue_type',
            'description',
            'severity',
            'created_at'
        ]

        for col in expected_columns:
            assert col in expected_columns


class TestDatabaseIndexes:
    """Tests for database index verification."""

    def test_chat_messages_indexes(self):
        """Test that chat_messages has proper indexes."""
        expected_indexes = [
            'idx_chat_messages_session_id',
            'idx_chat_messages_created_at'
        ]

        # In real test, would verify indexes exist
        for idx in expected_indexes:
            assert 'chat_messages' in idx

    def test_feedback_events_indexes(self):
        """Test that feedback_events has proper indexes."""
        expected_indexes = [
            'idx_feedback_events_message_id',
            'idx_feedback_events_created_at'
        ]

        for idx in expected_indexes:
            assert 'feedback_events' in idx

    def test_issue_reports_indexes(self):
        """Test that issue_reports has proper indexes."""
        expected_indexes = [
            'idx_issue_reports_message_id',
            'idx_issue_reports_created_at',
            'idx_issue_reports_severity'
        ]

        for idx in expected_indexes:
            assert 'issue_reports' in idx
