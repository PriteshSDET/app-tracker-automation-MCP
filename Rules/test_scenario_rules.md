# Test Scenario Rules

## Purpose
Capture complete business flows and the key variations needed to validate each capability.

## Template
- **Scenario Name**: Business flow name.
- **Objective**: What business outcome the scenario covers.
- **Primary Flow**: Main steps for the happy path.
- **Alternate Flows**: Variations or optional branches.
- **Negative Flows**: Error or validation conditions.
- **Coverage Notes**: Risk areas, data conditions, integrations.
- **Related Test Cases**: List of test cases mapped to this scenario.

## Best Practice Example
- **Scenario Name**: User login and session validation
- **Objective**: Ensure valid login and session behavior across success and failure conditions.
- **Primary Flow**:
  1. Navigate to login page.
  2. Submit valid credentials.
  3. Verify dashboard access.
- **Alternate Flows**:
  - Password reset link navigation.
  - Login with "Remember me" checked.
- **Negative Flows**:
  - Invalid password error message.
  - Locked account warning after failed attempts.
- **Coverage Notes**:
  - Verify session cookie expiration.
  - Confirm error text is accessible and localized.
- **Related Test Cases**:
  - Verify successful login with valid credentials
  - Verify login failure with invalid password
  - Verify password reset navigation
