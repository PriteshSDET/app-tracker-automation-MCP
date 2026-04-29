"""
Table component for handling data tables.
"""

from playwright.sync_api import Page
from components.base_component import BaseComponent


class Table(BaseComponent):
    """Table component class"""
    
    def __init__(self, page: Page, locator: str):
        super().__init__(page, locator)
    
    def get_row_count(self) -> int:
        """Get number of rows in table"""
        rows = self.element.locator("tbody tr")
        return len(rows.all())
    
    def get_column_count(self) -> int:
        """Get number of columns in table"""
        headers = self.element.locator("thead th")
        return len(headers.all())
    
    def get_cell_text(self, row_index: int, column_index: int) -> str:
        """Get text from specific cell"""
        cell = self.element.locator(f"tbody tr:nth-child({row_index + 1}) td:nth-child({column_index + 1})")
        return cell.text_content()
    
    def get_row_data(self, row_index: int) -> list:
        """Get all data from specific row"""
        row = self.element.locator(f"tbody tr:nth-child({row_index + 1})")
        cells = row.locator("td")
        return cells.all_inner_texts()
    
    def get_column_data(self, column_index: int) -> list:
        """Get all data from specific column"""
        cells = self.element.locator(f"tbody tr td:nth-child({column_index + 1})")
        return cells.all_inner_texts()
    
    def get_all_data(self) -> list:
        """Get all table data as 2D list"""
        rows = self.element.locator("tbody tr")
        all_data = []
        for i in range(len(rows.all())):
            all_data.append(self.get_row_data(i))
        return all_data
    
    def find_row_by_text(self, search_text: str) -> int:
        """Find row index containing specific text"""
        rows = self.element.locator("tbody tr")
        for i, row in enumerate(rows.all()):
            if search_text in row.text_content():
                return i
        return -1
    
    def click_row(self, row_index: int):
        """Click on specific row"""
        row = self.element.locator(f"tbody tr:nth-child({row_index + 1})")
        row.click()
    
    def sort_by_column(self, column_index: int):
        """Sort table by specific column"""
        header = self.element.locator(f"thead th:nth-child({column_index + 1})")
        header.click()
    
    def is_row_selected(self, row_index: int) -> bool:
        """Check if specific row is selected"""
        row = self.element.locator(f"tbody tr:nth-child({row_index + 1})")
        return "selected" in row.get_attribute("class")
