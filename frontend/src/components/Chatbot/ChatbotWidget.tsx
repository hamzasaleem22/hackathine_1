/**
 * ChatbotWidget - Complete with User Story 2 (Selected Text Q&A)
 */
import React, { useState, useEffect } from 'react';
import { ChatbotButton } from './ChatbotButton';
import { MessageList } from './MessageList';
import { InputField } from './InputField';
import { AskAboutButton } from './AskAboutButton';
import { useTextSelection } from '../../hooks/useTextSelection';
import styles from './ChatbotWidget.module.css';

// Inline simplified hook with context and conversation history support (T084)
function useSimpleChatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentContext, setCurrentContext] = useState<string | null>(null);
  const [sessionId] = useState(() => 'session-' + Date.now()); // Persistent session ID

  const sendMessage = async (text: string, context?: string) => {
    // Add user message with context indicator
    const userMessage = {
      id: Date.now().toString(),
      role: 'user' as const,
      content: text,
      context: context || null,
      timestamp: Date.now(),
    };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    // Store context for this query
    if (context) {
      setCurrentContext(context);
    }

    try {
      const apiUrl = 'http://127.0.0.1:8000';

      // Build conversation history from previous messages (T084)
      // Only include last 5 Q&A pairs to keep prompt size manageable
      const conversationHistory: Array<{question: string; answer: string}> = [];
      const messagesToInclude = messages.slice(-10); // Last 10 messages = 5 Q&A pairs

      for (let i = 0; i < messagesToInclude.length - 1; i += 2) {
        if (messagesToInclude[i].role === 'user' && messagesToInclude[i + 1].role === 'assistant') {
          conversationHistory.push({
            question: messagesToInclude[i].content,
            answer: messagesToInclude[i + 1].content,
          });
        }
      }

      const requestBody: any = {
        question: text,
        session_id: sessionId, // Use persistent session ID
      };

      // Add context if provided (User Story 2)
      if (context) {
        requestBody.context = context;
      }

      // Add conversation history if available (T084)
      if (conversationHistory.length > 0) {
        requestBody.conversation_history = conversationHistory;
      }

      const response = await fetch(`${apiUrl}/api/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody),
      });

      if (response.ok) {
        const data = await response.json();
        const botMessage = {
          id: (Date.now() + 1).toString(),
          role: 'assistant' as const,
          content: data.answer,
          citations: data.citations || [],
          timestamp: Date.now(),
        };
        setMessages(prev => [...prev, botMessage]);
      } else {
        throw new Error('API request failed');
      }
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant' as const,
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: Date.now(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setCurrentContext(null); // Clear context after use
    }
  };

  const clearChat = () => {
    setMessages([]);
    setCurrentContext(null);
  };

  return {
    isOpen,
    messages,
    isLoading,
    currentContext,
    sendMessage,
    clearChat,
    open: () => setIsOpen(true),
    close: () => setIsOpen(false),
    toggle: () => setIsOpen(!isOpen),
  };
}

export const ChatbotWidget: React.FC = () => {
  const {
    isOpen,
    messages,
    isLoading,
    currentContext,
    sendMessage,
    clearChat,
    close,
    toggle,
    open,
  } = useSimpleChatbot();

  // Text selection hook (User Story 2)
  const {
    selectedText,
    isValid: isSelectionValid,
    position: selectionPosition,
    clearSelection,
    isTooShort,
  } = useTextSelection({
    minLength: 10,
    maxLength: 2000,
  });

  // Handle "Ask about this" button click
  const handleAskAboutSelection = () => {
    if (isSelectionValid && selectedText) {
      // Open chatbot if closed
      if (!isOpen) {
        open();
      }
      // Don't send immediately - let user type their question
      // The context will be shown in the UI
      clearSelection();
    }
  };

  // Escape key handler
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        close();
      }
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, close]);

  // Get context to display (either current or from last message)
  const displayContext = currentContext || (
    messages.length > 0 && messages[messages.length - 1].role === 'user'
      ? messages[messages.length - 1].context
      : null
  );

  return (
    <>
      {/* Ask About Button (User Story 2) */}
      <AskAboutButton
        onClick={handleAskAboutSelection}
        position={selectionPosition}
        visible={isSelectionValid && !isOpen}
      />

      {/* Show tooltip for short selections */}
      {isTooShort && !isOpen && (
        <div
          style={{
            position: 'fixed',
            left: selectionPosition?.x + 'px',
            top: (selectionPosition?.y || 0) - 30 + 'px',
            transform: 'translate(-50%, -100%)',
            background: '#333',
            color: 'white',
            padding: '4px 8px',
            borderRadius: '4px',
            fontSize: '12px',
            zIndex: 10000,
            whiteSpace: 'nowrap',
          }}
        >
          Select more text (min 10 characters)
        </div>
      )}

      {/* Chatbot Button */}
      {!isOpen && (
        <ChatbotButton onClick={toggle} isOpen={isOpen} />
      )}

      {/* Chatbot Modal */}
      {isOpen && (
        <div className={styles.chatbotWidget} role="dialog" aria-label="Chatbot">
          {/* Header */}
          <div className={styles.header}>
            <h2 className={styles.title}>Physical AI Assistant</h2>
            <div className={styles.headerActions}>
              <button onClick={clearChat} className={styles.clearButton}>
                Clear
              </button>
              <button onClick={close} className={styles.closeButton}>
                ✕
              </button>
            </div>
          </div>

          {/* Context Display (User Story 2) */}
          {displayContext && (
            <div className={styles.contextBanner}>
              <div className={styles.contextLabel}>📝 Context:</div>
              <div className={styles.contextText}>
                {displayContext.length > 100
                  ? displayContext.substring(0, 100) + '...'
                  : displayContext}
              </div>
            </div>
          )}

          {/* Messages */}
          <div className={styles.messagesContainer}>
            <MessageList messages={messages} isLoading={isLoading} />
          </div>

          {/* Input */}
          <div className={styles.inputContainer}>
            <InputField
              onSubmit={(text) => sendMessage(text, selectedText || undefined)}
              disabled={isLoading}
              placeholder={
                selectedText
                  ? 'Ask about the selected text...'
                  : 'Ask a question about the textbook...'
              }
            />
          </div>

          {/* Footer */}
          <div className={styles.footer}>
            <span className={styles.contentInfo}>
              Powered by Physical AI Textbook
            </span>
          </div>
        </div>
      )}
    </>
  );
};

export default ChatbotWidget;
