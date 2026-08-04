"""The scoring verdict vocabulary, and the map from the ladder's vocabulary onto it.

**Three vocabularies meet here and none of them is allowed to leak.** `harness.results` has
`CheckStatus`/`ProofStatus`; `ladder.statuses` has `AdjudicationStatus` (CERTIFIED/FAILED/
UNKNOWN/ENV_DEATH/ERRORED) plus a separate `ElaborationStatus`. Neither is the right thing to
persist: the ladder's vocabulary is about *what the ladder did*, while a score record is about
*what we learned about the candidate*. Mapping at this boundary keeps both upstream vocabularies
free to grow without silently changing what a stored verdict means.

The mapping is deliberately lossy in one direction only: several ladder outcomes collapse to
ERROR, but nothing collapses INTO `FAIL`. `FAIL` is the strong claim -- this candidate is
refuted by this fact -- and after 2026-08-05 there is exactly one way to earn it (a tier-1
kernel-certified false).

**The mechanism invariant** (`check_mechanism_invariant`) is enforced in code rather than
documented and hoped for, because violating it silently corrupts every downstream ratio:

- a **decide** fact may only be PASS / FAIL / ERROR. It can never be UNKNOWN-by-exhaustion --
  `decide` either computes or it doesn't. (A missing `Decidable` instance now maps to UNKNOWN at
  tier 1; that is `unadjudicable`, carried as UNKNOWN, and the invariant permits it explicitly.)
- a **proof** fact may only be PASS / UNKNOWN / ERROR. It can never be FAIL, because a tactic
  failing to close a goal is not evidence the goal is false -- the ladder's founding doctrine.
"""

from enum import Enum

from ladder.statuses import AdjudicationStatus

DECIDE = "decide"
PROOF = "proof"


class Verdict(Enum):
    """What we learned about the candidate from one fact."""

    PASS = "pass"        # certified: the fact holds of this candidate
    FAIL = "fail"        # kernel-certified negative: the fact is false of this candidate
    UNKNOWN = "unknown"  # not adjudicable within budget, or untestable through this splice
    ERROR = "error"      # infrastructure failed; says nothing about the candidate

    @property
    def counts_in_denominator(self) -> bool:
        """Fidelity is `PASS / (PASS + FAIL)`. UNKNOWN and ERROR are excluded, per
        `docs/design/task_schema_v1_1.md`'s scoring semantics -- a fact we could not resolve is
        not a fact the candidate got wrong, and folding it in either way would be a claim we
        cannot support."""
        return self in (Verdict.PASS, Verdict.FAIL)


# Ladder outcome -> what it tells us about the candidate.
_MAP = {
    AdjudicationStatus.CERTIFIED: Verdict.PASS,
    AdjudicationStatus.FAILED: Verdict.FAIL,
    AdjudicationStatus.UNKNOWN: Verdict.UNKNOWN,
    AdjudicationStatus.ENV_DEATH: Verdict.ERROR,
    AdjudicationStatus.ERRORED: Verdict.ERROR,
}

# Outcomes worth one retry before being recorded: the machinery broke, which says nothing about
# the candidate, so a single repeat is cheap insurance against a transient. UNKNOWN is NOT here
# -- exhausting the tactic budget twice costs twice as much and tells us the same thing.
RETRYABLE = frozenset({AdjudicationStatus.ENV_DEATH, AdjudicationStatus.ERRORED})


def verdict_for(status: AdjudicationStatus) -> Verdict:
    """Map one ladder outcome. Unknown enum members fail loudly rather than defaulting: a new
    `AdjudicationStatus` silently becoming ERROR (or worse, FAIL) is exactly the kind of drift
    that produces confidently wrong numbers."""
    try:
        return _MAP[status]
    except KeyError:  # pragma: no cover -- guards a future enum addition
        raise ValueError(
            f"no verdict mapping for {status!r}; add it to scoring.verdicts._MAP deliberately "
            "rather than letting it default"
        ) from None


def check_mechanism_invariant(mechanism: str, verdict: Verdict) -> None:
    """Raise if `verdict` is impossible for `mechanism`. Called on every fact before it is
    written, so a mapping bug surfaces at the fact that caused it rather than as an inexplicable
    aggregate weeks later."""
    if mechanism == DECIDE:
        if verdict is Verdict.UNKNOWN:
            return  # untestable-through-this-splice; see the module docstring
        allowed = {Verdict.PASS, Verdict.FAIL, Verdict.ERROR}
    elif mechanism == PROOF:
        allowed = {Verdict.PASS, Verdict.UNKNOWN, Verdict.ERROR}
    else:
        raise ValueError(f"unknown fact mechanism {mechanism!r}")

    if verdict not in allowed:
        raise ValueError(
            f"mechanism {mechanism!r} may not produce verdict {verdict.value!r} "
            f"(allowed: {sorted(v.value for v in allowed)}). "
            "A proof fact reaching FAIL means something claimed a tactic failure as a refutation."
        )


def fidelity(verdicts: list[Verdict]) -> float | None:
    """`PASS / (PASS + FAIL)`, or `None` when nothing resolved.

    `None` rather than 0.0 deliberately: a candidate whose every fact came back UNKNOWN has not
    scored zero, it has not been scored at all, and averaging those two together downstream
    would be a category error."""
    denominator = sum(1 for v in verdicts if v.counts_in_denominator)
    if denominator == 0:
        return None
    return sum(1 for v in verdicts if v is Verdict.PASS) / denominator
