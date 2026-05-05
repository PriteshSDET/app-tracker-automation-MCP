# Regression Suite Learnings: App Tracker Flow & State Management

**Date**: May 04, 2026
**Context**: Fixing timeout and target-page-closed errors during the integration of new component-driven utility classes into `APP_Tracker_Regression.ts`.

### 1. Tab Navigation & Authentication Persistence
When attempting to open the Application Tracker in a new tab, using a manual JavaScript fallback like `window.open('https://onboarding-uat.adityabirlasunlifeinsurance.com/app-tracker/applications', '_blank')` causes a loss of the LEAP authentication session (cookies are not passed). This results in the page redirecting to the login screen, breaking all subsequent validations with "target page closed" errors.
*   **Best Practice**: Always trigger the new tab via the actual DOM element using `link.click()`, `link.evaluate("el => el.click()")`, or `link.click(modifiers=["Control"])` to preserve the browser context and session cookies.

### 2. Unicode Logging Crashes (Windows `cp1252`)
When scraping currency strings from the UI (like `₹ 30,318.00`), the Indian Rupee symbol (`₹` or `\u20b9`) cannot be encoded by standard Windows terminals running the default `cp1252` encoding. Attempting to pass this string to `self.logger.info()` will instantly crash the TypeScript execution with a `UnicodeEncodeError`.
*   **Best Practice**: Always sanitize text extracted from the UI that might contain special symbols before logging it.
    *   *Example*: `premium = premium.replace('\u20b9', 'Rs.').replace('₹', 'Rs.')`
    *   *Example 2*: Ensure arrows like `→` (`\u2192`) in static logger strings are replaced with ASCII equivalents like `->`.

### 3. Modals/Drawers Blocking the UI Thread
During regression, certain actions (like validating the Application Number Search) click on table rows, which triggers a right-side "Detail Drawer". If this drawer is left open, Playwright cannot interact with the underlying table, filter chips, or navigation bar, leading to `Timeout 3000ms exceeded` errors for subsequent tests.
*   **Best Practice**: Clean up the UI state immediately. Use robust locators to close drawers. If generic selectors fail, use `button:has(svg path[d*='specific-svg-path'])` to explicitly target the close button's exact graphic.

### 4. Test Phase Ordering & State Mutation
Tests that mutate the state of the page (e.g., leaving a search string in the search bar, which filters a 10-row table down to 1 row) will break any subsequent tests that rely on the default state (e.g., pagination tests that expect multiple pages, or chip tests that expect default counts).
*   **Best Practice**: 
    1.  Run **Stateless / Self-Cleaning** Component Utility tests *first* (they interact with the UI but reset it before finishing).
    2.  Run **State Mutating** Legacy tests *last* so their residual effects (active searches) do not corrupt the environment for other validations.

### 5. Playwright Wait States & Invalid Arguments
Playwright's `wait_for(state="...")` ONLY accepts four specific states: `attached`, `detached`, `visible`, and `hidden`.
*   **The Bug**: Using `btn.wait_for(state="enabled")` will crash the test script with a `StrictMode` or `Invalid Argument` exception.
*   **Best Practice**: If you need to ensure an element is actionable, Playwright's `click()` method does this automatically. If strict actionability checks are timing out due to minor UI overlaps (common in Radix/MUI component wrappers), bypass it safely using `btn.click(force=True)`.

### 6. Optimizing Locator Delays with OR Selectors
When falling back across multiple selectors (e.g., waiting for a dialog to appear using an array of 5 different potential CSS selectors), placing them in a `for` loop with a `try/except` block and a 5-second `wait_for` timeout will cascade into massive delays (e.g., 5s x 6 selectors = 30-second delay) if the element is slightly delayed or absent.
*   **Best Practice**: Use Playwright's native comma-separated OR selector engine. Combine your array into a single string: `or_selector = ", ".join(SELECTOR_ARRAY)`. Then do `page.locator(or_selector).first.wait_for(timeout=5000)`. This queries all selectors simultaneously and resolves instantly, eliminating false timeout cascades.

