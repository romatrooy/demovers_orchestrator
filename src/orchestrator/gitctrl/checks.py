class GitChangeChecker:
    def __init__(self, repo: GitRepository): ...

    def scope_check(
        self,
        task_id: str,
        attempt_id: str,
        change_scope: list[str],
        base_revision: str,
        head_revision: str,
    ) -> ChangeReport:
        """Проверка выхода за change_scope при завершении попытки."""
        ...

    def base_freshness_check(
        self,
        task_id: str,
        change_scope: list[str],
        base_revision: str,
        head_revision: str,
    ) -> ChangeReport:
        """Проверка актуальности основания перед повтором."""
        ...
