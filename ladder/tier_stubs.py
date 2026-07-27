"""Tier 3/4/5 interface stubs -- Session A scope is clean interfaces only. Real implementations
are Session B's (tiers 3-4, on the EC2 box, per the reward doc's own tier split: tier 3 needs
the hammer/cvc5 toolchain only the EC2 environment has, `docs/ec2_runbook.md`) or later (tier 5
waits on Bedrock entitlement regardless of which session or machine implements it,
`docs/deferred.md`'s blocked-slice entry). Every function here raises `NotImplementedError`
unconditionally; `ladder.adjudicate`'s loop catches that specifically and treats it as "this
tier isn't available yet," falling through to the next tier (or to UNKNOWN) rather than
crashing -- Session A must be usable standalone without Session B landing first.
"""

from lean_interact import AutoLeanServer

from ladder.budgets import LadderBudgets
from ladder.statuses import TierAttempt


def adjudicate_tier3_hammer(
    server: AutoLeanServer,
    env: int,
    canonical_statement: str,
    anchors: list[str],
    budgets: LadderBudgets,
    *,
    imports: list[str] | None = None,
) -> TierAttempt:
    """Tier 3 -- hammer (LeanHammer, or Lean-auto + Duper with `anchors` as explicit premises;
    reward doc §3 names both configurations, the pilot decides which). Interface only.

    Signature notes, resolved at the interface level only -- actual verification is Session B's:

    - `anchors`: the fact's explicit-premise list (reward doc §3, tier 3) is present in the
      signature even though tier 3 doesn't run here, so `ladder.adjudicate`'s call site doesn't
      need to change shape when Session B fills this in.
    - `--load-dynlib`: `docs/deferred.md`'s own entry ("Ladder worker's Lean invocations must
      pass `--load-dynlib=<cvc5 .so path>`... Verify whether `LeanInteract`'s config surface
      supports injecting this flag") is NOT resolved here -- that verification needs a real
      hammer-capable EC2 environment this session doesn't have, and this session makes no
      network calls or EC2 changes by its own rules. What IS decided at the interface level:
      this function takes `server: AutoLeanServer` (matching every other tier), on the
      assumption that whatever `--load-dynlib` mechanism Session B finds gets threaded through
      `LeanREPLConfig`/`AutoLeanServer` CONSTRUCTION before this function is ever called, not
      as a per-call parameter here -- the same pattern `harness.repl` already uses for every
      other REPL-level configuration (project dir, memory guard, timeout). If Session B instead
      finds `LeanInteract` has no such injection point and must shell out to
      `lake env lean --load-dynlib=...` directly (bypassing `AutoLeanServer` for tier 3
      specifically), this interface will need to change -- flagged here, not guessed at.
    - Goal-file batching: `docs/ec2_runbook.md`'s smoke test runs one goal per `lake env lean`
      invocation; whether tier 3 batches multiple facts' goals into one hammer invocation (to
      amortize the premise-selection-server round trip) or stays one-goal-per-call is also
      Session B's call. This stub takes one `canonical_statement` -- the simpler single-goal
      shape -- with room for a sibling `adjudicate_tier3_hammer_batch` later if batching earns
      its complexity.
    """
    raise NotImplementedError(
        "tier 3 (hammer) needs the EC2 hammer toolchain (docs/ec2_runbook.md) -- Session B."
    )


def adjudicate_tier4_equivalence(
    server: AutoLeanServer,
    candidate_env: int,
    truth_env: int,
    candidate_name: str,
    truth_name: str,
    budgets: LadderBudgets,
) -> TierAttempt:
    """Tier 4 -- equivalence transfer (reward doc §3: "attempt candidate = truth (or ↔) via
    tiers 2-3; success transfers the entire fact suite"). Takes BOTH environments -- unlike
    every other tier, which only ever touches one environment at a time, the equivalence goal
    quantifies over the candidate's declaration and the truth's declaration simultaneously, so
    both must already be spliced/available before this is called. Interface only: real
    implementation composes tiers 2-3 as internal sub-attempts, which only matters once tier 3
    is real (Session B)."""
    raise NotImplementedError(
        "tier 4 (equivalence transfer) attempts tiers 2-3 internally -- needs a real tier 3 first (Session B)."
    )


def adjudicate_tier5_flagship(canonical_statement: str, anchors: list[str], budgets: LadderBudgets) -> TierAttempt:
    """Tier 5 -- Bedrock flagship, last resort (reward doc §6). Mirrors
    `bedrock.client.BedrockClient.send`'s own call shape (system/user message in, text out) at
    the PARAMETER level -- a system prompt would be a proof-writing instruction, the user
    message the goal plus `anchors` -- WITHOUT importing `bedrock` (this session's own rule: no
    `bedrock/` changes, no network calls). Whoever wires this in later constructs a real
    `BedrockClient` at the call site, not inside this function. Budget/cap enforcement
    (`budgets.tier5_max_calls_per_round`/`tier5_max_dollars_per_round`) is the CALLER's
    responsibility (a round-level driver, not `ladder.adjudicate`'s per-fact loop) -- this
    function's job is one fact, not round-level spend tracking."""
    raise NotImplementedError(
        "tier 5 (Bedrock flagship) waits on Bedrock entitlement (docs/deferred.md) -- not this session regardless."
    )
