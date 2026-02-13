/**
 * Chatbot API service for querying the RAG backend.
 */

const API_URL = process.env.REACT_APP_API_URL || 'https://backend-vert-zeta-89.vercel.app';
const TIMEOUT_MS = 30000; // 30 seconds

export interface QueryRequest {
  question: string;
  session_id?: string;
  context?: string;
}

export interface Citation {
  section: string;
  url: string;
  score: number;
  module_id?: string;
  chapter_id?: string;
}

export interface QueryResponse {
  answer: string;
  citations: Citation[];
  confidence: number;
  message_id: string;
  response_time_ms: number;
}

export interface ContentStatus {
  last_updated: string;
  content_version: string;
  indexed_modules: string[];
  total_chunks: number;
  indexing_complete: boolean;
}

export class NetworkError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'NetworkError';
  }
}

export class TimeoutError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'TimeoutError';
  }
}

/**
 * Fetch with timeout wrapper
 */
async function fetchWithTimeout(
  url: string,
  options: RequestInit,
  timeout: number = TIMEOUT_MS
): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    });
    clearTimeout(timeoutId);
    return response;
  } catch (error) {
    clearTimeout(timeoutId);
    if (error.name === 'AbortError') {
      throw new TimeoutError('Request timeout - server took too long to respond');
    }
    throw new NetworkError('Network request failed - check your connection');
  }
}

/**
 * Query the chatbot with a question
 */
export async function fetchQuery(request: QueryRequest): Promise<QueryResponse> {
  // Validate question
  if (!request.question || request.question.trim().length === 0) {
    throw new Error('Question cannot be empty');
  }

  if (request.question.length > 2000) {
    throw new Error('Question must be 2000 characters or less');
  }

  try {
    const response = await fetchWithTimeout(
      `${API_URL}/api/query`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      },
      TIMEOUT_MS
    );

    if (!response.ok) {
      if (response.status === 429) {
        const retryAfter = response.headers.get('Retry-After');
        throw new Error(
          `Rate limit exceeded. Please try again in ${retryAfter || '60'} seconds.`
        );
      }

      if (response.status >= 500) {
        throw new Error('Server error - please try again later');
      }

      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Failed to process query');
    }

    const data: QueryResponse = await response.json();
    return data;
  } catch (error) {
    if (error instanceof NetworkError || error instanceof TimeoutError) {
      throw error;
    }
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Unknown error occurred');
  }
}

/**
 * Get content indexing status
 */
export async function fetchContentStatus(): Promise<ContentStatus> {
  try {
    const response = await fetchWithTimeout(
      `${API_URL}/api/content-status`,
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      },
      10000 // 10 second timeout for status check
    );

    if (!response.ok) {
      throw new Error('Failed to fetch content status');
    }

    const data: ContentStatus = await response.json();
    return data;
  } catch (error) {
    // Return default status on error
    return {
      last_updated: new Date().toISOString().split('T')[0],
      content_version: 'unknown',
      indexed_modules: [],
      total_chunks: 0,
      indexing_complete: false,
    };
  }
}

/**
 * Check if backend is online
 */
export async function checkConnection(): Promise<boolean> {
  try {
    const response = await fetchWithTimeout(
      `${API_URL}/health`,
      {
        method: 'GET',
      },
      5000 // 5 second timeout
    );
    return response.ok;
  } catch {
    return false;
  }
}
