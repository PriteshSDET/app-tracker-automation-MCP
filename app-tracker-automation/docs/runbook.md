# Runbook

## Test Execution Guide

This runbook provides step-by-step instructions for running tests in different scenarios.

## Quick Start

### Run All Tests
```bash
# Set PYTHONPATH and run all tests
$env:PYTHONPATH = ".\app-tracker-automation"; pytest
```

### Run Specific Test Categories
```bash
# Sanity tests (critical path)
$env:PYTHONPATH = ".\app-tracker-automation"; pytest -m sanity

# Smoke tests (core features)
$env:PYTHONPATH = ".\app-tracker-automation"; pytest -m smoke

# Regression tests (full suite)
$env:PYTHONPATH = ".\app-tracker-automation"; pytest -m regression

# API tests
$env:PYTHONPATH = ".\app-tracker-automation"; pytest -m api
```

## Environment Setup

### Local Development
```bash
# Set PYTHONPATH and environment
$env:PYTHONPATH = ".\app-tracker-automation"; $env:ENVIRONMENT="dev"; pytest --env=dev
```

### CI/CD Pipeline
```bash
# Set PYTHONPATH and run with headless browser
$env:PYTHONPATH = ".\app-tracker-automation"; pytest --headed=false

# Generate reports
$env:PYTHONPATH = ".\app-tracker-automation"; pytest --html=reports/html/report.html --alluredir=reports/allure

# Run on specific browser
$env:PYTHONPATH = ".\app-tracker-automation"; pytest --browser=chromium
```

## Test Categories

### Sanity Tests
**Purpose**: Quick validation of critical functionality
**Execution Time**: < 5 minutes
**When to Run**: Every code commit

```bash
pytest -m sanity -v --tb=short
```

**Coverage**:
- Login functionality
- Dashboard accessibility
- Basic navigation
- Core module access

### Smoke Tests
**Purpose**: Core business functionality validation
**Execution Time**: < 15 minutes
**When to Run**: Before merges, daily

```bash
pytest -m smoke -v --maxfail=3
```

**Coverage**:
- User registration flow
- Policy quote generation
- Claim submission
- Payment processing

### Regression Tests
**Purpose**: Comprehensive feature testing
**Execution Time**: < 2 hours
**When to Run**: Before releases, weekly

```bash
pytest -m regression -v --maxfail=10 --junitxml=reports/junit/results.xml
```

**Coverage**:
- All existing functionality
- Integration points
- Edge cases
- Error scenarios

## Browser Testing

### Cross-Browser Testing
```bash
# Chrome/Chromium
pytest --browser=chromium

# Firefox
pytest --browser=firefox

# Safari/WebKit
pytest --browser=webkit

# All browsers (parallel)
pytest --browser=chromium,firefox,webkit -n auto
```

### Mobile Testing
```bash
# Mobile viewport
pytest --viewport="375,667"

# Tablet viewport
pytest --viewport="768,1024"
```

## Reporting

### HTML Reports
```bash
pytest --html=reports/html/report.html --self-contained-html
```

### Allure Reports
```bash
# Generate report
pytest --alluredir=reports/allure

# View report
allure serve reports/allure

# Generate static report
allure generate reports/allure -o reports/allure-report
```

### JUnit Reports
```bash
pytest --junitxml=reports/junit/results.xml
```

### Excel Reports
```bash
pytest --excel-report=reports/excel/results.xlsx
```

## Debugging

### Debug Mode
```bash
# Debug with Playwright Inspector
pytest --debug

# Debug specific test
pytest tests/sanity/test_login.py::TestLogin::test_success --debug
```

### Headful Mode
```bash
# Run with visible browser
pytest --headed=true

# Slow mode for debugging
pytest --headed=true --slowmo=1000
```

### Trace Files
```bash
# Generate trace files
pytest --tracing=retain-on-failure

# View trace
playwright show-trace trace.zip
```

## Data Management

### Test Data Setup
```bash
# Load test data
pytest --testdata=environment=staging

# Use specific user
pytest --user=admin
```

### Database Setup
```bash
# Reset test database
pytest --reset-db

# Load test fixtures
pytest --load-fixtures
```

## Performance Testing

### Performance Metrics
```bash
# Run with performance monitoring
pytest --performance

# Generate performance report
pytest --performance-report=reports/performance/
```

### Load Testing
```bash
# Run load tests
pytest -m load --users=10 --duration=300
```

## CI/CD Integration

### GitHub Actions
```yaml
# .github/workflows/test.yml
name: Run Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install
      - name: Run tests
        run: pytest -m sanity --alluredir=reports/allure
```

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'playwright install'
                sh 'pytest -m smoke --junitxml=reports/junit/results.xml'
            }
        }
    }
}
```

## Troubleshooting

### Common Issues

#### Element Not Found
```bash
# Increase timeout
pytest --timeout=60000

# Run with retries
pytest --retry=3
```

#### Browser Launch Issues
```bash
# Reinstall browsers
playwright install --force

# Check browser versions
playwright install --dry-run
```

#### Memory Issues
```bash
# Run tests sequentially
pytest -n 1

# Increase memory limit
pytest --maxfail=1
```

### Log Analysis
```bash
# View execution logs
tail -f logs/execution.log

# Filter errors
grep "ERROR" logs/execution.log
```

### Screenshot Analysis
```bash
# View failed screenshots
ls screenshots/failed/

# Compare screenshots
diff screenshots/before.png screenshots/after.png
```

## Maintenance

### Regular Tasks
1. **Daily**: Run smoke tests
2. **Weekly**: Run regression tests
3. **Monthly**: Update dependencies
4. **Quarterly**: Review test coverage

### Health Checks
```bash
# Check framework health
pytest --health-check

# Validate test data
pytest --validate-data

# Check locators
pytest --validate-locators
```

### Updates
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Update Playwright
playwright install --with-deps

# Update browsers
playwright install --force
```

## Emergency Procedures

### Test Failures
1. **Immediate**: Check test logs
2. **Investigation**: Review screenshots and traces
3. **Analysis**: Identify root cause
4. **Resolution**: Fix or mark as known issue
5. **Verification**: Re-run affected tests

### System Outages
1. **Pause**: Stop test execution
2. **Notify**: Alert team members
3. **Monitor**: Track system status
4. **Resume**: Restart when system is stable
5. **Validate**: Run sanity tests

### Data Corruption
1. **Stop**: Halt all test execution
2. **Backup**: Preserve current state
3. **Restore**: Reset to last known good state
4. **Validate**: Verify data integrity
5. **Resume**: Restart test execution

## Best Practices

### Test Execution
1. Use appropriate test categories
2. Monitor resource usage
3. Review test results regularly
4. Maintain test environments
5. Keep dependencies updated

### Reporting
1. Generate comprehensive reports
2. Track trends over time
3. Share results with stakeholders
4. Archive historical data
5. Use metrics for improvement

### Troubleshooting
1. Start with logs and screenshots
2. Use debugging tools effectively
3. Document findings
4. Share knowledge with team
5. Prevent future occurrences

## Contact Information

### Team Contacts
- **Test Lead**: [Email/Slack]
- **Dev Team**: [Email/Slack]
- **Ops Team**: [Email/Slack]

### Escalation
1. **Level 1**: Test team members
2. **Level 2**: Test lead
3. **Level 3**: Development team
4. **Level 4**: Operations team

## Resources

### Documentation
- [Framework Guide](framework-guide.md)
- [API Documentation](https://playwright.dev/python/)
- [Pytest Documentation](https://docs.pytest.org/)

### Tools
- Playwright Inspector
- Allure Report Viewer
- VS Code with extensions
- Git for version control

### Monitoring
- Test execution dashboards
- Performance metrics
- Error tracking systems
- Log aggregation tools
