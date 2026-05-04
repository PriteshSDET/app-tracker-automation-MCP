"""
Top Navigation & Controls Component Utility
=============================================
Source: components/Top Navigation & Controls.md
UI:
  - ABSLI | LEAP Logo: <img alt='ABSLI'> on the left
  - Page Title:        <span> "App Tracker" next to logo separator
  - Theme Toggle:      button[aria-label='Toggle theme'] (moon/sun icon)
  - User Avatar Menu:  button[aria-label='Account menu'] with initials (e.g. "SU")
  - Download Button:   button or link with text "Download N Records"

Selectors derived from actual OuterHTML:
  - Logo img:          img[alt='ABSLI']
  - Page title:        span.font-semibold:text-is('App Tracker')
  - Theme toggle:      button[aria-label='Toggle theme']
  - Account menu btn:  button[aria-label='Account menu']
  - User initials:     span[role='img'][aria-label]  (e.g. aria-label='SU')
  - Download button:   button:has-text('Download')
"""

import logging
import re
from typing import Optional
from playwright.sync_api import Page, Locator


class TopNavigationControls:
    """
    Utility class for the Top Navigation & Controls component.

    Usage:
        nav = TopNavigationControls(page)
        nav.validate_all()
        nav.is_logo_visible()                 -> True
        nav.get_page_title()                  -> 'App Tracker'
        nav.get_user_initials()               -> 'SU'
        nav.toggle_theme()
        nav.open_account_menu()
        nav.click_download(expected_count=10)
        nav.get_download_button_text()        -> 'Download 10 Records'
    """

    # --- Selectors (from actual OuterHTML) ---
    LOGO_IMG        = "img[alt='ABSLI']"
    PAGE_TITLE      = "span.font-semibold.text-foreground.whitespace-nowrap"
    THEME_TOGGLE    = "button[aria-label='Toggle theme']"
    ACCOUNT_BTN     = "button[aria-label='Account menu']"
    USER_AVATAR     = "span[role='img']"                        # has aria-label='SU' etc.
    DOWNLOAD_BTN    = "button:has-text('Download')"
    DOWNLOAD_ALT    = [
        "button:has-text('Download')",
        "a:has-text('Download')",
        "[data-testid='download-btn']",
    ]
    NAV_CONTAINER   = "div.flex.items-center.justify-between.w-full"

    def __init__(self, page: Page, timeout: int = 15000):
        self.page = page
        self.timeout = timeout
        self.logger = logging.getLogger(self.__class__.__name__)

    # ------------------------------------------------------------------ #
    #  Private helpers
    # ------------------------------------------------------------------ #

    def _nav(self) -> Locator:
        return self.page.locator(self.NAV_CONTAINER).first

    def _download_btn(self) -> Optional[Locator]:
        for sel in self.DOWNLOAD_ALT:
            try:
                el = self.page.locator(sel).first
                if el.is_visible(timeout=3000):
                    return el
            except Exception:
                continue
        return None

    # ------------------------------------------------------------------ #
    #  Visibility Checks
    # ------------------------------------------------------------------ #

    def is_logo_visible(self) -> bool:
        """Returns True if the ABSLI logo image is visible."""
        try:
            return self.page.locator(self.LOGO_IMG).first.is_visible(timeout=3000)
        except Exception:
            return False

    def is_page_title_visible(self) -> bool:
        """Returns True if the 'App Tracker' title text is visible."""
        try:
            return self.page.locator(self.PAGE_TITLE).first.is_visible(timeout=3000)
        except Exception:
            return False

    def is_account_menu_visible(self) -> bool:
        """Returns True if the user account/avatar button is visible."""
        try:
            return self.page.locator(self.ACCOUNT_BTN).first.is_visible(timeout=3000)
        except Exception:
            return False

    def is_download_btn_visible(self) -> bool:
        """Returns True if the Download Records button is visible."""
        return self._download_btn() is not None

    def is_theme_toggle_visible(self) -> bool:
        """Returns True if the theme toggle button is visible."""
        try:
            return self.page.locator(self.THEME_TOGGLE).first.is_visible(timeout=3000)
        except Exception:
            return False

    # ------------------------------------------------------------------ #
    #  Read State
    # ------------------------------------------------------------------ #

    def get_page_title(self) -> Optional[str]:
        """Returns the page title text (e.g. 'App Tracker')."""
        try:
            el = self.page.locator(self.PAGE_TITLE).first
            el.wait_for(state="visible", timeout=self.timeout)
            txt = el.text_content(timeout=2000) or ""
            self.logger.info(f"[OK] Page title: '{txt.strip()}'")
            return txt.strip()
        except Exception as e:
            self.logger.warning(f"[WARN] Could not read page title: {e}")
            return None

    def get_logo_src(self) -> Optional[str]:
        """Returns the src URL of the ABSLI logo image."""
        try:
            src = self.page.locator(self.LOGO_IMG).first.get_attribute("src", timeout=3000)
            self.logger.info(f"[OK] Logo src: {src}")
            return src
        except Exception as e:
            self.logger.warning(f"[WARN] Could not read logo src: {e}")
            return None

    def get_user_initials(self) -> Optional[str]:
        """Returns the current user's initials shown in the avatar (e.g. 'SU')."""
        try:
            avatar = self.page.locator(self.USER_AVATAR).first
            # aria-label on the span holds initials
            label = avatar.get_attribute("aria-label", timeout=3000)
            if label:
                self.logger.info(f"[OK] User initials: {label}")
                return label.strip()
            # Fallback: inner span text
            inner = avatar.locator("span[aria-hidden='true']").first
            txt = inner.text_content(timeout=1000) or ""
            self.logger.info(f"[OK] User initials (inner): {txt.strip()}")
            return txt.strip()
        except Exception as e:
            self.logger.warning(f"[WARN] Could not read user initials: {e}")
            return None

    def get_download_button_text(self) -> Optional[str]:
        """Returns the full text of the Download button (e.g. 'Download 10 Records')."""
        try:
            btn = self._download_btn()
            if btn:
                txt = btn.text_content(timeout=2000) or ""
                self.logger.info(f"[OK] Download button text: '{txt.strip()}'")
                return txt.strip()
        except Exception as e:
            self.logger.warning(f"[WARN] Could not read download button text: {e}")
        return None

    def get_download_record_count(self) -> Optional[int]:
        """
        Parses the download button text to extract the count.
        'Download 10 Records' -> 10
        """
        txt = self.get_download_button_text()
        if not txt:
            return None
        m = re.search(r"(\d+)", txt)
        if m:
            count = int(m.group(1))
            self.logger.info(f"[OK] Download record count: {count}")
            return count
        return None

    # ------------------------------------------------------------------ #
    #  Interactions
    # ------------------------------------------------------------------ #

    def toggle_theme(self) -> bool:
        """Clicks the theme toggle button (dark/light mode switch)."""
        try:
            btn = self.page.locator(self.THEME_TOGGLE).first
            btn.wait_for(state="visible", timeout=self.timeout)
            btn.click()
            self.logger.info("[OK] Theme toggled")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Could not toggle theme: {e}")
            return False

    def open_account_menu(self) -> bool:
        """Clicks the user account/avatar button to open the account menu dialog."""
        try:
            btn = self.page.locator(self.ACCOUNT_BTN).first
            btn.wait_for(state="visible",  timeout=self.timeout)
            btn.click(force=True)
            self.logger.info("[OK] Account menu opened")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Could not open account menu: {e}")
            return False

    def close_account_menu(self) -> None:
        """Closes the account menu by pressing Escape."""
        try:
            self.page.keyboard.press("Escape")
            self.logger.info("[OK] Account menu closed")
        except Exception as e:
            self.logger.warning(f"[WARN] Could not close account menu: {e}")

    def click_download(self, expected_count: Optional[int] = None) -> bool:
        """
        Clicks the Download Records button.
        If expected_count is given, verifies the button text contains that count first.
        """
        try:
            btn = self._download_btn()
            if not btn:
                self.logger.warning("[WARN] Download button not found")
                return False

            if expected_count is not None:
                actual_count = self.get_download_record_count()
                if actual_count != expected_count:
                    self.logger.warning(
                        f"[WARN] Download count mismatch: expected {expected_count}, got {actual_count}"
                    )

            btn.wait_for(state="visible", timeout=self.timeout)
            btn.click()
            self.logger.info(f"[OK] Download button clicked")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Could not click download button: {e}")
            return False

    # ------------------------------------------------------------------ #
    #  Composite Validation
    # ------------------------------------------------------------------ #

    def validate_all(self) -> dict:
        """
        Full validation of the Top Navigation & Controls component.
        Returns result dict with keys: logo_visible, page_title, user_initials,
        theme_toggle_visible, download_visible, download_text, download_count.
        """
        result = {
            "logo_visible":         False,
            "page_title":           None,
            "user_initials":        None,
            "theme_toggle_visible": False,
            "download_visible":     False,
            "download_text":        None,
            "download_count":       None,
        }

        try:
            self.page.wait_for_load_state("networkidle", timeout=self.timeout)
        except Exception:
            pass

        result["logo_visible"]         = self.is_logo_visible()
        result["page_title"]           = self.get_page_title()
        result["user_initials"]        = self.get_user_initials()
        result["theme_toggle_visible"] = self.is_theme_toggle_visible()
        result["download_visible"]     = self.is_download_btn_visible()
        result["download_text"]        = self.get_download_button_text()
        result["download_count"]       = self.get_download_record_count()

        if result["logo_visible"] and result["page_title"] == "App Tracker":
            self.logger.info("[OK] Top Navigation & Controls validated successfully")
        else:
            self.logger.warning("[WARN] Top Navigation validation partial - check results")

        self.logger.info(f"[TopNavigationControls] Validation result: {result}")
        return result
