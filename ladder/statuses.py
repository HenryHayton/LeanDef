"""Status vocabulary for the adjudication ladder (reward doc §3, §10).

Per the reward doc's reliability requirement (§10), environment death is recorded as its own
status, distinct from FAILED/UNKNOWN: "a death is an infrastructure event, not evidence about
the fact." ERRORED is kept separate again from ENV_DEATH: ENV_DEATH is specifically the "Unknown
environment" signature this codebase already recognizes (`miner.verify`/`miner.discharge`'s own
duplicated detector, mirrored in `ladder.tier2`); ERRORED covers every other infrastructure
failure (a REPL timeout that isn't env death, an unparseable response, ...).

The two-stage split reward doc §10 also requires ("does the goal elaborate? / what does the
ladder do with it once it does") is `Adjudication.elaboration` (stage one) versus `.status`
(stage two) -- two independent fields on the same record, not folded into one vocabulary.
"""

from dataclasses import dataclass, field
from enum import Enum


class AdjudicationStatus(Enum):
    CERTIFIED = "certified"  # some tier proved the fact
    FAILED = "failed"        # a tier proved the fact's NEGATION -- tier-1 decide only, in
    # practice: a decide-mechanism statement computing to false IS a genuine kernel-certified
    # negative result. Proof-mechanism tiers (2+) never produce this status in this session's
    # ladder -- a tactic failing to close a goal is not evidence the goal is false (reward doc
    # §2.3: "the ladder only ever finds proofs, it never adjudicates by opinion"), so a
    # tier-2 tactic that doesn't discharge the goal is UNKNOWN for that attempt, not FAILED.
    UNKNOWN = "unknown"      # every available tier exhausted its budget without a verdict
    ENV_DEATH = "env_death"  # the shared REPL environment died and recovery exhausted its budget
    ERRORED = "errored"      # any other infrastructure failure


class ElaborationStatus(Enum):
    ELABORATES = "elaborates"
    DOES_NOT_ELABORATE = "does_not_elaborate"
    UNKNOWN = "unknown"  # the elaboration probe itself errored -- could not be determined


@dataclass(frozen=True)
class TierAttempt:
    """One tier's (or, within tier 2, one tactic's) attempt at discharging a fact."""

    tier: int
    tactic: str | None  # the specific tactic within tier 2; None for tiers 1, 3-5
    status: AdjudicationStatus
    elapsed_s: float
    detail: str = ""


@dataclass(frozen=True)
class Adjudication:
    """The ladder's full outcome for one fact: the two-stage split (reward doc §10) plus the
    ladder result. `script`/`axiom_closure` are populated only when `status is CERTIFIED`
    (reward doc §3.2's cache record shape; `axiom_closure` per §3.3's audit)."""

    fact_id: str
    elaboration: ElaborationStatus
    status: AdjudicationStatus
    tier: int | None  # the tier that produced `status`; None when no tier reached a verdict
    script: str | None
    axiom_closure: list[str] | None
    wall_clock_s: float
    attempts: list[TierAttempt] = field(default_factory=list)
    detail: str = ""
    from_cache: bool = False
