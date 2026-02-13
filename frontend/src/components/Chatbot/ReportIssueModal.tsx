/**
 * ReportIssueModal Component
 *
 * Modal for reporting issues with chatbot responses.
 */
import React, { useState } from 'react';
import styles from './ReportIssueModal.module.css';

export interface ReportIssueModalProps {
  messageId: string;
  isOpen: boolean;
  onClose: () => void;
  onSubmit?: () => void;
}

export const ReportIssueModal: React.FC<ReportIssueModalProps> = ({
  messageId,
  isOpen,
  onClose,
  onSubmit,
}) => {
  const [issueType, setIssueType] = useState<string>('incorrect');
  const [description, setDescription] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isSubmitting || !description.trim()) return;

    setIsSubmitting(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/report-issue', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message_id: messageId,
          issue_type: issueType,
          description: description.trim(),
        }),
      });

      if (response.ok) {
        setSubmitted(true);
        onSubmit?.();
        setTimeout(() => {
          onClose();
          setSubmitted(false);
          setDescription('');
          setIssueType('incorrect');
        }, 2000);
      }
    } catch (error) {
      console.error('Failed to submit issue:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <div className={styles.header}>
          <h3>Report Issue</h3>
          <button onClick={onClose} className={styles.closeButton}>
            ✕
          </button>
        </div>

        {submitted ? (
          <div className={styles.successMessage}>
            ✅ Issue reported successfully! Thank you for helping us improve.
          </div>
        ) : (
          <form onSubmit={handleSubmit} className={styles.form}>
            <div className={styles.field}>
              <label htmlFor="issue-type">Issue Type:</label>
              <select
                id="issue-type"
                value={issueType}
                onChange={(e) => setIssueType(e.target.value)}
                className={styles.select}
              >
                <option value="incorrect">Incorrect information</option>
                <option value="incomplete">Incomplete answer</option>
                <option value="harmful">Harmful/inappropriate content</option>
              </select>
            </div>

            <div className={styles.field}>
              <label htmlFor="description">Description:</label>
              <textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Please describe the issue..."
                className={styles.textarea}
                rows={4}
                required
                maxLength={1000}
              />
              <div className={styles.charCount}>
                {description.length}/1000
              </div>
            </div>

            <div className={styles.actions}>
              <button
                type="button"
                onClick={onClose}
                className={styles.cancelButton}
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={isSubmitting || !description.trim()}
                className={styles.submitButton}
              >
                {isSubmitting ? 'Submitting...' : 'Submit Report'}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};
