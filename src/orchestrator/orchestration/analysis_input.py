import json
from pathlib import Path
from typing import Any

from orchestrator.domain.packages import AnalysisPackage


def load_task_description(path: str | Path) -> AnalysisPackage:
    """Wrap a plain-text demo task in the normal analysis-package shape."""
    task_path = Path(path)
    try:
        description = task_path.read_text(encoding="utf-8-sig").strip()
    except OSError as error:
        raise ValueError(f"cannot read task description '{task_path}': {error}") from error

    if not description:
        raise ValueError(f"task description '{task_path}' is empty")

    title = next((line.strip() for line in description.splitlines() if line.strip()), "")
    return AnalysisPackage(
        specification={"title": title[:120], "content": description},
        documents=[],
        constraints=[],
        previous_results=[],
        remarks=["Input loaded from a plain-text demo task."],
    )


def load_analysis_package(path: str | Path) -> AnalysisPackage:
    """Load an analysis-package JSON file for local orchestration."""
    package_path = Path(path)
    try:
        with package_path.open("r", encoding="utf-8") as source:
            payload: Any = json.load(source)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"analysis package is not valid JSON at line {error.lineno}, column {error.colno}"
        ) from error

    try:
        return AnalysisPackage.from_mapping(payload)
    except ValueError as error:
        raise ValueError(f"invalid analysis package '{package_path}': {error}") from error
