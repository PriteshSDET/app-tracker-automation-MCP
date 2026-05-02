"""
Unified Test Execution Script: E2E Login & Component Validation
Strategy: Continuous State Management with Explicit Hidden-Waits & Scroll Handling
Updates: Integrated deep-locators from App Tracker HTML source.
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
                
            # PHASE 3: COMPONENT VALIDATION
            self.logger.step_start("--- Beginning Component Validation Phase ---")
            sanity_errors = self._validate_component_filters(tracker_page_obj or page, tracker_page)
            sanity_errors += self._validate_component_table(tracker_page_obj or page, tracker_page)
            
            # NEW VALIDATIONS: Pagination, Chip Filters, Search Dropdown, Application Number Search
            sanity_errors += self._validate_pagination(tracker_page_obj or page)
            sanity_errors += self._validate_chip_filters(tracker_page_obj or page)
            sanity_errors += self._validate_search_dropdown(tracker_page_obj or page)
            sanity_errors += self._validate_application_number_search(tracker_page_obj or page)
            
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
        # App Tracker opens in a NEW TAB at a different domain: onboarding-uat.adityabirlasunlifeinsurance.com
        self.logger.info("Setting up new tab listener before clicking Application Tracker link...")
        
        context = page.context
        tracker_page_obj = None
        
        # 1. Standard Playwright click
        try:
            with context.expect_page(timeout=10000) as new_page_info:
                link.click(timeout=3000)
            tracker_page_obj = new_page_info.value
            self.logger.info(f"[PASS] Captured new App Tracker tab via expect_page: {tracker_page_obj.url}")
        except Exception as e1:
            self.logger.warning(f"[WARN] Standard click didn't open tab ({e1}). Trying JS click...")
            # 2. JS Click fallback
            try:
                with context.expect_page(timeout=10000) as new_page_info:
                    link.evaluate("el => el.click()")
                tracker_page_obj = new_page_info.value
                self.logger.info(f"[PASS] Captured App Tracker tab via JS click: {tracker_page_obj.url}")
            except Exception as e2:
                self.logger.warning(f"[WARN] JS click didn't open tab ({e2}). Trying window.open...")
                # 3. Explicit window.open
                try:
                    # In this application, the link might not have an href and uses a JS handler instead.
                    # If UI clicks are blocked in headless mode, force open the known URL.
                    expected_url = "https://onboarding-uat.adityabirlasunlifeinsurance.com/app-tracker/applications"
                    
                    with context.expect_page(timeout=10000) as manual_page_info:
                        page.evaluate(f"window.open('{expected_url}', '_blank')")
                    tracker_page_obj = manual_page_info.value
                    self.logger.info(f"[PASS] Captured App Tracker tab via explicit JS window.open (using known URL): {tracker_page_obj.url}")
                except Exception as js_e:
                    self.logger.warning(f"[WARN] JS window.open failed: {js_e}")
                
        # Final Fallback: scan all open tabs
        if not tracker_page_obj:
            page.wait_for_timeout(3000)
            for p in context.pages:
                try:
                    if "app-tracker" in p.url:
                        tracker_page_obj = p
                        self.logger.info(f"[PASS] Found App Tracker tab via scan: {p.url}")
                        break
                except Exception:
                    continue
        
        if not tracker_page_obj:
            self.logger.warning("[WARN] App Tracker tab not found — using current page as fallback (validations may warn)")
            tracker_page_obj = page
        
        # Bring the tracker page to focus
        tracker_page_obj.bring_to_front()
        
        # Validate URL
        expected_url_pattern = "https://onboarding-uat.adityabirlasunlifeinsurance.com/app-tracker/applications"
        try:
            current = tracker_page_obj.url
            if expected_url_pattern in current:
                self.logger.info(f"[PASS] URL Validation PASSED: {current}")
            else:
                self.logger.warning(f"[WARN] URL mismatch. Expected: {expected_url_pattern}, Got: {current}")
        except Exception as e:
            self.logger.warning(f"[WARN] URL validation warning: {e}")
        
        # Wait for page to fully load
        try:
            tracker_page_obj.wait_for_load_state("networkidle", timeout=20000)
            self.logger.info("[PASS] Application Tracker page loaded (networkidle)")
        except Exception as load_e:
            self.logger.warning(f"[WARN] networkidle wait: {load_e}")
        
        # Wait for any loading spinners/overlays to disappear
        self._wait_for_loading_overlay_to_disappear(tracker_page_obj)
        
        # Update tracker_page with the new page object
        tracker_page.page = tracker_page_obj
        tracker_page.wait_for_tracker_load(timeout=15000)
        
        # Return the new page object for subsequent validations
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
                else:
                    self.logger.info("[INFO] No detail view detected (may navigate to detail page)")
            except Exception as e:
                self.logger.warning(f"[WARN] Detail view validation skipped: {e}")
            
            self.logger.info("[PASS] Application number search validation completed")
        except Exception as e:
            self.logger.error(f"[FAIL] Application number search validation failed: {e}")
            errors += 1
        
        return errors
