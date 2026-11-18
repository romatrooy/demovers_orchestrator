import argparse
import asyncio
import json
import sys
from dataclasses import asdict

from orchestrator.agents.analyst import DemoAnalystAgent
from orchestrator.orchestration.analysis_input import load_task_description
from orchestrator.orchestration.decomposition import DecompositionService


async def _decompose(args: argparse.Namespace) -> int:
    package = load_task_description(args.input)
    analyst = DemoAnalystAgent(
        change_scope=args.scope or ["src/orchestrator"],
        specification_id=args.spec_id,
        version=args.spec_version,
    )
    graph = await DecompositionService(analyst).build_graph(package)
    rendered = json.dumps(asdict(graph), ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as destination:
            destination.write(rendered + "\n")
    else:
        print(rendered)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a text-file decomposition demo.")
    parser.add_argument("input", help="UTF-8 .txt file with the task description")
    parser.add_argument(
        "--scope",
        action="append",
        help="Repository-relative change_scope path; repeat for multiple paths",
    )
    parser.add_argument("--spec-id", default="demo-spec")
    parser.add_argument("--spec-version", type=int, default=1)
    parser.add_argument("--output", help="Write the DAG JSON to this path")
    args = parser.parse_args()

    try:
        return asyncio.run(_decompose(args))
    except (OSError, ValueError) as error:
        print(f"decomposition failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
