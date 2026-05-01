# Debugging Workflow and Strategies

## Purpose
Systematic approach to debugging test failures to reduce repeated debugging cycles and prevent the same issues from recurring.

---

## 🎯 Debugging Philosophy

### Core Principles
1. **Reproduce First** - Can you consistently reproduce the issue?
2. **Isolate Next** - Narrow down to the exact failing step
3. **Analyze Then** - Understand why it's failing
4. **Fix Once** - Apply the correct fix
5. **Document Always** - Record the solution for future reference

### Goal
- Reduce debugging time by 50%
- Prevent recurring issues
- Build knowledge base
- Improve test stability

---

## 🔄 Systematic Debugging Workflow

### Phase 1: Reproduction

#### Step 1.1: Confirm Failure Consistency
```bash
# Run test 3 times to check consistency
pytest tests/smoke/test_login.py -v --count=3

# Check if it's:
# - Consistent failure (same error every time)
# - Intermittent failure (sometimes passes, sometimes fails)
# - Environment-specific (fails only in UAT)
```

**Decision Tree:**
- **Consistent failure** → Proceed to Phase 2
- **Intermittent failure** → Check synchronization, network, loading states
- **Environment-specific** → Check environment configuration, data, network

#### Step 1.2: Enable Debugging Mode
```python
# conftest.py - Add debugging fixtures
@pytest.fixture
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": None,  # Full screen
        "record_video": "retain-on-failure",  # Keep video on failure
    }

@pytest.fixture
def launch_arguments(launch_arguments):
    return {
        **launch_arguments,
        "headless": False,  # Headed mode for debugging
        "slow_mo": 100,  # Slow down actions
        "args": ["--start-maximized"],  # Full screen
    }
```

**Why:** See what's happening in real-time, capture evidence

#### Step 1.3: Capture Evidence
```python
# Add to test or conftest.py
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            # Screenshot
            page.screenshot(path=f"screenshots/{item.name}_failure.png")
            
            # HTML snapshot
            with open(f"screenshots/{item.name}_failure.html", "w") as f:
                f.write(page.content())
            
            # Console logs
            console_logs = []
            page.on("console", lambda msg: console_logs.append(msg.text))
            with open(f"screenshots/{item.name}_console.txt", "w") as f:
                f.write("\n".join(console_logs))
```

**Why:** Evidence helps understand failure context

---

### Phase 2: Isolation

#### Step 2.1: Binary Search Test Steps
```python
# Original test
def test_login_flow(self, page):
    # Step 1
    page.goto(url)
    # Step 2
    username.fill("user")
    # Step 3
    password.fill("pass")
    # Step 4
    login_button.click()
    # Step 5
    assert dashboard.is_visible()

# Comment out half the steps
def test_login_flow(self, page):
    # Step 1
    page.goto(url)
    # Step 2
    username.fill("user")
    # Comment out rest
    # password.fill("pass")
    # login_button.click()
    # assert dashboard.is_visible()
```

**If passes:** Failure is in commented out section  
**If fails:** Failure is in active section

#### Step 2.2: Run Individual Methods
```bash
# Run specific test method
pytest tests/smoke/test_login.py::TestLogin::test_login_flow -v

# Run with verbose output
pytest tests/smoke/test_login.py::TestLogin::test_login_flow -vv -s

# Run with traceback
pytest tests/smoke/test_login.py::TestLogin::test_login_flow --tb=long
```

**Why:** Narrow down to exact failing line

#### Step 2.3: Check Page State at Failure
```python
# Add before failing step
logger.info(f"Current URL: {page.url}")
logger.info(f"Page title: {page.title()}")
logger.info(f"Element visible: {element.is_visible()}")
logger.info(f"Element count: {page.locator(selector).count()}")
logger.info(f"Element text: {element.text_content()}")
logger.info(f"Element enabled: {element.is_enabled()}")
```

**Why:** Understand page state when failure occurs

---

### Phase 3: Analysis

#### Step 3.1: Analyze Error Message
```python
# Common error patterns and their meanings

# TimeoutError: Timeout 15000ms exceeded
# Meaning: Element not found within timeout
# Causes: Wrong selector, element not loaded, slow network
# Fix: Check selector, add wait, increase timeout

# StrictModeViolation: strict mode violation
# Meaning: Selector matches multiple elements
# Causes: Generic selector, duplicate elements
# Fix: Use .first, more specific selector

# ElementNotInteractableError: Element is not visible
# Meaning: Element exists but not interactable
# Causes: Hidden element, overlay blocking, disabled
# Fix: Wait for visible, check overlay, check enabled

# TargetClosedError: Target page, context or browser has been closed
# Meaning: Page was closed
# Causes: Navigation without wait, page crash
# Fix: Add network idle wait, check page state
```

#### Step 3.2: Check Element in DOM
```python
# Use browser DevTools or Playwright Inspector
# Check if element exists
element_count = page.locator(selector).count()
logger.info(f"Element count: {element_count}")

# Check element attributes
element = page.locator(selector).first
logger.info(f"Element classes: {element.get_attribute('class')}")
logger.info(f"Element id: {element.get_attribute('id')}")
logger.info(f"Element aria-label: {element.get_attribute('aria-label')}")
```

#### Step 3.3: Check Network Activity
```python
# Monitor network requests
requests = []
page.on("request", lambda request: requests.append(request.url))
page.on("response", lambda response: print(f"Response: {response.url} - {response.status}"))

# After action
logger.info(f"Requests made: {len(requests)}")
for req in requests:
    logger.info(f"  {req}")
```

**Why:** Check if API calls completed, network errors

#### Step 3.4: Check Console Errors
```python
# Capture console errors
errors = []
page.on("console", lambda msg: 
    errors.append(msg.text) if msg.type == "error" else None
)

# After test
if errors:
    logger.error(f"Console errors: {errors}")
```

**Why:** JavaScript errors can cause test failures

---

### Phase 4: Fix Application

#### Step 4.1: Apply Appropriate Fix

**Fix 1: Add Missing Wait**
```python
# Before
element.click()

# After
page.wait_for_load_state("networkidle", timeout=15000)
element.wait_for(state="visible", timeout=5000)
element.click()
```

**Fix 2: Fix Selector**
```python
# Before - Wrong selector
element = page.locator("#wrong-id")

# After - Correct selector with fallbacks
element_selectors = [
    "#correct-id",
    "[data-testid='submit']",
    ".submit-button"
]
for selector in element_selectors:
    try:
        element = page.locator(selector).first
        if element.is_visible(timeout=3000):
            break
    except:
        continue
```

**Fix 3: Increase Timeout**
```python
# Before - Too short
element.wait_for(state="visible", timeout=3000)

# After - Appropriate for UAT
element.wait_for(state="visible", timeout=15000)
```

**Fix 4: Add Loading Overlay Wait**
```python
# Before
element.click()

# After
_wait_for_loading_overlay_to_disappear(page)
element.click()
```

**Fix 5: Handle Strict Mode**
```python
# Before
element = page.get_by_text("Submit")

# After
element = page.get_by_text("Submit").first
```

#### Step 4.2: Verify Fix
```bash
# Run test 5 times to ensure stability
pytest tests/smoke/test_login.py -v --count=5

# Run in different environments
pytest tests/smoke/test_login.py --env=uat
pytest tests/smoke/test_login.py --env=dev

# Run with different browsers
pytest tests/smoke/test_login.py --browser=chromium
pytest tests/smoke/test_login.py --browser=firefox
```

**Why:** Ensure fix is robust and not flaky

---

### Phase 5: Documentation

#### Step 5.1: Document the Issue
```markdown
## Issue: Login Button Timeout

### Symptoms
- Test fails with TimeoutError
- Occurs consistently in UAT
- Passes in dev environment

### Root Cause
- UAT environment slower than dev
- 3-second timeout insufficient
- Network requests not completed

### Fix Applied
- Increased timeout from 3000ms to 15000ms
- Added network idle wait before click
- Added loading overlay detection

### Code Changes
```python
# Before
element.click()

# After
page.wait_for_load_state("networkidle", timeout=15000)
_wait_for_loading_overlay_to_disappear(page)
element.click()
```

### Verification
- Test passes 5 consecutive runs
- Works in UAT and dev
- No regression in other tests
```

#### Step 5.2: Update Knowledge Base
```markdown
# Add to skills_database.md

### Skill: UAT Timeout Adjustment
**Learned From:** Login button timeout in UAT
**Pattern:** Use 15-second timeouts for UAT environments
**When to Apply:** All waits in UAT environment
**Key Insight:** UAT has slower API responses than dev
```

#### Step 5.3: Update Best Practices
```markdown
# Add to best_practices.md

### Environment-Specific Timeouts
- UAT: 15 seconds
- Dev: 3-5 seconds
- Production: 20 seconds
```

---

## 🛠️ Common Debugging Scenarios

### Scenario 1: Element Not Found

**Symptoms:**
```
TimeoutError: Timeout 15000ms exceeded
waiting for locator(".submit-button")
```

**Debugging Steps:**
1. Check if element exists in DOM
2. Check selector is correct
3. Check if element is in iframe
4. Check if element is dynamic (changes ID/class)
5. Check if element is behind overlay

**Fixes:**
```python
# Fix 1: Check element exists
if page.locator(selector).count() == 0:
    logger.error("Element not in DOM")

# Fix 2: Use fallback selectors
for sel in selectors:
    if page.locator(sel).count() > 0:
        selector = sel
        break

# Fix 3: Wait for element
page.wait_for_selector(selector, timeout=15000)

# Fix 4: Handle iframe
frame = page.frame("iframe-name")
frame.locator(selector).click()
```

---

### Scenario 2: Element Not Interactable

**Symptoms:**
```
ElementNotInteractableError: Element is not visible
```

**Debugging Steps:**
1. Check if element is visible
2. Check if element is enabled
3. Check if element is behind overlay
4. Check if element is scrolled out of view
5. Check if element is covered by another element

**Fixes:**
```python
# Fix 1: Wait for visible
element.wait_for(state="visible", timeout=15000)

# Fix 2: Wait for enabled
element.wait_for(state="enabled", timeout=5000)

# Fix 3: Scroll into view
element.scroll_into_view_if_needed()

# Fix 4: Wait for overlay
_wait_for_loading_overlay_to_disappear(page)

# Fix 5: Force click (last resort)
element.click(force=True)
```

---

### Scenario 3: Strict Mode Violation

**Symptoms:**
```
StrictModeViolation: strict mode violation
locator("text=Submit") resolved to 2 elements
```

**Debugging Steps:**
1. Check how many elements match selector
2. Identify which element should be targeted
3. Check if elements are in different contexts

**Fixes:**
```python
# Fix 1: Use .first
element = page.get_by_text("Submit").first

# Fix 2: Use more specific selector
element = page.locator("button.submit:has-text('Submit')").first

# Fix 3: Use nth
element = page.get_by_text("Submit").nth(0)

# Fix 4: Use filter
element = page.get_by_text("Submit").filter(has=page.locator(".primary"))
```

---

### Scenario 4: Intermittent Failures

**Symptoms:**
- Test sometimes passes, sometimes fails
- No consistent error message
- Random failures

**Debugging Steps:**
1. Check for race conditions
2. Check for timing issues
3. Check for network variability
4. Check for external dependencies
5. Check for shared state between tests

**Fixes:**
```python
# Fix 1: Add network idle wait
page.wait_for_load_state("networkidle", timeout=15000)

# Fix 2: Add retry logic
for attempt in range(3):
    try:
        element.click()
        break
    except:
        if attempt == 2:
            raise
        page.wait_for_timeout(1000)

# Fix 3: Clean up test data
@pytest.fixture(autouse=True)
def cleanup():
    yield
    # Clean up test data

# Fix 4: Use test isolation
@pytest.fixture
def fresh_page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
```

---

### Scenario 5: Page Navigation Issues

**Symptoms:**
```
TimeoutError: Timeout 60000ms exceeded
waiting for page.goto()
```

**Debugging Steps:**
1. Check if URL is correct
2. Check if network is accessible
3. Check if server is running
4. Check for authentication redirects
5. Check for SSL certificate issues

**Fixes:**
```python
# Fix 1: Verify URL
assert url.startswith("https://")

# Fix 2: Wait for navigation
page.goto(url, wait_until="networkidle", timeout=60000)

# Fix 3: Handle authentication
page.goto(url)
# Handle login if redirected

# Fix 4: Ignore SSL errors (UAT only)
context = browser.new_context(ignore_https_errors=True)
```

---

## 📊 Debugging Metrics

### Track These Metrics
- **Time to Reproduce:** How long to confirm failure
- **Time to Isolate:** How long to find failing step
- **Time to Fix:** How long to apply fix
- **Time to Verify:** How long to confirm fix works
- **Recurrence Rate:** How often same issue occurs

### Goal Metrics
- **Average Debug Time:** < 15 minutes
- **Recurrence Rate:** < 5%
- **First-Time Fix Rate:** > 80%

---

## 🎯 Debugging Checklist

### Before Debugging
- [ ] Can I reproduce the issue consistently?
- [ ] Do I have screenshots/videos of failure?
- [ ] Do I have console logs?
- [ ] Do I have network logs?

### During Debugging
- [ ] Have I isolated the failing step?
- [ ] Have I checked element in DOM?
- [ ] Have I checked network activity?
- [ ] Have I checked console errors?

### After Fixing
- [ ] Have I verified fix works?
- [ ] Have I run test multiple times?
- [ ] Have I tested in different environments?
- [ ] Have I documented the issue?
- [ ] Have I updated knowledge base?

---

## 🚀 Quick Debugging Commands

```bash
# Run single test with debug mode
pytest tests/smoke/test_login.py::TestLogin::test_login -v -s --headed

# Run with Playwright Inspector
PWDEBUG=1 pytest tests/smoke/test_login.py

# Run with screenshots
pytest tests/smoke/test_login.py -v --screenshot=only-on-failure

# Run with video
pytest tests/smoke/test_login.py -v --video=retain-on-failure

# Run with traceback
pytest tests/smoke/test_login.py -v --tb=long

# Run with last failed
pytest --lf

# Run with verbose output
pytest tests/smoke/test_login.py -vv
```

---

## 📚 Learning from Debugging

### After Each Debugging Session
1. **What was the root cause?**
2. **What was the fix?**
3. **Could this have been prevented?**
4. **What can be automated?**
5. **What should be documented?**

### Prevention Strategies
1. **Add pre-flight checks** - Verify environment before test
2. **Add assertions early** - Fail fast on issues
3. **Add retry logic** - Handle intermittent issues
4. **Add monitoring** - Track test health
5. **Add documentation** - Share learnings

---

*Last Updated: May 1, 2026*
