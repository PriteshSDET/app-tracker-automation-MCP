"""
Screenshot hook for capturing screenshots during test execution
"""

import os
import pytest
from playwright.sync_api import Page
from datetime import datetime
from utils.config import Config
from utils.logger import Logger


class ScreenshotHook:
    """Screenshot capture hook for tests"""
    
    def __init__(self):
        self.logger = Logger()
        self.screenshots_dir = "screenshots"
    
    def setup_screenshots_dir(self):
        """Create screenshots directory if it doesn't exist"""
        if not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)
        
        # Create subdirectories
        for subdir in ["passed", "failed", "debug"]:
            subdir_path = os.path.join(self.screenshots_dir, subdir)
            if not os.path.exists(subdir_path):
                os.makedirs(subdir_path)
    
    def take_screenshot(self, page: Page, name: str, status: str = "debug"):
        """
        Take screenshot with given name and status
        
        Args:
            page: Playwright page object
            name: Screenshot name
            status: Test status (passed, failed, debug)
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            filepath = os.path.join(self.screenshots_dir, status, filename)
            
            page.screenshot(path=filepath, full_page=True)
            self.logger.info(f"Screenshot saved: {filepath}")
            
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
    
    def take_failure_screenshot(self, page: Page, test_name: str):
        """Take screenshot on test failure"""
        self.take_screenshot(page, f"failure_{test_name}", "failed")
    
    def take_success_screenshot(self, page: Page, test_name: str):
        """Take screenshot on test success"""
        self.take_screenshot(page, f"success_{test_name}", "passed")
    
    def take_debug_screenshot(self, page: Page, step_name: str):
        """Take debug screenshot"""
        self.take_screenshot(page, f"debug_{step_name}", "debug")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Pytest hook to capture screenshots on test failure"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        page = getattr(item, "_page", None)
        if page is None:
            return
        
        screenshot_hook = ScreenshotHook()
        screenshot_hook.setup_screenshots_dir()
        
        if report.failed:
            screenshot_hook.take_failure_screenshot(page, item.name)
        elif report.passed:
            screenshot_hook.take_success_screenshot(page, item.name)


@pytest.fixture
def screenshot_hook():
    """Fixture providing screenshot hook instance"""
    hook = ScreenshotHook()
    hook.setup_screenshots_dir()
    return hook


@pytest.fixture
def page_with_screenshots(page):
    """Page fixture with automatic screenshot capture"""
    screenshot_hook = ScreenshotHook()
    screenshot_hook.setup_screenshots_dir()
    
    # Store page reference for hooks
    page._screenshot_hook = screenshot_hook
    
    yield page
    
    # Take final screenshot if test failed
    if hasattr(page, "_test_failed") and page._test_failed:
        screenshot_hook.take_failure_screenshot(page, "final")

