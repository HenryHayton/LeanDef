"""Tier 2 -- the pinned deterministic tactic set (reward doc §3: `rfl`, `omega`, `simp`,
`exact?`, `aesop`, plus the `norm_num`/`positivity` class). Extracted and adapted from
`miner.discharge`'s generic core (`attempt_statement`) -- that module's `Command`-per-tactic
loop, stop-at-first-success shape is the ancestor of `adjudicate_tier2` below (copy-adapted
per this task's own instruction, `miner/discharge.py` itself untouched).

**Reliability hardening (reward doc §10), and the design choice this session had to make:**
batch 4's own fix (`miner.discharge._attempt_statement_with_recovery`) reimports ONCE on
environment death and retries the whole statement -- if that one reimport doesn't itself
succeed, the caller gets back the same (possibly still-dead) environment id with no further
recovery attempted in that call. The reward doc names two acceptable fixes: heavy-tier
environment ISOLATION, or a BUDGETED recovery loop (more than one reimport attempt).

**This module chooses the budgeted recovery loop**, not isolation, for three reasons:
1. `AutoLeanServer` already self-heals at the process level (`is_alive()` check + restart,
   `harness.repl`'s own documented behavior) -- what batch 4's failure mode actually needed was
   a WARM-ENVIRONMENT-level retry budget, not a new process-isolation mechanism underneath one
   that already exists.
2. True per-heavy-tactic isolation (a dedicated second `AutoLeanServer` for `exact?`/`aesop`
   calls) costs a full cold Mathlib import (~1 minute, this project's own measured number) EVERY
   time it would be invoked, with no warm-spare pooling built this session -- prohibitively
   expensive at per-fact granularity for what recovery, when it works, actually costs (seconds:
   one `warm_import` call).
3. A budgeted loop directly fixes the DEMONSTRATED batch-4 failure (one reimport attempt was
   not enough) with the SAME mechanism this codebase already trusts elsewhere
   (`miner.verify.verify_all_with_recovery`, `miner.discharge._attempt_statement_with_recovery`)
   -- just budgeted (`LadderBudgets.env_death_max_recovery_attempts`, default 3) instead of
   single-shot. If recovery is STILL exhausted after the full budget, the tactic ladder for
   that fact stops immediately (the whole tier -- not just the current tactic -- reports
   ENV_DEATH; trying the remaining tactics against an environment that just needed 3 failed
   reimport attempts is not expected to fare better) and the refreshed-or-still-dead
   environment id is returned to the caller regardless, so the NEXT fact in a batch always
   gets whatever the current, real environment state is -- never silently poisoned the way
   batch 4's cascading 718-failure run was.

Heavy tactics (`exact?`, `aesop`, `TacticBudget.heavy`) are exactly where this recovery path is
expected to actually fire -- narrow, deterministic tactics essentially never crash an
environment -- but the recovery loop itself is not tactic-conditional: any tactic's attempt
that shows the "Unknown environment" signature gets the same budgeted recovery, since a shared
environment can in principle die from any REPL call, not only a heavy one.
"""

import re

from lean_interact import AutoLeanServer, Command

from harness import config as cfg
from harness.repl import run_checked, warm_import
from harness.results import CheckStatus
from ladder.budgets import LadderBudgets
from ladder.statuses import AdjudicationStatus, TierAttempt

# Same marker-text detection `miner.discharge`/`miner.verify` already use, duplicated rather
# than imported -- both of those are private implementation details of different modules, and
# this codebase's own established convention (`miner.discharge`'s module docstring gives the
# same reasoning for its own copy) is to copy small private detectors rather than reach across
# a module boundary for them.
_ENV_DEATH_MARKERS = ("Unknown environment", "unknown environment")


def _looks_like_env_death(detail: str) -> bool:
    return any(marker in detail for marker in _ENV_DEATH_MARKERS)


def _safe_theorem_name(fact_id: str, tactic: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_]", "_", f"{fact_id}_{tactic}")
    return f"__ladder_tier2_{safe}"


def _recover_environment(server: AutoLeanServer, imports: list[str] | None, budgets: LadderBudgets) -> int | None:
    """The budgeted recovery loop -- see module docstring for the design choice this
    implements. Returns the refreshed environment id, or `None` if every attempt in the
    budget failed."""
    for _ in range(budgets.env_death_max_recovery_attempts):
        reimport = warm_import(server, imports=imports, timeout=cfg.DEFAULT_WARMUP_TIMEOUT)
        if reimport.status is CheckStatus.PASSED:
            return reimport.env
    return None


def _run_tactic_with_recovery(
    server: AutoLeanServer, env: int, cmd: str, tactic_budget, budgets: LadderBudgets, *, imports: list[str] | None
) -> tuple[TierAttempt, int]:
    check = run_checked(server, Command(cmd=cmd, env=env), timeout=tactic_budget.timeout_s, retries=budgets.retry_on_timeout_attempts)

    if _looks_like_env_death(check.detail):
        recovered_env = _recover_environment(server, imports, budgets)
        if recovered_env is None:
            return (
                TierAttempt(tier=2, tactic=tactic_budget.tactic, status=AdjudicationStatus.ENV_DEATH, elapsed_s=check.elapsed_s, detail=check.detail),
                env,
            )
        env = recovered_env
        check = run_checked(server, Command(cmd=cmd, env=env), timeout=tactic_budget.timeout_s, retries=budgets.retry_on_timeout_attempts)
        if _looks_like_env_death(check.detail):
            return (
                TierAttempt(tier=2, tactic=tactic_budget.tactic, status=AdjudicationStatus.ENV_DEATH, elapsed_s=check.elapsed_s, detail=check.detail),
                env,
            )

    if check.status is CheckStatus.PASSED:
        status = AdjudicationStatus.CERTIFIED
        # The declare command itself opened a NEW environment (the one the theorem actually
        # exists in) -- confirmed empirically (scratchpad verification run, 2026-07-27): a
        # `#print axioms` against the PRE-declare env id fails with "Unknown constant", even
        # though the declare command itself reported PASSED. Every downstream consumer of a
        # CERTIFIED attempt (the axiom audit, cache replay, the next fact in a chained batch)
        # needs the POST-declare env, not the one this call started with.
        if check.env is not None:
            env = check.env
    elif check.status is CheckStatus.FAILED:
        # A tactic failing to close a goal is not evidence the goal is false (reward doc
        # §2.3) -- UNKNOWN for this attempt, never FAILED (see ladder.statuses's own note).
        status = AdjudicationStatus.UNKNOWN
    else:
        status = AdjudicationStatus.ERRORED
    return TierAttempt(tier=2, tactic=tactic_budget.tactic, status=status, elapsed_s=check.elapsed_s, detail=check.detail), env


class Tier2Result:
    """`attempts`: one per tactic tried, in order (for reporting -- "which tactics won, wall-
    clocks"). `winning`/`winning_theorem_name`/`winning_script` are set only when a tactic
    certified the goal; `winning_theorem_name` is the ALREADY-DECLARED theorem the caller can
    hand straight to `ladder.axiom_audit.audit_proof_axioms` -- tier 2 declares under a name
    directly (not an anonymous `example` re-declared later) specifically so the audit needs no
    second search over the same goal."""

    def __init__(self, attempts: list[TierAttempt], winning: TierAttempt | None, winning_theorem_name: str | None, winning_script: str | None, env: int):
        self.attempts = attempts
        self.winning = winning
        self.winning_theorem_name = winning_theorem_name
        self.winning_script = winning_script
        self.env = env


def adjudicate_tier2(
    server: AutoLeanServer,
    env: int,
    fact_id: str,
    canonical_statement: str,
    budgets: LadderBudgets,
    *,
    imports: list[str] | None = None,
) -> Tier2Result:
    """Try each tier-2 tactic, in order, against `canonical_statement` as a freshly-DECLARED
    theorem (not an anonymous goal); stop at the first that discharges it. `env` in the
    returned `Tier2Result` may differ from the input `env` if a death-and-recovery cycle fired
    -- callers MUST carry it forward to whatever comes next (the same discipline
    `miner.discharge`'s own `(result, env)` return shape already established; this module's
    contribution is budgeting that recovery, not the tuple-forwarding convention itself)."""
    attempts: list[TierAttempt] = []
    for tactic_budget in budgets.tier2_tactics:
        theorem_name = _safe_theorem_name(fact_id, tactic_budget.tactic)
        cmd = f"theorem {theorem_name} : {canonical_statement} := by {tactic_budget.tactic}"
        attempt, env = _run_tactic_with_recovery(server, env, cmd, tactic_budget, budgets, imports=imports)
        attempts.append(attempt)
        if attempt.status is AdjudicationStatus.CERTIFIED:
            return Tier2Result(attempts, attempt, theorem_name, f"by {tactic_budget.tactic}", env)
        if attempt.status is AdjudicationStatus.ENV_DEATH:
            return Tier2Result(attempts, None, None, None, env)
    return Tier2Result(attempts, None, None, None, env)
