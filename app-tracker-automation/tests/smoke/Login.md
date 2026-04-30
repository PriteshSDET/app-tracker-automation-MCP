# Test Plan: Login & App Tracker Navigation

## 1. Test Case Overview
**Title:** End-to-End Authentication to Application Tracker  
**Module:** UAT Portal / Onboarding  
**Environment:** Aditya Birla Sun Life (UAT)  
**Goal:** Verify successful login, dashboard rendering, and redirection to the 'Application Tracker' workspace.

## 2. Prerequisites
- **Browser:** Google Chrome (Latest Stable)
- **Network:** Stable connection (Simulate Throttled 4G for perf testing optional)
- **Credentials:** Valid UAT Admin ID and Password
- **Cache:** Browser cache cleared (First-run scenario)

## 3. Test Data Setup
| Field | Value Source |
| :--- | :--- |
| **Login ID** | Loaded from `.env` file (`ADITYA_BIRLA_USER`) |
| **Password** | Loaded from `.env` file (`ADITYA_BIRLA_PASS`) |

**Note**: Credentials are loaded using multi-path .env loading strategy for flexibility across execution contexts.

## 4. Step-by-Step Execution

### Phase 1: Navigation & Authentication
| Step # | User Action | Expected Result | Validation Checkpoint |
| :--- | :--- | :--- | :--- |
| **1** | Initialize browser with full-screen mode and inject layout CSS | Browser opens maximized. CSS styles injected to prevent viewport issues. | Browser Configuration, Layout Stability |
| **2** | Navigate to `leapuat.adityabirlasunlifeinsurance.com/uat/#/login` | Page loads within <2s. Header displays red branding (`Aditya Birla Capital`). Centered login form visible. **Blue "UAT" badge fixed bottom-left.** URL contains `#/login`. | Layout, Branding, Env Badge, URL |
| **3** | Enter credentials from .env file | Credentials loaded from `ADITYA_BIRLA_USER` and `ADITYA_BIRLA_PASS`. Text populates. Password masks as bullets. | Credential Loading, Input Masking |
| **4** | Click `LOGIN >` button | Button clicks (active state). POST request fires. Redirect triggers immediately. | CTA Response, Network Call |
| **5** | Observe Post-Login Transition | Redirects to `/dashboard` (`leapuat...#\/dashboard`). Page renders without flicker. Session token persists. | Routing Flow, Session Mgmt |

### Phase 2: App Tracker Setup
| Step # | User Action | Expected Result | Validation Checkpoint |
| :--- | :--- | :--- | :--- |
| **6** | Click `MENU ▾` button (Top Right) using precise selector `button.menu-button[aria-label='menu']` | Menu button clicked. Dropdown expands cleanly. Items: `Help`, `Application Tracker`, `Approvals`, `Logout`. | Navigation Menu, Alignment |
| **7** | Click `Application Tracker` link | **URL Changes** to: `onboarding-uat.adityabirlasunlifeinsurance.com/app-tracker/applications`.<br>**New tab opens** for Application Tracker. | Deep Linking, Domain Routing, Tab Handling |
| **8** | Switch to Application Tracker tab and wait for load | Application Tracker page loads. URL contains `app-tracker/applications`. | Tab Switching, Page Load |

### Phase 3: Component Validation
| Step # | User Action | Expected Result | Validation Checkpoint |
| :--- | :--- | :--- | :--- |
| **9** | Validate Filter Components | **Filter Button**: Visible and clickable.<br>**Title**: "Policy List" displayed.<br>**Search Box**: Text input field (not image) with placeholder.<br>**Date Filter**: "Prev + Current Month" option.<br>**Filter Chips**: Status tags (Pending, Approved, etc.).<br>**Download Button**: Export functionality.<br>**Sort Dropdown**: Clickable with modal closure handling. | Component Presence, Functionality |
| **10**| Validate Table Components | **Table Header**: Columns visible (App.No, Proposer Name, Plan Name, Modal Premium, Policy Status).<br>**Table Rows**: Data rows displayed using `.MuiBox-root.jss138, tbody tr` selector.<br>**Plan Name**: Extracted using `.first` selector to avoid strict mode violation.<br>**Premium Amount**: Contains currency symbol (₹).<br>**Status Tag**: Status indicators (Pending, etc.).<br>**Sorting Indicator**: SVG icons in table headers.<br>**Row Interaction**: Rows clickable with `force=True`. | Data Structure, Element Extraction, Interaction |
| **11**| Check Global Consistency | `UAT` badge persists in bottom-left corner across all views. No sensitive data leaks in URL fragments. | Security, Environment Safety |

## 5. Pass/Fail Criteria
- **PASS:** Zero console errors; credentials loaded from .env; seamless routing between Login → Dashboard → Tracker; UI matches visual design specs; UAT badge visible throughout; all component validations pass (filters and table).
- **FAIL:** Credentials not loaded from .env; blank screens during transition; broken menu links; missing components (e.g., missing UAT badge); failure to redirect to correct domain; component validation failures.

## 6. Edge Cases & Negative Testing
1.  **Invalid Credentials:** Expect inline error message, red borders on inputs, focus reset to first field.
2.  **Session Expiry:** Refresh on `/app-tracker` while logged out → Should auto-redirect to `/login`.
3.  **Network Failure:** Simulate offline mode on click → Should show error toast/alert and not hang indefinitely.
4.  **Keyboard Navigation:** Tab through all elements → Ensure visible focus rings (no mouse-only navigation).
5.  **Sort Dropdown Timeout:** Open filter modal blocks sort button → Test uses Escape key to close modals before clicking sort.
6.  **Search Box Image Input:** Targeting magnifying glass instead of text input → Test uses `input[type="text"]` selector.
7.  **Table Strict Mode Violation:** Multiple `.plan-name` elements → Test uses `.first` selector to target first element only.
8.  **.env File Not Found:** Credentials not loaded → Test uses multi-path loading strategy to find .env file.