"""
Wait utilities for handling element waits and timeouts
"""

from playwright.sync_api import Page, expect
import time
from utils.config import Config
from utils.logger import Logger


class Waits:
    """Wait utility class for handling various wait scenarios"""
    
    def __init__(self, page: Page):
        self.page = page
        self.logger = Logger()
    
    def wait_for_element_visible(self, locator, timeout: int = None):
        """Wait for element to be visible - accepts string or Locator object"""
        from playwright.sync_api import Locator
        timeout = timeout or Config.ELEMENT_WAIT_TIMEOUT
        try:
            if isinstance(locator, Locator):
                locator.wait_for(state="visible", timeout=timeout)
                self.logger.debug(f"Locator element became visible")
            else:
                self.page.locator(locator).wait_for(state="visible", timeout=timeout)
                self.logger.debug(f"Element {locator} became visible")
        except Exception as e:
            locator_str = str(locator) if isinstance(locator, str) else "Locator object"
            self.logger.error(f"Element {locator_str} did not become visible within {timeout}ms: {str(e)}")
            raise
    
    def wait_for_element_hidden(self, locator: str, timeout: int = None):
        """Wait for element to be hidden"""
        timeout = timeout or Config.ELEMENT_WAIT_TIMEOUT
        try:
            self.page.locator(locator).wait_for(state="hidden", timeout=timeout)
            self.logger.debug(f"Element {locator} became hidden")
        except Exception as e:
            self.logger.error(f"Element {locator} did not become hidden within {timeout}ms: {str(e)}")
            raise
    
    def wait_for_element_enabled(self, locator: str, timeout: int = None):
        """Wait for element to be enabled"""
        timeout = timeout or Config.ELEMENT_WAIT_TIMEOUT
        try:
            element = self.page.locator(locator)
            element.wait_for(state="visible", timeout=timeout)
            expect(element).to_be_enabled(timeout=timeout)
            self.logger.debug(f"Element {locator} became enabled")
        except Exception as e:
            self.logger.error(f"Element {locator} did not become enabled within {timeout}ms: {str(e)}")
            raise
    
    def wait_for_element_disappear(self, locator: str, timeout: int = None):
        """Wait for element to disappear from DOM"""
        timeout = timeout or Config.ELEMENT_WAIT_TIMEOUT
        try:
            self.page.locator(locator).wait_for(state="detached", timeout=timeout)
            self.logger.debug(f"Element {locator} disappeared from DOM")
        except Exception as e:
            self.logger.error(f"Element {locator} did not disappear within {timeout}ms: {str(e)}")
            raise
    
    def wait_for_page_load(self, timeout: int = None):
        """Wait for page to fully load"""
        timeout = timeout or Config.PAGE_LOAD_TIMEOUT
        try:
            self.page.wait_for_load_state("domcontentloaded", timeout=timeout)
            self.page.wait_for_load_state("networkidle", timeout=timeout)
            self.logger.debug("Page loaded successfully")
        except Exception as e:
            self.logger.error(f"Page did not load within {timeout}ms: {str(e)}")
            raise
    
    def wait_for_url_change(self, expected_url: str, timeout: int = None):
        """Wait for URL to change to expected value"""
        timeout = timeout or Config.ELEMENT_WAIT_TIMEOUT
        try:
            self.page.wait_for_url(expected_url, timeout=timeout)
            self.logger.debug(f"URL changed to {expected_url}")
        except Exception as e:
            self.logger.error(f"URL did not change to {expected_url} within {timeout}ms: {str(e)}")
            raise
    
    def wait_for_url_contains(self, substring: str, timeout: int = None):
        """Wait for URL to contain a substring"""
        timeout = timeout or Config.ELEMENT_WAIT_TIMEOUT
        try:
            self.page.wait_for_url(lambda url: substring in url, timeout=timeout)
            self.logger.debug(f"URL contains '{substring}'")
        except Exception as e:
            self.logger.error(f"URL did not contain '{substring}' within {timeout}ms: {str(e)}")
            raise
    
    def wait_for_text_to_appear(self, locator: str, text: str, timeout: int = None):
        """Wait for specific text to appear in element"""
        timeout = timeout or Config.ELEMENT_WAIT_TIMEOUT
        try:
            element = self.page.locator(locator)
            element.wait_for(state="visible", timeout=timeout)
            expect(element).to_contain_text(text, timeout=timeout)
            self.logger.debug(f"Text '{text}' appeared in element {locator}")
        except Exception as e:
            self.logger.error(f"Text '{text}' did not appear in element {locator} within {timeout}ms: {str(e)}")
            raise
    
    def wait_for_count(self, locator: str, expected_count: int, timeout: int = None):
        """Wait for specific number of elements to appear"""
        timeout = timeout or Config.ELEMENT_WAIT_TIMEOUT
        try:
            elements = self.page.locator(locator)
            expect(elements).to_have_count(expected_count, timeout=timeout)
            self.logger.debug(f"Found {expected_count} elements matching {locator}")
        except Exception as e:
            self.logger.error(f"Did not find {expected_count} elements matching {locator} within {timeout}ms: {str(e)}")
            raise
    
    def wait_for_ajax_complete(self, timeout: int = None):
        """Wait for AJAX requests to complete"""
        timeout = timeout or Config.AJAX_WAIT_TIMEOUT
        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout)
            self.logger.debug("AJAX requests completed")
        except Exception as e:
            self.logger.error(f"AJAX requests did not complete within {timeout}ms: {str(e)}")
            raise
    
    def wait_for_element_attribute(self, locator: str, attribute: str, value: str, timeout: int = None):
        """Wait for element to have specific attribute value"""
        timeout = timeout or Config.ELEMENT_WAIT_TIMEOUT
        start_time = time.time()
        
        while (time.time() - start_time) * 1000 < timeout:
            element = self.page.locator(locator)
            if element.is_visible():
                actual_value = element.get_attribute(attribute)
                if actual_value == value:
                    self.logger.debug(f"Element {locator} has attribute {attribute}={value}")
                    return
            time.sleep(0.5)
        
        raise TimeoutError(f"Element {locator} did not have attribute {attribute}={value} within {timeout}ms")
    
    def wait_for_element_class(self, locator: str, class_name: str, timeout: int = None):
        """Wait for element to have specific CSS class"""
        timeout = timeout or Config.ELEMENT_WAIT_TIMEOUT
        start_time = time.time()
        
        while (time.time() - start_time) * 1000 < timeout:
            element = self.page.locator(locator)
            if element.is_visible():
                classes = element.get_attribute("class") or ""
                if class_name in classes:
                    self.logger.debug(f"Element {locator} has class {class_name}")
                    return
            time.sleep(0.5)
        
        raise TimeoutError(f"Element {locator} did not have class {class_name} within {timeout}ms")
