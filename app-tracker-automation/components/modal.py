"""
Modal component for handling modal dialogs.
"""

from playwright.sync_api import Page
from components.base_component import BaseComponent


class Modal(BaseComponent):
    """Modal component class"""
    
    def __init__(self, page: Page, locator: str):
        super().__init__(page, locator)
    
    def is_open(self) -> bool:
        """Check if modal is open"""
        return self.is_visible()
    
    def wait_for_open(self, timeout: int = 30000):
        """Wait for modal to open"""
        self.wait_for_visible(timeout)
    
    def close(self):
        """Close modal"""
        close_button = self.element.locator(".modal-close")
        if close_button.is_visible():
            close_button.click()
        else:
            self.page.press("Escape")
    
    def get_title(self) -> str:
        """Get modal title"""
        title_element = self.element.locator(".modal-title")
        return title_element.text_content()
    
    def get_content(self) -> str:
        """Get modal content"""
        content_element = self.element.locator(".modal-content")
        return content_element.text_content()
    
    def confirm(self):
        """Click confirm/OK button"""
        confirm_button = self.element.locator("button[data-action='confirm']")
        confirm_button.click()
    
    def cancel(self):
        """Click cancel button"""
        cancel_button = self.element.locator("button[data-action='cancel']")
        cancel_button.click()
    
    def is_closable(self) -> bool:
        """Check if modal can be closed"""
        close_button = self.element.locator(".modal-close")
        return close_button.is_visible()
    
    def get_buttons(self) -> list:
        """Get all modal buttons"""
        buttons = self.element.locator("button")
        return buttons.all_inner_texts()
    
    def click_button_by_text(self, text: str):
        """Click button by its text"""
        button = self.element.locator(f"button:has-text('{text}')")
        button.click()
