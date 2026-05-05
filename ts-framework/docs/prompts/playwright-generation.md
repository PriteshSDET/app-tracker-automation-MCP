# Playwright Code Generation Prompt (TypeScript)

## Purpose
Generate robust Playwright test code using TypeScript from test cases, incorporating learned synchronization patterns.

## Framework Standards
- Use **Page Object Model (POM)** pattern.
- Implement **component-driven architecture**.
- Follow **TypeScript naming conventions** (camelCase for methods, PascalCase for classes).
- Include comprehensive **logging** using the framework's `Logger` class.
- Apply synchronization best practices (Avoid `waitForTimeout`).

## Environment-Aware Code Generation

### For UAT Environments
**Timeout Configuration:**
```typescript
const TIMEOUT_UAT = 15000;  // 15 seconds for UAT
const TIMEOUT_DEV = 3000;   // 3 seconds for dev
```

**Synchronization Pattern:**
```typescript
// Before critical interactions
await page.waitForLoadState('networkidle', { timeout: 15000 });

// Before element interactions
await element.waitFor({ state: 'attached', timeout: 5000 });
await element.waitFor({ state: 'visible', timeout: 5000 });
await element.waitFor({ state: 'enabled', timeout: 5000 });
```

## Code Structure

### Test File Template
```typescript
import { test, expect } from '@playwright/test';
import { LoginPage } from '../../pages/aditya_birla_login_page';
import { Logger } from '../../utils/logger';

test('Test Case Name', async ({ page }) => {
    const logger = new Logger('TestScenario');
    const loginPage = new LoginPage(page);
    
    logger.info('Phase 1: Authentication');
    await loginPage.load();
    await loginPage.enterCredentials(process.env.USER!, process.env.PASS!);
    
    logger.info('Phase 2: Validation');
    await expect(page.locator('.dashboard')).toBeVisible({ timeout: 15000 });
});
```

### Page Object Template
```typescript
import { Page, Locator } from '@playwright/test';
import { BasePage } from './base_page';

export class LoginPage extends BasePage {
    readonly usernameInput: Locator;
    readonly passwordInput: Locator;
    readonly loginButton: Locator;

    constructor(page: Page) {
        super(page);
        this.usernameInput = page.locator('#username');
        this.passwordInput = page.locator('#password');
        this.loginButton = page.locator('button[type="submit"]');
    }

    async enterCredentials(user: string, pass: string) {
        await this.waitForNetworkIdle();
        await this.usernameInput.fill(user);
        await this.passwordInput.fill(pass);
    }
}
```

## Best Practices

### ✅ DO Use These Patterns
1. **Network Idle Waits**: `await page.waitForLoadState('networkidle', { timeout: 15000 });`
2. **Explicit Waits**: `await element.waitFor({ state: 'visible' });`
3. **Flexible Selectors**: Use `page.locator('button').filter({ hasText: 'Submit' }).first()`
4. **Soft Logging**: Wrap optional validations in try-catch with `logger.warn()`.

### ❌ DON'T Use These Patterns
1. **Static Timeouts**: `await page.waitForTimeout(5000);` (Flaky)
2. **Single Element Assumption**: Always use `.first()` or specific filters to avoid strict mode violations.
3. **Hardcoded Selectors**: Move selectors to Locators or POM classes.

---
*Last Updated: May 5, 2026 - Migrated to TypeScript/Playwright Native Framework*
