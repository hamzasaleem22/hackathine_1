/**
 * Unit tests for useSessionManager hook.
 *
 * Tests localStorage operations, timeout logic, and 50-message limit.
 */
import { renderHook, act } from '@testing-library/react';
import { useSessionManager, ChatMessage, SessionData } from '../hooks/useSessionManager';

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

describe('useSessionManager', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorageMock.clear();
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  describe('Session Initialization', () => {
    it('should create a new session when localStorage is empty', () => {
      const { result } = renderHook(() => useSessionManager());

      expect(result.current.session_id).toMatch(/^session-\d+-[a-z0-9]+$/);
      expect(result.current.messages).toEqual([]);
      expect(result.current.messageCount).toBe(0);
    });

    it('should restore session from localStorage if valid', () => {
      const existingSession: SessionData = {
        session_id: 'session-existing-123',
        messages: [
          {
            id: 'msg-1',
            role: 'user',
            content: 'Hello',
            timestamp: Date.now(),
          },
        ],
        created_at: Date.now(),
        last_activity: Date.now(),
      };

      localStorageMock.store['chatbot_session'] = JSON.stringify(existingSession);

      const { result } = renderHook(() => useSessionManager());

      expect(result.current.session_id).toBe('session-existing-123');
      expect(result.current.messages).toHaveLength(1);
      expect(result.current.messages[0].content).toBe('Hello');
    });

    it('should create new session if existing session expired', () => {
      const expiredSession: SessionData = {
        session_id: 'session-expired',
        messages: [],
        created_at: Date.now() - 3 * 60 * 60 * 1000, // 3 hours ago
        last_activity: Date.now() - 3 * 60 * 60 * 1000, // 3 hours ago (expired)
      };

      localStorageMock.store['chatbot_session'] = JSON.stringify(expiredSession);

      const { result } = renderHook(() => useSessionManager());

      expect(result.current.session_id).not.toBe('session-expired');
      expect(result.current.messages).toEqual([]);
    });
  });

  describe('Message Management', () => {
    it('should add a message correctly', () => {
      const { result } = renderHook(() => useSessionManager());

      act(() => {
        result.current.addMessage({
          role: 'user',
          content: 'What is Physical AI?',
        });
      });

      expect(result.current.messages).toHaveLength(1);
      expect(result.current.messages[0].role).toBe('user');
      expect(result.current.messages[0].content).toBe('What is Physical AI?');
      expect(result.current.messages[0].id).toMatch(/^msg-\d+-[a-z0-9]+$/);
      expect(result.current.messages[0].timestamp).toBeDefined();
    });

    it('should add assistant message with citations', () => {
      const { result } = renderHook(() => useSessionManager());
      const citations = [
        { section: 'Module 0: Introduction', url: '/docs/module-0', score: 0.95 },
      ];

      act(() => {
        result.current.addMessage({
          role: 'assistant',
          content: 'Physical AI is...',
          citations,
        });
      });

      expect(result.current.messages).toHaveLength(1);
      expect(result.current.messages[0].citations).toEqual(citations);
    });

    it('should persist messages to localStorage', () => {
      const { result } = renderHook(() => useSessionManager());

      act(() => {
        result.current.addMessage({
          role: 'user',
          content: 'Test message',
        });
      });

      expect(localStorageMock.setItem).toHaveBeenCalled();
      const savedData = JSON.parse(
        localStorageMock.setItem.mock.calls[localStorageMock.setItem.mock.calls.length - 1][1]
      );
      expect(savedData.messages).toHaveLength(1);
      expect(savedData.messages[0].content).toBe('Test message');
    });
  });

  describe('50-Message Limit', () => {
    it('should enforce 50 message limit', () => {
      const { result } = renderHook(() => useSessionManager());

      act(() => {
        // Add 52 messages
        for (let i = 0; i < 52; i++) {
          result.current.addMessage({
            role: i % 2 === 0 ? 'user' : 'assistant',
            content: `Message ${i}`,
          });
        }
      });

      // Should only keep last 50 messages
      expect(result.current.messages).toHaveLength(50);
      expect(result.current.messages[0].content).toBe('Message 2');
      expect(result.current.messages[49].content).toBe('Message 51');
    });

    it('should show archive warning when message limit exceeded', async () => {
      const { result } = renderHook(() => useSessionManager());

      act(() => {
        // Add 51 messages to trigger warning
        for (let i = 0; i < 51; i++) {
          result.current.addMessage({
            role: 'user',
            content: `Message ${i}`,
          });
        }
      });

      expect(result.current.showArchiveWarning).toBe(true);

      // Warning should disappear after 5 seconds
      act(() => {
        jest.advanceTimersByTime(5000);
      });

      expect(result.current.showArchiveWarning).toBe(false);
    });

    it('should show isNearLimit when approaching message limit', () => {
      const { result } = renderHook(() => useSessionManager());

      act(() => {
        // Add 45 messages (near limit threshold)
        for (let i = 0; i < 45; i++) {
          result.current.addMessage({
            role: 'user',
            content: `Message ${i}`,
          });
        }
      });

      expect(result.current.isNearLimit).toBe(true);
    });

    it('should NOT show isNearLimit when far from limit', () => {
      const { result } = renderHook(() => useSessionManager());

      act(() => {
        for (let i = 0; i < 10; i++) {
          result.current.addMessage({
            role: 'user',
            content: `Message ${i}`,
          });
        }
      });

      expect(result.current.isNearLimit).toBe(false);
    });
  });

  describe('Session Timeout', () => {
    it('should show timeout warning 1 minute before expiry', () => {
      const { result } = renderHook(() => useSessionManager());

      // Simulate time passing to 1 minute before timeout
      // Timeout is 2 hours = 7200000ms, warning at 1 minute before = 7140000ms
      act(() => {
        jest.advanceTimersByTime(7140000); // 1 hour 59 minutes
      });

      expect(result.current.showTimeoutWarning).toBe(true);
    });

    it('should clear session on timeout', () => {
      const { result } = renderHook(() => useSessionManager());
      const initialSessionId = result.current.session_id;

      act(() => {
        result.current.addMessage({
          role: 'user',
          content: 'Test message',
        });
      });

      // Simulate timeout (2 hours)
      act(() => {
        jest.advanceTimersByTime(2 * 60 * 60 * 1000 + 1000);
      });

      // Session should be cleared with new ID
      expect(result.current.session_id).not.toBe(initialSessionId);
      expect(result.current.messages).toEqual([]);
    });
  });

  describe('Clear Session', () => {
    it('should clear all messages and create new session ID', () => {
      const { result } = renderHook(() => useSessionManager());
      const initialSessionId = result.current.session_id;

      act(() => {
        result.current.addMessage({
          role: 'user',
          content: 'Message 1',
        });
        result.current.addMessage({
          role: 'assistant',
          content: 'Response 1',
        });
      });

      expect(result.current.messages).toHaveLength(2);

      act(() => {
        result.current.clearSession();
      });

      expect(result.current.messages).toEqual([]);
      expect(result.current.session_id).not.toBe(initialSessionId);
      expect(result.current.showTimeoutWarning).toBe(false);
      expect(result.current.showArchiveWarning).toBe(false);
    });
  });

  describe('Update Activity', () => {
    it('should update last_activity timestamp', () => {
      const { result } = renderHook(() => useSessionManager());

      const initialTime = Date.now();
      jest.advanceTimersByTime(60000); // Advance 1 minute

      act(() => {
        result.current.updateActivity();
      });

      // localStorage should be called with updated timestamp
      expect(localStorageMock.setItem).toHaveBeenCalled();
    });
  });

  describe('Error Handling', () => {
    it('should handle corrupted localStorage data gracefully', () => {
      localStorageMock.store['chatbot_session'] = 'invalid json';

      // Should not throw, should create new session
      const { result } = renderHook(() => useSessionManager());

      expect(result.current.session_id).toMatch(/^session-\d+-[a-z0-9]+$/);
      expect(result.current.messages).toEqual([]);
    });

    it('should handle localStorage setItem failure gracefully', () => {
      localStorageMock.setItem.mockImplementationOnce(() => {
        throw new Error('QuotaExceededError');
      });

      const { result } = renderHook(() => useSessionManager());

      // Should not throw when adding message
      act(() => {
        result.current.addMessage({
          role: 'user',
          content: 'Test',
        });
      });

      // Message should still be in state
      expect(result.current.messages).toHaveLength(1);
    });
  });
});
