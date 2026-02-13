/**
 * InitializingBanner component
 *
 * Displays a banner when the chatbot is still indexing content and not ready for queries.
 * This handles the edge case where a user attempts to use the chatbot before indexing is complete.
 */
import React from 'react';
import styles from './InitializingBanner.module.css';

interface InitializingBannerProps {
  /** Current indexing status */
  isIndexing: boolean;
  /** Number of chunks indexed so far */
  chunksIndexed?: number;
}

export const InitializingBanner: React.FC<InitializingBannerProps> = ({
  isIndexing,
  chunksIndexed = 0,
}) => {
  if (!isIndexing) {
    return null;
  }

  return (
    <div className={styles.banner} role="alert" aria-live="polite">
      <div className={styles.iconContainer}>
        <div className={styles.spinner} aria-hidden="true" />
      </div>
      <div className={styles.content}>
        <h3 className={styles.title}>Chatbot Initializing...</h3>
        <p className={styles.message}>
          We're indexing the textbook content to provide accurate answers.
          {chunksIndexed > 0 && (
            <span className={styles.progress}>
              {' '}
              ({chunksIndexed} sections indexed)
            </span>
          )}
        </p>
        <p className={styles.submessage}>This usually takes a few moments. Please check back shortly.</p>
      </div>
    </div>
  );
};

export default InitializingBanner;
