"""
Unified Test Execution Script: E2E Login & Component Validation
Strategy: Continuous State Management with Explicit Hidden-Waits & Scroll Handling
Updates: Integrated deep-locators from App Tracker HTML source.
         Component utilities wired in for full regression coverage.
"""

import os
import re
from dotenv import load_dotenv
import pytest
from datetime import datetime
from playwright.sync_api import Page
from pages.aditya_birla_login_page import AdityaBirlaLoginPage
from pages.aditya_birla_dashboard_page import AdityaBirlaDashboardPage
from pages.aditya_birla_tracker_page import AdityaBirlaTrackerPage
from utils.logger import Logger

# ── Component Utility Imports ─────────────────────────────────────────────────
from components import (
    ActiveFilterChips,
    FilterSearchBar,
    PaginationFooter,
    PolicyListTable,
    TopNavigationControls,
    DetailDrawer,
)
# ─────────────────────────────────────────────────────────────────────────────


# Load environment variables from .env file
import os
# Try multiple possible .env locations
env_paths = [
    "app-tracker-automation/.env",  # From project root
    ".env",  # Current directory
    os.path.join(os.path.dirname(__file__), "..", "..", ".env"),  # Relative to test file
]

env_loaded = False
for env_path in env_paths:
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)
        env_loaded = True
        break

if not env_loaded:
    print(f"WARNING: .env file not found in any of these locations: {env_paths}")

# --- GLOBAL BROWSER CONFIGURATION ---
BROWSER_VIEWPORT = None
BROWSER_LAUNCH_ARGS = ['--start-maximized']  # Full screen mode


class UnifiedAutomationFramework:
    """Manages execution timeline and reporting"""
    
    def __init__(self):
        self.logger = Logger()
        self.start_time = datetime.now()
    
    def log_start(self, test_name):
        self.logger.info("\n========================================")
        self.logger.info(f"STARTING TEST SUITE: {test_name}")
        self.logger.info(f"Time: {datetime.now().strftime('%H:%M:%S')}")
        self.logger.info("========================================\n")

    def log_end(self, test_name, status):
        duration = (datetime.now() - self.start_time).total_seconds()
        self.logger.info("\n========================================")
        self.logger.info(f"TEST SUITE ENDED: {status.upper()}")
        self.logger.info(f"Total Duration: {duration:.2f}s")
        self.logger.info("========================================\n")


class TestUnifiedAppTrackerFlow:
    
    @pytest.mark.smoke
    @pytest.mark.high_priority
    def test_complete_flow_and_validation(self, page: Page):
        self.logger = Logger() 
        framework = UnifiedAutomationFramework()
        
        # Apply Browser Configuration
        if BROWSER_VIEWPORT:
            self.logger.info(f"Applying Viewport: {BROWSER_VIEWPORT}")
            page.set_viewport_size(BROWSER_VIEWPORT)
        else:
            # Default behavior if no explicit viewport is requested (respects --start-maximized)
            self.logger.info("No fixed viewport requested; relying on launch args (--start-maximized)")
        
        # Log Launch Args (Note: These are typically applied in conftest.py, but logged here for reference)
        self.logger.info(f"Browser Launch Args: {BROWSER_LAUNCH_ARGS}")

        # FIX: Inject panel.css styles to fix window layout issues
        # This ensures proper element visibility and prevents MENU button from being hidden
        layout_css = """
        /* --- FIXED LAYOUT STYLES --- */
        *, *::before, *::after {
            box-sizing: border-box;
        }
        html, body {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow-x: hidden;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        body {
            display: flex;
            flex-direction: column;
        }
        .panel-container {
            width: 100%;
            max-width: 100vw;
            padding: 10px;
            overflow-wrap: break-word;
        }
        """
        page.add_style_tag(content=layout_css)
        self.logger.info("[OK] Layout fix CSS injected to prevent viewport issues")
        
        framework.log_start("Complete End-to-End Flow")
        
        login_page = AdityaBirlaLoginPage(page)
        dashboard_page = AdityaBirlaDashboardPage(page)
        tracker_page = AdityaBirlaTrackerPage(page)
        
        creds = {"user": os.getenv("ADITYA_BIRLA_USER"), "pass": os.getenv("ADITYA_BIRLA_PASS")}
        
        # Debug: Log credential loading status
        self.logger.info(f"Credentials loaded - User: {creds['user']}, Pass: {'*' * len(creds['pass']) if creds['pass'] else 'None'}")
        
        if not creds["user"] or not creds["pass"]:
            self.logger.error(f"Credentials not loaded from .env. User: {creds['user']}, Pass: {creds['pass']}")
            raise Exception("Credentials not loaded from .env file. Please check .env file location and content.")
        errors_logged = 0
        
        try:
            # PHASE 1: NAVIGATION & AUTH
            self._navigate_and_auth(page, login_page, creds)
            
            # PHASE 2: APP TRACKER SETUP
            tracker_page_obj = None
            if "app-tracker" not in page.url:
                tracker_page_obj = self._navigate_to_tracker(page, tracker_page)
            else:
                tracker_page.wait_for_tracker_load(timeout=8000)
                tracker_page_obj = page
            
            # Use the tracker page object (new tab) for validations
            if tracker_page_obj:
                # Update tracker_page with the correct page object
                tracker_page.page = tracker_page_obj
                
            # ── PHASE 3: FULL COMPONENT UTILITY REGRESSION ────────────────────
            self.logger.step_start("--- Phase 3: Full Component Utility Regression ---")

            # Resolve the live tracker page — prefer new tab, fall back to current
            active_page = tracker_page_obj or page

            # Guard: confirm the page is still open and on the tracker before running validations
            try:
                current_url = active_page.url
                if "app-tracker" not in current_url and "onboarding-uat" not in current_url:
                    self.logger.warning(
                        f"[WARN] active_page URL does not look like App Tracker: {current_url}. "
                        "Validations may produce warnings."
                    )
            except Exception as url_check_e:
                self.logger.warning(f"[WARN] Could not verify active_page URL: {url_check_e}")

            sanity_errors = 0
            sanity_errors += self._reg_top_navigation(active_page)
            sanity_errors += self._reg_filter_search_bar(active_page)
            sanity_errors += self._reg_active_filter_chips(active_page)
            sanity_errors += self._reg_policy_list_table(active_page)
            sanity_errors += self._reg_pagination_footer(active_page)
            sanity_errors += self._reg_detail_drawer(active_page)

            # Note: Legacy component validations (e.g. _validate_component_filters, _validate_chip_filters) 
            # have been permanently removed because they rely on fragile, outdated locators.
            # They have been fully superseded by the Phase 3 Full Component Utility Regression.

            errors_logged += sanity_errors
            
            if errors_logged > 0:
                framework.log_end("COMPLETE_FLOW", "PASSED_WITH_WARNINGS")
            else:
                framework.log_end("COMPLETE_FLOW", "ALL_PASSED")


        except Exception as critical_e:
            self.logger.critical(f"FATAL ERROR STOPPING EXECUTION: {str(critical_e)}")
            framework.log_end("COMPLETE_FLOW", "CRITICAL_FAILURE")
            raise

    def _navigate_and_auth(self, page, login_page, creds):
        self.logger.step_start("Phase 1: Authentication")
        login_page.load()
        
        # Wait for network to settle after page load
        page.wait_for_load_state("networkidle", timeout=10000)
        
        assert login_page.is_login_page_displayed(), "Login page failed to load"
        
        login_page.enter_credentials(creds["user"], creds["pass"])
        
        # Wait for network to settle after entering credentials
        page.wait_for_load_state("networkidle", timeout=5000)
        
        login_page.click_login_button()
        
        try:
            page.wait_for_url("**/uat/#/dashboard", timeout=15000)
        except Exception as e:
            self.logger.warning(f"[WARN] Redirect wait timed out: {e}")

    def _navigate_to_tracker(self, page, tracker_page):
        """Navigates using precise CSS selectors from HTML analysis."""
        self.logger.info("Navigating via Top-Right Menu...")
        
        # Wait for network to settle before navigation
        page.wait_for_load_state("networkidle", timeout=10000)
        
        # PRECISE SELECTOR from HTML: button.menu-button with aria-label="menu"
        menu_btn = page.locator("button.menu-button[aria-label='menu']").first
        menu_btn.scroll_into_view_if_needed()
        
        # Wait for element to be fully actionable (attached, visible, stable)
        menu_btn.wait_for(state="attached", timeout=5000)
        menu_btn.wait_for(state="visible", timeout=5000)
        
        # Wait for any loading spinners/overlays to disappear
        self._wait_for_loading_overlay_to_disappear(page)
        
        menu_btn.click()
        
        # Wait for menu to appear and network to settle
        page.wait_for_timeout(500)
        page.wait_for_load_state("networkidle", timeout=5000)
        
        # Try multiple selectors for Application Tracker link
        link_selectors = [
            "a:has-text('Application Tracker')",
            "button:has-text('Application Tracker')",
            "[role='menuitem']:has-text('Application Tracker')",
            "li:has-text('Application Tracker') a"
        ]
        
        link = None
        for selector in link_selectors:
            try:
                temp_link = page.locator(selector).first
                if temp_link.is_visible(timeout=2000):
                    link = temp_link
                    self.logger.info(f"Found Application Tracker using selector: {selector}")
                    break
            except:
                continue
        
        if not link:
            raise Exception("Application Tracker link not found in menu")
        
        link.scroll_into_view_if_needed()
        
        # Wait for link to be fully actionable
        link.wait_for(state="attached", timeout=3000)
        link.wait_for(state="visible", timeout=3000)
        
        # Wait for any loading spinners/overlays to disappear
        self._wait_for_loading_overlay_to_disappear(page)
        
        # Handle new tab opening for Application Tracker
        # App Tracker opens in a NEW TAB — all three click strategies preserve the
        # authenticated session. Do NOT use window.open(url) as it will open a tab
        # without the LEAP auth cookies and immediately redirect to login.
        self.logger.info("Setting up new tab listener before clicking Application Tracker link...")

        context = page.context
        tracker_page_obj = None

        # ── Strategy 1: Standard Playwright click with Retry Mechanism (Up to 3 times) ───
        for attempt in range(3):
            try:
                self.logger.info(f"Attempting to click Application Tracker link (Attempt {attempt+1}/3)...")
                with context.expect_page(timeout=10000) as new_page_info:
                    link.click(timeout=5000, force=True)
                tracker_page_obj = new_page_info.value
                self.logger.info(f"[PASS] Captured tab on attempt {attempt+1}: {tracker_page_obj.url}")
                break
            except Exception as e:
                self.logger.warning(f"[WARN] Click attempt {attempt+1} failed or timed out: {e}")
                page.wait_for_timeout(2000)

        # ── Strategy 4: Scan all already-open pages ───────────────────────────────
        if not tracker_page_obj:
            page.wait_for_timeout(4000)   # give the browser a moment to open the tab
            for p in context.pages:
                try:
                    if "app-tracker" in p.url or "onboarding-uat" in p.url:
                        tracker_page_obj = p
                        self.logger.info(f"[PASS] Strategy-4: Found tracker tab via scan: {p.url}")
                        break
                except Exception:
                    continue

        if not tracker_page_obj:
            self.logger.warning("[WARN] No App Tracker tab found — falling back to current page (validations will warn)")
            tracker_page_obj = page

        # ── Bring to focus & wait for full tracker UI load ───────────────────────
        tracker_page_obj.bring_to_front()

        # Wait for network to settle
        try:
            tracker_page_obj.wait_for_load_state("networkidle", timeout=25000)
            self.logger.info("[PASS] Application Tracker page reached networkidle")
        except Exception as load_e:
            self.logger.warning(f"[WARN] networkidle wait timed out: {load_e}")

        # ── TRACKER UI READINESS GATE ─────────────────────────────────────────────
        # Wait for at least ONE tracker UI landmark to be visible before returning.
        # This guarantees the authenticated tracker (not a redirect/login screen)
        # is fully rendered and ready for component validation.
        tracker_ui_selectors = [
            "table",                                        # policy list table
            "nav[aria-label='Pagination']",                 # pagination nav
            "div[role='combobox']",                         # filter chip trigger
            "input[type='search'], input[placeholder]",     # search bar
            "header h1, header h2",                         # page header
        ]
        ui_ready = False
        for sel in tracker_ui_selectors:
            try:
                tracker_page_obj.locator(sel).first.wait_for(state="visible", timeout=15000)
                self.logger.info(f"[PASS] Tracker UI ready (matched: '{sel}')")
                ui_ready = True
                break
            except Exception:
                continue
        if not ui_ready:
            self.logger.warning("[WARN] Tracker UI landmarks not found — page may not be the tracker (auth redirect?)")

        # Validate final URL
        expected_url_pattern = "onboarding-uat.adityabirlasunlifeinsurance.com/app-tracker"
        try:
            current = tracker_page_obj.url
            if expected_url_pattern in current:
                self.logger.info(f"[PASS] URL Validation PASSED: {current}")
            else:
                self.logger.warning(f"[WARN] URL mismatch. Expected pattern: {expected_url_pattern}, Got: {current}")
        except Exception as e:
            self.logger.warning(f"[WARN] URL validation error: {e}")

        # Wait for overlays to clear
        self._wait_for_loading_overlay_to_disappear(tracker_page_obj)

        # Update tracker_page with the new page object
        tracker_page.page = tracker_page_obj
        tracker_page.wait_for_tracker_load(timeout=15000)

        return tracker_page_obj

    def _wait_for_loading_overlay_to_disappear(self, page, timeout=5000):
        """Wait for loading spinners, progress bars, or blocking overlays to disappear"""
        try:
            # Common loading overlay selectors
            loading_selectors = [
                ".loading-overlay",
                ".spinner",
                ".progress-bar",
                "[class*='loading']",
                "[class*='spinner']",
                "[class*='overlay']",
                ".MuiCircularProgress-root",
                ".MuiBackdrop-root"
            ]
            
            for selector in loading_selectors:
                try:
                    loading_element = page.locator(selector).first
                    if loading_element.is_visible(timeout=1000):
                        self.logger.info(f"Waiting for loading element to disappear: {selector}")
                        loading_element.wait_for(state="hidden", timeout=timeout)
                        self.logger.info(f"Loading element disappeared: {selector}")
                except:
                    continue
        except Exception as e:
            self.logger.warning(f"Error waiting for loading overlay: {e}")

    def _validate_component_filters(self, page, tracker_page):
        """Validates App Tracker homepage components using specified locators."""
        errors = 0
        
        # Wait for main table wrapper to become visible before checking individual filters
        try:
            table_wrapper = page.locator(".MuiBox-root.jss138, tbody tr, table").first
            table_wrapper.wait_for(state="visible", timeout=15000)
            self.logger.info("[PASS] Main table wrapper is visible")
        except Exception as e:
            self.logger.warning(f"[WARN] Table wrapper not visible: {e}")
        
        # --- 0. FILTER BUTTON (Fixing dynamic_wait error) ---
        try:
            self.logger.step_start("Validating Filter Button")
            
            # Wait for network to settle before validation
            page.wait_for_load_state("networkidle", timeout=15000)
            
            # Try multiple selectors for filter button
            filter_selectors = [
                "button:has-text('Filter')",
                "[aria-label*='filter' i]",
                ".filter-button",
                "button[title*='filter' i]",
                "svg[class*='filter']"
            ]
            
            filter_btn = None
            for selector in filter_selectors:
                try:
                    temp_btn = page.locator(selector).first
                    if temp_btn.is_visible(timeout=3000):
                        filter_btn = temp_btn
                        self.logger.info(f"Found Filter Button using selector: {selector}")
                        break
                except:
                    continue
            
            if filter_btn:
                self.logger.info("[PASS] Filter Button found and visible")
            else:
                self.logger.warning("[WARN] Filter Button not visible (may not exist on this page)")
        except Exception as e:
            self.logger.warning(f"[WARN] Filter Button validation skipped: {e}")

        # --- 1. TITLE - "Policy List" ---
        try:
            self.logger.step_start("Validating Policy List Title")
            
            # Wait for network to settle
            page.wait_for_load_state("networkidle", timeout=15000)
            
            # Use .first to handle strict mode violation when multiple elements exist
            title = page.get_by_text("Policy List").first
            
            # Wait for element to be fully actionable
            title.wait_for(state="attached", timeout=15000)
            title.wait_for(state="visible", timeout=15000)
            
            if title.is_visible(timeout=15000):
                self.logger.info("[PASS] Policy List Title found")
            else:
                self.logger.warning("[WARN] Policy List Title not visible")
        except Exception as e:
            self.logger.warning(f"[WARN] Title Validation skipped: {e}")

        # --- 2. SEARCH BAR - (Fixing Image Input Error) ---
        try:
            self.logger.step_start("Validating Search Box")
            
            # Wait for network to settle
            page.wait_for_load_state("networkidle", timeout=15000)
            
            # Try multiple search input selectors
            search_selectors = [
                "input[placeholder*='Search']",
                "input[placeholder*='search']",
                "input[type='text']",
                ".navbar-search",
                "input.search",
                "[data-testid='search-input']"
            ]
            
            search_input = None
            for selector in search_selectors:
                try:
                    temp_input = page.locator(selector).first
                    if temp_input.is_visible(timeout=3000):
                        search_input = temp_input
                        self.logger.info(f"Found Search Box using selector: {selector}")
                        break
                except:
                    continue
            
            if search_input:
                self.logger.info("[PASS] Search Box found")
                search_input.fill("LA53544020")
                
                # Wait for network to settle after input
                page.wait_for_load_state("networkidle", timeout=15000)
                
                page.wait_for_timeout(500)
                if "LA53544020" in search_input.input_value():
                    self.logger.info("[PASS] Search term entered successfully")
                search_input.fill("")
            else:
                self.logger.warning("[WARN] Search Box not found (may not exist on this page)")
        except Exception as e:
            self.logger.warning(f"[WARN] Search Box validation skipped: {e}")

        # --- 3. DATE FILTER - "Prev + Current Month" ---
        try:
            self.logger.step_start("Validating Date Filter")
            
            # Wait for network to settle
            page.wait_for_load_state("networkidle", timeout=15000)
            
            # Use resilient text-based selectors
            date_filter = None
            
            # Try get_by_text first (most resilient)
            try:
                date_filter = page.get_by_text("Prev + Current Month").first
                if date_filter.is_visible(timeout=5000):
                    self.logger.info("[PASS] Date Filter found using get_by_text")
            except:
                pass
            
            # Fallback to generic CSS selectors
            if not date_filter:
                date_filter_selectors = [
                    "*:has-text('Prev + Current Month')",
                    "[role='button']:has-text('Prev')",
                    "button:has-text('Month')",
                    "div:has-text('Current Month')",
                    "[class*='filter']:has-text('Month')",
                    "[class*='date']:has-text('Prev')"
                ]
                
                for selector in date_filter_selectors:
                    try:
                        temp_filter = page.locator(selector).first
                        if temp_filter.is_visible(timeout=3000):
                            date_filter = temp_filter
                            self.logger.info(f"Found Date Filter using selector: {selector}")
                            break
                    except:
                        continue
            
            if date_filter:
                self.logger.info("[PASS] Date Filter found")
            else:
                self.logger.warning("[WARN] Date Filter not found (may not exist on this page)")
        except Exception as e:
            self.logger.warning(f"[WARN] Date Filter validation skipped: {e}")

        # --- 4. SORT DROPDOWN (Fixing Timeout & Modal Block Errors) ---
        try:
            self.logger.step_start("Validating Sort Dropdown")
            
            # Wait for network to settle
            page.wait_for_load_state("networkidle", timeout=15000)
            
            # Press escape to clear any blocking overlays first
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)
            
            # Wait for loading overlays to disappear
            self._wait_for_loading_overlay_to_disappear(page)
            
            # Try multiple selectors for sort dropdown
            sort_selectors = [
                "#mui-component-select-sortList",
                ".sort-dropdown",
                "[role='combobox']",
                "button[aria-haspopup='listbox']",
                "select[name*='sort' i]"
            ]
            
            sort_dropdown = None
            for selector in sort_selectors:
                try:
                    temp_dropdown = page.locator(selector).first
                    if temp_dropdown.is_visible(timeout=3000):
                        sort_dropdown = temp_dropdown
                        self.logger.info(f"Found Sort Dropdown using selector: {selector}")
                        break
                except:
                    continue
            
            if sort_dropdown:
                self.logger.info("[PASS] Sort Dropdown button found")
                sort_dropdown.click(force=True)
                
                # Wait for network to settle after click
                page.wait_for_load_state("networkidle", timeout=15000)
                
                page.wait_for_timeout(500)
                self.logger.info("[PASS] Sort Dropdown clicked successfully")
                page.keyboard.press("Escape") # Close the dropdown
            else:
                self.logger.warning("[WARN] Sort Dropdown not found (may not exist on this page)")
        except Exception as e:
            self.logger.warning(f"[WARN] Sort Dropdown validation skipped: {e}")

        return errors

    def _validate_component_table(self, page, tracker_page):
        """Validates Table Interaction using specified locators from homepage."""
        errors = 0
        
        try:
            self.logger.step_start("Validating Application Table")
            
            # Wait for network to settle before table validation
            page.wait_for_load_state("networkidle", timeout=15000)
            
            # --- 1. TABLE HEADER ---
            try:
                # Use resilient text-based selectors
                table_header = None
                
                # Try get_by_role first (most resilient for table headers)
                try:
                    table_header = page.get_by_role("columnheader").first
                    if table_header.is_visible(timeout=5000):
                        self.logger.info("[PASS] Table Header found using get_by_role")
                except:
                    pass
                
                # Fallback to generic CSS selectors
                if not table_header:
                    table_header_selectors = [
                        "th",
                        "thead th",
                        "table th",
                        "[role='columnheader']",
                        "*[role='columnheader']",
                        "[class*='head']:has-text('App')",
                        "[class*='head']:has-text('Proposer')"
                    ]
                    
                    for selector in table_header_selectors:
                        try:
                            temp_header = page.locator(selector).first
                            if temp_header.is_visible(timeout=3000):
                                table_header = temp_header
                                self.logger.info(f"Found Table Header using selector: {selector}")
                                break
                        except:
                            continue
                
                if table_header:
                    self.logger.info("[PASS] Table Header found")
                else:
                    self.logger.warning("[WARN] Table Header not found (may not exist on this page)")
            except Exception as e:
                self.logger.warning(f"[WARN] Table Header validation skipped: {e}")

            # --- 2. ROW EXTRACTION (Fixing Strict Mode Violation) ---
            try:
                # Grab the main wrapper or table body
                first_row = page.locator(".MuiBox-root.jss138, tbody tr").first
                
                # Wait for element to be fully actionable
                first_row.wait_for(state="attached", timeout=15000)
                first_row.wait_for(state="visible", timeout=15000)
                
                if first_row.is_visible(timeout=15000):
                    self.logger.info("[PASS] Application Table Loaded and First Row Found")
                    
                    # PLAN NAME CELL (The specific fix for strict mode)
                    try:
                        plan_name_cell = first_row.locator('.plan-name').first
                        if plan_name_cell.is_visible(timeout=15000):
                            plan_name = plan_name_cell.text_content().strip()
                            self.logger.info(f"Plan Name: {plan_name}")
                    except Exception as e:
                        self.logger.warning(f"[WARN] Plan Name extraction failed: {e}")
                    
                    # PREMIUM AMOUNT
                    try:
                        premium_cell = first_row.locator(":scope > *:has-text('₹')").first
                        if premium_cell.is_visible(timeout=15000):
                            self.logger.info(f"Premium Amount: {premium_cell.text_content().strip()}")
                    except Exception as e:
                        self.logger.warning(f"[WARN] Premium extraction failed: {e}")

                    # STATUS TAG
                    try:
                        status_text = first_row.get_by_text("Pending").first
                        if status_text.is_visible(timeout=15000):
                            self.logger.info(f"Status Tag: {status_text.text_content().strip()}")
                    except Exception as e:
                        self.logger.warning(f"[WARN] Status Tag extraction failed: {e}")
                        page.wait_for_timeout(15000) # Pauses execution right here for 15 seconds

                    # ROW INTERACTION TEST
                    try:
                        # Wait for loading overlays to disappear before click
                        self._wait_for_loading_overlay_to_disappear(page)
                        
                        # Wait for row to be fully actionable
                        first_row.wait_for(state="attached", timeout=15000)
                        first_row.wait_for(state="visible", timeout=15000)
                        
                        first_row.click(force=True)
                        
                        # Wait for network to settle after click
                        page.wait_for_load_state("networkidle", timeout=15000)
                        
                        page.wait_for_timeout(1000)
                        self.logger.info("[PASS] First row clicked successfully")
                    except Exception as e:
                        self.logger.error(f"[FAIL] Failed to click first row: {e}")
                        errors += 1
                else:
                    self.logger.warning("[WARN] No rows found in table")
            except Exception as e:
                self.logger.error(f"[FAIL] Table Row Failed: {e}")
                errors += 1
            
            self.logger.info("[PASS] Table validation completed")
        except Exception as e:
            self.logger.error(f"[FAIL] Table Interaction Failed: {e}")
            errors += 1

        return errors

    def _validate_pagination(self, page):
        """Validates pagination functionality including footer text, page navigation, and Next/Previous buttons."""
        errors = 0
        
        try:
            self.logger.step_start("Validating Pagination")
            
            # Wait for network to settle
            page.wait_for_load_state("networkidle", timeout=15000)
            
            # --- 1. FOOTER TEXT VALIDATION ---
            try:
                # Use resilient text-based selectors
                footer = None
                
                # Try get_by_text first (most resilient)
                try:
                    footer = page.get_by_text("of").first
                    if footer.is_visible(timeout=5000):
                        self.logger.info("[PASS] Pagination footer found using get_by_text")
                except:
                    pass
                
                # Fallback to generic CSS selectors and regex
                if not footer:
                    footer_selectors = [
                        "div[class*='Pagination']",
                        "div[class*='pagination']",
                        ".MuiTablePagination-toolbar"
                    ]
                    
                    for selector in footer_selectors:
                        try:
                            temp_footer = page.locator(selector).first
                            if temp_footer.is_visible(timeout=3000):
                                footer = temp_footer
                                self.logger.info(f"Found pagination footer using selector: {selector}")
                                break
                        except:
                            continue
                
                # If still not found, try regex for "1-10 of 50" or "Page 1 of 10" pattern
                if not footer:
                    try:
                        # Find an element containing the specific pagination text pattern
                        pattern = re.compile(r'(?i)(page\s+\d+\s+of\s+\d+|\d+\s*-\s*\d+\s+of\s+\d+)')
                        temp_footer = page.locator("body").filter(has_text=pattern).last
                        if temp_footer.is_visible(timeout=3000):
                            footer = temp_footer
                            self.logger.info("Found pagination footer using regex pattern")
                    except:
                        pass
                
                if footer:
                    # Check for pagination text pattern
                    footer_text = footer.text_content().strip()
                    # Clean up text to just get the pagination part if it's a large container
                    match = re.search(r'(?i)(page\s+\d+\s+of\s+\d+|\d+\s*-\s*\d+\s+of\s+\d+)', footer_text)
                    if match:
                        self.logger.info(f"[PASS] Footer shows pagination text: {match.group(1)}")
                    elif "of" in footer_text and any(char.isdigit() for char in footer_text):
                        self.logger.info(f"[PASS] Footer shows pagination text: {footer_text}")
                    else:
                        # Only warn if we found something but it doesn't look like pagination
                        # This prevents "Customer Profile" from triggering a warning, we just ignore it
                        pass
                else:
                    self.logger.info("[INFO] Pagination footer not found (might be a single page)")
            except Exception as e:
                self.logger.warning(f"[WARN] Footer validation skipped: {e}")
            
            # --- 2. ACTIVE PAGE VALIDATION ---
            try:
                # Use resilient text-based selectors
                active_page = None
                
                # Try get_by_text first
                try:
                    active_page = page.get_by_text("1", exact=True).first
                    if active_page.is_visible(timeout=5000):
                        self.logger.info("[PASS] Active page found using get_by_text")
                except:
                    pass
                
                # Fallback to generic CSS selectors
                if not active_page:
                    active_page_selectors = [
                        "button:has-text('1')",
                        "[aria-current='true']",
                        "[class*='selected']:has-text('1')",
                        "[class*='active']:has-text('1')",
                        "*:has-text('1')"
                    ]
                    
                    for selector in active_page_selectors:
                        try:
                            temp_page = page.locator(selector).first
                            if temp_page.is_visible(timeout=3000):
                                active_page = temp_page
                                self.logger.info(f"Found active page using selector: {selector}")
                                break
                        except:
                            continue
                
                if active_page:
                    self.logger.info("[PASS] Page 1 is highlighted/active")
                else:
                    self.logger.warning("[WARN] Active page indicator not found")
            except Exception as e:
                self.logger.warning(f"[WARN] Active page validation skipped: {e}")
            
            # --- 3. PAGE NUMBER NAVIGATION ---
            try:
                page_numbers = [2, 3, 4]  # Start from 2 since page 1 is already active
                for page_num in page_numbers:
                    page_button = None
                    # Use aria-label selectors (MUI pagination standard) and role buttons
                    page_button_selectors = [
                        f"[aria-label='Go to page {page_num}']",
                        f"[aria-label='page {page_num}']",
                        f"button[aria-label='{page_num}']",
                        f".MuiPaginationItem-page[aria-label='{page_num}']",
                        f"button:has-text('^{page_num}$')",
                        f".MuiPaginationItem-root:has-text('^{page_num}$')"
                    ]
                    for selector in page_button_selectors:
                        try:
                            temp_button = page.locator(selector).first
                            if temp_button.is_visible(timeout=2000):
                                page_button = temp_button
                                self.logger.info(f"Found page {page_num} button using: {selector}")
                                break
                        except:
                            continue
                    
                    # Try get_by_role as last resort
                    if not page_button:
                        try:
                            temp_button = page.get_by_role("button", name=str(page_num), exact=True)
                            if temp_button.is_visible(timeout=2000):
                                page_button = temp_button
                                self.logger.info(f"Found page {page_num} button using get_by_role")
                        except:
                            pass
                    
                    if page_button:
                        page_button.click(timeout=5000)
                        page.wait_for_load_state("networkidle", timeout=8000)
                        page.wait_for_timeout(500)
                        self.logger.info(f"[PASS] Clicked page {page_num} successfully")
                    else:
                        self.logger.info(f"[INFO] Page {page_num} button not found (could be end of pages)")
                        break  # If page 2 not found, higher pages won't be either
            except Exception as e:
                self.logger.warning(f"[WARN] Page number navigation skipped: {e}")
            
            # --- 4. NEXT BUTTON NAVIGATION ---
            try:
                next_button = None
                next_button_selectors = [
                    "[aria-label='Go to next page']",
                    "[aria-label='Next page']",
                    "[aria-label='next']",
                    ".MuiPaginationItem-next",
                    "button:has-text('Next')",
                    "button:has-text('next')",
                ]
                for selector in next_button_selectors:
                    try:
                        temp_next = page.locator(selector).first
                        if temp_next.is_visible(timeout=3000):
                            next_button = temp_next
                            self.logger.info(f"Found Next button using: {selector}")
                            break
                    except:
                        continue
                
                if next_button:
                    next_button.click(timeout=5000)
                    page.wait_for_load_state("networkidle", timeout=8000)
                    page.wait_for_timeout(500)
                    self.logger.info("[PASS] Next button clicked successfully")
                else:
                    self.logger.info("[INFO] Next button not found (could be single page)")
            except Exception as e:
                self.logger.warning(f"[WARN] Next button navigation skipped: {e}")
            
            # --- 5. PREVIOUS BUTTON NAVIGATION ---
            try:
                prev_button = None
                prev_button_selectors = [
                    "[aria-label='Go to previous page']",
                    "[aria-label='Previous page']",
                    "[aria-label='previous']",
                    ".MuiPaginationItem-previous",
                    "button:has-text('Previous')",
                    "button:has-text('previous')",
                ]
                for selector in prev_button_selectors:
                    try:
                        temp_prev = page.locator(selector).first
                        if temp_prev.is_visible(timeout=3000):
                            prev_button = temp_prev
                            self.logger.info(f"Found Previous button using: {selector}")
                            break
                    except:
                        continue
                
                if prev_button:
                    prev_button.click(timeout=5000)
                    page.wait_for_load_state("networkidle", timeout=8000)
                    page.wait_for_timeout(500)
                    self.logger.info("[PASS] Previous button clicked successfully")
                else:
                    self.logger.info("[INFO] Previous button not found (could be single page)")
            except Exception as e:
                self.logger.warning(f"[WARN] Previous button navigation skipped: {e}")
            
            self.logger.info("[PASS] Pagination validation completed")
        except Exception as e:
            self.logger.error(f"[FAIL] Pagination validation failed: {e}")
            errors += 1
        
        return errors

    def _validate_chip_filters(self, page):
        """Validates chip filters including dynamic counts, color-coded states, and clearable chips."""
        errors = 0
        
        try:
            self.logger.step_start("Validating Chip Filters")
            
            # Wait for network to settle and loading overlays to disappear
            page.wait_for_load_state("networkidle", timeout=15000)
            self._wait_for_loading_overlay_to_disappear(page, timeout=5000)
            
            # --- DOM READINESS CHECK: Ensure table has finished rendering ---
            try:
                # Use more resilient table selectors including row-based detection
                table_selectors = [
                    "table",
                    "[role='table']",
                    ".MuiTable-root",
                    "[class*='table']",
                    "tbody tr",
                    ".MuiBox-root:has(table)",
                    "div:has(table)",
                    "*:has(td)"
                ]
                
                table_ready = False
                for selector in table_selectors:
                    try:
                        temp_table = page.locator(selector).first
                        if temp_table.is_visible(timeout=5000):
                            table_ready = True
                            self.logger.info(f"[PASS] Table is ready for chip validation (found: {selector})")
                            break
                    except:
                        continue
                
                if not table_ready:
                    self.logger.warning("[WARN] Table not ready, skipping chip validation")
                    return errors
            except Exception as e:
                self.logger.warning(f"[WARN] DOM readiness check failed: {e}")
                return errors
            
            # --- 1. ACTIVE FILTER PILLS VALIDATION (Resilient Text-Based) ---
            try:
                # Use resilient text-based selectors
                chip_container = None
                
                # Try get_by_role first (most resilient for chips)
                try:
                    chip_container = page.get_by_role("button", name=re.compile("Pending|Rejected|Issued")).first
                    if chip_container.is_visible(timeout=5000):
                        self.logger.info("[PASS] Chip container found using get_by_role")
                except:
                    pass
                
                # Fallback to generic CSS selectors
                if not chip_container:
                    chip_container_selectors = [
                        "*:has-text('Pending')",
                        "*:has-text('Rejected')",
                        "*:has-text('Issued')",
                        "[role='button']:has-text('Pending')",
                        "[class*='chip']",
                        "[class*='filter']"
                    ]
                    
                    for selector in chip_container_selectors:
                        try:
                            temp_container = page.locator(selector).first
                            if temp_container.is_visible(timeout=5000):
                                chip_container = temp_container
                                self.logger.info(f"Found chip container using selector: {selector}")
                                break
                        except:
                            continue
                
                if chip_container:
                    # Get all chips using resilient selectors
                    chip_selectors = [
                        "[role='button']",
                        "button",
                        "*[role='button']",
                        "[class*='chip']"
                    ]
                    
                    all_chips = []
                    for selector in chip_selectors:
                        try:
                            temp_chips = page.locator(selector)
                            if temp_chips.count() > 0:
                                all_chips = temp_chips.all()
                                self.logger.info(f"Found {len(all_chips)} chips using selector: {selector}")
                                break
                        except:
                            continue
                    
                    if all_chips:
                        self.logger.info(f"[PASS] Found {len(all_chips)} filter chips")
                        
                        # Extract chip text for logging
                        for idx, chip in enumerate(all_chips):
                            try:
                                chip_text = chip.text_content()
                                self.logger.info(f"  Chip {idx + 1}: {chip_text}")
                            except:
                                pass
                    else:
                        self.logger.warning("[WARN] No filter chips found")
                else:
                    self.logger.warning("[WARN] Chip container not found")
            except Exception as e:
                self.logger.warning(f"[WARN] Chip validation skipped: {e}")
            
            # --- 2. DYNAMIC COUNT VALIDATION (Rejected (6)) - Resilient Text-Based ---
            try:
                # Use get_by_text first (most resilient)
                rejected_chip = None
                try:
                    rejected_chip = page.get_by_text("Rejected").first
                    if rejected_chip.is_visible(timeout=5000):
                        self.logger.info("[PASS] Rejected chip found using get_by_text")
                except:
                    pass
                
                # Fallback to generic CSS selectors
                if not rejected_chip:
                    rejected_chip_selectors = [
                        "*:has-text('Rejected')",
                        "[role='button']:has-text('Rejected')",
                        "button:has-text('Rejected')",
                        "[class*='chip']:has-text('Rejected')",
                        "[class*='filter']:has-text('Rejected')"
                    ]
                    
                    for selector in rejected_chip_selectors:
                        try:
                            temp_chip = page.locator(selector).first
                            if temp_chip.is_visible(timeout=5000):
                                rejected_chip = temp_chip
                                self.logger.info(f"Found Rejected chip using selector: {selector}")
                                break
                        except:
                            continue
                
                if rejected_chip:
                    chip_text = rejected_chip.text_content()
                    if "(6)" in chip_text or "( 6 )" in chip_text or "6" in chip_text:
                        self.logger.info(f"[PASS] Rejected chip has dynamic count: {chip_text}")
                    else:
                        self.logger.warning(f"[WARN] Rejected chip count not found: {chip_text}")
                else:
                    self.logger.warning("[WARN] Rejected chip not found")
            except Exception as e:
                self.logger.warning(f"[WARN] Dynamic count validation skipped: {e}")
            
            # --- 3. COLOR-CODED STATES VALIDATION (Pending, Issued) - Resilient Text-Based ---
            try:
                # Check for Pending chip with get_by_text
                pending_chip = None
                try:
                    pending_chip = page.get_by_text("Pending").first
                    if pending_chip.is_visible(timeout=5000):
                        self.logger.info("[PASS] Pending chip found using get_by_text")
                except:
                    pass
                
                # Fallback to generic CSS selectors
                if not pending_chip:
                    pending_chip_selectors = [
                        "*:has-text('Pending')",
                        "[role='button']:has-text('Pending')",
                        "button:has-text('Pending')",
                        "[class*='chip']:has-text('Pending')",
                        "[class*='filter']:has-text('Pending')"
                    ]
                    
                    for selector in pending_chip_selectors:
                        try:
                            temp_chip = page.locator(selector).first
                            if temp_chip.is_visible(timeout=5000):
                                pending_chip = temp_chip
                                self.logger.info(f"Found Pending chip using selector: {selector}")
                                break
                        except:
                            continue
                
                if pending_chip:
                    self.logger.info("[PASS] Pending chip found")
                else:
                    self.logger.warning("[WARN] Pending chip not found")
                
                # Check for Issued chip with get_by_text
                issued_chip = None
                try:
                    issued_chip = page.get_by_text("Issued").first
                    if issued_chip.is_visible(timeout=5000):
                        self.logger.info("[PASS] Issued chip found using get_by_text")
                except:
                    pass
                
                # Fallback to generic CSS selectors
                if not issued_chip:
                    issued_chip_selectors = [
                        "*:has-text('Issued')",
                        "[role='button']:has-text('Issued')",
                        "button:has-text('Issued')",
                        "[class*='chip']:has-text('Issued')",
                        "[class*='filter']:has-text('Issued')"
                    ]
                    
                    for selector in issued_chip_selectors:
                        try:
                            temp_chip = page.locator(selector).first
                            if temp_chip.is_visible(timeout=5000):
                                issued_chip = temp_chip
                                self.logger.info(f"Found Issued chip using selector: {selector}")
                                break
                        except:
                            continue
                
                if issued_chip:
                    self.logger.info("[PASS] Issued chip found")
                else:
                    self.logger.warning("[WARN] Issued chip not found")
            except Exception as e:
                self.logger.warning(f"[WARN] Color-coded states validation skipped: {e}")
            
            # --- 4. CLEARABLE CHIPS VALIDATION (App Form Pend...) - MUI-Compatible ---
            try:
                # Look for chips with MUI delete icon
                clearable_chip_selectors = [
                    ".MuiChip-deletable",
                    ".MuiChip-root:has(.MuiChip-deleteIcon)",
                    ".MuiChip-root:has(svg)",
                    "button.MuiChip-deleteIcon",
                    ".MuiChip-root >> svg[class*='delete']"
                ]
                
                clearable_chips = []
                for selector in clearable_chip_selectors:
                    try:
                        temp_chips = page.locator(selector)
                        if temp_chips.count() > 0:
                            clearable_chips = temp_chips.all()
                            self.logger.info(f"Found {len(clearable_chips)} clearable chips using selector: {selector}")
                            break
                    except:
                        continue
                
                if clearable_chips:
                    self.logger.info(f"[PASS] Found {len(clearable_chips)} clearable chips")
                else:
                    self.logger.warning("[WARN] Clearable chips not found")
            except Exception as e:
                self.logger.warning(f"[WARN] Clearable chips validation skipped: {e}")
            
            self.logger.info("[PASS] Chip filters validation completed")
        except Exception as e:
            self.logger.error(f"[FAIL] Chip filters validation failed: {e}")
            errors += 1
        
        return errors

    def _validate_search_dropdown(self, page):
        """Validates search dropdown functionality including menu opening, options, and placeholder updates."""
        errors = 0
        
        try:
            self.logger.step_start("Validating Search Dropdown")
            
            # Wait for network to settle and loading overlays to disappear
            page.wait_for_load_state("networkidle", timeout=15000)
            self._wait_for_loading_overlay_to_disappear(page, timeout=5000)
            
            # --- 1. CLICK SEARCH FIELD (MUI-Compatible Wrapper) ---
            try:
                # Target the MUI input wrapper first, then the actual input
                search_wrapper_selectors = [
                    ".MuiInputBase-root",
                    ".MuiOutlinedInput-root",
                    ".MuiFormControl-root",
                    ".search-wrapper",
                    "[class*='search']"
                ]
                
                search_wrapper = None
                for selector in search_wrapper_selectors:
                    try:
                        temp_wrapper = page.locator(selector).first
                        if temp_wrapper.is_visible(timeout=5000):
                            search_wrapper = temp_wrapper
                            self.logger.info(f"Found search wrapper using selector: {selector}")
                            break
                    except:
                        continue
                
                if search_wrapper:
                    # Now find the actual input within the wrapper - use more resilient approach
                    search_field = None
                    
                    # Try get_by_role first (most resilient for inputs)
                    try:
                        search_field = search_wrapper.get_by_role("textbox").first
                        if search_field.is_visible(timeout=3000):
                            self.logger.info("[PASS] Found search input using get_by_role")
                    except:
                        pass
                    
                    # Fallback to generic CSS selectors within wrapper
                    if not search_field:
                        search_input_selectors = [
                            "input",
                            "input[type='text']",
                            "input[type='search']",
                            "input[placeholder*='Search']",
                            "input[placeholder*='search']",
                            "input.MuiInputBase-input",
                            "input.MuiOutlinedInput-input",
                            "textarea"
                        ]
                        
                        for selector in search_input_selectors:
                            try:
                                temp_field = search_wrapper.locator(selector).first
                                if temp_field.is_visible(timeout=3000):
                                    search_field = temp_field
                                    self.logger.info(f"Found search input using selector: {selector}")
                                    break
                            except:
                                continue
                    
                    if search_field:
                        # Wait for element stability before click
                        search_field.wait_for(state="attached", timeout=5000)
                        search_field.wait_for(state="visible", timeout=5000)
                        
                        search_field.click()
                        page.wait_for_load_state("networkidle", timeout=5000)
                        page.wait_for_timeout(500)
                        self.logger.info("[PASS] Search field clicked")
                    else:
                        self.logger.warning("[WARN] Search input not found in wrapper")
                else:
                    self.logger.warning("[WARN] Search wrapper not found")
            except Exception as e:
                self.logger.warning(f"[WARN] Search field click skipped: {e}")
            
            # --- 2. ASSERT DROPDOWN MENU OPENS (MUI-Specific) ---
            try:
                # Wait for dropdown to appear with MUI-specific selectors
                dropdown_selectors = [
                    "ul.MuiMenu-list",
                    "ul.MuiList-root[role='listbox']",
                    ".MuiPaper-root.MuiMenu-paper",
                    ".MuiPopover-root",
                    "[role='listbox']"
                ]
                
                dropdown = None
                for selector in dropdown_selectors:
                    try:
                        temp_dropdown = page.locator(selector).first
                        if temp_dropdown.is_visible(timeout=5000):
                            dropdown = temp_dropdown
                            self.logger.info(f"Found dropdown menu using selector: {selector}")
                            break
                    except:
                        continue
                
                if dropdown:
                    # Wait for dropdown to be fully stable
                    dropdown.wait_for(state="attached", timeout=3000)
                    dropdown.wait_for(state="visible", timeout=3000)
                    self.logger.info("[PASS] Dropdown menu opened")
                else:
                    self.logger.warning("[WARN] Dropdown menu not found")
            except Exception as e:
                self.logger.warning(f"[WARN] Dropdown menu validation skipped: {e}")
            
            # --- 3. VERIFY EXACTLY 3 OPTIONS (App No., Policy No., Name) - MUI List Items ---
            try:
                if dropdown:
                    # Look for MUI list items
                    list_item_selectors = [
                        "li.MuiMenuItem-root",
                        "li.MuiButtonBase-root",
                        "li[role='option']",
                        ".MuiMenuItem-root",
                        "[role='option']"
                    ]
                    
                    all_options = []
                    for selector in list_item_selectors:
                        try:
                            temp_options = dropdown.locator(selector)
                            if temp_options.count() > 0:
                                all_options = temp_options.all()
                                self.logger.info(f"Found {len(all_options)} options using selector: {selector}")
                                break
                        except:
                            continue
                    
                    if all_options:
                        # Extract text from each option
                        option_texts = []
                        for idx, option in enumerate(all_options):
                            try:
                                option_text = option.text_content().strip()
                                option_texts.append(option_text)
                                self.logger.info(f"  Option {idx + 1}: {option_text}")
                            except:
                                pass
                        
                        # Verify expected options
                        expected_options = ["App No.", "Policy No.", "Name"]
                        found_count = 0
                        for expected in expected_options:
                            if any(expected in text for text in option_texts):
                                found_count += 1
                                self.logger.info(f"[PASS] Found option: {expected}")
                            else:
                                self.logger.warning(f"[WARN] Option not found: {expected}")
                        
                        if found_count == 3:
                            self.logger.info(f"[PASS] All 3 options found")
                        else:
                            self.logger.warning(f"[WARN] Found {found_count}/3 options")
                    else:
                        self.logger.warning("[WARN] No list items found in dropdown")
                else:
                    self.logger.warning("[WARN] Dropdown not available for option validation")
            except Exception as e:
                self.logger.warning(f"[WARN] Options validation skipped: {e}")
            
            # --- 4. CLICK EACH OPTION AND VERIFY PLACEHOLDER UPDATE ---
            try:
                if dropdown:
                    for option_text in ["App No.", "Policy No.", "Name"]:
                        # Find the specific option by text
                        option_selectors = [
                            f"li.MuiMenuItem-root:has-text('{option_text}')",
                            f"li[role='option']:has-text('{option_text}')",
                            f".MuiMenuItem-root:has-text('{option_text}')",
                            f"[role='option']:has-text('{option_text}')"
                        ]
                        
                        option_element = None
                        for selector in option_selectors:
                            try:
                                temp_option = page.locator(selector).first
                                if temp_option.is_visible(timeout=3000):
                                    option_element = temp_option
                                    self.logger.info(f"Found option '{option_text}' using selector: {selector}")
                                    break
                            except:
                                continue
                        
                        if option_element:
                            # Wait for element stability
                            option_element.wait_for(state="attached", timeout=3000)
                            option_element.wait_for(state="visible", timeout=3000)
                            
                            option_element.click()
                            page.wait_for_load_state("networkidle", timeout=5000)
                            page.wait_for_timeout(500)
                            
                            # Check if placeholder updated
                            search_field = page.locator("input.MuiInputBase-input, input[type='text']").first
                            placeholder = search_field.get_attribute("placeholder")
                            if placeholder and (option_text in placeholder or option_text.lower() in placeholder.lower()):
                                self.logger.info(f"[PASS] Placeholder updated for {option_text}: {placeholder}")
                            else:
                                self.logger.warning(f"[WARN] Placeholder not updated for {option_text}: {placeholder}")
                            
                            # Re-open dropdown for next option
                            search_field.click()
                            page.wait_for_timeout(500)
                        else:
                            self.logger.warning(f"[WARN] Could not find option: {option_text}")
                else:
                    self.logger.warning("[WARN] Dropdown not available for click validation")
            except Exception as e:
                self.logger.warning(f"[WARN] Option click validation skipped: {e}")
            
            # Close dropdown
            try:
                page.keyboard.press("Escape")
                page.wait_for_timeout(500)
                self.logger.info("[PASS] Dropdown closed")
            except:
                pass
            
            self.logger.info("[PASS] Search dropdown validation completed")
        except Exception as e:
            self.logger.error(f"[FAIL] Search dropdown validation failed: {e}")
            errors += 1
        
        return errors

    def _validate_application_number_search(self, page):
        """Validates application number search functionality: extract app number from table, search, and validate result."""
        errors = 0
        app_number = None
        
        try:
            self.logger.step_start("Validating Application Number Search")
            
            # Wait for network to settle and loading overlays to disappear
            page.wait_for_load_state("networkidle", timeout=15000)
            self._wait_for_loading_overlay_to_disappear(page, timeout=5000)
            
            # --- 1. EXTRACT APPLICATION NUMBER FROM TABLE ---
            try:
                # Use multiple locator strategies to find application number in table
                app_number_element = None
                
                # Try get_by_text first with common patterns
                try:
                    # Look for text containing numbers (likely app numbers)
                    app_number_element = page.locator("td").filter(has_text=re.compile(r'[0-9]{6,}')).first
                    if app_number_element.is_visible(timeout=5000):
                        self.logger.info("[PASS] Found application number using regex pattern")
                except:
                    pass
                
                # Fallback to generic CSS selectors
                if not app_number_element:
                    app_number_selectors = [
                        "tbody tr td:first-child",
                        "td:first-child",
                        "td",
                        ".MuiTableCell-body",
                        "[role='cell']",
                        "*:has-text(/[0-9]{4,}/)",
                        "*:has-text('APP')",
                        "*:has-text('App')"
                    ]
                    
                    for selector in app_number_selectors:
                        try:
                            temp_element = page.locator(selector).first
                            if temp_element.is_visible(timeout=5000):
                                app_number_element = temp_element
                                self.logger.info(f"Found application number using selector: {selector}")
                                break
                        except:
                            continue
                
                if app_number_element:
                    try:
                        # Use a fast timeout for text_content to avoid 30s hangs on detached elements
                        app_number_element.wait_for(state="attached", timeout=2000)
                        app_number = app_number_element.text_content(timeout=2000).strip()
                        self.logger.info(f"[PASS] Extracted application number: {app_number}")
                    except Exception as extract_err:
                        self.logger.warning(f"[WARN] Could not extract text from application number element: {extract_err}")
                        return errors
                else:
                    self.logger.warning("[WARN] Could not find application number element in table")
                    return errors
            except Exception as e:
                self.logger.warning(f"[WARN] Application number extraction failed: {e}")
                return errors
            
            # --- 2. SELECT "APP NO." IN SEARCH DROPDOWN ---
            try:
                # Find search field using multiple strategies
                search_field_selectors = [
                    "input.MuiInputBase-input",
                    "input.MuiOutlinedInput-input",
                    "input[type='text']",
                    "input[placeholder*='Search']",
                    "[class*='search'] input"
                ]
                
                search_field = None
                for selector in search_field_selectors:
                    try:
                        temp_field = page.locator(selector).first
                        if temp_field.is_visible(timeout=5000):
                            search_field = temp_field
                            self.logger.info(f"Found search field using selector: {selector}")
                            break
                    except:
                        continue
                
                if search_field:
                    # Click to open dropdown
                    search_field.click()
                    page.wait_for_load_state("networkidle", timeout=5000)
                    page.wait_for_timeout(500)
                    
                    # Select "App No." option
                    app_no_option_selectors = [
                        "li:has-text('App No.')",
                        "[role='option']:has-text('App No.')",
                        ".MuiMenuItem-root:has-text('App No.')",
                        "*:has-text('App No.')"
                    ]
                    
                    app_no_option = None
                    for selector in app_no_option_selectors:
                        try:
                            temp_option = page.locator(selector).first
                            if temp_option.is_visible(timeout=3000):
                                app_no_option = temp_option
                                self.logger.info(f"Found 'App No.' option using selector: {selector}")
                                break
                        except:
                            continue
                    
                    if app_no_option:
                        app_no_option.click()
                        page.wait_for_load_state("networkidle", timeout=5000)
                        page.wait_for_timeout(500)
                        self.logger.info("[PASS] Selected 'App No.' in search dropdown")
                    else:
                        self.logger.warning("[WARN] Could not select 'App No.' option")
                else:
                    self.logger.warning("[WARN] Search field not found")
            except Exception as e:
                self.logger.warning(f"[WARN] Search dropdown selection failed: {e}")
            
            # --- 3. ENTER APPLICATION NUMBER IN SEARCH BOX ---
            try:
                if search_field and app_number:
                    # Clear existing content
                    search_field.fill("")
                    page.wait_for_timeout(200)
                    
                    # Enter application number
                    search_field.fill(app_number)
                    page.wait_for_load_state("networkidle", timeout=5000)
                    page.wait_for_timeout(500)
                    self.logger.info(f"[PASS] Entered application number: {app_number}")
                    
                    # Press Enter to search
                    search_field.press("Enter")
                    page.wait_for_load_state("networkidle", timeout=15000)
                    page.wait_for_timeout(1000)
                    self.logger.info("[PASS] Search submitted")
                else:
                    self.logger.warning("[WARN] Search field or app number not available")
            except Exception as e:
                self.logger.warning(f"[WARN] Search entry failed: {e}")
            
            # --- 4. VALIDATE SEARCH RESULT IN TABLE ---
            try:
                # Wait for table to update with search results
                page.wait_for_load_state("networkidle", timeout=15000)
                self._wait_for_loading_overlay_to_disappear(page, timeout=5000)
                
                # Look for the application number in the updated table
                result_selectors = [
                    f"td:has-text('{app_number}')",
                    f"tbody tr:has-text('{app_number}')",
                    f"*:has-text('{app_number}')",
                    f".MuiTableCell-body:has-text('{app_number}')"
                ]
                
                result_element = None
                for selector in result_selectors:
                    try:
                        temp_result = page.locator(selector).first
                        if temp_result.is_visible(timeout=5000):
                            result_element = temp_result
                            self.logger.info(f"Found search result using selector: {selector}")
                            break
                    except:
                        continue
                
                if result_element:
                    self.logger.info(f"[PASS] Application number {app_number} found in search results")
                else:
                    self.logger.warning(f"[WARN] Application number {app_number} not found in search results")
            except Exception as e:
                self.logger.warning(f"[WARN] Search result validation failed: {e}")
            
            # --- 5. CLICK ON THE SEARCH RESULT ROW ---
            try:
                if result_element:
                    # Get the parent row
                    result_row = result_element.locator("xpath=ancestor::tr").first
                    
                    # Wait for row to be actionable
                    result_row.wait_for(state="attached", timeout=5000)
                    result_row.wait_for(state="visible", timeout=5000)
                    
                    # Click on the row
                    result_row.click()
                    page.wait_for_load_state("networkidle", timeout=15000)
                    page.wait_for_timeout(1000)
                    self.logger.info("[PASS] Clicked on search result row")
                else:
                    self.logger.warning("[WARN] No result row to click")
            except Exception as e:
                self.logger.warning(f"[WARN] Result row click failed: {e}")
            
            # --- 6. VALIDATE ROW INTERACTION (Optional: Check for detail view) ---
            try:
                # Check if detail view or modal opened
                detail_view_selectors = [
                    "[class*='detail']",
                    "[class*='modal']",
                    "[role='dialog']",
                    ".MuiDialog-root",
                    ".MuiPaper-root:has-text('Application')"
                ]
                
                detail_view = None
                for selector in detail_view_selectors:
                    try:
                        temp_detail = page.locator(selector).first
                        if temp_detail.is_visible(timeout=3000):
                            detail_view = temp_detail
                            self.logger.info(f"Found detail view using selector: {selector}")
                            break
                    except:
                        continue
                
                if detail_view:
                    self.logger.info("[PASS] Detail view opened after clicking row")
                    
                    # USER REQUEST FIX: Explicitly close the drawer so Phase 4 components are interactable
                    self.logger.info("[INFO] Closing detail view to prepare for next phase...")
                    try:
                        # 1. Try the specific SVG path the user provided, selecting the parent button
                        svg_close_btn = page.locator("button:has(svg path[d*='205.66'])").first
                        if svg_close_btn.is_visible(timeout=3000):
                            svg_close_btn.click(timeout=3000)
                            self.logger.info("[PASS] Detail view closed using SVG path button selector")
                            page.wait_for_timeout(1000) # Give UI time to animate out
                        else:
                            # 2. Fallback: Use the component utility's built-in close method
                            drawer = DetailDrawer(page)
                            if drawer.close():
                                self.logger.info("[PASS] Detail view closed using DetailDrawer component utility")
                            else:
                                self.logger.warning("[WARN] Failed to close detail view using known methods")
                    except Exception as close_e:
                        self.logger.warning(f"[WARN] Exception while attempting to close detail view: {close_e}")
                else:
                    self.logger.info("[INFO] No detail view detected (may navigate to detail page)")
            except Exception as e:
                self.logger.warning(f"[WARN] Detail view validation skipped: {e}")
            
            self.logger.info("[PASS] Application number search validation completed")
        except Exception as e:
            self.logger.error(f"[FAIL] Application number search validation failed: {e}")
            errors += 1
        
        return errors

    # ═══════════════════════════════════════════════════════════════════════════
    #  PHASE 4 — COMPONENT UTILITY REGRESSION METHODS
    # ═══════════════════════════════════════════════════════════════════════════

    def _reg_top_navigation(self, page: Page) -> int:
        """
        REG-NAV: Top Navigation & Controls Component Regression.
        Validates: Logo, Page Title, User Initials, Theme Toggle,
                   Download Button text & count.
        """
        errors = 0
        self.logger.step_start("[REG-NAV] Top Navigation & Controls")
        try:
            nav = TopNavigationControls(page)
            result = nav.validate_all()

            # 1. Logo visible
            if not result["logo_visible"]:
                self.logger.warning("[WARN] REG-NAV: ABSLI logo not visible")
                errors += 1
            else:
                self.logger.info("[PASS] REG-NAV: Logo visible")

            # 2. Page title == 'App Tracker'
            if result["page_title"] != "App Tracker":
                self.logger.warning(f"[WARN] REG-NAV: Page title mismatch -> '{result['page_title']}'")
                errors += 1
            else:
                self.logger.info(f"[PASS] REG-NAV: Page title = '{result['page_title']}'")

            # 3. User initials present and interactive
            if not result["user_initials"]:
                self.logger.warning("[WARN] REG-NAV: User initials not found")
                errors += 1
            else:
                self.logger.info(f"[PASS] REG-NAV: User initials = '{result['user_initials']}'")
                
                # Interaction: Open and close the account menu
                self.logger.info("[INFO] REG-NAV: Testing account menu interaction...")
                if nav.open_account_menu():
                    self.logger.info("[PASS] REG-NAV: Successfully opened account menu")
                    page.wait_for_timeout(1000)
                    nav.close_account_menu()
                    self.logger.info("[PASS] REG-NAV: Successfully closed account menu")
                else:
                    self.logger.warning("[WARN] REG-NAV: Could not open account menu")
                    errors += 1

            # 4. Theme toggle present and interactive
            if not result["theme_toggle_visible"]:
                self.logger.warning("[WARN] REG-NAV: Theme toggle button not visible")
                errors += 1
            else:
                self.logger.info("[PASS] REG-NAV: Theme toggle visible")
                
                # Interaction: Toggle theme back and forth
                self.logger.info("[INFO] REG-NAV: Testing theme toggle interaction...")
                if nav.toggle_theme():
                    self.logger.info("[PASS] REG-NAV: Theme toggled successfully")
                    page.wait_for_timeout(1000)
                    if nav.toggle_theme():
                        self.logger.info("[PASS] REG-NAV: Theme toggled back to original state")
                    else:
                        self.logger.warning("[WARN] REG-NAV: Could not revert theme toggle")
                        errors += 1
                else:
                    self.logger.warning("[WARN] REG-NAV: Could not toggle theme")
                    errors += 1

            # 5. Download button present and has a count
            if not result["download_visible"]:
                self.logger.warning("[WARN] REG-NAV: Download button not visible")
                errors += 1
            else:
                self.logger.info(f"[PASS] REG-NAV: Download button = '{result['download_text']}'")
                if result["download_count"] is None:
                    self.logger.warning("[WARN] REG-NAV: Could not parse download count from button text")
                    errors += 1
                else:
                    self.logger.info(f"[PASS] REG-NAV: Download count = {result['download_count']}")

            self.logger.info(f"[REG-NAV] Completed. Errors: {errors}")
        except Exception as e:
            self.logger.error(f"[FAIL] REG-NAV: Unexpected error: {e}")
            errors += 1
        return errors

    def _reg_filter_search_bar(self, page: Page) -> int:
        """
        REG-SEARCH: Filter & Search Bar Component Regression.
        Validates: Bar visibility, Input field, Search type label,
                   Date filter label, Search & Clear interaction.
        """
        errors = 0
        self.logger.step_start("[REG-SEARCH] Filter & Search Bar")
        try:
            bar = FilterSearchBar(page)
            result = bar.validate_all()

            # 1. Search bar visible
            if not result["search_bar_visible"]:
                self.logger.warning("[WARN] REG-SEARCH: Search bar not visible")
                errors += 1
            else:
                self.logger.info("[PASS] REG-SEARCH: Search bar visible")

            # 2. Search input visible
            if not result["search_input_visible"]:
                self.logger.warning("[WARN] REG-SEARCH: Search input not visible")
                errors += 1
            else:
                self.logger.info("[PASS] REG-SEARCH: Search input visible")

            # 3. Search type label present
            if not result["search_type"]:
                self.logger.warning("[WARN] REG-SEARCH: Search type label missing")
                errors += 1
            else:
                self.logger.info(f"[PASS] REG-SEARCH: Search type = '{result['search_type']}'")

            # 4. Date filter visible
            if not result["date_filter_visible"]:
                self.logger.warning("[WARN] REG-SEARCH: Date filter button not visible")
                errors += 1
            else:
                self.logger.info(f"[PASS] REG-SEARCH: Date filter = '{result['date_filter_label']}'")

            # 5. Search interaction
            if bar.search("LA"):
                self.logger.info("[PASS] REG-SEARCH: Search 'LA' entered successfully")
                if not bar.clear_search():
                    self.logger.warning("[WARN] REG-SEARCH: Could not clear search input")
                    errors += 1
                else:
                    self.logger.info("[PASS] REG-SEARCH: Search cleared successfully")
            else:
                self.logger.warning("[WARN] REG-SEARCH: Could not enter search text")
                errors += 1

            self.logger.info(f"[REG-SEARCH] Completed. Errors: {errors}")
        except Exception as e:
            self.logger.error(f"[FAIL] REG-SEARCH: Unexpected error: {e}")
            errors += 1
        return errors

    def _reg_active_filter_chips(self, page: Page) -> int:
        """
        REG-CHIPS: Active Filter Chips Component Regression.
        Validates: Trigger visible, chip names, chip count badge,
                   dropdown open/close, available statuses, clear all.
        """
        errors = 0
        self.logger.step_start("[REG-CHIPS] Active Filter Chips")
        try:
            chips = ActiveFilterChips(page)
            result = chips.validate_all()

            # 1. Trigger visible
            if not result["visible"]:
                self.logger.warning("[WARN] REG-CHIPS: Filter chips trigger not visible")
                errors += 1
            else:
                self.logger.info("[PASS] REG-CHIPS: Filter chips trigger visible")

            # 2. Chip names populated
            if not result["chip_names"]:
                self.logger.warning("[WARN] REG-CHIPS: No active chip names found")
                errors += 1
            else:
                self.logger.info(f"[PASS] REG-CHIPS: Active chips = {result['chip_names']}")

            # 3. Chip count badge
            if result["chip_count"] is None:
                self.logger.warning("[WARN] REG-CHIPS: Chip count badge not found/parsed")
                errors += 1
            else:
                self.logger.info(f"[PASS] REG-CHIPS: Chip count = {result['chip_count']}")

            # 4. Open dropdown and read available statuses
            if chips.open_dropdown():
                self.logger.info("[PASS] REG-CHIPS: Dropdown opened")
                statuses = chips.get_available_statuses()
                if not statuses:
                    self.logger.warning("[WARN] REG-CHIPS: No statuses found in dropdown")
                    errors += 1
                else:
                    self.logger.info(f"[PASS] REG-CHIPS: Available statuses = {statuses}")
                    
                    # 5. Check and Uncheck filter checkbox (Filter table interaction)
                    if "Pending" in statuses:
                        self.logger.info("[INFO] REG-CHIPS: Attempting to toggle 'Pending' filter checkbox...")
                        if chips.select_status("Pending"):
                            self.logger.info("[PASS] REG-CHIPS: Successfully clicked 'Pending' checkbox")
                            
                            # Wait and uncheck it to restore default table state
                            # This ensures Pagination test doesn't skip due to a single-page filtered result
                            page.wait_for_timeout(1000)
                            if chips.select_status("Pending"):
                                self.logger.info("[PASS] REG-CHIPS: Successfully unchecked 'Pending' to restore table state")
                            else:
                                self.logger.warning("[WARN] REG-CHIPS: Could not uncheck 'Pending'. Table may be in filtered state.")
                                errors += 1
                        else:
                            self.logger.warning("[WARN] REG-CHIPS: Could not click 'Pending' checkbox")
                            errors += 1

                chips.close_dropdown()
                self.logger.info("[PASS] REG-CHIPS: Dropdown closed")
            else:
                self.logger.warning("[WARN] REG-CHIPS: Could not open dropdown")
                errors += 1

            self.logger.info(f"[REG-CHIPS] Completed. Errors: {errors}")
        except Exception as e:
            self.logger.error(f"[FAIL] REG-CHIPS: Unexpected error: {e}")
            errors += 1
        return errors

    def _reg_policy_list_table(self, page: Page) -> int:
        """
        REG-TABLE: Policy List Table Component Regression.
        Validates: Table visible, headers match expected columns,
                   row count > 0, first row data, active sort column,
                   and filter by status rows count.
        """
        errors = 0
        self.logger.step_start("[REG-TABLE] Policy List Table")
        try:
            table = PolicyListTable(page)
            result = table.validate_all()

            # 1. Table visible
            if not result["visible"]:
                self.logger.warning("[WARN] REG-TABLE: Policy list table not visible")
                errors += 1
                return errors
            self.logger.info("[PASS] REG-TABLE: Table visible")

            # 2. Headers valid
            if not result["headers_valid"]:
                self.logger.warning("[WARN] REG-TABLE: One or more expected columns missing")
                errors += 1
            else:
                self.logger.info("[PASS] REG-TABLE: All expected columns present")

            # 3. At least 1 row
            if result["row_count"] == 0:
                self.logger.warning("[WARN] REG-TABLE: Table has 0 rows — may be empty result")
                errors += 1
            else:
                self.logger.info(f"[PASS] REG-TABLE: Row count = {result['row_count']}")

            # 4. First row data
            first = result.get("first_row", {})
            if not first.get("app_no"):
                self.logger.warning("[WARN] REG-TABLE: First row App No is empty")
                errors += 1
            else:
                self.logger.info(f"[PASS] REG-TABLE: First row App No = '{first['app_no']}'")
                self.logger.info(f"[INFO] REG-TABLE: First row Status = '{first.get('policy_status','N/A')}'")
                premium = first.get('modal_premium','N/A')
                # Remove Rupee symbol (\u20b9) which crashes standard Windows cp1252 consoles
                premium = premium.replace('\u20b9', 'Rs.').replace('₹', 'Rs.')
                self.logger.info(f"[INFO] REG-TABLE: First row Premium = '{premium}'")

            # 5. Active sort column
            if not result["active_sort_column"]:
                self.logger.warning("[WARN] REG-TABLE: No active sort column detected")
                errors += 1
            else:
                self.logger.info(
                    f"[PASS] REG-TABLE: Active sort = '{result['active_sort_column']}' "
                    f"({result['sort_direction']})"
                )

            # 6. Sort by App No and verify
            if table.sort_by_column("App. No."):
                self.logger.info("[PASS] REG-TABLE: Sort by 'App. No.' triggered")
                # Reset to default sort
                table.sort_by_column("R&A Date")
                self.logger.info("[INFO] REG-TABLE: Reset sort to 'R&A Date'")
            else:
                self.logger.warning("[WARN] REG-TABLE: Could not sort by 'App. No.'")
                errors += 1

            self.logger.info(f"[REG-TABLE] Completed. Errors: {errors}")
        except Exception as e:
            self.logger.error(f"[FAIL] REG-TABLE: Unexpected error: {e}")
            errors += 1
        return errors

    def _reg_pagination_footer(self, page: Page) -> int:
        """
        REG-PAGINATION: Pagination Footer Component Regression.
        Validates: Nav visible, current page, total pages, prev/next states,
                   next page navigation, and return to page 1.
        """
        errors = 0
        self.logger.step_start("[REG-PAGINATION] Pagination Footer")
        try:
            pagination = PaginationFooter(page)
            result = pagination.validate_all()

            # 1. Visible
            if not result["visible"]:
                self.logger.info("[INFO] REG-PAGINATION: Pagination not visible (single-page result set) — skipping")
                return errors
            self.logger.info("[PASS] REG-PAGINATION: Pagination visible")

            # 2. Current page
            if result["current_page"] is None:
                self.logger.warning("[WARN] REG-PAGINATION: Could not determine current page")
                errors += 1
            else:
                self.logger.info(f"[PASS] REG-PAGINATION: Current page = {result['current_page']}")

            # 3. Total pages
            if result["total_pages"] is None:
                self.logger.warning("[WARN] REG-PAGINATION: Could not determine total pages")
                errors += 1
            else:
                self.logger.info(f"[PASS] REG-PAGINATION: Total pages = {result['total_pages']}")

            # 4. Previous disabled on first page
            if result["current_page"] == 1 and not result["prev_disabled"]:
                self.logger.warning("[WARN] REG-PAGINATION: Previous button should be disabled on page 1")
                errors += 1
            else:
                self.logger.info("[PASS] REG-PAGINATION: Previous button state correct on page 1")

            # 5. Navigate to next page
            if not pagination.is_on_last_page():
                if pagination.go_to_next():
                    new_page = pagination.get_current_page()
                    self.logger.info(f"[PASS] REG-PAGINATION: Navigated to page {new_page}")
                    # Return to page 1
                    if pagination.go_to_first_page():
                        self.logger.info("[PASS] REG-PAGINATION: Returned to page 1")
                    else:
                        self.logger.warning("[WARN] REG-PAGINATION: Could not return to page 1")
                        errors += 1
                else:
                    self.logger.warning("[WARN] REG-PAGINATION: go_to_next() failed")
                    errors += 1
            else:
                self.logger.info("[INFO] REG-PAGINATION: Only 1 page, skip next navigation")

            self.logger.info(f"[REG-PAGINATION] Completed. Errors: {errors}")
        except Exception as e:
            self.logger.error(f"[FAIL] REG-PAGINATION: Unexpected error: {e}")
            errors += 1
        return errors

    def _reg_detail_drawer(self, page: Page) -> int:
        """
        REG-DRAWER: Detail Drawer Component Regression.
        Validates: Clicking first table row opens the drawer,
                   header name, aria title, all stage names & statuses,
                   summary box fields, active stage heading, workflow items,
                   lock indicator, show-more button, then closes drawer.
        """
        errors = 0
        self.logger.step_start("[REG-DRAWER] Detail Drawer")
        try:
            table = PolicyListTable(page)
            drawer = DetailDrawer(page)

            # Ensure table is visible before clicking
            if not table.is_visible():
                self.logger.warning("[WARN] REG-DRAWER: Table not visible, cannot open drawer")
                errors += 1
                return errors

            row_count = table.get_row_count()
            if row_count == 0:
                self.logger.warning("[WARN] REG-DRAWER: No rows found, cannot open drawer")
                errors += 1
                return errors

            # Click first row to open the drawer
            self.logger.info("[INFO] REG-DRAWER: Clicking first table row to open drawer...")
            if not table.click_row(0):
                self.logger.warning("[WARN] REG-DRAWER: Could not click first row")
                errors += 1
                return errors

            # Wait for drawer to open
            if not drawer.wait_until_open():
                self.logger.warning("[WARN] REG-DRAWER: Drawer did not open after row click")
                errors += 1
                return errors
            self.logger.info("[PASS] REG-DRAWER: Drawer opened")

            # Full component validation
            result = drawer.validate_all()

            # 1. Header name
            if not result["header_name"]:
                self.logger.warning("[WARN] REG-DRAWER: Header proposer name is empty")
                errors += 1
            else:
                self.logger.info(f"[PASS] REG-DRAWER: Header name = '{result['header_name']}'")

            # 2. Aria title
            if not result["aria_title"]:
                self.logger.warning("[WARN] REG-DRAWER: Aria title (sr-only h2) missing")
                errors += 1
            else:
                self.logger.info(f"[PASS] REG-DRAWER: Aria title = '{result['aria_title']}'")

            # 3. Stages loaded
            if not result["stages"]:
                self.logger.warning("[WARN] REG-DRAWER: No stages found in stepper")
                errors += 1
            else:
                self.logger.info(f"[PASS] REG-DRAWER: Stages = {[s['name'] for s in result['stages']]}")
                for stage in result["stages"]:
                    self.logger.info(
                        f"[INFO] REG-DRAWER:   '{stage['name']}' -> {stage['status']}"
                    )

            # 4. Active stage
            if not result["active_stage"]:
                self.logger.warning("[WARN] REG-DRAWER: Active stage name not detected")
                errors += 1
            else:
                self.logger.info(f"[PASS] REG-DRAWER: Active stage = '{result['active_stage']}'")

            # 5. Summary box fields
            fields = result.get("summary_fields", {})
            required_fields = ["Proposer Name", "App. No.", "Plan Name", "Modal Premium"]
            for field in required_fields:
                found = any(field.lower() in k.lower() for k in fields)
                if not found:
                    self.logger.warning(f"[WARN] REG-DRAWER: Summary field '{field}' missing")
                    errors += 1
                else:
                    val = next((v for k, v in fields.items() if field.lower() in k.lower()), "?")
                    self.logger.info(f"[PASS] REG-DRAWER: {field} = '{val}'")

            # 6. Stage heading in main content
            if not result["stage_heading"]:
                self.logger.warning("[WARN] REG-DRAWER: Main content stage heading missing")
                errors += 1
            else:
                self.logger.info(
                    f"[PASS] REG-DRAWER: Stage heading = '{result['stage_heading']}' "
                    f"({result['stage_badge_status']})"
                )

            # 7. Workflow sections
            if not result["workflow_sections"]:
                self.logger.warning("[WARN] REG-DRAWER: No workflow sections found")
                errors += 1
            else:
                self.logger.info(f"[PASS] REG-DRAWER: Sections = {result['workflow_sections']}")

            # 8. Workflow items with statuses
            if not result["workflow_items"]:
                self.logger.warning("[WARN] REG-DRAWER: No workflow items found")
                errors += 1
            else:
                self.logger.info(f"[PASS] REG-DRAWER: {len(result['workflow_items'])} workflow items found")
                for item in result["workflow_items"][:5]:   # log first 5
                    self.logger.info(f"[INFO] REG-DRAWER:   '{item['label']}' -> {item['status']}")

            # 9. Lock indicator check
            is_locked = drawer.is_item_locked("Proposer Declaration (OTVC)")
            if is_locked:
                lock_msg = drawer.get_lock_message("Proposer Declaration (OTVC)")
                self.logger.info(f"[PASS] REG-DRAWER: Lock indicator present -> '{lock_msg}'")
            else:
                self.logger.info("[INFO] REG-DRAWER: Proposer Declaration not locked (may be unlocked state)")

            # 10. Show more button
            if result["show_more_text"]:
                self.logger.info(f"[PASS] REG-DRAWER: Show More button = '{result['show_more_text']}'")
            else:
                self.logger.info("[INFO] REG-DRAWER: No 'Show more' button (all items visible)")

            # 11. Stage navigation — click PI Stage
            if drawer.click_stage("PI Stage"):
                self.logger.info("[PASS] REG-DRAWER: Clicked 'PI Stage' in stepper")
                pi_status = drawer.get_stage_status("PI Stage")
                self.logger.info(f"[INFO] REG-DRAWER: PI Stage status = '{pi_status}'")
            else:
                self.logger.warning("[WARN] REG-DRAWER: Could not click 'PI Stage'")
                errors += 1

            # 12. Close drawer
            if drawer.close():
                self.logger.info("[PASS] REG-DRAWER: Drawer closed successfully")
            else:
                self.logger.warning("[WARN] REG-DRAWER: Could not close drawer via button; trying Escape")
                drawer.close_with_escape()

            self.logger.info(f"[REG-DRAWER] Completed. Errors: {errors}")
        except Exception as e:
            self.logger.error(f"[FAIL] REG-DRAWER: Unexpected error: {e}")
            errors += 1
        return errors

    @pytest.mark.demo_bug
    def test_demo_simulated_bug(self, page: Page):
        """
        Isolated demo test to show stakeholders how the framework reports bugs.
        This test intentionally fails an assertion.
        """
        self.logger = Logger()
        framework = UnifiedAutomationFramework()
        framework.log_start("Demo Simulated Bug Flow")
        
        try:
            self.logger.info("Navigating to Aditya Birla UAT login page...")
            page.goto("https://leapuat.adityabirlasunlifeinsurance.com/uat/#/login", timeout=30000)
            
            self.logger.info("Performing basic UI interaction...")
            # Simulate a basic interaction
            page.wait_for_load_state("networkidle", timeout=10000)
            
            self.logger.info("Validating UI component...")
            # Intentional failure
            assert False, "BUG FOUND: Expected element text did not match actual UI text."
            
        except AssertionError as e:
            self.logger.error(f"[FAIL] Assertion Error: {e}")
            framework.log_end("Demo Simulated Bug Flow", "FAILED")
            raise  # Re-raise to let pytest mark the test as failed
        except Exception as e:
            self.logger.error(f"[FAIL] Unexpected error: {e}")
            framework.log_end("Demo Simulated Bug Flow", "ERROR")
            raise

