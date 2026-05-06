# Playwright Code Generation Prompt (Python)

## Purpose
Generate robust Playwright test code using Python from test cases, incorporating learned synchronization patterns.

## Framework Standards
- Use **Page Object Model (POM)** pattern.
- Implement **component-driven architecture**.
- Follow **Python naming conventions** (snake_case for methods and variables, PascalCase for classes).
- Include comprehensive **logging** using the framework's `Logger` class.
- Apply synchronization best practices (Avoid `page.wait_for_timeout`).
- Use **Synchronous Playwright API** (`playwright.sync_api`).
- **Data-Driven & Traceability**: Scripts MUST be data-driven. Every test iteration must log its **Automation Mapping tag** (e.g., `[DDT-01]`) for clear traceability to the test case table.

## Environment-Aware Code Generation

### For UAT Environments
**Timeout Configuration:**
```python
TIMEOUT_UAT = 15000  # 15 seconds for UAT
TIMEOUT_DEV = 3000   # 3 seconds for dev
```

**Synchronization Pattern:**
```python
# Before critical interactions
page.wait_for_load_state('networkidle', timeout=15000)

# Before element interactions
element.wait_for(state='attached', timeout=5000)
element.wait_for(state='visible', timeout=5000)
element.wait_for(state='enabled', timeout=5000)
```

## Code Structure

### Test File Template
```python
import pytest
import os
from playwright.sync_api import Page, expect
from pages.aditya_birla_login_page import AdityaBirlaLoginPage
from utils.logger import Logger

def test_scenario_name(page: Page):
    logger = Logger('TestScenario')
    login_page = AdityaBirlaLoginPage(page)
    
    logger.info('Phase 1: Authentication')
    login_page.load()
    login_page.enter_credentials(os.getenv("ADITYA_BIRLA_USER"), os.getenv("ADITYA_BIRLA_PASS"))
    
    logger.info('Phase 2: Validation')
    expect(page.locator('.dashboard')).to_be_visible(timeout=15000)
```

### Page Object Template
```python
from playwright.sync_api import Page, Locator
from .base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator('#username')
        self.password_input = page.locator('#password')
        self.login_button = page.locator('button[type="submit"]')

    def enter_credentials(self, user: str, pass_val: str):
        self.wait_for_network_idle()
        self.username_input.fill(user)
        self.password_input.fill(pass_val)
        self.login_button.click()
```

## Best Practices

### ✅ DO Use These Patterns
1. **Network Idle Waits**: `page.wait_for_load_state('networkidle', timeout=15000)`
2. **Explicit Waits**: `element.wait_for(state='visible')`
3. **Flexible Selectors**: Use `page.locator('button').filter(has_text='Submit').first`
4. **Soft Logging**: Wrap optional validations in try-catch with `logger.warning()`.

### ❌ DON'T Use These Patterns
1. **Static Timeouts**: `page.wait_for_timeout(5000)` (Flaky)
2. **Single Element Assumption**: Always use `.first` or specific filters to avoid strict mode violations.
3. **Hardcoded Selectors**: Move selectors to Locators or POM classes.

---
*Last Updated: May 6, 2026 - Migrated to Python/Playwright Sync Framework*
