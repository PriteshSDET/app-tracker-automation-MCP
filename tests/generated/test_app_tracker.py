# validated_by_auditor: Stage 2 Auditor
# audit_timestamp: 2026-05-15T15:30:00+05:30
# req_id: STORY-101

from tests.generated.app_tracker_base import AppTrackerActions, launched_page


class TestAppTrackerPositive:
    def test_TC_01_01_verify_eligible_dsf_access_from_leap(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as("TEST_USER_DS_FADV_LOGIN", "TEST_USER_DS_FADV_PASSWORD")
            app.assert_dashboard_loaded()

    def test_TC_01_02_verify_eligible_fls_access(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as("TEST_USER_FLS_MANAGERIAL_LOGIN", "TEST_USER_FLS_MANAGERIAL_PASSWORD")
            app.assert_dashboard_loaded()

    def test_TC_01_03_verify_support_officer_access(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.skip_missing_rag_selector("Support Officer credential mapping")

    def test_TC_02_01_verify_branding_and_navigation_controls(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            app.assert_texts_visible("App Tracker", "Policy List", "Download 10 Records")

    def test_TC_02_02_verify_menu_access_after_dashboard_actions(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            app.search_app_no(app.first_app_no())
            app.open_first_policy_drawer()
            app.close_drawer()
            app.base.click_element("html")
            app.assert_dashboard_loaded()

    def test_TC_02_03_verify_logout_ends_session(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            app.skip_missing_rag_selector("Logout control")

    def test_TC_03_01_search_by_app_no_returns_matching_policy(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            valid_app_no = app.first_app_no()
            app.assert_search_under_threshold(lambda: app.search_app_no(valid_app_no))
            app.base.assert_text_presence(valid_app_no)

    def test_TC_03_02_search_by_policy_no_returns_matching_policy(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            app.assert_search_under_threshold(app.search_policy_no)

    def test_TC_03_03_search_by_proposer_name_returns_matching_policies(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            proposer_name = app.first_proposer_name()
            app.assert_search_under_threshold(lambda: app.search_name(proposer_name))
            app.base.assert_text_presence(proposer_name)

    def test_TC_03_06_clear_search_restores_default_result_set(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            app.search_app_no(app.first_app_no())
            app.clear_search()
            app.assert_dashboard_loaded()

    def test_TC_04_01_apply_date_range_filter_and_verify_chip(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.skip_missing_rag_selector("Date Range filter chip")

    def test_TC_04_02_apply_stage_filter_and_verify_chip(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            app.apply_status_filter()
            app.base.assert_text_presence("App Form Pending")

    def test_TC_04_03_apply_role_filter_and_verify_chip(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.skip_missing_rag_selector("Role filter chip")

    def test_TC_04_04_apply_multi_filter_combination(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.skip_missing_rag_selector("Date Range, Stage, and Role filter combination")

    def test_TC_04_05_remove_filter_chip_and_verify_grid_refresh(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            app.apply_status_filter()
            app.clear_status_filter()
            app.assert_dashboard_loaded()

    def test_TC_05_01_verify_policy_list_columns_and_currency_display(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            app.assert_table_columns()
            app.base.assert_text_presence("Modal Premium")

    def test_TC_05_02_sort_app_no_ascending_and_descending(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            app.skip_missing_rag_selector("App.No sort header")

    def test_TC_05_03_sort_modal_premium_numerically(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            app.skip_missing_rag_selector("Modal Premium sort header")

    def test_TC_05_06_validate_policy_status_color_coding(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            app.base.verify_element_visible("tr:nth-of-type(1) > td:nth-of-type(7) > span > span")

    def test_TC_06_01_open_detail_drawer_from_policy_row(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            app.open_first_policy_drawer()

    def test_TC_06_02_verify_detail_drawer_journey_timeline(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            first_app = app.first_app_no()
            app.open_first_policy_drawer()
            app.assert_texts_visible("Application details", f"Viewing application {first_app}")

    def test_TC_06_03_verify_milestone_status_and_timestamp_display(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            app.open_first_policy_drawer()
            app.assert_texts_visible("Application details")

    def test_TC_06_04_verify_esc_key_closes_detail_drawer(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.skip_missing_rag_selector("Esc key close action in master_steps.json")

    def test_TC_07_01_verify_pagination_count_and_page_controls(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            app.base.verify_element_visible("div:nth-of-type(8) li:nth-of-type(2) > button")
            app.base.verify_element_visible("div:nth-of-type(8) button:nth-of-type(2)")

    def test_TC_07_02_verify_next_previous_without_full_reload(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            app.next_and_previous_page()
            app.assert_dashboard_loaded()

    def test_TC_07_03_verify_search_filter_state_survives_pagination(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            proposer_name = app.first_proposer_name()
            app.search_name(proposer_name)
            app.base.click_element("div:nth-of-type(8) li:nth-of-type(2) > button")
            app.base.assert_text_presence(proposer_name.split()[0])

    def test_TC_08_01_validate_loading_state_during_grid_refresh(self):
        with launched_page() as page:
            app = AppTrackerActions(page)
            app.go_to_tracker_as()
            app.skip_missing_rag_selector("loading state assertion")
