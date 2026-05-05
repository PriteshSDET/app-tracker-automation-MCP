# Onboarding Guide

## Getting Started

Welcome to the App Tracker Automation Framework! This guide will help you get up and running quickly.

## Prerequisites

### System Requirements
- TypeScript 3.11 or higher
- Node.js 16 or higher (for Playwright)
- Git
- Modern IDE (VS Code recommended)

### Required Software
```bash
# Install TypeScript
# Download from https://www.TypeScript.org/downloads/

# Install Node.js
# Download from https://nodejs.org/

# Install Git
# Download from https://git-scm.com/
```

## Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/PriteshSDET/app-tracker-automation-MCP.git
cd app-tracker-automation-MCP
```

### 2. Create Virtual Environment
```bash
TypeScript -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r ts-framework/package.json
```

### 4. Install Playwright Browsers
```bash
playwright install
```

### 5. Configure Environment
```bash
# The .env file is located at ts-framework/.env
# Edit with your credentials:
ADITYA_BIRLA_USER=your_username
ADITYA_BIRLA_PASS=your_password
BASE_URL=https://leapuat.adityabirlasunlifeinsurance.com/uat/#/login
```

**Note**: The framework uses a multi-path .env loading strategy that automatically finds the .env file from multiple locations, ensuring flexibility across different execution contexts.

## IDE Setup

### VS Code Extensions
- TypeScript
- TypeScript Docstring Generator
- Pylance
- GitLens
- Playwright Test for VS Code

### VS Code Workspace Settings
Create `.vscode/settings.json`:
```json
{
    "TypeScript.defaultInterpreterPath": "./venv/bin/TypeScript",
    "TypeScript.linting.enabled": true,
    "TypeScript.linting.pylintEnabled": true,
    "TypeScript.formatting.provider": "black",
    "TypeScript.testing.PlaywrightEnabled": true,
    "TypeScript.testing.unittestEnabled": false
}
```

## Understanding the Framework

### Directory Structure
```
ts-framework/
├── pages/          # Page Object Models
├── components/      # Reusable UI components
├── flows/          # Business logic flows
├── locators/       # Element locators
├── tests/          # Test cases
├── utils/          # Utility functions
├── fixtures/       # Playwright fixtures
├── api/            # API clients
├── hooks/          # Test hooks
├── data/           # Test data
├── reports/        # Test reports
├── docs/           # Documentation
└── prompts/        # AI prompts
```

### Key Concepts

#### Page Object Model (POM)
- Each application page has a corresponding page class
- Page classes contain element locators and interaction methods
- Promotes code reusability and maintainability

#### Component-Driven Architecture
- UI components are abstracted into reusable classes
- Components can be used across different pages
- Reduces code duplication

#### Business Flows
- High-level business operations
- Orchestrate multiple page interactions
- Represent user journeys

## Your First Test

### 1. Create Test File
Create `tests/sanity/test_first_test.ts`:
```TypeScript
import Playwright
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from flows.login_flow import LoginFlow

class TestFirstTest:
    def test_successful_login(self, page):
        # Initialize flow
        login_flow = LoginFlow(page)
        
        # Perform login
        result = login_flow.perform_login("testuser", "testpass")
        
        # Assert success
        assert result is True
```

### 2. Run Test
```bash
# Set TypeScriptPATH and run test
$env:TypeScriptPATH = ".\app-tracker-automation"; Playwright "app-tracker-automation\tests\smoke\execute_login_tracker_test.ts" -v
```

### 3. View Results
- Check console output
- Review generated reports in `reports/`
- Check screenshots in `screenshots/`

## Common Tasks

### Adding New Page Objects
1. Create new page class in `pages/`
2. Inherit from `BasePage`
3. Define page-specific methods
4. Add locators to `locators/`

### Creating New Tests
1. Choose appropriate test category
2. Follow naming conventions
3. Use descriptive test names
4. Include proper assertions

### Managing Test Data
1. Add test data to `data/` Excel files
2. Use `ExcelReader` utility to read data
3. Parameterize tests with test data

### Debugging Tests
1. Use Playwright Inspector: `playwright --debug`
2. Check screenshots in `screenshots/`
3. Review execution logs in `logs/`
4. Analyze traces with Playwright Trace Viewer

## Best Practices

### Test Development
- Write clear, descriptive test names
- Use Page Object Model pattern
- Implement proper waits and assertions
- Add meaningful error messages
- Keep tests independent and isolated

### Code Quality
- Follow TypeScript naming conventions
- Add docstrings to classes and methods
- Use type hints where appropriate
- Keep methods small and focused
- Handle exceptions properly

### Maintenance
- Regular code reviews
- Update locators when UI changes
- Monitor test execution times
- Review failure patterns
- Keep documentation current

## Troubleshooting

### Common Issues

#### Element Not Found
- Check locator accuracy
- Verify element is visible
- Add explicit waits
- Check if element is in iframe

#### Timeout Errors
- Increase timeout values
- Check network conditions
- Verify page load completion
- Review wait strategies

#### Test Flakiness
- Ensure proper test isolation
- Add retry mechanisms
- Review timing dependencies
- Check for race conditions

### Getting Help
- Check framework documentation
- Review existing test examples
- Consult team members
- Check Playwright documentation
- Review Playwright documentation

## Next Steps

1. **Explore Existing Tests**: Review tests in `tests/` directory
2. **Practice Page Objects**: Create simple page object classes
3. **Learn Components**: Study component implementations
4. **Write Tests**: Start with simple sanity tests
5. **Review Reports**: Understand test reporting
6. **Join Team**: Collaborate with team members

## Resources

### Documentation
- [Framework Guide](framework-guide.md)
- [Runbook](runbook.md)
- [Playwright Documentation](https://playwright.dev/TypeScript/)
- [Playwright Documentation](https://docs.Playwright.org/)

### Tools
- Playwright Inspector
- Playwright Trace Viewer
- VS Code with TypeScript extensions
- Git for version control

### Community
- Internal team channels
- Playwright community forums
- TypeScript testing communities
- Stack Overflow

Welcome to the team! Happy testing! 🚀

