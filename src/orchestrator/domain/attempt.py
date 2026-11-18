from dataclasses import dataclass
from typing import Optional
from .enums import AttemptStatus

@dataclass
class Attempt:
    attempt_id: str
    task_id: str
    agent_id: str
    status: AttemptStatus
    version: int
    base_revision: Optional[str] = None   # Git SHA на старте
    head_revision: Optional[str] = None
    worktree_id: Optional[str] = None     # идентификатор рабочей копии
    report_id: Optional[str] = None       # freshness report, если был
