"""Verifier for Lean 4 definitional faithfulness."""

from harness.admissibility import AdmissibilityFailure, AdmissibilityVerdict, check_admissibility
from harness.facts import Fact
from harness.repl import (
    WarmupTimeoutError,
    get_warm_environment,
    run_checked,
    start_server_with_watchdog,
    warm_import,
)
from harness.results import (
    CandidateScore,
    CheckResult,
    CheckStatus,
    ExcessiveUnknownFlag,
    FactResult,
    ProofStatus,
)
from harness.scoring import PinnedSignature, run_facts, score_candidate, score_spliced_candidate, splice_candidate
from harness.task_schema import TaskSchemaError, ValidatedTask, validate_task_data, validate_task_dir

__all__ = [
    "AdmissibilityFailure",
    "AdmissibilityVerdict",
    "check_admissibility",
    "Fact",
    "WarmupTimeoutError",
    "get_warm_environment",
    "run_checked",
    "start_server_with_watchdog",
    "warm_import",
    "CandidateScore",
    "CheckResult",
    "CheckStatus",
    "ExcessiveUnknownFlag",
    "FactResult",
    "ProofStatus",
    "PinnedSignature",
    "run_facts",
    "score_candidate",
    "score_spliced_candidate",
    "splice_candidate",
    "TaskSchemaError",
    "ValidatedTask",
    "validate_task_data",
    "validate_task_dir",
]
