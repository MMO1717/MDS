// Test file for dark mode functionality
describe('Dark Mode Toggle', () => {
    beforeEach(() => {
        // Clear localStorage before each test
        localStorage.clear();
        // Load the page
        cy.visit('index.html');
    });

    it('should toggle dark mode when button is clicked', () => {
        // Check that dark mode is initially disabled
        cy.get('body').should('not.have.class', 'dark-mode');
        
        // Click the dark mode toggle
        cy.get('#darkModeToggle').click();
        
        // Check that dark mode is now enabled
        cy.get('body').should('have.class', 'dark-mode');
        
        // Check that the button text changed
        cy.get('#darkModeToggle').should('contain', '☀️');
    });

    it('should persist dark mode preference', () => {
        // Click the dark mode toggle
        cy.get('#darkModeToggle').click();
        
        // Reload the page
        cy.reload();
        
        // Check that dark mode is still enabled
        cy.get('body').should('have.class', 'dark-mode');
    });

    it('should load saved preference from localStorage', () => {
        // Set dark mode preference in localStorage
        localStorage.setItem('darkMode', 'enabled');
        
        // Load the page
        cy.visit('index.html');
        
        // Check that dark mode is enabled
        cy.get('body').should('have.class', 'dark-mode');
    });
});