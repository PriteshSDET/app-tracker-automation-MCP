"""
Logger utility for test execution logging
"""

import logging
import os
from datetime import datetime
from utils.config import Config


class Logger:
    """Custom logger class for test execution"""
    
    def __init__(self, name: str = None):
        """Initialize logger with configuration"""
        self.logger = logging.getLogger(name or __name__)
        
        # Avoid multiple handlers
        if not self.logger.handlers:
            self._setup_logger()
    
    def _setup_logger(self):
        """Setup logger configuration"""
        # Set log level
        level = getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)
        self.logger.setLevel(level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler
        if Config.LOG_FILE:
            # Create logs directory if it doesn't exist
            log_dir = os.path.dirname(Config.LOG_FILE)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            file_handler = logging.FileHandler(Config.LOG_FILE)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log critical message"""
        self.logger.critical(message)
    
    def test_start(self, test_name: str):
        """Log test start"""
        self.info(f"=== TEST START: {test_name} ===")
    
    def test_end(self, test_name: str, status: str):
        """Log test end"""
        self.info(f"=== TEST END: {test_name} - {status} ===")
    
    def step_start(self, step_name: str):
        """Log step start"""
        self.info(f"--- STEP START: {step_name} ---")
    
    def step_end(self, step_name: str, status: str):
        """Log step end"""
        self.info(f"--- STEP END: {step_name} - {status} ---")
    
    def screenshot(self, description: str, path: str):
        """Log screenshot taken"""
        self.info(f"SCREENSHOT: {description} -> {path}")
    
    def action(self, action: str, element: str = None):
        """Log user action"""
        if element:
            self.info(f"ACTION: {action} on {element}")
        else:
            self.info(f"ACTION: {action}")
    
    def validation(self, expected: str, actual: str, result: str):
        """Log validation result"""
        self.info(f"VALIDATION: Expected '{expected}', Actual '{actual}' -> {result}")


class TestLogger:
    """Test-specific logger with additional context"""
    
    def __init__(self, test_name: str):
        self.test_name = test_name
        self.logger = Logger(f"test.{test_name}")
        self.start_time = None
    
    def start_test(self):
        """Start test logging"""
        self.start_time = datetime.now()
        self.logger.test_start(self.test_name)
    
    def end_test(self, status: str = "PASSED"):
        """End test logging"""
        if self.start_time:
            duration = datetime.now() - self.start_time
            self.logger.info(f"TEST DURATION: {duration.total_seconds():.2f} seconds")
        self.logger.test_end(self.test_name, status)
    
    def log_step(self, step_name: str, status: str = "PASSED"):
        """Log test step"""
        self.logger.step_start(step_name)
        self.logger.step_end(step_name, status)

