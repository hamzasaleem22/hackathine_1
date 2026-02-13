/**
 * Input field component for chat messages.
 * Includes character counter and validation.
 */
import React, { useState, useRef, useEffect, KeyboardEvent } from 'react';
import { Send } from 'lucide-react';
import styles from './InputField.module.css';

const MAX_LENGTH = 2000;

export interface InputFieldProps {
  onSubmit: (message: string) => void;
  disabled: boolean;
  placeholder?: string;
}

export function InputField({
  onSubmit,
  disabled,
  placeholder = 'Ask a question...',
}: InputFieldProps) {
  const [value, setValue] = useState('');
  const [showHint, setShowHint] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [value]);

  // Auto-focus when enabled
  useEffect(() => {
    if (!disabled && textareaRef.current) {
      textareaRef.current.focus();
    }
  }, [disabled]);

  const handleSubmit = () => {
    const trimmed = value.trim();

    if (!trimmed) {
      setShowHint(true);
      setTimeout(() => setShowHint(false), 3000);
      return;
    }

    if (trimmed.length > MAX_LENGTH) {
      return;
    }

    onSubmit(trimmed);
    setValue('');
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const isOverLimit = value.length > MAX_LENGTH;
  const isNearLimit = value.length > MAX_LENGTH * 0.9;
  const isEmpty = value.trim().length === 0;

  return (
    <div className={styles.inputContainer}>
      {/* Character counter */}
      {value.length > 0 && (
        <div
          className={`${styles.characterCounter} ${isOverLimit ? styles.overLimit : ''} ${
            isNearLimit ? styles.nearLimit : ''
          }`}
        >
          {value.length} / {MAX_LENGTH}
        </div>
      )}

      {/* Empty hint */}
      {showHint && (
        <div className={styles.emptyHint} role="alert">
          Please enter a question
        </div>
      )}

      <div className={styles.inputWrapper}>
        <textarea
          ref={textareaRef}
          className={styles.textarea}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled}
          data-testid="chatbot-input"
          rows={1}
          maxLength={MAX_LENGTH + 100} // Allow typing slightly over to show error
        />

        <button
          className={styles.sendButton}
          onClick={handleSubmit}
          disabled={disabled || isEmpty || isOverLimit}
          aria-label="Send message"
          data-testid="chatbot-submit"
          type="button"
        >
          <Send size={20} />
        </button>
      </div>

      {/* Keyboard hint */}
      <div className={styles.keyboardHint}>
        Press <kbd>Enter</kbd> to send, <kbd>Shift+Enter</kbd> for new line
      </div>
    </div>
  );
}
