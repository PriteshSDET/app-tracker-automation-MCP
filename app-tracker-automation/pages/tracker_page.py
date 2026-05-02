"""
Tracker Page Object Model
Handles application tracking functionality for the insurance portal
"""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from locators.tracker_locators import TrackerLocators


class TrackerPage(BasePage):
    """Tracker page object"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = TrackerLocators()
    
    def is_tracker_displayed(self) -> bool:
        """Check if tracker page is displayed"""
        return self.is_element_visible(self.locators.tracker_container)
    
    def search_application(self, application_id: str):
        """Search for specific application"""
        self.fill_text(self.locators.search_input, application_id)
        self.click_element(self.locators.search_button)
    
    def get_application_status(self, application_id: str) -> str:
        """Get status of specific application"""
        locator = f"{self.locators.application_row}[data-id='{application_id}'] {self.locators.status_column}"
        return self.page.locator(locator).text_content()
    
    def filter_by_status(self, status: str):
        """Filter applications by status"""
        self.click_element(self.locators.status_filter)
        self.click_element(f"{self.locators.status_option}[data-status='{status}']")
    
    def view_application_details(self, application_id: str):
        """View detailed information for an application"""
        locator = f"{self.locators.application_row}[data-id='{application_id}'] {self.locators.view_details_button}"
        self.click_element(locator)
    
    def export_applications(self, format: str = "excel"):
        """Export applications list"""
        self.click_element(self.locators.export_button)
        self.click_element(f"{self.locators.export_option}[data-format='{format}']")
    
    def get_total_applications_count(self) -> int:
        """Get total number of applications"""
        text = self.page.locator(self.locators.total_count).text_content()
        return int(text) if text else 0

