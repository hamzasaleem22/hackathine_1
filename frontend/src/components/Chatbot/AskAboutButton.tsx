/**
 * AskAboutButton Component
 *
 * Floating button that appears near selected text, allowing users to ask
 * context-specific questions about the selection.
 */
import React from 'react';
import styles from './AskAboutButton.module.css';

export interface AskAboutButtonProps {
  onClick: () => void;
  position: { x: number; y: number } | null;
  visible: boolean;
}

export const AskAboutButton: React.FC<AskAboutButtonProps> = ({
  onClick,
  position,
  visible,
}) => {
  if (!visible || !position) {
    return null;
  }

  return (
    <button
      className={styles.askAboutButton}
      onClick={onClick}
      style={{
        position: 'fixed',
        left: `${position.x}px`,
        top: `${position.y}px`,
        transform: 'translate(-50%, -100%)',
      }}
      aria-label="Ask about selected text"
    >
      <span className={styles.icon}>💬</span>
      <span className={styles.text}>Ask about this</span>
    </button>
  );
};

export default AskAboutButton;
