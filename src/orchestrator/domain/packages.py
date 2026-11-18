from dataclasses import dataclass
from collections.abc import Mapping
from typing import Any, Optional

@dataclass
class AnalysisPackage:
    specification: dict[str, Any]
    documents: list[dict[str, Any]]
    constraints: list[str]
    previous_results: list[dict[str, Any]]   # при пересмотре
    remarks: list[str]

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "AnalysisPackage":
        """Build an analysis package from the JSON object passed to the orchestrator."""
        if not isinstance(value, Mapping):
            raise ValueError("analysis package must be a JSON object")

        expected = {
            "specification": dict,
            "documents": list,
            "constraints": list,
            "previous_results": list,
            "remarks": list,
        }
        missing = [name for name in expected if name not in value]
        if missing:
            raise ValueError(f"analysis package is missing required fields: {', '.join(missing)}")

        invalid = [
            f"{name} (expected {kind.__name__})"
            for name, kind in expected.items()
            if not isinstance(value[name], kind)
        ]
        if invalid:
            raise ValueError("invalid analysis package fields: " + ", ".join(invalid))

        for name in ("documents", "previous_results"):
            if not all(isinstance(item, dict) for item in value[name]):
                raise ValueError(f"analysis package field '{name}' must contain JSON objects")
        for name in ("constraints", "remarks"):
            if not all(isinstance(item, str) for item in value[name]):
                raise ValueError(f"analysis package field '{name}' must contain strings")

        return cls(
            specification=dict(value["specification"]),
            documents=list(value["documents"]),
            constraints=list(value["constraints"]),
            previous_results=list(value["previous_results"]),
            remarks=list(value["remarks"]),
        )

    def to_mapping(self) -> dict[str, Any]:
        """Return the package in the agreed JSON field format."""
        return {
            "specification": self.specification,
            "documents": self.documents,
            "constraints": self.constraints,
            "previous_results": self.previous_results,
            "remarks": self.remarks,
        }

@dataclass
class ExecutionPackage:
    task_id: str
    title: str
    description: str
    acceptance_criteria: list[str]
    expected_result: str
    change_scope: list[str]
    dependency_results: list[dict[str, Any]]
    previous_result: Optional[dict[str, Any]]
    rejection_reason: Optional[str]
