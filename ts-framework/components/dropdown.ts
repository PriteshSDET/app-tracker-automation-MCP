import { Page, Locator, expect } from '@playwright/test';
import { BaseComponent } from './base_component';
import { Logger } from './logger';

/**
 * Dropdown component for handling select/dropdown elements.
 * Updated with CSS selectors from App Tracker HTML analysis.
 */
export class Dropdown extends BaseComponent {
    protected logger: Logger;

    constructor(page: Page, locator: string) {
        super(page, locator);
        this.logger = new Logger();
    }

    private async _waitForLoadingOverlayToDisappear(timeout: number = 5000): Promise<void> {
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

    async selectOption(value: string): Promise<void> {
        await this.page.waitForLoadState("networkidle", { timeout: 10000 });
        await this.element.waitFor({ state: "attached", timeout: 5000 });
        await this.element.waitFor({ state: "visible", timeout: 5000 });
        
        await this._waitForLoadingOverlayToDisappear();
        await this.element.selectOption(value);
        await this.page.waitForLoadState("networkidle", { timeout: 5000 });
    }

    async selectOptionByLabel(label: string): Promise<void> {
        await this.page.waitForLoadState("networkidle", { timeout: 10000 });
        await this.element.waitFor({ state: "attached", timeout: 5000 });
        await this.element.waitFor({ state: "visible", timeout: 5000 });

        await this._waitForLoadingOverlayToDisappear();
        await this.element.selectOption({ label });
        await this.page.waitForLoadState("networkidle", { timeout: 5000 });
    }

    async selectOptionByIndex(index: number): Promise<void> {
        await this.page.waitForLoadState("networkidle", { timeout: 10000 });
        await this.element.waitFor({ state: "attached", timeout: 5000 });
        await this.element.waitFor({ state: "visible", timeout: 5000 });

        await this._waitForLoadingOverlayToDisappear();
        await this.element.selectOption({ index });
        await this.page.waitForLoadState("networkidle", { timeout: 5000 });
    }

    async getSelectedValue(): Promise<string> {
        return await this.element.inputValue();
    }

    async getSelectedText(): Promise<string | null> {
        return await this.element.textContent();
    }

    async getAllOptions(): Promise<string[]> {
        return await this.element.locator("option").allInnerTexts();
    }

    async isMultiple(): Promise<boolean> {
        return (await this.element.getAttribute("multiple")) !== null;
    }

    async clearSelection(): Promise<void> {
        await this.page.waitForLoadState("networkidle", { timeout: 10000 });
        await this.element.waitFor({ state: "attached", timeout: 5000 });
        await this.element.waitFor({ state: "visible", timeout: 5000 });

        await this._waitForLoadingOverlayToDisappear();
        await this.element.selectOption([]);
        await this.page.waitForLoadState("networkidle", { timeout: 5000 });
    }
}

/**
 * App Tracker Specific Dropdown Selectors
 */
export class AppTrackerDropdown extends Dropdown {
    static readonly FILTER_BUTTON = "button.filterButton.MuiButton-textSizeSmall";
    static readonly SORT_DROPDOWN = "#mui-component-select-sortList";
    static readonly SORT_OPTIONS = "ul.MuiList-root[role='listbox']";

    constructor(page: Page) {
        super(page, AppTrackerDropdown.FILTER_BUTTON);
    }

    async clickFilterButton(): Promise<void> {
        await this.page.waitForLoadState("networkidle", { timeout: 10000 });
        const filterBtn = this.page.locator(AppTrackerDropdown.FILTER_BUTTON).first();
        await filterBtn.waitFor({ state: "attached", timeout: 5000 });
        await filterBtn.waitFor({ state: "visible", timeout: 5000 });

        // Using private method from parent via type cast or changing access modifier if needed
        // Since it's private in Python, I made it private here too, but I'll change it to protected for subclasses.
        await (this as any)._waitForLoadingOverlayToDisappear();
        await filterBtn.click();
        await this.page.waitForLoadState("networkidle", { timeout: 5000 });
    }

    async clickSortDropdown(): Promise<void> {
        await this.page.waitForLoadState("networkidle", { timeout: 10000 });
        const sortDropdown = this.page.locator(AppTrackerDropdown.SORT_DROPDOWN).first();
        await sortDropdown.waitFor({ state: "attached", timeout: 5000 });
        await sortDropdown.waitFor({ state: "visible", timeout: 5000 });

        await (this as any)._waitForLoadingOverlayToDisappear();
        await sortDropdown.click();
        await this.page.waitForLoadState("networkidle", { timeout: 5000 });
    }

    async selectSortOption(optionText: string): Promise<void> {
        await this.page.waitForLoadState("networkidle", { timeout: 10000 });
        const optionLocator = `${AppTrackerDropdown.SORT_OPTIONS} li:has-text('${optionText}')`;
        const option = this.page.locator(optionLocator).first();
        
        await option.waitFor({ state: "attached", timeout: 5000 });
        await option.waitFor({ state: "visible", timeout: 5000 });

        await (this as any)._waitForLoadingOverlayToDisappear();
        await option.click();
        await this.page.waitForLoadState("networkidle", { timeout: 5000 });
    }
}
