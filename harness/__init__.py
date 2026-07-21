"""Verifier for Lean 4 definitional faithfulness."""

from harness.admissibility import AdmissibilityFailure, AdmissibilityVerdict, check_admissibility
from harness.repl import (
    WarmupTimeoutError,
    get_warm_environment,
    run_checked,
    start_server_with_watchdog,
    warm_import,
)
from harness.results import CandidateScore, CheckResult, CheckStatus
from harness.scoring import PinnedSignature, run_facts, score_candidate, score_spliced_candidate, splice_candidate

__all__ = [
    "AdmissibilityFailure",
    "AdmissibilityVerdict",
    "check_admissibility",
    "WarmupTimeoutError",
    "get_warm_environment",
    "run_checked",
    "start_server_with_watchdog",
    "warm_import",
    "CandidateScore",
    "CheckResult",
    "CheckStatus",
    "PinnedSignature",
    "run_facts",
    "score_candidate",
    "score_spliced_candidate",
    "splice_candidate",
]
