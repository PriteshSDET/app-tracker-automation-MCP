# Test Execution Guide - Login & Application Tracker (TypeScript)

## Overview
This guide provides step-by-step instructions for executing the Playwright/TypeScript test suite for Login & Application Tracker navigation using the migrated **ts-framework**.

## Framework Structure

### 📝 Test Case Input
- **`ts-framework/docs/stories/Login.md`** - Original test case specification

### 🤖 TypeScript Test Files
- **`ts-framework/tests/regression/app_tracker_regression.spec.ts`** - Main regression test implementation
- **`ts-framework/tests/smoke/test_login_tracker.spec.ts`** - Smoke test implementation

### 🏗️ Framework Components
- **`ts-framework/locators/aditya_birla_locators.ts`** - Aditya Birla specific element locators
- **`ts-framework/pages/`** - Page Objects (Login, Dashboard, Tracker)
- **`ts-framework/components/`** - Modular UI components (TopNav, FilterChips, etc.)

## Execution Instructions

### Prerequisites
1. **Install Dependencies**:
   ```bash
   cd ts-framework
   npm install
   npx playwright install
   ```

2. **Environment Setup**:
   - Configure credentials in `ts-framework/data/.env` or project root `.env`:
     ```bash
     ADITYA_BIRLA_USER=your_username
     ADITYA_BIRLA_PASS=your_password
     ```

### Option 1: Quick Execution (Headed)
```bash
cd ts-framework
npx playwright test app_tracker_regression.spec.ts --headed
```

### Option 2: Full Regression with Reporting
```bash
cd ts-framework
npx playwright test --reporter=html,list
```

### Option 3: Debug Mode
```bash
cd ts-framework
npx playwright test --debug
```

## Test Coverage

### ✅ Main Test Flow
1. **Top Navigation Interactions**: Theme toggling, Account Menu validation (Initials verification).
2. **Filter Chips Interactions**: Opening dropdown, clearing filters, selecting status, and table verification.
3. **Search Bar Validation**: Searching by App No. and verifying results.
4. **Pagination Validation**: Ensuring footer visibility and data counts.
5. **Policy Table Validation**: Data integrity and column checks.
6. **Detail Drawer Validation**: Row selection and side drawer content verification.

## Reports and Artifacts

### 📊 Generated Reports
- **HTML Report**: `ts-framework/reports/html/index.html` (or `playwright-report/`)
- **JSON Results**: `ts-framework/reports/json/report.json`

### 📸 Screenshots & Videos
- **Screenshots**: `ts-framework/test-results/` (on failure)
- **Videos**: `ts-framework/test-results/` (on failure)

## Troubleshooting

### Common Issues
1. **Navigation Failures**:
   - Ensure the `.env` file is in `ts-framework/data/` or the root.
   - Verify UAT environment availability.

2. **Timeout Errors**:
   - Playwright default timeout is 30s. Adjust in `playwright.config.ts` if environment is slow.

---

**Ready for Execution!** 🚀
Run `npx playwright test --headed` to see the automated flow in action.

