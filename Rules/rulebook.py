"""Rule definitions and audit helpers for QA artifacts."""

from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class TestCaseRule:
    title: str
    description: str
    preconditions: List[str]
    steps: List[str]
    expected_result: str
    test_data: Dict[str, str]
    priority: str
    tags: List[str]


def validate_test_case(test_case: TestCaseRule) -> List[str]:
    errors = []
    if not test_case.title:
        errors.append("Title is required.")
    if not test_case.description:
        errors.append("Description is required.")
    if not test_case.steps:
        errors.append("At least one step is required.")
    if not test_case.expected_result:
        errors.append("Expected result is required.")
    if not test_case.priority:
        errors.append("Priority is required.")
    if not test_case.tags:
        errors.append("At least one tag is required.")
    return errors


def audit_test_case(test_case: TestCaseRule) -> Dict[str, object]:
    return {
        "valid": len(validate_test_case(test_case)) == 0,
        "issues": validate_test_case(test_case),
        "auditNotes": [
            "Ensure traceability to requirements.",
            "Verify environment-agnostic design.",
            "Confirm no subjective criteria in expected results."
        ]
    }
