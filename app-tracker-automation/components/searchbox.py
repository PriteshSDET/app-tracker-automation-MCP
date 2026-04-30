"""
Searchbox component for handling search functionality.
Updated with CSS selectors from App Tracker HTML analysis.
"""

from playwright.sync_api import Page
from components.base_component import BaseComponent


class SearchBox(BaseComponent):
    """SearchBox component class"""
    
    def __init__(self, page: Page, locator: str):
        super().__init__(page, locator)
    
    def enter_search_term(self, term: str):
        """Enter search term"""
        self.element.fill(term)
    
    def clear_search(self):
        """Clear search input"""
        self.element.fill("")
    
    def submit_search(self):
        """Submit search"""
        self.element.press("Enter")
    
    def search(self, term: str):
        """Perform complete search operation"""
        self.enter_search_term(term)
        self.submit_search()
    
    def get_search_value(self) -> str:
        """Get current search value"""
        return self.element.input_value()
    
    def is_search_empty(self) -> bool:
        """Check if search box is empty"""
        return len(self.get_search_value()) == 0
    
    def wait_for_search_results(self, timeout: int = 30000):
        """Wait for search results to load"""
        # This would need to be implemented based on specific page behavior
        self.page.wait_for_timeout(1000)  # Placeholder
    
    def get_suggestions(self) -> list:
        """Get search suggestions if available"""
        suggestions_locator = self.page.locator(".search-suggestions li")
        return suggestions_locator.all_inner_texts()
    
    def select_suggestion(self, index: int):
        """Select search suggestion by index"""
        suggestions_locator = self.page.locator(".search-suggestions li")
        suggestions = suggestions_locator.all()
        if index < len(suggestions):
            suggestions[index].click()


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
        self.page.locator(self.SEARCH_INPUT).first.fill(term)
