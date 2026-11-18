from dataclasses import dataclass
from typing import Optional
from .enums import ControlType, ReportStatus

@dataclass
class ChangeReport:
    report_id: str
    task_id: str
    attempt_id: Optional[str]          # null для base_freshness_check
    control_type: ControlType
    checked_at: str
    base_revision: Optional[str]
    head_revision: Optional[str]
    affected_paths: list[str]
    out_of_scope_paths: list[str]
    has_uncommitted_changes: bool
    status: ReportStatus
    summary: str
    impossible_reason: Optional[str] = None
