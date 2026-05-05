# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: regression\app_tracker_regression.spec.ts >> app tracker regression flow
- Location: tests\regression\app_tracker_regression.spec.ts:11:5

# Error details

```
Error: ADITYA_BIRLA_USER must be provided

expect(received).not.toBe(expected) // Object.is equality

Expected: not ""
```

# Test source

```ts
  1  | import { test, expect, Page } from '@playwright/test';
  2  | import * as dotenv from 'dotenv';
  3  | import * as path from 'path';
  4  | import * as fs from 'fs';
  5  | import { AdityaBirlaLoginPage } from '../../pages/aditya_birla_login_page';
  6  | import { AdityaBirlaTrackerPage } from '../../pages/aditya_birla_tracker_page';
  7  | import { AdityaBirlaLocators } from '../../locators/aditya_birla_locators';
  8  | 
  9  | defaultPaths();
  10 | 
  11 | test('app tracker regression flow', async ({ page }) => {
  12 |   const username = process.env.ADITYA_BIRLA_USER || '';
  13 |   const password = process.env.ADITYA_BIRLA_PASS || '';
  14 | 
> 15 |   expect(username, 'ADITYA_BIRLA_USER must be provided').not.toBe('');
     |                                                              ^ Error: ADITYA_BIRLA_USER must be provided
  16 |   expect(password, 'ADITYA_BIRLA_PASS must be provided').not.toBe('');
  17 | 
  18 |   const loginPage = new AdityaBirlaLoginPage(page);
  19 |   const trackerPage = new AdityaBirlaTrackerPage(page);
  20 |   const locators = new AdityaBirlaLocators(page);
  21 | 
  22 |   await loginPage.load();
  23 |   await loginPage.enterCredentials(username, password);
  24 |   await loginPage.clickLoginButton();
  25 | 
  26 |   await page.waitForURL('**/dashboard', { timeout: 15000 });
  27 |   expect(page.url()).toContain('/dashboard');
  28 | 
  29 |   await trackerPage.navigateToTrackerPage();
  30 | 
  31 |   expect(await trackerPage.isTrackerTableVisible()).toBeTruthy();
  32 |   expect(await trackerPage.isApplicationSearchVisible()).toBeTruthy();
  33 | 
  34 |   const pageUrl = page.url();
  35 |   expect(pageUrl).toContain('app-tracker');
  36 | });
  37 | 
  38 | function defaultPaths() {
  39 |   const envPaths = [
  40 |     path.resolve(__dirname, '..', '..', 'app-tracker-automation', '.env'),
  41 |     path.resolve(__dirname, '..', '..', '.env'),
  42 |     path.resolve(__dirname, '..', '..', 'app-tracker-automation', 'tests', '.env')
  43 |   ];
  44 | 
  45 |   for (const envPath of envPaths) {
  46 |     if (fs.existsSync(envPath)) {
  47 |       dotenv.config({ path: envPath });
  48 |       break;
  49 |     }
  50 |   }
  51 | }
  52 | 
```