import json
from pathlib import Path
from typing import Any

from orchestrator.agents.base import AnalystAgent
from orchestrator.domain.graph import TaskGraphDraft
from orchestrator.domain.packages import AnalysisPackage
from orchestrator.validation.dag_validator import validate_task_graph


class DecompositionService:
    """Pass an already supplied analysis package to the analyst agent."""

    def __init__(self, analyst: AnalystAgent):
        self._analyst = analyst

    async def build_graph(self, package: AnalysisPackage) -> TaskGraphDraft:
        graph = await self._analyst.decompose(package)
        if not isinstance(graph, TaskGraphDraft):
            raise TypeError("analyst must return a TaskGraphDraft")
        validate_task_graph(graph)
        return graph


def load_task_graph(path: str | Path) -> TaskGraphDraft:
    graph_path = Path(path)
    try:
        with graph_path.open("r", encoding="utf-8-sig") as source:
            payload: Any = json.load(source)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"task graph is not valid JSON at line {error.lineno}, column {error.colno}"
        ) from error
    draft = TaskGraphDraft.from_mapping(payload)
    validate_task_graph(draft)
    return draft
