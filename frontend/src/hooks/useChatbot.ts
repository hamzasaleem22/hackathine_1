/**
 * Chatbot state management hook.
 * Manages chat UI state, loading, errors, and auto-hide behavior.
 */
import { useState, useCallback, useEffect } from 'react';
import { fetchQuery, QueryRequest, QueryResponse, NetworkError, TimeoutError } from '../services/chatbotApi';
import { useSessionManager, ChatMessage } from './useSessionManager';

export interface UseChatbotOptions {
  autoHideOnScroll?: boolean;
  scrollHideDelay?: number;
}

export function useChatbot(options: UseChatbotOptions = {}) {
  const {
    autoHideOnScroll = true,
    scrollHideDelay = 500,
  } = options;

  // Session management
  const sessionManager = useSessionManager();

  // UI state
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isOffline, setIsOffline] = useState(false);

  /**
   * Send a query to the chatbot
   */
  const sendMessage = useCallback(async (question: string, context?: string) => {
    if (!question.trim()) {
      setError('Please enter a question');
      return;
    }

    if (question.length > 2000) {
      setError('Question must be 2000 characters or less');
      return;
    }

    // Clear previous error
    setError(null);
    setIsOffline(false);
    setIsLoading(true);

    // Add user message
    sessionManager.addMessage({
      role: 'user',
      content: question,
    });

    try {
      const request: QueryRequest = {
        question,
        session_id: sessionManager.session_id,
        context,
      };

      const response: QueryResponse = await fetchQuery(request);

      // Add assistant message
      sessionManager.addMessage({
        role: 'assistant',
        content: response.answer,
        citations: response.citations,
      });

      // Update activity timestamp
      sessionManager.updateActivity();
    } catch (err) {
      let errorMessage = 'Failed to get response. Please try again.';

      if (err instanceof NetworkError) {
        setIsOffline(true);
        errorMessage = 'Connection lost. Please check your internet and try again.';
      } else if (err instanceof TimeoutError) {
        errorMessage = 'Request timeout. The server is taking too long to respond.';
      } else if (err instanceof Error) {
        errorMessage = err.message;
      }

      setError(errorMessage);

      // Add error message to chat
      sessionManager.addMessage({
        role: 'assistant',
        content: `❌ ${errorMessage}`,
      });
    } finally {
      setIsLoading(false);
    }
  }, [sessionManager]);

  /**
   * Open chatbot
   */
  const open = useCallback(() => {
    setIsOpen(true);
    setError(null);
  }, []);

  /**
   * Close chatbot
   */
  const close = useCallback(() => {
    setIsOpen(false);
  }, []);

  /**
   * Toggle chatbot open/close
   */
  const toggle = useCallback(() => {
    setIsOpen((prev) => !prev);
    setError(null);
  }, []);

  /**
   * Clear chat history
   */
  const clearChat = useCallback(() => {
    sessionManager.clearSession();
    setError(null);
  }, [sessionManager]);

  /**
   * Auto-hide on scroll behavior
   */
  useEffect(() => {
    if (!autoHideOnScroll || !isOpen) return;

    let scrollTimeout: NodeJS.Timeout;
    let isScrolling = false;

    const handleScroll = () => {
      // Set scrolling flag
      isScrolling = true;

      // Clear previous timeout
      clearTimeout(scrollTimeout);

      // Minimize after delay
      scrollTimeout = setTimeout(() => {
        if (isScrolling && isOpen) {
          setIsOpen(false);
        }
        isScrolling = false;
      }, scrollHideDelay);
    };

    window.addEventListener('scroll', handleScroll);

    return () => {
      window.removeEventListener('scroll', handleScroll);
      clearTimeout(scrollTimeout);
    };
  }, [autoHideOnScroll, scrollHideDelay, isOpen]);

  /**
   * Check for online/offline status
   */
  useEffect(() => {
    const handleOnline = () => setIsOffline(false);
    const handleOffline = () => setIsOffline(true);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Initial check
    setIsOffline(!navigator.onLine);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return {
    // State
    isOpen,
    isLoading,
    error,
    isOffline,
    messages: sessionManager.messages,
    messageCount: sessionManager.messageCount,
    isNearLimit: sessionManager.isNearLimit,
    showTimeoutWarning: sessionManager.showTimeoutWarning,
    showArchiveWarning: sessionManager.showArchiveWarning,

    // Actions
    sendMessage,
    open,
    close,
    toggle,
    clearChat,
  };
}
