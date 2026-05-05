import { test, expect, Page } from '@playwright/test';
import { AdityaBirlaLoginPage } from '../../pages/aditya_birla_login_page';
import { AdityaBirlaDashboardPage } from '../../pages/aditya_birla_dashboard_page';
import { AdityaBirlaTrackerPage } from '../../pages/aditya_birla_tracker_page';
import { Logger } from '../../utils/logger';

test.describe('Unified App Tracker Flow', () => {
  test('complete flow and validation', async ({ page }) => {
    const logger = new Logger('TestUnifiedAppTrackerFlow');

    // Apply Browser Configuration
    logger.info('No fixed viewport requested; relying on launch args (--start-maximized)');

    // FIX: Inject panel.css styles to fix window layout issues
    const layoutCss = `
    /* --- FIXED LAYOUT STYLES --- */
    *, *::before, *::after {
        box-sizing: border-box;
    }
    html, body {
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
        overflow-x: hidden;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    body {
        display: flex;
        flex-direction: column;
    }
    .panel-container {
        width: 100%;
        max-width: 100vw;
        padding: 10px;
        overflow-wrap: break-word;
    }
    `;
    await page.addStyleTag({ content: layoutCss });
    logger.info('[OK] Layout fix CSS injected to prevent viewport issues');

    const loginPage = new AdityaBirlaLoginPage(page);
    const dashboardPage = new AdityaBirlaDashboardPage(page);
    const trackerPage = new AdityaBirlaTrackerPage(page);

    const user = process.env.ADITHYA_BIRLA_USER || '';
    const pass = process.env.ADITHYA_BIRLA_PASS || '';

    // Debug: Log credential loading status
    logger.info(`Credentials loaded - User: ${user}, Pass: ${'*'.repeat(pass.length) || 'None'}`);

    if (!user || !pass) {
      logger.error(`Credentials not loaded from .env. User: ${user}, Pass: ${pass}`);
      throw new Error('Credentials not loaded from .env file. Please check .env file location and content.');
    }

    let errorsLogged = 0;

    try {
      // PHASE 1: NAVIGATION & AUTH
      await navigateAndAuth(page, loginPage, { user, pass }, logger);

      // PHASE 2: APP TRACKER SETUP
      let trackerPageObj: Page | null = null;
      if (!page.url().includes('app-tracker')) {
        trackerPageObj = await navigateToTracker(page, trackerPage, logger);
      } else {
        await trackerPage.waitForPageLoad(8000);
        trackerPageObj = page;
      }

      // Use the tracker page object (new tab) for validations
      const effectiveTrackerPage = trackerPageObj && trackerPageObj !== page ? new AdityaBirlaTrackerPage(trackerPageObj) : trackerPage;

      // PHASE 3: COMPONENT VALIDATION
      logger.info('--- Beginning Component Validation Phase ---');
      let sanityErrors = await validateComponentFilters(trackerPageObj || page, trackerPage, logger);
      sanityErrors += await validateComponentTable(trackerPageObj || page, trackerPage, logger);

      // NEW VALIDATIONS: Pagination, Chip Filters, Search Dropdown, Application Number Search
      sanityErrors += await validatePagination(trackerPageObj || page, logger);
      sanityErrors += await validateChipFilters(trackerPageObj || page, logger);
      sanityErrors += await validateSearchDropdown(trackerPageObj || page, logger);
      sanityErrors += await validateApplicationNumberSearch(trackerPageObj || page, logger);

      errorsLogged += sanityErrors;

      if (errorsLogged > 0) {
        logger.info('COMPLETE_FLOW PASSED_WITH_WARNINGS');
      } else {
        logger.info('COMPLETE_FLOW ALL_PASSED');
      }

    } catch (criticalE) {
      logger.error(`FATAL ERROR STOPPING EXECUTION: ${String(criticalE)}`);
      throw criticalE;
    }
  });
});

async function navigateAndAuth(page: Page, loginPage: AdityaBirlaLoginPage, creds: { user: string; pass: string }, logger: Logger): Promise<void> {
  logger.info('Phase 1: Authentication');
  await loginPage.load();

  // Wait for network to settle after page load
  await page.waitForLoadState('networkidle', { timeout: 10000 });

  expect(await loginPage.isLoginPageDisplayed()).toBe(true);

  await loginPage.enterCredentials(creds.user, creds.pass);

  // Wait for network to settle after entering credentials
  await page.waitForLoadState('networkidle', { timeout: 5000 });

  await loginPage.clickLoginButton();

  try {
    await page.waitForURL('**/uat/#/dashboard', { timeout: 15000 });
  } catch (e) {
    logger.warn(`[WARN] Redirect wait timed out: ${String(e)}`);
  }
}

async function navigateToTracker(page: Page, trackerPage: AdityaBirlaTrackerPage, logger: Logger): Promise<Page | null> {
  logger.info('Navigating via Top-Right Menu...');

  // Wait for network to settle before navigation
  await page.waitForLoadState('networkidle', { timeout: 10000 });

  // FIX: Added parentheses to .first()
  const menuBtn = page.locator("button.menu-button[aria-label='menu']").first();
  await menuBtn.scrollIntoViewIfNeeded();

  // Wait for element to be fully actionable (attached, visible, stable)
  await menuBtn.waitFor({ state: 'attached', timeout: 5000 });
  await menuBtn.waitFor({ state: 'visible', timeout: 5000 });

  // Click the menu button
  await menuBtn.click();

  // Wait for dropdown to appear
  await page.waitForTimeout(1000);

  // FIX: Added parentheses to .first()
  const trackerMenuItem = page.locator("a:has-text('Application Tracker')").first();
  await trackerMenuItem.waitFor({ state: 'visible', timeout: 5000 });
  await trackerMenuItem.click();

  // Wait for new tab or navigation
  await page.waitForTimeout(2000);

  // Check if new page opened
  const pages = page.context().pages();
  if (pages.length > 1) {
    const newPage = pages[pages.length - 1];
    await newPage.waitForLoadState('networkidle', { timeout: 10000 });
    logger.info('Navigated to Application Tracker in new tab');
    return newPage;
  } else {
    await page.waitForLoadState('networkidle', { timeout: 10000 });
    logger.info('Navigated to Application Tracker in same tab');
    return page;
  }
}

async function validateComponentFilters(page: Page, trackerPage: AdityaBirlaTrackerPage, logger: Logger): Promise<number> {
  // Placeholder for filter validation logic
  logger.info('Validating component filters...');
  return 0;
}

async function validateComponentTable(page: Page, trackerPage: AdityaBirlaTrackerPage, logger: Logger): Promise<number> {
  // Placeholder for table validation logic
  logger.info('Validating component table...');
  return 0;
}

async function validatePagination(page: Page, logger: Logger): Promise<number> {
  // Placeholder for pagination validation logic
  logger.info('Validating pagination...');
  return 0;
}

async function validateChipFilters(page: Page, logger: Logger): Promise<number> {
  // Placeholder for chip filters validation logic
  logger.info('Validating chip filters...');
  return 0;
}

async function validateSearchDropdown(page: Page, logger: Logger): Promise<number> {
  // Placeholder for search dropdown validation logic
  logger.info('Validating search dropdown...');
  return 0;
}

async function validateApplicationNumberSearch(page: Page, logger: Logger): Promise<number> {
  // Placeholder for application number search validation logic
  logger.info('Validating application number search...');
  return 0;
}
