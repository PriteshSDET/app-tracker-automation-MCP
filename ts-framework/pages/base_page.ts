import { Page } from '@playwright/test';
import { Logger } from '../utils/logger';
import { Waits } from '../utils/waits';

export class BasePage {
  protected page: Page;
  protected logger: Logger;
  protected waits: Waits;

  constructor(page: Page) {
    this.page = page;
    this.logger = new Logger('BasePage');
    this.waits = new Waits(page);
  }

  async navigateTo(url: string): Promise<void> {
    this.logger.info(`Navigating to: ${url}`);
    await this.page.goto(url);
  }

  async getTitle(): Promise<string> {
    return await this.page.title();
  }

  async waitForPageLoad(timeout: number = 30000): Promise<void> {
    await this.waits.waitForPageLoad(timeout);
  }

  async takeScreenshot(name: string): Promise<void> {
    await this.page.screenshot({ path: `screenshots/${name}.png` });
  }

  async isElementVisible(locator: string): Promise<boolean> {
    return await this.page.locator(locator).isVisible();
  }

  async clickElement(locator: string): Promise<void> {
    await this.page.locator(locator).click();
  }

  async fillText(locator: string, text: string): Promise<void> {
    await this.page.locator(locator).fill(text);
  }
}