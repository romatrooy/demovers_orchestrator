import re

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

        requirements = [
            match.group(1).strip()
            for line in description.splitlines()
            if (match := re.match(r"^\s*(?:[-*]|\d+[.)])\s+(.+?)\s*$", line))
        ]
        tasks: list[TaskDraft] = []
        requirement_keys: list[str] = []
        dependency_check_key: str | None = None

        for index, requirement in enumerate(requirements, start=1):
            client_key = f"demo-task-{index:02d}"
            dependencies = [dependency_check_key] if dependency_check_key and "цик" in requirement.lower() else []
            if "ошиб" in requirement.lower():
                dependencies = list(requirement_keys)
            if "depends_on" in requirement or "ссыл" in requirement.lower():
                dependency_check_key = client_key

            tasks.append(
                TaskDraft(
                    client_key=client_key,
                    title=requirement.rstrip(".;")[:120],
                    description=f"В рамках задачи «{title}»: {requirement}",
                    acceptance_criteria=[requirement.rstrip(".;") + "."],
                    expected_result=f"Реализовано требование: {requirement.rstrip(';.')}.",
                    change_scope=self._change_scope,
                    depends_on=dependencies,
                )
            )
            requirement_keys.append(client_key)

        if not tasks:
            tasks.append(
                TaskDraft(
                    client_key="demo-task-01",
                    title=title[:120],
                    description=description,
                    acceptance_criteria=["Реализация соответствует описанию задачи."],
                    expected_result="Изменения, соответствующие описанию задачи.",
                    change_scope=self._change_scope,
                    depends_on=[],
                )
            )
            requirement_keys.append("demo-task-01")

        if re.search(r"до вызова Tracker|до передачи графа", description, re.IGNORECASE):
            tasks.append(
                TaskDraft(
                    client_key="demo-task-integration",
                    title="Подключить проверку DAG перед отправкой в Tracker",
                    description=(
                        "Вызвать проверку после построения TaskGraphDraft и до передачи "
                        "графа в Tracker; отклонять невалидный граф с понятной ошибкой."
                    ),
                    acceptance_criteria=[
                        "Проверка выполняется до отправки графа в Tracker.",
                        "Невалидный граф не передаётся в Tracker.",
                    ],
                    expected_result="Валидный граф готов к передаче; невалидный отклонён локально.",
                    change_scope=self._change_scope,
                    depends_on=requirement_keys,
                )
            )

        return TaskGraphDraft(
            specification_version=self._version,
            base_spec_id=self._specification_id,
            tasks=tasks,
        )
