from orchestrator.agents.base import AnalystAgent
from orchestrator.domain.graph import TaskGraphDraft
from orchestrator.domain.packages import AnalysisPackage


class DecompositionService:
    """Pass an already supplied analysis package to the analyst agent."""

    def __init__(self, analyst: AnalystAgent):
        self._analyst = analyst

    async def build_graph(self, package: AnalysisPackage) -> TaskGraphDraft:
        graph = await self._analyst.decompose(package)
        if not isinstance(graph, TaskGraphDraft):
            raise TypeError("analyst must return a TaskGraphDraft")
        return graph
