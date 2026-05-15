"""QA Auditor Agent - Specialized agent for auditing test artifacts."""

import os
from typing import Dict, List, Any
from .agent import LLMAgent


class QAAuditorAgent(LLMAgent):
    def __init__(self, rules_folder_path: str = None):
        super().__init__()
        self.rules_folder = rules_folder_path or os.path.join(os.path.dirname(__file__), '..', 'Rules')
        self.load_rules()

    def load_rules(self) -> None:
        """Load rules from the Rules folder."""
        # Load QA auditor rules
        qa_rules_path = os.path.join(self.rules_folder, 'qa_auditor_rules.md')
        if os.path.exists(qa_rules_path):
            with open(qa_rules_path, 'r') as f:
                self.add_context('qa_auditor_rules', f.read())

        # Load other rule files
        rule_files = ['test_case_rules.md', 'test_scenario_rules.md', 'test_script_rules.md']
        for rule_file in rule_files:
            rule_path = os.path.join(self.rules_folder, rule_file)
            if os.path.exists(rule_path):
                with open(rule_path, 'r') as f:
                    self.add_context(rule_file.replace('.md', '_rules'), f.read())

    def audit_artifact(self, artifact_type: str, artifact_content: str) -> Dict[str, Any]:
        """Audit a test artifact against the loaded rules."""
        rules = [
            "Requirement traceability",
            "Business impact clarity",
            "Rule compliance",
            "Data realism",
            "Reusability",
            "Security and privacy",
            "LLM / AI-generated validation"
        ]

        prompt = self.create_prompt(
            f"Audit this {artifact_type} artifact for compliance with QA standards.",
            rules
        )

        # Simulate audit process (in real implementation, this would call an LLM)
        audit_result = {
            "artifact_type": artifact_type,
            "artifact_content": artifact_content[:200] + "..." if len(artifact_content) > 200 else artifact_content,
            "checklist_results": {
                "requirement_traceability": "Pass" if "requirement" in artifact_content.lower() else "Needs Review",
                "business_impact": "Pass" if "impact" in artifact_content.lower() else "Needs Review",
                "rule_compliance": "Pass",  # Assume compliant for demo
                "data_realism": "Pass" if "test data" in artifact_content.lower() else "Needs Review",
                "reusability": "Pass" if "reusable" in artifact_content.lower() else "Needs Review",
                "security_privacy": "Pass" if "sensitive" not in artifact_content.lower() else "Needs Review",
                "llm_validation": "Pass"  # Assume validated
            },
            "findings": [],
            "recommendations": [],
            "approval_status": "Approved" if all(v == "Pass" for v in [
                "requirement_traceability", "business_impact", "rule_compliance",
                "data_realism", "reusability", "security_privacy", "llm_validation"
            ]) else "Needs Changes"
        }

        return audit_result

    def generate_audit_report(self, audit_results: List[Dict[str, Any]]) -> str:
        """Generate a comprehensive audit report."""
        report = "# QA Audit Report\n\n"
        for i, result in enumerate(audit_results, 1):
            report += f"## Artifact {i}: {result['artifact_type']}\n"
            report += f"- **Status**: {result['approval_status']}\n"
            report += f"- **Findings**: {', '.join(result['findings']) or 'None'}\n"
            report += f"- **Recommendations**: {', '.join(result['recommendations']) or 'None'}\n\n"

        return report