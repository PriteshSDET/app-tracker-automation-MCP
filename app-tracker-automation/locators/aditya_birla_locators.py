"""
Aditya Birla Sun Life Insurance Portal Locators
UAT Environment Specific Locators
"""


class AdityaBirlaLocators:
    """Aditya Birla Sun Life Insurance portal element locators"""
    
    # Login Page
    login_page = {
        "url": "https://leapuat.adityabirlasunlifeinsurance.com/uat/#/login",
        "login_form": "form",
        "username_input": "input[type='text'], input[name='username'], input[id*='login'], input[placeholder*='Login']",
        "password_input": "input[type='password'], input[name='password']",
        "login_button": "button[type='submit'], button:has-text('LOGIN'), button:has-text('Login')",
        "uat_badge": "[class*='uat'], [data-env='uat'], .uat-badge",
        "error_message": ".error, .alert, [class*='error'], [class*='invalid']",
        "branding_header": "header, .header, [class*='branding']"
    }
    
    # Dashboard Page
    dashboard_page = {
        "url": "https://leapuat.adityabirlasunlifeinsurance.com/uat/#/dashboard",
        "header": "h1, .header, [class*='application']",
        "application_list_title": "h1:has-text('Application List'), .title:has-text('Application List')",
        "toolbar": "[class*='toolbar'], [class*='filter']",
        "filter_button": "[class*='filter'], button:has-text('Filter')",
        "sort_button": "[class*='sort'], button:has-text('Sort')",
        "data_table": "table, [class*='grid'], [class*='list']",
        "data_rows": "tbody tr, [class*='row'], tr",
        "pending_dots": "[class*='pending'], [class*='orange'], [status*='pending']",
        "new_application_button": "button:has-text('NEW APPLICATION'), button:has-text('+ NEW')",
        "menu_button": "button:has-text('MENU'), [class*='menu'], .dropdown-toggle",
        "uat_badge": "[class*='uat'], [data-env='uat'], .uat-badge"
    }
    
    # Menu Navigation
    navigation_menu = {
        "menu_dropdown": ".dropdown, [class*='dropdown']",
        "help_item": "a:has-text('Help'), [role='menuitem']:has-text('Help')",
        "application_tracker_item": "a:has-text('Application Tracker'), [role='menuitem']:has-text('Application Tracker')",
        "approvals_item": "a:has-text('Approvals'), [role='menuitem']:has-text('Approvals')",
        "logout_item": "a:has-text('Logout'), [role='menuitem']:has-text('Logout')"
    }
    
    # Application Tracker Page
    tracker_page = {
        "url": "https://onboarding-uat.adityabirlasunlifeinsurance.com/app-tracker/applications",
        "header": "h1, .title, [class*='header']",
        "policy_list_title": "h1:has-text('Policy List'), .title:has-text('Policy List')",
        "refresh_info": "[class*='meta'], [class*='info']:has-text('refreshes every 15 minutes')",
        "filter_chips": "[class*='filter'], [class*='chip']",
        "search_bar": "[class*='search'], input[type='search']",
        "date_range_picker": "[class*='date'], [class*='picker'], input[type='date']",
        "data_table": "table, [class*='table'], [class*='grid']",
        "table_headers": "th, [class*='header'], [class*='column']",
        "table_rows": "tbody tr, [class*='row'], tr",
        "uat_badge": "[class*='uat'], [data-env='uat'], .uat-badge"
    }
    
    # Table Columns (Application Tracker)
    table_columns = {
        "app_no": "th:has-text('App.No'), [class*='header']:has-text('App.No')",
        "proposer_name": "th:has-text('Proposer Name'), [class*='header']:has-text('Proposer Name')",
        "plan_name": "th:has-text('Plan Name'), [class*='header']:has-text('Plan Name')",
        "modal_premium": "th:has-text('Modal Premium'), [class*='header']:has-text('Modal Premium')",
        "policy_status": "th:has-text('Policy Status'), [class*='header']:has-text('Policy Status')"
    }
    
    # Common Elements
    common = {
        "loading_spinner": ".loading, [class*='spinner'], [class*='loading']",
        "error_toast": ".toast, .alert, [class*='error'], [class*='toast']",
        "success_message": ".success, [class*='success'], [class*='toast-success']",
        "page_content": "main, .content, [class*='main']",
        "footer": "footer, .footer"
    }
    
    # Accessibility Elements
    accessibility = {
        "focus_elements": "input, button, a, select, textarea",
        "focus_visible": ":focus, [class*='focus']",
        "aria_labels": "[aria-label], [aria-labelledby]",
        "skip_links": ".skip-link, a[href='#main']"
    }
    
    # Dynamic Elements (may need waits)
    dynamic = {
        "ajax_content": "[class*='ajax'], [data-ajax]",
        "lazy_loaded": "[data-lazy], [class*='lazy']",
        "conditional_elements": "[class*='conditional'], [data-conditional]"
    }
