"""
Paginator component for handling pagination controls.
"""

from playwright.sync_api import Page
from components.base_component import BaseComponent


class Paginator(BaseComponent):
    """Paginator component class"""
    
    def __init__(self, page: Page, locator: str):
        super().__init__(page, locator)
    
    def go_to_page(self, page_number: int):
        """Navigate to specific page number"""
        page_button = self.element.locator(f"button[data-page='{page_number}']")
        page_button.click()
    
    def go_to_next_page(self):
        """Navigate to next page"""
        next_button = self.element.locator("button[data-action='next']")
        if next_button.is_enabled():
            next_button.click()
    
    def go_to_previous_page(self):
        """Navigate to previous page"""
        prev_button = self.element.locator("button[data-action='previous']")
        if prev_button.is_enabled():
            prev_button.click()
    
    def go_to_first_page(self):
        """Navigate to first page"""
        first_button = self.element.locator("button[data-action='first']")
        if first_button.is_enabled():
            first_button.click()
    
    def go_to_last_page(self):
        """Navigate to last page"""
        last_button = self.element.locator("button[data-action='last']")
        if last_button.is_enabled():
            last_button.click()
    
    def get_current_page(self) -> int:
        """Get current page number"""
        current_page_element = self.element.locator("span[data-current-page]")
        return int(current_page_element.text_content())
    
    def get_total_pages(self) -> int:
        """Get total number of pages"""
        total_pages_element = self.element.locator("span[data-total-pages]")
        return int(total_pages_element.text_content())
    
    def is_next_page_available(self) -> bool:
        """Check if next page is available"""
        next_button = self.element.locator("button[data-action='next']")
        return next_button.is_enabled()
    
    def is_previous_page_available(self) -> bool:
        """Check if previous page is available"""
        prev_button = self.element.locator("button[data-action='previous']")
        return prev_button.is_enabled()
