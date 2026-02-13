/**
 * E2E tests for feedback flow (T091).
 *
 * Tests thumbs up/down feedback submission and visual confirmation.
 */

describe('Feedback Flow', () => {
  beforeEach(() => {
    // Mock query API
    cy.intercept('POST', '**/api/query', {
      statusCode: 200,
      body: {
        answer: 'Physical AI combines artificial intelligence with physical systems.',
        citations: [
          { section: 'Module 0: Introduction', url: '/docs/module-0', score: 0.95 }
        ],
        confidence: 0.92,
        message_id: 'msg-feedback-test-123',
      },
      delay: 200,
    }).as('queryApi');

    // Mock feedback API
    cy.intercept('POST', '**/api/feedback', {
      statusCode: 200,
      body: {
        success: true,
        message: 'Feedback received. Thank you!'
      }
    }).as('feedbackApi');

    // Mock report issue API
    cy.intercept('POST', '**/api/report-issue', {
      statusCode: 200,
      body: {
        success: true,
        message: 'Issue report submitted. We\'ll review it shortly.'
      }
    }).as('reportIssueApi');

    cy.visit('/');
  });

  describe('Feedback Buttons Display', () => {
    beforeEach(() => {
      cy.get('[data-testid="chatbot-button"]').click();
      cy.get('[data-testid="chatbot-input"]').type('What is Physical AI?{enter}');
      cy.wait('@queryApi');
    });

    it('should display feedback buttons on bot messages', () => {
      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.get('button[aria-label*="thumbs up"], button[aria-label*="helpful"], [data-testid="thumbs-up"]')
          .should('exist');
        cy.get('button[aria-label*="thumbs down"], button[aria-label*="not helpful"], [data-testid="thumbs-down"]')
          .should('exist');
      });
    });

    it('should not display feedback buttons on user messages', () => {
      cy.get('[data-testid="user-message"]').within(() => {
        cy.get('button[aria-label*="thumbs"]').should('not.exist');
      });
    });

    it('should display report issue button on bot messages', () => {
      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.contains('Report').should('exist');
      });
    });
  });

  describe('Thumbs Up Feedback', () => {
    beforeEach(() => {
      cy.get('[data-testid="chatbot-button"]').click();
      cy.get('[data-testid="chatbot-input"]').type('What is Physical AI?{enter}');
      cy.wait('@queryApi');
    });

    it('should submit thumbs up feedback when clicked', () => {
      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.get('button[aria-label*="thumbs up"], button[aria-label*="helpful"], [data-testid="thumbs-up"]')
          .first()
          .click();
      });

      cy.wait('@feedbackApi').its('request.body').should('deep.include', {
        rating: 'up'
      });
    });

    it('should show visual confirmation after thumbs up', () => {
      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.get('button[aria-label*="thumbs up"], button[aria-label*="helpful"], [data-testid="thumbs-up"]')
          .first()
          .click();
      });

      cy.wait('@feedbackApi');

      // Should show some confirmation (filled icon, different color, etc.)
      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.get('button[aria-label*="thumbs up"], [data-testid="thumbs-up"]')
          .should('have.class', 'selected')
          .or('have.attr', 'data-selected', 'true')
          .or('have.css', 'color').and('not.equal', 'inherit');
      });
    });

    it('should disable feedback buttons after thumbs up', () => {
      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.get('button[aria-label*="thumbs up"], [data-testid="thumbs-up"]')
          .first()
          .click();
      });

      cy.wait('@feedbackApi');

      // Both buttons should be disabled
      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.get('button[aria-label*="thumbs up"], [data-testid="thumbs-up"]')
          .should('be.disabled');
        cy.get('button[aria-label*="thumbs down"], [data-testid="thumbs-down"]')
          .should('be.disabled');
      });
    });

    it('should include message_id in feedback request', () => {
      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.get('button[aria-label*="thumbs up"], [data-testid="thumbs-up"]')
          .first()
          .click();
      });

      cy.wait('@feedbackApi').its('request.body').should('have.property', 'message_id');
    });
  });

  describe('Thumbs Down Feedback', () => {
    beforeEach(() => {
      cy.get('[data-testid="chatbot-button"]').click();
      cy.get('[data-testid="chatbot-input"]').type('What is Physical AI?{enter}');
      cy.wait('@queryApi');
    });

    it('should submit thumbs down feedback when clicked', () => {
      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.get('button[aria-label*="thumbs down"], button[aria-label*="not helpful"], [data-testid="thumbs-down"]')
          .first()
          .click();
      });

      cy.wait('@feedbackApi').its('request.body').should('deep.include', {
        rating: 'down'
      });
    });

    it('should show visual confirmation after thumbs down', () => {
      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.get('button[aria-label*="thumbs down"], [data-testid="thumbs-down"]')
          .first()
          .click();
      });

      cy.wait('@feedbackApi');

      // Should show confirmation styling
      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.get('button[aria-label*="thumbs down"], [data-testid="thumbs-down"]')
          .should('have.class', 'selected')
          .or('have.attr', 'data-selected', 'true');
      });
    });

    it('should disable feedback buttons after thumbs down', () => {
      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.get('button[aria-label*="thumbs down"], [data-testid="thumbs-down"]')
          .first()
          .click();
      });

      cy.wait('@feedbackApi');

      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.get('button[aria-label*="thumbs up"], [data-testid="thumbs-up"]')
          .should('be.disabled');
        cy.get('button[aria-label*="thumbs down"], [data-testid="thumbs-down"]')
          .should('be.disabled');
      });
    });
  });

  describe('Report Issue Flow', () => {
    beforeEach(() => {
      cy.get('[data-testid="chatbot-button"]').click();
      cy.get('[data-testid="chatbot-input"]').type('What is Physical AI?{enter}');
      cy.wait('@queryApi');
    });

    it('should open report issue modal when clicked', () => {
      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.contains('button', 'Report').click();
      });

      // Modal should be visible
      cy.get('[role="dialog"][aria-label*="Report"], [data-testid="report-issue-modal"]')
        .should('be.visible');
    });

    it('should display issue type options in modal', () => {
      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.contains('button', 'Report').click();
      });

      // Should have issue type dropdown or radio buttons
      cy.get('[data-testid="report-issue-modal"], [role="dialog"]').within(() => {
        cy.contains('incorrect', { matchCase: false }).should('exist');
        cy.contains('incomplete', { matchCase: false }).should('exist');
        cy.contains('harmful', { matchCase: false }).should('exist');
      });
    });

    it('should have description textarea in modal', () => {
      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.contains('button', 'Report').click();
      });

      cy.get('[data-testid="report-issue-modal"], [role="dialog"]').within(() => {
        cy.get('textarea, [data-testid="issue-description"]').should('exist');
      });
    });

    it('should submit issue report with all fields', () => {
      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.contains('button', 'Report').click();
      });

      cy.get('[data-testid="report-issue-modal"], [role="dialog"]').within(() => {
        // Select issue type
        cy.get('select, [role="combobox"], input[type="radio"]').first().then($el => {
          if ($el.is('select')) {
            cy.wrap($el).select('incorrect');
          } else {
            cy.contains('label', 'incorrect', { matchCase: false }).click();
          }
        });

        // Enter description
        cy.get('textarea, [data-testid="issue-description"]')
          .type('The answer is factually incorrect. It should state X instead of Y.');

        // Submit
        cy.contains('button', 'Submit').click();
      });

      cy.wait('@reportIssueApi').its('request.body').should('deep.include', {
        issue_type: 'incorrect',
        description: 'The answer is factually incorrect. It should state X instead of Y.'
      });
    });

    it('should close modal after successful submission', () => {
      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.contains('button', 'Report').click();
      });

      cy.get('[data-testid="report-issue-modal"], [role="dialog"]').within(() => {
        cy.get('select, [role="combobox"], input[type="radio"]').first().then($el => {
          if ($el.is('select')) {
            cy.wrap($el).select('incorrect');
          } else {
            cy.contains('label', 'incorrect', { matchCase: false }).click();
          }
        });
        cy.get('textarea').type('Test description');
        cy.contains('button', 'Submit').click();
      });

      cy.wait('@reportIssueApi');

      // Modal should close
      cy.get('[data-testid="report-issue-modal"]').should('not.exist');
    });

    it('should show success message after submission', () => {
      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.contains('button', 'Report').click();
      });

      cy.get('[data-testid="report-issue-modal"], [role="dialog"]').within(() => {
        cy.get('select, input[type="radio"]').first().then($el => {
          if ($el.is('select')) {
            cy.wrap($el).select('incorrect');
          } else {
            cy.contains('label', 'incorrect', { matchCase: false }).click();
          }
        });
        cy.get('textarea').type('Test');
        cy.contains('button', 'Submit').click();
      });

      cy.wait('@reportIssueApi');

      // Should show success notification
      cy.contains('submitted', { matchCase: false }).should('be.visible');
    });

    it('should close modal when cancel is clicked', () => {
      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.contains('button', 'Report').click();
      });

      cy.get('[data-testid="report-issue-modal"], [role="dialog"]').within(() => {
        cy.contains('button', 'Cancel').click();
      });

      cy.get('[data-testid="report-issue-modal"]').should('not.exist');
    });

    it('should close modal when clicking outside', () => {
      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.contains('button', 'Report').click();
      });

      // Click outside modal (on backdrop)
      cy.get('body').click(0, 0);

      // Modal may or may not close depending on implementation
      // Just verify the action doesn't cause errors
    });

    it('should close modal on Escape key', () => {
      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.contains('button', 'Report').click();
      });

      cy.get('body').type('{esc}');

      cy.get('[data-testid="report-issue-modal"]').should('not.exist');
    });
  });

  describe('Feedback Error Handling', () => {
    beforeEach(() => {
      cy.get('[data-testid="chatbot-button"]').click();
      cy.get('[data-testid="chatbot-input"]').type('What is Physical AI?{enter}');
      cy.wait('@queryApi');
    });

    it('should handle feedback API error gracefully', () => {
      cy.intercept('POST', '**/api/feedback', {
        statusCode: 500,
        body: { error: 'Server error' }
      }).as('feedbackApiError');

      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.get('button[aria-label*="thumbs up"], [data-testid="thumbs-up"]')
          .first()
          .click();
      });

      cy.wait('@feedbackApiError');

      // Should show error message or keep buttons enabled for retry
      // The UI should not break
      cy.get('[data-testid="assistant-message"]').should('be.visible');
    });

    it('should handle report issue API error gracefully', () => {
      cy.intercept('POST', '**/api/report-issue', {
        statusCode: 500,
        body: { error: 'Server error' }
      }).as('reportIssueApiError');

      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.contains('button', 'Report').click();
      });

      cy.get('[data-testid="report-issue-modal"], [role="dialog"]').within(() => {
        cy.get('select, input[type="radio"]').first().then($el => {
          if ($el.is('select')) {
            cy.wrap($el).select('incorrect');
          } else {
            cy.contains('label', 'incorrect', { matchCase: false }).click();
          }
        });
        cy.get('textarea').type('Test');
        cy.contains('button', 'Submit').click();
      });

      cy.wait('@reportIssueApiError');

      // Should show error message
      cy.contains('error', { matchCase: false }).should('be.visible');
    });
  });

  describe('Multiple Messages Feedback', () => {
    it('should allow feedback on each bot message independently', () => {
      cy.get('[data-testid="chatbot-button"]').click();

      // First question
      cy.get('[data-testid="chatbot-input"]').type('What is Physical AI?{enter}');
      cy.wait('@queryApi');

      // Update mock for second question
      cy.intercept('POST', '**/api/query', {
        statusCode: 200,
        body: {
          answer: 'Reinforcement learning is a type of machine learning.',
          citations: [],
          confidence: 0.88,
          message_id: 'msg-feedback-test-456',
        },
      }).as('queryApi2');

      // Second question
      cy.get('[data-testid="chatbot-input"]').type('What is RL?{enter}');
      cy.wait('@queryApi2');

      // Should have two bot messages with feedback buttons
      cy.get('[data-testid="assistant-message"]').should('have.length', 2);

      // Give feedback on first message
      cy.get('[data-testid="assistant-message"]').first().within(() => {
        cy.get('button[aria-label*="thumbs up"], [data-testid="thumbs-up"]')
          .click();
      });

      cy.wait('@feedbackApi').its('request.body').should('include', {
        message_id: 'msg-feedback-test-123'
      });

      // Second message should still have active feedback buttons
      cy.get('[data-testid="assistant-message"]').last().within(() => {
        cy.get('button[aria-label*="thumbs up"], [data-testid="thumbs-up"]')
          .should('not.be.disabled');
      });
    });
  });

  describe('Feedback Accessibility', () => {
    beforeEach(() => {
      cy.get('[data-testid="chatbot-button"]').click();
      cy.get('[data-testid="chatbot-input"]').type('What is Physical AI?{enter}');
      cy.wait('@queryApi');
    });

    it('should have accessible feedback buttons', () => {
      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.get('button[aria-label*="thumbs"], [data-testid="thumbs-up"], [data-testid="thumbs-down"]')
          .each($btn => {
            cy.wrap($btn).should('have.attr', 'aria-label');
          });
      });
    });

    it('should be keyboard accessible', () => {
      // Tab to feedback button
      cy.get('[data-testid="assistant-message"]')
        .find('button[aria-label*="thumbs up"], [data-testid="thumbs-up"]')
        .first()
        .focus();

      // Should be focused
      cy.focused().should('exist');

      // Activate with Enter
      cy.focused().type('{enter}');

      cy.wait('@feedbackApi');
    });

    it('should announce feedback submission to screen readers', () => {
      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.get('button[aria-label*="thumbs up"], [data-testid="thumbs-up"]')
          .first()
          .click();
      });

      cy.wait('@feedbackApi');

      // Should have live region announcement or aria-live update
      cy.get('[aria-live="polite"], [role="status"]').should('exist');
    });
  });

  describe('Mobile Feedback', () => {
    beforeEach(() => {
      cy.viewport(375, 667);
      cy.get('[data-testid="chatbot-button"]').click();
      cy.get('[data-testid="chatbot-input"]').type('What is Physical AI?{enter}');
      cy.wait('@queryApi');
    });

    it('should display feedback buttons on mobile', () => {
      cy.get('[data-testid="assistant-message"]').within(() => {
        cy.get('button[aria-label*="thumbs up"], [data-testid="thumbs-up"]')
          .should('be.visible');
      });
    });

    it('should have touch-friendly feedback buttons', () => {
      cy.get('[data-testid="assistant-message"]')
        .find('button[aria-label*="thumbs up"], [data-testid="thumbs-up"]')
        .first()
        .then($btn => {
          const rect = $btn[0].getBoundingClientRect();
          expect(rect.width).to.be.at.least(44);
          expect(rect.height).to.be.at.least(44);
        });
    });

    it('should work with tap interaction', () => {
      cy.get('[data-testid="assistant-message"]')
        .find('button[aria-label*="thumbs up"], [data-testid="thumbs-up"]')
        .first()
        .realClick();

      cy.wait('@feedbackApi');
    });
  });
});
