"""
Dashboard Page Object Model
Handles dashboard functionality for the insurance portal
"""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from locators.shared_locators import SharedLocators


class DashboardPage(BasePage):
    """Dashboard page object"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = SharedLocators()
    
    def is_dashboard_displayed(self) -> bool:
        """Check if dashboard is displayed"""
        return self.is_element_visible(self.locators.dashboard_container)
    
    def get_welcome_message(self) -> str:
        """Get welcome message"""
        return self.page.locator(self.locators.welcome_message).text_content()
    
    def navigate_to_policies(self):
        """Navigate to policies section"""
        self.click_element(self.locators.policies_link)
    
    def navigate_to_claims(self):
        """Navigate to claims section"""
        self.click_element(self.locators.claims_link)
    
    def navigate_to_profile(self):
        """Navigate to profile section"""
        self.click_element(self.locators.profile_link)
    
    def logout(self):
        """Perform logout"""
        self.click_element(self.locators.logout_button)
    
    def get_active_policies_count(self) -> int:
        """Get number of active policies"""
        text = self.page.locator(self.locators.active_policies_count).text_content()
        return int(text) if text else 0
    
    def get_pending_claims_count(self) -> int:
        """Get number of pending claims"""
        text = self.page.locator(self.locators.pending_claims_count).text_content()
        return int(text) if text else 0

