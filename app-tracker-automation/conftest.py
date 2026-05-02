import pytest
import os
import subprocess
from playwright.sync_api import Page, BrowserContext, Browser, sync_playwright
from utils.config import Config
from utils.logger import Logger

@pytest.fixture(scope="session")
def browser():
    """Browser fixture for Playwright"""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=['--start-maximized']  # Keeps the physical window maximized
        )
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser: Browser):
    """Page fixture for Playwright"""
    context = browser.new_context(
        # FIX: Remove viewport constraint to use full screen - ensures MENU button is visible
        viewport=None,  # Let browser use full screen size
        ignore_https_errors=True
    )
    page = context.new_page()
    yield page
    page.close()
    context.close()

@pytest.fixture(scope="session")
def config():
    """Configuration fixture"""
    return Config()

@pytest.fixture(scope="function")
def logger():
    """Logger fixture"""
    return Logger()

# ==========================================
# AUTO-RUN REPORTS HOOK
# ==========================================
def pytest_sessionfinish(session, exitstatus):
    """Runs automatically after the test session finishes."""
    print("\n\n--- Test Session Complete: Launching Reports ---")
    
    # 1. Open the Pytest-HTML Report
    html_report_path = os.path.abspath("reports/html/report.html") # Adjusted path based on your terminal output
    if os.path.exists(html_report_path):
        try:
            if os.name == 'nt':
                os.startfile(html_report_path)
            elif os.sys.platform == "darwin":
                subprocess.Popen(["open", html_report_path])
            else:
                subprocess.Popen(["xdg-open", html_report_path])
            print("[OK] HTML Report opened.")
        except Exception as e:
            print(f"Could not open HTML report: {e}")

    # 2. Trigger Allure Serve in the background (Non-blocking)
    if os.path.exists("allure-results"):
        print("🌐 Launching Allure Dashboard...")
        try:
            if os.name == 'nt':
                # FIX: Popen with shell=True runs this in the background on Windows
                subprocess.Popen("allure serve allure-results", shell=True)
            else:
                subprocess.Popen(["allure", "serve", "allure-results"])
        except Exception as e:
            print(f"Could not launch Allure: {e}")
