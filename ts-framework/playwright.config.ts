import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  outputDir: './test-results',
  timeout: 30000,
  expect: {
    timeout: 10000,
  },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: 1,
  workers: 4,
  reporter: [
    ['html', { outputFolder: 'reports/html' }],
    ['json', { outputFile: 'reports/json/report.json' }],
    ['junit', { outputFile: 'reports/junit/report.xml' }],
    ['allure-playwright']
  ],
  use: {
    baseURL: 'https://leapuat.adityabirlasunlifeinsurance.com/uat/#/login',
    headless: process.env.HEADLESS ? process.env.HEADLESS.toLowerCase() === 'true' : false,
    viewport: null,
    ignoreHTTPSErrors: true,
    launchOptions: { args: ['--start-maximized'] },
    screenshot: 'only-on-failure',
    trace: 'on-first-retry',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});