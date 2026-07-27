"""The per-fact adjudication loop (reward doc §3). `adjudicate_fact` tries tiers in order per
the fact's mechanism: decide-mechanism -> tier 1 only; proof-mechanism -> tiers 2..5 as
available. Tiers 3-5 are interface stubs this session (`ladder.tier_stubs`), so a
proof-mechanism fact tier 2 can't discharge simply ends UNKNOWN, not an exception --
`NotImplementedError` from a stub tier is caught and treated as "this tier isn't available
yet," never a crash, so Session A is usable standalone without Session B landing first.

**Cache-first** (reward doc §3.2): every proof-mechanism fact is looked up before any tier
runs. A hit replays (never re-searches); a replay failure demotes the fact to UNKNOWN for this
call and flags the cache entry for re-search, then this SAME call still attempts a real search
below (a poisoned cache entry must not silently strand a fact as UNKNOWN forever) -- but the
FACT's own status for this call is still built from whatever the fresh search finds, exactly as
if there had been no cache entry at all.

**Axiom audit gates CERTIFIED** (reward doc §3.3): a tier claiming success is not trusted until
its declared theorem passes `ladder.axiom_audit.audit_proof_axioms`. An audit failure demotes
the fact to UNKNOWN, logged in the returned `Adjudication.detail` -- per the reward doc's own
rule ("A proof exceeding the permitted set fails certification... and is logged").

**The two-stage split** (reward doc §10) is `Adjudication.elaboration` (does the bare Prop
elaborate at all, via a `#check` probe with no proof attempt) versus `.status` (what the ladder
did with it once it does) -- recorded on every proof-mechanism fact regardless of outcome.
"""

import time

from lean_interact import AutoLeanServer, Command

from harness.facts import Fact
from harness.repl import run_checked
from harness.results import CheckStatus
from ladder.axiom_audit import audit_proof_axioms
from ladder.budgets import DEFAULT_LADDER_BUDGETS, LadderBudgets
from ladder.cache import CacheEntry, ProofScriptCache, replay, statement_hash, toolchain_pin
from ladder.statuses import Adjudication, AdjudicationStatus, ElaborationStatus, TierAttempt
from ladder.tier1 import adjudicate_tier1
from ladder.tier2 import adjudicate_tier2
from ladder.tier_stubs import adjudicate_tier3_hammer, adjudicate_tier4_equivalence, adjudicate_tier5_flagship


def _probe_elaboration(server: AutoLeanServer, env: int, canonical_statement: str, budgets: LadderBudgets) -> ElaborationStatus:
    """Stage one of the two-stage split (reward doc §10): does the bare Prop elaborate at all,
    independent of whether anything can prove it. `#check` is enough -- elaboration doesn't
    need a completed proof."""
    check = run_checked(server, Command(cmd=f"#check ({canonical_statement} : Prop)", env=env), timeout=budgets.tier1_timeout_s)
    if check.status is CheckStatus.PASSED:
        return ElaborationStatus.ELABORATES
    if check.status is CheckStatus.FAILED:
        return ElaborationStatus.DOES_NOT_ELABORATE
    return ElaborationStatus.UNKNOWN


def _audit_and_finalize(
    fact: Fact,
    canonical_statement: str,
    tier: int,
    theorem_name: str,
    script: str,
    env: int,
    server: AutoLeanServer,
    budgets: LadderBudgets,
    cache: ProofScriptCache | None,
    pin: str,
    attempts: list[TierAttempt],
    elaboration: ElaborationStatus,
    start: float,
) -> Adjudication:
    """A tier claims it discharged the goal (`theorem_name` is already declared in `env`) --
    audit before trusting it. Only on a passing audit does the fact certify and the cache
    write happen; an audit failure demotes to UNKNOWN, per the reward doc's own rule."""
    audit = audit_proof_axioms(server, env, theorem_name, timeout=budgets.tier1_timeout_s)
    elapsed = time.perf_counter() - start
    if not audit.passed:
        return Adjudication(
            fact_id=fact.id, elaboration=elaboration, status=AdjudicationStatus.UNKNOWN, tier=tier,
            script=None, axiom_closure=None, wall_clock_s=elapsed, attempts=attempts,
            detail=f"axiom audit failed: {audit.detail}",
        )

    axiom_closure = sorted(audit.axioms)
    if cache is not None:
        cache.put(CacheEntry(
            statement_hash=statement_hash(canonical_statement), toolchain_pin=pin, tier=tier,
            script=script, axiom_closure=axiom_closure, wall_clock_s=elapsed, canonical_statement=canonical_statement,
        ))
    return Adjudication(
        fact_id=fact.id, elaboration=elaboration, status=AdjudicationStatus.CERTIFIED, tier=tier,
        script=script, axiom_closure=axiom_closure, wall_clock_s=elapsed, attempts=attempts,
    )


def adjudicate_fact(
    fact: Fact,
    env: int,
    server: AutoLeanServer,
    budgets: LadderBudgets = DEFAULT_LADDER_BUDGETS,
    cache: ProofScriptCache | None = None,
    *,
    imports: list[str] | None = None,
) -> tuple[Adjudication, int]:
    """Returns `(adjudication, current_env)` -- `current_env` may differ from the input `env`
    if tier 2's own recovery loop refreshed it; callers chaining multiple facts through the
    same environment MUST carry it forward (see `ladder.tier2`'s module docstring)."""
    start = time.perf_counter()

    if fact.mechanism == "decide":
        attempt = adjudicate_tier1(server, env, fact.statement, budgets)
        elapsed = time.perf_counter() - start
        decided = attempt.status in (AdjudicationStatus.CERTIFIED, AdjudicationStatus.FAILED)
        return (
            Adjudication(
                fact_id=fact.id,
                elaboration=ElaborationStatus.ELABORATES if decided else ElaborationStatus.UNKNOWN,
                status=attempt.status,
                tier=1 if decided else None,
                script=fact.statement if attempt.status is AdjudicationStatus.CERTIFIED else None,
                axiom_closure=None,  # tier 1 is kernel computation, not an assembled proof term -- no axiom audit applies
                wall_clock_s=elapsed,
                attempts=[attempt],
            ),
            env,
        )

    # proof mechanism: cache first.
    canonical_statement = fact.statement
    pin = toolchain_pin()
    if cache is not None:
        entry = cache.get(canonical_statement, pin)
        if entry is not None:
            replay_check = replay(entry, server, env, timeout=budgets.tier1_timeout_s)
            if replay_check.status is CheckStatus.PASSED:
                elapsed = time.perf_counter() - start
                return (
                    Adjudication(
                        fact_id=fact.id, elaboration=ElaborationStatus.ELABORATES, status=AdjudicationStatus.CERTIFIED,
                        tier=entry.tier, script=entry.script, axiom_closure=entry.axiom_closure, wall_clock_s=elapsed,
                        attempts=[], from_cache=True,
                    ),
                    env,
                )
            cache.flag_for_research(entry)
            # falls through to a real search below -- see module docstring.

    elaboration = _probe_elaboration(server, env, canonical_statement, budgets)
    if elaboration is not ElaborationStatus.ELABORATES:
        elapsed = time.perf_counter() - start
        return (
            Adjudication(
                fact_id=fact.id, elaboration=elaboration, status=AdjudicationStatus.UNKNOWN, tier=None,
                script=None, axiom_closure=None, wall_clock_s=elapsed, attempts=[],
                detail="statement did not elaborate; no tier attempted",
            ),
            env,
        )

    attempts: list[TierAttempt] = []

    tier2_result = adjudicate_tier2(server, env, fact.id, canonical_statement, budgets, imports=imports)
    attempts.extend(tier2_result.attempts)
    env = tier2_result.env

    if tier2_result.winning is not None:
        return (
            _audit_and_finalize(
                fact, canonical_statement, 2, tier2_result.winning_theorem_name, tier2_result.winning_script,
                env, server, budgets, cache, pin, attempts, elaboration, start,
            ),
            env,
        )

    if any(a.status is AdjudicationStatus.ENV_DEATH for a in tier2_result.attempts):
        elapsed = time.perf_counter() - start
        return (
            Adjudication(
                fact_id=fact.id, elaboration=elaboration, status=AdjudicationStatus.ENV_DEATH, tier=None,
                script=None, axiom_closure=None, wall_clock_s=elapsed, attempts=attempts,
                detail="environment-death recovery exhausted its budget",
            ),
            env,
        )

    # Tiers 3-5: interface stubs this session. NotImplementedError means "not available yet,"
    # not a crash -- falls through to UNKNOWN exactly as if the tier had simply failed to
    # discharge the goal.
    for stub_call in (
        lambda: adjudicate_tier3_hammer(server, env, canonical_statement, fact.anchors, budgets, imports=imports),
        lambda: adjudicate_tier4_equivalence(server, env, env, "candidate", "truth", budgets),
        lambda: adjudicate_tier5_flagship(canonical_statement, fact.anchors, budgets),
    ):
        try:
            attempt = stub_call()
        except NotImplementedError:
            continue
        attempts.append(attempt)  # pragma: no cover -- unreachable this session (every stub raises)

    elapsed = time.perf_counter() - start
    return (
        Adjudication(
            fact_id=fact.id, elaboration=elaboration, status=AdjudicationStatus.UNKNOWN, tier=None,
            script=None, axiom_closure=None, wall_clock_s=elapsed, attempts=attempts,
            detail="no available tier discharged the goal within budget",
        ),
        env,
    )
