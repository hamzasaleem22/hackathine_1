/**
 * Unit tests for useChatbot hook.
 *
 * Tests chat state management, message history, and session timeout.
 */
import { renderHook, act, waitFor } from '@testing-library/react';
import { useChatbot } from '../hooks/useChatbot';
import * as chatbotApi from '../services/chatbotApi';

// Mock the chatbotApi module
jest.mock('../services/chatbotApi', () => ({
  fetchQuery: jest.fn(),
  NetworkError: class NetworkError extends Error {
    constructor(message: string) {
      super(message);
      this.name = 'NetworkError';
    }
  },
  TimeoutError: class TimeoutError extends Error {
    constructor(message: string) {
      super(message);
      this.name = 'TimeoutError';
    }
  },
}));

// Mock localStorage
const localStorageMock = {
  store: {} as Record<string, string>,
  getItem: jest.fn((key: string) => localStorageMock.store[key] || null),
  setItem: jest.fn((key: string, value: string) => {
    localStorageMock.store[key] = value;
  }),
  removeItem: jest.fn((key: string) => {
    delete localStorageMock.store[key];
  }),
  clear: jest.fn(() => {
    localStorageMock.store = {};
  }),
};

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
  writable: true,
});

// Mock navigator.onLine
Object.defineProperty(navigator, 'onLine', {
  value: true,
  writable: true,
});

describe('useChatbot', () => {
  const mockFetchQuery = chatbotApi.fetchQuery as jest.Mock;

  beforeEach(() => {
    jest.clearAllMocks();
    localStorageMock.clear();
    jest.useFakeTimers();
    (navigator as any).onLine = true;
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  describe('Initial State', () => {
    it('should initialize with closed state', () => {
      const { result } = renderHook(() => useChatbot());

      expect(result.current.isOpen).toBe(false);
      expect(result.current.isLoading).toBe(false);
      expect(result.current.error).toBeNull();
      expect(result.current.messages).toEqual([]);
    });

    it('should detect offline status on mount', () => {
      (navigator as any).onLine = false;

      const { result } = renderHook(() => useChatbot());

      expect(result.current.isOffline).toBe(true);
    });
  });

  describe('Open/Close/Toggle', () => {
    it('should open chatbot', () => {
      const { result } = renderHook(() => useChatbot());

      act(() => {
        result.current.open();
      });

      expect(result.current.isOpen).toBe(true);
    });

    it('should close chatbot', () => {
      const { result } = renderHook(() => useChatbot());

      act(() => {
        result.current.open();
      });
      expect(result.current.isOpen).toBe(true);

      act(() => {
        result.current.close();
      });
      expect(result.current.isOpen).toBe(false);
    });

    it('should toggle chatbot', () => {
      const { result } = renderHook(() => useChatbot());

      expect(result.current.isOpen).toBe(false);

      act(() => {
        result.current.toggle();
      });
      expect(result.current.isOpen).toBe(true);

      act(() => {
        result.current.toggle();
      });
      expect(result.current.isOpen).toBe(false);
    });

    it('should clear error when opening', () => {
      const { result } = renderHook(() => useChatbot());

      // Manually set error state
      act(() => {
        result.current.sendMessage(''); // This sets an error
      });

      expect(result.current.error).not.toBeNull();

      act(() => {
        result.current.open();
      });

      expect(result.current.error).toBeNull();
    });
  });

  describe('Send Message', () => {
    it('should validate empty question', async () => {
      const { result } = renderHook(() => useChatbot());

      await act(async () => {
        await result.current.sendMessage('');
      });

      expect(result.current.error).toBe('Please enter a question');
      expect(mockFetchQuery).not.toHaveBeenCalled();
    });

    it('should validate whitespace-only question', async () => {
      const { result } = renderHook(() => useChatbot());

      await act(async () => {
        await result.current.sendMessage('   ');
      });

      expect(result.current.error).toBe('Please enter a question');
    });

    it('should validate question length exceeding 2000 characters', async () => {
      const { result } = renderHook(() => useChatbot());

      await act(async () => {
        await result.current.sendMessage('a'.repeat(2001));
      });

      expect(result.current.error).toBe('Question must be 2000 characters or less');
      expect(mockFetchQuery).not.toHaveBeenCalled();
    });

    it('should set loading state during API call', async () => {
      mockFetchQuery.mockImplementation(
        () => new Promise((resolve) => setTimeout(() => resolve({
          answer: 'Test answer',
          citations: [],
          confidence: 0.9,
          message_id: 'msg-123',
          response_time_ms: 100,
        }), 1000))
      );

      const { result } = renderHook(() => useChatbot());

      act(() => {
        result.current.sendMessage('What is Physical AI?');
      });

      expect(result.current.isLoading).toBe(true);

      await act(async () => {
        jest.advanceTimersByTime(1000);
      });

      expect(result.current.isLoading).toBe(false);
    });

    it('should add user message and bot response', async () => {
      const mockResponse = {
        answer: 'Physical AI is a field combining...',
        citations: [{ section: 'Module 0', url: '/docs/module-0', score: 0.95 }],
        confidence: 0.9,
        message_id: 'msg-123',
        response_time_ms: 100,
      };

      mockFetchQuery.mockResolvedValueOnce(mockResponse);

      const { result } = renderHook(() => useChatbot());

      await act(async () => {
        await result.current.sendMessage('What is Physical AI?');
      });

      expect(result.current.messages).toHaveLength(2);
      expect(result.current.messages[0].role).toBe('user');
      expect(result.current.messages[0].content).toBe('What is Physical AI?');
      expect(result.current.messages[1].role).toBe('assistant');
      expect(result.current.messages[1].content).toBe('Physical AI is a field combining...');
      expect(result.current.messages[1].citations).toEqual(mockResponse.citations);
    });

    it('should include context in request when provided', async () => {
      mockFetchQuery.mockResolvedValueOnce({
        answer: 'This refers to...',
        citations: [],
        confidence: 0.9,
        message_id: 'msg-123',
        response_time_ms: 100,
      });

      const { result } = renderHook(() => useChatbot());

      await act(async () => {
        await result.current.sendMessage('What does this mean?', 'Selected text context');
      });

      expect(mockFetchQuery).toHaveBeenCalledWith(
        expect.objectContaining({
          question: 'What does this mean?',
          context: 'Selected text context',
        })
      );
    });
  });

  describe('Error Handling', () => {
    it('should handle network error', async () => {
      mockFetchQuery.mockRejectedValueOnce(new chatbotApi.NetworkError('Connection lost'));

      const { result } = renderHook(() => useChatbot());

      await act(async () => {
        await result.current.sendMessage('Test question');
      });

      expect(result.current.error).toBe('Connection lost. Please check your internet and try again.');
      expect(result.current.isOffline).toBe(true);
    });

    it('should handle timeout error', async () => {
      mockFetchQuery.mockRejectedValueOnce(new chatbotApi.TimeoutError('Request timed out'));

      const { result } = renderHook(() => useChatbot());

      await act(async () => {
        await result.current.sendMessage('Test question');
      });

      expect(result.current.error).toBe('Request timeout. The server is taking too long to respond.');
    });

    it('should handle generic error', async () => {
      mockFetchQuery.mockRejectedValueOnce(new Error('Something went wrong'));

      const { result } = renderHook(() => useChatbot());

      await act(async () => {
        await result.current.sendMessage('Test question');
      });

      expect(result.current.error).toBe('Something went wrong');
    });

    it('should add error message to chat', async () => {
      mockFetchQuery.mockRejectedValueOnce(new Error('API error'));

      const { result } = renderHook(() => useChatbot());

      await act(async () => {
        await result.current.sendMessage('Test question');
      });

      expect(result.current.messages).toHaveLength(2);
      expect(result.current.messages[1].role).toBe('assistant');
      expect(result.current.messages[1].content).toContain('API error');
    });
  });

  describe('Clear Chat', () => {
    it('should clear all messages and error', async () => {
      mockFetchQuery.mockResolvedValueOnce({
        answer: 'Test answer',
        citations: [],
        confidence: 0.9,
        message_id: 'msg-123',
        response_time_ms: 100,
      });

      const { result } = renderHook(() => useChatbot());

      await act(async () => {
        await result.current.sendMessage('Test question');
      });

      expect(result.current.messages).toHaveLength(2);

      act(() => {
        result.current.clearChat();
      });

      expect(result.current.messages).toEqual([]);
      expect(result.current.error).toBeNull();
    });
  });

  describe('Auto-hide on Scroll', () => {
    it('should auto-hide when scrolling (enabled by default)', () => {
      const { result } = renderHook(() => useChatbot({ autoHideOnScroll: true }));

      act(() => {
        result.current.open();
      });
      expect(result.current.isOpen).toBe(true);

      // Simulate scroll event
      act(() => {
        window.dispatchEvent(new Event('scroll'));
      });

      // Advance timer past scroll hide delay (500ms default)
      act(() => {
        jest.advanceTimersByTime(600);
      });

      expect(result.current.isOpen).toBe(false);
    });

    it('should NOT auto-hide when disabled', () => {
      const { result } = renderHook(() => useChatbot({ autoHideOnScroll: false }));

      act(() => {
        result.current.open();
      });
      expect(result.current.isOpen).toBe(true);

      // Simulate scroll event
      act(() => {
        window.dispatchEvent(new Event('scroll'));
        jest.advanceTimersByTime(600);
      });

      expect(result.current.isOpen).toBe(true);
    });

    it('should respect custom scroll hide delay', () => {
      const { result } = renderHook(() =>
        useChatbot({ autoHideOnScroll: true, scrollHideDelay: 1000 })
      );

      act(() => {
        result.current.open();
      });

      // Simulate scroll event
      act(() => {
        window.dispatchEvent(new Event('scroll'));
        jest.advanceTimersByTime(500); // Less than custom delay
      });

      expect(result.current.isOpen).toBe(true); // Still open

      act(() => {
        jest.advanceTimersByTime(600); // Now past delay
      });

      expect(result.current.isOpen).toBe(false);
    });
  });

  describe('Online/Offline Status', () => {
    it('should update offline status on online event', () => {
      (navigator as any).onLine = false;

      const { result } = renderHook(() => useChatbot());
      expect(result.current.isOffline).toBe(true);

      act(() => {
        (navigator as any).onLine = true;
        window.dispatchEvent(new Event('online'));
      });

      expect(result.current.isOffline).toBe(false);
    });

    it('should update offline status on offline event', () => {
      const { result } = renderHook(() => useChatbot());
      expect(result.current.isOffline).toBe(false);

      act(() => {
        window.dispatchEvent(new Event('offline'));
      });

      expect(result.current.isOffline).toBe(true);
    });
  });

  describe('Session Manager Integration', () => {
    it('should expose session manager state', () => {
      const { result } = renderHook(() => useChatbot());

      expect(result.current.messageCount).toBeDefined();
      expect(result.current.isNearLimit).toBeDefined();
      expect(result.current.showTimeoutWarning).toBeDefined();
      expect(result.current.showArchiveWarning).toBeDefined();
    });
  });
});
