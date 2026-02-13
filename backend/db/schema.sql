-- Database schema for RAG Chatbot
-- PostgreSQL syntax with proper CREATE INDEX statements

-- ====================================
-- Chat Sessions Table
-- ====================================
CREATE TABLE IF NOT EXISTS chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id_hash VARCHAR(64) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_activity_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for chat_sessions
CREATE INDEX IF NOT EXISTS idx_session_hash ON chat_sessions(session_id_hash);
CREATE INDEX IF NOT EXISTS idx_session_created ON chat_sessions(created_at);

-- ====================================
-- Chat Messages Table
-- ====================================
CREATE TABLE IF NOT EXISTS chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    citations_json JSONB,
    response_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for chat_messages
CREATE INDEX IF NOT EXISTS idx_message_session ON chat_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_message_created ON chat_messages(created_at);

-- ====================================
-- Feedback Events Table
-- ====================================
CREATE TABLE IF NOT EXISTS feedback_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_id UUID REFERENCES chat_messages(id) ON DELETE CASCADE,
    rating VARCHAR(10) CHECK (rating IN ('up', 'down')),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for feedback_events
CREATE INDEX IF NOT EXISTS idx_feedback_message ON feedback_events(message_id);
CREATE INDEX IF NOT EXISTS idx_feedback_created ON feedback_events(created_at);

-- ====================================
-- Issue Reports Table
-- ====================================
CREATE TABLE IF NOT EXISTS issue_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_id UUID REFERENCES chat_messages(id) ON DELETE CASCADE,
    issue_type VARCHAR(50) CHECK (issue_type IN ('incorrect', 'incomplete', 'harmful', 'other')),
    description TEXT,
    severity VARCHAR(20) CHECK (severity IN ('low', 'medium', 'high')) DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for issue_reports
CREATE INDEX IF NOT EXISTS idx_issue_message ON issue_reports(message_id);
CREATE INDEX IF NOT EXISTS idx_issue_created ON issue_reports(created_at);
CREATE INDEX IF NOT EXISTS idx_issue_severity ON issue_reports(severity);

-- ====================================
-- Comments
-- ====================================
COMMENT ON TABLE chat_sessions IS 'Stores chat session metadata with anonymized session IDs';
COMMENT ON TABLE chat_messages IS 'Stores all chat questions and answers with citations';
COMMENT ON TABLE feedback_events IS 'Stores user feedback (thumbs up/down) for answers';
COMMENT ON TABLE issue_reports IS 'Stores reported issues with answers for quality improvement';
