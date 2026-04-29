"""
Configuration management utility - Fixed for Logging Attributes
"""

import os
from dotenv import load_dotenv
import json

class Config:
    """Configuration class for managing test settings"""
    
    # Load environment variables
    load_dotenv()
    
    # --- LOGGING CONFIGURATION ---
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "automation.log")  # <-- ADDED THIS ATTRIBUTE

    # Environment settings
    BASE_URL = os.getenv("BASE_URL", "https://insurance-portal.example.com")
    API_URL = os.getenv("API_URL", "https://api.insurance-portal.example.com")
    
    # Browser Settings
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    BROWSER = os.getenv("BROWSER", "chromium")
    BROWSER_TIMEOUT = int(os.getenv("BROWSER_TIMEOUT", "30000"))
    
    # Viewport Settings
    BROWSER_VIEWPORT = None 
    BROWSER_LAUNCH_ARGS = [
        '--window-size=1280,800',
        '--force-device-scale-factor=1',
        '--disable-blink-features=AutomationControlled'
    ]
    
    # Authentication Settings
    TEST_USERNAME = os.getenv("USERNAME", "testuser")
    TEST_PASSWORD = os.getenv("PASSWORD", "testpass")
    
    # Database Settings
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "5432"))
    
    # Timeouts
    PAGE_LOAD_TIMEOUT = 30000
    ELEMENT_WAIT_TIMEOUT = 10000
    AJAX_WAIT_TIMEOUT = 5000

    @classmethod
    def get_playwright_launch_config(cls):
        """Helper to return consistent launch arguments."""
        return {
            "headless": cls.HEADLESS,
            "args": cls.BROWSER_LAUNCH_ARGS
        }

    @classmethod
    def get_context_config(cls):
        """Helper for Browser Context configuration."""
        return {
            "viewport": cls.BROWSER_VIEWPORT,
            "ignore_https_errors": True
        }