/**
 * Floating chatbot button component.
 * Fixed position in bottom-right corner.
 */
import React from 'react';
import { MessageCircle } from 'lucide-react';
import styles from './ChatbotButton.module.css';

export interface ChatbotButtonProps {
  onClick: () => void;
  isOpen: boolean;
  unreadCount?: number;
}

export function ChatbotButton({ onClick, isOpen, unreadCount = 0 }: ChatbotButtonProps) {
  return (
    <button
      className={styles.chatbotButton}
      onClick={onClick}
      aria-label={isOpen ? 'Close chatbot' : 'Open chatbot'}
      data-testid="chatbot-button"
      type="button"
    >
      <MessageCircle size={24} />
      {unreadCount > 0 && !isOpen && (
        <span className={styles.badge} data-testid="unread-badge">
          {unreadCount > 9 ? '9+' : unreadCount}
        </span>
      )}
    </button>
  );
}
