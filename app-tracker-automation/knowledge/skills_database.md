# Skills Database - AI Learning System

## Purpose
This database captures learnings from each project execution to improve future analysis and test generation capabilities.

## Project: Aditya Birla App Tracker Automation
**Date Range:** April 28 - May 1, 2026
**Technology Stack:** Playwright + Python + Pytest
**Domain:** Insurance Portal Testing

---

## Learned Skills & Patterns

### 1. Playwright Synchronization Best Practices

#### Skill: Network Idle Waits
**Learned From:** Aditya Birla project - premature element interactions causing failures
**Pattern:**
```python
# Always wait for network to settle before critical interactions
page.wait_for_load_state("networkidle", timeout=15000)
```
**When to Apply:**
- After page load
- After credential entry
- Before menu navigation
- After link clicks
- Before component validation
- After search input
- After dropdown clicks

**Key Insight:** UAT environments need more time (15s) for data loading than dev environments (3-5s)

#### Skill: Element Stability Checks
**Learned From:** Elements not fully actionable before clicks
**Pattern:**
```python
# Wait for element to be fully actionable before interaction
element.wait_for(state="attached", timeout=5000)
element.wait_for(state="visible", timeout=5000)
element.wait_for(state="enabled", timeout=5000)
```
**When to Apply:** Before any click, fill, or interaction with elements

**Key Insight:** Elements can be attached but not visible/enabled, causing flaky tests

#### Skill: Loading Overlay Detection
**Learned From:** Blocking spinners/overlays preventing element interactions
**Pattern:**
```python
def _wait_for_loading_overlay_to_disappear(self, page, timeout=5000):
    """Wait for loading spinners, progress bars, or blocking overlays to disappear"""
    loading_selectors = [
        ".loading-overlay",
        ".spinner",
        ".progress-bar",
        "[class*='loading']",
        "[class*='spinner']",
        "[class*='overlay']",
        ".MuiCircularProgress-root",
        ".MuiBackdrop-root"
    ]
    
    for selector in loading_selectors:
        try:
            loading_element = page.locator(selector).first
            if loading_element.is_visible(timeout=1000):
                loading_element.wait_for(state="hidden", timeout=timeout)
        except:
            continue
```
**When to Apply:** Before critical clicks (menu, navigation, dropdowns)

**Key Insight:** Material-UI apps use specific spinner classes (MuiCircularProgress, MuiBackdrop)

---

### 2. Component Validation Strategies

#### Skill: Multiple Selector Fallbacks
**Learned From:** Single selectors timing out, strict mode violations
**Pattern:**
```python
filter_selectors = [
    "button:has-text('Filter')",
    "[aria-label*='filter' i]",
    ".filter-button",
    "button[title*='filter' i]",
    "svg[class*='filter']"
]

for selector in filter_selectors:
    try:
        element = page.locator(selector).first
        if element.is_visible(timeout=3000):
            # Use this element
            break
    except:
        continue
```
**When to Apply:** Elements that might not exist on all pages or have varying implementations

**Key Insight:** UI variations require flexible selector strategies

#### Skill: Strict Mode Violation Handling
**Learned From:** `get_by_text("Policy List")` resolved to 2 elements
**Pattern:**
```python
# Use .first to handle multiple matching elements
element = page.get_by_text("Policy List").first
```
**When to Apply:** When text or selectors might match multiple elements

**Key Insight:** Always use `.first` when multiple elements could match

#### Skill: Non-Blocking Validation
**Learned From:** Optional components causing test failures
**Pattern:**
```python
try:
    # Validate optional component
    if element:
        logger.info("[PASS] Component found")
    else:
        logger.warning("[WARN] Component not found (may not exist on this page)")
except Exception as e:
    logger.warning(f"[WARN] Component validation skipped: {e}")
```
**When to Apply:** Optional UI components that shouldn't fail the test

**Key Insight:** Tests should continue unless critical failure occurs

---

### 3. UAT Environment Characteristics

#### Skill: Timeout Adjustment for UAT
**Learned From:** 3-second timeouts too short for UAT data loading
**Pattern:**
```python
# Use longer timeouts for UAT environments
TIMEOUT_UAT = 15000  # 15 seconds
TIMEOUT_DEV = 3000   # 3 seconds
```
**When to Apply:** All waits in UAT environment

**Key Insight:** UAT has slower API responses and data loading than dev

#### Skill: Table Wrapper Pre-Condition Wait
**Learned From:** Individual filters failing before table loaded
**Pattern:**
```python
# Wait for main table wrapper before checking individual components
table_wrapper = page.locator(".MuiBox-root.jss138, tbody tr, table").first
table_wrapper.wait_for(state="visible", timeout=15000)
```
**When to Apply:** Before validating table-dependent components

**Key Insight:** Parent elements must be loaded before child validation

---

### 4. CSS Framework Patterns

#### Skill: Material-UI Selector Patterns
**Learned From:** Aditya Birla uses Material-UI framework
**Patterns:**
```python
# Button patterns
"button.MuiButtonBase-root.MuiIconButton-root"
"button.MuiButton-textSizeSmall"

# Dropdown patterns
"#mui-component-select-sortList"
"ul.MuiList-root[role='listbox']"

# Spinner patterns
".MuiCircularProgress-root"
".MuiBackdrop-root"

# Box/Container patterns
".MuiBox-root.jss138"
".MuiBox-root.jss58"
```
**When to Apply:** Material-UI based applications

**Key Insight:** Material-UI uses predictable class naming conventions

#### Skill: CSS Injection for Layout Fixes
**Learned From:** Viewport scaling causing MENU button to be hidden
**Pattern:**
```python
panel_css = """
*, *::before, *::after {
    box-sizing: border-box;
}
html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow-x: hidden;
}
body {
    display: flex;
    flex-direction: column;
}
"""
page.add_init_script(panel_css)
```
**When to Apply:** Layout issues causing element visibility problems

**Key Insight:** CSS injection can fix viewport-related issues without changing app code

---

### 5. Page Object Model Best Practices

#### Skill: Synchronization in Page Objects
**Learned From:** Page objects without synchronization causing flaky tests
**Pattern:**
```python
class AdityaBirlaLoginPage:
    def enter_credentials(self, username, password):
        # Wait for network to settle
        self.page.wait_for_load_state("networkidle", timeout=10000)
        
        # Wait for elements to be actionable
        self.username_input.wait_for(state="attached", timeout=5000)
        self.username_input.wait_for(state="visible", timeout=5000)
        self.username_input.wait_for(state="enabled", timeout=5000)
        
        # Wait for loading overlays
        self._wait_for_loading_overlay_to_disappear()
        
        # Perform action
        self.username_input.fill(username)
        
        # Wait for network to settle after action
        self.page.wait_for_load_state("networkidle", timeout=5000)
```
**When to Apply:** All page object methods that interact with elements

**Key Insight:** Page objects should handle synchronization, not test scripts

---

### 6. Component Reusability Patterns

#### Skill: Base Component with Synchronization
**Learned From:** Repeating synchronization code across components
**Pattern:**
```python
class BaseComponent:
    def __init__(self, page, locator):
        self.page = page
        self.element = page.locator(locator)
        self.logger = Logger()
    
    def _wait_for_loading_overlay_to_disappear(self, timeout=5000):
        # Reusable loading overlay detection
        pass
    
    def _wait_for_element_actionable(self, timeout=5000):
        # Reusable element stability check
        self.element.wait_for(state="attached", timeout=timeout)
        self.element.wait_for(state="visible", timeout=timeout)
        self.element.wait_for(state="enabled", timeout=timeout)
```
**When to Apply:** Creating reusable component classes

**Key Insight:** Base components should provide common synchronization methods

---

### 7. Error Handling Strategies

#### Skill: Soft Logging vs Hard Failures
**Learned From:** Tests failing on minor issues preventing execution
**Pattern:**
```python
# Soft logging for non-critical issues
try:
    # Validation
    logger.info("[PASS] Component validated")
except Exception as e:
    logger.warning(f"[WARN] Component validation skipped: {e}")
    errors += 1

# Hard failure for critical issues
try:
    # Critical operation
    if not critical_condition:
        raise Exception("Critical failure")
except Exception as e:
    logger.error(f"[FAIL] Critical error: {e}")
    raise
```
**When to Apply:** Distinguish between optional and critical validations

**Key Insight:** Not all failures should stop test execution

---

### 8. Environment Configuration

#### Skill: Multi-Path .env Loading
**Learned From:** .env file not found in different execution contexts
**Pattern:**
```python
env_paths = [
    "app-tracker-automation/.env",
    ".env",
    os.path.join(os.path.dirname(__file__), "..", "..", ".env"),
]

env_loaded = False
for env_path in env_paths:
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)
        env_loaded = True
        break
```
**When to Apply:** Loading environment variables in test scripts

**Key Insight:** Multiple fallback paths improve robustness across execution contexts

---

### 9. Browser Configuration

#### Skill: Full Screen Mode for Visibility
**Learned From:** Elements hidden due to viewport constraints
**Pattern:**
```python
# .env configuration
BROWSER_VIEWPORT = None  # Let browser use full screen
BROWSER_LAUNCH_ARGS = ['--start-maximized']  # Full screen mode
```
**When to Apply:** Configuring browser for element visibility

**Key Insight:** Full screen mode prevents elements from being hidden

---

### 10. Test Execution Patterns

#### Skill: Three-Phase Test Structure
**Learned From:** Clear separation of concerns in test flow
**Pattern:**
```python
# Phase 1: Authentication
# - Navigate to login page
# - Enter credentials
# - Click login button
# - Verify dashboard

# Phase 2: App Tracker Setup
# - Click menu button
# - Navigate to Application Tracker
# - Wait for page load

# Phase 3: Component Validation
# - Validate filters
# - Validate table
# - Validate interactions
```
**When to Apply:** Structuring end-to-end test flows

**Key Insight:** Clear phases improve test maintainability and debugging

---

## Future Application Guidelines

### When Analyzing New User Stories:

1. **Assess Environment Type:**
   - If UAT: Use 15-second timeouts
   - If dev: Use 3-5 second timeouts
   - If unknown: Start with 15s, optimize later

2. **Identify CSS Framework:**
   - Material-UI: Use Mui* class patterns
   - Bootstrap: Use .btn, .form-control patterns
   - Custom: Analyze HTML structure

3. **Determine Component Criticality:**
   - Critical: Use hard failures
   - Optional: Use soft logging with warnings

4. **Apply Synchronization:**
   - Always use network idle waits before critical interactions
   - Always check element stability before actions
   - Always wait for loading overlays before clicks

5. **Use Flexible Selectors:**
   - Provide multiple fallback selectors
   - Use .first for potentially multiple matches
   - Use aria-labels when available

6. **Structure Page Objects:**
   - Include synchronization in all methods
   - Provide base component with common waits
   - Handle loading overlays automatically

7. **Configure Browser:**
   - Use full screen mode for visibility
   - Ignore HTTPS errors for UAT
   - Inject CSS for layout fixes if needed

---

## Learned Anti-Patterns (What NOT to Do)

### 1. ❌ Don't Use Static Timeouts
**Anti-Pattern:** `page.wait_for_timeout(3000)`
**Why:** Unreliable, doesn't wait for actual page state
**Solution:** Use `wait_for_load_state("networkidle")` or element state waits

### 2. ❌ Don't Assume Single Element Matches
**Anti-Pattern:** `page.get_by_text("Submit")`
**Why:** Strict mode violation if multiple elements match
**Solution:** Use `.first` or more specific selectors

### 3. ❌ Don't Ignore Loading Overlays
**Anti-Pattern:** Click directly without checking for spinners
**Why:** Clicks blocked by invisible overlays
**Solution:** Wait for overlays to disappear before interaction

### 4. ❌ Don't Use Hard Failures for Optional Components
**Anti-Pattern:** `assert element.is_visible()`
**Why:** Test fails on non-critical missing components
**Solution:** Use soft logging with warnings

### 5. ❌ Don't Skip Network Idle Waits
**Anti-Pattern:** Click immediately after page load
**Why:** Background APIs still loading, causing flaky tests
**Solution:** Always wait for network idle before interactions

---

## Metrics for Success

### Quality Indicators:
- Test execution time: < 30 seconds for smoke tests
- Flakiness rate: < 5%
- False positive rate: < 10%
- Component detection rate: > 90%

### Improvement Indicators:
- Reduced timeout values (faster execution)
- Fewer selector fallbacks needed
- Less CSS injection required
- Simpler error handling needed

---

## Next Learning Opportunities

### To Learn From Future Projects:
1. Different CSS frameworks (Angular, Vue, React)
2. API testing patterns
3. Mobile automation patterns
4. Performance testing integration
5. Accessibility testing patterns
6. Cross-browser compatibility issues
7. CI/CD pipeline optimization
8. Test data management strategies

---

## Debugging Strategies (Learned from Aditya Birla Project)

### Systematic Debugging Approach
**5-Phase Debugging Workflow:**
1. **Reproduction** - Confirm failure consistency, enable debugging mode, capture evidence
2. **Isolation** - Binary search test steps, run individual methods, check page state
3. **Analysis** - Analyze error message, check element in DOM, check network activity
4. **Fix Application** - Apply appropriate fix, verify fix
5. **Documentation** - Document issue, update knowledge base, update best practices

### Common Debugging Scenarios

**Scenario 1: Element Not Found**
- Check if element exists in DOM
- Check selector is correct
- Check if element is in iframe
- Check if element is dynamic
- Fix: Use fallback selectors, wait for element, handle iframe

**Scenario 2: Element Not Interactable**
- Check if element is visible
- Check if element is enabled
- Check if element is behind overlay
- Check if element is scrolled out of view
- Fix: Wait for visible/enabled, scroll into view, wait for overlay

**Scenario 3: Strict Mode Violation**
- Check how many elements match selector
- Identify which element should be targeted
- Fix: Use .first, more specific selector, nth, filter

**Scenario 4: Intermittent Failures**
- Check for race conditions
- Check for timing issues
- Check for network variability
- Fix: Add network idle wait, add retry logic, clean up test data

**Scenario 5: Page Navigation Issues**
- Check if URL is correct
- Check if network is accessible
- Check if server is running
- Fix: Verify URL, wait for navigation, handle authentication, ignore SSL errors

### Debugging Metrics
- **Time to Reproduce:** How long to confirm failure
- **Time to Isolate:** How long to find failing step
- **Time to Fix:** How long to apply fix
- **Time to Verify:** How long to confirm fix works
- **Recurrence Rate:** How often same issue occurs

**Goal Metrics:**
- Average Debug Time: < 15 minutes
- Recurrence Rate: < 5%
- First-Time Fix Rate: > 80%

---

## Pre-Flight Best Practices (Learned from Aditya Birla Project)

### Daily Pre-Flight Checklist
**Environment Check:**
- Application is running and accessible
- Test data is available and valid
- Network is stable
- Services are up

**Test-Specific Pre-Flight:**
- Understand user story completely
- Analyze application (CSS framework, JS framework)
- Classify components (critical, important, optional)
- Plan test structure

**Technical Pre-Flight:**
- Python dependencies installed
- Playwright browsers installed
- Environment variables loaded
- Code quality checks passed

### Common Pre-Flight Issues and Fixes
**Issue 1: Application Not Running**
- Check: `curl -I https://uat.example.com`
- Fix: Start server, check firewall, verify URL, check VPN

**Issue 2: Credentials Invalid**
- Check: Verify .env file
- Fix: Update credentials, check account active, verify password

**Issue 3: Dependencies Missing**
- Check: `pip list | grep playwright`
- Fix: `pip install -r requirements.txt`, `playwright install`

**Issue 4: Browser Not Installed**
- Check: `playwright install --dry-run`
- Fix: `playwright install chromium firefox webkit`

**Issue 5: Timeouts Too Short**
- Check: Verify .env timeout values
- Fix: Increase timeout for UAT (15s), use network idle waits

**Issue 6: Selectors Wrong**
- Check: Use Playwright Inspector
- Fix: Verify selector, use fallback selectors, use stable selectors

### Pre-Flight Metrics
- **Pre-Flight Time:** < 5 minutes
- **Issues Found Rate:** > 20% (catching issues is good)
- **Test Success Rate:** > 95% after pre-flight
- **Debugging Time Reduction:** > 50%

---

*Last Updated: May 1, 2026*
*Project: Aditya Birla App Tracker Automation*
