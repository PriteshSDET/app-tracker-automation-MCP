"""
Dropdown component for handling select/dropdown elements.
Updated with CSS selectors from App Tracker HTML analysis.
Enhanced with robust synchronization for UAT environment.
"""

from playwright.sync_api import Page
from components.base_component import BaseComponent
from utils.logger import Logger


class Dropdown(BaseComponent):
    """Dropdown component class with App Tracker specific selectors"""
    
    def __init__(self, page: Page, locator: str):
        super().__init__(page, locator)
        self.logger = Logger()
    
    def _wait_for_loading_overlay_to_disappear(self, timeout=5000):
        """Wait for loading spinners, progress bars, or blocking overlays to disappear"""
        try:
            loading_selectors = [
                ".loading-overlay",
                ".spinner",
                ".progress-bar",
                "[class*='loading']",
                "[class*='spinner']",
                "[class*='overlay']",
                ".MuiCircularProgress-root",
                ".MuiBackdrop-root"
            ]
            
            for selector in loading_selectors:
                try:
                    loading_element = self.page.locator(selector).first
                    if loading_element.is_visible(timeout=1000):
                        self.logger.info(f"Waiting for loading element to disappear: {selector}")
                        loading_element.wait_for(state="hidden", timeout=timeout)
                        self.logger.info(f"Loading element disappeared: {selector}")
                except:
                    continue
        except Exception as e:
            self.logger.warning(f"Error waiting for loading overlay: {e}")
    
    def select_option(self, value: str):
        """Select option by value"""
        # Wait for network to settle before interaction
        self.page.wait_for_load_state("networkidle", timeout=10000)
        
        # Wait for element to be fully actionable
        self.element.wait_for(state="attached", timeout=5000)
        self.element.wait_for(state="visible", timeout=5000)
        self.element.wait_for(state="enabled", timeout=5000)
        
        # Wait for loading overlays to disappear
        self._wait_for_loading_overlay_to_disappear()
        
        self.element.select_option(value)
        
        # Wait for network to settle after selection
        self.page.wait_for_load_state("networkidle", timeout=5000)
    
    def select_option_by_label(self, label: str):
        """Select option by visible text"""
        # Wait for network to settle before interaction
        self.page.wait_for_load_state("networkidle", timeout=10000)
        
        # Wait for element to be fully actionable
        self.element.wait_for(state="attached", timeout=5000)
        self.element.wait_for(state="visible", timeout=5000)
        self.element.wait_for(state="enabled", timeout=5000)
        
        # Wait for loading overlays to disappear
        self._wait_for_loading_overlay_to_disappear()
        
        self.element.select_option(label=label)
        
        # Wait for network to settle after selection
        self.page.wait_for_load_state("networkidle", timeout=5000)
    
    def select_option_by_index(self, index: int):
        """Select option by index"""
        # Wait for network to settle before interaction
        self.page.wait_for_load_state("networkidle", timeout=10000)
        
        # Wait for element to be fully actionable
        self.element.wait_for(state="attached", timeout=5000)
        self.element.wait_for(state="visible", timeout=5000)
        self.element.wait_for(state="enabled", timeout=5000)
        
        # Wait for loading overlays to disappear
        self._wait_for_loading_overlay_to_disappear()
        
        self.element.select_option(index=index)
        
        # Wait for network to settle after selection
        self.page.wait_for_load_state("networkidle", timeout=5000)
    
    def get_selected_value(self) -> str:
        """Get selected option value"""
        return self.element.input_value()
    
    def get_selected_text(self) -> str:
        """Get selected option text"""
        return self.element.text_content()
    
    def get_all_options(self) -> list:
        """Get all available options"""
        return self.element.locator("option").all_inner_texts()
    
    def is_multiple(self) -> bool:
        """Check if dropdown allows multiple selection"""
        return self.element.get_attribute("multiple") is not None
    
    def clear_selection(self):
        """Clear selected options"""
        # Wait for network to settle before interaction
        self.page.wait_for_load_state("networkidle", timeout=10000)
        
        # Wait for element to be fully actionable
        self.element.wait_for(state="attached", timeout=5000)
        self.element.wait_for(state="visible", timeout=5000)
        self.element.wait_for(state="enabled", timeout=5000)
        
        # Wait for loading overlays to disappear
        self._wait_for_loading_overlay_to_disappear()
        
        self.element.select_option([])
        
        # Wait for network to settle after clearing
        self.page.wait_for_load_state("networkidle", timeout=5000)


# App Tracker Specific Dropdown Selectors
class AppTrackerDropdown(Dropdown):
    """App Tracker specific dropdown with Material-UI selectors"""
    
    # Filter Button Selector (from HTML)
    FILTER_BUTTON = "button.filterButton.MuiButton-textSizeSmall"
    
    # Sort Dropdown Selector (from HTML)
    SORT_DROPDOWN = "#mui-component-select-sortList"
    
    # Sort Options Container
    SORT_OPTIONS = "ul.MuiList-root[role='listbox']"
    
    def __init__(self, page: Page):
        super().__init__(page, self.FILTER_BUTTON)
    
    def click_filter_button(self):
        """Click the filter button to open filter dropdown"""
        # Wait for network to settle before interaction
        self.page.wait_for_load_state("networkidle", timeout=10000)
        
        filter_btn = self.page.locator(self.FILTER_BUTTON).first
        
        # Wait for element to be fully actionable
        filter_btn.wait_for(state="attached", timeout=5000)
        filter_btn.wait_for(state="visible", timeout=5000)
        filter_btn.wait_for(state="enabled", timeout=5000)
        
        # Wait for loading overlays to disappear
        self._wait_for_loading_overlay_to_disappear()
        
        filter_btn.click()
        
        # Wait for network to settle after click
        self.page.wait_for_load_state("networkidle", timeout=5000)
    
    def click_sort_dropdown(self):
        """Click the sort dropdown to open options"""
        # Wait for network to settle before interaction
        self.page.wait_for_load_state("networkidle", timeout=10000)
        
        sort_dropdown = self.page.locator(self.SORT_DROPDOWN).first
        
        # Wait for element to be fully actionable
        sort_dropdown.wait_for(state="attached", timeout=5000)
        sort_dropdown.wait_for(state="visible", timeout=5000)
        sort_dropdown.wait_for(state="enabled", timeout=5000)
        
        # Wait for loading overlays to disappear
        self._wait_for_loading_overlay_to_disappear()
        
        sort_dropdown.click()
        
        # Wait for network to settle after click
        self.page.wait_for_load_state("networkidle", timeout=5000)
    
    def select_sort_option(self, option_text: str):
        """Select a sort option by text"""
        # Wait for network to settle before interaction
        self.page.wait_for_load_state("networkidle", timeout=10000)
        
        option_locator = f"{self.SORT_OPTIONS} li:has-text('{option_text}')"
        option = self.page.locator(option_locator).first
        
        # Wait for element to be fully actionable
        option.wait_for(state="attached", timeout=5000)
        option.wait_for(state="visible", timeout=5000)
        option.wait_for(state="enabled", timeout=5000)
        
        # Wait for loading overlays to disappear
        self._wait_for_loading_overlay_to_disappear()
        
        option.click()
        
        # Wait for network to settle after selection
        self.page.wait_for_load_state("networkidle", timeout=5000)

