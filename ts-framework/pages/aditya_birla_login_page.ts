import { Page } from '@playwright/test';
import { BasePage } from './base_page';
import { AdityaBirlaLocators } from '../locators/aditya_birla_locators';

export class AdityaBirlaLoginPage extends BasePage {
  private locators: AdityaBirlaLocators;

  constructor(page: Page) {
    super(page);
    this.locators = new AdityaBirlaLocators(page);
  }

  async load(): Promise<void> {
    this.logger.info('Loading Aditya Birla UAT login page');
    await this.navigateTo(this.locators.loginPageUrl);
    await this.waits.waitForPageLoad();

    // Wait for network to settle after page load
    await this.page.waitForLoadState('networkidle', { timeout: 10000 });

    // Wait for any loading overlays to disappear
    await this.waitForLoadingOverlayToDisappear();
  }

  async isLoginPageDisplayed(): Promise<boolean> {
    try {
      // Check URL
      const currentUrl = this.page.url();
      if (!currentUrl.includes('leapuat.adityabirlasunlifeinsurance.com')) {
        return false;
      }

      // Check key elements
      const usernameVisible = await this.locators.usernameInput.isVisible();
      const passwordVisible = await this.locators.passwordInput.isVisible();
      const loginButtonVisible = await this.locators.loginButton.isVisible();

      return usernameVisible && passwordVisible && loginButtonVisible;

    } catch (e) {
      this.logger.error(`Error checking login page display: ${String(e)}`);
      return false;
    }
  }

  async enterCredentials(username: string, password: string): Promise<void> {
    try {
      this.logger.info(`Entering credentials for user: ${username}`);

      const usernameInput = this.locators.usernameInput.first();
      await this.waits.waitForElementVisible(this.locators.usernameInput);

      // Wait for element to be fully actionable
      await usernameInput.waitFor({ state: 'attached', timeout: 5000 });
      await usernameInput.waitFor({ state: 'visible', timeout: 5000 });

      await usernameInput.fill(username);

      // Wait for network to settle after username input
      await this.page.waitForLoadState('networkidle', { timeout: 3000 });

      const passwordInput = this.locators.passwordInput.first();
      await this.waits.waitForElementVisible(this.locators.passwordInput);

      // Wait for element to be fully actionable
      await passwordInput.waitFor({ state: 'attached', timeout: 5000 });
      await passwordInput.waitFor({ state: 'visible', timeout: 5000 });

      await passwordInput.fill(password);

      // Verify password masking
      const passwordType = await passwordInput.getAttribute('type');
      if (passwordType !== 'password') {
        this.logger.warn('Password field is not properly masked');
      }

      // Wait for network to settle after password input
      await this.page.waitForLoadState('networkidle', { timeout: 3000 });

      this.logger.info('Credentials entered successfully');

    } catch (e) {
      this.logger.error(`Failed to enter credentials: ${String(e)}`);
      throw e;
    }
  }

  async clickLoginButton(): Promise<void> {
    try {
      this.logger.info('Clicking login button');

      const loginButton = this.locators.loginButton.first();
      
      // NATIVE PLAYWRIGHT WAITS: Replaces custom this.waits method to fix Type mismatch
      await loginButton.waitFor({ state: 'attached', timeout: 5000 });
      await loginButton.waitFor({ state: 'visible', timeout: 5000 });

      // Explicitly check if it is enabled before clicking
      if (!(await loginButton.isEnabled())) {
         throw new Error("Login button is present but disabled.");
      }

      // Wait for any loading overlays to disappear
      await this.waitForLoadingOverlayToDisappear();

      await loginButton.click();

      this.logger.info('Login button clicked');

    } catch (e) {
      this.logger.error(`Failed to click login button: ${String(e)}`);
      throw e;
    }
  }

  async login(username: string, password: string): Promise<boolean> {
    try {
      this.logger.info(`Starting login flow for user: ${username}`);

      // Load login page
      await this.load();

      // Verify page is displayed
      if (!(await this.isLoginPageDisplayed())) {
        throw new Error('Login page is not properly displayed');
      }

      // Enter credentials
      await this.enterCredentials(username, password);

      // Click login
      await this.clickLoginButton();

      // Wait for redirect
      await this.page.waitForTimeout(3000);

      // Check if login was successful (redirected away from login page)
      const currentUrl = this.page.url();
      if (currentUrl.includes('#/login')) {
        // Check for error message
        const errorVisible = await this.locators.errorMessage.isVisible();
        if (errorVisible) {
          const errorText = await this.getErrorMessage();
          this.logger.error(`Login failed with error: ${errorText}`);
          return false;
        } else {
          this.logger.error('Login failed - still on login page');
          return false;
        }
      } else {
        this.logger.info('Login successful - redirected from login page');
        return true;
      }

    } catch (e) {
      this.logger.error(`Login flow failed: ${String(e)}`);
      return false;
    }
  }

  async getErrorMessage(): Promise<string> {
    try {
      const errorElement = this.locators.errorMessage.first();
      if (await errorElement.isVisible()) {
        const text = await errorElement.textContent();
        return text ? text.trim() : '';
      }
      return '';
    } catch {
      return '';
    }
  }

  async verifyUatBadge(): Promise<boolean> {
    return await this.locators.uatBadge.isVisible();
  }

  async verifyBranding(): Promise<boolean> {
    return await this.locators.brandingHeader.isVisible();
  }

  async waitForPageLoad(timeout: number = 10000): Promise<void> {
    try {
      // Wait for URL to contain login
      await this.waits.waitForUrlContains('#/login', timeout);

      // Wait for key elements to be visible
      await this.waits.waitForElementVisible(this.locators.usernameInput, timeout);
      await this.waits.waitForElementVisible(this.locators.passwordInput, timeout);
      await this.waits.waitForElementVisible(this.locators.loginButton, timeout);

      this.logger.info('Login page loaded successfully');

    } catch (e) {
      this.logger.error(`Login page load timeout: ${String(e)}`);
      throw e;
    }
  }

  async clearCredentials(): Promise<void> {
    try {
      const usernameInput = this.locators.usernameInput.first();
      const passwordInput = this.locators.passwordInput.first();

      await usernameInput.fill('');
      await passwordInput.fill('');

      this.logger.info('Credentials cleared');

    } catch (e) {
      this.logger.error(`Failed to clear credentials: ${String(e)}`);
      throw e;
    }
  }

  async isUsernameFocused(): Promise<boolean> {
    try {
      const usernameInput = this.locators.usernameInput.first();
      // FIX: Ask the browser if this element is the currently active/focused element
      return await usernameInput.evaluate((node) => document.activeElement === node);
    } catch {
      return false;
    }
  }

  async isPasswordFocused(): Promise<boolean> {
    try {
      const passwordInput = this.locators.passwordInput.first();
      // FIX: Ask the browser if this element is the currently active/focused element
      return await passwordInput.evaluate((node) => document.activeElement === node);
    } catch {
      return false;
    }
  }

  async getPageTitle(): Promise<string> {
    return await this.page.title();
  }

  private async waitForLoadingOverlayToDisappear(timeout: number = 5000): Promise<void> {
    try {
      // Common loading overlay selectors
      const loadingSelectors = [
        '.loading-overlay',
        '.spinner',
        '.progress-bar',
        "[class*='loading']",
        "[class*='spinner']",
        "[class*='overlay']",
        '.MuiCircularProgress-root',
        '.MuiBackdrop-root'
      ];

      for (const selector of loadingSelectors) {
        try {
          const loadingElement = this.page.locator(selector).first();
          if (await loadingElement.isVisible({ timeout: 1000 })) {
            this.logger.info(`Waiting for loading element to disappear: ${selector}`);
            await loadingElement.waitFor({ state: 'hidden', timeout });
            this.logger.info(`Loading element disappeared: ${selector}`);
          }
        } catch {
          continue;
        }
      }
    } catch (e) {
      this.logger.error(`Error waiting for loading overlay: ${String(e)}`);
    }
  }
}