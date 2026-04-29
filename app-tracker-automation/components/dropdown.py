"""
Dropdown component for handling select/dropdown elements.
"""

from playwright.sync_api import Page
from components.base_component import BaseComponent


class Dropdown(BaseComponent):
    """Dropdown component class"""
    
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
