import { Page, Locator, expect } from '@playwright/test';
import { BaseComponent } from './base_component';
import { Logger } from './logger';

/**
 * Searchbox component for handling search functionality.
 */
export class SearchBox extends BaseComponent {
    protected logger: Logger;

    constructor(page: Page, locator: string) {
        super(page, locator);
        this.logger = new Logger();
    }

    protected async _waitForLoadingOverlayToDisappear(timeout: number = 5000): Promise<void> {
        try {
            const loadingSelectors = [
                ".loading-overlay",
                ".spinner",
                ".progress-bar",
                "[class*='loading']",
                "[class*='spinner']",
                "[class*='overlay']",
                ".MuiCircularProgress-root",
                ".MuiBackdrop-root"
            ];

            for (const selector of loadingSelectors) {
                try {
                    const loadingElement = this.page.locator(selector).first();
                    if (await loadingElement.isVisible({ timeout: 1000 })) {
                        this.logger.info(`Waiting for loading element to disappear: ${selector}`);
                        await loadingElement.waitFor({ state: "hidden", timeout });
                        this.logger.info(`Loading element disappeared: ${selector}`);
                    }
                } catch (e) {
                    continue;
                }
            }
        } catch (e) {
            this.logger.warning(`Error waiting for loading overlay: ${e}`);
        }
    }

    async enterSearchTerm(term: string): Promise<void> {
        await this.page.waitForLoadState("networkidle", { timeout: 10000 });
        await this.element.waitFor({ state: "attached", timeout: 5000 });
        await this.element.waitFor({ state: "visible", timeout: 5000 });

        await this._waitForLoadingOverlayToDisappear();
        await this.element.fill(term);
        await this.page.waitForLoadState("networkidle", { timeout: 5000 });
    }

    async clearSearch(): Promise<void> {
        await this.page.waitForLoadState("networkidle", { timeout: 10000 });
        await this.element.waitFor({ state: "attached", timeout: 5000 });
        await this.element.waitFor({ state: "visible", timeout: 5000 });

        await this._waitForLoadingOverlayToDisappear();
        await this.element.fill("");
        await this.page.waitForLoadState("networkidle", { timeout: 5000 });
    }

    async submitSearch(): Promise<void> {
        await this.page.waitForLoadState("networkidle", { timeout: 10000 });
        await this.element.waitFor({ state: "attached", timeout: 5000 });
        await this.element.waitFor({ state: "visible", timeout: 5000 });

        await this._waitForLoadingOverlayToDisappear();
        await this.element.press("Enter");
        await this.page.waitForLoadState("networkidle", { timeout: 10000 });
    }

    async search(term: string): Promise<void> {
        await this.enterSearchTerm(term);
        await this.submitSearch();
        await this.page.waitForLoadState("networkidle", { timeout: 15000 });
    }

    async getSearchValue(): Promise<string> {
        return await this.element.inputValue();
    }

    async isSearchEmpty(): Promise<boolean> {
        const val = await this.getSearchValue();
        return val.length === 0;
    }

    async waitForSearchResults(timeout: number = 30000): Promise<void> {
        await this.page.waitForLoadState("networkidle", { timeout });
        await this._waitForLoadingOverlayToDisappear(timeout);
    }

    async getSuggestions(): Promise<string[]> {
        const suggestionsLocator = this.page.locator(".search-suggestions li");
        return await suggestionsLocator.allInnerTexts();
    }

    async selectSuggestion(index: number): Promise<void> {
        await this.page.waitForLoadState("networkidle", { timeout: 10000 });
        const suggestionsLocator = this.page.locator(".search-suggestions li");
        const suggestions = await suggestionsLocator.all();
        
        if (index < suggestions.length) {
            await suggestions[index].waitFor({ state: "attached", timeout: 5000 });
            await suggestions[index].waitFor({ state: "visible", timeout: 5000 });

            await this._waitForLoadingOverlayToDisappear();
            await suggestions[index].click();
            await this.page.waitForLoadState("networkidle", { timeout: 5000 });
        }
    }
}

/**
 * App Tracker Specific Search Box Selectors
 */
export class AppTrackerSearchBox extends SearchBox {
    static readonly SEARCH_INPUT = "input.navbar-search";
    static readonly SEARCH_CONTAINER = ".MuiBox-root.jss58";

    constructor(page: Page) {
        super(page, AppTrackerSearchBox.SEARCH_INPUT);
    }

    async enterSearchTerm(term: string): Promise<void> {
        await this.page.waitForLoadState("networkidle", { timeout: 10000 });
        const searchInput = this.page.locator(AppTrackerSearchBox.SEARCH_INPUT).first();
        await searchInput.waitFor({ state: "attached", timeout: 5000 });
        await searchInput.waitFor({ state: "visible", timeout: 5000 });

        await this._waitForLoadingOverlayToDisappear();
        await searchInput.fill(term);
        await this.page.waitForLoadState("networkidle", { timeout: 5000 });
    }
}
