# Test Case Generation Prompt

## Purpose
Generate exhaustive, professionally formatted test cases and scenarios from analyzed stories using high-coverage testing techniques and learned patterns.

## Input Format
- Analyzed story output
- Test scenarios list
- Business requirements
- Technical specifications
- Environment type (UAT/dev/production)

## Generation Guidelines

### 1. Exhaustive Coverage Mandate
- **No 'Happy Path' Only**: You MUST apply exhaustive testing techniques for every User Story.
- **Techniques**: Boundary Value Analysis (BVA), Equivalence Class Partitioning (ECP), Negative Testing, and Edge Cases.
- **Hierarchy Standard**: For every 1 User Story, generate a minimum of **5 to 10 distinct Test Scenarios**.
- **Depth Standard**: For every 1 Test Scenario, generate a minimum of **10 to 15 specific Test Cases**.
- **Data-Driven Priority**: All generated cases must be designed for **Data-Driven Testing (DDT)**.

### 2. Environment-Aware Test Design
**For UAT Environments:**
- Use 15-second timeouts for all waits.
- Include network idle waits before critical interactions.
- Add element stability checks (attached, visible, enabled).
- Wait for loading overlays before clicks.
- Use soft logging for optional components.

### 3. Component Criticality Classification
**Critical Components (Hard Failures):**
- Login authentication, Data submission, Critical navigation, Payment processing.

**Optional Components (Soft Warnings):**
- UI decorations, Optional filters, Non-critical buttons, Display elements.

### 4. Synchronization Patterns (Python/Playwright)
```python
# Before critical interactions
page.wait_for_load_state("networkidle", timeout=15000)

# Before element interactions
element.wait_for(state="visible", timeout=5000)

# Before clicks on navigation elements
self._wait_for_loading_overlay_to_disappear(page)
```

## Beautiful Visual Formatting (Markdown)

### Header Structure
Use clear **H2 (##)** for the User Story and **H3 (###)** for Scenarios.

### Test Case Table Standard
All test cases MUST be presented in a clean Markdown table with the following columns:
`Test Case ID | Type | Description | Test Data / Payload | Expected Result | Automation Mapping`

### Emojis for Visual Clarity
- ✅ **Positive**: Standard happy-path scenarios.
- ❌ **Negative**: Error handling and invalid input scenarios.
- ⚠️ **Edge Case**: Boundary values, unusual states, and rare conditions.
- 📊 **Status/Priority**: Use charts and icons to denote importance.

## Traceability & Automation Mapping
Every Test Case must have an **'Automation Mapping' tag** (e.g., `[DDT-Payload-01]`).
- This tag MUST directly connect the table row to a JSON payload index or a specific test function in the automation script.
- **Rule**: The business must be able to trace exactly which line of code validates which business requirement.

## Output Format Example

### ## User Story: [Story Title]

### ### Scenario 1: [Scenario Description]
| Test Case ID | Type | Description | Test Data / Payload | Expected Result | Automation Mapping |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TC-001 | ✅ Positive | [Description] | `{"key": "val"}` | [Result] | `[DDT-01]` |
| TC-002 | ❌ Negative | [Description] | `{"key": ""}` | [Error] | `[DDT-02]` |
| TC-003 | ⚠️ Edge | [Description] | `{"key": "LONG_STR"}` | [Handled] | `[DDT-03]` |

---
*Last Updated: May 6, 2026 - Upgraded to Exhaustive & Visual Standards*
