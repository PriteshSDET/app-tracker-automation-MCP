# Test Case Rules

## Purpose
Define a standardized test case structure that is easy to review, execute, and maintain.

## Template
- **Title**: Clear, business-focused test name.
- **Description**: Short summary of what the test validates.
- **Preconditions**: System state or data required before execution.
- **Steps**: Numbered, atomic actions.
- **Expected Result**: Specific observable outcome.
- **Test Data**: Input values or data sets referenced by the test.
- **Priority**: High / Medium / Low.
- **Tags**: Component, regression, smoke, security, etc.

## Best Practice Example
- **Title**: Verify successful login with valid credentials
- **Description**: Confirm that a user can sign in and reach the dashboard.
- **Preconditions**:
  1. User account exists with active status.
  2. Login page is reachable.
- **Steps**:
  1. Navigate to the login page.
  2. Enter valid username.
  3. Enter valid password.
  4. Click Sign In.
- **Expected Result**:
  - User is redirected to the dashboard.
  - Welcome banner displays the user's name.
- **Test Data**:
  - username: `test.user@example.com`
  - password: `ValidP@ssw0rd`
- **Priority**: High
- **Tags**: login, regression, smoke

## Review Notes
- Keep one business validation per test case.
- Avoid technical implementation details in the steps.
- Ensure expected results are measurable and precise.
