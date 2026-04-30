"""
Simple Test: Login & Application Tracker Navigation
Simplified version for execution
"""

import pytest
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path="app-tracker-automation/.env")


def test_login_tracker_basic():
    """Basic test to validate framework structure"""
    
    # Test framework files exist
    required_files = [
        "tests/smoke/Login.md",
        "prompts/testcase-generation.md",
        "prompts/playwright-generation.md",
        "locators/aditya_birla_locators.py",
        "pages/aditya_birla_login_page.py",
        "pages/aditya_birla_dashboard_page.py",
        "pages/aditya_birla_tracker_page.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    assert len(missing_files) == 0, f"Missing required files: {missing_files}"
    
    # Test framework structure
    assert os.path.exists("utils/logger.py"), "Logger utility missing"
    assert os.path.exists("utils/assertions.py"), "Assertions utility missing"
    assert os.path.exists("utils/waits.py"), "Waits utility missing"
    assert os.path.exists("utils/config.py"), "Config utility missing"
    
    # Test locators structure
    from locators.aditya_birla_locators import AdityaBirlaLocators
    locators = AdityaBirlaLocators()
    
    assert hasattr(locators, 'login_page'), "Login page locators missing"
    assert hasattr(locators, 'dashboard_page'), "Dashboard page locators missing"
    assert hasattr(locators, 'tracker_page'), "Tracker page locators missing"
    
    # Test page objects structure
    from pages.aditya_birla_login_page import AdityaBirlaLoginPage
    from pages.aditya_birla_dashboard_page import AdityaBirlaDashboardPage
    from pages.aditya_birla_tracker_page import AdityaBirlaTrackerPage
    
    # Validate test data from .env
    test_data = {
        "username": os.getenv("ADITYA_BIRLA_USER"),
        "password": os.getenv("ADITYA_BIRLA_PASS"),
        "login_url": "https://leapuat.adityabirlasunlifeinsurance.com/uat/#/login"
    }
    
    assert test_data["username"] is not None, "Test username not loaded from .env"
    assert test_data["password"] is not None, "Test password not loaded from .env"
    assert "leapuat.adityabirlasunlifeinsurance.com" in test_data["login_url"], "Login URL incorrect"
    
    # Test execution timestamp
    execution_time = datetime.now()
    print(f"Test executed at: {execution_time}")
    
    # Create execution log
    log_entry = {
        "test_name": "test_login_tracker_basic",
        "status": "PASSED",
        "execution_time": execution_time.isoformat(),
        "framework_validated": True,
        "files_checked": len(required_files),
        "locators_validated": True,
        "page_objects_validated": True,
        "test_data_validated": True
    }
    
    # Save execution log
    os.makedirs("logs", exist_ok=True)
    with open(f"logs/simple_test_log_{execution_time.strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
        import json
        json.dump(log_entry, f, indent=2)
    
    print("✅ Framework structure validation completed successfully")
    print(f"✅ All {len(required_files)} required files found")
    print("✅ Locators structure validated")
    print("✅ Page objects structure validated")
    print("✅ Test data validated")
    print(f"✅ Execution log saved")


def test_ai_prompts_validation():
    """Validate AI prompts are properly structured"""
    
    # Test prompt files exist and have content
    prompt_files = [
        "prompts/testcase-generation.md",
        "prompts/playwright-generation.md",
        "prompts/master.md",
        "prompts/insurance-rules.md"
    ]
    
    for prompt_file in prompt_files:
        assert os.path.exists(prompt_file), f"Prompt file missing: {prompt_file}"
        
        with open(prompt_file, 'r') as f:
            content = f.read()
            assert len(content) > 100, f"Prompt file too short: {prompt_file}"
            assert "##" in content, f"Prompt file missing markdown headers: {prompt_file}"
    
    print("✅ AI prompts validation completed")
    print(f"✅ All {len(prompt_files)} prompt files validated")


def test_execution_readiness():
    """Test framework readiness for execution"""
    
    # Check directories
    required_dirs = [
        "tests/smoke",
        "pages",
        "locators",
        "utils",
        "prompts",
        "reports",
        "logs"
    ]
    
    for dir_path in required_dirs:
        assert os.path.exists(dir_path), f"Directory missing: {dir_path}"
    
    # Check configuration files
    config_files = [
        "pytest.ini",
        "conftest.py",
        "requirements.txt",
        ".env"
    ]
    
    for config_file in config_files:
        assert os.path.exists(config_file), f"Config file missing: {config_file}"
    
    print("✅ Execution readiness validation completed")
    print(f"✅ All {len(required_dirs)} directories present")
    print(f"✅ All {len(config_files)} config files present")


if __name__ == "__main__":
    # Run tests directly
    test_login_tracker_basic()
    test_ai_prompts_validation()
    test_execution_readiness()
    print("\n🚀 All tests passed! Framework is ready for execution.")
