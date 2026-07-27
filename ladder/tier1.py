"""Tier 1 (decide) -- reward doc §3: "unchanged; reuses `harness/` as built." A thin wrapper
only: no new adjudication logic, just a projection of `harness.repl.run_checked`'s existing
three-way `CheckStatus` (PASSED/FAILED/ERRORED) onto the ladder's own status vocabulary
(`ladder.statuses.AdjudicationStatus`), so `ladder.adjudicate`'s loop has one uniform attempt
shape across every tier.
"""

from lean_interact import AutoLeanServer, Command

from harness.repl import run_checked
from harness.results import CheckStatus
from ladder.budgets import LadderBudgets
from ladder.statuses import AdjudicationStatus, TierAttempt


def adjudicate_tier1(server: AutoLeanServer, env: int, statement: str, budgets: LadderBudgets) -> TierAttempt:
    """`statement` is the full runnable decide-mechanism command (schema v1.1 §3.1's decide
    canonical form), run exactly as `harness.scoring.run_facts` already does for mechanism
    `decide` -- no behavior change, just the status projection. PASSED -> CERTIFIED (the
    statement computed to true); FAILED -> FAILED (computed to false -- a genuine, kernel-
    certified negative result, the one place in this ladder FAILED is produced); anything else
    -> ERRORED."""
    check = run_checked(server, Command(cmd=statement, env=env), timeout=budgets.tier1_timeout_s)
    if check.status is CheckStatus.PASSED:
        status = AdjudicationStatus.CERTIFIED
    elif check.status is CheckStatus.FAILED:
        status = AdjudicationStatus.FAILED
    else:
        status = AdjudicationStatus.ERRORED
    return TierAttempt(tier=1, tactic=None, status=status, elapsed_s=check.elapsed_s, detail=check.detail)
