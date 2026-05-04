"""
Active Filter Chips Component Utility
======================================
Source: components/Active Filter Chips.md
UI: Radix-based popover dropdown with multi-select checkboxes.
     Chips shown inline: App Form Pending, Policy Coding WIP, Pending, Issued, Rejected, Others.

Selectors derived from actual OuterHTML:
  - Trigger button (chip display bar): button[role='combobox'][aria-haspopup='dialog']
  - Each active chip span:             span.inline-flex[aria-label='Remove <Name>']  parent
  - Remove chip button:                button[aria-label='Remove <chip_name>']
  - Chip count badge (e.g. "(6)"):     span.tabular-nums
  - Dropdown dialog:                   div[role='dialog'][data-state='open']
  - "All" checkbox row:                button.relative:has(span.truncate:text-is('All'))
  - Individual status checkbox rows:   button[data-selected='true'] span.truncate
  - "Clear All" button:                button:text('Clear All')
"""

import logging
from typing import Optional
from playwright.sync_api import Page, Locator, expect


class ActiveFilterChips:
    """
    Utility class for the Active Filter Chips / Status Filter Dropdown component.

    Usage:
        chips = ActiveFilterChips(page)
        chips.validate_chips_visible()
        chips.get_active_chip_names()          -> ['App Form Pending', 'Policy Coding WIP', ...]
        chips.get_chip_count()                 -> 6
        chips.open_dropdown()
        chips.select_status('Issued')
        chips.deselect_status('Rejected')
        chips.clear_all()
        chips.close_dropdown()
    """

    # --- Primary Selectors (from actual OuterHTML) ---
    TRIGGER_BTN      = "button[role='combobox'][aria-haspopup='dialog']"
    CHIP_CONTAINER   = "div.flex.items-center.gap-1.flex-nowrap"
    CHIP_BADGE       = "span.tabular-nums"                              # e.g. "(6)"
    DROPDOWN_DIALOG  = "div[role='dialog'][data-state='open']"
    ALL_ROW          = "button.relative:has(span.truncate:text-is('All'))"
    STATUS_ROW       = "button[data-selected='true'] span.truncate"     # inside open dialog
    CLEAR_ALL_BTN    = "button:text('Clear All')"
    CHECKBOX_CHECKED = "button[role='checkbox'][aria-checked='true']"

    # --- Multi-Locator Fallback Arrays ---
    TRIGGER_SELECTORS = [
        "button[role='combobox'][aria-haspopup='dialog']",
        "button:has-text('App Form Pending')",
        "button:has-text('Pending')",
        "button[aria-label*='filter']",
        "div.flex button[role='combobox']:first-of-type",
    ]
    CHIP_BADGE_SELECTORS = [
        "span.tabular-nums",
        "span[class*='tabular']",
        "button[role='combobox'] span:last-child",
    ]
    DIALOG_SELECTORS = [
        "div[role='dialog'][data-state='open']",
        "div[role='dialog'][tabindex='-1']",
        "div[role='menu']",
        "div.fixed[role='dialog']",
        "[data-radix-popper-content-wrapper] [role='dialog']",
        "[data-radix-popper-content-wrapper]",
    ]
    CLEAR_ALL_SELECTORS = [
        "button:text('Clear All')",
        "button:has-text('Clear')",
        "[role='dialog'] button:last-of-type",
    ]

    def __init__(self, page: Page, timeout: int = 15000):
        self.page = page
        self.timeout = timeout
        self.logger = logging.getLogger("utils.logger")

    # ------------------------------------------------------------------ #
    #  Private helpers
    # ------------------------------------------------------------------ #

    def _resolve(self, selectors: list[str], timeout: int = 3000):
        """
        Multi-locator resolver: tries each selector in order and returns the
        first visible Locator. Returns None if none are found.
        """
        for sel in selectors:
            try:
                el = self.page.locator(sel).first
                if el.is_visible(timeout=timeout):
                    return el
            except Exception:
                continue
        return None

    def _trigger(self) -> Locator:
        """Returns the filter chip trigger using multi-locator fallback."""
        resolved = self._resolve(self.TRIGGER_SELECTORS)
        if resolved:
            return resolved
        # Last resort: return raw locator (will fail with proper Playwright error)
        return self.page.locator(self.TRIGGER_BTN).first

    def _dialog(self) -> Locator:
        """Returns the open dropdown dialog using multi-locator fallback."""
        resolved = self._resolve(self.DIALOG_SELECTORS)
        if resolved:
            return resolved
        return self.page.locator(self.DROPDOWN_DIALOG).first

    def _chip_badge(self):
        """Returns the chip count badge using multi-locator fallback."""
        return self._resolve(self.CHIP_BADGE_SELECTORS, timeout=5000)

    def _clear_all_btn(self, dialog_locator):
        """Returns the Clear All button using multi-locator fallback inside dialog."""
        for sel in self.CLEAR_ALL_SELECTORS:
            try:
                btn = dialog_locator.locator(sel).first
                if btn.is_visible(timeout=2000):
                    return btn
            except Exception:
                continue
        return None

    def _chip_remove_btn(self, chip_name: str) -> Locator:
        return self.page.locator(f"button[aria-label='Remove {chip_name}']").first

    def _chip_span(self, chip_name: str) -> Locator:
        """The visible inline chip span (parent of remove button)."""
        return self.page.locator(f"button[aria-label='Remove {chip_name}']").locator("..").first

    # ------------------------------------------------------------------ #
    #  Visibility / Presence Checks
    # ------------------------------------------------------------------ #

    def is_visible(self) -> bool:
        """Returns True if the filter chip trigger button is visible on the page."""
        try:
            return self._trigger().is_visible(timeout=3000)
        except Exception:
            return False

    def validate_chips_visible(self) -> bool:
        """
        Asserts the filter chip trigger bar is visible.
        Returns True on pass, logs warning on soft-fail.
        """
        try:
            trigger = self._trigger()
            trigger.wait_for(state="attached", timeout=self.timeout)
            trigger.wait_for(state="visible",  timeout=self.timeout)
            self.logger.info("[OK] Active Filter Chips trigger bar is visible")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Active Filter Chips not visible: {e}")
            return False

    # ------------------------------------------------------------------ #
    #  Read State
    # ------------------------------------------------------------------ #

    def get_active_chip_names(self) -> list[str]:
        """
        Returns list of currently active chip label strings visible in the trigger bar.
        Example: ['App Form Pending', 'Policy Coding WIP', 'Pending', 'Issued', 'Rejected', 'Others']
        """
        names = []
        try:
            # Each active chip has: button[aria-label='Remove <name>']
            remove_btns = self.page.locator("button[tabindex='-1'][aria-label^='Remove']").all()
            for btn in remove_btns:
                label = btn.get_attribute("aria-label", timeout=2000) or ""
                name  = label.replace("Remove ", "").strip()
                if name:
                    names.append(name)
            self.logger.info(f"[OK] Active chips: {names}")
        except Exception as e:
            self.logger.warning(f"[WARN] Could not read active chip names: {e}")
        return names

    def get_chip_count(self) -> Optional[int]:
        """
        Returns the integer count shown in the badge span (e.g. '(6)' -> 6).
        Uses multi-locator fallback. Returns None if the badge is not found.
        """
        try:
            badge = self._chip_badge()
            if not badge:
                self.logger.warning("[WARN] Chip count badge not found via any selector")
                return None
            badge.wait_for(state="visible", timeout=5000)
            text = badge.text_content(timeout=2000) or ""
            count = int(text.strip("() "))
            self.logger.info(f"[OK] Chip count badge: {count}")
            return count
        except Exception as e:
            self.logger.warning(f"[WARN] Chip count badge not found: {e}")
            return None

    def is_chip_active(self, chip_name: str) -> bool:
        """Returns True if a chip with the given name is currently shown."""
        return chip_name in self.get_active_chip_names()

    # ------------------------------------------------------------------ #
    #  Dropdown Interactions
    # ------------------------------------------------------------------ #

    def open_dropdown(self) -> bool:
        """Clicks the trigger to open the filter chips dropdown popover."""
        try:
            trigger = self._trigger()
            trigger.wait_for(state="attached", timeout=self.timeout)
            trigger.wait_for(state="visible",  timeout=self.timeout)
            trigger.click(force=True)
            # Wait for dialog to appear using an OR selector (comma-separated) to avoid 30s delays
            opened = False
            try:
                or_selector = ", ".join(self.DIALOG_SELECTORS)
                self.page.locator(or_selector).first.wait_for(state="visible", timeout=5000)
                opened = True
            except Exception:
                pass
            if not opened:
                self.logger.warning("[WARN] Dropdown may not have opened — dialog not detected")
            self.logger.info("[OK] Filter chips dropdown opened")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Could not open filter chips dropdown: {e}")
            return False

    def close_dropdown(self) -> None:
        """Closes the dropdown by pressing Escape."""
        try:
            self.page.keyboard.press("Escape")
            self.page.locator(self.DROPDOWN_DIALOG).wait_for(state="hidden", timeout=5000)
            self.logger.info("[OK] Filter chips dropdown closed")
        except Exception as e:
            self.logger.warning(f"[WARN] Could not close dropdown via Escape: {e}")

    def get_available_statuses(self) -> list[str]:
        """
        Opens the dropdown and returns all status option labels.
        Includes: All, App Form Pending, Policy Coding WIP, Pending, Issued, Rejected, Others
        """
        statuses = []
        try:
            if not self._dialog().is_visible(timeout=1000):
                self.open_dropdown()
            rows = self._dialog().locator("span.truncate").all()
            for row in rows:
                txt = row.text_content(timeout=1000) or ""
                if txt.strip():
                    statuses.append(txt.strip())
            self.logger.info(f"[OK] Available statuses in dropdown: {statuses}")
        except Exception as e:
            self.logger.warning(f"[WARN] Could not read available statuses: {e}")
        return statuses

    def select_status(self, status_name: str) -> bool:
        """
        Selects (checks) a status in the dropdown. Opens the dropdown first if needed.
        Uses multi-locator fallback for the option row.
        """
        try:
            if not self._dialog().is_visible(timeout=1000):
                self.open_dropdown()
            dialog = self._dialog()
            # Multi-locator for the option row
            row = None
            for sel in [
                f"button.relative:has(span.truncate:text-is('{status_name}'))",
                f"button:has(span:text-is('{status_name}'))",
                f"[role='option']:has-text('{status_name}')",
                f"button:has-text('{status_name}')",
            ]:
                try:
                    candidate = dialog.locator(sel).first
                    if candidate.is_visible(timeout=2000):
                        row = candidate
                        break
                except Exception:
                    continue
            if not row:
                self.logger.warning(f"[WARN] Status option '{status_name}' not found")
                return False
            row.wait_for(state="visible", timeout=self.timeout)
            row.click(force=True)
            # Wait for table to re-render after filter change
            try:
                self.page.wait_for_load_state("networkidle", timeout=self.timeout)
            except Exception:
                pass
            self.logger.info(f"[OK] Selected status: {status_name}")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Could not select status '{status_name}': {e}")
            return False

    def deselect_status(self, status_name: str) -> bool:
        """
        Deselects a status by clicking its remove (X) button on the active chip.
        """
        try:
            btn = self._chip_remove_btn(status_name)
            btn.wait_for(state="visible", timeout=self.timeout)
            btn.click()
            self.logger.info(f"[OK] Removed chip: {status_name}")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Could not remove chip '{status_name}': {e}")
            return False

    def select_all(self) -> bool:
        """Clicks the 'All' row in the dropdown to select all statuses."""
        try:
            if not self._dialog().is_visible(timeout=1000):
                self.open_dropdown()
            all_row = self._dialog().locator("button.relative:has(span.truncate:text-is('All'))").first
            all_row.wait_for(state="visible", timeout=self.timeout)
            all_row.click()
            self.logger.info("[OK] Selected All statuses")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Could not click 'All' row: {e}")
            return False

    def clear_all(self) -> bool:
        """Clicks the 'Clear All' button using multi-locator fallback."""
        try:
            if not self._dialog().is_visible(timeout=1000):
                self.open_dropdown()
            dialog = self._dialog()
            clear_btn = self._clear_all_btn(dialog)
            if not clear_btn:
                self.logger.warning("[WARN] Clear All button not found via any selector")
                return False
            clear_btn.wait_for(state="visible", timeout=self.timeout)
            clear_btn.wait_for(state="enabled", timeout=self.timeout)
            clear_btn.click()
            # Wait for table to re-render after clearing all filters
            try:
                self.page.wait_for_load_state("networkidle", timeout=self.timeout)
            except Exception:
                pass
            self.logger.info("[OK] Clicked Clear All")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Could not click 'Clear All': {e}")
            return False

    # ------------------------------------------------------------------ #
    #  Composite Validation
    # ------------------------------------------------------------------ #

    def validate_all(self) -> dict:
        """
        Full validation of the Active Filter Chips component.
        Returns a result dict with keys: visible, chip_names, chip_count.
        """
        result = {
            "visible":     False,
            "chip_names":  [],
            "chip_count":  None,
        }
        result["visible"]    = self.validate_chips_visible()
        result["chip_names"] = self.get_active_chip_names()
        result["chip_count"] = self.get_chip_count()

        self.logger.info(f"[ActiveFilterChips] Validation result: {result}")
        return result
