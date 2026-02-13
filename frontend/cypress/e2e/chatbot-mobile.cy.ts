/**
 * E2E tests for Chatbot mobile responsiveness.
 *
 * Tests the chatbot behavior on various mobile viewport sizes and touch interactions.
 */

// Common mobile viewport sizes
const viewports = {
  iphone: { width: 375, height: 667, name: 'iPhone SE' },
  iphonePlus: { width: 414, height: 896, name: 'iPhone 11 Pro Max' },
  android: { width: 360, height: 640, name: 'Android Small' },
  androidLarge: { width: 412, height: 915, name: 'Android Large' },
  ipad: { width: 768, height: 1024, name: 'iPad' },
  ipadPro: { width: 1024, height: 1366, name: 'iPad Pro' },
};

describe('Chatbot Mobile Responsiveness', () => {
  beforeEach(() => {
    // Mock API responses
    cy.intercept('POST', '**/api/query', {
      statusCode: 200,
      body: {
        answer: 'Physical AI combines AI with physical systems for real-world interaction.',
        citations: [
          { section: 'Module 0: Introduction', url: '/docs/module-0', score: 0.95 },
        ],
        confidence: 0.92,
        message_id: 'msg-mobile-test',
      },
      delay: 300,
    }).as('queryApi');
  });

  describe('Small Mobile Devices (iPhone SE, Android Small)', () => {
    beforeEach(() => {
      cy.viewport(viewports.iphone.width, viewports.iphone.height);
      cy.visit('/');
    });

    it('should display chatbot button in mobile view', () => {
      cy.get('[data-testid="chatbot-button"]')
        .should('be.visible')
        .and('not.be.covered');
    });

    it('should open chatbot fullscreen or near-fullscreen on mobile', () => {
      cy.get('[data-testid="chatbot-button"]').click();

      cy.get('[role="dialog"]').should('be.visible');

      // Chatbot should take significant portion of screen on mobile
      cy.get('[role="dialog"]').then(($dialog) => {
        const dialogWidth = $dialog.width() || 0;
        const dialogHeight = $dialog.height() || 0;

        // Should take at least 80% of viewport width on mobile
        expect(dialogWidth).to.be.at.least(viewports.iphone.width * 0.8);
        // Should have reasonable height
        expect(dialogHeight).to.be.at.least(300);
      });
    });

    it('should have accessible touch targets (min 44x44px)', () => {
      cy.get('[data-testid="chatbot-button"]').click();

      // Check close button is large enough for touch
      cy.contains('button', '✕').then(($btn) => {
        const rect = $btn[0].getBoundingClientRect();
        expect(rect.width).to.be.at.least(44);
        expect(rect.height).to.be.at.least(44);
      });

      // Check submit button is large enough
      cy.get('[data-testid="chatbot-submit"]').then(($btn) => {
        const rect = $btn[0].getBoundingClientRect();
        expect(rect.width).to.be.at.least(44);
        expect(rect.height).to.be.at.least(44);
      });
    });

    it('should have input field that is easily tappable', () => {
      cy.get('[data-testid="chatbot-button"]').click();

      cy.get('[data-testid="chatbot-input"]')
        .should('be.visible')
        .then(($input) => {
          const rect = $input[0].getBoundingClientRect();
          // Input should have reasonable height for touch
          expect(rect.height).to.be.at.least(40);
        });
    });

    it('should complete Q&A flow on mobile', () => {
      cy.get('[data-testid="chatbot-button"]').click();

      // Type and send question
      cy.get('[data-testid="chatbot-input"]').type('What is Physical AI?');
      cy.get('[data-testid="chatbot-submit"]').click();

      // Wait for response
      cy.wait('@queryApi');

      // Verify messages are visible
      cy.get('[data-testid="user-message"]').should('be.visible');
      cy.get('[data-testid="assistant-message"]').should('be.visible');
    });

    it('should scroll messages properly in constrained viewport', () => {
      cy.get('[data-testid="chatbot-button"]').click();

      // Send multiple messages to trigger scroll
      for (let i = 0; i < 3; i++) {
        cy.get('[data-testid="chatbot-input"]').type(`Question ${i + 1}`);
        cy.get('[data-testid="chatbot-submit"]').click();
        cy.wait('@queryApi');
      }

      // Last message should be visible (auto-scroll to bottom)
      cy.get('[data-testid="assistant-message"]').last().should('be.visible');
    });
  });

  describe('Medium Mobile Devices (iPhone Plus, Android Large)', () => {
    beforeEach(() => {
      cy.viewport(viewports.iphonePlus.width, viewports.iphonePlus.height);
      cy.visit('/');
    });

    it('should display chatbot properly on larger phones', () => {
      cy.get('[data-testid="chatbot-button"]').click();
      cy.get('[role="dialog"]').should('be.visible');
      cy.contains('Physical AI Assistant').should('be.visible');
    });

    it('should not overlap with page content', () => {
      cy.get('[data-testid="chatbot-button"]').should('be.visible');

      // Button should be positioned in bottom-right corner
      cy.get('[data-testid="chatbot-button"]').then(($btn) => {
        const rect = $btn[0].getBoundingClientRect();
        // Should be near bottom
        expect(rect.bottom).to.be.at.least(viewports.iphonePlus.height - 100);
        // Should be near right
        expect(rect.right).to.be.at.least(viewports.iphonePlus.width - 100);
      });
    });

    it('should handle keyboard appearing (input remains visible)', () => {
      cy.get('[data-testid="chatbot-button"]').click();

      // Focus on input (simulates keyboard appearing on mobile)
      cy.get('[data-testid="chatbot-input"]').focus();

      // Input should still be visible
      cy.get('[data-testid="chatbot-input"]').should('be.visible');
    });
  });

  describe('Tablet Devices (iPad, iPad Pro)', () => {
    beforeEach(() => {
      cy.viewport(viewports.ipad.width, viewports.ipad.height);
      cy.visit('/');
    });

    it('should display chatbot as modal on tablet', () => {
      cy.get('[data-testid="chatbot-button"]').click();

      cy.get('[role="dialog"]').should('be.visible');

      // On tablet, chatbot should be reasonably sized modal, not fullscreen
      cy.get('[role="dialog"]').then(($dialog) => {
        const dialogWidth = $dialog.width() || 0;
        // Should not take full width on tablet
        expect(dialogWidth).to.be.at.most(viewports.ipad.width * 0.9);
      });
    });

    it('should have proper spacing and layout on tablet', () => {
      cy.get('[data-testid="chatbot-button"]').click();

      // All UI elements should be visible
      cy.contains('Physical AI Assistant').should('be.visible');
      cy.contains('button', 'Clear').should('be.visible');
      cy.contains('button', '✕').should('be.visible');
      cy.get('[data-testid="chatbot-input"]').should('be.visible');
      cy.contains('Powered by Physical AI Textbook').should('be.visible');
    });
  });

  describe('Orientation Changes', () => {
    it('should handle portrait to landscape transition', () => {
      // Start in portrait
      cy.viewport(viewports.iphone.width, viewports.iphone.height);
      cy.visit('/');
      cy.get('[data-testid="chatbot-button"]').click();
      cy.get('[role="dialog"]').should('be.visible');

      // Switch to landscape
      cy.viewport(viewports.iphone.height, viewports.iphone.width);

      // Chatbot should still be visible and functional
      cy.get('[role="dialog"]').should('be.visible');
      cy.get('[data-testid="chatbot-input"]').should('be.visible');
    });

    it('should handle landscape to portrait transition', () => {
      // Start in landscape
      cy.viewport(viewports.iphone.height, viewports.iphone.width);
      cy.visit('/');
      cy.get('[data-testid="chatbot-button"]').click();
      cy.get('[role="dialog"]').should('be.visible');

      // Switch to portrait
      cy.viewport(viewports.iphone.width, viewports.iphone.height);

      // Chatbot should still be visible and functional
      cy.get('[role="dialog"]').should('be.visible');
      cy.get('[data-testid="chatbot-input"]').should('be.visible');
    });
  });

  describe('Touch Interactions', () => {
    beforeEach(() => {
      cy.viewport(viewports.iphone.width, viewports.iphone.height);
      cy.visit('/');
    });

    it('should open chatbot with tap', () => {
      // Using realClick from cypress-real-events for more realistic touch simulation
      cy.get('[data-testid="chatbot-button"]').realClick();
      cy.get('[role="dialog"]').should('be.visible');
    });

    it('should close chatbot with tap on close button', () => {
      cy.get('[data-testid="chatbot-button"]').click();
      cy.get('[role="dialog"]').should('be.visible');

      cy.contains('button', '✕').realClick();
      cy.get('[role="dialog"]').should('not.exist');
    });

    it('should allow scrolling through messages with touch', () => {
      cy.get('[data-testid="chatbot-button"]').click();

      // Send multiple messages to create scrollable content
      for (let i = 0; i < 4; i++) {
        cy.get('[data-testid="chatbot-input"]').type(`Question number ${i + 1}`);
        cy.get('[data-testid="chatbot-submit"]').click();
        cy.wait('@queryApi');
      }

      // Should be able to see messages (scrolling works)
      cy.get('[data-testid="user-message"]').first().should('exist');
      cy.get('[data-testid="assistant-message"]').last().should('be.visible');
    });
  });

  describe('Responsive Typography', () => {
    it('should have readable text on small screens', () => {
      cy.viewport(viewports.android.width, viewports.android.height);
      cy.visit('/');
      cy.get('[data-testid="chatbot-button"]').click();

      // Title should be visible and not truncated badly
      cy.contains('Physical AI Assistant').should('be.visible');

      // Input placeholder should be readable
      cy.get('[data-testid="chatbot-input"]').should('be.visible');
    });

    it('should scale appropriately on tablets', () => {
      cy.viewport(viewports.ipad.width, viewports.ipad.height);
      cy.visit('/');
      cy.get('[data-testid="chatbot-button"]').click();

      // Elements should be properly sized for larger screen
      cy.contains('Physical AI Assistant').should('be.visible');
      cy.get('[data-testid="chatbot-input"]').should('be.visible');
    });
  });

  describe('Edge Cases', () => {
    beforeEach(() => {
      cy.viewport(viewports.iphone.width, viewports.iphone.height);
      cy.visit('/');
    });

    it('should handle very small viewport gracefully', () => {
      cy.viewport(320, 480); // Very small device
      cy.get('[data-testid="chatbot-button"]').click();

      // Should still function
      cy.get('[role="dialog"]').should('be.visible');
      cy.get('[data-testid="chatbot-input"]').should('be.visible');
    });

    it('should handle long messages on mobile', () => {
      cy.get('[data-testid="chatbot-button"]').click();

      // Type a long message
      const longMessage = 'This is a very long question that might wrap on mobile screens. '.repeat(3);
      cy.get('[data-testid="chatbot-input"]').type(longMessage);
      cy.get('[data-testid="chatbot-submit"]').click();

      cy.wait('@queryApi');

      // Long message should display properly (wrapped, not overflowing)
      cy.get('[data-testid="user-message"]')
        .should('be.visible')
        .and('not.have.css', 'overflow', 'visible');
    });

    it('should maintain functionality after multiple open/close cycles', () => {
      // Open and close multiple times
      for (let i = 0; i < 3; i++) {
        cy.get('[data-testid="chatbot-button"]').click();
        cy.get('[role="dialog"]').should('be.visible');
        cy.contains('button', '✕').click();
        cy.get('[role="dialog"]').should('not.exist');
      }

      // Should still work
      cy.get('[data-testid="chatbot-button"]').click();
      cy.get('[data-testid="chatbot-input"]').type('Still works?');
      cy.get('[data-testid="chatbot-submit"]').click();
      cy.wait('@queryApi');
      cy.get('[data-testid="assistant-message"]').should('be.visible');
    });
  });

  describe('Performance on Mobile', () => {
    beforeEach(() => {
      cy.viewport(viewports.iphone.width, viewports.iphone.height);
      cy.visit('/');
    });

    it('should open chatbot quickly (< 500ms)', () => {
      const startTime = Date.now();

      cy.get('[data-testid="chatbot-button"]').click();
      cy.get('[role="dialog"]').should('be.visible').then(() => {
        const endTime = Date.now();
        const duration = endTime - startTime;
        expect(duration).to.be.lessThan(500);
      });
    });

    it('should respond to input without noticeable lag', () => {
      cy.get('[data-testid="chatbot-button"]').click();

      // Type quickly
      cy.get('[data-testid="chatbot-input"]')
        .type('Quick typing test', { delay: 0 })
        .should('have.value', 'Quick typing test');
    });
  });
});
