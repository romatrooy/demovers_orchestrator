from dataclasses import dataclass
from typing import Optional

@dataclass
class TaskDraft:
    """Задача до импорта в Трекер (с client_key)."""
    client_key: str
    title: str
    description: str
    acceptance_criteria: list[str]
    expected_result: str
    change_scope: list[str]          # пути относительно корня репозитория
    depends_on: list[str]            # client_key зависимостей

@dataclass
class TaskGraphDraft:
    specification_version: int
    base_spec_id: str
    tasks: list[TaskDraft]

@dataclass
class ImportedTask:
    client_key: str
    task_id: str
    version: int
    status: str

@dataclass
class ImportedGraph:
    graph_id: str
    graph_version: int
    specification_version: int
    tasks: list[ImportedTask]
