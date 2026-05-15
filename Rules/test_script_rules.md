# Test Script Rules

## Purpose
Define implementation standards for automation scripts that follow the framework rules.

## Template
- **Script Name**: Clear automation test identifier.
- **Objective**: Business validation performed by the script.
- **Page Objects Used**: Reusable page object classes.
- **Data Driven**: Test data definitions.
- **Preconditions**: Environment or setup requirements.
- **Test Steps**: High-level automation flow.
- **Assertions**: Expected outcomes and validation points.
- **Metadata**: Tags, owner, stability notes.

## Best Practice Example
- **Script Name**: test_login_valid_credentials
- **Objective**: Automate a successful login and dashboard landing validation.
- **Page Objects Used**:
  - `LoginPage`
  - `DashboardPage`
- **Data Driven**:
  - credential set: valid user from secure test data store
- **Preconditions**:
  - Application environment is available.
  - User account is provisioned.
- **Test Steps**:
  1. Launch browser and navigate to login page.
  2. Perform login through `LoginPage.login()`.
  3. Verify dashboard visible via `DashboardPage.is_displayed()`.
- **Assertions**:
  - URL contains `/dashboard`.
  - Welcome banner includes expected user name.
- **Metadata**:
  - Tags: login, regression, ui
  - Owner: qa-team
  - Stability: stable

## Coding Best Practices
- Use page object methods instead of low-level selectors in tests.
- Avoid fixed delays; use explicit waits.
- Keep test methods small and focused.
- Log meaningful step details and capture failure artifacts.
