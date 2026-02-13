/**
 * Unit tests for ChatbotWidget component.
 *
 * Tests UI rendering, user interactions, and state management.
 */
import React from 'react';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ChatbotWidget } from '../components/Chatbot/ChatbotWidget';

// Mock CSS module
jest.mock('../components/Chatbot/ChatbotWidget.module.css', () => ({
  chatbotWidget: 'chatbotWidget',
  header: 'header',
  title: 'title',
  headerActions: 'headerActions',
  clearButton: 'clearButton',
  closeButton: 'closeButton',
  contextBanner: 'contextBanner',
  contextLabel: 'contextLabel',
  contextText: 'contextText',
  messagesContainer: 'messagesContainer',
  inputContainer: 'inputContainer',
  footer: 'footer',
  contentInfo: 'contentInfo',
}));

// Mock child components
jest.mock('../components/Chatbot/ChatbotButton', () => ({
  ChatbotButton: ({ onClick, isOpen }: { onClick: () => void; isOpen: boolean }) => (
    <button data-testid="chatbot-button" onClick={onClick}>
      {isOpen ? 'Close' : 'Open'} Chatbot
    </button>
  ),
}));

jest.mock('../components/Chatbot/MessageList', () => ({
  MessageList: ({ messages, isLoading }: { messages: any[]; isLoading: boolean }) => (
    <div data-testid="message-list">
      {messages.map((msg: any, index: number) => (
        <div key={msg.id || index} data-testid={`message-${msg.role}`}>
          {msg.content}
        </div>
      ))}
      {isLoading && <div data-testid="loading">Loading...</div>}
    </div>
  ),
}));

jest.mock('../components/Chatbot/InputField', () => ({
  InputField: ({
    onSubmit,
    disabled,
    placeholder,
  }: {
    onSubmit: (text: string) => void;
    disabled: boolean;
    placeholder: string;
  }) => (
    <div data-testid="input-field">
      <input
        data-testid="chatbot-input"
        placeholder={placeholder}
        disabled={disabled}
        onKeyDown={(e) => {
          if (e.key === 'Enter' && !e.shiftKey) {
            const input = e.target as HTMLInputElement;
            onSubmit(input.value);
            input.value = '';
          }
        }}
      />
      <button
        data-testid="submit-button"
        onClick={() => {
          const input = document.querySelector('[data-testid="chatbot-input"]') as HTMLInputElement;
          if (input && input.value.trim()) {
            onSubmit(input.value);
            input.value = '';
          }
        }}
        disabled={disabled}
      >
        Send
      </button>
    </div>
  ),
}));

jest.mock('../components/Chatbot/AskAboutButton', () => ({
  AskAboutButton: ({
    onClick,
    visible,
    position,
  }: {
    onClick: () => void;
    visible: boolean;
    position: { x: number; y: number } | null;
  }) =>
    visible && position ? (
      <button data-testid="ask-about-button" onClick={onClick}>
        Ask about this
      </button>
    ) : null,
}));

// Mock useTextSelection hook
const mockUseTextSelection = {
  selectedText: '',
  isValid: false,
  position: null as { x: number; y: number } | null,
  clearSelection: jest.fn(),
  isTooShort: false,
};

jest.mock('../hooks/useTextSelection', () => ({
  useTextSelection: () => mockUseTextSelection,
}));

// Mock fetch API
const mockFetch = jest.fn();
global.fetch = mockFetch;

describe('ChatbotWidget', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockFetch.mockReset();
    // Reset text selection mock
    mockUseTextSelection.selectedText = '';
    mockUseTextSelection.isValid = false;
    mockUseTextSelection.position = null;
    mockUseTextSelection.isTooShort = false;
    mockUseTextSelection.clearSelection = jest.fn();
  });

  describe('Initial Rendering', () => {
    it('should render chatbot button when closed', () => {
      render(<ChatbotWidget />);

      expect(screen.getByTestId('chatbot-button')).toBeInTheDocument();
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    });

    it('should not render the modal initially', () => {
      render(<ChatbotWidget />);

      expect(screen.queryByText('Physical AI Assistant')).not.toBeInTheDocument();
    });
  });

  describe('Open/Close Behavior', () => {
    it('should open chatbot modal when button is clicked', () => {
      render(<ChatbotWidget />);

      fireEvent.click(screen.getByTestId('chatbot-button'));

      expect(screen.getByRole('dialog')).toBeInTheDocument();
      expect(screen.getByText('Physical AI Assistant')).toBeInTheDocument();
    });

    it('should hide chatbot button when modal is open', () => {
      render(<ChatbotWidget />);

      fireEvent.click(screen.getByTestId('chatbot-button'));

      expect(screen.queryByTestId('chatbot-button')).not.toBeInTheDocument();
    });

    it('should close chatbot modal when close button is clicked', () => {
      render(<ChatbotWidget />);

      // Open the chatbot
      fireEvent.click(screen.getByTestId('chatbot-button'));
      expect(screen.getByRole('dialog')).toBeInTheDocument();

      // Close it
      fireEvent.click(screen.getByText('✕'));

      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
      expect(screen.getByTestId('chatbot-button')).toBeInTheDocument();
    });

    it('should close chatbot modal on Escape key press', () => {
      render(<ChatbotWidget />);

      // Open the chatbot
      fireEvent.click(screen.getByTestId('chatbot-button'));
      expect(screen.getByRole('dialog')).toBeInTheDocument();

      // Press Escape
      fireEvent.keyDown(document, { key: 'Escape' });

      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    });

    it('should not close on Escape when already closed', () => {
      render(<ChatbotWidget />);

      // Press Escape when closed
      fireEvent.keyDown(document, { key: 'Escape' });

      // Should still be closed, button still visible
      expect(screen.getByTestId('chatbot-button')).toBeInTheDocument();
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    });
  });

  describe('Message Sending', () => {
    beforeEach(() => {
      mockFetch.mockResolvedValue({
        ok: true,
        json: () =>
          Promise.resolve({
            answer: 'Physical AI is a field that combines...',
            citations: [{ section: 'Module 0', url: '/docs/module-0', score: 0.95 }],
          }),
      });
    });

    it('should send message and display response', async () => {
      render(<ChatbotWidget />);

      // Open chatbot
      fireEvent.click(screen.getByTestId('chatbot-button'));

      // Type and submit message
      const input = screen.getByTestId('chatbot-input') as HTMLInputElement;
      fireEvent.change(input, { target: { value: 'What is Physical AI?' } });
      fireEvent.keyDown(input, { key: 'Enter' });

      // Wait for API response
      await waitFor(() => {
        expect(screen.getByTestId('message-user')).toHaveTextContent('What is Physical AI?');
      });

      await waitFor(() => {
        expect(screen.getByTestId('message-assistant')).toHaveTextContent(
          'Physical AI is a field that combines...'
        );
      });
    });

    it('should show loading state while sending message', async () => {
      mockFetch.mockImplementation(
        () =>
          new Promise((resolve) =>
            setTimeout(
              () =>
                resolve({
                  ok: true,
                  json: () => Promise.resolve({ answer: 'Response', citations: [] }),
                }),
              100
            )
          )
      );

      render(<ChatbotWidget />);

      // Open and send message
      fireEvent.click(screen.getByTestId('chatbot-button'));
      const input = screen.getByTestId('chatbot-input') as HTMLInputElement;
      fireEvent.change(input, { target: { value: 'Test question' } });
      fireEvent.keyDown(input, { key: 'Enter' });

      // Should show loading state
      await waitFor(() => {
        expect(screen.getByTestId('loading')).toBeInTheDocument();
      });

      // Wait for response
      await waitFor(
        () => {
          expect(screen.queryByTestId('loading')).not.toBeInTheDocument();
        },
        { timeout: 200 }
      );
    });

    it('should handle API error gracefully', async () => {
      mockFetch.mockResolvedValue({
        ok: false,
        status: 500,
      });

      render(<ChatbotWidget />);

      // Open and send message
      fireEvent.click(screen.getByTestId('chatbot-button'));
      const input = screen.getByTestId('chatbot-input') as HTMLInputElement;
      fireEvent.change(input, { target: { value: 'Test question' } });
      fireEvent.keyDown(input, { key: 'Enter' });

      // Should show error message
      await waitFor(() => {
        expect(screen.getByTestId('message-assistant')).toHaveTextContent(
          'Sorry, I encountered an error. Please try again.'
        );
      });
    });

    it('should handle network error gracefully', async () => {
      mockFetch.mockRejectedValue(new Error('Network error'));

      render(<ChatbotWidget />);

      // Open and send message
      fireEvent.click(screen.getByTestId('chatbot-button'));
      const input = screen.getByTestId('chatbot-input') as HTMLInputElement;
      fireEvent.change(input, { target: { value: 'Test question' } });
      fireEvent.keyDown(input, { key: 'Enter' });

      // Should show error message
      await waitFor(() => {
        expect(screen.getByTestId('message-assistant')).toHaveTextContent(
          'Sorry, I encountered an error. Please try again.'
        );
      });
    });

    it('should include context in API request when provided', async () => {
      mockUseTextSelection.selectedText = 'Selected text for context';
      mockUseTextSelection.isValid = true;
      mockUseTextSelection.position = { x: 100, y: 100 };

      render(<ChatbotWidget />);

      // Open and send message
      fireEvent.click(screen.getByTestId('chatbot-button'));
      const input = screen.getByTestId('chatbot-input') as HTMLInputElement;
      fireEvent.change(input, { target: { value: 'What does this mean?' } });
      fireEvent.keyDown(input, { key: 'Enter' });

      await waitFor(() => {
        expect(mockFetch).toHaveBeenCalledWith(
          'http://127.0.0.1:8000/api/query',
          expect.objectContaining({
            method: 'POST',
            body: expect.stringContaining('Selected text for context'),
          })
        );
      });
    });
  });

  describe('Clear Chat', () => {
    it('should clear all messages when Clear button is clicked', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ answer: 'Test response', citations: [] }),
      });

      render(<ChatbotWidget />);

      // Open and send a message
      fireEvent.click(screen.getByTestId('chatbot-button'));
      const input = screen.getByTestId('chatbot-input') as HTMLInputElement;
      fireEvent.change(input, { target: { value: 'Test question' } });
      fireEvent.keyDown(input, { key: 'Enter' });

      // Wait for response
      await waitFor(() => {
        expect(screen.getByTestId('message-user')).toBeInTheDocument();
      });

      // Click Clear button
      fireEvent.click(screen.getByText('Clear'));

      // Messages should be cleared
      expect(screen.queryByTestId('message-user')).not.toBeInTheDocument();
      expect(screen.queryByTestId('message-assistant')).not.toBeInTheDocument();
    });
  });

  describe('Text Selection (User Story 2)', () => {
    it('should show Ask About button when text is selected', () => {
      mockUseTextSelection.selectedText = 'Selected text for testing';
      mockUseTextSelection.isValid = true;
      mockUseTextSelection.position = { x: 100, y: 100 };

      render(<ChatbotWidget />);

      expect(screen.getByTestId('ask-about-button')).toBeInTheDocument();
    });

    it('should not show Ask About button when no valid selection', () => {
      mockUseTextSelection.selectedText = '';
      mockUseTextSelection.isValid = false;
      mockUseTextSelection.position = null;

      render(<ChatbotWidget />);

      expect(screen.queryByTestId('ask-about-button')).not.toBeInTheDocument();
    });

    it('should not show Ask About button when chatbot is open', () => {
      mockUseTextSelection.selectedText = 'Selected text';
      mockUseTextSelection.isValid = true;
      mockUseTextSelection.position = { x: 100, y: 100 };

      render(<ChatbotWidget />);

      // Open chatbot
      fireEvent.click(screen.getByTestId('chatbot-button'));

      // Ask About button should be hidden when chatbot is open
      expect(screen.queryByTestId('ask-about-button')).not.toBeInTheDocument();
    });

    it('should open chatbot when Ask About button is clicked and chatbot is closed', () => {
      mockUseTextSelection.selectedText = 'Selected text for testing';
      mockUseTextSelection.isValid = true;
      mockUseTextSelection.position = { x: 100, y: 100 };

      render(<ChatbotWidget />);

      fireEvent.click(screen.getByTestId('ask-about-button'));

      expect(screen.getByRole('dialog')).toBeInTheDocument();
      expect(mockUseTextSelection.clearSelection).toHaveBeenCalled();
    });

    it('should show "too short" tooltip when selection is too short', () => {
      mockUseTextSelection.selectedText = 'Short';
      mockUseTextSelection.isValid = false;
      mockUseTextSelection.position = { x: 100, y: 100 };
      mockUseTextSelection.isTooShort = true;

      render(<ChatbotWidget />);

      expect(screen.getByText('Select more text (min 10 characters)')).toBeInTheDocument();
    });

    it('should not show "too short" tooltip when chatbot is open', () => {
      mockUseTextSelection.selectedText = 'Short';
      mockUseTextSelection.isValid = false;
      mockUseTextSelection.position = { x: 100, y: 100 };
      mockUseTextSelection.isTooShort = true;

      render(<ChatbotWidget />);

      // Open chatbot
      fireEvent.click(screen.getByTestId('chatbot-button'));

      expect(screen.queryByText('Select more text (min 10 characters)')).not.toBeInTheDocument();
    });
  });

  describe('Input Field Placeholder', () => {
    it('should show default placeholder when no text is selected', () => {
      mockUseTextSelection.selectedText = '';

      render(<ChatbotWidget />);
      fireEvent.click(screen.getByTestId('chatbot-button'));

      expect(screen.getByTestId('chatbot-input')).toHaveAttribute(
        'placeholder',
        'Ask a question about the textbook...'
      );
    });

    it('should show context placeholder when text is selected', () => {
      mockUseTextSelection.selectedText = 'Some selected text for context';
      mockUseTextSelection.isValid = true;

      render(<ChatbotWidget />);
      fireEvent.click(screen.getByTestId('chatbot-button'));

      expect(screen.getByTestId('chatbot-input')).toHaveAttribute(
        'placeholder',
        'Ask about the selected text...'
      );
    });
  });

  describe('UI Elements', () => {
    it('should render header with title', () => {
      render(<ChatbotWidget />);
      fireEvent.click(screen.getByTestId('chatbot-button'));

      expect(screen.getByText('Physical AI Assistant')).toBeInTheDocument();
    });

    it('should render Clear and Close buttons in header', () => {
      render(<ChatbotWidget />);
      fireEvent.click(screen.getByTestId('chatbot-button'));

      expect(screen.getByText('Clear')).toBeInTheDocument();
      expect(screen.getByText('✕')).toBeInTheDocument();
    });

    it('should render footer with powered by text', () => {
      render(<ChatbotWidget />);
      fireEvent.click(screen.getByTestId('chatbot-button'));

      expect(screen.getByText('Powered by Physical AI Textbook')).toBeInTheDocument();
    });

    it('should render message list component', () => {
      render(<ChatbotWidget />);
      fireEvent.click(screen.getByTestId('chatbot-button'));

      expect(screen.getByTestId('message-list')).toBeInTheDocument();
    });

    it('should render input field component', () => {
      render(<ChatbotWidget />);
      fireEvent.click(screen.getByTestId('chatbot-button'));

      expect(screen.getByTestId('input-field')).toBeInTheDocument();
    });

    it('should have proper accessibility attributes', () => {
      render(<ChatbotWidget />);
      fireEvent.click(screen.getByTestId('chatbot-button'));

      const dialog = screen.getByRole('dialog');
      expect(dialog).toHaveAttribute('aria-label', 'Chatbot');
    });
  });

  describe('Conversation History', () => {
    it('should include conversation history in subsequent requests', async () => {
      mockFetch
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve({ answer: 'First response', citations: [] }),
        })
        .mockResolvedValueOnce({
          ok: true,
          json: () => Promise.resolve({ answer: 'Second response', citations: [] }),
        });

      render(<ChatbotWidget />);
      fireEvent.click(screen.getByTestId('chatbot-button'));

      // Send first message
      const input = screen.getByTestId('chatbot-input') as HTMLInputElement;
      fireEvent.change(input, { target: { value: 'First question' } });
      fireEvent.keyDown(input, { key: 'Enter' });

      await waitFor(() => {
        expect(screen.getByTestId('message-assistant')).toHaveTextContent('First response');
      });

      // Send second message
      fireEvent.change(input, { target: { value: 'Follow-up question' } });
      fireEvent.keyDown(input, { key: 'Enter' });

      await waitFor(() => {
        expect(mockFetch).toHaveBeenCalledTimes(2);
      });

      // Second request should include conversation history
      const secondCallBody = JSON.parse(mockFetch.mock.calls[1][1].body);
      expect(secondCallBody.conversation_history).toBeDefined();
      expect(secondCallBody.conversation_history).toHaveLength(1);
      expect(secondCallBody.conversation_history[0].question).toBe('First question');
      expect(secondCallBody.conversation_history[0].answer).toBe('First response');
    });
  });

  describe('Session ID', () => {
    it('should include session_id in API requests', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ answer: 'Test response', citations: [] }),
      });

      render(<ChatbotWidget />);
      fireEvent.click(screen.getByTestId('chatbot-button'));

      const input = screen.getByTestId('chatbot-input') as HTMLInputElement;
      fireEvent.change(input, { target: { value: 'Test question' } });
      fireEvent.keyDown(input, { key: 'Enter' });

      await waitFor(() => {
        expect(mockFetch).toHaveBeenCalled();
      });

      const requestBody = JSON.parse(mockFetch.mock.calls[0][1].body);
      expect(requestBody.session_id).toBeDefined();
      expect(requestBody.session_id).toMatch(/^session-\d+$/);
    });
  });
});
