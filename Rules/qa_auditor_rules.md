# QA Auditor Rules

## Purpose
Provide auditors with a checklist to review and approve test artifacts.

## Template
- **Artifact Type**: Test case, scenario, script.
- **Reviewer**: Name or role.
- **Review Date**: Date of review.
- **Checklist Items**:
  - Requirement traceability
  - Business impact clarity
  - Rule compliance
  - Data realism
  - Reusability
  - Security and privacy
  - LLM / AI-generated validation
- **Findings**: Summary of issues or improvements.
- **Recommendations**: Action items for author.
- **Approval Status**: Approved / Needs changes.

## Best Practice Example
- **Artifact Type**: Test case
- **Reviewer**: QA Auditor
- **Review Date**: 2026-05-09
- **Checklist Items**:
  - Traceable to requirement ID RQ-12345
  - Steps are atomic and clear
  - Expected result is measurable
  - Test data avoids sensitive production values
  - Tags are consistent with framework taxonomy
  - LLM-generated content reviewed for accuracy
- **Findings**:
  - Step 4 is ambiguous about form submission.
  - Expected result should include URL assertion.
- **Recommendations**:
  - Clarify step 4 to exactly click the submit button.
  - Add expected result assertion for dashboard URL.
- **Approval Status**: Needs changes
