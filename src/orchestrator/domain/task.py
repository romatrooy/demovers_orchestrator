from dataclasses import dataclass
from typing import Optional
from .enums import TaskStatus

@dataclass
class Task:
    task_id: str
    graph_id: str
    client_key: Optional[str]
    title: str
    status: TaskStatus
    version: int
    change_scope: list[str]
    agent_id: Optional[str] = None
    active_attempt_id: Optional[str] = None
    executable: bool = False
