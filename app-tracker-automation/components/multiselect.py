"""
Multi-select component for handling multiple selection elements.
"""

from playwright.sync_api import Page
from components.base_component import BaseComponent


class MultiSelect(BaseComponent):
    """Multi-select component class"""
    
    def __init__(self, page: Page, locator: str):
        super().__init__(page, locator)
    
    def select_options(self, values: list):
        """Select multiple options by values"""
        self.element.select_option(values)
    
    def select_options_by_labels(self, labels: list):
        """Select multiple options by visible text"""
        self.element.select_option(labels=labels)
    
    def deselect_all(self):
        """Deselect all options"""
        self.element.select_option([])
    
    def get_selected_values(self) -> list:
        """Get all selected option values"""
        return self.element.input_value()
    
    def get_selected_texts(self) -> list:
        """Get all selected option texts"""
        selected_options = self.element.locator("option:checked")
        return selected_options.all_inner_texts()
    
    def get_all_available_options(self) -> list:
        """Get all available options"""
        return self.element.locator("option").all_inner_texts()
    
    def is_option_selected(self, value: str) -> bool:
        """Check if specific option is selected"""
        option = self.element.locator(f"option[value='{value}']")
        return option.is_checked()
    
    def get_selected_count(self) -> int:
        """Get number of selected options"""
        return len(self.element.locator("option:checked").all())
