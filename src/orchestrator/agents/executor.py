from orchestrator.domain.result import AttemptResult
from orchestrator.domain.task import Task


class DemoExecutionFailure(RuntimeError):
    pass


class DemoExecutor:
    """No-op executor for demonstrating the task lifecycle."""

    agent_id = "demo-executor"

    def __init__(self, fail_task: str | None = None):
        self._fail_task = fail_task

    async def execute(self, task: Task) -> AttemptResult:
        if task.client_key == self._fail_task:
            raise DemoExecutionFailure("демо-агент смоделировал ошибку выполнения")
        return AttemptResult(
            description=f"Демо-агент завершил задачу '{task.client_key}'.",
            artifacts=[],
        )
