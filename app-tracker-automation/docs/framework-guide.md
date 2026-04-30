# Framework Guide

## Overview

The App Tracker Automation Framework is a component-driven automation framework designed for insurance portal testing using Playwright, Python, and Pytest.

## Architecture

### Component-Driven Design

The framework follows a component-driven architecture with clear separation of concerns:

- **Pages/**: Page Object Model classes representing application pages
- **Components/**: Reusable UI components (dropdowns, tables, search boxes)
- **Flows/**: Business logic flows that orchestrate page interactions
- **Locators/**: Centralized element locators for maintainability
- **Utils/**: Utility functions and helper classes
- **Fixtures/**: Pytest fixtures for test setup and teardown

### Key Components

#### Base Classes
- `BasePage`: Common functionality for all page objects
- `BaseComponent`: Common functionality for all UI components

#### Page Objects
- `LoginPage`: Authentication functionality
- `DashboardPage`: Main dashboard interactions
- `TrackerPage`: Application tracking functionality

#### UI Components
- `Dropdown`: Select/dropdown interactions
- `Table`: Data table operations
- `SearchBox`: Search functionality
- `BaseComponent`: Common functionality for all UI components

#### Business Flows
- `LoginFlow`: Complete authentication workflow
- `TrackerFlow`: Application tracking workflow

## Test Organization

### Test Categories
- **Sanity**: Quick critical path validation
- **Smoke**: Core functionality testing
- **Regression**: Comprehensive feature testing
- **API**: Backend API testing

### Test Structure
```
tests/
├── sanity/     # Critical path tests
├── smoke/      # Core feature tests
├── regression/ # Full regression suite
├── api/        # API tests
├── generated/  # AI-generated tests
└── drafts/     # Work in progress
```

## Configuration

### Environment Setup
- `.env`: Environment variables (located at `app-tracker-automation/.env`)
- `data/env.json`: Environment configurations
- `utils/config.py`: Configuration management

**Environment Variables**:
```bash
ADITYA_BIRLA_USER=your_username
ADITYA_BIRLA_PASS=your_password
BASE_URL=https://leapuat.adityabirlasunlifeinsurance.com/uat/#/login
```

**Note**: The framework uses a multi-path .env loading strategy to ensure credentials are loaded correctly across different execution contexts.

### Test Data
- `data/users.xlsx`: User credentials
- `data/testdata.xlsx`: Test data sets
- `data/roles.json`: User roles and permissions

## Running Tests

### Prerequisites
```bash
pip install -r app-tracker-automation/requirements.txt
playwright install
```

### Test Execution
```bash
# Set PYTHONPATH and run all tests
$env:PYTHONPATH = ".\app-tracker-automation"; pytest

# Run specific test categories
$env:PYTHONPATH = ".\app-tracker-automation"; pytest -m sanity
$env:PYTHONPATH = ".\app-tracker-automation"; pytest -m smoke
$env:PYTHONPATH = ".\app-tracker-automation"; pytest -m regression

# Run with specific browser
$env:PYTHONPATH = ".\app-tracker-automation"; pytest --browser=chromium
$env:PYTHONPATH = ".\app-tracker-automation"; pytest --browser=firefox
$env:PYTHONPATH = ".\app-tracker-automation"; pytest --browser=webkit

# Generate reports
$env:PYTHONPATH = ".\app-tracker-automation"; pytest --html=reports/html/report.html --alluredir=reports/allure
```

## Reporting

### Report Types
- **HTML**: Interactive HTML reports
- **Allure**: Detailed test reports with screenshots
- **JUnit**: CI/CD integration
- **Excel**: Test summary reports

### Artifacts
- **Screenshots**: Passed/failed test screenshots
- **Videos**: Failed test video recordings
- **Traces**: Execution traces for debugging
- **Logs**: Detailed execution logs

## Best Practices

### Test Development
1. Use Page Object Model pattern
2. Implement component reusability
3. Follow naming conventions
4. Add comprehensive assertions
5. Include proper error handling

### Code Organization
1. Keep locators separate from page objects
2. Use descriptive test names
3. Group related tests together
4. Implement proper test fixtures
5. Add meaningful test documentation

### Maintenance
1. Regular test review and refactoring
2. Update locators when UI changes
3. Monitor test execution times
4. Review failure patterns
5. Keep documentation current

## Troubleshooting

### Common Issues
1. **Element not found**: Check locators and wait strategies
2. **Timeout errors**: Increase timeouts or adjust waits
3. **Flaky tests**: Review test isolation and timing
4. **Browser issues**: Update browser drivers

### Debugging Tools
1. Playwright Inspector: `playwright --debug`
2. Trace viewer: `playwright show-trace`
3. Screenshot analysis: Review captured screenshots
4. Log analysis: Check execution logs

## Extending the Framework

### Adding New Pages
1. Create page class inheriting from `BasePage`
2. Define page-specific locators
3. Implement page methods
4. Add to flows as needed

### Adding New Components
1. Create component class inheriting from `BaseComponent`
2. Implement component-specific methods
3. Add to relevant page objects
4. Update tests accordingly

### Adding New Flows
1. Create flow class in `flows/` directory
2. Implement business logic
3. Handle error scenarios
4. Add comprehensive logging

## Integration

### CI/CD Pipeline
- GitHub Actions workflows configured
- Multi-browser testing support
- Automated report generation
- Artifact storage and retention

### Test Management
- Test case tracking in `plans/`
- Coverage matrix in `plans/coverage-matrix.xlsx`
- Story analysis in `stories/`
- AI-generated prompts in `prompts/`
