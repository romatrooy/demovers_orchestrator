class TrackerClient:
    def __init__(self, base_url: str, token: str): ...

    # Спецификации
    async def get_analysis_package(
        self, spec_id: str, specification_version: int
    ) -> AnalysisPackage: ...

    # Граф
    async def import_task_graph(
        self, spec_id: str, specification_version: int, graph: TaskGraphDraft,
        idempotency_key: str
    ) -> ImportedGraph: ...

    async def replace_task_graph(
        self, graph_id: str, graph: TaskGraphDraft,
        base_graph_version: int, idempotency_key: str
    ) -> ImportedGraph: ...

    # Задачи
    async def get_executable_tasks(self, graph_id: str) -> list[Task]: ...
    async def get_task(self, task_id: str) -> Task: ...
    async def assign(
        self, task_id: str, agent_id: str, expected_version: int,
        idempotency_key: str
    ) -> Task: ...

    async def get_execution_package(self, task_id: str) -> ExecutionPackage: ...

    # Попытки
    async def start_attempt(
        self, task_id: str, agent_id: str, expected_version: int,
        base_revision: str, worktree_id: str,
        report_id: Optional[str], idempotency_key: str
    ) -> Attempt: ...

    async def complete_attempt(
        self, attempt_id: str, result: AttemptResult,
        expected_version: int, idempotency_key: str
    ) -> None: ...

    async def fail_attempt(
        self, attempt_id: str, failure_reason: str,
        expected_version: int, idempotency_key: str
    ) -> None: ...

    # Отчёты
    async def submit_report(
        self, report: ChangeReport, idempotency_key: str
    ) -> ChangeReport: ...

    # Публикация
    async def confirm_publication(
        self, task_id: str, result_version: str,
        base_revision: str, head_revision: str,
        idempotency_key: str
    ) -> None: ...

    # Восстановление
    async def get_graph_state(self, graph_id: str) -> dict: ...
    async def list_assigned_and_in_progress(self, graph_id: str) -> list[Task]: ...
