import { test, expect, Page } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';
import * as dotenv from 'dotenv';
import { AdityaBirlaLoginPage } from '../../pages/aditya_birla_login_page';
import { AdityaBirlaDashboardPage } from '../../pages/aditya_birla_dashboard_page';
import { AdityaBirlaTrackerPage } from '../../pages/aditya_birla_tracker_page';
import { Logger } from '../../utils/logger';

defaultPaths();

test.describe('Login Tracker Navigation', () => {
  test('login to tracker navigation', async ({ page }) => {
    const logger = new Logger('TestLoginTrackerNavigation');
    const loginPage = new AdityaBirlaLoginPage(page);
    const dashboardPage = new AdityaBirlaDashboardPage(page);
    const trackerPage = new AdityaBirlaTrackerPage(page);

    const username = process.env.ADITYA_BIRLA_USER || '';
    const password = process.env.ADITYA_BIRLA_PASS || '';

    logger.info(`Credentials loaded - User: ${username}, Pass: ${password ? '*'.repeat(password.length) : 'None'}`);

    expect(username, 'ADITYA_BIRLA_USER is required').not.toBe('');
    expect(password, 'ADITYA_BIRLA_PASS is required').not.toBe('');

    try {
      await loginPage.load();
      await loginPage.enterCredentials(username, password);
      await loginPage.clickLoginButton();

      await page.waitForURL('**/uat/#/dashboard', { timeout: 15000 });
      logger.info('[OK] Successfully redirected to dashboard');

      logger.info('Phase 2: App Tracker Navigation');
      const menuBtn = page.locator("button.menu-button[aria-label='menu']").first();
      await menuBtn.scrollIntoViewIfNeeded();
      await menuBtn.waitFor({ state: 'visible', timeout: 5000 });
      await menuBtn.click();
      logger.info('[OK] MENU button clicked');

      await page.waitForTimeout(500);

      const linkSelectors = [
        "a:has-text('Application Tracker')",
        "button:has-text('Application Tracker')",
        "[role='menuitem']:has-text('Application Tracker')",
        "li:has-text('Application Tracker') a"
      ];

      let link = null as null | import('@playwright/test').Locator;
      for (const selector of linkSelectors) {
        const tempLink = page.locator(selector).first();
        if (await tempLink.isVisible({ timeout: 2000 })) {
          link = tempLink;
          logger.info(`Found Application Tracker using selector: ${selector}`);
          break;
        }
      }

      expect(link, 'Application Tracker link not found in menu').not.toBeNull();
      await link!.scrollIntoViewIfNeeded();
      await link!.click({ force: true });
      logger.info('[OK] Application Tracker link clicked');

      await page.waitForTimeout(2000);
      const pages = page.context().pages();
      let trackerPageObj = pages.find((p) => p.url().includes('app-tracker')) || page;
      await trackerPageObj.bringToFront();

      const expectedUrlPattern = 'https://onboarding-uat.adityabirlasunlifeinsurance.com/app-tracker/applications';
      const actualUrl = trackerPageObj.url();
      if (actualUrl.includes(expectedUrlPattern)) {
        logger.info(`[OK] URL Validation PASSED: ${actualUrl}`);
      } else {
        logger.warn(`URL mismatch. Expected: ${expectedUrlPattern}, Got: ${actualUrl}`);
      }

      await trackerPageObj.waitForLoadState('networkidle', { timeout: 10000 });
      const effectiveTrackerPage = trackerPageObj !== page ? new AdityaBirlaTrackerPage(trackerPageObj) : trackerPage;
      await effectiveTrackerPage.waitForPageLoad(15000);
      logger.info('Application Tracker page loaded');

      const title = trackerPageObj.locator("h1, .title, [class*='header']").first();
      expect(await title.isVisible({ timeout: 3000 })).toBeTruthy();
      logger.info('[OK] Tracker title visible');

      const searchBox = trackerPageObj.locator("input[type='text'], input[placeholder*='Search']").first();
      expect(await searchBox.isVisible({ timeout: 3000 })).toBeTruthy();
      logger.info('[OK] Search box visible');

      const table = trackerPageObj.locator("table, [class*='table'], [class*='grid']").first();
      expect(await table.isVisible({ timeout: 3000 })).toBeTruthy();
      logger.info('[OK] Table visible');

    } catch (error) {
      logger.error(`Test failed with error: ${String(error)}`);
      await page.screenshot({ path: 'screenshots/failed/test_login_tracker_failure.png', fullPage: true });
      throw error;
    }
  });
});

function defaultPaths() {
  const envPaths = [
    path.resolve(__dirname, '..', '..', '.env'),
    path.resolve(__dirname, '..', '..', '..', '.env'),
    path.resolve(__dirname, '..', '..', 'data', '.env')
  ];

  for (const envPath of envPaths) {
    if (fs.existsSync(envPath)) {
      dotenv.config({ path: envPath });
      break;
    }
  }
}

