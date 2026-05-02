"""
Base Component class for reusable UI components.
Provides common functionality for all component objects.
"""

from playwright.sync_api import Page, expect
from utils.logger import Logger
from utils.waits import Waits


class BaseComponent:
    """Base class for all UI components"""
    
    def __init__(self, page: Page, locator: str):
        self.page = page
        self.locator = locator
        self.logger = Logger()
        self.waits = Waits(page)
        self.element = page.locator(locator)
    
    def is_visible(self) -> bool:
        """Check if component is visible"""
        return self.element.is_visible()
    
    def is_enabled(self) -> bool:
        """Check if component is enabled"""
        return self.element.is_enabled()
    
    def wait_for_visible(self, timeout: int = 30000):
        """Wait for component to be visible"""
        self.waits.wait_for_element_visible(self.locator, timeout)
    
    def wait_for_enabled(self, timeout: int = 30000):
        """Wait for component to be enabled"""
        self.waits.wait_for_element_enabled(self.locator, timeout)
    
    def click(self):
        """Click on component"""
        self.element.click()
    
    def hover(self):
        """Hover over component"""
        self.element.hover()
    
    def get_text(self) -> str:
        """Get text content of component"""
        return self.element.text_content()
    
    def get_attribute(self, attribute: str) -> str:
        """Get attribute value of component"""
        return self.element.get_attribute(attribute)
    
    def scroll_into_view(self):
        """Scroll component into view"""
        self.element.scroll_into_view_if_needed()

