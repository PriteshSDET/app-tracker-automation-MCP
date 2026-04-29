"""
Tracker page locators
"""


class TrackerLocators:
    """Tracker page element locators"""
    
    # Main container
    tracker_container = ".tracker-container"
    
    # Search elements
    search_input = "input[id='search-input']"
    search_button = "button[id='search-button']"
    clear_search_button = "button[id='clear-search']"
    
    # Table elements
    application_table = "table[id='applications-table']"
    application_row = "tbody tr"
    status_column = "td[data-column='status']"
    view_details_button = "button[data-action='view-details']"
    
    # Filter elements
    status_filter = "select[id='status-filter']"
    date_filter = "input[id='date-filter']"
    clear_filters_button = "button[id='clear-filters']"
    
    # Export elements
    export_button = "button[id='export-button']"
    export_option = "button[data-format]"
    
    # Pagination
    pagination_container = ".pagination"
    total_count = ".total-count"
    
    # Status options
    status_option = "option[data-status]"
    
    # Loading states
    loading_overlay = ".loading-overlay"
    no_results_message = ".no-results"
    
    # Details modal
    details_modal = ".details-modal"
    modal_close = ".modal-close"
