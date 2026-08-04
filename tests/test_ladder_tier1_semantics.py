"""Tier-1 decide semantics: what `FAILED` is allowed to mean (2026-08-05).

Before this, `ladder.tier1.adjudicate_tier1` mapped EVERY errored decide command to
`AdjudicationStatus.FAILED`, documented as "computed to false -- a genuine, kernel-certified
negative result". `harness.repl.run_checked` sets `CheckStatus.FAILED` whenever the command
produced errors, and a decide command errors for at least five distinct reasons. Probed against
live Mathlib (Lean v4.32.0), all five return `status = failed`:

| statement                            | Lean says                                    |
|--------------------------------------|----------------------------------------------|
| `(2:ℕ) + 2 = 5`                      | Tactic `decide` proved ... is false          |
| `∀ n : ℕ, n + 0 = n`                 | failed to synthesize / Decidable (...)       |
| `VTask.doesNotExist 1 = 1`           | Unknown identifier `...`                     |
| `Nat.factorial 2000 > 0`             | maximum recursion depth has been reached     |
| `(2:ℕ) + 2 = True`                   | failed to synthesize instance of type class  |

Only the first is evidence the proposition is false. The rest were being recorded as kernel
refutations of the candidate.

**Why this is a corpus-quality bug and not only a scoring bug**: the same tier-1 call adjudicates
facts during authoring validation, where a `Decidable`-synthesis failure would read as "the truth
definition refutes this fact" and drop a perfectly good fact from a suite.

**Why it bites candidates far harder than truth.** A truth splice is the real Mathlib definition,
whose `Decidable` instances resolve. A candidate may phrase the definition differently and fail
instance synthesis through the splice -- the exact failure `@[reducible]` was introduced to fix
for `Nat.ModEq`. Left unfixed, fidelity would be biased downward specifically for candidates that
phrase things unusually: the same differential-by-output-style problem Stage A fixed elsewhere.
"""

import pytest

from ladder.budgets import DEFAULT_LADDER_BUDGETS
from ladder.statuses import AdjudicationStatus
from ladder.tier1 import adjudicate_tier1, classify_decide_failure

# --- VERBATIM Lean v4.32.0 output, captured against live Mathlib -------------------------------

KERNEL_FALSE = "Tactic `decide` proved that the proposition\n  2 + 2 = 5\nis false"
KERNEL_FALSE_GCD = "Tactic `decide` proved that the proposition\n  Nat.gcd 12 8 = 5\nis false"
NO_DECIDABLE = (
    "failed to synthesize\n  Decidable (∀ (n : ℕ), n + 0 = n)\n\n"
    "Hint: Additional diagnostic information may be available using the "
    "`set_option diagnostics true` command."
)
NO_DECIDABLE_EXISTS = (
    "failed to synthesize\n  Decidable (∃ n, n > 5)\n\nHint: Additional diagnostic information "
    "may be available using the `set_option diagnostics true` command."
)
UNKNOWN_IDENT = "Unknown identifier `VTask.doesNotExist`"
UNKNOWN_CONST = "Unknown constant `Nat.noSuchFunction`"
RECURSION_DEPTH = (
    "maximum recursion depth has been reached\nuse `set_option maxRecDepth <num>` to increase "
    "limit\nuse `set_option diagnostics true` to get diagnostic information"
)
TYPE_CLASS_FAILURE = (
    "failed to synthesize instance of type class\n  HAdd ℕ ℕ Prop\n\nHint: Type class instance "
    "resolution failures can be inspected with the `set_option trace.Meta.synthInstance true` "
    "command.; Expected type must not contain metavariables\n  2 + 2 = True"
)
# Not reproduced on demand, but Lean's standard phrasing for the other computation blow-up.
DETERMINISTIC_TIMEOUT = "(deterministic) timeout at `whnf`, maximum number of heartbeats (200000) has been reached"


# --- the only route to FAILED -------------------------------------------------------------------


@pytest.mark.parametrize("detail", [KERNEL_FALSE, KERNEL_FALSE_GCD])
def test_decide_evaluating_the_proposition_false_is_the_only_route_to_failed(detail):
    assert classify_decide_failure(detail) is AdjudicationStatus.FAILED


def test_lowercase_and_untagged_phrasings_still_read_as_kernel_false():
    """Lean has reworded this before (`decide proved ...` -> ``Tactic `decide` proved ...``).
    Matching the stable middle of the sentence rather than its prefix keeps the ONE route to
    FAILED from silently closing on a version bump -- which would turn every real refutation
    into an ERROR and quietly destroy separation."""
    assert classify_decide_failure("decide proved that the proposition\n  1 = 2\nis false") is AdjudicationStatus.FAILED


# --- untestable-through-this-splice -> UNKNOWN ---------------------------------------------------


@pytest.mark.parametrize("detail", [NO_DECIDABLE, NO_DECIDABLE_EXISTS])
def test_missing_decidable_instance_is_unknown_not_failed(detail):
    """The fact is untestable through this splice. That is not evidence about the proposition,
    so it must not count against the candidate -- UNKNOWN is excluded from denominators."""
    assert classify_decide_failure(detail) is AdjudicationStatus.UNKNOWN


def test_a_different_failed_to_synthesize_is_not_mistaken_for_a_decidable_failure():
    """THE precision test. A type-class failure (`HAdd ℕ ℕ Prop`) shares the `failed to
    synthesize` prefix with the Decidable case but means something else entirely -- a malformed
    statement, i.e. broken machinery. Matching on the prefix alone would misclassify it."""
    assert classify_decide_failure(TYPE_CLASS_FAILURE) is AdjudicationStatus.ERRORED


# --- broken machinery -> ERRORED ------------------------------------------------------------------


@pytest.mark.parametrize("detail", [UNKNOWN_IDENT, UNKNOWN_CONST])
def test_unknown_identifier_is_errored(detail):
    """A broken splice, not a refutation. Retryable, and reported."""
    assert classify_decide_failure(detail) is AdjudicationStatus.ERRORED


@pytest.mark.parametrize("detail", [RECURSION_DEPTH, DETERMINISTIC_TIMEOUT])
def test_computation_blowups_are_errored(detail):
    assert classify_decide_failure(detail) is AdjudicationStatus.ERRORED


# --- the default must not be FAILED ---------------------------------------------------------------


@pytest.mark.parametrize(
    "detail",
    ["some error Lean has never emitted before", "", "   ", "a wild new diagnostic from Lean v5"],
)
def test_unrecognised_errors_default_to_errored_never_failed(detail):
    """FAILED is the strong claim -- it asserts a kernel-certified negative -- so it requires
    POSITIVE evidence. Anything unrecognised is broken machinery until proven otherwise. This
    inverts the old default, which was to call everything a refutation."""
    assert classify_decide_failure(detail) is AdjudicationStatus.ERRORED


# --- end-to-end through adjudicate_tier1, against live Mathlib ------------------------------------


def test_true_statement_certifies(mathlib_env):
    server, env = mathlib_env
    attempt = adjudicate_tier1(server, env, "example : (2:ℕ) + 2 = 4 := by decide", DEFAULT_LADDER_BUDGETS)
    assert attempt.status is AdjudicationStatus.CERTIFIED


def test_false_statement_is_a_real_kernel_refutation(mathlib_env):
    server, env = mathlib_env
    attempt = adjudicate_tier1(server, env, "example : (2:ℕ) + 2 = 5 := by decide", DEFAULT_LADDER_BUDGETS)
    assert attempt.status is AdjudicationStatus.FAILED


def test_undecidable_proposition_is_unknown_against_real_lean(mathlib_env):
    """The regression that matters: this used to be recorded as a refutation."""
    server, env = mathlib_env
    attempt = adjudicate_tier1(server, env, "example : ∀ n : ℕ, n + 0 = n := by decide", DEFAULT_LADDER_BUDGETS)
    assert attempt.status is AdjudicationStatus.UNKNOWN, attempt.detail


def test_broken_splice_reference_is_errored_against_real_lean(mathlib_env):
    server, env = mathlib_env
    attempt = adjudicate_tier1(
        server, env, "example : VTask.doesNotExist 1 = 1 := by decide", DEFAULT_LADDER_BUDGETS
    )
    assert attempt.status is AdjudicationStatus.ERRORED, attempt.detail


def test_recursion_blowup_is_errored_against_real_lean(mathlib_env):
    server, env = mathlib_env
    attempt = adjudicate_tier1(
        server, env, "example : Nat.factorial 2000 > 0 := by decide", DEFAULT_LADDER_BUDGETS
    )
    assert attempt.status is AdjudicationStatus.ERRORED, attempt.detail


def test_a_healthy_true_statement_is_unaffected_by_the_classifier(mathlib_env):
    """The classifier only ever sees `CheckStatus.FAILED`. A PASSED check must still certify,
    and an infrastructure `CheckStatus.ERRORED` (timeout, dead REPL) has no Lean message to
    read and short-circuits to ERRORED without consulting it."""
    server, env = mathlib_env
    attempt = adjudicate_tier1(server, env, "example : (3:ℕ) * 3 = 9 := by decide", DEFAULT_LADDER_BUDGETS)
    assert attempt.status is AdjudicationStatus.CERTIFIED
    assert attempt.detail == ""


# --- the stuck-instance sibling (found by integration, 2026-08-05) --------------------------------

STUCK_DECIDABLE = (
    "Tactic `decide` failed for proposition\n  VTask.clog 2 8 = 3\nbecause its `Decidable` instance\n"
    "  instDecidableEqNat (VTask.clog 2 8) 3\ndid not reduce to `isTrue` or `isFalse`.\n\n"
    "After unfolding the instances `instDecidableEqBool`, `instDecidableEqNat`, `Bool.decEq`, "
    "`Classical.propDecidable`, `Nat.decEq`, and `Nat.decLe`, reduction got stuck at the "
    "`Decidable` instance\n  match h : (VTask.clog 2 8).beq 3 with\n  | true => isTrue ⋯\n"
    "  | false => isFalse ⋯"
)


def test_a_stuck_decidable_instance_is_unknown_not_errored():
    """A NONCOMPUTABLE candidate (`sInf`, `Classical.propDecidable`) type-checks and HAS a
    `Decidable` instance, but the instance cannot evaluate. Semantically identical to a missing
    one: untestable through this splice, no evidence about the proposition, and no amount of
    retrying will change it.

    Found by the Stage B smoke, not by the original probe -- 14 facts on one real candidate were
    landing in the ERRORED default, mis-reported as broken machinery and burning a retry each.
    """
    assert classify_decide_failure(STUCK_DECIDABLE) is AdjudicationStatus.UNKNOWN


def test_the_stuck_marker_does_not_swallow_a_genuine_refutation():
    """Precision: a kernel-false verdict must still win, since both mention `decide`."""
    assert classify_decide_failure(KERNEL_FALSE) is AdjudicationStatus.FAILED
