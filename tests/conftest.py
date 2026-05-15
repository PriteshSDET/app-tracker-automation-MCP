import json
import os
from datetime import datetime

import pytest


ACTIVE_RAG_DIR = "rag/active/execution_logs/"


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        item.test_result = report.outcome
        item.error_message = str(report.longrepr) if report.failed else None


def pytest_sessionfinish(session, exitstatus):
    """Sync completed test execution data back to the active RAG."""
    print("\n[Test Pilot AI] Syncing execution data to RAG...")

    os.makedirs(ACTIVE_RAG_DIR, exist_ok=True)

    run_summary = {
        "timestamp": datetime.now().isoformat(),
        "total_passed": 0,
        "total_failed": 0,
        "failed_tests": [],
    }

    for item in session.items:
        if hasattr(item, "test_result"):
            if item.test_result == "passed":
                run_summary["total_passed"] += 1
            elif item.test_result == "failed":
                run_summary["total_failed"] += 1
                run_summary["failed_tests"].append(
                    {
                        "test_name": item.nodeid,
                        "error": item.error_message,
                    }
                )

    log_filename = f"{ACTIVE_RAG_DIR}run_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(log_filename, "w", encoding="utf-8") as file:
        json.dump(run_summary, file, indent=4)

    print(f"RAG Context Updated: Saved execution context to {log_filename}")
