// Custom Cypress commands

// Example command for chatbot testing
Cypress.Commands.add('openChatbot', () => {
  cy.get('[data-testid="chatbot-button"]').click();
  cy.get('[data-testid="chatbot-widget"]').should('be.visible');
});

Cypress.Commands.add('sendChatMessage', (message: string) => {
  cy.get('[data-testid="chatbot-input"]').type(message);
  cy.get('[data-testid="chatbot-submit"]').click();
});

Cypress.Commands.add('waitForChatResponse', () => {
  cy.get('[data-testid="message-loading"]', { timeout: 10000 }).should('not.exist');
  cy.get('[data-testid="bot-message"]').should('be.visible');
});

// TypeScript declarations
declare global {
  namespace Cypress {
    interface Chainable {
      openChatbot(): Chainable<void>;
      sendChatMessage(message: string): Chainable<void>;
      waitForChatResponse(): Chainable<void>;
    }
  }
}

export {};
