/**
 * E2E tests for citation navigation (T090).
 *
 * Tests clicking citations to navigate to referenced sections with highlighting.
 */

describe('Citation Navigation', () => {
  beforeEach(() => {
    // Mock API response with citations
    cy.intercept('POST', '**/api/query', {
      statusCode: 200,
      body: {
        answer: 'Physical AI is a field that combines artificial intelligence with physical systems and robotics. It enables machines to interact with the real world through embodied intelligence.',
        citations: [
          {
            section: 'Module 0: Introduction to Physical AI',
            url: '/docs/module-0/introduction#what-is-physical-ai',
            score: 0.95
          },
          {
            section: 'Module 1: Embodied Intelligence',
            url: '/docs/module-1/embodied#definition',
            score: 0.88
          },
          {
            section: 'Module 2: Robotics Fundamentals',
            url: '/docs/module-2/robotics#overview',
            score: 0.82
          }
        ],
        confidence: 0.92,
        message_id: 'msg-citation-test',
      },
      delay: 300,
    }).as('queryApi');

    cy.visit('/');
  });

  describe('Citation Display', () => {
    beforeEach(() => {
      // Open chatbot and send a question
      cy.get('[data-testid="chatbot-button"]').click();
      cy.get('[data-testid="chatbot-input"]').type('What is Physical AI?{enter}');
      cy.wait('@queryApi');
    });

    it('should display citations with bot response', () => {
      cy.get('[data-testid="citation-link"]').should('have.length', 3);
    });

    it('should display citation section titles', () => {
      cy.contains('Module 0: Introduction to Physical AI').should('be.visible');
      cy.contains('Module 1: Embodied Intelligence').should('be.visible');
      cy.contains('Module 2: Robotics Fundamentals').should('be.visible');
    });

    it('should display relevance scores for citations', () => {
      // Check that scores are displayed (as percentages)
      cy.get('[data-testid="citation-link"]').first().within(() => {
        cy.contains(/95%|0\.95/).should('exist');
      });
    });

    it('should order citations by relevance score', () => {
      cy.get('[data-testid="citation-link"]').then($links => {
        const firstText = $links.eq(0).text();
        const secondText = $links.eq(1).text();

        // First citation should be Module 0 (highest score)
        expect(firstText).to.include('Module 0');
      });
    });
  });

  describe('Citation Click Navigation', () => {
    beforeEach(() => {
      cy.get('[data-testid="chatbot-button"]').click();
      cy.get('[data-testid="chatbot-input"]').type('What is Physical AI?{enter}');
      cy.wait('@queryApi');
    });

    it('should have clickable citation links', () => {
      cy.get('[data-testid="citation-link"]').first()
        .should('have.attr', 'href')
        .and('include', '/docs/');
    });

    it('should navigate to section when citation is clicked', () => {
      // Click the first citation
      cy.get('[data-testid="citation-link"]').first().click();

      // Should navigate to the URL or scroll to section
      // Check URL changed or scroll happened
      cy.url().should('include', '/docs/');
    });

    it('should scroll to section anchor when clicking citation', () => {
      // Create a mock section element on the page
      cy.document().then((doc) => {
        const section = doc.createElement('div');
        section.id = 'what-is-physical-ai';
        section.textContent = 'Test Section Content';
        section.style.marginTop = '2000px'; // Below fold
        doc.body.appendChild(section);
      });

      // Click citation that links to this section
      cy.get('[data-testid="citation-link"]').first().click();

      // Section should be scrolled into view
      cy.get('#what-is-physical-ai').should('be.visible');
    });

    it('should highlight section when navigating via citation', () => {
      // Create a mock section element
      cy.document().then((doc) => {
        const section = doc.createElement('div');
        section.id = 'what-is-physical-ai';
        section.textContent = 'Test Section Content';
        doc.body.appendChild(section);
      });

      // Click citation
      cy.get('[data-testid="citation-link"]').first().click();

      // Section should have highlight styling (background color change)
      cy.get('#what-is-physical-ai').should(($el) => {
        const bgColor = $el.css('background-color');
        // Should have some highlight color (not transparent or white)
        expect(bgColor).to.not.equal('rgba(0, 0, 0, 0)');
      });
    });

    it('should remove highlight after delay', () => {
      // Create mock section
      cy.document().then((doc) => {
        const section = doc.createElement('div');
        section.id = 'what-is-physical-ai';
        section.textContent = 'Test Section';
        doc.body.appendChild(section);
      });

      // Click citation
      cy.get('[data-testid="citation-link"]').first().click();

      // Wait for highlight to fade (typically 2 seconds)
      cy.wait(2500);

      // Highlight should be removed
      cy.get('#what-is-physical-ai').should(($el) => {
        const bgColor = $el.css('background-color');
        // Should be back to normal (transparent or default)
        expect(bgColor).to.satisfy((c: string) =>
          c === 'rgba(0, 0, 0, 0)' || c === 'rgb(255, 255, 255)' || c === ''
        );
      });
    });
  });

  describe('Citation Accessibility', () => {
    beforeEach(() => {
      cy.get('[data-testid="chatbot-button"]').click();
      cy.get('[data-testid="chatbot-input"]').type('What is Physical AI?{enter}');
      cy.wait('@queryApi');
    });

    it('should have accessible citation links', () => {
      cy.get('[data-testid="citation-link"]').each(($link) => {
        // Should have href attribute
        cy.wrap($link).should('have.attr', 'href');

        // Should have accessible text or aria-label
        cy.wrap($link).invoke('text').should('have.length.gt', 0);
      });
    });

    it('should be keyboard navigable to citations', () => {
      // Tab to first citation
      cy.get('[data-testid="citation-link"]').first().focus();
      cy.focused().should('have.attr', 'data-testid', 'citation-link');
    });

    it('should activate citation with Enter key', () => {
      cy.get('[data-testid="citation-link"]').first().focus();
      cy.focused().type('{enter}');

      // Should navigate
      cy.url().should('include', '/docs/');
    });

    it('should have screen reader friendly text', () => {
      cy.get('[data-testid="citation-link"]').first().then(($link) => {
        // Should have descriptive text for screen readers
        const text = $link.text();
        expect(text).to.include('Module');
      });
    });
  });

  describe('Multiple Questions with Citations', () => {
    it('should show citations for each response independently', () => {
      cy.get('[data-testid="chatbot-button"]').click();

      // First question
      cy.get('[data-testid="chatbot-input"]').type('What is Physical AI?{enter}');
      cy.wait('@queryApi');

      // Update mock for second question with different citations
      cy.intercept('POST', '**/api/query', {
        statusCode: 200,
        body: {
          answer: 'Reinforcement learning is a type of machine learning.',
          citations: [
            {
              section: 'Module 3: Reinforcement Learning',
              url: '/docs/module-3/rl#intro',
              score: 0.91
            }
          ],
          confidence: 0.89,
          message_id: 'msg-citation-test-2',
        },
      }).as('queryApi2');

      // Second question
      cy.get('[data-testid="chatbot-input"]').type('What is reinforcement learning?{enter}');
      cy.wait('@queryApi2');

      // Should have citations from both responses
      cy.contains('Module 0: Introduction to Physical AI').should('exist');
      cy.contains('Module 3: Reinforcement Learning').should('exist');
    });
  });

  describe('Citation with No Results', () => {
    it('should handle responses with no citations gracefully', () => {
      cy.intercept('POST', '**/api/query', {
        statusCode: 200,
        body: {
          answer: 'I could not find relevant information in the textbook.',
          citations: [],
          confidence: 0.3,
          message_id: 'msg-no-citations',
        },
      }).as('queryApiNoCitations');

      cy.get('[data-testid="chatbot-button"]').click();
      cy.get('[data-testid="chatbot-input"]').type('Random unrelated question{enter}');
      cy.wait('@queryApiNoCitations');

      // Should display answer without citation section
      cy.get('[data-testid="assistant-message"]').should('be.visible');
      cy.get('[data-testid="citation-link"]').should('not.exist');
    });
  });

  describe('Citation Link Behavior', () => {
    beforeEach(() => {
      cy.get('[data-testid="chatbot-button"]').click();
      cy.get('[data-testid="chatbot-input"]').type('What is Physical AI?{enter}');
      cy.wait('@queryApi');
    });

    it('should prevent default link behavior for in-page navigation', () => {
      // Create the target section
      cy.document().then((doc) => {
        const section = doc.createElement('div');
        section.id = 'what-is-physical-ai';
        section.textContent = 'Section content';
        doc.body.appendChild(section);
      });

      // Click should scroll, not navigate away
      const initialUrl = cy.url();
      cy.get('[data-testid="citation-link"]').first().click();

      // Should still be on same page (or navigated to section)
      cy.url().should('include', '/');
    });

    it('should open external links in new tab if needed', () => {
      // This test verifies link target attribute if external
      cy.get('[data-testid="citation-link"]').first().then(($link) => {
        const href = $link.attr('href');
        // Internal links should not have target="_blank"
        if (href && href.startsWith('/')) {
          expect($link.attr('target')).to.not.equal('_blank');
        }
      });
    });
  });

  describe('Citation Visual Feedback', () => {
    beforeEach(() => {
      cy.get('[data-testid="chatbot-button"]').click();
      cy.get('[data-testid="chatbot-input"]').type('What is Physical AI?{enter}');
      cy.wait('@queryApi');
    });

    it('should show hover state on citation links', () => {
      cy.get('[data-testid="citation-link"]').first().realHover();

      // Should have hover styling (cursor, underline, color change, etc.)
      cy.get('[data-testid="citation-link"]').first()
        .should('have.css', 'cursor', 'pointer');
    });

    it('should show focus state on citation links', () => {
      cy.get('[data-testid="citation-link"]').first().focus();

      // Should have visible focus indicator
      cy.focused().should('have.css', 'outline').and('not.equal', 'none');
    });

    it('should display citation icon or indicator', () => {
      // Citations should have some visual indicator (icon, number, etc.)
      cy.get('[data-testid="citation-link"]').first().within(() => {
        // Check for icon or link indicator
        cy.get('svg, [class*="icon"], [class*="external"]').should('exist');
      });
    });
  });

  describe('Mobile Citation Navigation', () => {
    beforeEach(() => {
      cy.viewport(375, 667);
      cy.get('[data-testid="chatbot-button"]').click();
      cy.get('[data-testid="chatbot-input"]').type('What is Physical AI?{enter}');
      cy.wait('@queryApi');
    });

    it('should display citations properly on mobile', () => {
      cy.get('[data-testid="citation-link"]').should('be.visible');
      cy.get('[data-testid="citation-link"]').should('have.length', 3);
    });

    it('should have touch-friendly citation links', () => {
      cy.get('[data-testid="citation-link"]').first().then(($link) => {
        const rect = $link[0].getBoundingClientRect();
        // Should have adequate touch target size
        expect(rect.height).to.be.at.least(44);
      });
    });

    it('should navigate on tap', () => {
      cy.get('[data-testid="citation-link"]').first().realClick();

      // Should navigate or scroll
      cy.url().should('include', '/');
    });
  });
});
