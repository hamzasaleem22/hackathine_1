// Cypress E2E support file
import './commands';
import 'cypress-real-events';

// Prevent TypeScript errors
declare global {
  namespace Cypress {
    interface Chainable {
      // Add custom command types here if needed
    }
  }
}
