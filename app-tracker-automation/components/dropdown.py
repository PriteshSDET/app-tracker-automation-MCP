"""
Dropdown component for handling select/dropdown elements.
Updated with CSS selectors from App Tracker HTML analysis.
"""

from playwright.sync_api import Page
from components.base_component import BaseComponent


class Dropdown(BaseComponent):
    """Dropdown component class with App Tracker specific selectors"""
    
    def __init__(self, page: Page, locator: str):
        super().__init__(page, locator)
    
    def select_option(self, value: str):
        """Select option by value"""
        self.element.select_option(value)
    
    def select_option_by_label(self, label: str):
        """Select option by visible text"""
        self.element.select_option(label=label)
    
    def select_option_by_index(self, index: int):
        """Select option by index"""
        self.element.select_option(index=index)
    
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
        self.element.select_option([])


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
        self.page.locator(self.FILTER_BUTTON).first.click()
    
    def click_sort_dropdown(self):
        """Click the sort dropdown to open options"""
        self.page.locator(self.SORT_DROPDOWN).first.click()
    
    def select_sort_option(self, option_text: str):
        """Select a sort option by text"""
        option_locator = f"{self.SORT_OPTIONS} li:has-text('{option_text}')"
        self.page.locator(option_locator).first.click()
