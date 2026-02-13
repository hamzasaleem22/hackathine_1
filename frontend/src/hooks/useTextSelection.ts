/**
 * useTextSelection hook
 *
 * Detects and manages text selection on the page for context-aware queries.
 * Supports both desktop (mouse selection) and mobile (long-press) interactions.
 */
import { useState, useEffect, useCallback } from 'react';

export interface TextSelection {
  text: string;
  isValid: boolean;
  position: { x: number; y: number } | null;
}

interface UseTextSelectionOptions {
  minLength?: number;
  maxLength?: number;
  enableMobile?: boolean;
}

export function useTextSelection(options: UseTextSelectionOptions = {}) {
  const {
    minLength = 10,
    maxLength = 2000,
    enableMobile = true,
  } = options;

  const [selection, setSelection] = useState<TextSelection>({
    text: '',
    isValid: false,
    position: null,
  });

  const handleSelectionChange = useCallback(() => {
    const sel = window.getSelection();
    const text = sel?.toString().trim() || '';

    if (text.length >= minLength && text.length <= maxLength) {
      // Get selection position for button placement
      const range = sel?.getRangeAt(0);
      const rect = range?.getBoundingClientRect();

      setSelection({
        text,
        isValid: true,
        position: rect
          ? {
              x: rect.left + rect.width / 2,
              y: rect.top - 10, // Position above selection
            }
          : null,
      });
    } else if (text.length > 0 && text.length < minLength) {
      // Text is selected but too short
      setSelection({
        text,
        isValid: false,
        position: null,
      });
    } else {
      // No selection or cleared
      setSelection({
        text: '',
        isValid: false,
        position: null,
      });
    }
  }, [minLength, maxLength]);

  const clearSelection = useCallback(() => {
    window.getSelection()?.removeAllRanges();
    setSelection({
      text: '',
      isValid: false,
      position: null,
    });
  }, []);

  useEffect(() => {
    // Listen for selection changes
    document.addEventListener('selectionchange', handleSelectionChange);
    document.addEventListener('mouseup', handleSelectionChange);

    // Mobile support: touchend event
    if (enableMobile) {
      document.addEventListener('touchend', handleSelectionChange);
    }

    return () => {
      document.removeEventListener('selectionchange', handleSelectionChange);
      document.removeEventListener('mouseup', handleSelectionChange);
      if (enableMobile) {
        document.removeEventListener('touchend', handleSelectionChange);
      }
    };
  }, [handleSelectionChange, enableMobile]);

  return {
    selectedText: selection.text,
    isValid: selection.isValid,
    position: selection.position,
    clearSelection,
    hasSelection: selection.text.length > 0,
    isTooShort: selection.text.length > 0 && selection.text.length < minLength,
    isTooLong: selection.text.length > maxLength,
  };
}
