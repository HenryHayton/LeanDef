"""Result types shared across the verifier package.

Status vocabulary is per-mechanism, per `docs/design/task_schema_v1_1.md` "Scoring semantics"
(and the underlying tri-state protocol in
`docs/design/verifier_architecture_2026-07-20.md` §4):

- `CheckStatus` (mechanism `decide`): PASSED | FAILED | ERRORED. Unchanged from before this
  module existed -- this is also the vocabulary for infrastructure-level REPL checks that
  aren't fact adjudication at all (splicing, the admissibility gate's axiom probe).
- `ProofStatus` (mechanism `proof`): TRUE | FALSE | UNKNOWN | ERRORED. Nothing in this
  codebase produces `UNKNOWN` yet -- that's the future prover scaffold
  (`docs/decidability_bias_survey.md` finding 1) -- but the type exists now so fidelity and
  the EXCESSIVE_UNKNOWN flag have something real to compute against once it does.

Both vocabularies distinguish ERRORED (the check itself never got a clean answer: timeout,
REPL-level protocol error, unexpected exception) from a genuine negative result (FAILED /
FALSE). ERRORED and, for proof-mechanism facts, UNKNOWN are never folded into a failure.
"""

from dataclasses import dataclass, field
from enum import Enum

from harness import config as cfg


class CheckStatus(Enum):
    PASSED = "passed"
    FAILED = "failed"
    ERRORED = "errored"


class ProofStatus(Enum):
    TRUE = "true"
    FALSE = "false"
    UNKNOWN = "unknown"
    ERRORED = "errored"


@dataclass(frozen=True)
class CheckResult:
    """The outcome of one raw REPL check (a splice, an admissibility probe, a warm-up
    import, ...) -- always mechanism `decide` in spirit, whether or not it's adjudicating a
    fact at all."""

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


class SplicePath(Enum):
    """Which of the four enumerated splice attempts produced a result.

    Ordering is `plain -> noncomputable -> root_qualified -> both`, each step taken ONLY when
    the previous attempt's error specifically calls for it, so the common case costs exactly
    one REPL round-trip and the worst case is bounded at four.
    """

    PLAIN = "plain"
    NONCOMPUTABLE = "noncomputable"
    ROOT_QUALIFIED = "root_qualified"
    ROOT_QUALIFIED_NONCOMPUTABLE = "root_qualified+noncomputable"


@dataclass(frozen=True)
class SpliceAttempt:
    """One attempt in the ladder, kept whether it won or lost."""

    path: SplicePath
    cmd_text: str
    status: CheckStatus
    detail: str


@dataclass(frozen=True)
class SpliceOutcome:
    """The candidate-splice ladder's full outcome -- designed so Stage B can persist it
    per candidate by reading `path.value`, `retries_consumed` and `succeeded` directly.

    `result` is the CheckResult callers should score against. On success it is the winning
    attempt's. **On total failure it is the PLAIN attempt's**, deliberately: the plain error
    is the honest primary diagnostic ("this candidate does not compile"), and surfacing a
    retry's error instead would pollute the failure funnel with noise from a rescue that was
    never going to apply. Every attempt's error is still available in `attempts`.
    """

    result: CheckResult
    path: SplicePath
    cmd_text: str
    attempts: list[SpliceAttempt] = field(default_factory=list)

    @property
    def succeeded(self) -> bool:
        return self.result.status is CheckStatus.PASSED

    @property
    def retries_consumed(self) -> int:
        """Attempts beyond the first. 0 on the common path."""
        return max(len(self.attempts) - 1, 0)

    @property
    def secondary_details(self) -> list[str]:
        """Every non-winning attempt's error, for logging as secondary diagnostics."""
        return [f"{a.path.value}: {a.detail}" for a in self.attempts if a.status is not CheckStatus.PASSED]


@dataclass(frozen=True)
class FactResult:
    """The outcome of adjudicating one fact, of either mechanism. `status` is a
    `CheckStatus` for mechanism `decide` or a `ProofStatus` for mechanism `proof` -- which
    one it is tells you which mechanism produced this result, so no separate mechanism field
    is stored here."""

    fact_id: str
    status: CheckStatus | ProofStatus
    elapsed_s: float
    detail: str = ""
    raw_response: object | None = None

    @property
    def is_proof_mechanism(self) -> bool:
        return isinstance(self.status, ProofStatus)

    @property
    def certified(self) -> bool:
        """The fact held: PASSED (decide) or TRUE (proof)."""
        return self.status is CheckStatus.PASSED or self.status is ProofStatus.TRUE

    @property
    def is_unknown(self) -> bool:
        """Only possible for mechanism `proof`: both attempts (fact, negation) exhausted
        budget honestly. Never true for a `decide` result."""
        return self.status is ProofStatus.UNKNOWN

    @property
    def is_errored(self) -> bool:
        return self.status is CheckStatus.ERRORED or self.status is ProofStatus.ERRORED


@dataclass(frozen=True)
class ExcessiveUnknownFlag:
    """Raised (as data, not an exception) when too many of a candidate's proof-mechanism
    facts came back UNKNOWN. Per the schema: the cause is either a degenerate candidate or a
    defective task, and telling those apart is a human/agent judgment this flag surfaces,
    not one it makes."""

    unknown_count: int
    proof_fact_count: int
    threshold: float
    affected_fact_ids: list[str]

    @property
    def reason(self) -> str:
        pct = 100 * self.unknown_count / self.proof_fact_count
        return (
            f"{self.unknown_count}/{self.proof_fact_count} proof-mechanism facts UNKNOWN "
            f"({pct:.1f}% > {self.threshold * 100:.0f}% threshold): {self.affected_fact_ids}"
        )


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
    fact_results: list[FactResult] = field(default_factory=list)
    splice_outcome: SpliceOutcome | None = None
    """Which splice path won and what the retries cost (2026-08-04).

    `None` when the candidate was spliced from raw command text (`score_spliced_candidate`),
    where there is no body to rewrite and therefore no ladder to run. Populated by
    `score_candidate`. Stage B persists `splice_outcome.path.value` and `.retries_consumed`
    per candidate: a rescued candidate is a materially different observation from one that
    compiled plainly, and the rescue rate is itself a measurement of model output style.
    """

    @property
    def fidelity(self) -> float | None:
        """certified-passing / (total - UNKNOWN - ERRORED), per
        docs/design/task_schema_v1_1.md "Scoring semantics". `None` if there's nothing to
        score (inadmissible, no facts) or nothing resolved (every fact UNKNOWN/ERRORED) --
        a fraction with a zero denominator isn't a 0% or 100% score, it's not a score."""
        if not self.admissible or not self.fact_results:
            return None
        certified = sum(1 for r in self.fact_results if r.certified)
        unresolved = sum(1 for r in self.fact_results if r.is_unknown or r.is_errored)
        denominator = len(self.fact_results) - unresolved
        if denominator <= 0:
            return None
        return certified / denominator

    def excessive_unknown(self, threshold: float | None = None) -> ExcessiveUnknownFlag | None:
        """EXCESSIVE_UNKNOWN check: flags when UNKNOWNs exceed `threshold` (default
        `config.EXCESSIVE_UNKNOWN_THRESHOLD`, a dial not a schema commitment) of the
        candidate's proof-mechanism facts specifically -- decide-mechanism facts can't
        produce UNKNOWN, so they don't belong in this denominator. Returns `None` if there
        are no proof-mechanism facts at all, or if the rate is at or under threshold."""
        threshold = threshold if threshold is not None else cfg.EXCESSIVE_UNKNOWN_THRESHOLD
        proof_results = [r for r in self.fact_results if r.is_proof_mechanism]
        if not proof_results:
            return None
        unknown_results = [r for r in proof_results if r.is_unknown]
        if len(unknown_results) / len(proof_results) <= threshold:
            return None
        return ExcessiveUnknownFlag(
            unknown_count=len(unknown_results),
            proof_fact_count=len(proof_results),
            threshold=threshold,
            affected_fact_ids=[r.fact_id for r in unknown_results],
        )
