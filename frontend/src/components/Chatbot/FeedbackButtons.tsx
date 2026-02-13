/**
 * FeedbackButtons Component
 *
 * Thumbs up/down buttons for user feedback on chatbot responses.
 */
import React, { useState } from 'react';
import styles from './FeedbackButtons.module.css';

export interface FeedbackButtonsProps {
  messageId: string;
  onFeedback?: (rating: 'up' | 'down') => void;
}

export const FeedbackButtons: React.FC<FeedbackButtonsProps> = ({
  messageId,
  onFeedback,
}) => {
  const [feedback, setFeedback] = useState<'up' | 'down' | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleFeedback = async (rating: 'up' | 'down') => {
    if (feedback || isSubmitting) return;

    setIsSubmitting(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message_id: messageId,
          rating: rating,
        }),
      });

      if (response.ok) {
        setFeedback(rating);
        onFeedback?.(rating);
      }
    } catch (error) {
      console.error('Failed to submit feedback:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className={styles.feedbackButtons}>
      <button
        onClick={() => handleFeedback('up')}
        className={`${styles.feedbackButton} ${feedback === 'up' ? styles.active : ''}`}
        disabled={feedback !== null || isSubmitting}
        aria-label="Helpful"
      >
        👍
      </button>
      <button
        onClick={() => handleFeedback('down')}
        className={`${styles.feedbackButton} ${feedback === 'down' ? styles.active : ''}`}
        disabled={feedback !== null || isSubmitting}
        aria-label="Not helpful"
      >
        👎
      </button>
      {feedback && (
        <span className={styles.thankYou}>Thanks!</span>
      )}
    </div>
  );
};
