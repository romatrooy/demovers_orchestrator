from orchestrator.domain.graph import TaskGraphDraft


class DagValidationError(ValueError):
    def __init__(self, client_key: str | None, reason: str):
        self.client_key = client_key
        self.reason = reason
        super().__init__(f"[{client_key or 'graph'}] {reason}")


def validate_task_graph(draft: TaskGraphDraft) -> None:
    """Reject malformed task graphs before they are imported into a tracker."""
    keys = [task.client_key for task in draft.tasks]

    for key in keys:
        if not isinstance(key, str) or not key.strip():
            raise DagValidationError(None, "client_key не может быть пустым")

    seen: set[str] = set()
    for key in keys:
        if key in seen:
            raise DagValidationError(key, "client_key не уникален в пределах графа")
        seen.add(key)

    key_set = set(keys)
    for task in draft.tasks:
        if not isinstance(task.depends_on, list):
            raise DagValidationError(task.client_key, "depends_on должен быть списком client_key")
        for dependency in task.depends_on:
            if not isinstance(dependency, str):
                raise DagValidationError(task.client_key, "depends_on должен содержать строки client_key")
            if dependency not in key_set:
                raise DagValidationError(
                    task.client_key,
                    f"depends_on ссылается на несуществующий client_key '{dependency}'",
                )
            if dependency == task.client_key:
                raise DagValidationError(task.client_key, "задача не может зависеть от самой себя")

        if not isinstance(task.change_scope, list) or not any(
            isinstance(path, str) and path.strip() for path in task.change_scope
        ):
            raise DagValidationError(
                task.client_key,
                "должен быть задан хотя бы один непустой путь change_scope",
            )

    _check_no_cycles(draft)


def _check_no_cycles(draft: TaskGraphDraft) -> None:
    tasks = {task.client_key: task for task in draft.tasks}
    state: dict[str, int] = {}
    path: list[str] = []

    def visit(client_key: str) -> None:
        state[client_key] = 1
        path.append(client_key)
        for dependency in tasks[client_key].depends_on:
            if state.get(dependency, 0) == 1:
                cycle_start = path.index(dependency)
                cycle = " -> ".join(path[cycle_start:] + [dependency])
                raise DagValidationError(client_key, f"обнаружен цикл зависимостей: {cycle}")
            if state.get(dependency, 0) == 0:
                visit(dependency)
        path.pop()
        state[client_key] = 2

    for client_key in tasks:
        if state.get(client_key, 0) == 0:
            visit(client_key)
