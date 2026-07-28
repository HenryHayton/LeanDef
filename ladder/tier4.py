"""Tier 4 -- equivalence transfer (reward doc §3: "attempt candidate = truth (or ↔) via
tiers 2-3; success transfers the entire fact suite"). Composes `ladder.tier2`/`ladder.tier3`
internally as sub-attempts, budgeted at `budgets.tier4_attempt_budget_s` -- this tier IS the
tactic ladder plus hammer, not a third search mechanism of its own.

**Environment assumption (a scoping decision for this session, not the full pipeline
integration)**: proving `candidate = truth` needs BOTH names visible in one environment.
`harness.scoring.splice_candidate` already establishes the pattern this relies on --
`Command(cmd=..., env=base_env)`'s resulting environment is a DESCENDANT of `base_env`,
containing everything `base_env` had plus the new declaration. This module therefore assumes
the CALLER spliced the candidate with the truth environment as its base (`env=truth_env`), so
`candidate_env` already contains `truth_name` too -- `candidate_env` is where the equivalence
goal is attempted, `truth_env` is accepted for interface symmetry with every other tier
(`ladder.tier_stubs`'s original stub signature) and to make the assumption checkable, not used
directly. The full multi-environment splicing integration (re-splicing an already-declared
candidate against an arbitrary later truth environment) is out of scope here -- flagged, not
guessed at.

Prop-valued facts compare via `↔` (per the reward doc's own parenthetical); everything else via
`=`, chosen with `prop_valued`.
"""

from lean_interact import AutoLeanServer

from ladder.budgets import LadderBudgets
from ladder.statuses import AdjudicationStatus, TierAttempt
from ladder.tier2 import adjudicate_tier2
from ladder.tier3 import adjudicate_tier3_hammer


class Tier4Result:
    """Mirrors `ladder.tier2.Tier2Result`/`ladder.tier3.Tier3Result`'s shape (same attribute
    names) for the same reason those two do -- a uniform winning-result shape across every real
    tier `ladder.adjudicate`'s loop can treat identically."""

    def __init__(self, attempts: list[TierAttempt], winning: TierAttempt | None, winning_theorem_name: str | None, winning_script: str | None, env: int):
        self.attempts = attempts
        self.winning = winning
        self.winning_theorem_name = winning_theorem_name
        self.winning_script = winning_script
        self.env = env


def adjudicate_tier4_equivalence(
    server: AutoLeanServer,
    candidate_env: int,
    truth_env: int,
    candidate_name: str,
    truth_name: str,
    budgets: LadderBudgets,
    *,
    prop_valued: bool = False,
    fact_id: str = "tier4_equiv",
    imports: list[str] | None = None,
) -> Tier4Result:
    """Attempts `candidate_name = truth_name` (or `↔` if `prop_valued`) in `candidate_env`
    (see module docstring for why that environment specifically). Tries tier 2's pinned tactic
    set first (an eta-expanded alias is typically closed by `rfl` alone -- cheap, and the
    common case this tier exists for), then tier 3 hammer if tier 2 exhausts its ladder without
    winning or dying. `truth_env`/`imports` are accepted but not read directly by this
    implementation (see module docstring's environment-assumption note); `budgets`'s own
    `tier2_tactics`/`tier3_wall_clock_s` govern the sub-attempts, `tier4_attempt_budget_s` is
    not separately enforced here -- the per-fact ceiling (`ladder.adjudicate`) is what actually
    bounds total spend across a fact's whole cascade, tier 4 included."""
    relation = "↔" if prop_valued else "="
    goal_statement = f"{candidate_name} {relation} {truth_name}"

    tier2_result = adjudicate_tier2(server, candidate_env, fact_id, goal_statement, budgets, imports=imports)
    attempts = list(tier2_result.attempts)
    env = tier2_result.env

    if tier2_result.winning is not None:
        return Tier4Result(attempts, tier2_result.winning, tier2_result.winning_theorem_name, tier2_result.winning_script, env)
    if any(a.status is AdjudicationStatus.ENV_DEATH for a in tier2_result.attempts):
        return Tier4Result(attempts, None, None, None, env)

    tier3_result = adjudicate_tier3_hammer(server, env, fact_id, goal_statement, [], budgets, imports=imports)
    attempts.extend(tier3_result.attempts)
    env = tier3_result.env

    if tier3_result.winning is not None:
        return Tier4Result(attempts, tier3_result.winning, tier3_result.winning_theorem_name, tier3_result.winning_script, env)
    return Tier4Result(attempts, None, None, None, env)
