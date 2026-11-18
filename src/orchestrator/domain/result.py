from dataclasses import dataclass
from typing import Optional

@dataclass
class Artifact:
    name: str
    type: str
    uri: str

@dataclass
class AttemptResult:
    description: str
    artifacts: list[Artifact]
