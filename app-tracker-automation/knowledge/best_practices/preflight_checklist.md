# Pre-Flight Checklist - Before Test Execution

## Purpose
Prevent common issues by verifying environment, configuration, and prerequisites before running tests. This checklist reduces debugging time by catching issues early.

---

## 🚀 Daily Pre-Flight Checklist

### Environment Check
- [ ] **Application is Running**
  - URL is accessible: `curl -I https://uat.example.com`
  - Login page loads
  - No maintenance banners
  - No error pages

- [ ] **Test Data is Available**
  - Valid credentials exist in `.env`
  - Test user accounts are active
  - Required test data is in database
  - Data is not stale/expired

- [ ] **Network is Stable**
  - Internet connection is working
  - VPN is connected (if required)
  - Firewall allows test execution
  - Proxy settings are correct

- [ ] **Services are Up**
  - Database is accessible
  - API endpoints are responding
  - External services are available
  - No service outages

---

## 📋 Test-Specific Pre-Flight Checklist

### Before Writing New Tests

#### 1. Understand the User Story
- [ ] **Read the user story completely**
  - Understand the business requirement
  - Identify acceptance criteria
  - Note edge cases
  - Understand user flow

- [ ] **Analyze the Application**
  - Identify CSS framework (Material-UI, Bootstrap, custom)
  - Identify JavaScript framework (React, Angular, Vue)
  - Note dynamic elements (IDs, classes that change)
  - Map component hierarchy

- [ ] **Classify Components**
  - **Critical:** Login, data submission, payments
  - **Important:** Navigation, search, filters
  - **Optional:** Decorations, tooltips, help text

- [ ] **Plan Test Structure**
  - Three-phase structure (Authentication, Navigation, Validation)
  - Test data requirements
  - Environment-specific configurations
  - Error handling strategy

#### 2. Environment Configuration
- [ ] **Set Environment Type**
  ```python
  # .env
  ENVIRONMENT=UAT  # or DEV, PRODUCTION
  ```

- [ ] **Configure Timeouts**
  ```python
  # UAT: 15 seconds
  # Dev: 3-5 seconds
  # Production: 20 seconds
  TIMEOUT_UAT=15000
  TIMEOUT_DEV=3000
  ```

- [ ] **Configure Browser**
  ```python
  # .env
  HEADLESS=false  # true for CI, false for local
  BROWSER=chromium
  BROWSER_VIEWPORT=None  # Full screen
  BROWSER_LAUNCH_ARGS=--start-maximized
  ```

- [ ] **Configure Logging**
  ```python
  # .env
  LOG_LEVEL=INFO
  LOG_FILE=logs/test_execution.log
  SCREENSHOT_ON_FAILURE=true
  VIDEO_ON_FAILURE=true
  ```

#### 3. Test Data Setup
- [ ] **Verify Credentials**
  ```python
  # .env
  ADITYA_BIRLA_USER=test_user@example.com
  ADITYA_BIRLA_PASS=secure_password
  ```

- [ ] **Create Test Data**
  - Test user accounts
  - Test records in database
  - Required configuration values
  - Mock data if needed

- [ ] **Clean Old Data**
  - Remove stale test data
  - Reset test user state
  - Clear temporary records
  - Verify clean state

---

## 🔧 Technical Pre-Flight Checklist

### Before Running Tests

#### 1. Dependency Check
- [ ] **Python Dependencies**
  ```bash
  pip list | grep playwright
  pip list | grep pytest
  pip list | grep allure
  ```

- [ ] **Playwright Browsers**
  ```bash
  playwright install chromium
  playwright install firefox
  playwright install webkit
  ```

- [ ] **Environment Variables**
  ```bash
  # Verify .env file exists
  ls -la .env
  
  # Verify variables are loaded
  python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('BASE_URL'))"
  ```

#### 2. Code Quality Check
- [ ] **Code Formatting**
  ```bash
  black tests/
  flake8 tests/
  ```

- [ ] **Import Check**
  ```bash
  python -m py_compile tests/smoke/test_login.py
  ```

- [ ] **Syntax Check**
  ```bash
  pytest --collect-only tests/smoke/
  ```

#### 3. Configuration Check
- [ ] **conftest.py Configuration**
  - Browser fixtures are correct
  - Timeout values are appropriate
  - Logging is configured
  - Screenshot/video settings are correct

- [ ] **.env Configuration**
  - All required variables are set
  - Values are correct for environment
  - No hardcoded values in code
  - Secrets are not committed

- [ ] **PYTHONPATH Configuration**
  ```bash
  export PYTHONPATH="${PYTHONPATH}:$(pwd)"
  # Or in .env
  PYTHONPATH=/path/to/project
  ```

---

## 🧪 Test Execution Pre-Flight Checklist

### Before Running Test Suite

#### 1. Test Selection
- [ ] **Identify Tests to Run**
  - Smoke tests: Quick validation
  - Regression tests: Full coverage
  - Specific test: Debugging single issue

- [ ] **Check Test Dependencies**
  - Tests are independent
  - No shared state between tests
  - Cleanup is implemented
  - Test data is isolated

#### 2. Execution Mode
- [ ] **Choose Execution Mode**
  - Headed mode: For debugging
  - Headless mode: For CI/CD
  - Slow mode: For observing actions

- [ ] **Configure Reporting**
  - Allure reports enabled
  - JUnit XML for CI
  - Console output for local
  - Screenshots on failure

#### 3. Resource Check
- [ ] **Disk Space**
  ```bash
  df -h  # Ensure space for screenshots/videos
  ```

- [ ] **Memory**
  ```bash
  free -h  # Ensure sufficient memory
  ```

- [ ] **CPU**
  ```bash
  top  # Check CPU availability
  ```

---

## 🚨 Common Pre-Flight Issues and Fixes

### Issue 1: Application Not Running
**Symptoms:** Connection refused, timeout  
**Check:**
```bash
curl -I https://uat.example.com
```

**Fix:**
- Start application server
- Check firewall settings
- Verify URL is correct
- Check VPN connection

### Issue 2: Credentials Invalid
**Symptoms:** Login fails, 401 error  
**Check:**
```bash
# Verify .env file
cat .env | grep USER
```

**Fix:**
- Update credentials in .env
- Check account is active
- Verify password is correct
- Check account is not locked

### Issue 3: Dependencies Missing
**Symptoms:** ImportError, ModuleNotFoundError  
**Check:**
```bash
pip list | grep playwright
```

**Fix:**
```bash
pip install -r requirements.txt
playwright install
```

### Issue 4: Browser Not Installed
**Symptoms:** Executable doesn't exist  
**Check:**
```bash
playwright install --help
```

**Fix:**
```bash
playwright install chromium
playwright install firefox
playwright install webkit
```

### Issue 5: Timeouts Too Short
**Symptoms:** TimeoutError consistently  
**Check:**
```bash
# Check .env timeout values
cat .env | grep TIMEOUT
```

**Fix:**
- Increase timeout for UAT (15s)
- Increase timeout for production (20s)
- Use network idle waits
- Add loading overlay detection

### Issue 6: Selectors Wrong
**Symptoms:** Element not found  
**Check:**
```bash
# Use Playwright Inspector
playwright codegen https://uat.example.com
```

**Fix:**
- Verify selector with Inspector
- Use multiple fallback selectors
- Check for dynamic IDs/classes
- Use stable selectors (data-testid, ARIA)

---

## 📊 Pre-Flight Metrics

### Track These Metrics
- **Pre-Flight Time:** Time spent on checklist
- **Issues Found:** Number of issues caught
- **Issues Prevented:** Issues that would have caused test failure
- **Time Saved:** Debugging time saved by catching issues early

### Goal Metrics
- **Pre-Flight Time:** < 5 minutes
- **Issues Found Rate:** > 20% (catching issues is good)
- **Test Success Rate:** > 95% after pre-flight
- **Debugging Time Reduction:** > 50%

---

## 🎯 Quick Pre-Flight Commands

```bash
# Quick environment check
curl -I $BASE_URL

# Quick dependency check
pip list | grep playwright

# Quick browser check
playwright install --dry-run

# Quick syntax check
pytest --collect-only tests/smoke/

# Quick config check
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('BASE_URL:', os.getenv('BASE_URL'))"

# Quick test run (smoke)
pytest tests/smoke/ -v --maxfail=1
```

---

## 📝 Pre-Flight Template

### Copy This Template for Each Test Session

```markdown
## Pre-Flight Checklist - [Date]

### Environment
- [ ] Application running: [URL]
- [ ] Test data available: [Yes/No]
- [ ] Network stable: [Yes/No]
- [ ] Services up: [Yes/No]

### Configuration
- [ ] Environment type: [UAT/DEV/PROD]
- [ ] Timeouts configured: [Yes/No]
- [ ] Browser configured: [Yes/No]
- [ ] Logging configured: [Yes/No]

### Test Data
- [ ] Credentials verified: [Yes/No]
- [ ] Test data created: [Yes/No]
- [ ] Old data cleaned: [Yes/No]

### Technical
- [ ] Dependencies installed: [Yes/No]
- [ ] Browsers installed: [Yes/No]
- [ ] Code formatted: [Yes/No]
- [ ] Syntax check passed: [Yes/No]

### Execution
- [ ] Tests selected: [List]
- [ ] Execution mode: [Headed/Headless]
- [ ] Reporting configured: [Yes/No]
- [ ] Resources available: [Yes/No]

### Issues Found
- [Issue 1]: [Description] - [Fix]
- [Issue 2]: [Description] - [Fix]

### Notes
[Any additional notes]
```

---

## 🚀 Automation Opportunities

### Automate These Checks
```python
# pre_flight_check.py
import os
import requests
from dotenv import load_dotenv

def run_pre_flight_checks():
    """Automated pre-flight checks"""
    load_dotenv()
    
    issues = []
    
    # Check application
    try:
        response = requests.head(os.getenv("BASE_URL"), timeout=10)
        if response.status_code != 200:
            issues.append(f"Application not accessible: {response.status_code}")
    except Exception as e:
        issues.append(f"Application check failed: {e}")
    
    # Check credentials
    if not os.getenv("TEST_USERNAME"):
        issues.append("TEST_USERNAME not set in .env")
    
    # Check dependencies
    try:
        import playwright
    except ImportError:
        issues.append("Playwright not installed")
    
    # Report
    if issues:
        print("❌ Pre-flight checks failed:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ All pre-flight checks passed")
        return True

if __name__ == "__main__":
    run_pre_flight_checks()
```

**Usage:**
```bash
python pre_flight_check.py
pytest tests/smoke/  # Only if checks pass
```

---

## 📚 Continuous Improvement

### After Each Test Execution
1. **Document issues found during pre-flight**
2. **Update checklist with new checks**
3. **Automate manual checks**
4. **Share with team**

### Weekly Review
1. **Review pre-flight metrics**
2. **Identify common issues**
3. **Add new checks**
4. **Improve automation**

---

*Last Updated: May 1, 2026*
