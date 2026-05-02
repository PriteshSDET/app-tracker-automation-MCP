"""
Failure hook for handling test failures and error reporting
"""

import os
import traceback
import pytest
from datetime import datetime
from playwright.sync_api import Page
from utils.config import Config
from utils.logger import Logger


class FailureHook:
    """Failure handling hook for tests"""
    
    def __init__(self):
        self.logger = Logger()
        self.failures_dir = "bugs/open"
    
    def setup_failures_dir(self):
        """Create failures directory if it doesn't exist"""
        if not os.path.exists(self.failures_dir):
            os.makedirs(self.failures_dir)
    
    def capture_failure_details(self, page: Page, test_name: str, error: Exception):
        """
        Capture detailed failure information
        
        Args:
            page: Playwright page object
            test_name: Name of the failed test
            error: Exception that caused the failure
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            failure_report = {
                "test_name": test_name,
                "timestamp": timestamp,
                "error_message": str(error),
                "error_type": type(error).__name__,
                "traceback": traceback.format_exc(),
                "url": page.url if page else "N/A",
                "title": page.title() if page else "N/A"
            }
            
            # Save failure report
            report_filename = f"failure_{test_name}_{timestamp}.json"
            report_path = os.path.join(self.failures_dir, report_filename)
            
            import json
            with open(report_path, 'w') as f:
                json.dump(failure_report, f, indent=2)
            
            self.logger.error(f"Failure details saved: {report_path}")
            
            # Take screenshot if page is available
            if page:
                screenshot_path = os.path.join(self.failures_dir, f"failure_{test_name}_{timestamp}.png")
                page.screenshot(path=screenshot_path, full_page=True)
                self.logger.error(f"Failure screenshot saved: {screenshot_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to capture failure details: {str(e)}")
    
    def log_failure(self, test_name: str, error: Exception):
        """Log failure information"""
        self.logger.error(f"Test '{test_name}' failed: {str(error)}")
        self.logger.error(f"Error type: {type(error).__name__}")
        self.logger.debug(f"Full traceback: {traceback.format_exc()}")
    
    def create_bug_report(self, test_name: str, error: Exception, page: Page = None):
        """
        Create detailed bug report
        
        Args:
            test_name: Name of the failed test
            error: Exception that caused the failure
            page: Playwright page object (optional)
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            bug_report = {
                "bug_id": f"BUG_{timestamp}",
                "test_name": test_name,
                "severity": "HIGH",
                "priority": "HIGH",
                "status": "OPEN",
                "reported_at": datetime.now().isoformat(),
                "error": {
                    "message": str(error),
                    "type": type(error).__name__,
                    "traceback": traceback.format_exc()
                },
                "environment": {
                    "base_url": Config.BASE_URL,
                    "browser": Config.BROWSER,
                    "headless": Config.HEADLESS
                },
                "page_info": {
                    "url": page.url if page else "N/A",
                    "title": page.title() if page else "N/A"
                }
            }
            
            # Save bug report
            bug_filename = f"bug_{test_name}_{timestamp}.json"
            bug_path = os.path.join(self.failures_dir, bug_filename)
            
            import json
            with open(bug_path, 'w') as f:
                json.dump(bug_report, f, indent=2)
            
            self.logger.error(f"Bug report created: {bug_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to create bug report: {str(e)}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Pytest hook to handle test failures"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        failure_hook = FailureHook()
        failure_hook.setup_failures_dir()
        
        # Get page object if available
        page = getattr(item, "_page", None)
        
        # Get exception if available
        error = getattr(report, "longrepr", None)
        if not error and hasattr(call, "excinfo"):
            error = call.excinfo[1] if call.excinfo else None
        
        # Capture failure details
        if error:
            failure_hook.capture_failure_details(page, item.name, error)
            failure_hook.create_bug_report(item.name, error, page)


@pytest.fixture
def failure_hook():
    """Fixture providing failure hook instance"""
    hook = FailureHook()
    hook.setup_failures_dir()
    return hook


@pytest.fixture
def page_with_failure_handling(page):
    """Page fixture with automatic failure handling"""
    failure_hook = FailureHook()
    failure_hook.setup_failures_dir()
    
    # Store references for hooks
    page._failure_hook = failure_hook
    page._test_name = "unknown"
    
    yield page
    
    # Handle any uncaught failures
    if hasattr(page, "_test_failed") and page._test_failed:
        error = getattr(page, "_last_error", Exception("Unknown error"))
        failure_hook.capture_failure_details(page, page._test_name, error)

