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

from dataclasses import dataclass, replace


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

    # Tier 3 (hammer).
    #
    # `tier3_enabled` is a real switch, not a reliance on the import being missing. Without
    # `$SCORING_EXTRA_IMPORTS` the `hammer` tactic is simply unknown, so the attempt fails in
    # ~0ms -- which looks like "the hammer tried and lost" in the attempt log when in fact it was
    # never available. Turning it off explicitly keeps that distinction honest, and saves a REPL
    # round-trip per fact on every run that has no Hammer build (e.g. the laptop).
    tier3_enabled: bool = True
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

    # Decide-fallback (2026-08-07): escalate an UNKNOWN decide fact to tier 2 rather than
    # writing it off. UNKNOWN there means the `Decidable` instance is missing or stuck -- the
    # signature of a NONCOMPUTABLE candidate -- so without this the instrument silently rewards
    # algorithm-by-reduction over definition-by-characterization. Tier 2 only finds proofs, so
    # this can only ever turn UNKNOWN into CERTIFIED; it cannot refute anything.
    decide_fallback: bool = True


DEFAULT_LADDER_BUDGETS = LadderBudgets()


# Membership-shaped extension (adopted 2026-08-06 after the Stage C pilot's follow-up probe).
#
# The pilot discharged 14/14 global facts and 1/6 membership facts. The global successes were
# largely `exact?` finding the fact's ANCHOR THEOREM on Mathlib's shelf -- a lookup, not a proof
# search. Membership facts are bespoke concrete claims with no library twin, so lookup cannot
# help them: they need the definition UNFOLDED and the resulting concrete goal discharged.
#
# Re-running the five non-discharges with unfolding tactics recovered 4/5, every one via the
# same shape -- `simp [<task symbol>, <real name>]` -- in ~0.6 s for all five. So the membership
# gap was never a proof-search deficiency; the tactic set simply never unfolded the definition.
#
# BOTH names are unfolded because the splice is `@[reducible] def VTask.X := _root_.Real`: naming
# only the task symbol can resolve to the alias without reaching the real definition's body.
#
# Built per fact rather than pinned globally, since the symbols differ per task. Appended AFTER
# the standard set so the cheap pinned tactics still run first and nothing already working
# changes order.
def equivalence_induction_tactics(
    task_symbol: str, real_name: str, mathlib_name: str | None = None, max_args: int = 3
) -> tuple[TacticBudget, ...]:
    """Templates for `VTask.X = Mathlib.X` between two RECURSIVE definitions.

    Tier 4 previously offered only tier 2's pinned set then hammer. None of those can prove an
    equality of functions defined by recursion: it needs `funext` to get to a pointwise goal and
    then induction aligned with the recursion. Measured (11 Aug 2026) on a `Nat.choose` candidate
    that is character-for-character Mathlib's:

        rfl                                   FAILED   <- tier 4's first attempt
        simp [VTask.choose, Nat.choose]       FAILED
        aesop                                 FAILED
        funext n k; induction n generalizing k …   PASSED

    That mattered enormously: equivalence certification transfers the WHOLE fact suite, and all
    27 equivalence-certified candidates in the corpus had zero unknowns while all 731 unknowns
    sat in the 189 non-certified ones. `Nat.choose` alone had 16 admissible candidates, none
    certified, carrying 128 unknowns.

    A small template family, not a bespoke prover: `funext` over 1..max_args arguments, with and
    without `generalizing`, closed by `simp` over both definitions. `generalizing` matters when
    the recursion moves the later argument (Pascal's rule recurses on both), which plain
    `induction` cannot express.
    """
    # `real_name` here is the TRUTH ALIAS (`VTruth.X`), which is `@[reducible] def VTruth.X :=
    # Mathlib.X`. Unfolding it reaches `Mathlib.X` but NOT `Mathlib.X`'s equation lemmas, which is
    # what an induction proof actually needs -- measured: every template failed on the
    # Mathlib-identical Nat.choose until the real Mathlib name was added to the simp set.
    names = ", ".join(n for n in (task_symbol, real_name, mathlib_name) if n)
    out: list[TacticBudget] = []
    for n in range(1, max_args + 1):
        vs = " ".join(f"a{i}" for i in range(n))
        out.append(TacticBudget(f"funext {vs} <;> simp [{names}]", 15.0))
    out.append(TacticBudget(
        f"funext a0; induction a0 <;> simp_all [{names}]", 30.0, heavy=True))
    for n in range(2, max_args + 1):
        vs = [f"a{i}" for i in range(n)]
        head, rest = vs[0], " ".join(vs[1:])
        out.append(TacticBudget(
            f"funext {' '.join(vs)}; induction {head} generalizing {rest} <;> "
            f"simp_all [{names}]", 45.0, heavy=True))
        # `induction` on the first argument is not enough when the definition also matches on a
        # LATER one: after `induction a0`, `choose (n+1) a1` is still stuck until `a1` is split.
        # Measured -- the four-clause `Nat.choose` needs exactly this and the plain form above
        # fails on it.
        out.append(TacticBudget(
            f"funext {' '.join(vs)}; induction {head} generalizing {rest} <;> "
            f"cases {vs[1]} <;> simp_all [{names}]", 45.0, heavy=True))
    return tuple(out)


def with_global_unfolding_tactics(
    budgets: LadderBudgets, task_symbol: str, real_name: str | None = None
) -> LadderBudgets:
    """`budgets` with INTROS-LED definition-unfolding tactics appended, for global facts.

    Separate from `with_membership_tactics` for one measured reason: a global fact is
    ∀-quantified, and `simp [VTask.X]` on an unopened `∀` never reaches the body. The membership
    set omits `intros` because membership facts are already closed propositions.

    Measured on `∀ n, VTask.choose n 0 = 1` against a candidate that is character-for-character
    Mathlib's `Nat.choose` (11 Aug 2026):

        by simp                              FAILED   <- tier 2's pinned set
        by aesop                             FAILED   <- tier 2's pinned set
        by intros <;> rfl                    FAILED   <- unfolding alone is not enough
        by intros <;> simp [VTask.choose]    PASSED

    `rfl` fails because the three overlapping clauses compile to a nested matcher, so
    `choose n 0` cannot reduce until `n` is in weak-head normal form -- `simp` does that case
    split, bare unfolding does not. The `rename_i`/`cases` variant is kept as a deeper fallback
    for goals where simp's own splitting is not enough.
    """
    names = task_symbol if not real_name else f"{task_symbol}, {real_name}"
    extension = (
        TacticBudget(f"intros <;> simp [{names}]", 15.0),
        TacticBudget(f"intros <;> simp_all [{names}]", 15.0),
        TacticBudget(f"intros <;> simp [{names}] <;> omega", 15.0),
        TacticBudget(f"unfold {task_symbol} <;> intros <;> rfl", 10.0),
        TacticBudget(f"intros <;> rename_i n <;> cases n <;> simp [{names}]", 20.0, heavy=True),
        TacticBudget(f"intros <;> simp only [{names}] <;> aesop", 30.0, heavy=True),
    )
    return replace(budgets, tier2_tactics=budgets.tier2_tactics + extension)


def with_membership_tactics(
    budgets: LadderBudgets, task_symbol: str, real_name: str | None = None
) -> LadderBudgets:
    """`budgets` with definition-unfolding tactics appended to its tier-2 set."""
    names = task_symbol if not real_name else f"{task_symbol}, {real_name}"
    extension = (
        TacticBudget(f"simp [{names}]", 15.0),
        TacticBudget(f"simp [{names}] <;> omega", 15.0),
        TacticBudget(f"simp [{names}] <;> decide", 15.0),
        TacticBudget("tauto", 10.0),
        TacticBudget(f"constructor <;> simp [{names}]", 15.0),
        TacticBudget(f"simp only [{names}] <;> aesop", 30.0, heavy=True),
    )
    return replace(budgets, tier2_tactics=budgets.tier2_tactics + extension)
