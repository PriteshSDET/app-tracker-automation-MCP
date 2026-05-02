"""
Shared locators used across multiple pages
"""


class SharedLocators:
    """Shared element locators"""
    
    # Navigation
    main_navigation = ".main-navigation"
    dashboard_link = "a[href='/dashboard']"
    policies_link = "a[href='/policies']"
    claims_link = "a[href='/claims']"
    profile_link = "a[href='/profile']"
    logout_button = "button[id='logout']"
    
    # Dashboard elements
    dashboard_container = ".dashboard-container"
    welcome_message = ".welcome-message"
    active_policies_count = ".active-policies-count"
    pending_claims_count = ".pending-claims-count"
    
    # Common elements
    header = "header"
    footer = "footer"
    main_content = "main"
    
    # User menu
    user_menu = ".user-menu"
    user_menu_toggle = ".user-menu-toggle"
    
    # Notifications
    notification_bell = ".notification-bell"
    notification_dropdown = ".notification-dropdown"
    
    # Search
    global_search = ".global-search"
    global_search_input = ".global-search input"
    
    # Loading states
    page_loader = ".page-loader"
    content_loader = ".content-loader"
    
    # Error states
    error_page = ".error-page"
    error_message = ".error-message"
    
    # Success states
    success_message = ".success-message"
    
    # Modals
    modal_overlay = ".modal-overlay"
    modal_container = ".modal-container"
    
    # Forms
    form_container = ".form-container"
    submit_button = "button[type='submit']"
    cancel_button = "button[type='button']"
    
    # Tables
    table_container = ".table-container"
    table_header = ".table-header"
    table_body = ".table-body"
    
    # Common buttons
    add_button = ".add-button"
    edit_button = ".edit-button"
    delete_button = ".delete-button"
    save_button = ".save-button"
    
    # Breadcrumbs
    breadcrumbs = ".breadcrumbs"
    breadcrumb_item = ".breadcrumb-item"

