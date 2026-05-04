"""
Policy List Table Component Utility
=====================================
Source: components/Policy list table.md
UI:
  Columns: App. No. | Proposer Name | Plan Name | App. Recv. On |
           Modal Premium | Policy No. | Policy Status | R&A Date | (arrow)
  Sorting: R&A Date has aria-sort='descending' (default)
  Table:   div.overflow-auto > table.w-full (min-width: 1120px)
  Rows:    tbody tr.group[class*='cursor-pointer']
  Status badge: span.inline-flex[class*='bg-amber'] or bg-success etc.

Selectors derived from actual OuterHTML:
  Table wrapper:       div.overflow-auto
  Table:               div.overflow-auto table.w-full
  Header row:          thead tr
  Header cells:        thead th  (contain column names in span)
  Body rows:           tbody tr
  App No cell:         td:nth-child(1) span
  Proposer cell:       td:nth-child(2) span
  Plan Name cell:      td:nth-child(3) span
  App Recv On cell:    td:nth-child(4) span
  Modal Premium cell:  td:nth-child(5) span
  Policy No cell:      td:nth-child(6) span
  Policy Status badge: td:nth-child(7) span.inline-flex
  R&A Date cell:       td:nth-child(8) span
  Sort indicator (R&A):th[aria-sort='descending']
"""

import logging
from typing import Optional
from playwright.sync_api import Page, Locator


class PolicyListTable:
    """
    Utility class for the Policy List Table component.

    Usage:
        table = PolicyListTable(page)
        table.validate_all()
        table.get_row_count()                          -> 10
        table.get_headers()                            -> ['App. No.', 'Proposer Name', ...]
        table.get_row_data(0)                          -> {'app_no': 'LA53544020', ...}
        table.get_all_rows_data()                      -> [{'app_no': ...}, ...]
        table.click_row(0)
        table.sort_by_column('App. No.')
        table.get_active_sort_column()                 -> 'R&A Date'
        table.find_row_by_app_no('LA53544020')         -> Locator
        table.get_policy_status_badge(row_index=0)     -> 'App Form Pending'
    """

    # --- Selectors (from actual OuterHTML) ---
    TABLE_WRAPPER   = "div.overflow-auto"
    TABLE           = "div.overflow-auto table.w-full"
    THEAD           = "div.overflow-auto table thead"
    TBODY           = "div.overflow-auto table tbody"
    HEADER_CELLS    = "div.overflow-auto table thead th"
    BODY_ROWS       = "div.overflow-auto table tbody tr"

    # Column indices (1-based for CSS :nth-child)
    COL_APP_NO      = 1
    COL_PROPOSER    = 2
    COL_PLAN        = 3
    COL_APP_DATE    = 4
    COL_PREMIUM     = 5
    COL_POLICY_NO   = 6
    COL_STATUS      = 7
    COL_RA_DATE     = 8

    # Status badge classes (from actual HTML)
    STATUS_BADGE_SEL = "span.inline-flex.items-center.rounded.font-medium"

    def __init__(self, page: Page, timeout: int = 15000):
        self.page = page
        self.timeout = timeout
        self.logger = logging.getLogger(self.__class__.__name__)

    # ------------------------------------------------------------------ #
    #  Private helpers
    # ------------------------------------------------------------------ #

    def _table(self) -> Locator:
        return self.page.locator(self.TABLE).first

    def _rows(self) -> list[Locator]:
        return self.page.locator(self.BODY_ROWS).all()

    def _row(self, index: int) -> Locator:
        return self.page.locator(self.BODY_ROWS).nth(index)

    def _cell_text(self, row: Locator, col_index: int) -> str:
        """Extracts text from a specific column cell (1-based index)."""
        try:
            cell = row.locator(f"td:nth-child({col_index})").first
            span = cell.locator("span").first
            return (span.text_content(timeout=2000) or "").strip()
        except Exception:
            return ""

    # ------------------------------------------------------------------ #
    #  Visibility Checks
    # ------------------------------------------------------------------ #

    def is_visible(self) -> bool:
        try:
            return self._table().is_visible(timeout=3000)
        except Exception:
            return False

    def validate_visible(self) -> bool:
        try:
            wrapper = self.page.locator(self.TABLE_WRAPPER).first
            wrapper.wait_for(state="attached", timeout=self.timeout)
            wrapper.wait_for(state="visible",  timeout=self.timeout)
            table = self._table()
            table.wait_for(state="visible", timeout=self.timeout)
            self.logger.info("[OK] Policy List Table is visible")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Policy List Table not visible: {e}")
            return False

    # ------------------------------------------------------------------ #
    #  Read Headers
    # ------------------------------------------------------------------ #

    def get_headers(self) -> list[str]:
        """Returns list of column header labels."""
        headers = []
        try:
            cells = self.page.locator(self.HEADER_CELLS).all()
            for cell in cells:
                # Header text is in span.inline-flex or direct text
                span = cell.locator("span.inline-flex").first
                try:
                    txt = span.text_content(timeout=1000) or ""
                except Exception:
                    txt = cell.text_content(timeout=1000) or ""
                # Remove SVG artifacts if any - take only the readable text
                txt = txt.strip()
                if txt:
                    headers.append(txt)
            self.logger.info(f"[OK] Table headers: {headers}")
        except Exception as e:
            self.logger.warning(f"[WARN] Could not read table headers: {e}")
        return headers

    def validate_headers(self) -> bool:
        """Checks that all expected columns are present."""
        expected = [
            "App. No.", "Proposer Name", "Plan Name", "App. Recv. On",
            "Modal Premium", "Policy No.", "Policy Status", "R&A Date"
        ]
        headers = self.get_headers()
        missing = [h for h in expected if not any(h in hdr for hdr in headers)]
        if missing:
            self.logger.warning(f"[WARN] Missing expected columns: {missing}")
            return False
        self.logger.info("[OK] All expected columns present")
        return True

    # ------------------------------------------------------------------ #
    #  Read Rows
    # ------------------------------------------------------------------ #

    def get_row_count(self) -> int:
        """Returns number of data rows currently visible in the table body."""
        try:
            rows = self._rows()
            count = len(rows)
            self.logger.info(f"[OK] Table row count: {count}")
            return count
        except Exception as e:
            self.logger.warning(f"[WARN] Could not count rows: {e}")
            return 0

    def get_row_data(self, index: int) -> dict:
        """
        Returns a dict of all column values for the row at the given index (0-based).
        Keys: app_no, proposer_name, plan_name, app_recv_on, modal_premium,
              policy_no, policy_status, ra_date
        """
        data = {}
        try:
            row = self._row(index)
            row.wait_for(state="attached", timeout=self.timeout)
            data["app_no"]        = self._cell_text(row, self.COL_APP_NO)
            data["proposer_name"] = self._cell_text(row, self.COL_PROPOSER)
            data["plan_name"]     = self._cell_text(row, self.COL_PLAN)
            data["app_recv_on"]   = self._cell_text(row, self.COL_APP_DATE)
            data["modal_premium"] = self._cell_text(row, self.COL_PREMIUM)
            data["policy_no"]     = self._cell_text(row, self.COL_POLICY_NO)
            data["policy_status"] = self.get_policy_status_badge(row_index=index)
            data["ra_date"]       = self._cell_text(row, self.COL_RA_DATE)
            self.logger.info(f"[OK] Row {index} data: {data}")
        except Exception as e:
            self.logger.warning(f"[WARN] Could not read row {index} data: {e}")
        return data

    def get_all_rows_data(self) -> list[dict]:
        """Returns data for all visible rows."""
        all_data = []
        count = self.get_row_count()
        for i in range(count):
            all_data.append(self.get_row_data(i))
        return all_data

    def get_policy_status_badge(self, row_index: int) -> str:
        """Returns the Policy Status badge text for the given row (e.g. 'App Form Pending')."""
        try:
            row = self._row(row_index)
            status_cell = row.locator(f"td:nth-child({self.COL_STATUS})").first
            badge = status_cell.locator(self.STATUS_BADGE_SEL).first
            txt = badge.text_content(timeout=2000) or ""
            return txt.strip()
        except Exception as e:
            self.logger.warning(f"[WARN] Could not read status badge for row {row_index}: {e}")
            return ""

    def get_column_values(self, col_index: int) -> list[str]:
        """Returns all values in a specific column (1-based index) for visible rows."""
        values = []
        try:
            rows = self._rows()
            for row in rows:
                values.append(self._cell_text(row, col_index))
        except Exception as e:
            self.logger.warning(f"[WARN] Could not read column {col_index}: {e}")
        return values

    # ------------------------------------------------------------------ #
    #  Find / Search Rows
    # ------------------------------------------------------------------ #

    def find_row_by_app_no(self, app_no: str) -> Optional[Locator]:
        """Returns the row Locator for a given App Number, or None if not found."""
        try:
            row = self.page.locator(
                f"div.overflow-auto table tbody tr:has(span:text-is('{app_no}'))"
            ).first
            if row.is_visible(timeout=3000):
                self.logger.info(f"[OK] Found row for App No: {app_no}")
                return row
        except Exception:
            pass
        self.logger.warning(f"[WARN] Row not found for App No: {app_no}")
        return None

    def find_rows_by_status(self, status: str) -> list[Locator]:
        """Returns all rows where Policy Status badge matches the given status text."""
        matched = []
        try:
            rows = self._rows()
            for row in rows:
                try:
                    badge = row.locator(
                        f"td:nth-child({self.COL_STATUS}) {self.STATUS_BADGE_SEL}"
                    ).first
                    txt = badge.text_content(timeout=1000) or ""
                    if status.lower() in txt.lower():
                        matched.append(row)
                except Exception:
                    continue
            self.logger.info(f"[OK] Found {len(matched)} rows with status '{status}'")
        except Exception as e:
            self.logger.warning(f"[WARN] Error finding rows by status: {e}")
        return matched

    # ------------------------------------------------------------------ #
    #  Interactions
    # ------------------------------------------------------------------ #

    def click_row(self, index: int) -> bool:
        """Clicks on a table row to open the application detail view."""
        try:
            row = self._row(index)
            row.wait_for(state="visible", timeout=self.timeout)
            row.click()
            self.page.wait_for_load_state("networkidle", timeout=self.timeout)
            self.logger.info(f"[OK] Clicked row {index}")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Could not click row {index}: {e}")
            return False

    def click_row_by_app_no(self, app_no: str) -> bool:
        """Finds and clicks the row with the given App Number."""
        row = self.find_row_by_app_no(app_no)
        if not row:
            return False
        try:
            row.click()
            self.page.wait_for_load_state("networkidle", timeout=self.timeout)
            self.logger.info(f"[OK] Clicked row for App No: {app_no}")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Could not click row for App No '{app_no}': {e}")
            return False

    def sort_by_column(self, column_header: str) -> bool:
        """
        Clicks the column header to trigger sorting.
        column_header: exact text as shown e.g. 'App. No.', 'R&A Date', 'Modal Premium'
        """
        try:
            # Headers with sort indicator contain aria-sort attribute
            header = self.page.locator(
                f"div.overflow-auto thead th:has(span:has-text('{column_header}'))"
            ).first
            header.wait_for(state="visible", timeout=self.timeout)
            header.click()
            self.page.wait_for_load_state("networkidle", timeout=self.timeout)
            self.logger.info(f"[OK] Sorted by column: {column_header}")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Could not sort by '{column_header}': {e}")
            return False

    def get_active_sort_column(self) -> Optional[str]:
        """Returns the header text of the currently sorted column (has aria-sort attr)."""
        try:
            sorted_th = self.page.locator(
                "div.overflow-auto thead th[aria-sort]"
            ).first
            if sorted_th.is_visible(timeout=3000):
                txt = sorted_th.locator("span.inline-flex").first.text_content(timeout=2000) or ""
                sort_dir = sorted_th.get_attribute("aria-sort", timeout=1000)
                self.logger.info(f"[OK] Active sort: '{txt.strip()}' ({sort_dir})")
                return txt.strip()
        except Exception as e:
            self.logger.warning(f"[WARN] Could not determine active sort column: {e}")
        return None

    def get_active_sort_direction(self) -> Optional[str]:
        """Returns 'ascending' or 'descending' for the currently sorted column."""
        try:
            sorted_th = self.page.locator("div.overflow-auto thead th[aria-sort]").first
            return sorted_th.get_attribute("aria-sort", timeout=3000)
        except Exception:
            return None

    # ------------------------------------------------------------------ #
    #  Composite Validation
    # ------------------------------------------------------------------ #

    def validate_all(self) -> dict:
        """
        Full validation of the Policy List Table component.
        Returns result dict with keys: visible, headers_valid, row_count,
        first_row, active_sort_column, sort_direction.
        """
        result = {
            "visible":             False,
            "headers_valid":       False,
            "row_count":           0,
            "first_row":           {},
            "active_sort_column":  None,
            "sort_direction":      None,
        }

        try:
            self.page.wait_for_load_state("networkidle", timeout=self.timeout)
        except Exception:
            pass

        result["visible"]            = self.validate_visible()
        if not result["visible"]:
            return result

        result["headers_valid"]      = self.validate_headers()
        result["row_count"]          = self.get_row_count()
        result["active_sort_column"] = self.get_active_sort_column()
        result["sort_direction"]     = self.get_active_sort_direction()

        if result["row_count"] > 0:
            result["first_row"] = self.get_row_data(0)

        self.logger.info(f"[PolicyListTable] Validation result: {result}")
        return result
