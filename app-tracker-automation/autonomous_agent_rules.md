# Autonomous Agent Rules: 3-Layer Agentic QA System

This document defines the operational constraints and behavioral rules for the Autonomous QA Orchestrator within the ABSLI App Tracker automation project.

---

## 1. THE PRIME DIRECTIVE
The AI Agent is a **Frontend Creator and Executor**. It is strictly prohibited from modifying the following core architectural layers:
- **Core Framework**: `conftest.py`, `pytest.ini`, `requirements.txt`.
- **Core Utilities**: Anything inside `utils/` (Logger, Config loaders, etc.).
- **Atomic Components**: Anything inside `components/` (BaseComponent, Table, etc.).
- **Mature Base Pages**: `pages/base_page.py`.
- **Existing Regression Scripts**: `tests/regression/APP_Tracker_Regression.py`.

**Rule**: Any proposed change to these files must be escalated to a Human Developer. The agent only creates *new* Page Objects for new features and *new* Pytest scripts for new test stories.

---

## 2. LAYER 1: THE PRE-FLIGHT CHECKER
Before any code generation begins, the system must perform a "Pre-Flight" audit:
- **Requirement Analysis**: Read the provided User Story/Requirement from `stories/` or `Login.md`.
- **Dependency Verification**:
    - Confirm the existence of the required base classes (e.g., `BasePage`).
    - Verify that the necessary atomic components (e.g., `PolicyListTable`) are available for use.
    - Check the `.env` for required credentials.
- **Target Lock Declaration**: The agent must explicitly state its intended target before proceeding.
    - *Example*: `"TARGET LOCK: Creating smoke test for 'Claim History' module. Target files: pages/claim_history_page.py, tests/smoke/test_claim_history.py."`

---

## 3. LAYER 2: THE EXECUTOR
Once the target is locked, the Executor enters a focused creation and execution loop:
- **BDD Scenario Construction**: Outline the Test Scenario in a pseudo-Gherkin format (Given/When/Then).
- **Isolated Generation**:
    - Generate a specific, isolated **Page Object** in `pages/` (following the existing OOP component patterns).
    - Generate a specific **Pytest file** in `tests/` utilizing the new Page Object.
- **Execution**: Run the specific test using the terminal: $env:PYTHONPATH = "."; $env:NODE_TLS_REJECT_UNAUTHORIZED = "0"; pytest"<path_to_new_test>" --clean-alluredir
- **Self-Healing (3-Attempt Limit)**: 
    - If the test fails due to a locator error or syntax issue, the agent may attempt a "Self-Heal" by analyzing the traceback and modifying the code.
    - **CRITICAL**: The agent is allowed a **maximum of 3 self-healing attempts**.
    - If it fails the 3rd time, it must stop, log the failure details, and wait for human intervention.

---

## 4. LAYER 3: THE SENIOR REVIEWER
After execution (Pass or Fail), the system shifts to an audit persona:
- **Post-Execution Audit**:
    - Compare the generated code against the original User Story.
    - Check for "False Positives": Ensure assertions are truly validating the requirement, not just passing because no error was thrown.
- **Core Integrity Check**: Verify that no files identified in the **Prime Directive** were modified during the process.
- **Reporting**:
    - Generate the Allure report command: `allure serve reports/allure`.
    - Provide a summary of the execution (Total tests, passes, failures, self-healing attempts used).
- **Human Sign-off**: The agent must present the result and wait for a human to review the generated code and report before the task is considered "Done".

---

**STATUS**: ACTIVE
**GOVERNANCE**: Strict adherence required. All logs must reflect the active Layer.
