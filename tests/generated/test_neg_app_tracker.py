# validated_by_auditor: Stage 2 Auditor
# audit_timestamp: 2026-05-15T15:30:00+05:30
# req_id: STORY-101

from tests.generated.app_tracker_base import (
    AppTrackerActions,
    RecorderSelectors,
    launched_page,
    restricted_role_matrix,
)


class TestAppTrackerNegative:
    def test_TC_01_04_verify_restricted_sp_user_cannot_access_tracker(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.login_to_leap("TEST_USER_SP_RESTRICTED_LOGIN", "TEST_USER_SP_RESTRICTED_PASSWORD")
            app.base.click_element(RecorderSelectors.USER_MENU)
            app.assert_application_tracker_entry_absent()

    def test_TC_01_05_verify_restricted_partner_roles_cannot_access_tracker(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            for user_env, pass_env in restricted_role_matrix():
                app.login_to_leap(user_env, pass_env)
                app.base.click_element(RecorderSelectors.USER_MENU)
                app.assert_application_tracker_entry_absent()

    def test_TC_03_04_search_no_matching_app_no_shows_empty_state(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            app.search_app_no(app_no="ZZZ00000000")
            app.base.assert_text_presence("No")

    def test_TC_03_05_search_malformed_value_is_safely_handled(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            app.search_app_no("<script>alert(1)</script>")
            app.assert_no_script_injection()

    def test_TC_04_06_invalid_filter_combination_shows_empty_state(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            app.apply_status_filter()
            app.search_app_no("ZZZ00000000")
            app.base.assert_text_presence("No")

    def test_TC_05_04_validate_premium_anomaly_handling(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.skip_missing_rag_selector("premium anomaly data injection")

    def test_TC_05_05_validate_duplicate_app_no_handling(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.skip_missing_rag_selector("duplicate App No. synthetic dataset")

    def test_TC_06_05_verify_non_row_elements_do_not_open_drawer(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            app.base.click_element(RecorderSelectors.NON_ROW_CONTAINER)
            app.assert_drawer_absent()

    def test_TC_07_04_verify_browser_back_disabled_after_leap_redirection(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            app.assert_browser_back_controlled()

    def test_TC_08_02_validate_api_service_failure_handling(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.skip_missing_rag_selector("API/service failure simulation")

    def test_TC_08_03_validate_stale_session_or_token_expiry_handling(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.skip_missing_rag_selector("stale session or token expiry setup")

    def test_TC_08_04_validate_permission_denial_after_role_change(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.skip_missing_rag_selector("permission revocation setup")
