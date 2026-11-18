class OrchestratorEngine:
    def __init__(
        self,
        tracker: TrackerClient,
        git_checker: GitChangeChecker,
        analyst: AnalystAgent,
        executor_factory: Callable[..., ExecutorAgent],
    ): ...

    async def run_specification(
        self, project_id: str, spec_id: str, specification_version: int
    ) -> None:
        """Полный цикл: декомпозиция → исполнение → публикация."""
        ...

    async def recovery(self) -> None:
        """Восстановление после перезапуска."""
        ...
