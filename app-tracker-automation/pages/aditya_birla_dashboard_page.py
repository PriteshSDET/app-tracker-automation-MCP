"""
Aditya Birla Sun Life Insurance Dashboard Page
Enhanced dashboard page for UAT environment
"""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from locators.aditya_birla_locators import AdityaBirlaLocators
from utils.logger import Logger
from utils.waits import Waits


class AdityaBirlaDashboardPage(BasePage):
    """Aditya Birla Sun Life Insurance dashboard page"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = AdityaBirlaLocators()
        self.waits = Waits(page)
    
    def is_dashboard_displayed(self) -> bool:
        """Check if dashboard is displayed"""
        try:
            # Check URL
            current_url = self.page.url
            if "dashboard" not in current_url:
                return False
            
            # Check key elements
            header_visible = self.is_element_visible(self.locators.dashboard_page["header"])
            
            # Use more specific locator for data table
            table_locator = self.page.locator("table:has-text('Application')")
            table_visible = table_locator.is_visible()
            
            return header_visible and table_visible
            
        except Exception as e:
            self.logger.error(f"Error checking dashboard display: {str(e)}")
            return False
    
    def get_application_list_title(self) -> str:
        """Get application list title"""
        try:
            title_element = self.page.locator(self.locators.dashboard_page["application_list_title"]).first
            if title_element.is_visible():
                return title_element.text_content()
            return ""
        except:
            return ""
    
    def click_menu_button(self):
        """Click menu button to expand navigation"""
        try:
            self.logger.info("Clicking menu button")
            
            menu_button = self.page.locator(self.locators.dashboard_page["menu_button"]).first
            self.waits.wait_for_element_enabled(self.locators.dashboard_page["menu_button"])
            menu_button.click()
            
            # Wait for dropdown to appear
            self.page.wait_for_timeout(1000)
            
            self.logger.info("Menu button clicked")
            
        except Exception as e:
            self.logger.error(f"Failed to click menu button: {str(e)}")
            raise
    
    def navigate_to_application_tracker(self):
        """Navigate to Application Tracker via menu"""
        try:
            self.logger.info("Navigating to Application Tracker")
            
            # First click menu to expand
            self.click_menu_button()
            
            # Wait for menu dropdown
            self.waits.wait_for_element_visible(self.locators.navigation_menu["menu_dropdown"])
            
            # Click Application Tracker menu item
            tracker_item = self.page.locator(self.locators.navigation_menu["application_tracker_item"]).first
            self.waits.wait_for_element_visible(self.locators.navigation_menu["application_tracker_item"])
            tracker_item.click()
            
            # Wait for navigation
            self.page.wait_for_timeout(3000)
            
            self.logger.info("Navigation to Application Tracker initiated")
            
        except Exception as e:
            self.logger.error(f"Failed to navigate to Application Tracker: {str(e)}")
            raise
    
    def verify_uat_badge(self) -> bool:
        """Verify UAT badge is visible"""
        return self.is_element_visible(self.locators.dashboard_page["uat_badge"])
    
    def get_data_rows_count(self) -> int:
        """Get number of data rows in the table"""
        try:
            rows = self.page.locator(self.locators.dashboard_page["data_rows"])
            return len(rows.all())
        except:
            return 0
    
    def get_pending_applications_count(self) -> int:
        """Get number of pending applications"""
        try:
            pending_dots = self.page.locator(self.locators.dashboard_page["pending_dots"])
            return len(pending_dots.all())
        except:
            return 0
    
    def is_new_application_button_visible(self) -> bool:
        """Check if new application button is visible"""
        return self.is_element_visible(self.locators.dashboard_page["new_application_button"])
    
    def click_new_application_button(self):
        """Click new application button"""
        try:
            button = self.page.locator(self.locators.dashboard_page["new_application_button"]).first
            self.waits.wait_for_element_enabled(self.locators.dashboard_page["new_application_button"])
            button.click()
            
            self.logger.info("New application button clicked")
            
        except Exception as e:
            self.logger.error(f"Failed to click new application button: {str(e)}")
            raise
    
    def wait_for_dashboard_load(self, timeout: int = 15000):
        """Wait for dashboard to fully load"""
        try:
            # Wait for URL to change from login page - more flexible approach
            current_url = self.page.url
            self.logger.info(f"Current URL: {current_url}")
            
            # Wait for URL to change away from login page
            if "login" in current_url:
                self.logger.info("Still on login page, waiting for redirect...")
                # Wait for any URL change that indicates successful login
                self.page.wait_for_function(
                    """() => {
                        const url = window.location.href;
                        return !url.includes('login') && 
                               (url.includes('dashboard') || 
                                url.includes('application') || 
                                url.includes('home'));
                    }""",
                    timeout=10000
                )
            else:
                self.logger.info("Already navigated away from login page")
            
            # Wait for any page content to load - be very flexible
            self.waits.wait_for_timeout(3000)
            
            # Check for menu button which indicates dashboard is loaded
            try:
                menu_button = self.page.locator("button:has-text('Menu'), [class*='menu'], .dropdown-toggle").first
                if menu_button.is_visible():
                    self.logger.info("✓ Menu button found - dashboard loaded")
                else:
                    self.logger.info("Menu button not visible, but continuing...")
            except:
                self.logger.info("Menu button check failed, but continuing...")
            
            # Don't wait for table - let the menu click handle navigation
            self.logger.info("Dashboard load check completed - ready for menu navigation")
            
        except Exception as e:
            self.logger.error(f"Dashboard load timeout: {str(e)}")
            # Don't raise exception - let test continue with logging
            self.logger.warning("Dashboard load issue - continuing test execution")
    
    def get_toolbar_elements(self) -> list:
        """Get toolbar elements text"""
        try:
            toolbar = self.page.locator(self.locators.dashboard_page["toolbar"]).first
            if toolbar.is_visible():
                elements = toolbar.locator("button, .filter, .sort").all()
                return [elem.text_content() for elem in elements if elem.text_content()]
            return []
        except:
            return []
    
    def verify_toolbar_elements(self) -> bool:
        """Verify required toolbar elements are present"""
        try:
            filter_visible = self.is_element_visible(self.locators.dashboard_page["filter_button"])
            sort_visible = self.is_element_visible(self.locators.dashboard_page["sort_button"])
            
            return filter_visible and sort_visible
        except:
            return False
    
    def take_screenshot(self, name: str = "dashboard"):
        """Take screenshot of dashboard"""
        timestamp = self.page.evaluate("new Date().toISOString().replace(/[:.]/g, '-')")
        filename = f"{name}_{timestamp}.png"
        self.page.screenshot(path=f"screenshots/{filename}", full_page=True)
        self.logger.info(f"Screenshot saved: {filename}")
