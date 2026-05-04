# Test Plan: Login & App Tracker Navigation

## 1. Test Case Overview
**Title:** End-to-End Authentication and Component Validation
**Module:** UAT Portal / Onboarding  
**Environment:** Aditya Birla Sun Life (UAT)  
**Goal:** Verify successful login, redirection to the Application Tracker workspace, and robust validation of all object-oriented UI components (Navigation, Search, Filters, Tables, and Detail Drawers).

## 2. Prerequisites
- **Browser:** Playwright Chromium (Headless or UI mode)
- **Network:** Stable connection
- **Credentials:** Valid UAT ID and Password
- **Execution:** Run via `pytest tests/regression/APP_Tracker_Regression.py`

## 3. Test Data Setup
| Field | Value Source |
| :--- | :--- |
| **Login ID** | Loaded from `.env` file (`ADITYA_BIRLA_USER`) |
| **Password** | Loaded from `.env` file (`ADITYA_BIRLA_PASS`) |

## 4. Step-by-Step Execution

### Phase 1: Navigation & Authentication
| Step # | User Action | Expected Result | Validation Checkpoint |
| :--- | :--- | :--- | :--- |
| **1** | Initialize browser | Browser opens maximized. CSS layout fixes injected. | Browser Configuration, Layout Stability |
| **2** | Navigate to login URL | Page loads within <2s. | Network Idle, URL matching |
| **3** | Enter credentials from .env | Credentials populated in input fields. | Credential Loading |
| **4** | Click `LOGIN >` button | Form submits, post-login transition occurs. | Auth Persistence |

### Phase 2: App Tracker Setup
| Step # | User Action | Expected Result | Validation Checkpoint |
| :--- | :--- | :--- | :--- |
| **5** | Click Top-Right Menu `≡` | Menu opens cleanly without intercept issues. | Menu attachment/visibility |
| **6** | Click `Application Tracker` link | Employs a robust **3-attempt retry loop** using `click(force=True)`. If successful, the browser opens a new tab while preserving LEAP authentication cookies. | Context Persistence, Domain Routing |
| **7** | Capture New Tab | The script successfully captures the new `app-tracker/applications` tab. If it fails, falls back to scanning all open pages. | Browser Context Scanning |

### Phase 3: Component Utility Regression
*Note: Validations are executed using isolated, self-cleaning Python component classes to prevent state mutation.*

| Step # | Component | Validation Sequence | Resilience Mechanism |
| :--- | :--- | :--- | :--- |
| **8** | Top Navigation & Controls | Checks ABSLI Logo, Page Title, User Initials, Theme Toggle, and Download count.<br>**Interactions**: Toggles Theme (Dark/Light) and clicks Account Menu to verify dropdowns, then safely restores state. | Native Playwright interactions via `force=True` to bypass overlay strict mode crashes. |
| **9** | Filter & Search Bar | Checks Search Input visibility and Search Type labels.<br>**Interactions**: Injects text "LA" into the search field, verifies functionality, then clears text to preserve table state. | Component reset guarantees subsequent table validations are not broken by narrowed data. |
| **10**| Active Filter Chips | Parses active chips and dynamically counts them.<br>**Interactions**: Opens dropdown by clicking specific visible chip triggers (e.g. "Pending"), checks a new filter, then deliberately unchecks it. | Utilizes an "OR" CSS selector string (`", ".join(selectors)`) to instantly detect modal visibility without cascading 30-second delays. |
| **11**| Policy List Table | Validates header columns, ensures 10 rows are rendered, checks extracting application numbers and currency strings (Premium).<br>**Interactions**: Clicks a header column to test sorting and restores it. | Graceful currency parsing (`₹`) avoids Python cp1252 `UnicodeEncodeError` terminal crashes. |
| **12**| Pagination Footer | Checks if the dataset is single-page or multi-page.<br>**Interactions**: Skips interacting if only 1 page exists to prevent false positive failures. | Dynamic skip logic. |
| **13**| Detail Drawer | **Interactions**: Clicks the first table row to open the side-drawer. Validates Header, Proposer Name, Stages (PI Stage, Underwriting, etc.). Clicks specific stages in the stepper, then explicitly clicks the SVG 'X' button to close. | Explicit drawer closure using precise SVG paths prevents Playwright thread blocking on underlying components. |

## 5. Pass/Fail Criteria
- **PASS:** Zero timeouts. UI components successfully interacted with and states successfully reverted. Tab navigation succeeds without losing authentication.
- **FAIL:** `Timeout 10000ms exceeded`, target page closed errors, strict mode violations (`btn.wait_for(state="enabled")`), or corrupted table states causing pagination skips.

## 6. Known Edge Cases & Workarounds
1. **Playwright `enabled` Wait State:** Using `.wait_for(state="enabled")` causes invalid argument crashes. **Fix**: Use `.wait_for(state="visible")` and `.click(force=True)`.
2. **React Combobox Dropdowns:** Generic click events on MUI/React dropdown triggers often fail silently. **Fix**: Click the *actual visible element inside* the combobox (like the "Pending" chip text).
3. **Multi-Selector Timeouts:** Sequential `try/except` loops over locator selectors cascade into 30+ second delays. **Fix**: Combine them into a single `or_selector = ", ".join(selectors)`.
4. **Console Encoding Crashes:** Extracting `₹` symbols natively crashes Windows `cp1252` terminals. **Fix**: Wrap logging logic to catch or sanitize Unicode encodes.