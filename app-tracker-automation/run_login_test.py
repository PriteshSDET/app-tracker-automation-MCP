"""
Test Runner Script: Execute Login & Tracker Test
Uses framework prompts and comprehensive logging
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from utils.logger import Logger


def setup_environment():
    """Setup test environment"""
    logger = Logger()
    
    logger.info("=== TEST EXECUTION SETUP ===")
    logger.info("Setting up environment for AI-generated test execution")
    
    # Create necessary directories
    directories = ["screenshots/passed", "screenshots/failed", "reports", "logs"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Created directory: {directory}")
    
    # Check if test files exist
    test_files = [
        "tests/smoke/execute_login_tracker_test.py",
        "tests/smoke/Login.md",
        "prompts/testcase-generation.md",
        "prompts/playwright-generation.md"
    ]
    
    for file_path in test_files:
        if os.path.exists(file_path):
            logger.info(f"[OK] Found: {file_path}")
        else:
            logger.error(f"[ERROR] Missing: {file_path}")
            return False
    
    logger.info("Environment setup completed")
    return True


def run_test_with_pytest():
    """Run test using pytest with comprehensive reporting"""
    logger = Logger()
    
    logger.info("=== RUNNING PYTEST EXECUTION ===")
    
    # Pytest command with all options
    pytest_command = [
        sys.executable, "-m", "pytest",
        "tests/smoke/execute_login_tracker_test.py",
        "-v",  # Verbose output
        "--html=reports/html/login_test_report.html",  # HTML report
        "--self-contained-html",  # Self-contained HTML
        "--alluredir=reports/allure",  # Allure report
        "--junitxml=reports/junit/login_test_results.xml",  # JUnit XML
        "--tb=short",  # Short traceback
        "--maxfail=3",  # Stop after 3 failures
        "--browser=chromium",  # Use Chromium browser
        "--screenshot=only-on-failure",  # Screenshot on failure only
        "--video=retain-on-failure",  # Video on failure only
        "--tracing=retain-on-failure"  # Trace on failure only
    ]
    
    try:
        logger.info(f"Executing command: {' '.join(pytest_command)}")
        
        # Run pytest
        result = subprocess.run(
            pytest_command,
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        # Log output
        logger.info("=== PYTEST STDOUT ===")
        logger.info(result.stdout)
        
        if result.stderr:
            logger.error("=== PYTEST STDERR ===")
            logger.error(result.stderr)
        
        # Log result
        if result.returncode == 0:
            logger.info("[OK] Pytest execution completed successfully")
        else:
            logger.error(f"[ERROR] Pytest execution failed with return code: {result.returncode}")
        
        return result.returncode == 0
        
    except Exception as e:
        logger.error(f"Failed to run pytest: {str(e)}")
        return False


def generate_execution_summary():
    """Generate comprehensive execution summary"""
    logger = Logger()
    
    logger.info("=== GENERATING EXECUTION SUMMARY ===")
    
    summary = {
        "execution_info": {
            "timestamp": datetime.now().isoformat(),
            "framework": "App Tracker Automation",
            "test_type": "AI-Generated Smoke Test",
            "prompts_used": ["testcase-generation.md", "playwright-generation.md"],
            "environment": "UAT",
            "browser": "Chromium"
        },
        "test_files": {
            "test_case": "tests/smoke/Login.md",
            "test_script": "tests/smoke/execute_login_tracker_test.py",
            "locators": "locators/aditya_birla_locators.py",
            "pages": [
                "pages/aditya_birla_login_page.py",
                "pages/aditya_birla_dashboard_page.py",
                "pages/aditya_birla_tracker_page.py"
            ]
        },
        "reports_generated": [],
        "artifacts_created": []
    }
    
    # Check for generated reports
    report_files = [
        "reports/html/login_test_report.html",
        "reports/junit/login_test_results.xml"
    ]
    
    for report_file in report_files:
        if os.path.exists(report_file):
            summary["reports_generated"].append(report_file)
            logger.info(f"[OK] Report generated: {report_file}")
    
    # Check for artifacts
    artifact_dirs = ["screenshots", "reports/allure"]
    for artifact_dir in artifact_dirs:
        if os.path.exists(artifact_dir):
            files = os.listdir(artifact_dir)
            if files:
                summary["artifacts_created"].extend([f"{artifact_dir}/{file}" for file in files])
                logger.info(f"[OK] Artifacts in {artifact_dir}: {len(files)} files")
    
    # Save summary
    summary_file = f"reports/execution_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    logger.info(f"Execution summary saved: {summary_file}")
    return summary_file


def main():
    """Main execution function"""
    logger = Logger()
    
    logger.info("=== AI-DRIVEN TEST EXECUTION START ===")
    logger.info("Framework: App Tracker Automation")
    logger.info("Test: Login & Application Tracker Navigation")
    logger.info("Generated using: testcase-generation.md, playwright-generation.md")
    
    try:
        # Step 1: Setup environment
        if not setup_environment():
            logger.error("Environment setup failed")
            return False
        
        # Step 2: Run tests
        success = run_test_with_pytest()
        
        # Step 3: Generate summary
        summary_file = generate_execution_summary()
        
        # Step 4: Final status
        if success:
            logger.info("=== TEST EXECUTION COMPLETED SUCCESSFULLY ===")
            logger.info(f"View reports: reports/html/login_test_report.html")
            logger.info(f"View summary: {summary_file}")
            return True
        else:
            logger.error("=== TEST EXECUTION FAILED ===")
            logger.info("Check logs and screenshots for details")
            return False
            
    except Exception as e:
        logger.error(f"Test execution failed with exception: {str(e)}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
