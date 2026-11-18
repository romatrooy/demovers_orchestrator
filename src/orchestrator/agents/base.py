from abc import ABC, abstractmethod

from orchestrator.domain.graph import TaskGraphDraft
from orchestrator.domain.packages import AnalysisPackage, ExecutionPackage
from orchestrator.domain.result import AttemptResult


class BaseAgent(ABC):
    agent_id: str

class AnalystAgent(BaseAgent):
    @abstractmethod
    async def decompose(self, package: AnalysisPackage) -> TaskGraphDraft: ...

class ExecutorAgent(BaseAgent):
    @abstractmethod
    async def execute(self, package: ExecutionPackage, worktree_id: str) -> AttemptResult: ...
