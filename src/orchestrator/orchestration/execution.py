from orchestrator.agents.executor import DemoExecutionFailure, DemoExecutor
from orchestrator.domain.task import Task
from orchestrator.tracker.mock_client import MockTrackerClient


class ExecutionManager:
    def __init__(self, tracker: MockTrackerClient, executor: DemoExecutor):
        self._tracker = tracker
        self._executor = executor

    async def process_executable_tasks(self, graph_id: str) -> None:
        while True:
            tasks = await self._tracker.get_executable_tasks(graph_id)
            if not tasks:
                return

            print(f"[ORCHESTRATOR] executable задач: {len(tasks)}")
            for task in tasks:
                await self.run_single_task(task)

    async def run_single_task(self, task: Task) -> None:
        print(f"[ORCHESTRATOR] assign {task.client_key} -> {self._executor.agent_id}")
        assigned = await self._tracker.assign(
            task_id=task.task_id,
            agent_id=self._executor.agent_id,
            expected_version=task.version,
            idempotency_key=f"demo-assign-{task.task_id}",
        )
        attempt = await self._tracker.start_attempt(
            task_id=assigned.task_id,
            agent_id=self._executor.agent_id,
            expected_version=assigned.version,
        )
        print(f"[ORCHESTRATOR] start_attempt {attempt.attempt_id} for {task.client_key}")

        try:
            result = await self._executor.execute(task)
        except DemoExecutionFailure as error:
            await self._tracker.fail_attempt(
                attempt_id=attempt.attempt_id,
                failure_reason=str(error),
                expected_version=attempt.version,
            )
            print(f"[ORCHESTRATOR] fail {task.client_key}: {error}")
            return

        await self._tracker.complete_attempt(
            attempt_id=attempt.attempt_id,
            result=result,
            expected_version=attempt.version,
        )
        print(f"[ORCHESTRATOR] complete {task.client_key}")
