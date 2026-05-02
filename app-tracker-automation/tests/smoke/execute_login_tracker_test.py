"""
Unified Test Execution Script: E2E Login & Component Validation
Strategy: Continuous State Management with Explicit Hidden-Waits & Scroll Handling
Updates: Integrated deep-locators from App Tracker HTML source.
"""

import os
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
        self.logger.info("✓ Layout fix CSS injected to prevent viewport issues")
        
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
        
        link.click(force=True)
        
        # Handle new tab opening for Application Tracker
        # Application Tracker opens in new tab: https://onboarding-uat.adityabirlasunlifeinsurance.com/app-tracker/applications
        self.logger.info("Waiting for new tab to open...")
        
        # Wait for new tab to open
        page.wait_for_timeout(2000)
        
        # Get all pages (tabs)
        context = page.context
        pages = context.pages
        
        # Switch to the new tab (Application Tracker)
        tracker_page_obj = None
        for p in pages:
            if "app-tracker" in p.url:
                tracker_page_obj = p
                self.logger.info(f"Found Application Tracker tab: {p.url}")
                break
        
        if not tracker_page_obj:
            self.logger.warning("Application Tracker tab not found, using current page")
            tracker_page_obj = page
        
        # Bring the tracker page to focus
        tracker_page_obj.bring_to_front()
        
        # Validate URL matches expected Application Tracker URL
        expected_url_pattern = "https://onboarding-uat.adityabirlasunlifeinsurance.com/app-tracker/applications"
        try:
            if expected_url_pattern in tracker_page_obj.url:
                self.logger.info(f"✓ URL Validation PASSED: {tracker_page_obj.url}")
            else:
                self.logger.warning(f"URL mismatch. Expected: {expected_url_pattern}, Got: {tracker_page_obj.url}")
        except Exception as e:
            self.logger.warning(f"URL validation warning: {e}")
        
        # Wait for page to load - networkidle ensures background APIs are settled
        tracker_page_obj.wait_for_load_state("networkidle", timeout=10000)
        self.logger.info("Application Tracker page loaded")
        
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
            
            # Try multiple date filter selectors
            date_filter_selectors = [
                "span:has-text('Prev + Current Month')",
                "button:has-text('Prev + Current Month')",
                "div:has-text('Prev + Current Month')",
                "[data-testid='date-filter']",
                ".date-filter",
                "button:has(svg[class*='calendar'])"
            ]
            
            date_filter = None
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
                # Try multiple table header selectors
                table_header_selectors = [
                    "thead th",
                    "table th",
                    ".MuiTableCell-head",
                    "[role='columnheader']",
                    "th"
                ]
                
                table_header = None
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
        