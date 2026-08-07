"""The per-fact adjudication loop (reward doc §3). `adjudicate_fact` tries tiers in order per
the fact's mechanism: decide-mechanism -> tier 1 only; proof-mechanism -> tiers 2..5 as
available. Tiers 1-4 are real as of Session B; tier 5 is still an interface stub
(`ladder.tier_stubs`, waits on Bedrock entitlement regardless of session) -- its
`NotImplementedError` is caught and treated as "this tier isn't available yet," never a crash.

**Tier 4's scope in this loop is deliberately narrow.** The reward doc's tier 4 is a
CANDIDATE-level operation ("attempt candidate = truth... success transfers the entire fact
suite") -- a round driver would call it once per candidate, not once per fact. This function
adjudicates one fact at a time and has no such driver yet, so tier 4 is offered here only as
one more per-fact fallback attempt, and only when the caller supplies enough context to attempt
it (`truth_env`/`candidate_name`/`truth_name`, all optional, all-or-nothing) -- omitting them
(the default) simply skips tier 4 for that call, exactly as if it were still a stub. Whole-suite
transfer on a single tier-4 success is NOT implemented here -- that requires a round-level
driver this session doesn't build; flagged, not guessed at.

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

**Per-fact ceiling enforcement** (reward doc §7's "per-fact total wall-clock"; previously an
unaggregated gap, `docs/deferred.md`): elapsed wall-clock since the fact's own adjudication
began is checked at every tier boundary -- before tier 2 starts, and again before each
subsequent tier is attempted. Once `LadderBudgets.per_fact_total_wall_clock_s` is exceeded, no
further tier is attempted at all (not even a cheap/stub one): the fact returns UNKNOWN
immediately with `BUDGET_EXHAUSTED_MARKER` in `Adjudication.detail`. This is a hard boundary
check, not mid-tier preemption -- a single tier already running (e.g. tier 2's own tactic
ladder, or a real tier 3/4 call) is not interrupted partway through; the ceiling only ever
prevents the *next* tier from starting.
"""

import re
import time

from lean_interact import AutoLeanServer, Command

from harness.facts import Fact
from harness.repl import run_checked
from harness.results import CheckStatus
from ladder.axiom_audit import audit_proof_axioms
from ladder.budgets import DEFAULT_LADDER_BUDGETS, LadderBudgets, with_membership_tactics
from ladder.cache import CacheEntry, ProofScriptCache, replay, statement_hash, toolchain_pin
from ladder.statuses import Adjudication, AdjudicationStatus, ElaborationStatus, TierAttempt
from ladder.tier1 import adjudicate_tier1
from ladder.tier2 import adjudicate_tier2
from ladder.tier3 import adjudicate_tier3_hammer
from ladder.tier4 import adjudicate_tier4_equivalence
from ladder.tier_stubs import adjudicate_tier5_flagship

BUDGET_EXHAUSTED_MARKER = "BUDGET_EXHAUSTED"



# `example : <PROP> := by decide` -> `<PROP>`. Decide facts are stored as full runnable commands
# (schema v1.1 §3.1), but tier 2 declares its own theorem around a BARE Prop, so the fallback has
# to recover the proposition from the command.
_DECIDE_PROP_RE = re.compile(r"^\s*example\s*:\s*(?P<prop>.+?)\s*:=\s*by\s+decide\s*$", re.DOTALL)
_TASK_SYMBOL_RE = re.compile(r"(?<![A-Za-z0-9_.])(VTask\.[A-Za-z_][A-Za-z0-9_.']*)")


def decide_statement_to_prop(statement: str) -> str | None:
    m = _DECIDE_PROP_RE.match(statement or "")
    return m.group("prop").strip() if m else None


def _decide_fallback(server, env, fact, budgets, imports):
    """Escalate an UNDECIDABLE decide fact to tier 2. Returns `(TierAttempt|None, env)`.

    **Why this exists.** A decide fact returns UNKNOWN when the `Decidable` instance is missing or
    stuck -- which is exactly what a NONCOMPUTABLE candidate does to every one of its decide
    facts. Measured on the prelim run: one model emitted noncomputable definitions in 32% of
    candidates and lost its entire decide coverage as a result, while a model that reduced the
    same object to an existing computable primitive scored cleanly. The instrument was therefore
    rewarding algorithm-by-reduction over definition-by-characterization -- a bias about
    *answer shape*, not correctness.

    The proposition is still perfectly true or false; it just cannot be settled by kernel
    computation through this splice. Tier 2 can often settle it by proof instead, with the
    membership extension supplying the definition-unfolding tactics that recovered 4/5 of the
    pilot's residue.

    Soundness is unchanged: tier 2 only ever finds PROOFS, so this can turn UNKNOWN into
    CERTIFIED and nothing else. It can never manufacture a FAILED, so no candidate can be
    refuted by this path.
    """
    prop = decide_statement_to_prop(fact.statement)
    if prop is None:
        return None, env
    sym = _TASK_SYMBOL_RE.search(prop)
    b = with_membership_tactics(budgets, sym.group(1)) if sym else budgets
    result = adjudicate_tier2(server, env, f"{fact.id}_decidefallback", prop, b, imports=imports)
    return result.winning, result.env


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


def _budget_exhausted(start: float, budgets: LadderBudgets) -> bool:
    return time.perf_counter() - start >= budgets.per_fact_total_wall_clock_s


def _budget_exhausted_adjudication(
    fact: Fact, elaboration: ElaborationStatus, attempts: list[TierAttempt], budgets: LadderBudgets, start: float
) -> Adjudication:
    elapsed = time.perf_counter() - start
    return Adjudication(
        fact_id=fact.id, elaboration=elaboration, status=AdjudicationStatus.UNKNOWN, tier=None,
        script=None, axiom_closure=None, wall_clock_s=elapsed, attempts=attempts,
        detail=(
            f"{BUDGET_EXHAUSTED_MARKER}: per-fact wall-clock ceiling "
            f"({budgets.per_fact_total_wall_clock_s}s) exceeded -- no further tier attempted"
        ),
    )


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
    truth_env: int | None = None,
    candidate_name: str | None = None,
    truth_name: str | None = None,
    prop_valued: bool = False,
) -> tuple[Adjudication, int]:
    """Returns `(adjudication, current_env)` -- `current_env` may differ from the input `env`
    if tier 2's own recovery loop refreshed it; callers chaining multiple facts through the
    same environment MUST carry it forward (see `ladder.tier2`'s module docstring).

    `truth_env`/`candidate_name`/`truth_name` are optional and all-or-nothing: supply all three
    to make tier 4 available for this call (see module docstring for the scoping this implies),
    or omit them to skip tier 4 entirely."""
    tier4_available = truth_env is not None and candidate_name is not None and truth_name is not None
    start = time.perf_counter()

    if fact.mechanism == "decide":
        attempt = adjudicate_tier1(server, env, fact.statement, budgets)
        attempts_d = [attempt]
        # Decide-fallback: UNKNOWN means "not settleable by computation through this splice",
        # not "not settleable". ERRORED is broken machinery and is NOT escalated -- retrying a
        # broken splice as a proof goal just spends budget on the same breakage.
        if budgets.decide_fallback and attempt.status is AdjudicationStatus.UNKNOWN:
            won, env = _decide_fallback(server, env, fact, budgets, imports)
            if won is not None:
                attempts_d.append(won)
                attempt = won
        elapsed = time.perf_counter() - start
        decided = attempt.status in (AdjudicationStatus.CERTIFIED, AdjudicationStatus.FAILED)
        return (
            Adjudication(
                fact_id=fact.id,
                elaboration=ElaborationStatus.ELABORATES if decided else ElaborationStatus.UNKNOWN,
                status=attempt.status,
                tier=(attempt.tier if decided else None),
                script=fact.statement if attempt.status is AdjudicationStatus.CERTIFIED else None,
                axiom_closure=None,  # tier 1 is kernel computation, not an assembled proof term -- no axiom audit applies
                wall_clock_s=elapsed,
                attempts=attempts_d,
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

    if _budget_exhausted(start, budgets):
        return _budget_exhausted_adjudication(fact, elaboration, attempts, budgets, start), env

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

    # Tier 3 (real): hammer. Wrapped rather than early-returned -- tier 4 comes AFTER this in the
    # cascade, so returning here would silently disable the equivalence fast path too.
    if budgets.tier3_enabled:
        if _budget_exhausted(start, budgets):
            return _budget_exhausted_adjudication(fact, elaboration, attempts, budgets, start), env

        tier3_result = adjudicate_tier3_hammer(server, env, fact.id, canonical_statement, fact.anchors, budgets, imports=imports)
        attempts.extend(tier3_result.attempts)
        env = tier3_result.env

        if tier3_result.winning is not None:
            return (
                _audit_and_finalize(
                    fact, canonical_statement, 3, tier3_result.winning_theorem_name, tier3_result.winning_script,
                    env, server, budgets, cache, pin, attempts, elaboration, start,
                ),
                env,
            )
        if any(a.status is AdjudicationStatus.ENV_DEATH for a in tier3_result.attempts):
            elapsed = time.perf_counter() - start
            return (
                Adjudication(
                    fact_id=fact.id, elaboration=elaboration, status=AdjudicationStatus.ENV_DEATH, tier=None,
                    script=None, axiom_closure=None, wall_clock_s=elapsed, attempts=attempts,
                    detail="environment-death recovery exhausted its budget",
                ),
                env,
            )

    # Tier 4 (real, narrow scope -- see module docstring): only attempted if the caller
    # supplied enough context; otherwise falls through exactly as if it were still a stub.
    if tier4_available:
        if _budget_exhausted(start, budgets):
            return _budget_exhausted_adjudication(fact, elaboration, attempts, budgets, start), env

        tier4_result = adjudicate_tier4_equivalence(
            server, env, truth_env, candidate_name, truth_name, budgets,
            prop_valued=prop_valued, fact_id=fact.id, imports=imports,
        )
        attempts.extend(tier4_result.attempts)
        env = tier4_result.env

        if tier4_result.winning is not None:
            return (
                _audit_and_finalize(
                    fact, canonical_statement, 4, tier4_result.winning_theorem_name, tier4_result.winning_script,
                    env, server, budgets, cache, pin, attempts, elaboration, start,
                ),
                env,
            )
        if any(a.status is AdjudicationStatus.ENV_DEATH for a in tier4_result.attempts):
            elapsed = time.perf_counter() - start
            return (
                Adjudication(
                    fact_id=fact.id, elaboration=elaboration, status=AdjudicationStatus.ENV_DEATH, tier=None,
                    script=None, axiom_closure=None, wall_clock_s=elapsed, attempts=attempts,
                    detail="environment-death recovery exhausted its budget",
                ),
                env,
            )

    # Tier 5: still an interface stub (waits on Bedrock entitlement regardless of session).
    # NotImplementedError means "not available yet," not a crash.
    if _budget_exhausted(start, budgets):
        return _budget_exhausted_adjudication(fact, elaboration, attempts, budgets, start), env
    try:
        attempt = adjudicate_tier5_flagship(canonical_statement, fact.anchors, budgets)
        attempts.append(attempt)  # pragma: no cover -- unreachable this session (the stub always raises)
    except NotImplementedError:
        pass

    elapsed = time.perf_counter() - start
    return (
        Adjudication(
            fact_id=fact.id, elaboration=elaboration, status=AdjudicationStatus.UNKNOWN, tier=None,
            script=None, axiom_closure=None, wall_clock_s=elapsed, attempts=attempts,
            detail="no available tier discharged the goal within budget",
        ),
        env,
    )
