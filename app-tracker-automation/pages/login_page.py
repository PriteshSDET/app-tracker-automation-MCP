"""
Login Page Object Model
Handles login functionality for the insurance portal
"""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from locators.login_locators import LoginLocators


class LoginPage(BasePage):
    """Login page object"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.locators = LoginLocators()
    
    def load(self):
        """Load login page"""
        self.navigate_to("/login")
        self.wait_for_page_load()
    
    def login(self, username: str, password: str):
        """Perform login with credentials"""
        self.logger.info(f"Attempting login for user: {username}")
        
        # Enter username
        self.page.locator(self.locators.username_input).fill(username)
        
        # Enter password
        self.page.locator(self.locators.password_input).fill(password)
        
        # Click login button
        self.page.locator(self.locators.login_button).click()
        
        # Wait for login to complete
        self.waits.wait_for_element_disappear(self.locators.login_button)
    
    def is_login_page_displayed(self) -> bool:
        """Check if login page is displayed"""
        return self.is_element_visible(self.locators.login_form)
    
    def get_error_message(self) -> str:
        """Get login error message"""
        return self.page.locator(self.locators.error_message).text_content()
    
    def is_login_successful(self) -> bool:
        """Check if login was successful"""
        return not self.is_element_visible(self.locators.login_form)

