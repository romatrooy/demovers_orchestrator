from dataclasses import dataclass
from collections.abc import Mapping
from typing import Any, Optional

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

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TaskGraphDraft":
        if not isinstance(value, Mapping):
            raise ValueError("task graph must be a JSON object")
        for field in ("specification_version", "base_spec_id", "tasks"):
            if field not in value:
                raise ValueError(f"task graph is missing required field '{field}'")
        if not isinstance(value["specification_version"], int):
            raise ValueError("specification_version must be an integer")
        if not isinstance(value["base_spec_id"], str):
            raise ValueError("base_spec_id must be a string")
        if not isinstance(value["tasks"], list):
            raise ValueError("tasks must be an array")

        tasks: list[TaskDraft] = []
        task_fields = {
            "client_key": str,
            "title": str,
            "description": str,
            "acceptance_criteria": list,
            "expected_result": str,
            "change_scope": list,
            "depends_on": list,
        }
        for index, raw_task in enumerate(value["tasks"]):
            if not isinstance(raw_task, Mapping):
                raise ValueError(f"tasks[{index}] must be an object")
            missing = [field for field in task_fields if field not in raw_task]
            if missing:
                raise ValueError(f"tasks[{index}] is missing required fields: {', '.join(missing)}")
            invalid = [
                field for field, expected_type in task_fields.items()
                if not isinstance(raw_task[field], expected_type)
            ]
            if invalid:
                raise ValueError(f"tasks[{index}] has invalid fields: {', '.join(invalid)}")
            if not all(isinstance(item, str) for item in raw_task["acceptance_criteria"]):
                raise ValueError(f"tasks[{index}].acceptance_criteria must contain strings")
            if not all(isinstance(item, str) for item in raw_task["change_scope"]):
                raise ValueError(f"tasks[{index}].change_scope must contain strings")
            if not all(isinstance(item, str) for item in raw_task["depends_on"]):
                raise ValueError(f"tasks[{index}].depends_on must contain strings")
            tasks.append(TaskDraft(**{field: raw_task[field] for field in task_fields}))

        return cls(
            specification_version=value["specification_version"],
            base_spec_id=value["base_spec_id"],
            tasks=tasks,
        )

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
