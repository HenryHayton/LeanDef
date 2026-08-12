"""Enforce the suite-composition rules the fact-proposal prompt states.

The prompt calls the decide cap "hard" and the reject floor "hard", but a prompt cannot enforce
anything -- it only asks. Measured on the 3-task calibration (11 Aug 2026), asking was not
enough: `List.nextOr` came back with 10 decide facts against a cap of 6, and
`ArithmeticFunction.dirichletInverseFun` with 6 facts against a floor of 8. The reject floor
happened to hold on all three (2, 3, 5), but "happened to" is not a guarantee either.

So the caps are applied here, mechanically, after the model has proposed and before anything
ships.

TRIMMING KEEPS PROPOSAL ORDER. An earlier revision asked the model to label each decide fact
"boundary" or "interior" so the trim could drop the weakest first. That label was dropped
(operator decision, 12 Aug 2026: it is an oversimplification, and the 50-task run showed Sonnet
ignoring it entirely -- 0 of 44 decide facts carried one). The prompt now simply asks for
casework at important points rather than randomly chosen ones, and the trim keeps the first
`DECIDE_CAP` in proposal order, which is the model's own priority ordering.

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
        keep, drop = decide[:DECIDE_CAP], decide[DECIDE_CAP:]
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
