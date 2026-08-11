"""Enforce the suite-composition rules the fact-proposal prompt states.

The prompt calls the decide cap "hard" and the reject floor "hard", but a prompt cannot enforce
anything -- it only asks. Measured on the 3-task calibration (11 Aug 2026), asking was not
enough: `List.nextOr` came back with 10 decide facts against a cap of 6, and
`ArithmeticFunction.dirichletInverseFun` with 6 facts against a floor of 8. The reject floor
happened to hold on all three (2, 3, 5), but "happened to" is not a guarantee either.

So the caps are applied here, mechanically, after the model has proposed and before anything
ships.

TRIMMING PREFERS BOUNDARY CHECKS. When a suite is over the decide cap, the facts dropped are the
INTERIOR ones first -- an interior arithmetic spot-check (`choose 10 3 = 120`) survives every
plausible misreading, because boundary and side-condition errors compute the interior correctly,
whereas `choose 0 0 = 1` is exactly where misreadings live. Unlabelled decide facts are treated
as interior: the prompt asks for the label, and an unlabelled fact is the one we know least
about.

The floor is NOT enforced by invention -- nothing here makes up facts. A suite under the floor
ships with `under_floor` recorded, so the batch report can show it rather than a silently short
suite looking identical to a full one.
"""

from dataclasses import dataclass, field

DECIDE_CAP = 6
REJECT_FLOOR = 2
SUITE_FLOOR = 8


@dataclass
class CompositionOutcome:
    kept: list = field(default_factory=list)
    dropped: list = field(default_factory=list)
    violations: list[str] = field(default_factory=list)
    trimmed_decide: int = 0

    @property
    def ok(self) -> bool:
        return not self.violations


def _is_reject(fact) -> bool:
    """Reject-shaped: the explicit label, or a negative statement. Both, because 42 of the 88
    reject-shaped facts in the authored corpus carried no polarity label at all and could only
    be found by looking at the statement."""
    if getattr(fact, "polarity", None) == "reject":
        return True
    stmt = getattr(fact, "statement", "") or ""
    return any(tok in stmt for tok in ("¬", "∉", "≠"))


def enforce(facts: list) -> CompositionOutcome:
    """Trim to the decide cap, then report floor violations. Never invents a fact."""
    out = CompositionOutcome()
    decide = [f for f in facts if getattr(f, "mechanism", None) == "decide"]
    other = [f for f in facts if getattr(f, "mechanism", None) != "decide"]

    if len(decide) > DECIDE_CAP:
        # Boundary-labelled first, then unlabelled/interior -- so the cap removes the least
        # discriminating checks rather than an arbitrary suffix.
        ranked = sorted(
            decide,
            key=lambda f: 0 if getattr(f, "boundary_vs_interior", None) == "boundary" else 1,
        )
        keep, drop = ranked[:DECIDE_CAP], ranked[DECIDE_CAP:]
        out.trimmed_decide = len(drop)
        out.dropped.extend(drop)
        decide = keep

    kept = [f for f in facts if f in decide or f in other]
    out.kept = kept

    n_reject = sum(1 for f in kept if _is_reject(f))
    if n_reject < REJECT_FLOOR:
        out.violations.append(f"reject_floor: {n_reject} < {REJECT_FLOOR}")
    if len(kept) < SUITE_FLOOR:
        out.violations.append(f"suite_floor: {len(kept)} < {SUITE_FLOOR}")
    return out
