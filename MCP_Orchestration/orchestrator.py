"""MCP orchestration prototype for context gathering and execution control."""

from typing import Dict, List, Any


class MCPOrchestrator:
    def __init__(self):
        self.context_store: Dict[str, Any] = {}
        self.execution_queue: List[Dict[str, Any]] = []

    def add_context(self, key: str, payload: Any) -> None:
        self.context_store[key] = payload

    def get_context(self, key: str) -> Any:
        return self.context_store.get(key)

    def schedule_test(self, test_id: str, metadata: Dict[str, Any]) -> None:
        self.execution_queue.append({"id": test_id, "metadata": metadata})

    def select_tests(self, rules: Dict[str, Any]) -> List[Dict[str, Any]]:
        selected = []
        for item in self.execution_queue:
            if item["metadata"].get("priority") in rules.get("priorities", ["high", "medium"]):
                selected.append(item)
        return selected

    def summarize_context(self) -> Dict[str, Any]:
        return {
            "contextCount": len(self.context_store),
            "queueSize": len(self.execution_queue)
        }
