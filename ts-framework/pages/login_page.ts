import { Page } from '@playwright/test';
import { BasePage } from './base_page';
import { LoginLocators } from '../locators/login_locators';

export class LoginPage extends BasePage {
  private locators: LoginLocators;

  constructor(page: Page) {
    super(page);
    this.locators = new LoginLocators();
  }

  async load(): Promise<void> {
    await this.navigateTo('/login');
    await this.waitForPageLoad();
  }

  async login(username: string, password: string): Promise<void> {
    this.logger.info(`Attempting login for user: ${username}`);

    // Enter username
    await this.page.locator(this.locators.username_input).fill(username);

    // Enter password
    await this.page.locator(this.locators.password_input).fill(password);

    // Click login button
    await this.page.locator(this.locators.login_button).click();

    // Wait for login to complete
    await this.waits.waitForElementDisappear(this.locators.login_button);
  }

  async isLoginPageDisplayed(): Promise<boolean> {
    return await this.isElementVisible(this.locators.login_form);
  }

  async getErrorMessage(): Promise<string> {
    return await this.page.locator(this.locators.error_message).textContent() || '';
  }

  async isLoginSuccessful(): Promise<boolean> {
    return !(await this.isElementVisible(this.locators.login_form));
  }
}