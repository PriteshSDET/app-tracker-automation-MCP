# Skill Database
*This document tracks advanced automation skills, best practices, and workarounds discovered during the ABSLI project.*

## 1. Playwright Check & Wait States
- **Wait States**: `wait_for(state="...")` only accepts `attached`, `detached`, `visible`, and `hidden`. It **does not** accept `enabled`. Trying to wait for `enabled` will crash the execution with a strict mode/invalid argument error.
- **Actionability**: Playwright automatically checks actionability (visible, stable, enabled) during a `.click()`. If it times out because a parent element is capturing the event or a React overlay is obscuring it, bypass it via `click(force=True)` rather than writing complex wait logic.

## 2. Optimizing Multi-Locator Fallbacks
When you have a list of fallback selectors for a single element (e.g. `['div[role="dialog"]', 'div[role="menu"]']`), looping through them with `wait_for(timeout=5000)` causes massive cumulative delays if the element is absent.
- **Skill**: Combine them into a single CSS OR string using commas.
- **Implementation**: `or_selector = ", ".join(selectors)` -> `page.locator(or_selector).first.wait_for(...)`. This delegates the matching to the browser engine, resolving instantly instead of cascading timeouts.

## 3. Handling Application State Mutation
Tests that interact with Search Bars or Filters mutate the underlying UI (e.g., filtering a table to 1 row). This breaks subsequent tests that expect default states (like Pagination testing).
- **Skill**: Enforce **Self-Cleaning Components**. If a test checks a filter box, it must immediately uncheck it before completing.
- **Architecture**: Always run Stateless/OOP tests *before* any legacy tests that permanently mutate the page state.

## 4. Headless Tab Navigation
- **Skill**: When navigating to a new tab inside an authenticated portal (like LEAP), do NOT use `window.open(url)`. It creates a fresh context without auth cookies, leading to a login redirect.
- **Implementation**: Always trigger the actual DOM link. If `link.click()` times out due to actionability, use `link.evaluate("el => el.click()")` or `link.click(force=True, modifiers=["Control"])`.

