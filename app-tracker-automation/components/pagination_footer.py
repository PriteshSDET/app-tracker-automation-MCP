"""
Pagination Footer Component Utility
=====================================
Source: components/Pagination Footer.md
UI:
  - Previous Button:      Disabled on first page  | aria-label="Previous page"
  - Page Number Buttons:  1, 2, 3, 4, 5 ... 19   | aria-label="Page N"
  - Active Page:          aria-current="page"
  - Next Button:          aria-label="Next page"
  - Record Count Text:    "1-10 of 187" (mobile/sm: "Page 1 of 19")

Selectors derived from actual OuterHTML:
  - Nav container:     nav[role='navigation'][aria-label='Pagination']
  - Previous button:   button[aria-label='Previous page']
  - Next button:       button[aria-label='Next page']
  - Page N button:     button[aria-label='Page N']
  - Active page:       button[aria-current='page']
  - Total pages text:  span:has(span.font-semibold)   (mobile counter "Page X of Y")
"""

import re
import logging
from typing import Optional
from playwright.sync_api import Page, Locator


class PaginationFooter:
    """
    Utility class for the Pagination Footer component.

    Usage:
        pagination = PaginationFooter(page)
        pagination.validate_all()
        pagination.get_current_page()         -> 1
        pagination.get_total_pages()          -> 19
        pagination.go_to_next()
        pagination.go_to_previous()
        pagination.go_to_page(3)
        pagination.is_on_last_page()
        pagination.is_previous_disabled()
    """

    # --- Selectors (from actual OuterHTML) ---
    NAV_CONTAINER   = "nav[role='navigation'][aria-label='Pagination']"
    PREV_BTN        = "button[aria-label='Previous page']"
    NEXT_BTN        = "button[aria-label='Next page']"
    ACTIVE_PAGE     = "button[aria-current='page']"
    PAGE_NUM_LIST   = "ul.hidden.sm\\:flex"                       # the ul holding page buttons
    MOBILE_COUNTER  = "span.sm\\:hidden"                          # "Page X of Y" on small screens

    def __init__(self, page: Page, timeout: int = 10000):
        self.page = page
        self.timeout = timeout
        self.logger = logging.getLogger(self.__class__.__name__)

    # ------------------------------------------------------------------ #
    #  Private helpers
    # ------------------------------------------------------------------ #

    def _nav(self) -> Locator:
        return self.page.locator(self.NAV_CONTAINER).first

    def _page_btn(self, page_num: int) -> Locator:
        return self.page.locator(f"button[aria-label='Page {page_num}']").first

    def _parse_page_of_text(self, text: str) -> tuple[Optional[int], Optional[int]]:
        """Parses 'Page 1 of 19' -> (1, 19). Returns (None, None) on parse failure."""
        match = re.search(r"Page\s+(\d+)\s+of\s+(\d+)", text, re.IGNORECASE)
        if match:
            return int(match.group(1)), int(match.group(2))
        return None, None

    # ------------------------------------------------------------------ #
    #  Visibility Checks
    # ------------------------------------------------------------------ #

    def is_visible(self) -> bool:
        """Returns True if the pagination nav is present on the page."""
        try:
            return self._nav().is_visible(timeout=3000)
        except Exception:
            return False

    def validate_visible(self) -> bool:
        """Asserts pagination nav is visible. Returns True on pass."""
        try:
            nav = self._nav()
            nav.wait_for(state="attached", timeout=self.timeout)
            nav.wait_for(state="visible",  timeout=self.timeout)
            self.logger.info("[OK] Pagination footer is visible")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Pagination footer not visible: {e}")
            return False

    # ------------------------------------------------------------------ #
    #  Read State
    # ------------------------------------------------------------------ #

    def get_current_page(self) -> Optional[int]:
        """Returns the currently active page number."""
        try:
            active = self.page.locator(self.ACTIVE_PAGE).first
            active.wait_for(state="visible", timeout=self.timeout)
            txt = active.text_content(timeout=2000) or ""
            page_num = int(txt.strip())
            self.logger.info(f"[OK] Current page: {page_num}")
            return page_num
        except Exception as e:
            # Fallback: try mobile counter
            try:
                mobile = self.page.locator(self.MOBILE_COUNTER).first
                txt = mobile.text_content(timeout=2000) or ""
                current, _ = self._parse_page_of_text(txt)
                if current:
                    self.logger.info(f"[OK] Current page (mobile): {current}")
                    return current
            except Exception:
                pass
            self.logger.warning(f"[WARN] Could not get current page: {e}")
            return None

    def get_total_pages(self) -> Optional[int]:
        """Returns total number of pages."""
        try:
            # Last visible page button in the list (may be last before ellipsis, or the real last)
            # Try mobile counter first (reliable "Page X of Y")
            mobile = self.page.locator(self.MOBILE_COUNTER).first
            if mobile.is_visible(timeout=2000):
                txt = mobile.text_content(timeout=2000) or ""
                _, total = self._parse_page_of_text(txt)
                if total:
                    self.logger.info(f"[OK] Total pages (mobile): {total}")
                    return total
        except Exception:
            pass
        try:
            # Last page button in ul (the highest aria-label="Page N")
            page_btns = self.page.locator("ul.hidden.sm\\:flex button[aria-label^='Page']").all()
            nums = []
            for btn in page_btns:
                label = btn.get_attribute("aria-label", timeout=1000) or ""
                m = re.search(r"Page\s+(\d+)", label)
                if m:
                    nums.append(int(m.group(1)))
            if nums:
                total = max(nums)
                self.logger.info(f"[OK] Total pages (from buttons): {total}")
                return total
        except Exception as e:
            self.logger.warning(f"[WARN] Could not determine total pages: {e}")
        return None

    def get_visible_page_numbers(self) -> list[int]:
        """Returns list of page numbers visible in the pagination bar (excluding ellipsis)."""
        nums = []
        try:
            btns = self.page.locator("ul.hidden.sm\\:flex button[aria-label^='Page']").all()
            for btn in btns:
                label = btn.get_attribute("aria-label", timeout=1000) or ""
                m = re.search(r"Page\s+(\d+)", label)
                if m:
                    nums.append(int(m.group(1)))
            self.logger.info(f"[OK] Visible page numbers: {nums}")
        except Exception as e:
            self.logger.warning(f"[WARN] Could not read page numbers: {e}")
        return nums

    def is_previous_disabled(self) -> bool:
        """Returns True if the Previous button is disabled (first page)."""
        try:
            prev = self.page.locator(self.PREV_BTN).first
            return prev.is_disabled(timeout=3000)
        except Exception:
            return False

    def is_next_disabled(self) -> bool:
        """Returns True if the Next button is disabled (last page)."""
        try:
            nxt = self.page.locator(self.NEXT_BTN).first
            return nxt.is_disabled(timeout=3000)
        except Exception:
            return False

    def is_on_first_page(self) -> bool:
        return self.is_previous_disabled()

    def is_on_last_page(self) -> bool:
        return self.is_next_disabled()

    # ------------------------------------------------------------------ #
    #  Navigation Actions
    # ------------------------------------------------------------------ #

    def go_to_next(self) -> bool:
        """Clicks the Next page button. Returns False if already on last page."""
        try:
            if self.is_next_disabled():
                self.logger.warning("[WARN] Already on last page, cannot go next")
                return False
            nxt = self.page.locator(self.NEXT_BTN).first
            nxt.wait_for(state="visible",  timeout=self.timeout)
            nxt.wait_for(state="enabled",  timeout=self.timeout)
            nxt.click()
            self.page.wait_for_load_state("networkidle", timeout=self.timeout)
            self.logger.info("[OK] Navigated to next page")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Could not go to next page: {e}")
            return False

    def go_to_previous(self) -> bool:
        """Clicks the Previous page button. Returns False if already on first page."""
        try:
            if self.is_previous_disabled():
                self.logger.warning("[WARN] Already on first page, cannot go previous")
                return False
            prev = self.page.locator(self.PREV_BTN).first
            prev.wait_for(state="visible", timeout=self.timeout)
            prev.wait_for(state="enabled", timeout=self.timeout)
            prev.click()
            self.page.wait_for_load_state("networkidle", timeout=self.timeout)
            self.logger.info("[OK] Navigated to previous page")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Could not go to previous page: {e}")
            return False

    def go_to_page(self, page_num: int) -> bool:
        """
        Clicks a specific page number button.
        Works only for page numbers visible in the pagination bar.
        """
        try:
            btn = self._page_btn(page_num)
            btn.wait_for(state="visible", timeout=self.timeout)
            btn.click()
            self.page.wait_for_load_state("networkidle", timeout=self.timeout)
            self.logger.info(f"[OK] Navigated to page {page_num}")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Could not go to page {page_num}: {e}")
            return False

    def go_to_first_page(self) -> bool:
        """Navigates to page 1."""
        return self.go_to_page(1)

    # ------------------------------------------------------------------ #
    #  Composite Validation
    # ------------------------------------------------------------------ #

    def validate_all(self) -> dict:
        """
        Full validation of the Pagination Footer component.
        Returns result dict with keys: visible, current_page, total_pages,
        prev_disabled, next_disabled, page_numbers.
        """
        result = {
            "visible":       False,
            "current_page":  None,
            "total_pages":   None,
            "prev_disabled": None,
            "next_disabled": None,
            "page_numbers":  [],
        }

        result["visible"]       = self.validate_visible()
        if not result["visible"]:
            self.logger.info("[INFO] Pagination not visible - likely single page result")
            return result

        result["current_page"]  = self.get_current_page()
        result["total_pages"]   = self.get_total_pages()
        result["prev_disabled"] = self.is_previous_disabled()
        result["next_disabled"] = self.is_next_disabled()
        result["page_numbers"]  = self.get_visible_page_numbers()

        self.logger.info(f"[PaginationFooter] Validation result: {result}")
        return result
