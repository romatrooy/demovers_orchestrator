@dataclass
class LocalAttemptState:
    attempt_id: str
    task_id: str
    agent_id: str
    worktree_id: str
    base_revision: str
    started_at: str
    pending_report: Optional[ChangeReport] = None

class LocalStateStore:
    """Хранит активные запуски и недоставленные отчёты для восстановления."""
    def save_attempt(self, state: LocalAttemptState) -> None: ...
    def get_active_attempts(self) -> list[LocalAttemptState]: ...
    def mark_report_pending(self, attempt_id: str, report: ChangeReport) -> None: ...
    def clear_attempt(self, attempt_id: str) -> None: ...
