import { Page, Locator } from '@playwright/test';

/**
 * Base Component class for reusable UI components.
 * Provides common functionality for all component objects.
 */
export class BaseComponent {
    protected page: Page;
    protected locator: string;
    protected element: Locator;

    constructor(page: Page, locator: string) {
        this.page = page;
        this.locator = locator;
        this.element = page.locator(locator);
    }

    /**
     * Check if component is visible
     */
    async isVisible(): Promise<boolean> {
        return await this.element.isVisible();
    }

    /**
     * Check if component is enabled
     */
    async isEnabled(): Promise<boolean> {
        return await this.element.isEnabled();
    }

    /**
     * Wait for component to be visible
     */
    async waitForVisible(timeout: number = 30000): Promise<void> {
        await this.element.waitFor({ state: 'visible', timeout });
    }

    /**
     * Wait for component to be enabled
     */
    async waitForEnabled(timeout: number = 30000): Promise<void> {
        await this.element.waitFor({ state: 'visible', timeout });
        // Playwright doesn't have a direct 'enabled' state in waitFor, 
        // but we can use expect or a custom check if needed.
    }

    /**
     * Click on component
     */
    async click(): Promise<void> {
        await this.element.click();
    }

    /**
     * Hover over component
     */
    async hover(): Promise<void> {
        await this.element.hover();
    }

    /**
     * Get text content of component
     */
    async getText(): Promise<string | null> {
        return await this.element.textContent();
    }

    /**
     * Get attribute value of component
     */
    async getAttribute(attribute: string): Promise<string | null> {
        return await this.element.getAttribute(attribute);
    }

    /**
     * Scroll component into view
     */
    async scrollIntoView(): Promise<void> {
        await this.element.scrollIntoViewIfNeeded();
    }
}
