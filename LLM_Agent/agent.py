"""LLM agent scaffolding for context, history, and review."""

from typing import Dict, List, Any


class LLMAgent:
    def __init__(self):
        self.context_store: Dict[str, Any] = {}
        self.chat_history: List[Dict[str, Any]] = []

    def add_context(self, source_id: str, content: str) -> None:
        self.context_store[source_id] = content

    def create_prompt(self, task: str, rules: List[str]) -> str:
        context_snippet = "\n".join(list(self.context_store.values())[:3])
        prompt = (
            f"Task: {task}\n"
            f"Rules:\n" + "\n".join(f"- {rule}" for rule in rules) + "\n"
            f"Context:\n{context_snippet}\n"
            "Provide a concise, rule-aligned response."
        )
        return prompt

    def add_chat_entry(self, role: str, message: str) -> None:
        self.chat_history.append({"role": role, "message": message})

    def review_artifact(self, artifact: str) -> Dict[str, Any]:
        return {
            "artifact": artifact,
            "reviewNotes": [
                "Verify alignment with folder 1 rules.",
                "Check for clear steps and pass/fail criteria.",
                "Ensure traceability to requirements and scenarios."
            ],
            "recommendation": "manual validation needed for ambiguous or domain-specific cases."
        }
