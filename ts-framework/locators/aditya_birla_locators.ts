import { Locator, Page } from '@playwright/test';

export class AdityaBirlaLocators {
  private page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  // Login Page
  get loginPageUrl(): string {
    return 'https://leapuat.adityabirlasunlifeinsurance.com/uat/#/login';
  }

  get loginForm(): Locator {
    return this.page.locator('form');
  }

  get usernameInput(): Locator {
    return this.page.locator("input[type='text']").or(this.page.locator("input[name='username']")).or(this.page.locator("input[id*='login']")).or(this.page.locator("input[placeholder*='Login']"));
  }

  get passwordInput(): Locator {
    return this.page.locator("input[type='password']").or(this.page.locator("input[name='password']"));
  }

  get loginButton(): Locator {
    return this.page.locator("button[type='submit']").or(this.page.locator("button:has-text('LOGIN')")).or(this.page.locator("button:has-text('Login')"));
  }

  get uatBadge(): Locator {
    return this.page.locator("[class*='uat']").or(this.page.locator("[data-env='uat']")).or(this.page.locator('.uat-badge'));
  }

  get errorMessage(): Locator {
    return this.page.locator('.error').or(this.page.locator('.alert')).or(this.page.locator("[class*='error']")).or(this.page.locator("[class*='invalid']"));
  }

  get brandingHeader(): Locator {
    return this.page.locator('header').or(this.page.locator('.header')).or(this.page.locator("[class*='branding']"));
  }

  // Dashboard Page
  get dashboardPageUrl(): string {
    return 'https://leapuat.adityabirlasunlifeinsurance.com/uat/#/dashboard';
  }

  get dashboardHeader(): Locator {
    return this.page.locator('h1').or(this.page.locator('.header')).or(this.page.locator("[class*='application']"));
  }

  get applicationListTitle(): Locator {
    return this.page.locator("h1:has-text('Application List')").or(this.page.locator(".title:has-text('Application List')"));
  }

  get toolbar(): Locator {
    return this.page.locator("[class*='toolbar']").or(this.page.locator("[class*='filter']"));
  }

  get filterButton(): Locator {
    return this.page.locator("[class*='filter']").or(this.page.locator("button:has-text('Filter')"));
  }

  get sortButton(): Locator {
    return this.page.locator("[class*='sort']").or(this.page.locator("button:has-text('Sort')"));
  }

  get dataTable(): Locator {
    return this.page.locator('table').or(this.page.locator("[class*='grid']")).or(this.page.locator("[class*='list']"));
  }

  get dataRows(): Locator {
    return this.page.locator('tbody tr').or(this.page.locator("[class*='row']")).or(this.page.locator('tr'));
  }

  get pendingDots(): Locator {
    return this.page.locator("[class*='pending']").or(this.page.locator("[class*='orange']")).or(this.page.locator("[status*='pending']"));
  }

  get newApplicationButton(): Locator {
    return this.page.locator("button:has-text('NEW APPLICATION')").or(this.page.locator("button:has-text('+ NEW')"));
  }

  get menuButton(): Locator {
    return this.page.locator("button:has-text('MENU')").or(this.page.locator("[class*='menu']")).or(this.page.locator('.dropdown-toggle'));
  }

  // Menu Navigation
  get menuDropdown(): Locator {
    return this.page.locator('.dropdown').or(this.page.locator("[class*='dropdown']"));
  }

  get helpItem(): Locator {
    return this.page.locator("a:has-text('Help')").or(this.page.locator("[role='menuitem']:has-text('Help')"));
  }

  get applicationTrackerItem(): Locator {
    return this.page.locator("a:has-text('Application Tracker')").or(this.page.locator("[role='menuitem']:has-text('Application Tracker')"));
  }

  get approvalsItem(): Locator {
    return this.page.locator("a:has-text('Approvals')").or(this.page.locator("[role='menuitem']:has-text('Approvals')"));
  }

  get logoutItem(): Locator {
    return this.page.locator("a:has-text('Logout')").or(this.page.locator("[role='menuitem']:has-text('Logout')"));
  }

  // Application Tracker Page
  get trackerPageUrl(): string {
    return 'https://onboarding-uat.adityabirlasunlifeinsurance.com/app-tracker/applications';
  }

  get trackerHeader(): Locator {
    return this.page.locator('h1').or(this.page.locator('.title')).or(this.page.locator("[class*='header']"));
  }

  get policyListTitle(): Locator {
    return this.page.locator("h1:has-text('Policy List')").or(this.page.locator(".title:has-text('Policy List')"));
  }

  get refreshInfo(): Locator {
    return this.page.locator("[class*='meta']").or(this.page.locator("[class*='info']:has-text('refreshes every 15 minutes')"));
  }

  get filterChips(): Locator {
    return this.page.locator("[class*='filter']").or(this.page.locator("[class*='chip']"));
  }

  get searchBar(): Locator {
    return this.page.locator("[class*='search']").or(this.page.locator("input[type='search']"));
  }

  get dateRangePicker(): Locator {
    return this.page.locator("[class*='date']").or(this.page.locator("[class*='picker']")).or(this.page.locator("input[type='date']"));
  }

  get tableHeaders(): Locator {
    return this.page.locator('th').or(this.page.locator("[class*='header']")).or(this.page.locator("[class*='column']"));
  }

  get tableRows(): Locator {
    return this.page.locator('tbody tr').or(this.page.locator("[class*='row']")).or(this.page.locator('tr'));
  }

  // Table Columns
  get appNoColumn(): Locator {
    return this.page.locator("th:has-text('App.No')").or(this.page.locator("[class*='header']:has-text('App.No')"));
  }

  get proposerNameColumn(): Locator {
    return this.page.locator("th:has-text('Proposer Name')").or(this.page.locator("[class*='header']:has-text('Proposer Name')"));
  }

  get planNameColumn(): Locator {
    return this.page.locator("th:has-text('Plan Name')").or(this.page.locator("[class*='header']:has-text('Plan Name')"));
  }

  get modalPremiumColumn(): Locator {
    return this.page.locator("th:has-text('Modal Premium')").or(this.page.locator("[class*='header']:has-text('Modal Premium')"));
  }

  get policyStatusColumn(): Locator {
    return this.page.locator("th:has-text('Policy Status')").or(this.page.locator("[class*='header']:has-text('Policy Status')"));
  }

  // Common Elements
  get loadingSpinner(): Locator {
    return this.page.locator('.loading').or(this.page.locator("[class*='spinner']")).or(this.page.locator("[class*='loading']"));
  }

  get errorToast(): Locator {
    return this.page.locator('.toast').or(this.page.locator('.alert')).or(this.page.locator("[class*='error']")).or(this.page.locator("[class*='toast']"));
  }

  get successMessage(): Locator {
    return this.page.locator('.success').or(this.page.locator("[class*='success']")).or(this.page.locator("[class*='toast-success']"));
  }

  get pageContent(): Locator {
    return this.page.locator('main').or(this.page.locator('.content')).or(this.page.locator("[class*='main']"));
  }

  get footer(): Locator {
    return this.page.locator('footer').or(this.page.locator('.footer'));
  }
}