# validated_by_auditor: Stage 2 Auditor
# audit_timestamp: 2026-05-15T15:30:00+05:30
# req_id: STORY-101

import os
import time
from contextlib import contextmanager

import pytest
from dotenv import load_dotenv
from playwright.sync_api import expect, sync_playwright


load_dotenv()


class RecorderSelectors:
    LOGIN_ID = "#loginId"
    PASSWORD = "#password"
    LOGIN_BUTTON = "text/LOGIN"
    USER_MENU = "span.MuiIconButton-label > span > span"
    APPLICATION_TRACKER = "aria/Application Tracker"
    APP_TRACKER_ROOT = "main"
    SEARCH_FIELD_DROPDOWN = "aria/Choose search field"
    SEARCH_INPUT = "input"
    SEARCH_APP_NO = "input"
    SEARCH_POLICY_NO = "input"
    SEARCH_NAME = "input"
    APP_NO_OPTION = "aria/App No."
    POLICY_NO_OPTION = "aria/Policy No.[role=\"button\"]"
    NAME_OPTION = "aria/Name"
    CLEAR_SEARCH = "aria/Clear search"
    FIRST_APP_NO_CELL = "tr:nth-of-type(1) > td.sticky"
    SECOND_PLAN_CELL = "tr:nth-of-type(2) > td:nth-of-type(3)"
    FIRST_STATUS_CELL = "tr:nth-of-type(1) > td:nth-of-type(7) > span > span"
    NON_ROW_CONTAINER = "main > div > div.items-start"
    DRAWER_BODY = "div.p-6"
    DRAWER_HEADER = "aria/[role=\"dialog\"]"
    CLOSE = "aria/Close"
    PAGE_2 = "div:nth-of-type(8) li:nth-of-type(2) > button"
    NEXT_PAGE = "div:nth-of-type(8) button:nth-of-type(2)"
    PREVIOUS_PAGE = "div:nth-of-type(8) button:nth-of-type(1) > span"
    DOWNLOAD_RECORDS = "div.items-start > button"
    STATUS_FILTER = "button.inline-flex > div.shrink-0"
    STATUS_APP_FORM_PENDING = "div.max-h-\\[300px\\] > button:nth-of-type(1) button"
    CLEAR_ALL_FILTERS = "div.border-t > button"


TEST_DATA = {
    "valid_app_no": os.getenv("VALID_APP_NO", "LA53544182"),
    "valid_policy_no": os.getenv("VALID_POLICY_NO", ""),
    "valid_proposer_name": os.getenv("VALID_PROPOSER_NAME", "Utpal Mal Utpal"),
    "invalid_app_no": os.getenv("INVALID_APP_NO", "ZZZ00000000"),
    "malformed_search": os.getenv("MALFORMED_SEARCH", "<script>alert(1)</script>"),
}


class BasePage:
    def __init__(self, page):
        self.page = page

    def navigate_to(self, url):
        self.page.goto(url, wait_until="domcontentloaded")

    def wait_for_page_load(self):
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_load_state("networkidle", timeout=30000)

    def click_element(self, locator):
        self._locator(locator).click(timeout=30000)

    def input_text(self, locator, text):
        target = self._locator(locator)
        target.fill("")
        target.fill(text)

    def select_dropdown_by_value(self, locator, value):
        self.click_element(locator)
        self.click_element(value)

    def verify_element_visible(self, locator):
        expect(self._locator(locator)).to_be_visible(timeout=30000)

    def assert_text_presence(self, text):
        locator = self.page.get_by_text(text, exact=False)
        self.page.wait_for_timeout(500)
        for index in range(locator.count()):
            if locator.nth(index).is_visible(timeout=1000):
                return
        expect(locator.first).to_be_visible(timeout=30000)

    def soft_verify_value(self, locator, expected_value):
        expect(self._locator(locator)).to_contain_text(expected_value, timeout=30000)

    def take_screenshot(self, name):
        self.page.screenshot(path=f"rag/active/execution_logs/{name}.png", full_page=True)

    def switch_to_new_tab(self):
        if len(self.page.context.pages) > 1:
            self.page = self.page.context.pages[-1]
            self.page.bring_to_front()

    def _locator(self, recorder_selector):
        if recorder_selector.startswith("aria/"):
            return self._aria_locator(recorder_selector[5:])
        if recorder_selector.startswith("text/"):
            return self.page.get_by_text(recorder_selector[5:], exact=True)
        if recorder_selector.startswith("xpath/"):
            return self.page.locator(recorder_selector)
        if recorder_selector.startswith("pierce/"):
            return self.page.locator(recorder_selector[7:])
        return self.page.locator(recorder_selector)

    def _aria_locator(self, aria_selector):
        if "[role=\"button\"]" in aria_selector:
            name = aria_selector.replace("[role=\"button\"]", "")
            return self.page.get_by_role("button", name=name, exact=True)
        if "[role=\"dialog\"]" in aria_selector:
            return self.page.get_by_role("dialog")
        if "[role=\"image\"]" in aria_selector or "[role=\"graphics-symbol\"]" in aria_selector:
            return self.page.get_by_label("Close").or_(self.page.get_by_role("button", name="Close"))
        return self.page.get_by_text(aria_selector, exact=True).or_(
            self.page.get_by_label(aria_selector, exact=True)
        ).first


class AppTrackerActions:
    def __init__(self, page):
        self.page = page
        self.base = BasePage(page)

    def login_to_leap(self, user_env="TEST_USER_DS_FADV_LOGIN", pass_env="TEST_USER_DS_FADV_PASSWORD"):
        user = os.getenv(user_env) or os.getenv("TEST_USER_ID")
        password = os.getenv(pass_env) or os.getenv("TEST_PASSWORD")
        if not user or not password:
            pytest.skip(f"Missing credentials: {user_env}/{pass_env}")
        self.base.navigate_to(os.getenv("BASE_URL") or os.getenv("TARGET_URL"))
        self.base.input_text(RecorderSelectors.LOGIN_ID, user)
        self.base.input_text(RecorderSelectors.PASSWORD, password)
        self.base.click_element(RecorderSelectors.LOGIN_BUTTON)
        self.base.wait_for_page_load()

    def open_app_tracker_from_menu(self):
        self.base.click_element(RecorderSelectors.USER_MENU)
        with self.page.context.expect_page(timeout=15000) as new_page_info:
            self.base.click_element(RecorderSelectors.APPLICATION_TRACKER)
        self.page = new_page_info.value
        self.page.wait_for_load_state("domcontentloaded", timeout=30000)
        self.base.page = self.page
        self.base.wait_for_page_load()

    def open_app_tracker_direct(self):
        url = os.getenv("APP_TRACKER_URL") or os.getenv("TARGET_URL")
        self.base.navigate_to(url)
        self.base.wait_for_page_load()

    def go_to_tracker_as(self, user_env="TEST_USER_DS_FADV_LOGIN", pass_env="TEST_USER_DS_FADV_PASSWORD"):
        self.login_to_leap(user_env, pass_env)
        self.open_app_tracker_from_menu()

    def assert_dashboard_loaded(self):
        self.base.verify_element_visible(RecorderSelectors.APP_TRACKER_ROOT)

    def search_app_no(self, app_no=None):
        self.base.input_text(RecorderSelectors.SEARCH_APP_NO, app_no or TEST_DATA["valid_app_no"])

    def search_policy_no(self, policy_no=None):
        policy_no = policy_no or TEST_DATA["valid_policy_no"]
        if not policy_no:
            pytest.skip("Missing VALID_POLICY_NO synthetic data")
        self.base.select_dropdown_by_value(
            RecorderSelectors.SEARCH_FIELD_DROPDOWN,
            RecorderSelectors.POLICY_NO_OPTION,
        )
        self.base.input_text(RecorderSelectors.SEARCH_POLICY_NO, policy_no)

    def search_name(self, proposer_name=None):
        self.base.select_dropdown_by_value(
            RecorderSelectors.SEARCH_FIELD_DROPDOWN,
            RecorderSelectors.NAME_OPTION,
        )
        self.base.input_text(
            RecorderSelectors.SEARCH_NAME,
            proposer_name or TEST_DATA["valid_proposer_name"],
        )

    def clear_search(self):
        self.base.click_element(RecorderSelectors.CLEAR_SEARCH)

    def assert_search_under_threshold(self, action, p95_ms=1000):
        start = time.perf_counter()
        action()
        self.page.wait_for_load_state("networkidle", timeout=30000)
        elapsed_ms = (time.perf_counter() - start) * 1000
        assert elapsed_ms <= p95_ms, f"Search exceeded threshold: {elapsed_ms:.2f} ms"

    def open_first_policy_drawer(self):
        self.base.click_element(RecorderSelectors.FIRST_APP_NO_CELL)
        self.base.verify_element_visible(RecorderSelectors.DRAWER_BODY)

    def close_drawer(self):
        self.base.click_element(RecorderSelectors.CLOSE)

    def next_and_previous_page(self):
        self.base.click_element(RecorderSelectors.NEXT_PAGE)
        self.base.wait_for_page_load()
        self.base.click_element(RecorderSelectors.PREVIOUS_PAGE)
        self.base.wait_for_page_load()

    def assert_texts_visible(self, *texts):
        for text in texts:
            self.base.assert_text_presence(text)

    def assert_table_columns(self):
        self.assert_texts_visible("App. No.", "Proposer Name", "Plan Name", "Modal Premium", "Policy Status")

    def first_app_no(self):
        return self.page.locator(RecorderSelectors.FIRST_APP_NO_CELL).inner_text(timeout=10000).strip()

    def first_proposer_name(self):
        return self.page.locator("tr:nth-of-type(1) > td:nth-of-type(2)").inner_text(timeout=10000).strip()

    def apply_status_filter(self):
        self.base.click_element(RecorderSelectors.STATUS_FILTER)
        self.base.verify_element_visible(RecorderSelectors.CLEAR_ALL_FILTERS)
        self.base.click_element(RecorderSelectors.STATUS_APP_FORM_PENDING)

    def clear_status_filter(self):
        self.base.click_element(RecorderSelectors.STATUS_FILTER)
        self.page.wait_for_timeout(500)
        self.page.locator(RecorderSelectors.CLEAR_ALL_FILTERS).click(timeout=30000, force=True)

    def assert_no_script_injection(self):
        assert "alert(1)" not in self.page.content()

    def assert_browser_back_controlled(self):
        before = self.page.url
        self.page.go_back(wait_until="domcontentloaded")
        assert self.page.url == before or "app-tracker" in self.page.url

    def skip_missing_rag_selector(self, capability):
        pytest.skip(f"Missing Chrome Recorder selector/data for {capability}; do not invent locators.")

    def assert_application_tracker_entry_absent(self):
        assert self.page.get_by_text("Application Tracker", exact=True).count() == 0

    def assert_drawer_absent(self):
        assert self.page.get_by_role("dialog").count() == 0


@contextmanager
def launched_page():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=os.getenv("HEADLESS", "true").lower() == "true"
        )
        context = browser.new_context()
        page = context.new_page()
        try:
            yield page
        finally:
            context.close()
            browser.close()


def restricted_role_matrix():
    return [
        ("TEST_USER_SP_RESTRICTED_LOGIN", "TEST_USER_SP_RESTRICTED_PASSWORD"),
        ("TEST_USER_TPD_RESTRICTED_LOGIN", "TEST_USER_TPD_RESTRICTED_PASSWORD"),
        ("TEST_USER_BANCA_RESTRICTED_LOGIN", "TEST_USER_BANCA_RESTRICTED_PASSWORD"),
        ("TEST_USER_HDFC_RESTRICTED_LOGIN", "TEST_USER_HDFC_RESTRICTED_PASSWORD"),
        ("TEST_USER_AXIS_RESTRICTED_LOGIN", "TEST_USER_AXIS_RESTRICTED_PASSWORD"),
    ]
