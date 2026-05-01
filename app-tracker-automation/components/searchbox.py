"""
Searchbox component for handling search functionality.
Updated with CSS selectors from App Tracker HTML analysis.
Enhanced with robust synchronization for UAT environment.
"""

from playwright.sync_api import Page
from components.base_component import BaseComponent
from utils.logger import Logger


class SearchBox(BaseComponent):
    """SearchBox component class"""
    
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
    
    def enter_search_term(self, term: str):
        """Enter search term"""
        # Wait for network to settle before interaction
        self.page.wait_for_load_state("networkidle", timeout=10000)
        
        # Wait for element to be fully actionable
        self.element.wait_for(state="attached", timeout=5000)
        self.element.wait_for(state="visible", timeout=5000)
        self.element.wait_for(state="enabled", timeout=5000)
        
        # Wait for loading overlays to disappear
        self._wait_for_loading_overlay_to_disappear()
        
        self.element.fill(term)
        
        # Wait for network to settle after input
        self.page.wait_for_load_state("networkidle", timeout=5000)
    
    def clear_search(self):
        """Clear search input"""
        # Wait for network to settle before interaction
        self.page.wait_for_load_state("networkidle", timeout=10000)
        
        # Wait for element to be fully actionable
        self.element.wait_for(state="attached", timeout=5000)
        self.element.wait_for(state="visible", timeout=5000)
        self.element.wait_for(state="enabled", timeout=5000)
        
        # Wait for loading overlays to disappear
        self._wait_for_loading_overlay_to_disappear()
        
        self.element.fill("")
        
        # Wait for network to settle after clearing
        self.page.wait_for_load_state("networkidle", timeout=5000)
    
    def submit_search(self):
        """Submit search"""
        # Wait for network to settle before interaction
        self.page.wait_for_load_state("networkidle", timeout=10000)
        
        # Wait for element to be fully actionable
        self.element.wait_for(state="attached", timeout=5000)
        self.element.wait_for(state="visible", timeout=5000)
        self.element.wait_for(state="enabled", timeout=5000)
        
        # Wait for loading overlays to disappear
        self._wait_for_loading_overlay_to_disappear()
        
        self.element.press("Enter")
        
        # Wait for network to settle after submission
        self.page.wait_for_load_state("networkidle", timeout=10000)
    
    def search(self, term: str):
        """Perform complete search operation"""
        self.enter_search_term(term)
        self.submit_search()
        
        # Wait for search results to load
        self.page.wait_for_load_state("networkidle", timeout=15000)
    
    def get_search_value(self) -> str:
        """Get current search value"""
        return self.element.input_value()
    
    def is_search_empty(self) -> bool:
        """Check if search box is empty"""
        return len(self.get_search_value()) == 0
    
    def wait_for_search_results(self, timeout: int = 30000):
        """Wait for search results to load"""
        # Wait for network to settle
        self.page.wait_for_load_state("networkidle", timeout=timeout)
        
        # Wait for loading overlays to disappear
        self._wait_for_loading_overlay_to_disappear(timeout)
    
    def get_suggestions(self) -> list:
        """Get search suggestions if available"""
        suggestions_locator = self.page.locator(".search-suggestions li")
        return suggestions_locator.all_inner_texts()
    
    def select_suggestion(self, index: int):
        """Select search suggestion by index"""
        # Wait for network to settle before interaction
        self.page.wait_for_load_state("networkidle", timeout=10000)
        
        suggestions_locator = self.page.locator(".search-suggestions li")
        suggestions = suggestions_locator.all()
        
        if index < len(suggestions):
            # Wait for element to be fully actionable
            suggestions[index].wait_for(state="attached", timeout=5000)
            suggestions[index].wait_for(state="visible", timeout=5000)
            suggestions[index].wait_for(state="enabled", timeout=5000)
            
            # Wait for loading overlays to disappear
            self._wait_for_loading_overlay_to_disappear()
            
            suggestions[index].click()
            
            # Wait for network to settle after selection
            self.page.wait_for_load_state("networkidle", timeout=5000)


# App Tracker Specific Search Box Selectors
class AppTrackerSearchBox(SearchBox):
    """App Tracker specific search box with Material-UI selectors"""
    
    # Search Input Selector (from HTML)
    SEARCH_INPUT = "input.navbar-search"
    
    # Search Container
    SEARCH_CONTAINER = ".MuiBox-root.jss58"
    
    def __init__(self, page: Page):
        super().__init__(page, self.SEARCH_INPUT)
    
    def enter_search_term(self, term: str):
        """Enter search term in App Tracker search box"""
        # Wait for network to settle before interaction
        self.page.wait_for_load_state("networkidle", timeout=10000)
        
        search_input = self.page.locator(self.SEARCH_INPUT).first
        
        # Wait for element to be fully actionable
        search_input.wait_for(state="attached", timeout=5000)
        search_input.wait_for(state="visible", timeout=5000)
        search_input.wait_for(state="enabled", timeout=5000)
        
        # Wait for loading overlays to disappear
        self._wait_for_loading_overlay_to_disappear()
        
        search_input.fill(term)
        
        # Wait for network to settle after input
        self.page.wait_for_load_state("networkidle", timeout=5000)
