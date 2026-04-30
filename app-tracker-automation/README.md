# App Tracker Automation Framework

A component-driven automation framework for insurance portal testing using Playwright, Python, and Pytest.

## Repository

**GitHub**: https://github.com/PriteshSDET/app-tracker-automation-MCP

## Structure

This framework follows a component-driven architecture with clear separation of concerns:

- **pages/**: Page Object Model classes
- **components/**: Reusable UI components
- **flows/**: Business logic flows
- **tests/**: Test cases organized by type
- **utils/**: Utility functions and helpers
- **fixtures/**: Pytest fixtures
- **data/**: Test data and configuration

## Getting Started

1. Clone repository:
   ```bash
   git clone https://github.com/PriteshSDET/app-tracker-automation-MCP.git
   cd app-tracker-automation-MCP
   ```

2. Install dependencies:
   ```bash
   pip install -r app-tracker-automation/requirements.txt
   playwright install
   ```

3. Configure environment variables in `app-tracker-automation/.env`:
   ```bash
   ADITYA_BIRLA_USER=your_username
   ADITYA_BIRLA_PASS=your_password
   ```

4. Run tests:
   ```bash
   $env:PYTHONPATH = ".\app-tracker-automation"; pytest "app-tracker-automation\tests\smoke\execute_login_tracker_test.py" --headed
   ```

## Recent Updates

- ✅ Integrated .env file for secure credential management
- ✅ Fixed 4 critical test execution errors
- ✅ Updated homepage component validation with Playwright locators
- ✅ Removed all hardcoded credentials from codebase
- ✅ Implemented multi-path .env loading strategy

## Documentation

See `docs/` folder for detailed documentation:
- [Onboarding Guide](docs/onboarding.md) - Setup and getting started
- [Framework Guide](docs/framework-guide.md) - Architecture and components
- [Runbook](docs/runbook.md) - Test execution instructions
- [Execution Guide](EXECUTION_GUIDE.md) - Specific test execution guide
