# Test Cases: Login & App Tracker Navigation

**Generated From:** stories/refined/login_tracker_story_analysis.md  
**Generation Date:** May 2, 2026  
**Environment:** UAT (Aditya Birla Sun Life Insurance)  
**Framework:** Playwright + Python + Pytest

---

## Test Case: TC001 - Successful Login Flow

### Priority
Critical

### Tags
smoke, critical, authentication

### Preconditions
- UAT environment is accessible
- Valid credentials available in .env file
- Browser is configured for full-screen mode
- Network connection is stable

### Test Steps
1. Initialize browser with full-screen mode and inject layout CSS
2. Navigate to `https://leapuat.adityabirlasunlifeinsurance.com/uat/#/login`
3. Wait for network idle (15s for UAT)
4. Verify login page loads within 2 seconds
5. Verify header displays "Aditya Birla Capital" branding
6. Verify blue "UAT" badge is visible in bottom-left corner
7. Load credentials from .env file (ADITYA_BIRLA_USER, ADITYA_BIRLA_PASS)
8. Enter username in login field
9. Enter password in password field
10. Verify password masks as bullets
11. Wait for element stability (attached, visible, enabled)
12. Click LOGIN > button
13. Wait for network idle (15s)
14. Wait for loading overlay to disappear
15. Verify redirect to `/dashboard`
16. Verify dashboard renders without flicker
17. Verify session token persists
18. Verify UAT badge persists on dashboard

### Expected Results
- Login page loads within 2 seconds
- Header displays correct branding
- UAT badge is visible
- Credentials populate correctly
- Password is masked
- Login button is clickable
- Redirect to dashboard occurs
- Dashboard renders without errors
- Session is established
- UAT badge remains visible

### Test Data Requirements
- Valid username from .env (ADITYA_BIRLA_USER)
- Valid password from .env (ADITYA_BIRLA_PASS)

### Error Handling
- If page load timeout: Log error, fail test (critical)
- If credentials not loaded: Log error, fail test (critical)
- If redirect fails: Log error, fail test (critical)
- If UAT badge missing: Log warning, continue (non-critical)

### Synchronization
- Network idle wait: 15s (UAT)
- Element stability checks: attached, visible, enabled
- Loading overlay detection before clicks
- CSS injection for layout stability

---

## Test Case: TC002 - Dashboard Navigation to Application Tracker

### Priority
Critical

### Tags
smoke, critical, navigation

### Preconditions
- User is logged in
- Dashboard is loaded
- Session is active

### Test Steps
1. Verify dashboard is fully loaded
2. Wait for network idle (15s)
3. Locate MENU button using multiple selectors:
   - `button.menu-button[aria-label='menu']`
   - `button[aria-label*='menu' i]`
   - `.menu-button`
   - `button:has-text('MENU')`
4. Wait for element stability (attached, visible, enabled)
5. Click MENU button
6. Wait for network idle (5s)
7. Verify menu expands with items: Help, Application Tracker, Approvals, Logout
8. Locate Application Tracker link
9. Wait for element stability
10. Click Application Tracker link
11. Wait for network idle (15s)
12. Verify new tab opens
13. Verify URL changes to `onboarding-uat.adityabirlasunlifeinsurance.com/app-tracker/applications`
14. Switch to Application Tracker tab
15. Wait for page load (15s)
16. Verify Application Tracker page loads
17. Verify URL contains `app-tracker/applications`

### Expected Results
- MENU button is visible and clickable
- Menu expands with correct items
- Application Tracker link is visible
- New tab opens
- URL changes to correct domain
- Application Tracker page loads
- UAT badge persists

### Test Data Requirements
- Valid session from TC001
- Application Tracker URL

### Error Handling
- If MENU button not found: Try fallback selectors, log error, fail test (critical)
- If menu doesn't expand: Log error, fail test (critical)
- If Application Tracker link not found: Log error, fail test (critical)
- If new tab doesn't open: Log error, fail test (critical)
- If page load timeout: Log error, fail test (critical)

### Synchronization
- Network idle wait: 15s (UAT)
- Element stability checks
- Tab switching wait
- Loading overlay detection

---

## Test Case: TC003 - Filter Components Validation

### Priority
High

### Tags
regression, components, filters

### Preconditions
- User is on Application Tracker page
- Page is fully loaded

### Test Steps
1. Wait for network idle (15s)
2. Validate Filter Button:
   - Try selectors: `.filter-button`, `button:has-text('Filter')`, `[data-testid='filter']`
   - If visible: Log PASS
   - If not visible: Log WARN (optional component)
3. Validate Policy List Title:
   - Use `page.get_by_text("Policy List").first`
   - Wait for element stability
   - If visible: Log PASS
   - If not visible: Log WARN (optional component)
4. Validate Search Box:
   - Try selectors: `input[placeholder*='Search']`, `input[placeholder*='search']`, `input[type='text']`, `.navbar-search`
   - If visible: Log PASS
   - If not visible: Log WARN (optional component)
5. Validate Date Filter:
   - Try selectors: `span:has-text('Prev + Current Month')`, `button:has-text('Prev + Current Month')`, `.date-filter`
   - If visible: Log PASS
   - If not visible: Log WARN (optional component)
6. Validate Filter Chips:
   - Look for status tags (Pending, Approved, etc.)
   - If visible: Log PASS
   - If not visible: Log WARN (optional component)
7. Validate Download Button:
   - Try selectors: `button:has-text('Download')`, `.download-button`, `[data-testid='download']`
   - If visible: Log PASS
   - If not visible: Log WARN (optional component)
8. Validate Sort Dropdown:
   - Try selectors: `#mui-component-select-sortList`, `button:has-text('Sort')`, `.sort-dropdown`
   - If visible: Log PASS
   - If not visible: Log WARN (optional component)

### Expected Results
- All filter components are present (or logged as warnings if optional)
- No console errors
- Components match design specifications
- UAT badge is visible

### Test Data Requirements
- Application Tracker page loaded

### Error Handling
- Use soft logging (WARN) for optional components
- Do not fail test if optional components are missing
- Log error if critical components fail to load

### Synchronization
- Network idle wait: 15s (UAT)
- Multiple selector fallbacks (3s each)
- Element stability checks
- Soft logging for non-critical components

---

## Test Case: TC004 - Table Components Validation

### Priority
High

### Tags
regression, components, table

### Preconditions
- User is on Application Tracker page
- Page is fully loaded

### Test Steps
1. Wait for network idle (15s)
2. Validate Table Header:
   - Try selectors: `thead th`, `table th`, `.MuiTableCell-head`, `[role='columnheader']`, `th`
   - If visible: Log PASS
   - If not visible: Log WARN (optional component)
3. Validate Table Rows:
   - Try selectors: `.MuiBox-root.jss138`, `tbody tr`, `table tbody tr`
   - Use `.first` to handle strict mode
   - If visible: Log PASS
   - If not visible: Log WARN (optional component)
4. Validate Plan Name Column:
   - Extract from first row using `.plan-name.first`
   - Wait for element stability
   - If visible: Log PASS and extract plan name
   - If not visible: Log WARN (optional component)
5. Validate Premium Amount Column:
   - Look for currency symbol (₹) in row
   - Use selector: `:scope > *:has-text('₹')`
   - If visible: Log PASS and extract amount
   - If not visible: Log WARN (optional component)
6. Validate Status Tags:
   - Look for status indicators (Pending, Approved, etc.)
   - If visible: Log PASS
   - If not visible: Log WARN (optional component)
7. Validate Sorting Indicators:
   - Look for SVG icons in table headers
   - If visible: Log PASS
   - If not visible: Log WARN (optional component)
8. Validate Row Interactivity:
   - Try clicking first row with `force=True`
   - If clickable: Log PASS
   - If not clickable: Log WARN (optional component)

### Expected Results
- Table headers display correct columns (App.No, Proposer Name, Plan Name, Modal Premium, Policy Status)
- Data rows are populated
- Currency symbol (₹) is present
- Status indicators are visible
- Sorting indicators are present
- Rows are clickable
- No console errors

### Test Data Requirements
- Application Tracker page loaded
- Table data present

### Error Handling
- Use soft logging (WARN) for optional components
- Use `.first` for strict mode violations
- Log error if table structure is completely missing

### Synchronization
- Network idle wait: 15s (UAT)
- Multiple selector fallbacks (3s each)
- Element stability checks
- Strict mode handling with `.first`

---

## Test Case: TC005 - Invalid Credentials (Negative Test)

### Priority
Medium

### Tags
negative, authentication, security

### Preconditions
- UAT environment is accessible
- Invalid test credentials available

### Test Steps
1. Navigate to login page
2. Wait for network idle (15s)
3. Enter invalid username
4. Enter invalid password
5. Wait for element stability
6. Click LOGIN > button
7. Wait for network idle (5s)
8. Verify inline error message is displayed
9. Verify input field borders turn red
10. Verify focus resets to first field
11. Verify no redirect occurs
12. Verify session is not created

### Expected Results
- Inline error message displayed
- Input fields show red borders
- Focus returns to first field
- No redirect to dashboard
- Session not created
- No console errors

### Test Data Requirements
- Invalid username (test data)
- Invalid password (test data)

### Error Handling
- If error message not displayed: Log error, fail test
- If redirect occurs: Log error, fail test
- If session created: Log error, fail test

### Synchronization
- Network idle wait: 15s (UAT)
- Element stability checks
- No loading overlay wait (should fail quickly)

---

## Test Case: TC006 - Session Expiry Handling

### Priority
Medium

### Tags
edge-case, session, security

### Preconditions
- User is logged in
- Session is active

### Test Steps
1. Log in successfully
2. Navigate to Application Tracker
3. Clear session or wait for expiry
4. Refresh Application Tracker page
5. Wait for network idle (15s)
6. Verify automatic redirect to login page
7. Verify no access to protected pages
8. Verify clear session expiry message
9. Verify no sensitive data exposure

### Expected Results
- Automatic redirect to login page
- No access to protected pages
- Clear session expiry message
- No sensitive data in URL
- No console errors

### Test Data Requirements
- Valid credentials
- Session management capability

### Error Handling
- If redirect doesn't occur: Log error, fail test
- If protected pages accessible: Log error, fail test (security issue)
- If sensitive data exposed: Log error, fail test (security issue)

### Synchronization
- Network idle wait: 15s (UAT)
- Page refresh wait
- Redirect detection

---

## Test Case: TC007 - Network Failure Handling

### Priority
Medium

### Tags
edge-case, network, resilience

### Preconditions
- UAT environment is accessible
- Network simulation capability

### Test Steps
1. Navigate to login page
2. Enter valid credentials
3. Simulate network offline
4. Click login button
5. Wait for response (5s)
6. Verify error toast/alert is displayed
7. Verify no indefinite loading
8. Verify user can retry
9. Verify no application crash
10. Restore network connection

### Expected Results
- Error message displayed
- No indefinite loading
- User can retry
- No application crash
- No console errors

### Test Data Requirements
- Valid credentials
- Network simulation tool

### Error Handling
- If indefinite loading: Log error, fail test
- If no error message: Log error, fail test
- If application crashes: Log error, fail test

### Synchronization
- Short timeout for network failure (5s)
- Error detection
- No network idle wait (network is down)

---

## Test Case: TC008 - Keyboard Navigation

### Priority
Low

### Tags
accessibility, keyboard, a11y

### Preconditions
- Login page is loaded
- Keyboard is available

### Test Steps
1. Navigate to login page
2. Press Tab to navigate to first field
3. Verify visible focus ring on username field
4. Enter username
5. Press Tab to navigate to password field
6. Verify visible focus ring on password field
7. Enter password
8. Press Tab to navigate to login button
9. Verify visible focus ring on login button
10. Press Enter to submit
11. Verify login proceeds
12. Verify tab order is logical

### Expected Results
- All elements accessible via keyboard
- Focus rings are visible
- Tab order is logical
- Enter key triggers actions
- No mouse-only navigation required

### Test Data Requirements
- Valid credentials

### Error Handling
- If focus rings not visible: Log warning (accessibility issue)
- If tab order illogical: Log warning (accessibility issue)
- If Enter key doesn't work: Log error, fail test

### Synchronization
- Standard element waits
- Focus detection
- No network idle waits needed

---

## Test Case: TC009 - Search Box Functionality

### Priority
High

### Tags
functional, search, components

### Preconditions
- User is on Application Tracker page
- Page is fully loaded

### Test Steps
1. Wait for network idle (15s)
2. Locate search input using multiple selectors:
   - `input[placeholder*='Search']`
   - `input[placeholder*='search']`
   - `input[type='text']`
   - `.navbar-search`
   - `input.search`
   - `[data-testid='search-input']`
3. Wait for element stability (attached, visible, enabled)
4. Verify search input is a text field (not image)
5. Enter search term "LA53544020"
6. Wait for network idle (5s)
7. Verify search term is visible in input
8. Verify search term persists in input_value()
9. Clear search input
10. Verify input is empty

### Expected Results
- Search input is a text field
- Input accepts text
- Search term is visible
- Search term persists
- Input can be cleared
- No console errors

### Test Data Requirements
- Search term: "LA53544020"

### Error Handling
- If search input not found: Log WARN (optional component)
- If input is image: Log error, fail test
- If input doesn't accept text: Log error, fail test
- If search term doesn't persist: Log error, fail test

### Synchronization
- Network idle wait: 15s (UAT)
- Multiple selector fallbacks (3s each)
- Element stability checks
- Input validation wait

---

## Test Case: TC010 - Sort Dropdown Functionality

### Priority
High

### Tags
functional, sort, components

### Preconditions
- User is on Application Tracker page
- Page is fully loaded

### Test Steps
1. Wait for network idle (15s)
2. Press Escape to clear any blocking overlays
3. Locate sort dropdown using multiple selectors:
   - `#mui-component-select-sortList`
   - `button:has-text('Sort')`
   - `.sort-dropdown`
   - `[data-testid='sort']`
4. Wait for element stability (attached, visible, enabled)
5. Click sort dropdown with `force=True`
6. Wait for network idle (5s)
7. Verify dropdown opens
8. Wait 500ms for animation
9. Press Escape to close dropdown
10. Verify dropdown closes
11. Verify no modal blocking issues
12. Verify no timeout errors

### Expected Results
- Sort button is clickable
- Dropdown opens on click
- Dropdown closes on Escape
- No modal blocking
- No timeout errors
- No console errors

### Test Data Requirements
- Application Tracker page loaded

### Error Handling
- If sort dropdown not found: Log WARN (optional component)
- If dropdown doesn't open: Log error, fail test
- If dropdown doesn't close: Log error, fail test
- If modal blocks: Log error, fail test

### Synchronization
- Network idle wait: 15s (UAT)
- Multiple selector fallbacks (3s each)
- Element stability checks
- Escape key to clear overlays
- Animation wait (500ms)

---

## Test Case: TC011 - Global Consistency Check

### Priority
Medium

### Tags
regression, consistency, security

### Preconditions
- User is logged in
- User has navigated through multiple pages

### Test Steps
1. Verify UAT badge on login page
2. Navigate to dashboard
3. Verify UAT badge on dashboard
4. Navigate to Application Tracker
5. Verify UAT badge on Application Tracker
6. Check URL fragments for sensitive data
7. Verify no credentials in URL
8. Verify no session tokens in URL
9. Verify no sensitive data in console logs

### Expected Results
- UAT badge persists across all views
- No sensitive data in URL fragments
- No credentials in URL
- No session tokens in URL
- No sensitive data in console logs
- No console errors

### Test Data Requirements
- Valid session

### Error Handling
- If UAT badge missing: Log warning (non-critical)
- If sensitive data in URL: Log error, fail test (security issue)
- If sensitive data in console: Log error, fail test (security issue)

### Synchronization
- Standard navigation waits
- URL validation
- Console log inspection

---

## Test Execution Summary

### Total Test Cases: 11
- Critical: 2 (TC001, TC002)
- High: 4 (TC003, TC004, TC009, TC010)
- Medium: 4 (TC005, TC006, TC007, TC011)
- Low: 1 (TC008)

### Estimated Execution Time
- Smoke tests (TC001, TC002): ~45 seconds
- Regression tests (TC003, TC004, TC009, TC010): ~60 seconds
- Negative/Edge cases (TC005-TC007, TC011): ~90 seconds
- Accessibility (TC008): ~30 seconds
- **Total:** ~3.5 minutes

### Environment-Specific Configuration
- **UAT Timeouts:** 15s for network idle, 5s for element waits
- **Dev Timeouts:** 3s for network idle, 2s for element waits
- **Production Timeouts:** 20s for network idle, 5s for element waits

### Component Criticality Classification
- **Critical (Hard Failures):** Login, navigation, session management
- **High (Soft Failures):** Filter components, table components, search, sort
- **Medium (Soft Failures):** Error handling, network resilience
- **Low (Soft Failures):** Accessibility, UI decorations

### Learned Patterns Applied
- Network idle waits before critical interactions
- Multiple selector fallbacks for dynamic UI
- Element stability checks (attached, visible, enabled)
- Loading overlay detection
- Strict mode handling with `.first`
- Soft logging for optional components
- CSS injection for layout stability
- Material-UI class pattern recognition

---

*Generated using testcase-generation.md framework*  
*Applied learnings from Aditya Birla project (April-May 2026)*  
*Last Updated: May 2, 2026*
