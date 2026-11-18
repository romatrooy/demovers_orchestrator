from orchestrator.agents.base import AnalystAgent
from orchestrator.domain.graph import TaskDraft, TaskGraphDraft
from orchestrator.domain.packages import AnalysisPackage


class DemoAnalystAgent(AnalystAgent):
    """Deterministic test analyst that returns a one-task graph draft."""

    agent_id = "demo-analyst"

    def __init__(self, change_scope: list[str], specification_id: str, version: int):
        if not change_scope or any(not scope.strip() for scope in change_scope):
            raise ValueError("at least one non-empty change_scope path is required")
        self._change_scope = [scope.strip() for scope in change_scope]
        self._specification_id = specification_id
        self._version = version

    async def decompose(self, package: AnalysisPackage) -> TaskGraphDraft:
        title = str(package.specification.get("title", "")).strip()
        description = str(package.specification.get("content", "")).strip()
        if not title or not description:
            raise ValueError("demo analysis package must contain specification.title and specification.content")

        task = TaskDraft(
            client_key="demo-task-1",
            title=title[:120],
            description=description,
            acceptance_criteria=["Реализация соответствует описанию задачи."],
            expected_result="Изменения в указанной области, соответствующие описанию задачи.",
            change_scope=self._change_scope,
            depends_on=[],
        )
        return TaskGraphDraft(
            specification_version=self._version,
            base_spec_id=self._specification_id,
            tasks=[task],
        )
