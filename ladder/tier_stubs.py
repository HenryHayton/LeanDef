"""Tier 5 interface stub -- tiers 3 (`ladder.tier3`) and 4 (`ladder.tier4`) are real as of
Session B (EC2 box). Tier 5 waits on Bedrock entitlement regardless of which session or
machine implements it (`docs/deferred.md`'s blocked-slice entry). It raises
`NotImplementedError` unconditionally; `ladder.adjudicate`'s loop catches that specifically and
treats it as "this tier isn't available yet," falling through to UNKNOWN rather than crashing.
"""

from ladder.budgets import LadderBudgets
from ladder.statuses import TierAttempt


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
