from orchestrator.agents.executor import DemoExecutor
from orchestrator.domain.graph import TaskGraphDraft
from orchestrator.orchestration.execution import ExecutionManager
from orchestrator.tracker.mock_client import MockTrackerClient
from orchestrator.validation.dag_validator import validate_task_graph


class OrchestratorEngine:
    def __init__(self, tracker: MockTrackerClient, executor: DemoExecutor):
        self._tracker = tracker
        self._execution = ExecutionManager(tracker, executor)

    async def run_graph(self, draft: TaskGraphDraft) -> None:
        print("[ORCHESTRATOR] проверка черновика DAG")
        validate_task_graph(draft)
        print("[ORCHESTRATOR] DAG валиден")

        imported = await self._tracker.import_task_graph(draft)
        print(
            f"[ORCHESTRATOR] граф отправлен в Mock Tracker: "
            f"graph_id={imported.graph_id}, graph_version={imported.graph_version}"
        )
        for item in imported.tasks:
            print(f"[TRACKER] {item.client_key} -> {item.task_id} ({item.status})")

        await self._execution.process_executable_tasks(imported.graph_id)

        print("[ORCHESTRATOR] финальные статусы:")
        statuses = await self._tracker.get_task_statuses(imported.graph_id)
        for task in statuses:
            print(f"  {task.client_key}: {task.status.value}")
