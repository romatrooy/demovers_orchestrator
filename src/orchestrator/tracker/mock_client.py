from dataclasses import replace

from orchestrator.domain.attempt import Attempt
from orchestrator.domain.graph import ImportedGraph, ImportedTask, TaskGraphDraft
from orchestrator.domain.result import AttemptResult
from orchestrator.domain.enums import AttemptStatus, TaskStatus
from orchestrator.domain.task import Task


class MockTrackerClient:
    """In-memory tracker used by the lifecycle demo."""

    def __init__(self) -> None:
        self.graph_id = "mock-graph-001"
        self._tasks: dict[str, Task] = {}
        self._dependencies: dict[str, list[str]] = {}
        self._attempts: dict[str, Attempt] = {}
        self._attempt_task_ids: dict[str, str] = {}
        self._counter = 0

    async def import_task_graph(self, draft: TaskGraphDraft) -> ImportedGraph:
        if self._tasks:
            raise RuntimeError("demo tracker accepts one task graph per run")

        imported: list[ImportedTask] = []
        for draft_task in draft.tasks:
            self._counter += 1
            task_id = f"mock-task-{self._counter:03d}"
            task = Task(
                task_id=task_id,
                graph_id=self.graph_id,
                client_key=draft_task.client_key,
                title=draft_task.title,
                status=TaskStatus.CREATED,
                version=1,
                change_scope=list(draft_task.change_scope),
                executable=False,
            )
            self._tasks[task_id] = task
            self._dependencies[task_id] = list(draft_task.depends_on)
            imported.append(
                ImportedTask(
                    client_key=draft_task.client_key,
                    task_id=task_id,
                    version=task.version,
                    status=task.status.value,
                )
            )

        return ImportedGraph(
            graph_id=self.graph_id,
            graph_version=1,
            specification_version=draft.specification_version,
            tasks=imported,
        )

    async def get_executable_tasks(self, graph_id: str) -> list[Task]:
        if graph_id != self.graph_id:
            raise ValueError(f"unknown graph_id '{graph_id}'")

        executable: list[Task] = []
        completed_keys = {
            task.client_key
            for task in self._tasks.values()
            if task.status == TaskStatus.ACCEPTED
        }
        for task_id, task in self._tasks.items():
            if task.status not in (TaskStatus.CREATED, TaskStatus.READY):
                continue
            if all(dependency in completed_keys for dependency in self._dependencies[task_id]):
                task.status = TaskStatus.READY
                task.executable = True
                executable.append(replace(task))
        return executable

    async def assign(
        self, task_id: str, agent_id: str, expected_version: int, idempotency_key: str
    ) -> Task:
        task = self._get_task(task_id)
        self._check_version(task.version, expected_version, task_id)
        if task.status != TaskStatus.READY or not task.executable:
            raise RuntimeError(f"task '{task_id}' is not executable")
        task.status = TaskStatus.ASSIGNED
        task.agent_id = agent_id
        task.executable = False
        task.version += 1
        return replace(task)

    async def start_attempt(
        self, task_id: str, agent_id: str, expected_version: int
    ) -> Attempt:
        task = self._get_task(task_id)
        self._check_version(task.version, expected_version, task_id)
        if task.status != TaskStatus.ASSIGNED or task.agent_id != agent_id:
            raise RuntimeError(f"task '{task_id}' is not assigned to '{agent_id}'")
        self._counter += 1
        attempt_id = f"mock-attempt-{self._counter:03d}"
        task.status = TaskStatus.IN_PROGRESS
        task.active_attempt_id = attempt_id
        task.version += 1
        attempt = Attempt(
            attempt_id=attempt_id,
            task_id=task_id,
            agent_id=agent_id,
            status=AttemptStatus.IN_PROGRESS,
            version=1,
            base_revision="mock-base",
            worktree_id=f"mock-worktree-{task_id}",
        )
        self._attempts[attempt_id] = attempt
        self._attempt_task_ids[attempt_id] = task_id
        return replace(attempt)

    async def complete_attempt(
        self, attempt_id: str, result: AttemptResult, expected_version: int
    ) -> None:
        attempt, task = self._get_attempt(attempt_id)
        self._check_version(attempt.version, expected_version, attempt_id)
        attempt.status = AttemptStatus.SUCCEEDED
        attempt.version += 1
        task.status = TaskStatus.ACCEPTED
        task.active_attempt_id = None
        task.version += 1
        print(f"[MOCK TRACKER] auto-accepted demo result for {task.client_key}")

    async def fail_attempt(
        self, attempt_id: str, failure_reason: str, expected_version: int
    ) -> None:
        attempt, task = self._get_attempt(attempt_id)
        self._check_version(attempt.version, expected_version, attempt_id)
        attempt.status = AttemptStatus.FAILED
        attempt.version += 1
        task.status = TaskStatus.FAILED
        task.active_attempt_id = None
        task.version += 1

    async def get_task_statuses(self, graph_id: str) -> list[Task]:
        if graph_id != self.graph_id:
            raise ValueError(f"unknown graph_id '{graph_id}'")
        return [replace(task) for task in self._tasks.values()]

    def _get_task(self, task_id: str) -> Task:
        try:
            return self._tasks[task_id]
        except KeyError as error:
            raise ValueError(f"unknown task_id '{task_id}'") from error

    def _get_attempt(self, attempt_id: str) -> tuple[Attempt, Task]:
        try:
            attempt = self._attempts[attempt_id]
            return attempt, self._get_task(self._attempt_task_ids[attempt_id])
        except KeyError as error:
            raise ValueError(f"unknown attempt_id '{attempt_id}'") from error

    @staticmethod
    def _check_version(actual: int, expected: int, object_id: str) -> None:
        if actual != expected:
            raise RuntimeError(
                f"version conflict for '{object_id}': expected {expected}, current {actual}"
            )
