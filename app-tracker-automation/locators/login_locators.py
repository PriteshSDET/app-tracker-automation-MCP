"""
Login page locators
"""


class LoginLocators:
    """Login page element locators"""
    
    # Form elements
    login_form = "form[id='login-form']"
    username_input = "input[id='username']"
    password_input = "input[id='password']"
    login_button = "button[type='submit']"
    
    # Error elements
    error_message = ".error-message"
    validation_error = ".validation-error"
    
    # Links
    forgot_password_link = "a[href='/forgot-password']"
    register_link = "a[href='/register']"
    
    # Remember me
    remember_me_checkbox = "input[id='remember-me']"
    
    # Social login
    google_login_button = "button[data-provider='google']"
    facebook_login_button = "button[data-provider='facebook']"
    
    # Loading states
    loading_spinner = ".loading-spinner"
    success_message = ".success-message"
