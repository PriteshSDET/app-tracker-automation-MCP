"""
Tracker Flow - Business logic for application tracking
"""

from pages.tracker_page import TrackerPage
from pages.dashboard_page import DashboardPage
from utils.logger import Logger


class TrackerFlow:
    """Tracker flow class handling application tracking business logic"""
    
    def __init__(self, page):
        self.page = page
        self.tracker_page = TrackerPage(page)
        self.dashboard_page = DashboardPage(page)
        self.logger = Logger()
    
    def navigate_to_tracker(self) -> bool:
        """
        Navigate to tracker page
        
        Returns:
            bool: True if navigation successful, False otherwise
        """
        try:
            self.logger.info("Navigating to tracker page")
            
            # Navigate from dashboard to tracker
            self.dashboard_page.navigate_to_policies()
            
            # Wait for page to load
            self.page.wait_for_timeout(2000)
            
            # Verify tracker page is displayed
            if self.tracker_page.is_tracker_displayed():
                self.logger.info("Successfully navigated to tracker page")
                return True
            else:
                self.logger.error("Tracker page is not displayed")
                return False
                
        except Exception as e:
            self.logger.error(f"Navigation to tracker failed: {str(e)}")
            return False
    
    def search_application(self, application_id: str) -> dict:
        """
        Search for specific application
        
        Args:
            application_id: Application ID to search
            
        Returns:
            dict: Search results with status and data
        """
        try:
            self.logger.info(f"Searching for application: {application_id}")
            
            # Perform search
            self.tracker_page.search_application(application_id)
            
            # Wait for search results
            self.page.wait_for_timeout(2000)
            
            # Get application status
            status = self.tracker_page.get_application_status(application_id)
            
            result = {
                "application_id": application_id,
                "status": status,
                "found": True if status else False
            }
            
            self.logger.info(f"Search result: {result}")
            return result
            
        except Exception as e:
            self.logger.error(f"Application search failed: {str(e)}")
            return {"application_id": application_id, "status": None, "found": False}
    
    def filter_applications_by_status(self, status: str) -> bool:
        """
        Filter applications by status
        
        Args:
            status: Status to filter by
            
        Returns:
            bool: True if filter applied successfully, False otherwise
        """
        try:
            self.logger.info(f"Filtering applications by status: {status}")
            
            # Apply filter
            self.tracker_page.filter_by_status(status)
            
            # Wait for filter to apply
            self.page.wait_for_timeout(2000)
            
            self.logger.info("Filter applied successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Filter application failed: {str(e)}")
            return False
    
    def export_applications(self, format: str = "excel") -> bool:
        """
        Export applications list
        
        Args:
            format: Export format (excel, csv, pdf)
            
        Returns:
            bool: True if export successful, False otherwise
        """
        try:
            self.logger.info(f"Exporting applications in {format} format")
            
            # Perform export
            self.tracker_page.export_applications(format)
            
            # Wait for export to complete
            self.page.wait_for_timeout(3000)
            
            self.logger.info("Export completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Export failed: {str(e)}")
            return False
    
    def get_applications_summary(self) -> dict:
        """
        Get summary of applications
        
        Returns:
            dict: Summary information
        """
        try:
            self.logger.info("Getting applications summary")
            
            total_count = self.tracker_page.get_total_applications_count()
            
            summary = {
                "total_applications": total_count,
                "timestamp": self.page.evaluate("new Date().toISOString()")
            }
            
            self.logger.info(f"Applications summary: {summary}")
            return summary
            
        except Exception as e:
            self.logger.error(f"Failed to get applications summary: {str(e)}")
            return {"total_applications": 0, "timestamp": None}
