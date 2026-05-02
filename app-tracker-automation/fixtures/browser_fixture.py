"""
Browser fixture for Playwright browser management
"""

import pytest
from playwright.sync_api import Browser, BrowserContext, Page
from utils.config import Config
from utils.logger import Logger


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context arguments"""
    return {
        **browser_context_args,
        "viewport": Config.BROWSER_VIEWPORT,
        "ignore_https_errors": True,
        "accept_downloads": True,
        "java_script_enabled": True
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Configure browser launch arguments for full screen mode"""
    return {
        **browser_type_launch_args,
        "args": Config.BROWSER_LAUNCH_ARGS
    }


@pytest.fixture(scope="function")
def authenticated_page(page: Page, browser: Browser):
    """Fixture providing authenticated page for tests"""
    from flows.login_flow import LoginFlow
    from data.env import ENVIRONMENT_CONFIG
    
    # Perform login
    login_flow = LoginFlow(page)
    login_flow.perform_login(
        username=ENVIRONMENT_CONFIG["test_user"]["username"],
        password=ENVIRONMENT_CONFIG["test_user"]["password"]
    )
    
    yield page
    
    # Cleanup - logout if still logged in
    try:
        login_flow.perform_logout()
    except:
        pass


@pytest.fixture(scope="function")
def mobile_page(browser: Browser):
    """Fixture providing mobile-sized page"""
    context = browser.new_context(
        viewport={"width": 375, "height": 667},
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15"
    )
    page = context.new_page()
    yield page
    page.close()
    context.close()


@pytest.fixture(scope="function")
def tablet_page(browser: Browser):
    """Fixture providing tablet-sized page"""
    context = browser.new_context(
        viewport={"width": 768, "height": 1024},
        user_agent="Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15"
    )
    page = context.new_page()
    yield page
    page.close()
    context.close()

