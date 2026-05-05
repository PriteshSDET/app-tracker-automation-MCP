import { Page } from '@playwright/test';
import { BasePage } from './base_page';
import { AdityaBirlaLocators } from '../locators/aditya_birla_locators';

export class AdityaBirlaDashboardPage extends BasePage {
  private locators: AdityaBirlaLocators;

  constructor(page: Page) {
    super(page);
    this.locators = new AdityaBirlaLocators(page);
  }

  async isDashboardDisplayed(): Promise<boolean> {
    try {
      // Check URL
      const currentUrl = this.page.url();
      if (!currentUrl.includes('dashboard')) {
        return false;
      }

      // Check key elements
      const headerVisible = await this.locators.dashboardHeader.isVisible();

      // Use more specific locator for data table
      const tableLocator = this.page.locator("table:has-text('Application')");
      const tableVisible = await tableLocator.isVisible();

      return headerVisible && tableVisible;

    } catch (e) {
      // TS Best Practice: Safely typecast caught errors
      const errorMessage = e instanceof Error ? e.message : String(e);
      this.logger.error(`Error checking dashboard display: ${errorMessage}`);
      return false;
    }
  }

  async getApplicationListTitle(): Promise<string> {
    try {
      // FIX: Added parentheses to call .first() as a method
      const titleElement = this.locators.applicationListTitle.first();
      
      if (await titleElement.isVisible()) {
        const text = await titleElement.textContent();
        return text ? text.trim() : '';
      }
      return '';
    } catch (e) {
      return '';
    }
  }
}