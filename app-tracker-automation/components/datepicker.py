"""
DatePicker component for handling date selection.
"""

from playwright.sync_api import Page
from components.base_component import BaseComponent


class DatePicker(BaseComponent):
    """DatePicker component class"""
    
    def __init__(self, page: Page, locator: str):
        super().__init__(page, locator)
    
    def select_date(self, date: str):
        """Select date in format YYYY-MM-DD"""
        self.element.fill(date)
    
    def select_today(self):
        """Select today's date"""
        today_button = self.element.locator("button[data-action='today']")
        today_button.click()
    
    def open_calendar(self):
        """Open calendar popup"""
        self.element.click()
    
    def close_calendar(self):
        """Close calendar popup"""
        self.element.press("Escape")
    
    def get_selected_date(self) -> str:
        """Get selected date"""
        return self.element.input_value()
    
    def select_year(self, year: int):
        """Select specific year"""
        year_dropdown = self.page.locator(".datepicker-year")
        year_dropdown.click()
        year_option = self.page.locator(f".datepicker-year option[value='{year}']")
        year_option.click()
    
    def select_month(self, month: int):
        """Select specific month (1-12)"""
        month_dropdown = self.page.locator(".datepicker-month")
        month_dropdown.click()
        month_option = self.page.locator(f".datepicker-month option[value='{month - 1}']")
        month_option.click()
    
    def select_day(self, day: int):
        """Select specific day"""
        day_button = self.page.locator(f".datepicker-day[data-day='{day}']")
        day_button.click()
    
    def navigate_next_month(self):
        """Navigate to next month"""
        next_button = self.page.locator(".datepicker-next")
        next_button.click()
    
    def navigate_previous_month(self):
        """Navigate to previous month"""
        prev_button = self.page.locator(".datepicker-previous")
        prev_button.click()
    
    def clear_date(self):
        """Clear selected date"""
        self.element.fill("")
    
    def is_date_valid(self) -> bool:
        """Check if entered date is valid"""
        # This would need to be implemented based on specific validation logic
        return True
