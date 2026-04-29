"""
Tabs component for handling tab navigation.
"""

from playwright.sync_api import Page
from components.base_component import BaseComponent


class Tabs(BaseComponent):
    """Tabs component class"""
    
    def __init__(self, page: Page, locator: str):
        super().__init__(page, locator)
    
    def get_tab_count(self) -> int:
        """Get number of tabs"""
        tabs = self.element.locator(".tab")
        return len(tabs.all())
    
    def get_active_tab_index(self) -> int:
        """Get index of active tab"""
        active_tab = self.element.locator(".tab.active")
        tabs = self.element.locator(".tab")
        return tabs.all().index(active_tab.all()[0])
    
    def get_active_tab_text(self) -> str:
        """Get text of active tab"""
        active_tab = self.element.locator(".tab.active")
        return active_tab.text_content()
    
    def click_tab_by_index(self, index: int):
        """Click tab by index"""
        tabs = self.element.locator(".tab")
        if index < len(tabs.all()):
            tabs.all()[index].click()
    
    def click_tab_by_text(self, text: str):
        """Click tab by text"""
        tab = self.element.locator(f".tab:has-text('{text}')")
        tab.click()
    
    def is_tab_active(self, index: int) -> bool:
        """Check if tab is active by index"""
        tabs = self.element.locator(".tab")
        if index < len(tabs.all()):
            return "active" in tabs.all()[index].get_attribute("class")
        return False
    
    def is_tab_active_by_text(self, text: str) -> bool:
        """Check if tab is active by text"""
        tab = self.element.locator(f".tab:has-text('{text}')")
        return "active" in tab.get_attribute("class")
    
    def get_all_tab_texts(self) -> list:
        """Get all tab texts"""
        tabs = self.element.locator(".tab")
        return tabs.all_inner_texts()
    
    def is_tab_disabled(self, index: int) -> bool:
        """Check if tab is disabled by index"""
        tabs = self.element.locator(".tab")
        if index < len(tabs.all()):
            return "disabled" in tabs.all()[index].get_attribute("class")
        return False
    
    def wait_for_tab_content(self, timeout: int = 30000):
        """Wait for tab content to load"""
        self.page.wait_for_timeout(1000)  # Placeholder
