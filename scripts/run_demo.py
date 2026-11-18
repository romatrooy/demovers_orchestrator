import argparse
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from orchestrator.agents.executor import DemoExecutor
from orchestrator.orchestration.decomposition import load_task_graph
from orchestrator.orchestration.engine import OrchestratorEngine
from orchestrator.tracker.mock_client import MockTrackerClient
from orchestrator.validation.dag_validator import DagValidationError


async def run(input_path: Path, fail_task: str | None) -> int:
    try:
        draft = load_task_graph(input_path)
        print(
            f"[ORCHESTRATOR] загружен граф: {len(draft.tasks)} задач, "
            f"спецификация={draft.base_spec_id}@{draft.specification_version}"
        )
        engine = OrchestratorEngine(
            tracker=MockTrackerClient(),
            executor=DemoExecutor(fail_task=fail_task),
        )
        await engine.run_graph(draft)
        return 0
    except DagValidationError as error:
        print(f"[ORCHESTRATOR] DAG отклонён: {error}", file=sys.stderr)
        return 2
    except (OSError, ValueError) as error:
        print(f"[ORCHESTRATOR] не удалось загрузить граф: {error}", file=sys.stderr)
        return 2


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the in-memory orchestration demo.")
    parser.add_argument(
        "--input",
        type=Path,
        default=ROOT / "data" / "input_graph.json",
        help="TaskGraphDraft JSON file",
    )
    parser.add_argument(
        "--fail-task",
        help="Simulate an executor failure for this client_key",
    )
    args = parser.parse_args()
    return asyncio.run(run(args.input, args.fail_task))


if __name__ == "__main__":
    raise SystemExit(main())
