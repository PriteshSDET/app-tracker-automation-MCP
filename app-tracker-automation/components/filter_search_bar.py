"""
Filter & Search Bar Component Utility
=======================================
Source: components/Filter & Search Bar.md
UI:
  - Search Type Selector:  dropdown button showing current field (e.g. "Name")
  - Search Input Field:    text input with placeholder "Search by Name"
  - Date Range Picker:     combobox button showing "Prev + Current Month"
  - Status Filter Trigger: combobox button (shows active filter chips, count badge)

Selectors derived from actual OuterHTML:
  - Search type selector btn:   button[aria-label='Choose search field']
  - Search input:               input[type='text'][placeholder*='Search']
  - Date range picker:          button[role='combobox'][aria-controls*='radix'][aria-expanded]
                                (the one with "Prev + Current Month" span inside)
  - Status filter trigger:      button[role='combobox'][aria-haspopup='dialog']
"""

import logging
from typing import Optional
from playwright.sync_api import Page, Locator


class FilterSearchBar:
    """
    Utility class for the Filter & Search Bar component.

    Usage:
        bar = FilterSearchBar(page)
        bar.validate_all()
        bar.get_search_type()             -> 'Name'
        bar.set_search_type('App No.')
        bar.search('LA12345678')
        bar.clear_search()
        bar.get_date_filter_label()       -> 'Prev + Current Month'
        bar.open_date_filter()
        bar.open_status_filter()
    """

    # --- Selectors (from actual OuterHTML) ---
    SEARCH_TYPE_BTN     = "button[aria-label='Choose search field']"
    SEARCH_INPUT        = "input[type='text'][placeholder*='Search']"
    SEARCH_INPUT_ALT    = [
        "input[placeholder*='Search']",
        "input[placeholder*='search']",
        "div.flex.items-center.gap-2.flex-1 input",
        ".flex-1.min-w-48 input",
    ]
    DATE_PICKER_BTN     = "button[role='combobox'][aria-expanded]"   # narrows further below
    STATUS_TRIGGER      = "button[role='combobox'][aria-haspopup='dialog']"
    SEARCH_WRAPPER      = "div.hidden.md\\:flex.items-center.gap-2"  # outer container
    DATE_PICKER_LABEL   = "Prev + Current Month"

    def __init__(self, page: Page, timeout: int = 15000):
        self.page = page
        self.timeout = timeout
        self.logger = logging.getLogger(self.__class__.__name__)

    # ------------------------------------------------------------------ #
    #  Private helpers
    # ------------------------------------------------------------------ #

    def _search_input(self) -> Optional[Locator]:
        """Returns the actual text input (skips type='image' magnifying glass)."""
        for sel in [self.SEARCH_INPUT] + self.SEARCH_INPUT_ALT:
            try:
                el = self.page.locator(sel).first
                if el.is_visible(timeout=2000):
                    attr = el.get_attribute("type", timeout=1000) or ""
                    if attr.lower() != "image":
                        return el
            except Exception:
                continue
        return None

    def _date_picker(self) -> Optional[Locator]:
        """Returns the date range picker button (has 'Prev + Current Month' text)."""
        try:
            # Use text content match for reliability
            el = self.page.locator(
                f"button[role='combobox']:has(span:text-is('{self.DATE_PICKER_LABEL}'))"
            ).first
            if el.is_visible(timeout=3000):
                return el
        except Exception:
            pass
        # Fallback: any combobox that is NOT the status trigger
        try:
            combos = self.page.locator(self.DATE_PICKER_BTN).all()
            for c in combos:
                txt = c.text_content(timeout=1000) or ""
                if "Month" in txt or "Date" in txt.lower():
                    return c
        except Exception:
            pass
        return None

    # ------------------------------------------------------------------ #
    #  Visibility Checks
    # ------------------------------------------------------------------ #

    def is_search_bar_visible(self) -> bool:
        try:
            return self.page.locator(self.SEARCH_TYPE_BTN).first.is_visible(timeout=3000)
        except Exception:
            return False

    def is_search_input_visible(self) -> bool:
        inp = self._search_input()
        return inp is not None and inp.is_visible(timeout=3000)

    def is_date_filter_visible(self) -> bool:
        dp = self._date_picker()
        return dp is not None

    # ------------------------------------------------------------------ #
    #  Read State
    # ------------------------------------------------------------------ #

    def get_search_type(self) -> Optional[str]:
        """Returns currently selected search field label (e.g. 'Name', 'App No.')."""
        try:
            btn = self.page.locator(self.SEARCH_TYPE_BTN).first
            btn.wait_for(state="visible", timeout=self.timeout)
            # The first <span class='font-medium'> holds the label
            label = btn.locator("span.font-medium").first.text_content(timeout=2000)
            self.logger.info(f"[OK] Search type: {label}")
            return (label or "").strip()
        except Exception as e:
            self.logger.warning(f"[WARN] Could not read search type: {e}")
            return None

    def get_search_value(self) -> Optional[str]:
        """Returns current value of the search input field."""
        try:
            inp = self._search_input()
            if inp:
                val = inp.input_value(timeout=2000)
                self.logger.info(f"[OK] Search input value: '{val}'")
                return val
        except Exception as e:
            self.logger.warning(f"[WARN] Could not read search value: {e}")
        return None

    def get_date_filter_label(self) -> Optional[str]:
        """Returns the label shown on the date range picker (e.g. 'Prev + Current Month')."""
        try:
            dp = self._date_picker()
            if dp:
                txt = dp.text_content(timeout=2000)
                label = (txt or "").strip()
                self.logger.info(f"[OK] Date filter label: {label}")
                return label
        except Exception as e:
            self.logger.warning(f"[WARN] Could not read date filter label: {e}")
        return None

    # ------------------------------------------------------------------ #
    #  Search Interactions
    # ------------------------------------------------------------------ #

    def set_search_type(self, field_name: str) -> bool:
        """
        Opens the search-type selector and picks the given field.
        field_name: e.g. 'Name', 'App No.', 'Policy No.'
        """
        try:
            btn = self.page.locator(self.SEARCH_TYPE_BTN).first
            btn.wait_for(state="visible", timeout=self.timeout)
            btn.click()
            # Wait for popover to open and pick the option
            option = self.page.locator(f"[role='dialog'] button:has-text('{field_name}')").first
            option.wait_for(state="visible", timeout=self.timeout)
            option.click()
            self.logger.info(f"[OK] Search type set to: {field_name}")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Could not set search type to '{field_name}': {e}")
            return False

    def search(self, text: str) -> bool:
        """Types the given text into the search input field."""
        try:
            inp = self._search_input()
            if not inp:
                self.logger.warning("[WARN] Search input not found")
                return False
            inp.wait_for(state="visible", timeout=self.timeout)
            inp.click()
            inp.fill(text)
            self.page.wait_for_load_state("networkidle", timeout=self.timeout)
            self.logger.info(f"[OK] Searched for: '{text}'")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Search failed for '{text}': {e}")
            return False

    def clear_search(self) -> bool:
        """Clears the current search input value."""
        try:
            inp = self._search_input()
            if not inp:
                self.logger.warning("[WARN] Search input not found for clear")
                return False
            inp.click()
            inp.fill("")
            self.page.wait_for_load_state("networkidle", timeout=self.timeout)
            self.logger.info("[OK] Search input cleared")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Could not clear search: {e}")
            return False

    def search_and_verify(self, text: str) -> bool:
        """Types text and verifies the input value matches."""
        if not self.search(text):
            return False
        val = self.get_search_value()
        if val == text:
            self.logger.info(f"[OK] Search verified: '{text}'")
            return True
        self.logger.warning(f"[WARN] Search verify failed: expected '{text}', got '{val}'")
        return False

    # ------------------------------------------------------------------ #
    #  Date Filter Interactions
    # ------------------------------------------------------------------ #

    def open_date_filter(self) -> bool:
        """Clicks the date range picker to open the calendar/options dropdown."""
        try:
            dp = self._date_picker()
            if not dp:
                self.logger.warning("[WARN] Date filter button not found")
                return False
            dp.wait_for(state="visible", timeout=self.timeout)
            dp.click()
            self.logger.info("[OK] Date filter opened")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Could not open date filter: {e}")
            return False

    def close_date_filter(self) -> None:
        """Closes the date filter by pressing Escape."""
        try:
            self.page.keyboard.press("Escape")
            self.logger.info("[OK] Date filter closed")
        except Exception as e:
            self.logger.warning(f"[WARN] Could not close date filter: {e}")

    # ------------------------------------------------------------------ #
    #  Status Filter Trigger
    # ------------------------------------------------------------------ #

    def open_status_filter(self) -> bool:
        """Clicks the status filter combobox trigger (active filter chips bar)."""
        try:
            trigger = self.page.locator(self.STATUS_TRIGGER).first
            trigger.wait_for(state="visible", timeout=self.timeout)
            trigger.click()
            self.logger.info("[OK] Status filter dropdown opened from search bar")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Could not open status filter: {e}")
            return False

    # ------------------------------------------------------------------ #
    #  Composite Validation
    # ------------------------------------------------------------------ #

    def validate_all(self) -> dict:
        """
        Full validation of the Filter & Search Bar component.
        Returns a result dict with keys: search_bar_visible, search_input_visible,
        search_type, date_filter_visible, date_filter_label.
        """
        result = {
            "search_bar_visible":   False,
            "search_input_visible": False,
            "search_type":          None,
            "date_filter_visible":  False,
            "date_filter_label":    None,
        }

        try:
            self.page.wait_for_load_state("networkidle", timeout=self.timeout)
        except Exception:
            pass

        result["search_bar_visible"]   = self.is_search_bar_visible()
        result["search_input_visible"] = self.is_search_input_visible()
        result["search_type"]          = self.get_search_type()
        result["date_filter_visible"]  = self.is_date_filter_visible()
        result["date_filter_label"]    = self.get_date_filter_label()

        if result["search_bar_visible"]:
            self.logger.info("[OK] Filter & Search Bar validated successfully")
        else:
            self.logger.warning("[WARN] Filter & Search Bar not fully visible")

        self.logger.info(f"[FilterSearchBar] Validation result: {result}")
        return result
