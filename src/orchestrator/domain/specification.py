from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class SpecificationVersion:
    spec_id: str
    version: int
    title: str
    content: str
    modules: list[str]
    acceptance_criteria: list[str]
    constraints: list[str]
    document_version_ids: list[str]
    created_at: str
