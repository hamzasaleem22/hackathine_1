/**
 * Session management hook for chatbot.
 * Handles session persistence, timeout, and message limits.
 */
import { useState, useEffect, useCallback } from 'react';

const SESSION_TIMEOUT_MS = 2 * 60 * 60 * 1000; // 2 hours
const MAX_MESSAGES = 50;
const WARNING_TIME_MS = 60 * 1000; // 1 minute before timeout

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
  citations?: any[];
}

export interface SessionData {
  session_id: string;
  messages: ChatMessage[];
  created_at: number;
  last_activity: number;
}

/**
 * Generate a unique session ID
 */
function generateSessionId(): string {
  return `session-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
}

/**
 * Load session from localStorage
 */
function loadSession(): SessionData | null {
  try {
    const stored = localStorage.getItem('chatbot_session');
    if (!stored) return null;

    const session: SessionData = JSON.parse(stored);

    // Check if session has expired
    const now = Date.now();
    if (now - session.last_activity > SESSION_TIMEOUT_MS) {
      localStorage.removeItem('chatbot_session');
      return null;
    }

    return session;
  } catch (error) {
    console.error('Failed to load session:', error);
    return null;
  }
}

/**
 * Save session to localStorage
 */
function saveSession(session: SessionData): void {
  try {
    localStorage.setItem('chatbot_session', JSON.stringify(session));
  } catch (error) {
    console.error('Failed to save session:', error);
  }
}

/**
 * useSessionManager hook
 */
export function useSessionManager() {
  const [session, setSession] = useState<SessionData>(() => {
    const existing = loadSession();
    if (existing) return existing;

    return {
      session_id: generateSessionId(),
      messages: [],
      created_at: Date.now(),
      last_activity: Date.now(),
    };
  });

  const [showTimeoutWarning, setShowTimeoutWarning] = useState(false);
  const [showArchiveWarning, setShowArchiveWarning] = useState(false);

  /**
   * Add a message to the session
   */
  const addMessage = useCallback((message: Omit<ChatMessage, 'id' | 'timestamp'>) => {
    setSession((prev) => {
      const newMessage: ChatMessage = {
        ...message,
        id: `msg-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`,
        timestamp: Date.now(),
      };

      const updatedMessages = [...prev.messages, newMessage];

      // Check message limit
      if (updatedMessages.length > MAX_MESSAGES) {
        // Archive old messages (keep last 50)
        setShowArchiveWarning(true);
        setTimeout(() => setShowArchiveWarning(false), 5000);
      }

      const newSession = {
        ...prev,
        messages: updatedMessages.slice(-MAX_MESSAGES),
        last_activity: Date.now(),
      };

      saveSession(newSession);
      return newSession;
    });
  }, []);

  /**
   * Clear the session
   */
  const clearSession = useCallback(() => {
    const newSession: SessionData = {
      session_id: generateSessionId(),
      messages: [],
      created_at: Date.now(),
      last_activity: Date.now(),
    };

    setSession(newSession);
    saveSession(newSession);
    setShowTimeoutWarning(false);
    setShowArchiveWarning(false);
  }, []);

  /**
   * Update last activity timestamp
   */
  const updateActivity = useCallback(() => {
    setSession((prev) => {
      const updated = {
        ...prev,
        last_activity: Date.now(),
      };
      saveSession(updated);
      return updated;
    });
  }, []);

  /**
   * Check for session timeout and show warning
   */
  useEffect(() => {
    const checkTimeout = () => {
      const now = Date.now();
      const timeRemaining = SESSION_TIMEOUT_MS - (now - session.last_activity);

      // Show warning 1 minute before timeout
      if (timeRemaining <= WARNING_TIME_MS && timeRemaining > 0) {
        setShowTimeoutWarning(true);
      } else if (timeRemaining <= 0) {
        // Session expired
        clearSession();
      } else {
        setShowTimeoutWarning(false);
      }
    };

    // Check every 30 seconds
    const interval = setInterval(checkTimeout, 30000);
    checkTimeout(); // Initial check

    return () => clearInterval(interval);
  }, [session.last_activity, clearSession]);

  /**
   * Save session on unmount
   */
  useEffect(() => {
    return () => {
      saveSession(session);
    };
  }, [session]);

  return {
    session_id: session.session_id,
    messages: session.messages,
    addMessage,
    clearSession,
    updateActivity,
    showTimeoutWarning,
    showArchiveWarning,
    messageCount: session.messages.length,
    isNearLimit: session.messages.length >= MAX_MESSAGES - 5,
  };
}
