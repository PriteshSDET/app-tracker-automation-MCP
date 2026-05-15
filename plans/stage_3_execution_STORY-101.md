# Stage 3 Execution Report: STORY-101

**Executor:** Agent-QA_Execution  
**Execution Timestamp:** 2026-05-15T15:45:00+05:30  
**Suite:** Regression target attempted; smoke-priority failures observed inside the same run  
**Req ID:** STORY-101  

## Status

**[BLOCKED / FAILED EXECUTION]**

The approved Stage 1B suite was executed under Stage 3. The first sandboxed run failed before browser startup due to Windows subprocess/named-pipe permission denial. The run was repeated outside the sandbox; Playwright launched, but the full regression attempt timed out after 10 minutes.

The escalated run wrote execution context to:

`rag/active/execution_logs/run_log_20260515_154452.json`

## Execution Summary

- Pytest command: `venv\Scripts\python.exe -m pytest tests\generated -q`
- Initial sandbox result: infrastructure failure before app access
- Escalated result: timed out after 10 minutes
- RAG-recorded results before timeout:
  - Passed: 0
  - Failed: 18
  - Remaining tests: not completed before timeout

## Recheck After Pytest/Pip Install

**Recheck Timestamp:** 2026-05-15T15:53:00+05:30

Tooling is now healthy:

- `pip 26.1.1`
- `pytest 9.0.3`
- `playwright 1.59.0`
- `python-dotenv 1.2.2`
- Pytest collection succeeds with all 39 generated tests.

A focused smoke rerun was executed:

`venv\Scripts\python.exe -m pytest tests\generated\test_app_tracker.py::TestAppTrackerPositive::test_TC_01_01_verify_eligible_dsf_access_from_leap -q`

Result:

- Normal sandbox run still fails before browser startup with `PermissionError: [WinError 5] Access is denied` during Playwright subprocess/named-pipe creation.
- Escalated run starts Playwright successfully, logs into LEAP, but fails because the expected App Tracker `main` element is not present.

Diagnostic navigation evidence:

- Final URL after `go_to_tracker_as(...)`: `https://leapuat.adityabirlasunlifeinsurance.com/uat/#/dashboard`
- Page title: `ABSLI | LEAP`

This confirms the current blocker is no longer missing pytest/pip. The active failure is that the flow remains on the LEAP dashboard instead of landing on the App Tracker application.

## New-Tab Flow Verification And Fix

**Verification Timestamp:** 2026-05-15T16:03:00+05:30

The requested flow is present in `Playwright_Framework/rag/recordings/APP TRACKER.JSON`.

Recorder evidence:

- LEAP dashboard navigation is recorded.
- Menu dropdown click is recorded using `span.MuiIconButton-label > span > span`.
- Application Tracker menu item click is recorded using `aria/Application Tracker`, `li:nth-of-type(2)`, and `xpath//*[@id="user-menu"]/div[3]/ul/li[2]`.
- The App Tracker target is recorded as `https://onboarding-uat.adityabirlasunlifeinsurance.com/app-tracker/applications`.
- A direct App Tracker navigation step is also present later in the recording with title `App Tracker`.

Root cause:

- The RAG flow was not missing.
- The Stage 1B helper clicked `Application Tracker`, then checked `context.pages` after the fact.
- The browser opens App Tracker in a new tab, so the helper needed to wrap the click with Playwright `expect_page`.

Fix applied:

- `tests/generated/app_tracker_base.py` now captures the new tab with `self.page.context.expect_page(...)`.
- The helper updates both `self.page` and `self.base.page` to the new App Tracker tab.

Verification after fix:

`venv\Scripts\python.exe -m pytest tests\generated\test_app_tracker.py::TestAppTrackerPositive::test_TC_01_01_verify_eligible_dsf_access_from_leap -q`

Result:

- `1 passed in 8.44s`
- RAG log: `rag/active/execution_logs/run_log_20260515_160254.json`

## Latest RAG Debug Pass

**Debug Timestamp:** 2026-05-15T16:30:00+05:30

Latest execution logs reviewed:

- `rag/active/execution_logs/run_log_20260515_162213.json`
- `rag/active/execution_logs/run_log_20260515_161558.json`

Both logs recorded:

- Passed: 5
- Failed: 9

Primary failures were automation precision issues, not missing pytest/pip:

- Search tests used the ARIA placeholder locator while the current page exposes the recorder-backed generic `input` selector.
- Text assertions matched hidden duplicate nodes before visible table rows.
- Pagination ARIA selectors resolved to duplicate elements and needed CSS selectors from the recorder.
- Filter `Clear All` detached/re-rendered during click and needed a more stable force-click after the popover opened.
- Some story text expectations were stale compared with current App Tracker UI, for example `App. No.` and `Download 10 Records`.

Fixes applied:

- Search fields now use the recorder-backed `input` selector.
- Search tests use live valid values from the visible first row instead of stale hardcoded values.
- Text assertion helper now scans for a visible matching node before failing.
- Pagination uses CSS selectors from `APP TRACKER.JSON`.
- Stage/status filter apply and clear flows now use recorded popover selectors.
- Additional previously skipped cases were converted to real checks where valid RAG selectors exist:
  - status filter apply
  - status filter removal
  - malformed search safety
  - invalid filter plus no-result search
  - browser Back control
  - menu/search/drawer workflow using recorded close selector

Remaining skips are intentionally retained where valid executable support is still missing, such as Support Officer credentials, Date Range/Role filters, sort-header selectors, service failure simulation, stale-session setup, permission revocation setup, duplicate dataset injection, and premium anomaly data injection.

Verification after edits:

- Python compile: PASS
- Pytest collection: PASS
- Collected tests: 39

The focused browser rerun for the four patched failures was requested, but escalation approval was declined, so no post-fix browser execution result was produced for those cases in this pass.

## RCA

**Primary RCA Category:** `FRAMEWORK_OR_ENVIRONMENT_BLOCKER`

The first execution attempt failed with:

`PermissionError: [WinError 5] Access is denied`

This occurred while Playwright attempted to create its driver subprocess/named pipe. That was not an application failure.

**Secondary RCA Category:** `APP_TRACKER_LANDING_OR_SESSION_FLOW_UNSTABLE`

After escalation, the browser execution reached the test flow, but the expected App Tracker dashboard DOM was not found. Representative failures:

- `TC-01-01` and `TC-01-02`: `main` was not visible after LEAP menu navigation.
- `TC-03-01`: `Search by App No.` field was not available.
- `TC-05-01`: expected policy list columns such as `App.No` were not available.
- `TC-06-01`: first policy row selector `tr:nth-of-type(1) > td.sticky` was not available.
- `TC-01-04` and `TC-01-05`: restricted-role tests found `Application Tracker` visible in the user menu.

These failures indicate that the suite did not reliably land on the App Tracker dashboard state captured in the RAG recording, or the role/session state differs from the audited assumptions.

Latest verification confirms the LEAP-to-App-Tracker new-tab handoff works after the `expect_page` helper fix. The original blocker was generated helper logic, not missing RAG evidence.

## App Bug Alert Assessment

**Alert Status:** Conditional `[APP_BUG]` candidate, not automatically sent.

The restricted-role failures are business-critical if the login role data is correct and the `Application Tracker` menu entry is genuinely visible to SP/TPD/Banca/HDFC/Axis users. However, because the same run also shows dashboard landing instability, this should be confirmed with a focused RBAC rerun before alerting.

## Self-Healing Assessment

**Result:** No self-healing update applied.

The manifest threshold is 3 consecutive passes. This run had 0 recorded passes, so no navigation or locator pattern was promoted as stable. `config/mcp_stable_patterns.json` was created with an empty `stable_patterns` list.

## Recommendations

1. Run a focused smoke rerun for only the five `[SMOKE-PRIORITY]` cases after confirming the active LEAP session and App Tracker redirect behavior.
2. Capture a fresh Chrome Recorder JSON for the current App Tracker landing path if the post-login redirect or menu structure has changed.
3. Confirm restricted-role credentials and manually verify whether `Application Tracker` is visible for SP, TPD, Banca, HDFC, and Axis users.
4. If restricted roles can access the menu after confirmation, raise an `[APP_BUG]` for RBAC leakage.
5. Add explicit smoke/sanity/regression pytest markers in Stage 1B generation so Stage 3 can execute suite slices without relying on title text.

## Orchestrator Instruction

Do not promote this run. Treat Stage 3 as blocked by execution/landing instability and loop findings back into locator/session stabilization before another executor run.
