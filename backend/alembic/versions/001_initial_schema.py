"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-02-12

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create initial database schema."""

    # Chat Sessions Table
    op.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            session_id_hash VARCHAR(64) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT NOW(),
            last_activity_at TIMESTAMP DEFAULT NOW()
        )
    """)

    op.execute("CREATE INDEX IF NOT EXISTS idx_session_hash ON chat_sessions(session_id_hash)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_session_created ON chat_sessions(created_at)")

    # Chat Messages Table
    op.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            citations_json JSONB,
            response_time_ms INTEGER,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)

    op.execute("CREATE INDEX IF NOT EXISTS idx_message_session ON chat_messages(session_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_message_created ON chat_messages(created_at)")

    # Feedback Events Table
    op.execute("""
        CREATE TABLE IF NOT EXISTS feedback_events (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            message_id UUID REFERENCES chat_messages(id) ON DELETE CASCADE,
            rating VARCHAR(10) CHECK (rating IN ('up', 'down')),
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)

    op.execute("CREATE INDEX IF NOT EXISTS idx_feedback_message ON feedback_events(message_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_feedback_created ON feedback_events(created_at)")

    # Issue Reports Table
    op.execute("""
        CREATE TABLE IF NOT EXISTS issue_reports (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            message_id UUID REFERENCES chat_messages(id) ON DELETE CASCADE,
            issue_type VARCHAR(50) CHECK (issue_type IN ('incorrect', 'incomplete', 'harmful', 'other')),
            description TEXT,
            severity VARCHAR(20) CHECK (severity IN ('low', 'medium', 'high')) DEFAULT 'medium',
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)

    op.execute("CREATE INDEX IF NOT EXISTS idx_issue_message ON issue_reports(message_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_issue_created ON issue_reports(created_at)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_issue_severity ON issue_reports(severity)")


def downgrade() -> None:
    """Drop all tables."""
    op.execute("DROP TABLE IF EXISTS issue_reports CASCADE")
    op.execute("DROP TABLE IF EXISTS feedback_events CASCADE")
    op.execute("DROP TABLE IF EXISTS chat_messages CASCADE")
    op.execute("DROP TABLE IF EXISTS chat_sessions CASCADE")
