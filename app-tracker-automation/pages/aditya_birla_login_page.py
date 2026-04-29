"""
Aditya Birla Sun Life Insurance Login Page
Enhanced login page for UAT environment
"""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from locators.aditya_birla_locators import AdityaBirlaLocators
from utils.logger import Logger
from utils.waits import Waits


class AdityaBirlaLoginPage(BasePage):
    """Aditya Birla Sun Life Insurance login page"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = AdityaBirlaLocators()
        self.waits = Waits(page)
    
    def load(self):
        """Load Aditya Birla UAT login page"""
        self.logger.info("Loading Aditya Birla UAT login page")
        self.navigate_to(self.locators.login_page["url"])
        self.waits.wait_for_page_load()
    
    def is_login_page_displayed(self) -> bool:
        """Check if login page is displayed"""
        try:
            # Check URL
            current_url = self.page.url
            if "leapuat.adityabirlasunlifeinsurance.com" not in current_url:
                return False
            
            # Check key elements
            username_visible = self.is_element_visible(self.locators.login_page["username_input"])
            password_visible = self.is_element_visible(self.locators.login_page["password_input"])
            login_button_visible = self.is_element_visible(self.locators.login_page["login_button"])
            
            return username_visible and password_visible and login_button_visible
            
        except Exception as e:
            self.logger.error(f"Error checking login page display: {str(e)}")
            return False
    
    def enter_credentials(self, username: str, password: str):
        """Enter login credentials"""
        try:
            self.logger.info(f"Entering credentials for user: {username}")
            
            # Find and fill username
            username_input = self.page.locator(self.locators.login_page["username_input"]).first
            self.waits.wait_for_element_visible(self.locators.login_page["username_input"])
            username_input.fill(username)
            
            # Find and fill password
            password_input = self.page.locator(self.locators.login_page["password_input"]).first
            self.waits.wait_for_element_visible(self.locators.login_page["password_input"])
            password_input.fill(password)
            
            # Verify password masking
            password_type = password_input.get_attribute("type")
            if password_type != "password":
                self.logger.warning("Password field is not properly masked")
            
            self.logger.info("Credentials entered successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to enter credentials: {str(e)}")
            raise
    
    def click_login_button(self):
        """Click the login button"""
        try:
            self.logger.info("Clicking login button")
            
            login_button = self.page.locator(self.locators.login_page["login_button"]).first
            self.waits.wait_for_element_enabled(self.locators.login_page["login_button"])
            login_button.click()
            
            self.logger.info("Login button clicked")
            
        except Exception as e:
            self.logger.error(f"Failed to click login button: {str(e)}")
            raise
    
    def login(self, username: str, password: str):
        """Perform complete login flow"""
        try:
            self.logger.info(f"Starting login flow for user: {username}")
            
            # Load login page
            self.load()
            
            # Verify page is displayed
            if not self.is_login_page_displayed():
                raise Exception("Login page is not properly displayed")
            
            # Enter credentials
            self.enter_credentials(username, password)
            
            # Click login
            self.click_login_button()
            
            # Wait for redirect
            self.page.wait_for_timeout(3000)
            
            # Check if login was successful (redirected away from login page)
            current_url = self.page.url
            if "#/login" in current_url:
                # Check for error message
                error_visible = self.is_element_visible(self.locators.login_page["error_message"])
                if error_visible:
                    error_text = self.get_error_message()
                    self.logger.error(f"Login failed with error: {error_text}")
                    return False
                else:
                    self.logger.error("Login failed - still on login page")
                    return False
            else:
                self.logger.info("Login successful - redirected from login page")
                return True
                
        except Exception as e:
            self.logger.error(f"Login flow failed: {str(e)}")
            return False
    
    def get_error_message(self) -> str:
        """Get login error message"""
        try:
            error_element = self.page.locator(self.locators.login_page["error_message"]).first
            if error_element.is_visible():
                return error_element.text_content()
            return ""
        except:
            return ""
    
    def verify_uat_badge(self) -> bool:
        """Verify UAT badge is visible"""
        return self.is_element_visible(self.locators.login_page["uat_badge"])
    
    def verify_branding(self) -> bool:
        """Verify Aditya Birla branding is visible"""
        return self.is_element_visible(self.locators.login_page["branding_header"])
    
    def wait_for_page_load(self, timeout: int = 10000):
        """Wait for login page to fully load"""
        try:
            # Wait for URL to contain login
            self.waits.wait_for_url_contains("#/login", timeout)
            
            # Wait for key elements to be visible
            self.waits.wait_for_element_visible(self.locators.login_page["username_input"], timeout)
            self.waits.wait_for_element_visible(self.locators.login_page["password_input"], timeout)
            self.waits.wait_for_element_visible(self.locators.login_page["login_button"], timeout)
            
            self.logger.info("Login page loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Login page load timeout: {str(e)}")
            raise
    
    def clear_credentials(self):
        """Clear username and password fields"""
        try:
            username_input = self.page.locator(self.locators.login_page["username_input"]).first
            password_input = self.page.locator(self.locators.login_page["password_input"]).first
            
            username_input.fill("")
            password_input.fill("")
            
            self.logger.info("Credentials cleared")
            
        except Exception as e:
            self.logger.error(f"Failed to clear credentials: {str(e)}")
    
    def is_username_focused(self) -> bool:
        """Check if username field has focus"""
        try:
            username_input = self.page.locator(self.locators.login_page["username_input"]).first
            return username_input.is_focused()
        except:
            return False
    
    def is_password_focused(self) -> bool:
        """Check if password field has focus"""
        try:
            password_input = self.page.locator(self.locators.login_page["password_input"]).first
            return password_input.is_focused()
        except:
            return False
    
    def get_page_title(self) -> str:
        """Get page title"""
        return self.page.title()
    
    def take_screenshot(self, name: str = "login_page"):
        """Take screenshot of login page"""
        timestamp = self.page.evaluate("new Date().toISOString().replace(/[:.]/g, '-')")
        filename = f"{name}_{timestamp}.png"
        self.page.screenshot(path=f"screenshots/{filename}", full_page=True)
        self.logger.info(f"Screenshot saved: {filename}")
