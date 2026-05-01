# Testing Automation Best Practices Guide

## Purpose
Prevent repeated debugging by following proven best practices from the start. This guide covers pre-flight checks, development practices, and common pitfalls to avoid.

---

## 🚀 Pre-Flight Checklist (Before Writing Tests)

### 1. Environment Assessment
- [ ] **Identify Environment Type**
  - UAT: Use 15-second timeouts
  - Dev: Use 3-5 second timeouts
  - Production: Use 20-second timeouts
  - Network conditions: Check latency, bandwidth

- [ ] **Verify Test Data Availability**
  - Valid credentials exist
  - Test data sets are available
  - Configuration values are set
  - Database is accessible

- [ ] **Check Application State**
  - Application is running
  - No maintenance windows scheduled
  - Required services are up
  - API endpoints are accessible

### 2. Framework Detection
- [ ] **Identify CSS Framework**
  - Material-UI: Look for `Mui*` classes
  - Bootstrap: Look for `.btn`, `.form-control`
  - Tailwind: Look for utility classes
  - Custom: Analyze HTML structure

- [ ] **Document Framework Patterns**
  - Button class patterns
  - Form input patterns
  - Modal/dialog patterns
  - Loading spinner patterns

- [ ] **Check JavaScript Framework**
  - React: Look for `data-reactroot`
  - Angular: Look for `ng-app`
  - Vue: Look for `data-v-*`
  - jQuery: Look for `$` usage

### 3. Component Analysis
- [ ] **Classify Component Criticality**
  - Critical: Login, data submission, payments
  - Important: Navigation, search, filters
  - Optional: Decorations, tooltips, help text

- [ ] **Identify Dynamic Elements**
  - Elements that load asynchronously
  - Elements with changing IDs
  - Elements with random classes
  - Elements that appear/disappear

- [ ] **Map User Flow**
  - Start point (login/home)
  - Navigation steps
  - Critical actions
  - End point (logout/exit)

### 4. Tool Configuration
- [ ] **Configure Browser Settings**
  - Headless vs headed mode
  - Viewport size (full screen recommended)
  - Ignore HTTPS errors for UAT
  - Disable animations if needed

- [ ] **Set Up Logging**
  - Enable detailed logging
  - Configure log levels
  - Set up log file paths
  - Enable screenshots on failure

- [ ] **Configure Timeouts**
  - Default timeout: 30000ms
  - Navigation timeout: 60000ms
  - Action timeout: 15000ms
  - Environment-specific adjustments

---

## ✅ Development Best Practices

### 1. Test Structure

#### Use Three-Phase Structure
```python
def test_scenario(self, page, config):
    # Phase 1: Setup/Authentication
    self._authenticate(page, config)
    
    # Phase 2: Execution/Navigation
    self._navigate_to_target(page)
    
    # Phase 3: Validation/Teardown
    self._validate_results(page)
```

**Why:** Clear separation improves debugging and maintenance

#### Use Descriptive Test Names
```python
# BAD
def test_1(self):
    pass

# GOOD
def test_user_can_login_with_valid_credentials(self):
    pass
```

**Why:** Self-documenting tests, easier to identify failures

### 2. Synchronization

#### Always Use Network Idle Waits
```python
# Before critical interactions
page.wait_for_load_state("networkidle", timeout=15000)
```

**When to Use:**
- After page load
- After form submission
- After navigation
- Before validation

**Why:** Prevents flaky tests from premature interactions

#### Check Element Stability
```python
# Before element interactions
element.wait_for(state="attached", timeout=5000)
element.wait_for(state="visible", timeout=5000)
element.wait_for(state="enabled", timeout=5000)
```

**Why:** Elements can be in DOM but not ready for interaction

#### Wait for Loading Overlays
```python
def _wait_for_loading_overlay_to_disappear(self, page):
    loading_selectors = [
        ".loading-overlay",
        ".spinner",
        ".progress-bar",
        "[class*='loading']",
        ".class*='spinner']",
        ".MuiCircularProgress-root",  # Material-UI
        ".MuiBackdrop-root"  # Material-UI
    ]
    
    for selector in loading_selectors:
        try:
            loading = page.locator(selector).first
            if loading.is_visible(timeout=1000):
                loading.wait_for(state="hidden", timeout=5000)
        except:
            continue
```

**Why:** Overlays block interactions and cause failures

### 3. Selector Strategy

#### Use Multiple Fallback Selectors
```python
element_selectors = [
    "button:has-text('Submit')",
    "[aria-label*='submit' i]",
    ".submit-button",
    "button[type='submit']",
    "input[type='submit']"
]

for selector in element_selectors:
    try:
        element = page.locator(selector).first
        if element.is_visible(timeout=3000):
            break
    except:
        continue
```

**Why:** UI changes break single selectors, fallbacks improve reliability

#### Use Stable Selectors
```python
# BAD - Dynamic ID
element = page.locator("#btn-12345")

# GOOD - Stable class
element = page.locator(".submit-button")

# GOOD - ARIA label
element = page.locator("[aria-label='Submit form']")

# GOOD - Data attribute
element = page.locator("[data-testid='submit-button']")
```

**Why:** Dynamic IDs change on each render, stable selectors don't

#### Handle Strict Mode Violations
```python
# BAD - Multiple elements match
element = page.get_by_text("Submit")

# GOOD - Use .first
element = page.get_by_text("Submit").first

# GOOD - Use more specific selector
element = page.locator("button.submit:has-text('Submit')").first
```

**Why:** Playwright strict mode requires single element matches

### 4. Error Handling

#### Classify Component Criticality
```python
# Critical components - Hard failure
try:
    login_button = page.locator("#login-btn").first
    login_button.wait_for(state="visible", timeout=15000)
    logger.info("[PASS] Login button found")
except Exception as e:
    logger.error(f"[FAIL] Critical component missing: {e}")
    raise  # Stop test

# Optional components - Soft warning
try:
    optional_filter = page.locator(".filter-button").first
    if optional_filter.is_visible(timeout=3000):
        logger.info("[PASS] Optional filter found")
    else:
        logger.warning("[WARN] Optional filter not found")
except Exception as e:
    logger.warning(f"[WARN] Optional validation skipped: {e}")
    # Continue test
```

**Why:** Not all failures should stop test execution

#### Use Meaningful Error Messages
```python
# BAD
assert element.is_visible()

# GOOD
if not element.is_visible(timeout=15000):
    raise AssertionError(
        f"Login button not visible after 15s. "
        f"Expected: #login-btn, "
        f"Actual: Element not found in DOM"
    )
```

**Why:** Clear error messages speed up debugging

### 5. Page Object Model

#### Create Base Page with Common Methods
```python
class BasePage:
    def __init__(self, page):
        self.page = page
        self.logger = Logger()
    
    def wait_for_network_idle(self, timeout=15000):
        self.page.wait_for_load_state("networkidle", timeout=timeout)
    
    def wait_for_element_actionable(self, element, timeout=5000):
        element.wait_for(state="attached", timeout=timeout)
        element.wait_for(state="visible", timeout=timeout)
        element.wait_for(state="enabled", timeout=timeout)
    
    def wait_for_loading_overlay_to_disappear(self, timeout=5000):
        # Implementation
        pass
```

**Why:** Reusable methods reduce code duplication and ensure consistency

#### Keep Page Methods Focused
```python
# BAD - Multiple responsibilities
def login_and_navigate(self, username, password):
    self.enter_credentials(username, password)
    self.click_login()
    self.navigate_to_dashboard()
    self.validate_dashboard()

# GOOD - Single responsibility
def enter_credentials(self, username, password):
    # Only enter credentials
    pass

def click_login_button(self):
    # Only click login
    pass
```

**Why:** Focused methods are easier to test and debug

### 6. Test Data Management

#### Use Environment Variables
```python
# .env file
ADITYA_BIRLA_USER=test_user@example.com
ADITYA_BIRLA_PASS=secure_password
BASE_URL=https://uat.example.com

# Test script
import os
from dotenv import load_dotenv

load_dotenv()
username = os.getenv("ADITYA_BIRLA_USER")
password = os.getenv("ADITYA_BIRLA_PASS")
```

**Why:** Credentials not hardcoded, easy to change environments

#### Use Test Data Factories
```python
class TestDataFactory:
    @staticmethod
    def valid_user():
        return {
            "username": "test@example.com",
            "password": "SecurePass123",
            "role": "user"
        }
    
    @staticmethod
    def invalid_user():
        return {
            "username": "invalid@example.com",
            "password": "WrongPass123",
            "role": "user"
        }
```

**Why:** Consistent test data, easy to maintain

### 7. Assertions

#### Use Specific Assertions
```python
# BAD - Generic
assert element.is_visible()

# GOOD - Specific
assert element.is_visible(), "Submit button should be visible"
assert element.text_content() == "Submit", "Button text should be 'Submit'"
assert element.is_enabled(), "Submit button should be enabled"
```

**Why:** Specific assertions provide clear failure reasons

#### Group Related Assertions
```python
# BAD - Scattered
assert title.is_visible()
assert title.text() == "Dashboard"
assert subtitle.is_visible()
assert subtitle.text() == "Welcome"

# GOOD - Grouped
def validate_dashboard_header(self):
    """Validate all dashboard header elements"""
    title = self.page.locator("h1.dashboard-title").first
    assert title.is_visible(), "Dashboard title should be visible"
    assert title.text_content() == "Dashboard", "Title should be 'Dashboard'"
    
    subtitle = self.page.locator("p.dashboard-subtitle").first
    assert subtitle.is_visible(), "Dashboard subtitle should be visible"
    assert subtitle.text_content() == "Welcome", "Subtitle should be 'Welcome'"
```

**Why:** Grouped assertions are easier to understand and maintain

---

## 🚫 Common Pitfalls and Prevention

### 1. Static Timeouts

**Pitfall:** Using `page.wait_for_timeout(3000)`  
**Problem:** Doesn't wait for actual page state  
**Prevention:** Use `wait_for_load_state("networkidle")` or element state waits

```python
# BAD
page.wait_for_timeout(3000)
element.click()

# GOOD
page.wait_for_load_state("networkidle", timeout=15000)
element.wait_for(state="visible", timeout=5000)
element.click()
```

### 2. Hardcoded Values

**Pitfall:** Hardcoding URLs, credentials, selectors  
**Problem:** Difficult to maintain, environment-specific  
**Prevention:** Use environment variables and configuration files

```python
# BAD
page.goto("https://uat.example.com/login")
username_input.fill("test@example.com")
password_input.fill("password123")

# GOOD
base_url = os.getenv("BASE_URL")
page.goto(f"{base_url}/login")
username_input.fill(os.getenv("TEST_USERNAME"))
password_input.fill(os.getenv("TEST_PASSWORD"))
```

### 3. Assuming Single Element Matches

**Pitfall:** Using selectors that match multiple elements  
**Problem:** Strict mode violations  
**Prevention:** Use `.first` or more specific selectors

```python
# BAD
element = page.get_by_text("Submit")

# GOOD
element = page.get_by_text("Submit").first
# OR
element = page.locator("button.submit:has-text('Submit')").first
```

### 4. Ignoring Loading States

**Pitfall:** Clicking while page is loading  
**Problem:** Clicks blocked, element not found  
**Prevention:** Wait for network idle and loading overlays

```python
# BAD
page.goto(url)
element.click()

# GOOD
page.goto(url)
page.wait_for_load_state("networkidle", timeout=15000)
_wait_for_loading_overlay_to_disappear(page)
element.click()
```

### 5. Brittle Selectors

**Pitfall:** Using dynamic IDs or fragile CSS classes  
**Problem:** Tests break on UI changes  
**Prevention:** Use stable selectors with fallbacks

```python
# BAD - Dynamic ID
element = page.locator("#btn-12345")

# GOOD - Stable class with fallbacks
element_selectors = [
    ".submit-button",
    "[data-testid='submit']",
    "button[type='submit']"
]
```

### 6. No Error Context

**Pitfall:** Generic error messages  
**Problem:** Difficult to debug failures  
**Prevention:** Provide detailed error context

```python
# BAD
assert element.is_visible()

# GOOD
if not element.is_visible(timeout=15000):
    raise AssertionError(
        f"Element not visible after 15s. "
        f"Selector: {selector}, "
        f"Page URL: {page.url}, "
        f"Expected: Element visible, "
        f"Actual: Element not found"
    )
```

### 7. Testing Implementation Details

**Pitfall:** Testing internal implementation rather than user behavior  
**Problem:** Tests break on refactoring  
**Prevention:** Test user-facing behavior

```python
# BAD - Testing implementation
assert page.locator("div.internal-class").count() == 5

# GOOD - Testing behavior
assert page.locator("table tbody tr").count() == 5
```

### 8. Skipping Cleanup

**Pitfall:** Not cleaning up test data  
**Problem:** Tests interfere with each other  
**Prevention:** Always clean up in teardown

```python
# BAD
def test_create_user(self):
    user = create_user()
    # No cleanup

# GOOD
def test_create_user(self):
    user = create_user()
    try:
        # Test logic
        pass
    finally:
        delete_user(user.id)
```

---

## 🔍 Debugging Strategies

### 1. Systematic Debugging Approach

#### Step 1: Reproduce the Issue
- Run test in headed mode to see what's happening
- Enable screenshots on failure
- Enable video recording
- Check browser console for errors

#### Step 2: Isolate the Problem
- Comment out test steps to find failing step
- Run individual test methods
- Check if issue is environment-specific
- Verify test data is correct

#### Step 3: Analyze the Failure
- Check error message for clues
- Review screenshots/videos
- Check page URL at failure
- Verify element exists in DOM

#### Step 4: Apply Fix
- Add missing wait
- Fix selector
- Update timeout
- Add error handling

#### Step 5: Verify Fix
- Run test multiple times
- Run in different environments
- Check for regression
- Update documentation

### 2. Common Debugging Techniques

#### Enable Headed Mode
```python
# conftest.py
@pytest.fixture
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": None,  # Full screen
    }

@pytest.fixture
def launch_arguments(launch_arguments):
    return {
        **launch_arguments,
        "headless": False,  # Headed mode for debugging
        "slow_mo": 100,  # Slow down actions
    }
```

#### Add Debug Logging
```python
logger.info(f"Current URL: {page.url}")
logger.info(f"Element visible: {element.is_visible()}")
logger.info(f"Element count: {page.locator(selector).count()}")
logger.info(f"Element text: {element.text_content()}")
```

#### Take Screenshots
```python
# On failure
page.screenshot(path="screenshots/failure.png")

# At specific points
page.screenshot(path="screenshots/step1.png")
```

#### Use Playwright Inspector
```bash
# Open Playwright Inspector
playwright codegen https://example.com

# Generate selectors interactively
# Test selectors in real-time
```

#### Check Network Activity
```python
# Log network requests
page.on("request", lambda request: print(f"Request: {request.url}"))
page.on("response", lambda response: print(f"Response: {response.url}"))
```

### 3. Debugging Checklist

- [ ] Test fails consistently or intermittently?
- [ ] Failure in specific environment or all environments?
- [ ] Element exists in DOM at failure?
- [ ] Element visible at failure?
- [ ] Element enabled at failure?
- [ ] Loading overlays present at failure?
- [ ] Network requests completed at failure?
- [ ] Console errors present?
- [ ] Selector matches multiple elements?
- [ ] Timeout value appropriate?

---

## 📋 Quick Reference

### Timeout Guidelines
| Environment | Network Idle | Element Wait | Action Timeout |
|-------------|--------------|--------------|----------------|
| Dev         | 3000ms       | 2000ms       | 5000ms         |
| UAT         | 15000ms      | 5000ms       | 10000ms        |
| Production  | 20000ms      | 5000ms       | 15000ms        |

### Selector Priority
1. **data-testid** (Most stable)
2. **ARIA labels** (Accessible, stable)
3. **CSS classes** (Framework-specific)
4. **Text content** (User-facing)
5. **HTML attributes** (type, name, id)

### Synchronization Order
1. Wait for network idle
2. Wait for loading overlays
3. Wait for element attached
4. Wait for element visible
5. Wait for element enabled
6. Perform action

---

## 🎯 Success Metrics

### Test Quality Indicators
- **Flakiness Rate:** < 5%
- **False Positive Rate:** < 10%
- **Execution Time:** < 30s for smoke tests
- **Maintenance Effort:** < 2 hours per week

### Code Quality Indicators
- **Code Duplication:** < 10%
- **Test Coverage:** > 80%
- **Page Object Usage:** 100%
- **Selector Stability:** > 90%

---

## 📚 Continuous Learning

### After Each Test Execution
1. Document what worked well
2. Document what failed
3. Identify patterns
4. Update best practices guide
5. Share with team

### Before Each New Project
1. Review best practices guide
2. Review skills database
3. Assess environment
4. Detect frameworks
5. Plan strategy

---

*Last Updated: May 1, 2026*
