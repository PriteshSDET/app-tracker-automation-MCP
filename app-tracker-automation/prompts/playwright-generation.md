# Playwright Code Generation Prompt

## Purpose
Generate robust Playwright test code from test cases using learned synchronization patterns from previous projects.

## Framework Standards
- Use Page Object Model pattern
- Implement component-driven architecture
- Follow Python naming conventions
- Include proper error handling
- Add comprehensive logging
- Apply synchronization best practices

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
page.wait_for_load_state("networkidle", timeout=15000)

# Before element interactions
element.wait_for(state="attached", timeout=5000)
element.wait_for(state="visible", timeout=5000)
element.wait_for(state="enabled", timeout=5000)

# Before navigation clicks
_wait_for_loading_overlay_to_disappear(page)
```

### For Dev Environments
**Faster Execution:**
```python
# Shorter timeouts for dev
page.wait_for_load_state("networkidle", timeout=3000)
element.wait_for(state="visible", timeout=2000)
```

## Code Structure

### Test File Template
```python
import pytest
from pages.login_page import LoginPage
from components.base_component import BaseComponent
from utils.logger import Logger

class TestScenario:
    def __init__(self):
        self.logger = Logger()
    
    def test_method_name(self, page, config):
        """Test description with three-phase structure"""
        
        # Phase 1: Authentication
        self._authenticate(page, config)
        
        # Phase 2: Navigation
        self._navigate_to_target(page)
        
        # Phase 3: Validation
        self._validate_components(page)
    
    def _authenticate(self, page, config):
        """Authentication phase with synchronization"""
        # Wait for network idle
        page.wait_for_load_state("networkidle", timeout=15000)
        
        # Enter credentials with element stability checks
        login_page = LoginPage(page)
        login_page.enter_credentials(
            config['username'],
            config['password']
        )
        
        # Wait for network idle after login
        page.wait_for_load_state("networkidle", timeout=15000)
    
    def _navigate_to_target(self, page):
        """Navigation phase with loading overlay detection"""
        # Wait for loading overlays
        self._wait_for_loading_overlay_to_disappear(page)
        
        # Click navigation element
        menu_button = page.locator("button[aria-label='menu']").first
        menu_button.wait_for(state="attached", timeout=5000)
        menu_button.wait_for(state="visible", timeout=5000)
        menu_button.wait_for(state="enabled", timeout=5000)
        menu_button.click()
        
        # Wait for network idle after navigation
        page.wait_for_load_state("networkidle", timeout=15000)
    
    def _validate_components(self, page):
        """Validation phase with flexible selectors"""
        errors = 0
        
        # Validate critical components (hard failure)
        try:
            critical_element = page.locator("#critical-component").first
            critical_element.wait_for(state="visible", timeout=15000)
            self.logger.info("[PASS] Critical component found")
        except Exception as e:
            self.logger.error(f"[FAIL] Critical component missing: {e}")
            raise
        
        # Validate optional components (soft warning)
        try:
            optional_element = self._find_element_with_fallbacks(page, [
                "button:has-text('Optional')",
                "[aria-label*='optional' i]",
                ".optional-button"
            ])
            if optional_element:
                self.logger.info("[PASS] Optional component found")
            else:
                self.logger.warning("[WARN] Optional component not found")
        except Exception as e:
            self.logger.warning(f"[WARN] Optional validation skipped: {e}")
        
        return errors
    
    def _wait_for_loading_overlay_to_disappear(self, page, timeout=5000):
        """Wait for loading spinners, progress bars, or blocking overlays to disappear"""
        loading_selectors = [
            ".loading-overlay",
            ".spinner",
            ".progress-bar",
            "[class*='loading']",
            "[class*='spinner']",
            "[class*='overlay']",
            ".MuiCircularProgress-root",  # Material-UI
            ".MuiBackdrop-root"  # Material-UI
        ]
        
        for selector in loading_selectors:
            try:
                loading_element = page.locator(selector).first
                if loading_element.is_visible(timeout=1000):
                    self.logger.info(f"Waiting for loading element to disappear: {selector}")
                    loading_element.wait_for(state="hidden", timeout=timeout)
                    self.logger.info(f"Loading element disappeared: {selector}")
            except:
                continue
    
    def _find_element_with_fallbacks(self, page, selectors):
        """Try multiple selectors to find element"""
        for selector in selectors:
            try:
                element = page.locator(selector).first
                if element.is_visible(timeout=3000):
                    self.logger.info(f"Found element using selector: {selector}")
                    return element
            except:
                continue
        return None
```

## Page Object Template

### Base Page with Synchronization
```python
from playwright.sync_api import Page
from utils.logger import Logger

class BasePage:
    """Base page class with synchronization methods"""
    
    def __init__(self, page: Page):
        self.page = page
        self.logger = Logger()
    
    def wait_for_network_idle(self, timeout=15000):
        """Wait for network to settle"""
        self.page.wait_for_load_state("networkidle", timeout=timeout)
    
    def wait_for_element_actionable(self, element, timeout=5000):
        """Wait for element to be fully actionable"""
        element.wait_for(state="attached", timeout=timeout)
        element.wait_for(state="visible", timeout=timeout)
        element.wait_for(state="enabled", timeout=timeout)
    
    def wait_for_loading_overlay_to_disappear(self, timeout=5000):
        """Wait for loading overlays to disappear"""
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
                loading_element = self.page.locator(selector).first
                if loading_element.is_visible(timeout=1000):
                    self.logger.info(f"Waiting for loading element: {selector}")
                    loading_element.wait_for(state="hidden", timeout=timeout)
            except:
                continue
```

### Specific Page Example
```python
from pages.base_page import BasePage
from locators.login_locators import LoginLocators

class LoginPage(BasePage):
    """Login page with full synchronization"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = LoginLocators()
    
    def load(self, url):
        """Load login page with network idle wait"""
        self.page.goto(url)
        self.wait_for_network_idle(timeout=15000)
    
    def enter_credentials(self, username, password):
        """Enter credentials with full synchronization"""
        # Wait for network idle
        self.wait_for_network_idle(timeout=10000)
        
        # Wait for loading overlays
        self.wait_for_loading_overlay_to_disappear()
        
        # Enter username
        username_input = self.page.locator(self.locators.USERNAME_INPUT).first
        self.wait_for_element_actionable(username_input)
        username_input.fill(username)
        
        # Wait for network idle after input
        self.wait_for_network_idle(timeout=5000)
        
        # Enter password
        password_input = self.page.locator(self.locators.PASSWORD_INPUT).first
        self.wait_for_element_actionable(password_input)
        password_input.fill(password)
        
        # Wait for network idle after input
        self.wait_for_network_idle(timeout=5000)
    
    def click_login_button(self):
        """Click login button with full synchronization"""
        # Wait for network idle
        self.wait_for_network_idle(timeout=10000)
        
        # Wait for loading overlays
        self.wait_for_loading_overlay_to_disappear()
        
        # Click login button
        login_button = self.page.locator(self.locators.LOGIN_BUTTON).first
        self.wait_for_element_actionable(login_button)
        login_button.click()
        
        # Wait for network idle after click
        self.wait_for_network_idle(timeout=15000)
```

## Component Template

### Base Component with Synchronization
```python
from playwright.sync_api import Page
from utils.logger import Logger

class BaseComponent:
    """Base component with synchronization methods"""
    
    def __init__(self, page: Page, locator: str):
        self.page = page
        self.element = page.locator(locator)
        self.logger = Logger()
    
    def _wait_for_loading_overlay_to_disappear(self, timeout=5000):
        """Wait for loading overlays to disappear"""
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
                loading_element = self.page.locator(selector).first
                if loading_element.is_visible(timeout=1000):
                    self.logger.info(f"Waiting for loading element: {selector}")
                    loading_element.wait_for(state="hidden", timeout=timeout)
            except:
                continue
    
    def _wait_for_element_actionable(self, timeout=5000):
        """Wait for element to be fully actionable"""
        self.element.wait_for(state="attached", timeout=timeout)
        self.element.wait_for(state="visible", timeout=timeout)
        self.element.wait_for(state="enabled", timeout=timeout)
```

### Dropdown Component Example
```python
from components.base_component import BaseComponent

class Dropdown(BaseComponent):
    """Dropdown with full synchronization"""
    
    def select_option(self, value):
        """Select option with full synchronization"""
        # Wait for network idle
        self.page.wait_for_load_state("networkidle", timeout=10000)
        
        # Wait for element to be actionable
        self._wait_for_element_actionable()
        
        # Wait for loading overlays
        self._wait_for_loading_overlay_to_disappear()
        
        # Select option
        self.element.select_option(value)
        
        # Wait for network idle after selection
        self.page.wait_for_load_state("networkidle", timeout=5000)
```

## Best Practices

### ✅ DO Use These Patterns

**1. Network Idle Waits:**
```python
page.wait_for_load_state("networkidle", timeout=15000)
```

**2. Element Stability Checks:**
```python
element.wait_for(state="attached", timeout=5000)
element.wait_for(state="visible", timeout=5000)
element.wait_for(state="enabled", timeout=5000)
```

**3. Loading Overlay Detection:**
```python
_wait_for_loading_overlay_to_disappear(page)
```

**4. Multiple Selector Fallbacks:**
```python
for selector in selectors:
    try:
        element = page.locator(selector).first
        if element.is_visible(timeout=3000):
            break
    except:
        continue
```

**5. Strict Mode Handling:**
```python
element = page.get_by_text("Submit").first
```

**6. Soft Logging for Optional Components:**
```python
try:
    # Validation
    logger.info("[PASS] Component validated")
except Exception as e:
    logger.warning(f"[WARN] Component validation skipped: {e}")
```

### ❌ DON'T Use These Patterns

**1. Static Timeouts:**
```python
# BAD
page.wait_for_timeout(3000)

# GOOD
page.wait_for_load_state("networkidle", timeout=15000)
```

**2. Single Element Assumption:**
```python
# BAD
element = page.get_by_text("Submit")

# GOOD
element = page.get_by_text("Submit").first
```

**3. Ignoring Loading Overlays:**
```python
# BAD
element.click()

# GOOD
_wait_for_loading_overlay_to_disappear(page)
element.click()
```

**4. Hard Failures for Optional Components:**
```python
# BAD
assert element.is_visible()

# GOOD
try:
    if element.is_visible():
        logger.info("[PASS] Component found")
    else:
        logger.warning("[WARN] Component not found")
except Exception as e:
    logger.warning(f"[WARN] Validation skipped: {e}")
```

## CSS Framework Patterns

### Material-UI
```python
# Buttons
"button.MuiButtonBase-root.MuiIconButton-root"
"button.MuiButton-textSizeSmall"

# Dropdowns
"#mui-component-select-sortList"
"ul.MuiList-root[role='listbox']"

# Spinners
".MuiCircularProgress-root"
".MuiBackdrop-root"

# Containers
".MuiBox-root.jss138"
```

### Bootstrap
```python
# Buttons
".btn", ".btn-primary"

# Forms
".form-control", ".form-group"

# Modals
".modal", ".modal-dialog"
```

## Browser Configuration

### Full Screen Mode
```python
# .env configuration
BROWSER_VIEWPORT = None
BROWSER_LAUNCH_ARGS = ['--start-maximized']
```

### CSS Injection for Layout Fixes
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

## Learned Patterns from Previous Projects

### Aditya Birla Project (April-May 2026)
**Key Learnings:**
- UAT requires 15-second timeouts (not 3-5s)
- Network idle waits prevent flaky tests
- Loading overlays block interactions
- Multiple selector fallbacks improve reliability
- Soft logging for optional components
- CSS injection fixes layout issues
- Material-UI has predictable class patterns
- Three-phase test structure improves maintainability

**Apply These Patterns:**
- Always use network idle waits in UAT
- Check for Material-UI classes if present
- Use flexible selectors for dynamic UI
- Implement loading overlay detection
- Classify component criticality
- Use base components with common synchronization

## Continuous Improvement

### After Each Test Execution:
1. Document synchronization patterns that worked
2. Document patterns that failed
3. Identify new CSS framework patterns
4. Update this prompt with learnings
5. Add to skills database

### Before Each New Project:
1. Review skills database
2. Identify relevant synchronization patterns
3. Check for CSS framework patterns
4. Apply appropriate timeout strategies
5. Document new learnings

---

*Last Updated: May 1, 2026 - Enhanced with Aditya Birla project synchronization patterns*
