# Story Analysis: Login & App Tracker Navigation

**Source:** tests/smoke/Login.md  
**Analysis Date:** May 2, 2026  
**Environment:** UAT (Aditya Birla Sun Life Insurance)  
**Module:** UAT Portal / Onboarding

---

## 1. User Story Summary

**Story Title:** End-to-End Authentication to Application Tracker

**Business Requirement:**
Users need to successfully log into the Aditya Birla Sun Life Insurance UAT portal, navigate to the dashboard, and access the Application Tracker workspace to view and manage insurance applications.

**Acceptance Criteria:**
- User can log in with valid credentials
- Dashboard loads correctly after login
- User can navigate to Application Tracker via menu
- Application Tracker page loads with all components
- Filter and table components are functional
- UAT environment badge is visible throughout

---

## 2. Test Scenarios Identified

### Scenario 1: Successful Login Flow (Happy Path)
**Priority:** Critical  
**Type:** UI / Smoke  
**Description:** Verify user can successfully log in with valid credentials and reach dashboard

**Steps:**
1. Navigate to login page
2. Enter valid credentials
3. Click login button
4. Verify redirect to dashboard
5. Verify session persistence

**Success Criteria:**
- Login page loads within 2 seconds
- Credentials accepted
- Redirect to dashboard occurs
- Dashboard renders without errors
- Session token persists

---

### Scenario 2: Dashboard Navigation to Application Tracker
**Priority:** Critical  
**Type:** UI / Smoke  
**Description:** Verify user can navigate from dashboard to Application Tracker

**Steps:**
1. Click MENU button
2. Verify menu expands
3. Click Application Tracker link
4. Verify new tab opens
5. Switch to Application Tracker tab
6. Verify page loads

**Success Criteria:**
- Menu button is clickable
- Menu expands with correct items
- Application Tracker link is visible
- New tab opens with correct URL
- Application Tracker page loads

---

### Scenario 3: Filter Components Validation
**Priority:** High  
**Type:** UI / Regression  
**Description:** Verify all filter components are present and functional

**Steps:**
1. Verify Filter Button is visible
2. Verify Policy List title is displayed
3. Verify Search Box is present
4. Verify Date Filter option exists
5. Verify Filter Chips are displayed
6. Verify Download Button is present
7. Verify Sort Dropdown is clickable

**Success Criteria:**
- All filter components are visible
- Components are clickable/interactive
- No console errors
- Components match design specifications

---

### Scenario 4: Table Components Validation
**Priority:** High  
**Type:** UI / Regression  
**Description:** Verify table structure and data display

**Steps:**
1. Verify table headers are visible
2. Verify table rows are displayed
3. Verify Plan Name column
4. Verify Premium Amount column
5. Verify Status tags
6. Verify sorting indicators
7. Verify row interactivity

**Success Criteria:**
- Table headers display correct columns
- Data rows are populated
- Currency symbol (₹) is present
- Status indicators are visible
- Rows are clickable

---

### Scenario 5: Invalid Credentials (Negative Test)
**Priority:** Medium  
**Type:** UI / Negative  
**Description:** Verify system handles invalid credentials correctly

**Steps:**
1. Navigate to login page
2. Enter invalid username
3. Enter invalid password
4. Click login button
5. Verify error message
6. Verify input field borders turn red
7. Verify focus resets to first field

**Success Criteria:**
- Inline error message displayed
- Input fields show red borders
- Focus returns to first field
- No redirect occurs
- Session not created

---

### Scenario 6: Session Expiry Handling
**Priority:** Medium  
**Type:** UI / Edge Case  
**Description:** Verify system handles session expiry correctly

**Steps:**
1. Log in successfully
2. Navigate to Application Tracker
3. Clear session / wait for expiry
4. Refresh Application Tracker page
5. Verify redirect to login

**Success Criteria:**
- Automatic redirect to login page
- No access to protected pages
- Clear session expiry message
- No sensitive data exposure

---

### Scenario 7: Network Failure Handling
**Priority:** Medium  
**Type:** UI / Edge Case  
**Description:** Verify system handles network failures gracefully

**Steps:**
1. Navigate to login page
2. Enter valid credentials
3. Simulate network offline
4. Click login button
5. Verify error toast/alert
6. Verify no indefinite hang

**Success Criteria:**
- Error message displayed
- No indefinite loading
- User can retry
- No application crash

---

### Scenario 8: Keyboard Navigation
**Priority:** Low  
**Type:** UI / Accessibility  
**Description:** Verify keyboard navigation works correctly

**Steps:**
1. Navigate to login page
2. Tab through all elements
3. Verify visible focus rings
4. Verify elements gain focus
5. Verify Enter key works for buttons

**Success Criteria:**
- All elements accessible via keyboard
- Focus rings are visible
- Tab order is logical
- Enter key triggers actions

---

### Scenario 9: Search Box Functionality
**Priority:** High  
**Type:** UI / Functional  
**Description:** Verify search box accepts input and filters results

**Steps:**
1. Locate search input field
2. Enter search term (e.g., "LA53544020")
3. Verify input is accepted
4. Verify search term persists
5. Clear search input

**Success Criteria:**
- Search input is a text field (not image)
- Input accepts text
- Search term is visible
- Input can be cleared
- No console errors

---

### Scenario 10: Sort Dropdown Functionality
**Priority:** High  
**Type:** UI / Functional  
**Description:** Verify sort dropdown opens and closes correctly

**Steps:**
1. Locate sort dropdown button
2. Click sort dropdown
3. Verify dropdown opens
4. Press Escape to close
5. Verify dropdown closes

**Success Criteria:**
- Sort button is clickable
- Dropdown opens on click
- Dropdown closes on Escape
- No modal blocking issues
- No timeout errors

---

## 3. Test Data Requirements

### Required Test Data
| Data Type | Source | Purpose |
|-----------|--------|---------|
| Valid Username | .env file (ADITYA_BIRLA_USER) | Successful login |
| Valid Password | .env file (ADITYA_BIRLA_PASS) | Successful login |
| Invalid Username | Test data | Negative testing |
| Invalid Password | Test data | Negative testing |
| Search Term | Test data (e.g., "LA53544020") | Search functionality |
| Application Number | Test data | Table validation |

### Configuration Requirements
| Configuration | Value | Purpose |
|----------------|-------|---------|
| Base URL | https://leapuat.adityabirlasunlifeinsurance.com/uat | Login page |
| Tracker URL | https://onboarding-uat.adityabirlasunlifeinsurance.com/app-tracker/applications | Application Tracker |
| Browser | Chrome (Latest Stable) | Test execution |
| Viewport | Full screen | Layout stability |
| Timeout (UAT) | 15000ms | Network waits |
| Timeout (Dev) | 3000ms | Network waits |

---

## 4. Test Type Classification

| Scenario | Test Type | Priority | Automation Level |
|----------|-----------|----------|------------------|
| Scenario 1 | UI / Smoke | Critical | Full |
| Scenario 2 | UI / Smoke | Critical | Full |
| Scenario 3 | UI / Regression | High | Full |
| Scenario 4 | UI / Regression | High | Full |
| Scenario 5 | UI / Negative | Medium | Full |
| Scenario 6 | UI / Edge Case | Medium | Full |
| Scenario 7 | UI / Edge Case | Medium | Partial |
| Scenario 8 | UI / Accessibility | Low | Full |
| Scenario 9 | UI / Functional | High | Full |
| Scenario 10 | UI / Functional | High | Full |

---

## 5. Dependencies

### External Dependencies
- UAT environment must be accessible
- Test credentials must be valid
- Network connection must be stable
- Application must be deployed

### Internal Dependencies
- .env file must be configured
- Playwright browsers must be installed
- Python dependencies must be installed
- Page objects must be implemented

---

## 6. Edge Cases Identified

1. **Selector Changes:** UI elements may have dynamic IDs/classes
2. **Loading Overlays:** Spinners may block interactions
3. **Modal Blocking:** Open modals may block other elements
4. **Strict Mode Violations:** Multiple elements with same text
5. **Network Latency:** UAT environment slower than dev
6. **Session Management:** Session expiry during test
7. **CSS Framework:** Material-UI specific patterns
8. **Viewport Issues:** Layout problems on different screen sizes

---

## 7. Success Criteria Summary

**Overall Success:**
- All critical scenarios pass
- No console errors
- Zero security vulnerabilities
- All components validated
- UAT badge visible throughout
- No sensitive data in URLs

**Failure Criteria:**
- Login fails with valid credentials
- Navigation broken
- Components missing
- Console errors present
- Security issues detected
- UAT badge missing

---

## 8. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| UAT environment down | Low | High | Pre-flight checks |
| Credentials expired | Medium | High | Regular credential rotation |
| UI changes break selectors | High | Medium | Multiple fallback selectors |
| Network issues | Medium | Medium | Retry logic, network waits |
| Session timeout | Medium | Low | Session management |

---

*Analysis completed using story-analysis.md framework*  
*Next Step: Generate test cases using testcase-generation.md approach*
