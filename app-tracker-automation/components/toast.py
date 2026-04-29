"""
Toast component for handling toast notifications.
"""

from playwright.sync_api import Page
from components.base_component import BaseComponent


class Toast(BaseComponent):
    """Toast component class"""
    
    def __init__(self, page: Page, locator: str):
        super().__init__(page, locator)
    
    def is_visible(self) -> bool:
        """Check if toast is visible"""
        return self.element.is_visible()
    
    def wait_for_visible(self, timeout: int = 10000):
        """Wait for toast to appear"""
        self.wait_for_visible(timeout)
    
    def wait_for_disappear(self, timeout: int = 10000):
        """Wait for toast to disappear"""
        self.waits.wait_for_element_disappear(self.locator, timeout)
    
    def get_message(self) -> str:
        """Get toast message"""
        message_element = self.element.locator(".toast-message")
        return message_element.text_content()
    
    def get_type(self) -> str:
        """Get toast type (success, error, warning, info)"""
        return self.element.get_attribute("data-type") or ""
    
    def is_success(self) -> bool:
        """Check if toast is success type"""
        return "success" in self.get_type()
    
    def is_error(self) -> bool:
        """Check if toast is error type"""
        return "error" in self.get_type()
    
    def is_warning(self) -> bool:
        """Check if toast is warning type"""
        return "warning" in self.get_type()
    
    def is_info(self) -> bool:
        """Check if toast is info type"""
        return "info" in self.get_type()
    
    def close(self):
        """Close toast manually"""
        close_button = self.element.locator(".toast-close")
        if close_button.is_visible():
            close_button.click()
    
    def get_title(self) -> str:
        """Get toast title if available"""
        title_element = self.element.locator(".toast-title")
        return title_element.text_content() if title_element.is_visible() else ""
