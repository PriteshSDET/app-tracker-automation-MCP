"""
Login Flow - Business logic for user authentication
"""

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.logger import Logger


class LoginFlow:
    """Login flow class handling authentication business logic"""
    
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)
        self.dashboard_page = DashboardPage(page)
        self.logger = Logger()
    
    def perform_login(self, username: str, password: str) -> bool:
        """
        Perform complete login flow
        
        Args:
            username: User username
            password: User password
            
        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            self.logger.info(f"Starting login flow for user: {username}")
            
            # Navigate to login page
            self.login_page.load()
            
            # Verify login page is displayed
            if not self.login_page.is_login_page_displayed():
                self.logger.error("Login page is not displayed")
                return False
            
            # Perform login
            self.login_page.login(username, password)
            
            # Wait for login to complete
            self.page.wait_for_timeout(2000)
            
            # Verify login was successful
            if self.login_page.is_login_successful():
                self.logger.info("Login successful")
                return True
            else:
                error_msg = self.login_page.get_error_message()
                self.logger.error(f"Login failed: {error_msg}")
                return False
                
        except Exception as e:
            self.logger.error(f"Login flow failed with exception: {str(e)}")
            return False
    
    def perform_logout(self) -> bool:
        """
        Perform logout flow
        
        Returns:
            bool: True if logout successful, False otherwise
        """
        try:
            self.logger.info("Starting logout flow")
            
            # Navigate to dashboard if not already there
            if not self.dashboard_page.is_dashboard_displayed():
                self.page.goto("/dashboard")
                self.page.wait_for_timeout(1000)
            
            # Perform logout
            self.dashboard_page.logout()
            
            # Wait for logout to complete
            self.page.wait_for_timeout(2000)
            
            # Verify logout was successful
            if self.login_page.is_login_page_displayed():
                self.logger.info("Logout successful")
                return True
            else:
                self.logger.error("Logout failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Logout flow failed with exception: {str(e)}")
            return False
    
    def verify_login_session(self) -> bool:
        """
        Verify if user is currently logged in
        
        Returns:
            bool: True if logged in, False otherwise
        """
        try:
            # Check if dashboard is displayed
            return self.dashboard_page.is_dashboard_displayed()
        except Exception:
            return False

