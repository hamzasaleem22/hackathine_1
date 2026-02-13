/**
 * Message list component with auto-scroll.
 * Displays user and bot messages with citations, feedback buttons, and report issue.
 */
import React, { useEffect, useRef, useState } from 'react';
import { ExternalLink } from 'lucide-react';
import { ChatMessage } from '../../hooks/useSessionManager';
import { FeedbackButtons } from './FeedbackButtons';
import { ReportIssueModal } from './ReportIssueModal';
import styles from './MessageList.module.css';

export interface MessageListProps {
  messages: ChatMessage[];
  isLoading: boolean;
}

export function MessageList({ messages, isLoading }: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [reportModalMessageId, setReportModalMessageId] = useState<string | null>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  // Citation click handler with section highlighting (T086)
  const handleCitationClick = (e: React.MouseEvent<HTMLAnchorElement>, url: string) => {
    e.preventDefault();

    // Extract section ID from URL (e.g., "/module-0/chapter" -> "chapter")
    const sectionId = url.split('/').pop();
    if (!sectionId) return;

    // Find element by ID
    const element = document.getElementById(sectionId);
    if (element) {
      // Smooth scroll to element
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });

      // Add highlight effect
      element.style.transition = 'background-color 0.3s ease';
      element.style.backgroundColor = 'rgba(255, 215, 0, 0.3)';

      // Remove highlight after 2 seconds
      setTimeout(() => {
        element.style.backgroundColor = '';
      }, 2000);
    } else {
      // If element not found, navigate normally
      window.location.href = url;
    }
  };

  if (messages.length === 0 && !isLoading) {
    return (
      <div className={styles.emptyState}>
        <p>Ask me anything about the Physical AI Textbook!</p>
        <p className={styles.hint}>
          Try: "What is Physical AI?" or "Explain embodied intelligence"
        </p>
      </div>
    );
  }

  return (
    <div className={styles.messageList}>
      {messages.map((message) => (
        <div
          key={message.id}
          className={`${styles.message} ${
            message.role === 'user' ? styles.userMessage : styles.botMessage
          }`}
          data-testid={`${message.role}-message`}
        >
          <div className={styles.messageContent}>
            {message.content}
          </div>

          {/* Citations */}
          {message.citations && message.citations.length > 0 && (
            <div className={styles.citations}>
              <div className={styles.citationsHeader}>Sources:</div>
              {message.citations.map((citation, index) => (
                <a
                  key={index}
                  href={citation.url}
                  className={styles.citation}
                  onClick={(e) => handleCitationClick(e, citation.url)}
                  data-testid="citation-link"
                >
                  <ExternalLink size={14} />
                  <span>{citation.section}</span>
                  <span className={styles.score}>
                    {Math.round(citation.score * 100)}% match
                  </span>
                </a>
              ))}
            </div>
          )}

          {/* Feedback & Report (User Story 3) - Only for bot messages */}
          {message.role === 'assistant' && message.id && (
            <div className={styles.messageActions}>
              <FeedbackButtons messageId={message.id} />
              <button
                onClick={() => setReportModalMessageId(message.id)}
                className={styles.reportButton}
                aria-label="Report issue"
              >
                🚩 Report Issue
              </button>
            </div>
          )}
        </div>
      ))}

      {/* Report Issue Modal */}
      {reportModalMessageId && (
        <ReportIssueModal
          messageId={reportModalMessageId}
          isOpen={true}
          onClose={() => setReportModalMessageId(null)}
        />
      )}

      {/* Loading indicator */}
      {isLoading && (
        <div className={`${styles.message} ${styles.botMessage}`} data-testid="message-loading">
          <div className={styles.loadingDots}>
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
}
