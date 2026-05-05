import { Page, expect } from '@playwright/test';
import { Logger } from './logger';

export class Assertions {
  private page: Page;
  private logger: Logger;

  constructor(page: Page) {
    this.page = page;
    this.logger = new Logger('Assertions');
  }

  async assertElementVisible(locator: string, message?: string) {
    try {
      const element = this.page.locator(locator);
      await expect(element).toBeVisible();
      this.logger.info(`Element ${locator} is visible`);
    } catch (e) {
      const errorMsg = message || `Element ${locator} should be visible`;
      this.logger.error(`Assertion failed: ${errorMsg}`);
      throw new Error(errorMsg);
    }
  }

  async assertElementHidden(locator: string, message?: string) {
    try {
      const element = this.page.locator(locator);
      await expect(element).toBeHidden();
      this.logger.info(`Element ${locator} is hidden`);
    } catch (e) {
      const errorMsg = message || `Element ${locator} should be hidden`;
      this.logger.error(`Assertion failed: ${errorMsg}`);
      throw new Error(errorMsg);
    }
  }

  async assertElementEnabled(locator: string, message?: string) {
    try {
      const element = this.page.locator(locator);
      await expect(element).toBeEnabled();
      this.logger.info(`Element ${locator} is enabled`);
    } catch (e) {
      const errorMsg = message || `Element ${locator} should be enabled`;
      this.logger.error(`Assertion failed: ${errorMsg}`);
      throw new Error(errorMsg);
    }
  }

  async assertElementDisabled(locator: string, message?: string) {
    try {
      const element = this.page.locator(locator);
      await expect(element).toBeDisabled();
      this.logger.info(`Element ${locator} is disabled`);
    } catch (e) {
      const errorMsg = message || `Element ${locator} should be disabled`;
      this.logger.error(`Assertion failed: ${errorMsg}`);
      throw new Error(errorMsg);
    }
  }
}