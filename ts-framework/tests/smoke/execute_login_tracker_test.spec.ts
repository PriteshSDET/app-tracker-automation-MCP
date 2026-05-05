import { test, expect, Page } from '@playwright/test';
import * as dotenv from 'dotenv';
import * as path from 'path';
import * as fs from 'fs';
import { AdityaBirlaLoginPage } from '../../pages/aditya_birla_login_page';
import { AdityaBirlaDashboardPage } from '../../pages/aditya_birla_dashboard_page';
import { AdityaBirlaTrackerPage } from '../../pages/aditya_birla_tracker_page';
import { Logger } from '../../utils/logger';

defaultPaths();

test('execute login tracker test', async ({ page }) => {
  const logger = new Logger('ExecuteLoginTrackerTest');
  const loginPage = new AdityaBirlaLoginPage(page);
  const dashboardPage = new AdityaBirlaDashboardPage(page);
  const trackerPage = new AdityaBirlaTrackerPage(page);

  const username = process.env.ADITYA_BIRLA_USER || '';
  const password = process.env.ADITYA_BIRLA_PASS || '';

  expect(username, 'ADITYA_BIRLA_USER is required').not.toBe('');
  expect(password, 'ADITYA_BIRLA_PASS is required').not.toBe('');

  try {
    await loginPage.load();
    await loginPage.enterCredentials(username, password);
    await loginPage.clickLoginButton();

    await page.waitForURL('**/uat/#/dashboard', { timeout: 15000 });
    logger.info('[OK] Dashboard loaded after login');

    await page.waitForLoadState('networkidle', { timeout: 10000 });

    const menuBtn = page.locator("button.menu-button[aria-label='menu']").first();
    await menuBtn.scrollIntoViewIfNeeded();
    await menuBtn.waitFor({ state: 'visible', timeout: 5000 });
    await menuBtn.click();

    await page.waitForTimeout(500);

    const linkSelectors = [
      "a:has-text('Application Tracker')",
      "button:has-text('Application Tracker')",
      "[role='menuitem']:has-text('Application Tracker')",
      "li:has-text('Application Tracker') a"
    ];

    let trackerLink = null as null | import('@playwright/test').Locator;
    for (const selector of linkSelectors) {
      const candidate = page.locator(selector).first();
      if (await candidate.isVisible({ timeout: 2000 })) {
        trackerLink = candidate;
        break;
      }
    }

    expect(trackerLink, 'Application Tracker navigation link not found').not.toBeNull();
    await trackerLink!.click({ force: true });

    await page.waitForTimeout(2000);
    const pages = page.context().pages();
    const trackerPageObj = pages.find((p) => p.url().includes('app-tracker')) || page;

    await trackerPageObj.waitForLoadState('networkidle', { timeout: 10000 });
    const targetTrackerPage = trackerPageObj !== page ? new AdityaBirlaTrackerPage(trackerPageObj) : trackerPage;
    await targetTrackerPage.waitForPageLoad(15000);

    const title = trackerPageObj.locator("h1, .title, [class*='header']").first();
    expect(await title.isVisible({ timeout: 3000 })).toBeTruthy();

    const table = trackerPageObj.locator("table, [class*='table'], [class*='grid']").first();
    expect(await table.isVisible({ timeout: 3000 })).toBeTruthy();

    logger.info('Execute login tracker test completed successfully');
  } catch (error) {
    await page.screenshot({ path: 'screenshots/failed/execute_login_tracker_test_failure.png', fullPage: true });
    throw error;
  }
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

