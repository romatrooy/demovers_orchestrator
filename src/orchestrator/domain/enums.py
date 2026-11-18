from enum import Enum

class TaskStatus(str, Enum):
    CREATED = "created"
    SPEC_REVIEW = "spec_review"
    SPEC_REVISION_REQUIRED = "spec_revision_required"
    READY = "ready"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    RESULT_REVIEW = "result_review"
    REWORK_REQUIRED = "rework_required"
    FAILED = "failed"
    ACCEPTED = "accepted"
    CANCELLED = "cancelled"
    MANUALLY_COMPLETED = "manually_completed"

class AttemptStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    SUCCEEDED = "succeeded"
    FAILED = "failed"

class ControlType(str, Enum):
    SCOPE_CHECK = "scope_check"
    BASE_FRESHNESS_CHECK = "base_freshness_check"

class ReportStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    IMPOSSIBLE = "impossible"
