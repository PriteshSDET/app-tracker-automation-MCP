"""
Constants used throughout the framework
"""

# Test categories
TEST_CATEGORIES = {
    "SANITY": "sanity",
    "SMOKE": "smoke",
    "REGRESSION": "regression",
    "API": "api",
    "INTEGRATION": "integration",
    "PERFORMANCE": "performance",
    "SECURITY": "security"
}

# Test priorities
TEST_PRIORITIES = {
    "CRITICAL": "critical",
    "HIGH": "high",
    "MEDIUM": "medium",
    "LOW": "low"
}

# Application statuses
APPLICATION_STATUSES = {
    "PENDING": "pending",
    "UNDER_REVIEW": "under_review",
    "APPROVED": "approved",
    "REJECTED": "rejected",
    "CANCELLED": "cancelled",
    "COMPLETED": "completed"
}

# Policy types
POLICY_TYPES = {
    "LIFE": "life",
    "HEALTH": "health",
    "AUTO": "auto",
    "HOME": "home",
    "TRAVEL": "travel"
}

# Claim statuses
CLAIM_STATUSES = {
    "SUBMITTED": "submitted",
    "UNDER_INVESTIGATION": "under_investigation",
    "APPROVED": "approved",
    "REJECTED": "rejected",
    "SETTLED": "settled",
    "CLOSED": "closed"
}

# User roles
USER_ROLES = {
    "ADMIN": "admin",
    "AGENT": "agent",
    "UNDERWRITER": "underwriter",
    "CLAIMS_ADJUSTER": "claims_adjuster",
    "CUSTOMER": "customer"
}

# Error messages
ERROR_MESSAGES = {
    "INVALID_LOGIN": "Invalid username or password",
    "SESSION_EXPIRED": "Your session has expired",
    "ACCESS_DENIED": "Access denied",
    "PAGE_NOT_FOUND": "Page not found",
    "SERVER_ERROR": "Internal server error"
}

# Success messages
SUCCESS_MESSAGES = {
    "LOGIN_SUCCESS": "Login successful",
    "LOGOUT_SUCCESS": "Logout successful",
    "POLICY_CREATED": "Policy created successfully",
    "CLAIM_SUBMITTED": "Claim submitted successfully",
    "PROFILE_UPDATED": "Profile updated successfully"
}

# Navigation URLs
URLS = {
    "LOGIN": "/login",
    "DASHBOARD": "/dashboard",
    "POLICIES": "/policies",
    "CLAIMS": "/claims",
    "PROFILE": "/profile",
    "TRACKER": "/tracker",
    "REPORTS": "/reports"
}

# File paths
FILE_PATHS = {
    "SCREENSHOTS": "screenshots",
    "REPORTS": "reports",
    "LOGS": "logs",
    "TEMP": "temp",
    "DOWNLOADS": "temp/downloads"
}

# Timeouts (in milliseconds)
TIMEOUTS = {
    "SHORT": 5000,
    "MEDIUM": 10000,
    "LONG": 30000,
    "EXTRA_LONG": 60000
}

# Browser types
BROWSERS = {
    "CHROMIUM": "chromium",
    "FIREFOX": "firefox",
    "WEBKIT": "webkit"
}

# Environment names
ENVIRONMENTS = {
    "DEV": "dev",
    "STAGING": "staging",
    "PRODUCTION": "production"
}
