import { Page } from '@playwright/test';
import { BasePage } from './base_page';
import { SharedLocators } from '../locators/shared_locators';

export class DashboardPage extends BasePage {
  private locators: SharedLocators;

  constructor(page: Page) {
    super(page);
    this.locators = new SharedLocators();
  }

  async isDashboardDisplayed(): Promise<boolean> {
    return await this.isElementVisible(this.locators.dashboard_container);
  }

  async getWelcomeMessage(): Promise<string> {
    return await this.page.locator(this.locators.welcome_message).textContent() || '';
  }

  async navigateToPolicies(): Promise<void> {
    await this.clickElement(this.locators.policies_link);
  }

  async navigateToClaims(): Promise<void> {
    await this.clickElement(this.locators.claims_link);
  }

  async navigateToProfile(): Promise<void> {
    await this.clickElement(this.locators.profile_link);
  }

  async logout(): Promise<void> {
    await this.clickElement(this.locators.logout_button);
  }

  async getActivePoliciesCount(): Promise<number> {
    const text = await this.page.locator(this.locators.active_policies_count).textContent();
    return text ? parseInt(text) : 0;
  }

  async getPendingClaimsCount(): Promise<number> {
    const text = await this.page.locator(this.locators.pending_claims_count).textContent();
    return text ? parseInt(text) : 0;
  }
}