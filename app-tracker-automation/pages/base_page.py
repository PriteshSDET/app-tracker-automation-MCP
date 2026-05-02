"""
Base Page class for Page Object Model pattern.
Provides common functionality for all page objects.
"""

from playwright.sync_api import Page, expect
from utils.logger import Logger
from utils.waits import Waits


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, page: Page):
        self.page = page
        self.logger = Logger()
        self.waits = Waits(page)
    
    def navigate_to(self, url: str):
        """Navigate to specified URL"""
        self.logger.info(f"Navigating to: {url}")
        self.page.goto(url)
    
    def get_title(self) -> str:
        """Get page title"""
        return self.page.title()
    
    def wait_for_page_load(self, timeout: int = 30000):
        """Wait for page to fully load"""
        self.waits.wait_for_page_load(timeout)
    
    def take_screenshot(self, name: str):
        """Take screenshot"""
        self.page.screenshot(path=f"screenshots/{name}.png")
    
    def is_element_visible(self, locator: str) -> bool:
        """Check if element is visible"""
        return self.page.locator(locator).is_visible()
    
    def click_element(self, locator: str):
        """Click on element"""
        self.page.locator(locator).click()
    
    def fill_text(self, locator: str, text: str):
        """Fill text in input field"""
        self.page.locator(locator).fill(text)

