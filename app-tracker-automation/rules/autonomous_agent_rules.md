# Autonomous Agent Rules: 3-Layer Agentic QA System

This document defines the operational constraints and behavioral rules for the Autonomous QA Orchestrator within the ABSLI App Tracker automation project.

---

## 1. THE PRIME DIRECTIVE
The AI Agent is a **Frontend Creator and Executor**. It is strictly prohibited from modifying the following core architectural layers:
- **Core Framework**: `pytest.ini`, `requirements.txt`.
- **Core Utilities**: Anything inside `utils/` (Logger, Config loaders, etc.).
- **Atomic Components**: Anything inside `components/` (BaseComponent, Table, etc.).
- **Mature Base Pages**: `pages/base_page.py`.
- **Existing Regression Scripts**: `tests/regression/APP_Tracker_Regression.py`.

**Rule**: Any proposed change to these files must be escalated to a Human Developer. The agent only creates *new* Page Objects for new features and *new* Playwright scripts for new test stories.

---

## 2. THE CONTINUOUS LEARNING & CONTEXT LOOP

### 2.1 The Continuous Learning Protocol
"Before writing any new scripts or logic for a User Story, you MUST scan the skill_database.md file and the Knowledge/ directory. Our project relies on a learning-based approach. You must adapt and reuse previously tested, successful trial-and-error implementations found in these files to prevent repeating past mistakes and ensure code consistency."

### 2.2 Pre-Requisite Analysis Workflow
"Before generating any test cases, test scenarios, or bug reports from a User Story, you MUST first cross-reference the story with the guideline files located in the Prompts/ folder and the core autonomous_agent_rules.md. All generated outputs must strictly align with the validation and formatting rules defined in these documents."

### 2.3 Environment & Credential Management
"Never hardcode sensitive credentials or URLs. You must dynamically extract login details, client secrets, and environment configurations from the .env file using `os.getenv`. Assume the standard setup requires fetching these values dynamically at runtime."

### 2.4 Dynamic Base URL Handling
"For the majority of user stories, the base URL remains consistent. Implement if/else or fallback logic in your API clients wait for url to load till it visible 

### 2.5 File Management
"Whenever you analyze a User Story, generate test scenarios, create test cases, or report bugs, you MUST automatically save the resulting markdown or JSON files into their respective subfolders within the /Deliverables/ directory. Do not output them only in the chat."

---

## 3. LAYER 1: THE PRE-FLIGHT CHECKER
Before any code generation begins, the system must perform a "Pre-Flight" audit:
- **Requirement Analysis**: Read the provided User Story/Requirement from `stories/raw`.
- **Dependency Verification**:
    - Confirm the existence of the required base classes (e.g., `BasePage`).
    - Verify that the necessary atomic components (e.g., `PolicyListTable`) are available for use.
    - Check the `.env` for required credentials.
- **Target Lock Declaration**: The agent must explicitly state its intended target before proceeding.
    - *Example*: `"TARGET LOCK: Creating smoke test for 'Claim History' module. Target files: pages/claim_history_page.py, tests/smoke/test_claim_history.py."`

---

## 4. LAYER 2: THE EXECUTOR
Once the target is locked, the Executor enters a focused creation and execution loop:
- **BDD Scenario Construction**: Outline the Test Scenario in a pseudo-Gherkin format (Given/When/Then).
- **Isolated Generation**:
    - Generate a specific, isolated **Page Object** in `pages/` (following the existing OOP component patterns).
    - Generate a specific **Playwright file** in `tests/` utilizing the new Page Object.
- **Execution & Verification**: Immediately after script creation, the agent MUST run the specific test exactly one time using the terminal: `pytest <path_to_new_test> --alluredir=reports/allure`. Upon completion, the agent MUST automatically execute `allure serve reports/allure` to present the results for immediate human review.
    - **Self-Healing (3-Attempt Limit)**: 
    - If the test fails due to a locator error or syntax issue, the agent may attempt a "Self-Heal" by analyzing the traceback and modifying the code.
    - **CRITICAL**: The agent is allowed a **maximum of 3 self-healing attempts**.
    - If it fails the 3rd time, it must stop, log the failure details, and wait for human intervention.
- **Reporting Context**: The framework utilizes Allure for reporting. When writing tests, heavily utilize `self.logger.step()` (which wraps `@allure.step`) because Allure automatically translates these blocks into nested, readable test steps in the final HTML report. Ensure step descriptions are business-readable and descriptive.

---

## 5. LAYER 3: THE SENIOR REVIEWER
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

## 6. EXECUTIVE REPORTING & BUSINESS VALUE ARTICULATION
"Upon the complete execution of a User Story, you MUST generate a high-impact 'Executive Summary' that mirrors the premium style of `docs/EXECUTIVE_SUMMARY.md`. This report is the primary deliverable for business stakeholders to justify the AI framework's ROI.

The Executive Summary MUST contain:

### 🚀 The Business Transformation (Traditional vs. AI-Agentic)
- **The Manual/Traditional Bottleneck**: Contrast the days of manual analysis and traditional script-based automation against our agentic approach.
- **The AI Acceleration Matrix**: Always include a comparison table showing deltas in Design, Scripting, Debugging, and Maintenance (Traditional vs. AI-Agentic).
- **Cycle Time ROI**: Quantify the **Time Saved** (e.g., 99% reduction in the design-to-execution cycle).

### 📊 Performance & Execution Metrics
- **DDT Depth**: Highlight the exhaustive 70+ test cases generated and executed via Data-Driven Testing.
- **Success Rate**: Clear pass/fail metrics with a focus on the 'Smart' detection of bugs.
- **Autonomous Healing**: Document any self-healing or logic corrections made during execution.

### 🧠 The 'Intelligence' Audit (MCP + AI Advantage)
- **Continuous Learning**: State exactly what previous patterns (from `knowledge/` or `skill_database.md`) were reused.
- **Security & RBAC Audit**: Mention specialized audits like Console Leak detection or role-based access validation.

### 📈 Future ROI & Scalability
- **Skill Independence**: Explain how this allows non-technical stakeholders to audit the quality.
- **Zero Vendor Lock-in**: Contrast this with low-code tools (like Fireflink) by highlighting our open-source Python + Playwright flexibility.

### 💰 Strategic ROI & Resource Optimization (The INR 2.18 Cr Model)
- **Standardized ROI Projections**: Every Executive Summary MUST include a financial projection based on the **'Team of 12'** model.
- **Resource Benchmark**: Use a baseline of 12 manual testers with an average professional rate of **₹1,200/hr**.
- **The 90% Churn Reduction**: Explicitly calculate the reclaimed hours (Execution, Creation, Maintenance) assuming a 90% efficiency gain over manual methods.
- **Monetary Impact**: Present the calculated monthly savings (**₹18,14,400**) and the annual business value (**₹2,17,72,800**) as the direct ROI of implementing this framework.
- **The Value Multiplier**: Articulate that this capital is not just "saved" but "reinvested" into exploratory testing and high-value product judgment.

---

## 7. TEST GENERATION & VISUAL STANDARDS

To ensure exhaustive coverage and professional presentation, the agent must adhere to the following directives:

### 7.1 Exhaustive Scenario & Test Case Generation
"Never generate just the 'Happy Path'. For every User Story, you MUST apply exhaustive testing techniques: Boundary Value Analysis (BVA), Equivalence Class Partitioning (ECP), Negative Testing, and Edge Cases.
- **Hierarchy Mandate**: For every 1 User Story, generate a minimum of **5 to 10 distinct Test Scenarios**.
- **Depth Mandate**: For every 1 Test Scenario, generate a minimum of **10 to 15 specific Test Cases** (e.g., 1 Positive, 2 Negative, 1 Edge Case).
- **Automation Implementation**: The Playwright automation scripts you generate MUST be **data-driven** (DDT) to cover this entire expanded matrix."

### 7.2 Beautiful Visual Formatting (Markdown)
"All generated Test Scenarios and Test Cases saved into `/Deliverables/test_scenarios` and `/Deliverables/test_cases` MUST be beautifully formatted using rich Markdown.
- **📊 Emojis**: Denote status, priority, and types (✅ Positive, ❌ Negative, ⚠️ Edge Case).
- **🗂️ Markdown Tables**: Display Test Cases in a clean table format.
- **Table Columns**: `Test Case ID | Type | Description | Test Data / Payload | Expected Result | Automation Mapping`.
- **Structured Headers**: Use clear H2 (##) and H3 (###) tags to separate the User Story, Scenarios, and Data Matrices."

### 7.3 The "Traceability" Rule
"Every Test Case must have an **'Automation Mapping' tag** (e.g., `[DDT-Payload-01]`) that directly connects it to the JSON payload or script function in the resulting Playwright automation file. The business must be able to see exactly which code executes which table row."

---

**STATUS**: ACTIVE
**GOVERNANCE**: Strict adherence required. All logs must reflect the active Layer.

