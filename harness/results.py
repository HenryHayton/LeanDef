"""Result types shared across the verifier package.

`CheckStatus.ERRORED` is a first-class outcome distinct from `FAILED`: it means the check
itself never got a clean answer (timeout, REPL-level protocol error, unexpected exception),
not that the fact was false or the candidate was rejected. See item 3 of the task that
introduced this module: a wedged call must be recorded as ERRORED and never silently folded
into FAILED.
"""

from dataclasses import dataclass, field
from enum import Enum


class CheckStatus(Enum):
    PASSED = "passed"
    FAILED = "failed"
    ERRORED = "errored"


@dataclass(frozen=True)
class CheckResult:
    """The outcome of one REPL check (a splice, a fact, an admissibility probe, ...)."""

    status: CheckStatus
    elapsed_s: float
    detail: str = ""  # empty for a clean PASSED/FAILED; explains ERRORED or a FAILED reason
    env: int | None = None  # resulting environment id, if the check produced one
    raw_response: object | None = None  # the CommandResponse, when one was obtained -- lets
    # callers (e.g. the admissibility gate) inspect messages/sorries/declarations without a
    # second REPL round-trip. None when the call errored before a response came back.

    @property
    def passed(self) -> bool:
        return self.status is CheckStatus.PASSED

    @property
    def errored(self) -> bool:
        return self.status is CheckStatus.ERRORED


@dataclass
class CandidateScore:
    """The full outcome of scoring one candidate: admissibility verdict, then (if admitted)
    per-fact results and fidelity. `fact_results` is empty and `fidelity` is `None` when the
    candidate was rejected at the admissibility gate -- the scoring path must not run facts
    against an inadmissible candidate."""

    label: str
    splice: CheckResult
    admissible: bool
    admissibility_detail: str
    fact_results: list[CheckResult] = field(default_factory=list)

    @property
    def fidelity(self) -> float | None:
        if not self.admissible or not self.fact_results:
            return None
        n_passed = sum(1 for r in self.fact_results if r.status is CheckStatus.PASSED)
        return n_passed / len(self.fact_results)
