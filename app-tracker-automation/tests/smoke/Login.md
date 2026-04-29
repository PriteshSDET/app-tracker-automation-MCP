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
| Field | Value Placeholder |
| :--- | :--- |
| **Login ID** | `BR4641` |
| **Password** | `q7LD4$J!d7` |

## 4. Step-by-Step Execution

| Step # | User Action | Expected Result | Validation Checkpoint |
| :--- | :--- | :--- | :--- |
| **1** | Open browser & navigate to `leapuat.adityabirlasunlifeinsurance.com/uat/#/login` | Page loads within <2s. Header displays red branding (`Aditya Birla Capital`). Centered login form visible. **Blue "UAT" badge fixed bottom-left.** URL contains `#/login`. | Layout, Branding, Env Badge, URL |
| **2** | Click/Tab into `Login ID/AD/ID` field | Cursor focuses. Visible outline/border appears (WCAG focus state). | Accessibility, Input Focus |
| **3** | Enter valid credentials in both fields | Text populates. Password masks as bullets. No premature validation errors. | Input Masking, Binding |
| **4** | Click `LOGIN >` button | Button clicks (active state). POST request fires. Redirect triggers immediately. | CTA Response, Network Call |
| **5** | Observe Post-Login Transition | Redirects to `/dashboard` (`leapuat...#\/dashboard`). Page renders without flicker. Session token persists. | Routing Flow, Session Mgmt |
| **6** | Verify Dashboard UI Elements | **Header:** "Application List".<br>**Toolbar:** "Filter (+2)", "Sort: Modified".<br>**Data:** 4 rows with orange "Pending" dots.<br>**FAB:** "+ NEW APPLICATION" button (bottom right).<br>**Badge:** UAT tag remains visible. | Component Presence, State Indicators |
| **7** | Hover & Click `MENU ▾` (Top Right) | Dropdown expands cleanly. Items: `Help`, `Application Tracker`, `Approvals`, `Logout`. | Navigation Menu, Alignment |
| **8** | Click `Application Tracker` | **URL Changes** to: `onboarding-uat.adityabirlasunlifeinsurance.com/app-tracker/applications`.<br>**Header Shifts** to: `App Tracker` (Left) + Utility icons (Right). | Deep Linking, Domain Routing |
| **9** | Verify App Tracker Layout | **Title:** "Policy List".<br>**Meta Text:** "This view refreshes every 15 minutes." displayed below title.<br>**Controls:** Filter chips, Search bar, Date range picker active. | Content Hierarchy, Contextual Info |
| **10**| Validate Table Data Structure | Grid displays correct columns: `App.No`, `Proposer Name`, `Plan Name`, `Modal Premium`, `Policy Status`. Rows show "Pending" statuses correctly mapped. | Data Mapping, Column Headers |
| **11**| Check Global Consistency | `UAT` badge persists in bottom-left corner across all views. No sensitive data leaks in URL fragments. | Security, Environment Safety |

## 5. Pass/Fail Criteria
- **PASS:** Zero console errors; seamless routing between Login → Dashboard → Tracker; UI matches visual design specs; UAT badge visible throughout.
- **FAIL:** Blank screens during transition; broken menu links; missing components (e.g., missing UAT badge); failure to redirect to correct domain.

## 6. Edge Cases & Negative Testing
1.  **Invalid Credentials:** Expect inline error message, red borders on inputs, focus reset to first field.
2.  **Session Expiry:** Refresh on `/app-tracker` while logged out → Should auto-redirect to `/login`.
3.  **Network Failure:** Simulate offline mode on click → Should show error toast/alert and not hang indefinitely.
4.  **Keyboard Navigation:** Tab through all elements → Ensure visible focus rings (no mouse-only navigation).