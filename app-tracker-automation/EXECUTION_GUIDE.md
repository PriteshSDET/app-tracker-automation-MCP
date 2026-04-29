# Test Execution Guide - Login & Application Tracker

## Overview
This guide provides step-by-step instructions for executing the AI-generated test for Login & Application Tracker navigation using the App Tracker Automation Framework.

## Generated Files

### 📝 Test Case Input
- **`tests/smoke/Login.md`** - Original test case specification with 11 detailed steps

### 🤖 AI-Generated Test Files
- **`tests/smoke/test_login_tracker.py`** - Initial Playwright test implementation
- **`tests/smoke/execute_login_tracker_test.py`** - Enhanced test with comprehensive logging
- **`run_login_test.py`** - Test runner script with environment setup

### 🏗️ Framework Components
- **`locators/aditya_birla_locators.py`** - Aditya Birla specific element locators
- **`pages/aditya_birla_login_page.py`** - Login page object
- **`pages/aditya_birla_dashboard_page.py`** - Dashboard page object
- **`pages/aditya_birla_tracker_page.py** - Application tracker page object

## Execution Instructions

### Prerequisites
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```

2. **Environment Setup**:
   - Ensure UAT environment is accessible
   - Verify credentials: `BR4641` / `q7LD4$J!d7`
   - Check network connectivity

### Option 1: Quick Execution
```bash
# Navigate to framework directory
cd app-tracker-automation

# Run the test runner script
python run_login_test.py
```

### Option 2: Pytest Execution
```bash
# Run specific test with comprehensive reporting
pytest tests/smoke/execute_login_tracker_test.py -v \
  --html=reports/html/login_test_report.html \
  --alluredir=reports/allure \
  --junitxml=reports/junit/login_test_results.xml \
  --browser=chromium \
  --screenshot=only-on-failure \
  --video=retain-on-failure
```

### Option 3: Individual Test Execution
```bash
# Run main test
pytest tests/smoke/execute_login_tracker_test.py::TestLoginTrackerNavigation::test_login_tracker_complete_flow -v

# Run negative tests
pytest tests/smoke/execute_login_tracker_test.py::TestLoginTrackerNavigation::test_login_negative_scenarios -v

# Run accessibility tests
pytest tests/smoke/execute_login_tracker_test.py::TestLoginTrackerNavigation::test_accessibility_compliance -v
```

## Test Coverage

### ✅ Main Test Flow (`test_login_tracker_complete_flow`)
1. **Navigate to Login Page**
   - URL: `https://leapuat.adityabirlasunlifeinsurance.com/uat/#/login`
   - Validate UAT badge and branding
   - Verify form elements

2. **Enter Credentials**
   - Username: `BR4641`
   - Password: `q7LD4$J!d7`
   - Validate input focus and masking

3. **Login Authentication**
   - Click LOGIN button
   - Verify POST request and redirect

4. **Dashboard Validation**
   - URL contains `dashboard`
   - Verify "Application List" header
   - Check toolbar elements (Filter, Sort)
   - Validate data table and pending indicators
   - Confirm UAT badge persistence

5. **Navigate to Application Tracker**
   - Click MENU ▾ dropdown
   - Select "Application Tracker"
   - Verify URL change to `app-tracker`

6. **Application Tracker Validation**
   - Verify "Policy List" title
   - Check refresh info ("15 minutes")
   - Validate table headers: App.No, Proposer Name, Plan Name, Modal Premium, Policy Status
   - Confirm filter controls (chips, search, date picker)
   - Validate data integrity

### ✅ Negative Tests (`test_login_negative_scenarios`)
1. **Invalid Credentials**
   - Test with wrong username/password
   - Verify error message display
   - Confirm focus reset to username field

2. **Empty Credentials**
   - Test with blank fields
   - Verify validation behavior

### ✅ Accessibility Tests (`test_accessibility_compliance`)
1. **Keyboard Navigation**
   - Tab through form elements
   - Verify focus order

2. **Focus Visibility**
   - Check focus indicators
   - Validate WCAG compliance

## Framework Prompts Used

### 🤖 AI Generation Process
The test was generated using the framework's AI prompts:

1. **`prompts/testcase-generation.md`**
   - Analyzed the Login.md test case
   - Generated positive and negative test scenarios
   - Defined test data requirements
   - Specified expected results

2. **`prompts/playwright-generation.md`**
   - Converted test cases to Playwright code
   - Implemented Page Object Model pattern
   - Added comprehensive logging
   - Included proper error handling

3. **`prompts/insurance-rules.md`**
   - Applied insurance domain knowledge
   - Validated business logic
   - Ensured compliance requirements

## Reports and Artifacts

### 📊 Generated Reports
- **HTML Report**: `reports/html/login_test_report.html`
- **Allure Report**: `reports/allure/`
- **JUnit XML**: `reports/junit/login_test_results.xml`
- **Execution Summary**: `reports/execution_summary_*.json`

### 📸 Screenshots
- **Success Screenshots**: `screenshots/passed/`
- **Failure Screenshots**: `screenshots/failed/`

### 🎥 Videos (on failure)
- **Test Videos**: `videos/failed/`

### 🔍 Traces (on failure)
- **Execution Traces**: `traces/failed/`

### 📝 Logs
- **Execution Logs**: `logs/execution.log`
- **Error Logs**: `logs/error.log`

## Validation Checkpoints

### ✅ Login Page Validation
- [ ] UAT badge visible
- [ ] Aditya Birla branding displayed
- [ ] Login form elements present
- [ ] URL contains `#/login`

### ✅ Dashboard Validation
- [ ] Application List header displayed
- [ ] Filter and Sort controls present
- [ ] Data table with rows visible
- [ ] Pending status indicators
- [ ] New Application button visible
- [ ] UAT badge persists

### ✅ Application Tracker Validation
- [ ] Policy List title displayed
- [ ] Refresh info ("15 minutes") visible
- [ ] All table headers present
- [ ] Filter controls active
- [ ] Data integrity verified
- [ ] UAT badge persists

### ✅ Cross-Page Consistency
- [ ] UAT badge visible on all pages
- [ ] No sensitive data in URLs
- [ ] Seamless navigation between pages
- [ ] Consistent branding throughout

## Troubleshooting

### Common Issues
1. **Element Not Found**
   - Check if selectors match actual UI
   - Verify page is fully loaded
   - Update locators in `aditya_birla_locators.py`

2. **Timeout Errors**
   - Increase wait timeouts
   - Check network connectivity
   - Verify UAT environment availability

3. **Authentication Failures**
   - Verify credentials are correct
   - Check if UAT environment is accessible
   - Validate session management

4. **Screenshot/Video Failures**
   - Ensure directories exist
   - Check file permissions
   - Verify disk space

### Debug Mode
```bash
# Run with visible browser for debugging
pytest tests/smoke/execute_login_tracker_test.py --headed=true --slowmo=1000

# Run with Playwright Inspector
pytest tests/smoke/execute_login_tracker_test.py --debug

# Run with tracing
pytest tests/smoke/execute_login_tracker_test.py --tracing=on
```

## Next Steps

### For Test Enhancement
1. Add more test scenarios based on business requirements
2. Implement data-driven testing with Excel files
3. Add performance testing metrics
4. Expand cross-browser testing

### For Framework Maintenance
1. Update locators when UI changes
2. Review and optimize test execution time
3. Add more comprehensive error handling
4. Enhance reporting capabilities

### For CI/CD Integration
1. Configure GitHub Actions workflow
2. Set up automated report generation
3. Implement test result notifications
4. Add environment-specific configurations

## Success Criteria

### ✅ Test Pass Criteria
- All 11 test steps execute successfully
- Zero console errors
- All validation checkpoints pass
- Screenshots captured for key steps
- Reports generated successfully

### ✅ Framework Validation
- Component-driven architecture working
- Page Object Model implemented correctly
- AI prompts generating valid code
- Comprehensive logging functioning
- Error handling working properly

---

**Ready for Execution!** 🚀

The AI-generated test is now ready for execution. Run `python run_login_test.py` to start the comprehensive test execution with full logging and reporting.
