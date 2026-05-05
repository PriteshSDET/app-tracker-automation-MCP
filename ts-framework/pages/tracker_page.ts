import { Page } from '@playwright/test';
import { BasePage } from './base_page';
import { TrackerLocators } from '../locators/tracker_locators';

export class TrackerPage extends BasePage {
  private locators: TrackerLocators;

  constructor(page: Page) {
    super(page);
    this.locators = new TrackerLocators();
  }

  async isTrackerDisplayed(): Promise<boolean> {
    return await this.isElementVisible(this.locators.tracker_container);
  }

  async searchApplication(applicationId: string): Promise<void> {
    await this.fillText(this.locators.search_input, applicationId);
    await this.clickElement(this.locators.search_button);
  }

  async getApplicationStatus(applicationId: string): Promise<string> {
    const locator = `${this.locators.application_row}[data-id='${applicationId}'] ${this.locators.status_column}`;
    return await this.page.locator(locator).textContent() || '';
  }

  async filterByStatus(status: string): Promise<void> {
    await this.clickElement(this.locators.status_filter);
    await this.clickElement(`${this.locators.status_option}[data-status='${status}']`);
  }

  async viewApplicationDetails(applicationId: string): Promise<void> {
    const locator = `${this.locators.application_row}[data-id='${applicationId}'] ${this.locators.view_details_button}`;
    await this.clickElement(locator);
  }

  async exportApplications(format: string = 'excel'): Promise<void> {
    await this.clickElement(this.locators.export_button);
    await this.clickElement(`${this.locators.export_option}[data-format='${format}']`);
  }

  async getTotalApplicationsCount(): Promise<number> {
    const text = await this.page.locator(this.locators.total_count).textContent();
    return text ? parseInt(text) : 0;
  }
}