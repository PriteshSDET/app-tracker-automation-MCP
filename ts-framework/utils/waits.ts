import { Page, Locator, expect } from '@playwright/test';
import { Config } from './config';
import { Logger } from './logger';

export class Waits {
  private page: Page;
  private logger: Logger;

  constructor(page: Page) {
    this.page = page;
    this.logger = new Logger('Waits');
  }

  async waitForElementVisible(locator: string | Locator, timeout?: number) {
    timeout = timeout || Config.ELEMENT_WAIT_TIMEOUT;
    try {
      const loc = typeof locator === 'string' ? this.page.locator(locator) : locator;
      await loc.waitFor({ state: 'visible', timeout });
      this.logger.debug('Locator element became visible');
    } catch (e) {
      const locatorStr = typeof locator === 'string' ? locator : 'Locator object';
      this.logger.error(`Element ${locatorStr} did not become visible within ${timeout}ms: ${String(e)}`);
      throw e;
    }
  }

  async waitForElementHidden(locator: string, timeout?: number) {
    timeout = timeout || Config.ELEMENT_WAIT_TIMEOUT;
    try {
      await this.page.locator(locator).waitFor({ state: 'hidden', timeout });
      this.logger.debug(`Element ${locator} became hidden`);
    } catch (e) {
      this.logger.error(`Element ${locator} did not become hidden within ${timeout}ms: ${String(e)}`);
      throw e;
    }
  }

  async waitForElementEnabled(locator: string, timeout?: number) {
    timeout = timeout || Config.ELEMENT_WAIT_TIMEOUT;
    try {
      const element = this.page.locator(locator);
      await element.waitFor({ state: 'visible', timeout });
      await expect(element).toBeEnabled({ timeout });
      this.logger.debug(`Element ${locator} became enabled`);
    } catch (e) {
      this.logger.error(`Element ${locator} did not become enabled within ${timeout}ms: ${String(e)}`);
      throw e;
    }
  }

  async waitForElementDisappear(locator: string, timeout?: number) {
    timeout = timeout || Config.ELEMENT_WAIT_TIMEOUT;
    try {
      await this.page.locator(locator).waitFor({ state: 'detached', timeout });
      this.logger.debug(`Element ${locator} disappeared from DOM`);
    } catch (e) {
      this.logger.error(`Element ${locator} did not disappear within ${timeout}ms: ${String(e)}`);
      throw e;
    }
  }

  async waitForPageLoad(timeout?: number) {
    timeout = timeout || Config.PAGE_LOAD_TIMEOUT;
    try {
      await this.page.waitForLoadState('domcontentloaded', { timeout });
      await this.page.waitForLoadState('load', { timeout });
      try {
        await this.page.waitForLoadState('networkidle', { timeout });
      } catch (innerError) {
        this.logger.warn(`Network idle not reached within ${timeout}ms, continuing anyway: ${String(innerError)}`);
      }
      this.logger.debug('Page loaded successfully');
    } catch (e) {
      this.logger.error(`Page did not load within ${timeout}ms: ${String(e)}`);
      throw e;
    }
  }

  async waitForUrlChange(expectedUrl: string, timeout?: number) {
    timeout = timeout || Config.ELEMENT_WAIT_TIMEOUT;
    try {
      await this.page.waitForURL(expectedUrl, { timeout });
      this.logger.debug(`URL changed to ${expectedUrl}`);
    } catch (e) {
      this.logger.error(`URL did not change to ${expectedUrl} within ${timeout}ms: ${String(e)}`);
      throw e;
    }
  }

  async waitForUrlContains(substring: string, timeout?: number) {
    timeout = timeout || Config.ELEMENT_WAIT_TIMEOUT;
    try {
      await this.page.waitForURL((url) => url.toString().includes(substring), { timeout });
      this.logger.debug(`URL contains '${substring}'`);
    } catch (e) {
      this.logger.error(`URL did not contain '${substring}' within ${timeout}ms: ${String(e)}`);
      throw e;
    }
  }

  async waitForTextToAppear(locator: string, text: string, timeout?: number) {
    timeout = timeout || Config.ELEMENT_WAIT_TIMEOUT;
    try {
      await expect(this.page.locator(locator)).toContainText(text, { timeout });
      this.logger.debug(`Text '${text}' appeared in element ${locator}`);
    } catch (e) {
      this.logger.error(`Text '${text}' did not appear in element ${locator} within ${timeout}ms: ${String(e)}`);
      throw e;
    }
  }
}