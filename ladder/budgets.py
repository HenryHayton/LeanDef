"""Unified ladder-budget configuration (reward doc §7): "One configuration object governs all
ladder execution... It replaces both `harness.config.PROOF_TIMEOUT`... and generalizes the
miner's `DISCHARGE_*` dials." `harness.config.PROOF_TIMEOUT` is retired in the same pass this
module lands (see `docs/deferred.md`'s entry, now marked done).

`miner.config`'s own `DISCHARGE_*`/`TACTIC_LADDER` dials are DELIBERATELY untouched --
instrument-scoped per the reward doc's own text ("which remain scoped to the measurement
instrument until the instrument is retired into the tier-2 rung"), not reused here even though
the tactic set overlaps: this module's tier-2 tactic set is a superset (adds the
`norm_num`/`positivity` class the reward doc names) with its own per-tactic budgets, tuned for
real discharge rather than a corpus-wide measurement sweep.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TacticBudget:
    tactic: str
    timeout_s: float
    heavy: bool = False  # exact?/aesop -- genuine proof search, the reward doc §10 reliability
    # requirement's named risk for environment death; see ladder.tier2's recovery loop.


# Order matters (mirrors miner.config.TACTIC_LADDER's own stated ordering philosophy): cheapest/
# most-specific first, broader automation next, the two search-based (heavy) tactics last.
DEFAULT_TIER2_TACTICS: tuple[TacticBudget, ...] = (
    TacticBudget("rfl", 5.0),
    TacticBudget("omega", 10.0),
    TacticBudget("norm_num", 10.0),
    TacticBudget("positivity", 10.0),
    TacticBudget("simp", 15.0),
    TacticBudget("exact?", 30.0, heavy=True),
    TacticBudget("aesop", 30.0, heavy=True),
)


@dataclass(frozen=True)
class LadderBudgets:
    """One object, read by every tier this session builds AND the two (tier 3, 5) it only
    stubs -- reward doc §7's "the defaults live in one config file the EC2 worker and the Mac
    replay path both read." Tier 3/4/5 fields are configuration only, unused until Session B
    (tier 3/4, on EC2) or Bedrock entitlement (tier 5) respectively.
    """

    # Tier 1 (decide). Deliberately its own value, not imported from `harness.config
    # .DECIDE_TIMEOUT` -- a config module importing another config module for one constant is
    # exactly the kind of coupling this unification is supposed to remove; restated here as
    # this ladder's own number (currently equal, not entangled).
    tier1_timeout_s: float = 60.0

    # Tier 2 (pinned tactic set).
    tier2_tactics: tuple[TacticBudget, ...] = DEFAULT_TIER2_TACTICS

    # Tier 3 (hammer) -- config only, unused until Session B (EC2).
    tier3_wall_clock_s: float = 60.0
    tier3_premise_count: int = 32

    # Tier 4 (equivalence transfer) -- config only, unused until Session B.
    tier4_attempt_budget_s: float = 60.0

    # Tier 5 (Bedrock flagship) -- config only, unused until Bedrock entitlement lands and a
    # later session wires it in. 0 means "not enabled" (a positive cap must be set deliberately
    # before tier 5 can ever run, not a default that silently permits spend).
    tier5_max_calls_per_round: int = 0
    tier5_max_dollars_per_round: float = 0.0

    # Per-fact ceiling across every tier attempted for that fact, regardless of mechanism.
    per_fact_total_wall_clock_s: float = 300.0

    # Retry-on-timeout: a genuinely slow (not dead) attempt gets one more try before being
    # counted against the fact. Threaded straight through to `harness.repl.run_checked`'s own
    # `retries=` parameter -- grounded in a real, measured number, not a guess:
    # `docs/ec2_runbook.md`'s hammer smoke test recorded ONE goal timing out at the full 60s
    # budget on one run and proving in 6.5s on an immediate repeat -- roughly 9x variance, no
    # other change -- "don't treat a single timeout as a hard failure without at least one
    # retry" is that section's own conclusion, generalized here to the whole ladder.
    retry_on_timeout_attempts: int = 1

    # Environment-death recovery (reward doc §10): a BUDGETED loop, not batch-4's single retry.
    # See `ladder.tier2`'s module docstring for the chosen design and its justification.
    env_death_max_recovery_attempts: int = 3


DEFAULT_LADDER_BUDGETS = LadderBudgets()
