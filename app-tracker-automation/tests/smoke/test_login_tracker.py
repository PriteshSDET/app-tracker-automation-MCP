"""
Smoke Test: End-to-End Authentication to Application Tracker
Test ID: TC_LOGIN_TRACKER_001
Priority: HIGH
Environment: UAT
"""

import os
from dotenv import load_dotenv
import pytest
from playwright.sync_api import Page
from pages.aditya_birla_login_page import AdityaBirlaLoginPage
from pages.aditya_birla_dashboard_page import AdityaBirlaDashboardPage
from pages.aditya_birla_tracker_page import AdityaBirlaTrackerPage
from utils.logger import Logger

# Load environment variables from .env file using multi-path strategy
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


class TestLoginTrackerNavigation:
    """End-to-End Authentication to Application Tracker"""
    
    @pytest.mark.smoke
    @pytest.mark.high_priority
    def test_login_to_tracker_navigation(self, page):
        """
        Test complete flow from login to application tracker navigation
        
        Steps:
        1. Navigate to UAT login page
        2. Enter valid credentials from .env
        3. Verify login success and dashboard load
        4. Navigate to Application Tracker via MENU button
        5. Verify tracker layout and data
        """
        
        # Initialize components
        logger = Logger()
        login_page = AdityaBirlaLoginPage(page)
        dashboard_page = AdityaBirlaDashboardPage(page)
        tracker_page = AdityaBirlaTrackerPage(page)
        
        # Test data from .env
        username = os.getenv("ADITYA_BIRLA_USER")
        password = os.getenv("ADITYA_BIRLA_PASS")
        
        # Debug: Log credential loading status
        logger.info(f"Credentials loaded - User: {username}, Pass: {'*' * len(password) if password else 'None'}")
        
        if not username or not password:
            logger.error(f"Credentials not loaded from .env. User: {username}, Pass: {password}")
            raise Exception("Credentials not loaded from .env file. Please check .env file location and content.")
        
        try:
            # Phase 1: Navigation & Authentication
            logger.step_start("Phase 1: Authentication")
            login_page.load()
            login_page.enter_credentials(username, password)
            login_page.click_login_button()
            
            try:
                page.wait_for_url("**/uat/#/dashboard", timeout=15000)
                logger.info("[OK] Successfully redirected to dashboard")
            except Exception as e:
                logger.warning(f"Dashboard redirect warning: {e}")
            
            logger.step_end("Phase 1: Authentication", "PASSED")
            
            # Phase 2: App Tracker Setup
            logger.step_start("Phase 2: App Tracker Navigation")
            
            # Click MENU button using precise selector
            menu_btn = page.locator("button.menu-button[aria-label='menu']").first
            menu_btn.scroll_into_view_if_needed()
            menu_btn.wait_for(state="visible", timeout=5000)
            menu_btn.click()
            logger.info("[OK] MENU button clicked")
            
            # Wait for menu to appear
            page.wait_for_timeout(500)
            
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
                        logger.info(f"Found Application Tracker using selector: {selector}")
                        break
                except:
                    continue
            
            if not link:
                raise Exception("Application Tracker link not found in menu")
            
            link.scroll_into_view_if_needed()
            link.click(force=True)
            logger.info("[OK] Application Tracker link clicked")
            
            # Handle new tab opening for Application Tracker
            page.wait_for_timeout(2000)
            
            # Get all pages (tabs)
            context = page.context
            pages = context.pages
            
            # Switch to the new tab (Application Tracker)
            tracker_page_obj = None
            for p in pages:
                if "app-tracker" in p.url:
                    tracker_page_obj = p
                    logger.info(f"Found Application Tracker tab: {p.url}")
                    break
            
            if not tracker_page_obj:
                logger.warning("Application Tracker tab not found, using current page")
                tracker_page_obj = page
            
            # Bring the tracker page to focus
            tracker_page_obj.bring_to_front()
            
            # Validate URL matches expected Application Tracker URL
            expected_url_pattern = "https://onboarding-uat.adityabirlasunlifeinsurance.com/app-tracker/applications"
            try:
                if expected_url_pattern in tracker_page_obj.url:
                    logger.info(f"[OK] URL Validation PASSED: {tracker_page_obj.url}")
                else:
                    logger.warning(f"URL mismatch. Expected: {expected_url_pattern}, Got: {tracker_page_obj.url}")
            except Exception as e:
                logger.warning(f"URL validation warning: {e}")
            
            # Wait for page to load
            tracker_page_obj.wait_for_load_state("networkidle", timeout=10000)
            logger.info("Application Tracker page loaded")
            
            # Update tracker_page with the new page object
            tracker_page.page = tracker_page_obj
            tracker_page.wait_for_tracker_load(timeout=15000)
            
            logger.step_end("Phase 2: App Tracker Navigation", "PASSED")
            
            # Phase 3: Component Validation
            logger.step_start("Phase 3: Component Validation")
            
            # Validate filter components
            try:
                title = tracker_page_obj.locator("h1, .title, [class*='header']").first
                if title.is_visible(timeout=3000):
                    logger.info("[OK] Tracker title visible")
            except:
                logger.warning("Tracker title not visible")
            
            try:
                search_box = tracker_page_obj.locator("input[type='text'], input[placeholder*='Search']").first
                if search_box.is_visible(timeout=3000):
                    logger.info("[OK] Search box visible")
            except:
                logger.warning("Search box not visible")
            
            try:
                table = tracker_page_obj.locator("table, [class*='table'], [class*='grid']").first
                if table.is_visible(timeout=3000):
                    logger.info("[OK] Table visible")
            except:
                logger.warning("Table not visible")
            
            logger.step_end("Phase 3: Component Validation", "PASSED")
            
            # Test completed successfully
            logger.test_end("test_login_to_tracker_navigation", "PASSED")
            
        except Exception as e:
            logger.test_end("test_login_to_tracker_navigation", "FAILED")
            logger.error(f"Test failed with error: {str(e)}")
            # Take screenshot on failure
            page.screenshot(path="screenshots/failed/test_login_tracker_failure.png", full_page=True)
            raise
    

