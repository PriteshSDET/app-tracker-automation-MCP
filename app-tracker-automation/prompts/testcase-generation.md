# Test Case Generation Prompt

## Purpose
Generate comprehensive test cases from analyzed stories using learned patterns from previous projects.

## Input Format
- Analyzed story output
- Test scenarios list
- Business requirements
- Technical specifications
- Environment type (UAT/dev/production)

## Generation Guidelines

### 1. Test Case Structure
- Create positive and negative test cases
- Include boundary value testing
- Add error handling scenarios
- Define test data requirements
- Specify expected results

### 2. Environment-Aware Test Design
**For UAT Environments:**
- Use 15-second timeouts for all waits
- Include network idle waits before critical interactions
- Add element stability checks (attached, visible, enabled)
- Wait for loading overlays before clicks
- Use soft logging for optional components

**For Dev Environments:**
- Use 3-5 second timeouts
- Standard element waits
- Faster test execution

### 3. Component Criticality Classification
**Critical Components (Hard Failures):**
- Login authentication
- Data submission
- Critical navigation
- Payment processing

**Optional Components (Soft Warnings):**
- UI decorations
- Optional filters
- Non-critical buttons
- Display elements

### 4. Synchronization Patterns (Learned from Aditya Birla Project)
**Always Include:**
```python
# Before critical interactions
page.wait_for_load_state("networkidle", timeout=15000)

# Before element interactions
element.wait_for(state="attached", timeout=5000)
element.wait_for(state="visible", timeout=5000)
element.wait_for(state="enabled", timeout=5000)

# Before clicks on navigation elements
_wait_for_loading_overlay_to_disappear(page)
```

**Loading Overlay Detection:**
```python
def _wait_for_loading_overlay_to_disappear(self, page, timeout=5000):
    loading_selectors = [
        ".loading-overlay",
        ".spinner",
        ".progress-bar",
        "[class*='loading']",
        "[class*='spinner']",
        "[class*='overlay']",
        ".MuiCircularProgress-root",  # Material-UI
        ".MuiBackdrop-root"  # Material-UI
    ]
```

### 5. Selector Strategy Patterns
**Multiple Fallback Selectors:**
```python
element_selectors = [
    "button:has-text('Submit')",
    "[aria-label*='submit' i]",
    ".submit-button",
    "button[type='submit']",
    "input[type='submit']"
]

for selector in element_selectors:
    try:
        element = page.locator(selector).first
        if element.is_visible(timeout=3000):
            break
    except:
        continue
```

**Strict Mode Handling:**
```python
# Always use .first when multiple elements might match
element = page.get_by_text("Submit").first
```

### 6. Test Phase Structure
**Three-Phase Pattern (Learned from Aditya Birla):**
- **Phase 1: Authentication** - Login, credential entry, verification
- **Phase 2: Navigation** - Menu clicks, page navigation, setup
- **Phase 3: Validation** - Component validation, data verification, interactions

### 7. Error Handling Strategy
**Soft Logging for Non-Critical:**
```python
try:
    # Validation
    logger.info("[PASS] Component validated")
except Exception as e:
    logger.warning(f"[WARN] Component validation skipped: {e}")
    errors += 1
```

**Hard Failures for Critical:**
```python
try:
    # Critical operation
    if not critical_condition:
        raise Exception("Critical failure")
except Exception as e:
    logger.error(f"[FAIL] Critical error: {e}")
    raise
```

### 8. CSS Framework Detection
**Material-UI Patterns:**
- Buttons: `.MuiButtonBase-root`, `.MuiIconButton-root`
- Dropdowns: `#mui-component-select-*`, `ul.MuiList-root[role='listbox']`
- Spinners: `.MuiCircularProgress-root`, `.MuiBackdrop-root`
- Containers: `.MuiBox-root.jss*`

**Bootstrap Patterns:**
- Buttons: `.btn`, `.btn-primary`
- Forms: `.form-control`, `.form-group`
- Modals: `.modal`, `.modal-dialog`

**Custom Frameworks:**
- Analyze HTML structure
- Identify class naming patterns
- Document specific selectors

## Output Format

### Test Case Template
```markdown
## Test Case: TC001 - [Title]

### Priority
High/Medium/Low

### Tags
smoke, regression, critical

### Preconditions
- User is logged in
- Dashboard is loaded
- Required data is available

### Test Steps
1. Navigate to [page]
2. Wait for network idle (15s)
3. Verify element is visible
4. Perform action
5. Wait for network idle (5s)
6. Verify result

### Expected Results
- Element is visible and actionable
- Action completes successfully
- Data is displayed correctly

### Test Data Requirements
- Valid credentials
- Test data sets
- Configuration values

### Error Handling
- If element not found: Log warning, continue
- If critical failure: Log error, fail test
- If timeout: Retry with longer timeout
```

## Anti-Patterns to Avoid

### ❌ Don't Use Static Timeouts
**Bad:** `page.wait_for_timeout(3000)`
**Good:** `page.wait_for_load_state("networkidle", timeout=15000)`

### ❌ Don't Assume Single Element Matches
**Bad:** `page.get_by_text("Submit")`
**Good:** `page.get_by_text("Submit").first`

### ❌ Don't Ignore Loading Overlays
**Bad:** Click directly without checking
**Good:** Wait for overlays to disappear

### ❌ Don't Use Hard Failures for Optional Components
**Bad:** `assert element.is_visible()`
**Good:** Soft logging with warnings

## Learned Patterns from Previous Projects

### Aditya Birla Project (April-May 2026)
**Key Learnings:**
- UAT requires 15-second timeouts (not 3-5s)
- Network idle waits prevent flaky tests
- Loading overlays block interactions
- Multiple selector fallbacks improve reliability
- Soft logging for optional components
- CSS injection fixes layout issues
- Material-UI has predictable class patterns

**Apply These Patterns:**
- Always use network idle waits in UAT
- Check for Material-UI classes if present
- Use flexible selectors for dynamic UI
- Implement loading overlay detection
- Classify component criticality

## Continuous Improvement

### After Each Test Execution:
1. Document what worked well
2. Document what failed
3. Identify patterns
4. Update this prompt with learnings
5. Add to skills database

### Before Each New Project:
1. Review skills database
2. Identify relevant patterns
3. Apply appropriate strategies
4. Adjust for new environment
5. Document new learnings

---

*Last Updated: May 1, 2026 - Enhanced with Aditya Birla project learnings*
