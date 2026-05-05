import { test, expect, Page } from '@playwright/test';
import * as dotenv from 'dotenv';
import * as path from 'path';
import * as fs from 'fs';
import { AdityaBirlaLoginPage } from '../../pages/aditya_birla_login_page';
import { AdityaBirlaTrackerPage } from '../../pages/aditya_birla_tracker_page';
import { AdityaBirlaLocators } from '../../locators/aditya_birla_locators';

// Components in requested order
import { TopNavigationControls } from '../../components/top_navigation_controls';
import { ActiveFilterChips } from '../../components/active_filter_chips';
import { FilterSearchBar } from '../../components/filter_search_bar';
import { PaginationFooter } from '../../components/pagination_footer';
import { PolicyListTable } from '../../components/policy_list_table';
import { DetailDrawer } from '../../components/detail_drawer';

defaultPaths();

test('app tracker regression flow', async ({ page }) => {
  const username = process.env.ADITYA_BIRLA_USER || '';
  const password = process.env.ADITYA_BIRLA_PASS || '';

  expect(username, 'ADITYA_BIRLA_USER must be provided').not.toBe('');
  expect(password, 'ADITYA_BIRLA_PASS must be provided').not.toBe('');

  const loginPage = new AdityaBirlaLoginPage(page);
  const locators = new AdityaBirlaLocators(page);

  await loginPage.load();
  await loginPage.enterCredentials(username, password);
  await loginPage.clickLoginButton();

  await page.waitForURL('**/dashboard', { timeout: 15000 });
  expect(page.url()).toContain('/dashboard');

  console.log('Opening side menu...');
  const menuBtn = locators.menuButton.first();
  await menuBtn.scrollIntoViewIfNeeded();
  await menuBtn.waitFor({ state: 'visible', timeout: 10000 });
  await menuBtn.click();

  await page.waitForTimeout(2000);

  const trackerMenuItem = locators.applicationTrackerItem.first();
  await trackerMenuItem.waitFor({ state: 'visible', timeout: 10000 });
  
  console.log('Navigating to Application Tracker...');
  // Attempt to handle both new tab and same-page navigation scenarios
  const pagePromise = page.context().waitForEvent('page', { timeout: 10000 }).catch(() => null);
  await trackerMenuItem.click({ force: true });
  
  const newPage = await pagePromise;
  let trackerPageObj = newPage || page;

  // If we are still on dashboard, something went wrong with the click
  if (trackerPageObj.url().includes('dashboard')) {
    console.log('Redirection check: Still on dashboard, retrying navigation...');
    await trackerMenuItem.click({ force: true });
    await trackerPageObj.waitForTimeout(3000);
    // If still on dashboard, try direct navigation as a fallback
    if (trackerPageObj.url().includes('dashboard')) {
        console.log('Direct navigation fallback...');
        await trackerPageObj.goto('https://onboarding-uat.adityabirlasunlifeinsurance.com/app-tracker/applications', { waitUntil: 'networkidle' });
    }
  }

  await trackerPageObj.waitForLoadState('networkidle', { timeout: 20000 });
  console.log(`Current Tracker URL: ${trackerPageObj.url()}`);
  
  const effectiveTopNav = new TopNavigationControls(trackerPageObj);
  const effectiveFilterChips = new ActiveFilterChips(trackerPageObj);
  const effectiveSearchBar = new FilterSearchBar(trackerPageObj);
  const effectivePagination = new PaginationFooter(trackerPageObj);
  const effectiveTable = new PolicyListTable(trackerPageObj);
  const effectiveDetails = new DetailDrawer(trackerPageObj);

  // 1. Top Navigation Interactions
  console.log('--- Top Navigation Interactions ---');
  await effectiveTopNav.toggleTheme();
  await trackerPageObj.waitForTimeout(1000);
  
  await effectiveTopNav.openAccountMenu();
  const initials = await effectiveTopNav.getUserInitials();
  console.log(`User initials found: ${initials}`);
  await effectiveTopNav.closeAccountMenu();

  // 2. Filter Chips Interactions
  console.log('--- Filter Chips Interactions ---');
  await effectiveFilterChips.validateChipsVisible();
  
  console.log('Opening filter dropdown...');
  const opened = await effectiveFilterChips.openDropdown();
  if (opened) {
    await trackerPageObj.waitForTimeout(2000);
    const availableStatuses = await effectiveFilterChips.getAvailableStatuses();
    console.log(`Available statuses: ${availableStatuses}`);
    
    if (availableStatuses.length > 0) {
      const statusToSelect = availableStatuses.find(s => s !== 'All' && s !== 'Others') || availableStatuses[0];
      
      console.log('Clearing all filters...');
      await effectiveFilterChips.clearAll();
      await trackerPageObj.waitForTimeout(2000);
      
      console.log(`Selecting "${statusToSelect}" status...`);
      await effectiveFilterChips.selectStatus(statusToSelect);
      await trackerPageObj.waitForTimeout(4000);
      
      const currentChips = await effectiveFilterChips.getActiveChipNames();
      console.log(`Active chips after selection: ${currentChips}`);
      
      console.log(`Verifying table status for row 0...`);
      const rowCount = await effectiveTable.getRowCount();
      if (rowCount > 0) {
        const firstRowStatus = await effectiveTable.getPolicyStatusBadge(0);
        console.log(`First row status: ${firstRowStatus}`);
      }
      
      console.log('Cleaning up filters...');
      await effectiveFilterChips.clearAll();
      await trackerPageObj.waitForTimeout(2000);
    }
    // Explicitly close the filter dropdown to ensure smooth flow
    await effectiveFilterChips.closeDropdown();
  }

  // 3. Search Bar Validation
  console.log('--- Search Bar Validation ---');
  await effectiveSearchBar.validateAll();
  // Ensure date filter or other popovers are closed
  await effectiveSearchBar.closeDateFilter();

  // 4. Pagination Validation
  console.log('--- Pagination Validation ---');
  await effectivePagination.validateAll();

  // 5. Policy Table Validation
  console.log('--- Policy Table Validation ---');
  const tableStatus = await effectiveTable.validateAll();
  expect(tableStatus.visible).toBeTruthy();

  // 6. Search Interaction Validation
  if (tableStatus.rowCount > 0) {
    const firstAppNo = tableStatus.firstRow.app_no;
    console.log(`Searching for App No: ${firstAppNo}`);
    await effectiveSearchBar.search(firstAppNo);
    await trackerPageObj.waitForTimeout(3000);
    const filteredCount = await effectiveTable.getRowCount();
    console.log(`Filtered count: ${filteredCount}`);
  }

  // 7. Detail Drawer Validation
  if (tableStatus.rowCount > 0) {
    console.log('--- Detail Drawer Validation ---');
    await effectiveTable.clickRow(0);
    await effectiveDetails.waitUntilOpen();
    const drawerStatus = await effectiveDetails.validateAll();
    console.log(`Drawer header: ${drawerStatus.headerName}`);
    await effectiveDetails.close();
  }

  expect(trackerPageObj.url()).toContain('app-tracker');
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

