"""
Detail Drawer Component Utility
=================================
Source: components/Detail Drawer.md
UI: Radix slide-out panel (right side) triggered by clicking a table row.

Structure:
  - Drawer:            div[role='dialog'][data-state='open']
  - Header:            header > proposer name + close button
  - Stepper (aside):   ol li button[aria-current='step'] — stage names + statuses
  - Summary Box:       aside > div.p-6 — key-value fields (Proposer Name, App No, etc.)
  - Main Content:      section — stage heading, workflow sections, items, lock indicators

Key Selectors (from actual OuterHTML):
  DRAWER:              div[role='dialog'][data-state='open']
  CLOSE_BTN:           button[aria-label='Close']
  HEADER_NAME:         header span.block.text-base.font-semibold
  ACTIVE_STAGE_BTN:    aside button[aria-current='step']
  STAGE_BTNS:          aside ol li button
  SUMMARY_FIELDS:      aside div.p-6 div.flex.flex-col.gap-0\\.5
  SECTION_HEADING:     section h3.text-sm.font-bold, section h4.text-sm.font-bold
  WORKFLOW_ITEM_ROW:   div.flex.items-center.gap-3.py-2
  STATUS_BADGE:        span.inline-flex.items-center.rounded.font-medium
  LOCK_BADGE:          span.inline-flex:has(span:text-is('Locked'))
  COPY_LINK_BTN:       button.text-xs.text-purple-700:text('Copy Link')
  SHOW_MORE_BTN:       button.text-sm.text-purple-700:has-text('Show')
"""

import logging
from typing import Optional
from playwright.sync_api import Page, Locator


class DetailDrawer:
    """
    Utility class for the Application Detail Drawer component.

    Usage:
        drawer = DetailDrawer(page)
        drawer.wait_until_open()
        drawer.get_header_name()               -> 'Sneha Akshay Pawar'
        drawer.close()

        # Stepper
        drawer.get_all_stages()                -> [{'name': 'Login & OTP Stage', 'status': 'In Progress'}, ...]
        drawer.get_active_stage_name()         -> 'Login & OTP Stage'
        drawer.get_stage_status('PI Stage')    -> 'Not Started'
        drawer.click_stage('PI Stage')

        # Summary box
        drawer.get_summary_field('App. No.')   -> 'LA53543595'
        drawer.get_all_summary_fields()        -> {'Proposer Name': 'Sneha...', ...}

        # Main content
        drawer.get_active_stage_heading()      -> 'Login & OTP Stage'
        drawer.get_workflow_sections()         -> ['Payment', 'Mandatory Declarations', ...]
        drawer.get_item_status('Photograph')   -> 'Pending'
        drawer.is_item_locked('Proposer Declaration (OTVC)') -> True
        drawer.click_copy_link('Mode of PIVC')
        drawer.click_show_more()
        drawer.validate_all()
    """

    # --- Primary Selectors ---
    DRAWER          = "div[role='dialog'][data-state='open']"
    CLOSE_BTN       = "button[aria-label='Close']"
    HEADER_NAME     = "header span.block.text-base.font-semibold"
    ASIDE           = "aside.w-60"
    STAGE_BTNS      = "aside.w-60 ol li button"
    ACTIVE_STAGE    = "aside.w-60 button[aria-current='step']"
    SUMMARY_BOX     = "aside.w-60 div.p-6"
    MAIN_SECTION    = "section.flex-1.overflow-y-auto"
    STAGE_HEADING   = "section.flex-1 h2.text-xl.font-bold"
    STATUS_BADGE    = "span.inline-flex.items-center.rounded.font-medium.whitespace-nowrap"
    LOCK_BADGE_SEL  = "span.inline-flex.items-center.rounded.font-medium:has(span:text-is('Locked'))"
    COPY_LINK_BTN   = "button.text-xs.text-purple-700"
    SHOW_MORE_BTN   = "button.text-sm.text-purple-700"
    WORKFLOW_ROW    = "div.flex.items-center.gap-3.py-2"

    # --- Multi-Locator Fallback Arrays ---
    DRAWER_SELECTORS = [
        "div[role='dialog'][data-state='open']",
        "div[role='dialog'][tabindex='-1']",
        "div.fixed.z-50[data-state='open']",
        "div.fixed.inset-y-0.right-0[role='dialog']",
    ]
    ASIDE_SELECTORS = [
        "aside.w-60",
        "aside.shrink-0.border-r",
        "aside.hidden.md\\:flex",
        "div[role='dialog'] aside",
    ]
    CLOSE_BTN_SELECTORS = [
        "button[aria-label='Close']",
        "header button[type='button']",
        "button:has(svg path[d*='205.66'])",
        "div[role='dialog'] header button",
    ]
    MAIN_SECTION_SELECTORS = [
        "section.flex-1.overflow-y-auto",
        "div.hidden.md\\:flex.flex-1 section",
        "div[role='dialog'] section",
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
        first visible Locator. Returns None if none are matched.
        """
        for sel in selectors:
            try:
                el = self.page.locator(sel).first
                if el.is_visible(timeout=timeout):
                    return el
            except Exception:
                continue
        return None

    def _drawer(self) -> Locator:
        """Returns the drawer dialog using multi-locator fallback."""
        resolved = self._resolve(self.DRAWER_SELECTORS)
        if resolved:
            return resolved
        return self.page.locator(self.DRAWER).first

    def _aside(self) -> Locator:
        """Returns the stepper aside panel using multi-locator fallback."""
        resolved = self._resolve(self.ASIDE_SELECTORS)
        if resolved:
            return resolved
        return self.page.locator(self.ASIDE).first

    def _main(self) -> Locator:
        """Returns the main content section using multi-locator fallback."""
        resolved = self._resolve(self.MAIN_SECTION_SELECTORS)
        if resolved:
            return resolved
        return self.page.locator(self.MAIN_SECTION).first

    def _summary_box(self) -> Locator:
        return self.page.locator(self.SUMMARY_BOX).first

    def _close_btn(self) -> Locator:
        """Returns the Close button using multi-locator fallback scoped inside drawer."""
        for sel in self.CLOSE_BTN_SELECTORS:
            try:
                el = self.page.locator(sel).first
                if el.is_visible(timeout=2000):
                    return el
            except Exception:
                continue
        return self.page.locator(self.CLOSE_BTN).first

    # ------------------------------------------------------------------ #
    #  Open / Close / Visibility
    # ------------------------------------------------------------------ #

    def is_open(self) -> bool:
        """Returns True if the drawer dialog is currently open and visible."""
        try:
            return self._drawer().is_visible(timeout=3000)
        except Exception:
            return False

    def wait_until_open(self) -> bool:
        """Waits for the drawer to fully open using multi-locator fallback."""
        try:
            # Phase 1: try each selector for attached state
            found_sel = None
            for sel in self.DRAWER_SELECTORS:
                try:
                    self.page.locator(sel).wait_for(state="attached", timeout=self.timeout)
                    found_sel = sel
                    break
                except Exception:
                    continue
            if not found_sel:
                self.logger.warning("[WARN] Drawer not found via any selector (attached check)")
                return False
            # Phase 2: wait for visible on the resolved selector
            self.page.locator(found_sel).wait_for(state="visible", timeout=self.timeout)
            self.logger.info(f"[OK] Detail Drawer is open (selector: {found_sel})")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Detail Drawer did not open: {e}")
            return False

    def close(self) -> bool:
        """Clicks the Close (X) button using multi-locator fallback, then waits for hidden."""
        try:
            btn = self._close_btn()
            btn.wait_for(state="visible", timeout=self.timeout)
            btn.click()
            # Wait for drawer to disappear — try all drawer selectors
            dismissed = False
            for sel in self.DRAWER_SELECTORS:
                try:
                    self.page.locator(sel).wait_for(state="hidden", timeout=5000)
                    dismissed = True
                    break
                except Exception:
                    continue
            if not dismissed:
                self.logger.warning("[WARN] Drawer may not have closed — hidden state not confirmed")
            self.logger.info("[OK] Detail Drawer closed")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Could not close drawer: {e}")
            return False

    def close_with_escape(self) -> None:
        """Alternative close using Escape key."""
        try:
            self.page.keyboard.press("Escape")
            self.logger.info("[OK] Drawer closed via Escape")
        except Exception as e:
            self.logger.warning(f"[WARN] Escape close failed: {e}")

    # ------------------------------------------------------------------ #
    #  Header
    # ------------------------------------------------------------------ #

    def get_header_name(self) -> Optional[str]:
        """Returns the proposer name shown in the drawer header."""
        try:
            el = self._drawer().locator(self.HEADER_NAME).first
            el.wait_for(state="visible", timeout=self.timeout)
            txt = el.text_content(timeout=2000) or ""
            self.logger.info(f"[OK] Drawer header name: '{txt.strip()}'")
            return txt.strip()
        except Exception as e:
            self.logger.warning(f"[WARN] Could not read header name: {e}")
            return None

    def get_aria_title(self) -> Optional[str]:
        """Returns the sr-only h2 aria title text (e.g. 'Application details — Sneha Akshay Pawar')."""
        try:
            h2 = self._drawer().locator("h2.sr-only").first
            return (h2.text_content(timeout=2000) or "").strip()
        except Exception:
            return None

    def get_aria_description(self) -> Optional[str]:
        """Returns the sr-only description text (e.g. 'Viewing application LA53543595')."""
        try:
            p = self._drawer().locator("p.sr-only").first
            return (p.text_content(timeout=2000) or "").strip()
        except Exception:
            return None

    # ------------------------------------------------------------------ #
    #  Stepper / Stage Navigator
    # ------------------------------------------------------------------ #

    def get_all_stages(self) -> list[dict]:
        """
        Returns list of all stages with name and status.
        E.g. [{'name': 'Login & OTP Stage', 'status': 'In Progress'}, ...]
        """
        stages = []
        try:
            btns = self._aside().locator("ol li button").all()
            for btn in btns:
                spans = btn.locator("span.flex.flex-col span").all()
                name   = spans[0].text_content(timeout=1000).strip() if len(spans) > 0 else ""
                status = spans[1].text_content(timeout=1000).strip() if len(spans) > 1 else ""
                if name:
                    stages.append({"name": name, "status": status})
            self.logger.info(f"[OK] Stages: {stages}")
        except Exception as e:
            self.logger.warning(f"[WARN] Could not read stages: {e}")
        return stages

    def get_active_stage_name(self) -> Optional[str]:
        """Returns the name of the currently selected/active stage."""
        try:
            btn = self._aside().locator("button[aria-current='step']").first
            name_span = btn.locator("span.flex.flex-col span").first
            txt = name_span.text_content(timeout=2000) or ""
            self.logger.info(f"[OK] Active stage: '{txt.strip()}'")
            return txt.strip()
        except Exception as e:
            self.logger.warning(f"[WARN] Could not read active stage: {e}")
            return None

    def get_stage_status(self, stage_name: str) -> Optional[str]:
        """Returns the status string for a given stage name (e.g. 'In Progress', 'Not Started')."""
        stages = self.get_all_stages()
        for s in stages:
            if stage_name.lower() in s["name"].lower():
                return s["status"]
        self.logger.warning(f"[WARN] Stage '{stage_name}' not found")
        return None

    def click_stage(self, stage_name: str) -> bool:
        """Clicks a stage button in the stepper by name, using multi-locator fallback."""
        try:
            # Multi-locator for the stage button
            btn = None
            for sel in [
                f"ol li button:has(span.flex.flex-col span:has-text('{stage_name}'))",
                f"ol li button:has(span:has-text('{stage_name}'))",
                f"aside button:has-text('{stage_name}')",
            ]:
                try:
                    candidate = self._aside().locator(sel).first
                    if candidate.is_visible(timeout=2000):
                        btn = candidate
                        break
                except Exception:
                    continue
            if not btn:
                self.logger.warning(f"[WARN] Stage button '{stage_name}' not found")
                return False
            btn.wait_for(state="visible", timeout=self.timeout)
            btn.click(force=True)
            # Stage switch is client-side — wait for h2 heading to update instead of networkidle
            try:
                self.page.locator(
                    f"section.flex-1 h2.text-xl.font-bold:has-text('{stage_name}')"
                ).wait_for(state="visible", timeout=self.timeout)
            except Exception:
                # Fallback: short networkidle in case of API call
                try:
                    self.page.wait_for_load_state("networkidle", timeout=5000)
                except Exception:
                    pass
            self.logger.info(f"[OK] Clicked stage: {stage_name}")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Could not click stage '{stage_name}': {e}")
            return False

    # ------------------------------------------------------------------ #
    #  Applicant Summary Box (left aside, below stepper)
    # ------------------------------------------------------------------ #

    def get_all_summary_fields(self) -> dict:
        """
        Returns all key-value pairs from the summary box.
        E.g. {'Proposer Name': 'Sneha Akshay Pawar', 'App. No.': 'LA53543595', ...}
        """
        data = {}
        try:
            box = self._summary_box()
            rows = box.locator("div.flex.flex-col.gap-0\\.5").all()
            for row in rows:
                spans = row.locator("span").all()
                if len(spans) >= 2:
                    label = (spans[0].text_content(timeout=1000) or "").strip()
                    value = (spans[1].text_content(timeout=1000) or "").strip()
                    if label:
                        data[label] = value
            self.logger.info(f"[OK] Summary fields: {data}")
        except Exception as e:
            self.logger.warning(f"[WARN] Could not read summary fields: {e}")
        return data

    def get_summary_field(self, label: str) -> Optional[str]:
        """
        Returns value for a specific label in the summary box.
        label: e.g. 'App. No.', 'Plan Name', 'Modal Premium', 'R&A Date'
        """
        fields = self.get_all_summary_fields()
        for key, val in fields.items():
            if label.lower() in key.lower():
                return val
        self.logger.warning(f"[WARN] Summary field '{label}' not found")
        return None

    # ------------------------------------------------------------------ #
    #  Main Content - Stage Heading & Badge
    # ------------------------------------------------------------------ #

    def get_active_stage_heading(self) -> Optional[str]:
        """Returns the h2 stage heading in the main content area."""
        try:
            h2 = self._main().locator("h2.text-xl.font-bold").first
            return (h2.text_content(timeout=2000) or "").strip()
        except Exception as e:
            self.logger.warning(f"[WARN] Could not read stage heading: {e}")
            return None

    def get_active_stage_badge_status(self) -> Optional[str]:
        """Returns the status badge text next to the main stage heading (e.g. 'In Progress')."""
        try:
            badge_area = self._main().locator("div.flex.flex-wrap.items-center.gap-x-3").first
            badge = badge_area.locator(self.STATUS_BADGE).first
            return (badge.text_content(timeout=2000) or "").strip()
        except Exception as e:
            self.logger.warning(f"[WARN] Could not read stage badge status: {e}")
            return None

    # ------------------------------------------------------------------ #
    #  Workflow Sections
    # ------------------------------------------------------------------ #

    def get_workflow_sections(self) -> list[str]:
        """
        Returns list of all section/sub-section headings in the main content.
        E.g. ['Payment', 'Mandatory Declarations', 'PIVC - Proposer', 'Document Upload', ...]
        """
        sections = []
        try:
            # h3 = section headings, h4 = sub-section headings, top-level spans also act as headings
            headings = self._main().locator("h3.text-sm.font-bold, h4.text-sm.font-bold").all()
            for h in headings:
                txt = (h.text_content(timeout=1000) or "").strip()
                if txt:
                    sections.append(txt)
            # Top-level items (Payment, Autopay) use span.font-bold not h3
            top_spans = self._main().locator(
                "div.hidden.md\\:flex > span.text-sm.font-bold"
            ).all()
            for sp in top_spans:
                txt = (sp.text_content(timeout=1000) or "").strip()
                if txt and txt not in sections:
                    sections.append(txt)
            self.logger.info(f"[OK] Workflow sections: {sections}")
        except Exception as e:
            self.logger.warning(f"[WARN] Could not read workflow sections: {e}")
        return sections

    # ------------------------------------------------------------------ #
    #  Workflow Items
    # ------------------------------------------------------------------ #

    def get_item_status(self, item_label: str) -> Optional[str]:
        """
        Returns the status badge text for a specific workflow item row.
        item_label: e.g. 'Photograph', 'KYC Address Proof', 'Mode of PIVC'
        """
        try:
            row = self._main().locator(
                f"div.flex.items-center.gap-3:has(span:has-text('{item_label}'))"
            ).first
            badge = row.locator(self.STATUS_BADGE).first
            txt = (badge.text_content(timeout=2000) or "").strip()
            self.logger.info(f"[OK] Item '{item_label}' status: {txt}")
            return txt
        except Exception as e:
            self.logger.warning(f"[WARN] Could not get status for '{item_label}': {e}")
            return None

    def get_all_item_statuses(self) -> list[dict]:
        """
        Returns list of all visible workflow item rows with their label and status.
        E.g. [{'label': 'Photograph', 'status': 'Pending'}, ...]
        """
        items = []
        try:
            rows = self._main().locator("div.flex.items-center.gap-3.py-2").all()
            for row in rows:
                # Label: first span with text inside the row
                label_spans = row.locator("span.text-sm.text-foreground.w-30").all()
                label = (label_spans[0].text_content(timeout=1000) or "").strip() if label_spans else ""
                # Status badge
                badge = row.locator(self.STATUS_BADGE).first
                try:
                    status = (badge.text_content(timeout=500) or "").strip()
                except Exception:
                    status = ""
                if label:
                    items.append({"label": label, "status": status})
        except Exception as e:
            self.logger.warning(f"[WARN] Could not read all item statuses: {e}")
        return items

    def is_item_locked(self, item_label: str) -> bool:
        """
        Returns True if the item has a 'Locked' badge (with lock SVG icon).
        item_label: e.g. 'Proposer Declaration (OTVC)'
        """
        try:
            # Find the section that has this label
            section = self._main().locator(
                f"div.hidden.md\\:flex:has(span:has-text('{item_label}'))"
            ).first
            locked = section.locator(self.LOCK_BADGE_SEL).first
            result = locked.is_visible(timeout=3000)
            self.logger.info(f"[OK] '{item_label}' locked: {result}")
            return result
        except Exception:
            return False

    def get_lock_message(self, item_label: str) -> Optional[str]:
        """Returns the explanatory lock message text for a locked item."""
        try:
            section = self._main().locator(
                f"div.hidden.md\\:flex:has(span:has-text('{item_label}'))"
            ).first
            msg = section.locator("span.text-sm.text-muted-foreground").first
            return (msg.text_content(timeout=2000) or "").strip()
        except Exception as e:
            self.logger.warning(f"[WARN] Could not read lock message: {e}")
            return None

    # ------------------------------------------------------------------ #
    #  Action Buttons
    # ------------------------------------------------------------------ #

    def click_copy_link(self, item_label: str = "Mode of PIVC") -> bool:
        """
        Clicks the 'Copy Link' button within a specific workflow item row.
        Defaults to the PIVC 'Copy Link' button.
        """
        try:
            row = self._main().locator(
                f"div.flex.items-center.gap-3:has(span:has-text('{item_label}'))"
            ).first
            btn = row.locator(self.COPY_LINK_BTN).first
            btn.wait_for(state="visible", timeout=self.timeout)
            btn.click()
            self.logger.info(f"[OK] Copy Link clicked for: {item_label}")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Could not click Copy Link for '{item_label}': {e}")
            return False

    def click_show_more(self) -> bool:
        """Clicks the 'Show N more' button to expand hidden document items."""
        try:
            btn = self._main().locator(self.SHOW_MORE_BTN).first
            btn.wait_for(state="visible", timeout=self.timeout)
            txt = btn.text_content(timeout=1000) or ""
            btn.click()
            self.page.wait_for_load_state("networkidle", timeout=self.timeout)
            self.logger.info(f"[OK] Show More clicked: '{txt.strip()}'")
            return True
        except Exception as e:
            self.logger.warning(f"[WARN] Could not click Show More: {e}")
            return False

    def get_show_more_text(self) -> Optional[str]:
        """Returns the text on the show-more button (e.g. 'Show 8 more')."""
        try:
            btn = self._main().locator(self.SHOW_MORE_BTN).first
            if btn.is_visible(timeout=2000):
                return (btn.text_content(timeout=1000) or "").strip()
        except Exception:
            pass
        return None

    # ------------------------------------------------------------------ #
    #  Composite Validation
    # ------------------------------------------------------------------ #

    def validate_all(self) -> dict:
        """
        Full validation of the Detail Drawer component.
        Returns result dict with all sub-component data.
        """
        result = {
            "is_open":              False,
            "header_name":          None,
            "aria_title":           None,
            "stages":               [],
            "active_stage":         None,
            "summary_fields":       {},
            "stage_heading":        None,
            "stage_badge_status":   None,
            "workflow_sections":    [],
            "workflow_items":       [],
            "show_more_text":       None,
        }

        result["is_open"] = self.wait_until_open()
        if not result["is_open"]:
            return result

        try:
            self.page.wait_for_load_state("networkidle", timeout=self.timeout)
        except Exception:
            pass

        result["header_name"]        = self.get_header_name()
        result["aria_title"]         = self.get_aria_title()
        result["stages"]             = self.get_all_stages()
        result["active_stage"]       = self.get_active_stage_name()
        result["summary_fields"]     = self.get_all_summary_fields()
        result["stage_heading"]      = self.get_active_stage_heading()
        result["stage_badge_status"] = self.get_active_stage_badge_status()
        result["workflow_sections"]  = self.get_workflow_sections()
        result["workflow_items"]     = self.get_all_item_statuses()
        result["show_more_text"]     = self.get_show_more_text()

        self.logger.info(f"[DetailDrawer] Validation result: {result}")
        return result
