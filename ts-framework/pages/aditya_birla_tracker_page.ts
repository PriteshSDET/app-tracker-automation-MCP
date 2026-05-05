import { Page } from '@playwright/test';
import { BasePage } from './base_page';
import { AdityaBirlaLocators } from '../locators/aditya_birla_locators';

export class AdityaBirlaTrackerPage extends BasePage {
  private locators: AdityaBirlaLocators;

  constructor(page: Page) {
    super(page);
    this.locators = new AdityaBirlaLocators(page);
  }

  async isTrackerDisplayed(): Promise<boolean> {
    try {
      // Check URL
      const currentUrl = this.page.url();
      if (!currentUrl.includes('app-tracker')) {
        return false;
      }

      // Check key elements
      const titleVisible = await this.locators.trackerHeader.isVisible();

      // Use more robust locator for tracker table content
      const tableLocator = this.page.locator("table:has-text('Application'), table:has-text('App.No'), [class*='table'], [class*='grid'], [role='grid'], .tracker-table").first();
      const tableVisible = await tableLocator.isVisible();

      return titleVisible && tableVisible;

    } catch (e) {
      // TS Best Practice: Safely typecast caught errors
      const errorMessage = e instanceof Error ? e.message : String(e);
      this.logger.error(`Error checking tracker display: ${errorMessage}`);
      return false;
    }
  }

  async getPolicyListTitle(): Promise<string> {
    try {
      // FIX: Added parentheses to call .first() as a method
      const titleElement = this.locators.policyListTitle.first();
      
      if (await titleElement.isVisible()) {
        const text = await titleElement.textContent();
        return text ? text.trim() : '';
      }
      return '';
    } catch (e) {
      return '';
    }
  }

  async navigateToTrackerPage(): Promise<void> {
    await this.navigateTo(this.locators.trackerPageUrl);
    await this.waitForPageLoad();
  }

  async isTrackerTableVisible(): Promise<boolean> {
    try {
      const tableLocator = this.page.locator("table:has-text('Application'), table:has-text('App.No'), [class*='table'], [class*='grid'], [role='grid'], .tracker-table").first();
      await tableLocator.waitFor({ state: 'visible', timeout: 10000 });
      return await tableLocator.isVisible();
    } catch {
      return false;
    }
  }

  async isApplicationSearchVisible(): Promise<boolean> {
    try {
      return await this.locators.searchBar.isVisible();
    } catch {
      return false;
    }
  }
}