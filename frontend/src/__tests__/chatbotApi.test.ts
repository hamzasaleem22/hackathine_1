/**
 * Unit tests for chatbotApi service.
 *
 * Tests API client using mocked fetch (error handling, retries, timeout).
 */
import {
  fetchQuery,
  fetchContentStatus,
  checkConnection,
  NetworkError,
  TimeoutError,
  QueryRequest,
  QueryResponse,
  ContentStatus,
} from '../services/chatbotApi';

// Mock fetch globally
const mockFetch = jest.fn();
global.fetch = mockFetch;

describe('chatbotApi', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  describe('fetchQuery', () => {
    const mockSuccessResponse: QueryResponse = {
      answer: 'Physical AI is a field that combines...',
      citations: [
        {
          section: 'Module 0: Introduction',
          url: '/docs/module-0',
          score: 0.95,
        },
      ],
      confidence: 0.9,
      message_id: 'msg-123',
      response_time_ms: 250,
    };

    it('should successfully fetch query response', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockSuccessResponse,
      });

      const request: QueryRequest = {
        question: 'What is Physical AI?',
        session_id: 'session-123',
      };

      const promise = fetchQuery(request);
      jest.runAllTimers();
      const result = await promise;

      expect(result).toEqual(mockSuccessResponse);
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/query'),
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(request),
        })
      );
    });

    it('should include context in request when provided', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockSuccessResponse,
      });

      const request: QueryRequest = {
        question: 'What does this mean?',
        session_id: 'session-123',
        context: 'Physical AI combines robotics and machine learning.',
      };

      const promise = fetchQuery(request);
      jest.runAllTimers();
      await promise;

      const callBody = JSON.parse(mockFetch.mock.calls[0][1].body);
      expect(callBody.context).toBe('Physical AI combines robotics and machine learning.');
    });

    it('should throw error for empty question', async () => {
      const request: QueryRequest = {
        question: '',
        session_id: 'session-123',
      };

      await expect(fetchQuery(request)).rejects.toThrow('Question cannot be empty');
    });

    it('should throw error for whitespace-only question', async () => {
      const request: QueryRequest = {
        question: '   ',
        session_id: 'session-123',
      };

      await expect(fetchQuery(request)).rejects.toThrow('Question cannot be empty');
    });

    it('should throw error for question exceeding 2000 characters', async () => {
      const request: QueryRequest = {
        question: 'a'.repeat(2001),
        session_id: 'session-123',
      };

      await expect(fetchQuery(request)).rejects.toThrow('Question must be 2000 characters or less');
    });

    it('should handle 429 rate limit response', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 429,
        headers: {
          get: (name: string) => (name === 'Retry-After' ? '60' : null),
        },
      });

      const request: QueryRequest = {
        question: 'Test question',
        session_id: 'session-123',
      };

      const promise = fetchQuery(request);
      jest.runAllTimers();

      await expect(promise).rejects.toThrow('Rate limit exceeded. Please try again in 60 seconds.');
    });

    it('should handle 500 server error', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
      });

      const request: QueryRequest = {
        question: 'Test question',
        session_id: 'session-123',
      };

      const promise = fetchQuery(request);
      jest.runAllTimers();

      await expect(promise).rejects.toThrow('Server error - please try again later');
    });

    it('should handle API error response with detail', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
        json: async () => ({ detail: 'Invalid request format' }),
      });

      const request: QueryRequest = {
        question: 'Test question',
        session_id: 'session-123',
      };

      const promise = fetchQuery(request);
      jest.runAllTimers();

      await expect(promise).rejects.toThrow('Invalid request format');
    });

    it('should throw NetworkError on fetch failure', async () => {
      mockFetch.mockRejectedValueOnce(new Error('Network failure'));

      const request: QueryRequest = {
        question: 'Test question',
        session_id: 'session-123',
      };

      const promise = fetchQuery(request);
      jest.runAllTimers();

      await expect(promise).rejects.toThrow(NetworkError);
    });

    it('should throw TimeoutError when request times out', async () => {
      // Create an abort error to simulate timeout
      const abortError = new Error('Aborted');
      abortError.name = 'AbortError';
      mockFetch.mockRejectedValueOnce(abortError);

      const request: QueryRequest = {
        question: 'Test question',
        session_id: 'session-123',
      };

      const promise = fetchQuery(request);
      jest.runAllTimers();

      await expect(promise).rejects.toThrow(TimeoutError);
    });

    it('should preserve NetworkError when thrown', async () => {
      mockFetch.mockRejectedValueOnce(new NetworkError('Connection lost'));

      const request: QueryRequest = {
        question: 'Test question',
        session_id: 'session-123',
      };

      const promise = fetchQuery(request);
      jest.runAllTimers();

      await expect(promise).rejects.toBeInstanceOf(NetworkError);
    });

    it('should preserve TimeoutError when thrown', async () => {
      mockFetch.mockRejectedValueOnce(new TimeoutError('Request timed out'));

      const request: QueryRequest = {
        question: 'Test question',
        session_id: 'session-123',
      };

      const promise = fetchQuery(request);
      jest.runAllTimers();

      await expect(promise).rejects.toBeInstanceOf(TimeoutError);
    });
  });

  describe('fetchContentStatus', () => {
    const mockContentStatus: ContentStatus = {
      last_updated: '2026-02-12',
      content_version: 'v1.0.0',
      indexed_modules: ['module-0'],
      total_chunks: 25,
      indexing_complete: true,
    };

    it('should successfully fetch content status', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockContentStatus,
      });

      const promise = fetchContentStatus();
      jest.runAllTimers();
      const result = await promise;

      expect(result).toEqual(mockContentStatus);
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/content-status'),
        expect.objectContaining({
          method: 'GET',
        })
      );
    });

    it('should return default status on error', async () => {
      mockFetch.mockRejectedValueOnce(new Error('Network error'));

      const promise = fetchContentStatus();
      jest.runAllTimers();
      const result = await promise;

      expect(result.indexing_complete).toBe(false);
      expect(result.indexed_modules).toEqual([]);
      expect(result.total_chunks).toBe(0);
      expect(result.content_version).toBe('unknown');
    });

    it('should return default status on non-ok response', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
      });

      const promise = fetchContentStatus();
      jest.runAllTimers();
      const result = await promise;

      expect(result.indexing_complete).toBe(false);
    });
  });

  describe('checkConnection', () => {
    it('should return true when health check succeeds', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
      });

      const promise = checkConnection();
      jest.runAllTimers();
      const result = await promise;

      expect(result).toBe(true);
      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining('/health'),
        expect.objectContaining({
          method: 'GET',
        })
      );
    });

    it('should return false when health check fails', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
      });

      const promise = checkConnection();
      jest.runAllTimers();
      const result = await promise;

      expect(result).toBe(false);
    });

    it('should return false on network error', async () => {
      mockFetch.mockRejectedValueOnce(new Error('Network error'));

      const promise = checkConnection();
      jest.runAllTimers();
      const result = await promise;

      expect(result).toBe(false);
    });
  });

  describe('Error Classes', () => {
    it('should create NetworkError with correct name', () => {
      const error = new NetworkError('Connection failed');
      expect(error.name).toBe('NetworkError');
      expect(error.message).toBe('Connection failed');
      expect(error).toBeInstanceOf(Error);
    });

    it('should create TimeoutError with correct name', () => {
      const error = new TimeoutError('Request timed out');
      expect(error.name).toBe('TimeoutError');
      expect(error.message).toBe('Request timed out');
      expect(error).toBeInstanceOf(Error);
    });
  });
});
