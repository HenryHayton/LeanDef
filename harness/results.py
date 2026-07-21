"""Result types shared across the verifier package.

Status vocabulary is per-mechanism, per `docs/design/task_schema_v1.md` "Scoring semantics"
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

    @property
    def fidelity(self) -> float | None:
        """certified-passing / (total - UNKNOWN - ERRORED), per
        docs/design/task_schema_v1.md "Scoring semantics". `None` if there's nothing to
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
