"""
Aditya Birla Sun Life Insurance Application Tracker Page
Enhanced tracker page for UAT environment
"""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from locators.aditya_birla_locators import AdityaBirlaLocators
from utils.logger import Logger
from utils.waits import Waits


class AdityaBirlaTrackerPage(BasePage):
    """Aditya Birla Sun Life Insurance Application Tracker page"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = AdityaBirlaLocators()
        self.waits = Waits(page)
    
    def is_tracker_displayed(self) -> bool:
        """Check if tracker page is displayed"""
        try:
            # Check URL
            current_url = self.page.url
            if "app-tracker" not in current_url:
                return False
            
            # Check key elements
            title_visible = self.is_element_visible(self.locators.tracker_page["header"])
            
            # Use more specific locator for data table
            table_locator = self.page.locator("table:has-text('Application')")
            table_visible = table_locator.is_visible()
            
            return title_visible and table_visible
            
        except Exception as e:
            self.logger.error(f"Error checking tracker display: {str(e)}")
            return False
    
    def get_policy_list_title(self) -> str:
        """Get policy list title"""
        try:
            title_element = self.page.locator(self.locators.tracker_page["policy_list_title"]).first
            if title_element.is_visible():
                return title_element.text_content()
            return ""
        except:
            return ""
    
    def get_refresh_info(self) -> str:
        """Get refresh information text"""
        try:
            refresh_element = self.page.locator(self.locators.tracker_page["refresh_info"]).first
            if refresh_element.is_visible():
                return refresh_element.text_content()
            return ""
        except:
            return ""
    
    def verify_table_headers(self) -> bool:
        """Verify all required table headers are present"""
        try:
            required_headers = [
                "App.No", "Proposer Name", "Plan Name", 
                "Modal Premium", "Policy Status"
            ]
            
            for header in required_headers:
                header_locator = self.locators.table_columns[header.lower().replace(".", "").replace(" ", "_")]
                header_element = self.page.locator(header_locator).first
                if not header_element.is_visible():
                    self.logger.error(f"Missing table header: {header}")
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error verifying table headers: {str(e)}")
            return False
    
    def get_table_rows_count(self) -> int:
        """Get number of data rows in the table"""
        try:
            rows = self.page.locator(self.locators.tracker_page["table_rows"])
            return len(rows.all())
        except:
            return 0
    
    def get_pending_status_count(self) -> int:
        """Get number of rows with pending status"""
        try:
            pending_indicators = self.page.locator(self.locators.dashboard_page["pending_dots"])
            return len(pending_indicators.all())
        except:
            return 0
    
    def verify_filter_controls(self) -> bool:
        """Verify filter controls are present"""
        try:
            filter_chips_visible = self.is_element_visible(self.locators.tracker_page["filter_chips"])
            search_bar_visible = self.is_element_visible(self.locators.tracker_page["search_bar"])
            date_picker_visible = self.is_element_visible(self.locators.tracker_page["date_range_picker"])
            
            return filter_chips_visible and search_bar_visible and date_picker_visible
            
        except Exception as e:
            self.logger.error(f"Error verifying filter controls: {str(e)}")
            return False
    
    def verify_uat_badge(self) -> bool:
        """Verify UAT badge is visible"""
        return self.is_element_visible(self.locators.tracker_page["uat_badge"])
    
    def wait_for_tracker_load(self, timeout: int = 15000):
        """Wait for tracker page to fully load"""
        try:
            # Wait for URL to contain app-tracker
            self.waits.wait_for_url_contains("app-tracker", timeout)
            
            # Wait for key elements to be visible
            self.waits.wait_for_element_visible(self.locators.tracker_page["header"], timeout)
            
            # Use more specific locator for data table - filter by common insurance table text
            table_locator = self.page.locator("table:has-text('Application')")
            self.waits.wait_for_element_visible(table_locator, timeout)
            
            self.logger.info("Tracker page loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Tracker page load timeout: {str(e)}")
            raise
    
    def search_applications(self, search_term: str):
        """Search applications by search term"""
        try:
            self.logger.info(f"Searching applications: {search_term}")
            
            search_input = self.page.locator(self.locators.tracker_page["search_bar"]).first
            self.waits.wait_for_element_visible(self.locators.tracker_page["search_bar"])
            
            search_input.fill(search_term)
            search_input.press("Enter")
            
            # Wait for search results
            self.page.wait_for_timeout(2000)
            
            self.logger.info("Search completed")
            
        except Exception as e:
            self.logger.error(f"Failed to search applications: {str(e)}")
            raise
    
    def clear_search(self):
        """Clear search input"""
        try:
            search_input = self.page.locator(self.locators.tracker_page["search_bar"]).first
            search_input.fill("")
            search_input.press("Enter")
            
            self.logger.info("Search cleared")
            
        except Exception as e:
            self.logger.error(f"Failed to clear search: {str(e)}")
    
    def get_table_data(self) -> list:
        """Get all table data as list of dictionaries"""
        try:
            data = []
            rows = self.page.locator(self.locators.tracker_page["table_rows"]).all()
            
            for row in rows:
                cells = row.locator("td").all()
                row_data = {}
                
                # Map columns to data
                if len(cells) >= 5:
                    row_data["app_no"] = cells[0].text_content()
                    row_data["proposer_name"] = cells[1].text_content()
                    row_data["plan_name"] = cells[2].text_content()
                    row_data["modal_premium"] = cells[3].text_content()
                    row_data["policy_status"] = cells[4].text_content()
                
                data.append(row_data)
            
            return data
            
        except Exception as e:
            self.logger.error(f"Failed to get table data: {str(e)}")
            return []
    
    def verify_data_integrity(self) -> bool:
        """Verify table data integrity"""
        try:
            data = self.get_table_data()
            
            for row in data:
                # Check required fields are not empty
                if not row.get("app_no") or not row.get("proposer_name"):
                    self.logger.error("Missing required data in table row")
                    return False
                
                # Check policy status is valid
                status = row.get("policy_status", "")
                valid_statuses = ["Pending", "Approved", "Rejected", "Completed"]
                if status and status not in valid_statuses:
                    self.logger.warning(f"Unknown policy status: {status}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error verifying data integrity: {str(e)}")
            return False
    
    def take_screenshot(self, name: str = "tracker"):
        """Take screenshot of tracker page"""
        timestamp = self.page.evaluate("new Date().toISOString().replace(/[:.]/g, '-')")
        filename = f"{name}_{timestamp}.png"
        self.page.screenshot(path=f"screenshots/{filename}", full_page=True)
        self.logger.info(f"Screenshot saved: {filename}")
    
    def get_page_info(self) -> dict:
        """Get comprehensive page information"""
        try:
            info = {
                "url": self.page.url,
                "title": self.page.title(),
                "policy_list_title": self.get_policy_list_title(),
                "refresh_info": self.get_refresh_info(),
                "table_rows_count": self.get_table_rows_count(),
                "pending_count": self.get_pending_status_count(),
                "uat_badge_visible": self.verify_uat_badge(),
                "filter_controls_present": self.verify_filter_controls(),
                "table_headers_valid": self.verify_table_headers(),
                "data_integrity_valid": self.verify_data_integrity()
            }
            
            return info
            
        except Exception as e:
            self.logger.error(f"Failed to get page info: {str(e)}")
            return {}
