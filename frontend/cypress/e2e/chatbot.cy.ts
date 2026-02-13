/**
 * E2E tests for Chatbot basic Q&A flow.
 *
 * Tests the complete user journey of asking questions and receiving answers.
 */

describe('Chatbot Q&A Flow', () => {
  beforeEach(() => {
    // Visit the homepage
    cy.visit('/');

    // Intercept API calls to mock responses
    cy.intercept('POST', '**/api/query', {
      statusCode: 200,
      body: {
        answer: 'Physical AI is a field that combines artificial intelligence with physical systems and robotics.',
        citations: [
          { section: 'Module 0: Introduction', url: '/docs/module-0', score: 0.95 },
          { section: 'Module 1: Foundations', url: '/docs/module-1', score: 0.85 },
        ],
        confidence: 0.92,
        message_id: 'msg-test-123',
        response_time_ms: 150,
      },
      delay: 500, // Simulate network delay
    }).as('queryApi');
  });

  describe('Opening and Closing Chatbot', () => {
    it('should display chatbot button on page load', () => {
      cy.get('[data-testid="chatbot-button"]').should('be.visible');
    });

    it('should open chatbot when button is clicked', () => {
      cy.get('[data-testid="chatbot-button"]').click();
      cy.get('[role="dialog"][aria-label="Chatbot"]').should('be.visible');
      cy.contains('Physical AI Assistant').should('be.visible');
    });

    it('should close chatbot when close button is clicked', () => {
      // Open chatbot
      cy.get('[data-testid="chatbot-button"]').click();
      cy.get('[role="dialog"]').should('be.visible');

      // Close chatbot
      cy.contains('button', '✕').click();
      cy.get('[role="dialog"]').should('not.exist');
      cy.get('[data-testid="chatbot-button"]').should('be.visible');
    });

    it('should close chatbot when Escape key is pressed', () => {
      // Open chatbot
      cy.get('[data-testid="chatbot-button"]').click();
      cy.get('[role="dialog"]').should('be.visible');

      // Press Escape
      cy.get('body').type('{esc}');
      cy.get('[role="dialog"]').should('not.exist');
    });
  });

  describe('Basic Q&A Interaction', () => {
    beforeEach(() => {
      // Open chatbot before each test
      cy.get('[data-testid="chatbot-button"]').click();
      cy.get('[role="dialog"]').should('be.visible');
    });

    it('should display empty state message initially', () => {
      cy.contains('Ask me anything about the Physical AI Textbook!').should('be.visible');
    });

    it('should send a question and receive a response', () => {
      // Type a question
      cy.get('[data-testid="chatbot-input"]').type('What is Physical AI?');
      cy.get('[data-testid="chatbot-submit"]').click();

      // Verify user message appears
      cy.get('[data-testid="user-message"]').should('contain', 'What is Physical AI?');

      // Wait for loading indicator
      cy.get('[data-testid="message-loading"]').should('be.visible');

      // Wait for response
      cy.wait('@queryApi');

      // Verify bot response appears
      cy.get('[data-testid="assistant-message"]', { timeout: 10000 })
        .should('be.visible')
        .and('contain', 'Physical AI is a field');

      // Loading indicator should be gone
      cy.get('[data-testid="message-loading"]').should('not.exist');
    });

    it('should display citations with the response', () => {
      // Send a question
      cy.get('[data-testid="chatbot-input"]').type('What is Physical AI?');
      cy.get('[data-testid="chatbot-submit"]').click();

      // Wait for response
      cy.wait('@queryApi');

      // Verify citations are displayed
      cy.get('[data-testid="citation-link"]').should('have.length.at.least', 1);
      cy.contains('Module 0: Introduction').should('be.visible');
    });

    it('should submit question on Enter key press', () => {
      // Type question and press Enter
      cy.get('[data-testid="chatbot-input"]').type('What is Physical AI?{enter}');

      // Verify question was sent
      cy.get('[data-testid="user-message"]').should('contain', 'What is Physical AI?');
      cy.wait('@queryApi');
    });

    it('should allow Shift+Enter for new line without submitting', () => {
      // Type multi-line question
      cy.get('[data-testid="chatbot-input"]').type('Line 1{shift+enter}Line 2');

      // Should not submit
      cy.get('[data-testid="user-message"]').should('not.exist');

      // Input should contain both lines
      cy.get('[data-testid="chatbot-input"]').should('contain.value', 'Line 1');
    });

    it('should not submit empty message', () => {
      // Click submit without typing
      cy.get('[data-testid="chatbot-submit"]').should('be.disabled');

      // Type only spaces
      cy.get('[data-testid="chatbot-input"]').type('   ');
      cy.get('[data-testid="chatbot-submit"]').should('be.disabled');
    });

    it('should clear input after sending message', () => {
      // Send a message
      cy.get('[data-testid="chatbot-input"]').type('Test question');
      cy.get('[data-testid="chatbot-submit"]').click();

      // Input should be cleared
      cy.get('[data-testid="chatbot-input"]').should('have.value', '');
    });
  });

  describe('Conversation History', () => {
    beforeEach(() => {
      cy.get('[data-testid="chatbot-button"]').click();
    });

    it('should maintain conversation history across multiple questions', () => {
      // First question
      cy.get('[data-testid="chatbot-input"]').type('What is Physical AI?');
      cy.get('[data-testid="chatbot-submit"]').click();
      cy.wait('@queryApi');

      // Update mock for second question
      cy.intercept('POST', '**/api/query', {
        statusCode: 200,
        body: {
          answer: 'Embodied AI refers to AI systems that interact with the physical world through a body.',
          citations: [],
          confidence: 0.88,
          message_id: 'msg-test-456',
        },
      }).as('queryApi2');

      // Second question
      cy.get('[data-testid="chatbot-input"]').type('What is embodied AI?');
      cy.get('[data-testid="chatbot-submit"]').click();
      cy.wait('@queryApi2');

      // Both Q&A pairs should be visible
      cy.get('[data-testid="user-message"]').should('have.length', 2);
      cy.get('[data-testid="assistant-message"]').should('have.length', 2);
    });

    it('should include conversation history in API request', () => {
      // First question
      cy.get('[data-testid="chatbot-input"]').type('What is Physical AI?');
      cy.get('[data-testid="chatbot-submit"]').click();
      cy.wait('@queryApi');

      // Intercept and verify second request includes history
      cy.intercept('POST', '**/api/query', (req) => {
        expect(req.body).to.have.property('conversation_history');
        expect(req.body.conversation_history).to.have.length.at.least(1);
        req.reply({
          answer: 'Follow-up response',
          citations: [],
          confidence: 0.9,
        });
      }).as('queryWithHistory');

      // Second question
      cy.get('[data-testid="chatbot-input"]').type('Tell me more');
      cy.get('[data-testid="chatbot-submit"]').click();
      cy.wait('@queryWithHistory');
    });
  });

  describe('Clear Chat Functionality', () => {
    beforeEach(() => {
      cy.get('[data-testid="chatbot-button"]').click();
    });

    it('should clear all messages when Clear button is clicked', () => {
      // Send a message first
      cy.get('[data-testid="chatbot-input"]').type('Test question');
      cy.get('[data-testid="chatbot-submit"]').click();
      cy.wait('@queryApi');

      // Verify message exists
      cy.get('[data-testid="user-message"]').should('exist');

      // Click Clear button
      cy.contains('button', 'Clear').click();

      // Messages should be cleared
      cy.get('[data-testid="user-message"]').should('not.exist');
      cy.get('[data-testid="assistant-message"]').should('not.exist');

      // Empty state should reappear
      cy.contains('Ask me anything about the Physical AI Textbook!').should('be.visible');
    });
  });

  describe('Error Handling', () => {
    beforeEach(() => {
      cy.get('[data-testid="chatbot-button"]').click();
    });

    it('should display error message when API fails', () => {
      // Mock API error
      cy.intercept('POST', '**/api/query', {
        statusCode: 500,
        body: { error: 'Internal server error' },
      }).as('queryApiError');

      // Send a message
      cy.get('[data-testid="chatbot-input"]').type('Test question');
      cy.get('[data-testid="chatbot-submit"]').click();

      // Wait for error response
      cy.wait('@queryApiError');

      // Should show error message in chat
      cy.get('[data-testid="assistant-message"]')
        .should('be.visible')
        .and('contain', 'Sorry, I encountered an error');
    });

    it('should handle network timeout gracefully', () => {
      // Mock network timeout
      cy.intercept('POST', '**/api/query', {
        forceNetworkError: true,
      }).as('queryApiTimeout');

      // Send a message
      cy.get('[data-testid="chatbot-input"]').type('Test question');
      cy.get('[data-testid="chatbot-submit"]').click();

      // Should show error message
      cy.get('[data-testid="assistant-message"]', { timeout: 15000 })
        .should('be.visible')
        .and('contain', 'error');
    });
  });

  describe('Session Management', () => {
    it('should include session_id in API requests', () => {
      cy.get('[data-testid="chatbot-button"]').click();

      // Intercept and verify session_id
      cy.intercept('POST', '**/api/query', (req) => {
        expect(req.body).to.have.property('session_id');
        expect(req.body.session_id).to.match(/^session-\d+$/);
        req.reply({
          answer: 'Test response',
          citations: [],
          confidence: 0.9,
        });
      }).as('queryWithSession');

      cy.get('[data-testid="chatbot-input"]').type('Test question');
      cy.get('[data-testid="chatbot-submit"]').click();
      cy.wait('@queryWithSession');
    });

    it('should use consistent session_id across multiple messages', () => {
      cy.get('[data-testid="chatbot-button"]').click();

      let capturedSessionId: string;

      // First request - capture session_id
      cy.intercept('POST', '**/api/query', (req) => {
        capturedSessionId = req.body.session_id;
        req.reply({
          answer: 'First response',
          citations: [],
        });
      }).as('firstQuery');

      cy.get('[data-testid="chatbot-input"]').type('First question');
      cy.get('[data-testid="chatbot-submit"]').click();
      cy.wait('@firstQuery');

      // Second request - verify same session_id
      cy.intercept('POST', '**/api/query', (req) => {
        expect(req.body.session_id).to.equal(capturedSessionId);
        req.reply({
          answer: 'Second response',
          citations: [],
        });
      }).as('secondQuery');

      cy.get('[data-testid="chatbot-input"]').type('Second question');
      cy.get('[data-testid="chatbot-submit"]').click();
      cy.wait('@secondQuery');
    });
  });

  describe('UI Elements and Accessibility', () => {
    beforeEach(() => {
      cy.get('[data-testid="chatbot-button"]').click();
    });

    it('should have proper dialog accessibility attributes', () => {
      cy.get('[role="dialog"]')
        .should('have.attr', 'aria-label', 'Chatbot');
    });

    it('should display header with title', () => {
      cy.contains('Physical AI Assistant').should('be.visible');
    });

    it('should display footer with powered by text', () => {
      cy.contains('Powered by Physical AI Textbook').should('be.visible');
    });

    it('should focus input field when chatbot opens', () => {
      // Input should be focused (or at least visible and interactable)
      cy.get('[data-testid="chatbot-input"]')
        .should('be.visible')
        .and('not.be.disabled');
    });
  });
});
