"""
Assertion utilities for test validations
"""

from playwright.sync_api import Page, expect
from utils.logger import Logger


class Assertions:
    """Assertion utility class for test validations"""
    
    def __init__(self, page: Page):
        self.page = page
        self.logger = Logger()
    
    def assert_element_visible(self, locator: str, message: str = None):
        """Assert element is visible"""
        try:
            element = self.page.locator(locator)
            expect(element).to_be_visible()
            self.logger.info(f"Element {locator} is visible")
        except Exception as e:
            error_msg = message or f"Element {locator} should be visible"
            self.logger.error(f"Assertion failed: {error_msg}")
            raise AssertionError(error_msg) from e
    
    def assert_element_hidden(self, locator: str, message: str = None):
        """Assert element is hidden"""
        try:
            element = self.page.locator(locator)
            expect(element).to_be_hidden()
            self.logger.info(f"Element {locator} is hidden")
        except Exception as e:
            error_msg = message or f"Element {locator} should be hidden"
            self.logger.error(f"Assertion failed: {error_msg}")
            raise AssertionError(error_msg) from e
    
    def assert_element_enabled(self, locator: str, message: str = None):
        """Assert element is enabled"""
        try:
            element = self.page.locator(locator)
            expect(element).to_be_enabled()
            self.logger.info(f"Element {locator} is enabled")
        except Exception as e:
            error_msg = message or f"Element {locator} should be enabled"
            self.logger.error(f"Assertion failed: {error_msg}")
            raise AssertionError(error_msg) from e
    
    def assert_element_disabled(self, locator: str, message: str = None):
        """Assert element is disabled"""
        try:
            element = self.page.locator(locator)
            expect(element).to_be_disabled()
            self.logger.info(f"Element {locator} is disabled")
        except Exception as e:
            error_msg = message or f"Element {locator} should be disabled"
            self.logger.error(f"Assertion failed: {error_msg}")
            raise AssertionError(error_msg) from e
    
    def assert_text_equals(self, locator: str, expected_text: str, message: str = None):
        """Assert element text equals expected text"""
        try:
            element = self.page.locator(locator)
            expect(element).to_have_text(expected_text)
            self.logger.info(f"Element {locator} text equals '{expected_text}'")
        except Exception as e:
            actual_text = element.text_content()
            error_msg = message or f"Expected text '{expected_text}', but got '{actual_text}'"
            self.logger.error(f"Assertion failed: {error_msg}")
            raise AssertionError(error_msg) from e
    
    def assert_text_contains(self, locator: str, expected_text: str, message: str = None):
        """Assert element text contains expected text"""
        try:
            element = self.page.locator(locator)
            expect(element).to_contain_text(expected_text)
            self.logger.info(f"Element {locator} text contains '{expected_text}'")
        except Exception as e:
            actual_text = element.text_content()
            error_msg = message or f"Expected text to contain '{expected_text}', but got '{actual_text}'"
            self.logger.error(f"Assertion failed: {error_msg}")
            raise AssertionError(error_msg) from e
    
    def assert_attribute_equals(self, locator: str, attribute: str, expected_value: str, message: str = None):
        """Assert element attribute equals expected value"""
        try:
            element = self.page.locator(locator)
            expect(element).to_have_attribute(attribute, expected_value)
            self.logger.info(f"Element {locator} attribute {attribute} equals '{expected_value}'")
        except Exception as e:
            actual_value = element.get_attribute(attribute)
            error_msg = message or f"Expected attribute {attribute} to be '{expected_value}', but got '{actual_value}'"
            self.logger.error(f"Assertion failed: {error_msg}")
            raise AssertionError(error_msg) from e
    
    def assert_url_equals(self, expected_url: str, message: str = None):
        """Assert current URL equals expected URL"""
        try:
            expect(self.page).to_have_url(expected_url)
            self.logger.info(f"Current URL equals '{expected_url}'")
        except Exception as e:
            actual_url = self.page.url
            error_msg = message or f"Expected URL '{expected_url}', but got '{actual_url}'"
            self.logger.error(f"Assertion failed: {error_msg}")
            raise AssertionError(error_msg) from e
    
    def assert_url_contains(self, expected_url: str, message: str = None):
        """Assert current URL contains expected URL"""
        try:
            expect(self.page).to_have_url(expected_url, timeout=5000)
            self.logger.info(f"Current URL contains '{expected_url}'")
        except Exception as e:
            actual_url = self.page.url
            # Check if expected_url is actually contained in actual_url
            if expected_url in actual_url:
                self.logger.info(f"Current URL contains '{expected_url}' - manually verified")
            else:
                error_msg = message or f"Expected URL to contain '{expected_url}', but got '{actual_url}'"
                self.logger.error(f"Assertion failed: {error_msg}")
                raise AssertionError(error_msg) from e
    
    def assert_title_equals(self, expected_title: str, message: str = None):
        """Assert page title equals expected title"""
        try:
            expect(self.page).to_have_title(expected_title)
            self.logger.info(f"Page title equals '{expected_title}'")
        except Exception as e:
            actual_title = self.page.title()
            error_msg = message or f"Expected title '{expected_title}', but got '{actual_title}'"
            self.logger.error(f"Assertion failed: {error_msg}")
            raise AssertionError(error_msg) from e
    
    def assert_element_count(self, locator: str, expected_count: int, message: str = None):
        """Assert number of elements equals expected count"""
        try:
            elements = self.page.locator(locator)
            expect(elements).to_have_count(expected_count)
            self.logger.info(f"Found {expected_count} elements matching {locator}")
        except Exception as e:
            actual_count = len(elements.all())
            error_msg = message or f"Expected {expected_count} elements, but found {actual_count}"
            self.logger.error(f"Assertion failed: {error_msg}")
            raise AssertionError(error_msg) from e
    
    def assert_element_selected(self, locator: str, message: str = None):
        """Assert element is selected"""
        try:
            element = self.page.locator(locator)
            expect(element).to_be_checked()
            self.logger.info(f"Element {locator} is selected")
        except Exception as e:
            error_msg = message or f"Element {locator} should be selected"
            self.logger.error(f"Assertion failed: {error_msg}")
            raise AssertionError(error_msg) from e
    
    def assert_element_not_selected(self, locator: str, message: str = None):
        """Assert element is not selected"""
        try:
            element = self.page.locator(locator)
            expect(element).not_to_be_checked()
            self.logger.info(f"Element {locator} is not selected")
        except Exception as e:
            error_msg = message or f"Element {locator} should not be selected"
            self.logger.error(f"Assertion failed: {error_msg}")
            raise AssertionError(error_msg) from e
    
    def assert_element_focused(self, locator: str, message: str = None):
        """Assert element has focus"""
        try:
            element = self.page.locator(locator)
            expect(element).to_be_focused()
            self.logger.info(f"Element {locator} has focus")
        except Exception as e:
            error_msg = message or f"Element {locator} should have focus"
            self.logger.error(f"Assertion failed: {error_msg}")
            raise AssertionError(error_msg) from e
    
    def assert_page_loaded(self, message: str = None):
        """Assert page is fully loaded"""
        try:
            expect(self.page).to_have_load_state("domcontentloaded")
            expect(self.page).to_have_load_state("networkidle")
            self.logger.info("Page is fully loaded")
        except Exception as e:
            error_msg = message or "Page should be fully loaded"
            self.logger.error(f"Assertion failed: {error_msg}")
            raise AssertionError(error_msg) from e

