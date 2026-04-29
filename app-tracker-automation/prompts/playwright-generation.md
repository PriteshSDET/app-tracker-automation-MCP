# Playwright Code Generation Prompt

## Purpose
Generate Playwright test code from test cases.

## Framework Standards
- Use Page Object Model pattern
- Implement component-driven architecture
- Follow Python naming conventions
- Include proper error handling
- Add comprehensive logging

## Code Structure
```python
import pytest
from pages.login_page import LoginPage
from components.base_component import BaseComponent

class TestScenario:
    def test_method_name(self, page, config, logger):
        # Test implementation
        pass
```

## Best Practices
- Use descriptive test names
- Include setup and teardown
- Add assertions for validation
- Implement wait strategies
- Handle dynamic elements
