"""Adversarial and well-formed candidate tests for the Layer 0 admissibility gate
(`harness.admissibility`) and the timeout/watchdog layer (`harness.repl.run_checked`).

Uses the existing bare-Lean `lean_server` fixture (`tests/conftest.py`) -- none of these
scenarios need Mathlib, so the suite stays fast. A signature/body/facts triple ("double")
distinct from the archived tau probe is used deliberately: this task does not convert the
archived case into a fixture.

Note: `ℕ` (blackboard-bold) is a Mathlib notation, not core Lean -- without an import it
doesn't resolve to `Nat`. These tests use the ASCII `Nat` throughout, matching the existing
bare-Lean tests in `test_lean_repl.py`.
"""

from lean_interact import Command

from harness import Fact, PinnedSignature, score_candidate, score_spliced_candidate
from harness.admissibility import AdmissibilityFailure, check_admissibility
from harness.repl import run_checked
from harness.results import CheckStatus

DOUBLE = PinnedSignature(name="double", type_sig="Nat → Nat")
TRUE_BODY = "fun n => 2 * n"
FACTS = [
    Fact(id="double_1", type="casework", mechanism="decide", statement="example : double 1 = 2 := by decide"),
    Fact(id="double_2", type="casework", mechanism="decide", statement="example : double 2 = 4 := by decide"),
    Fact(id="double_5", type="casework", mechanism="decide", statement="example : double 5 = 10 := by decide"),
]

# `env=None` starts a fresh, isolated session per test -- nothing needs importing first for
# these bare-Lean scenarios, and no baseline axioms are expected without Mathlib.
BASE_ENV = None
NO_BASELINE = frozenset()


def test_well_formed_candidate_passes_gate_and_scores(lean_server):
    score = score_candidate(
        lean_server, BASE_ENV, DOUBLE, TRUE_BODY, FACTS, label="true", baseline_axioms=NO_BASELINE
    )
    assert score.admissible, score.admissibility_detail
    assert score.fidelity == 1.0


def test_sorry_candidate_is_rejected(lean_server):
    score = score_candidate(
        lean_server, BASE_ENV, DOUBLE, "sorry", FACTS, label="sorry", baseline_axioms=NO_BASELINE
    )
    assert not score.admissible
    assert score.admissibility_detail.startswith("sorry:")


def test_axiom_declaring_candidate_is_rejected(lean_server):
    """A candidate that declares a new axiom and routes the pinned def through it must be
    rejected. In the full splice-and-score pipeline this is caught by the shadowing check --
    declaring a new axiom necessarily adds a second top-level declaration alongside the
    pinned def (see `harness/admissibility.py`'s module docstring). The second half of this
    test exercises the axiom-detection logic in isolation (`splice_response=None` skips the
    declaration-shape check) to prove that check independently works too, not just that
    *something* in the gate happens to catch this candidate.
    """
    cmd_text = "axiom cheat_double : Nat → Nat\nnoncomputable def double : Nat → Nat := cheat_double"

    score = score_spliced_candidate(
        lean_server, BASE_ENV, cmd_text, DOUBLE, FACTS, label="axiom", baseline_axioms=NO_BASELINE
    )
    assert not score.admissible

    splice = run_checked(lean_server, Command(cmd=cmd_text, env=BASE_ENV, declarations=True), timeout=30.0)
    assert splice.status is CheckStatus.PASSED, splice.detail
    verdict = check_admissibility(
        lean_server, splice.env, DOUBLE, baseline_axioms=NO_BASELINE, splice_response=None
    )
    assert not verdict.passed
    assert verdict.failure is AdmissibilityFailure.NEW_AXIOM


def test_dependency_shadowing_candidate_is_rejected(lean_server):
    """A candidate that smuggles an extra top-level declaration alongside the pinned def --
    the mechanism by which a real dependency could be redefined -- must be rejected."""
    cmd_text = "def sneakyHelper : Nat := 0\ndef double : Nat → Nat := fun n => 2 * n"
    score = score_spliced_candidate(
        lean_server, BASE_ENV, cmd_text, DOUBLE, FACTS, label="shadow", baseline_axioms=NO_BASELINE
    )
    assert not score.admissible
    assert score.admissibility_detail.startswith("name_shadowed:")


def test_admissible_candidate_can_still_score_badly(lean_server):
    """A candidate that clears the gate but is simply wrong must be admissible with low
    fidelity, not rejected -- admissibility and fidelity are different questions."""
    score = score_candidate(
        lean_server, BASE_ENV, DOUBLE, "fun _ => 0", FACTS, label="junk", baseline_axioms=NO_BASELINE
    )
    assert score.admissible
    assert score.fidelity == 0.0


def test_expensive_check_errors_via_watchdog_instead_of_hanging(lean_server):
    """A deliberately expensive `decide`, given a short timeout, must come back ERRORED --
    not hang, and not silently count as FAILED. `∀ n < 500000` genuinely runs long rather
    than fast-failing on Lean's recursion-depth limit (verified empirically before writing
    this test -- a naive `∀ n < 10000000` hits `maxRecDepth` and errors in ~1s instead)."""
    result = run_checked(
        lean_server,
        Command(cmd="set_option maxRecDepth 4000000 in example : ∀ n < 500000, n + 0 = n := by decide"),
        timeout=5.0,
        retries=1,
    )
    assert result.status is CheckStatus.ERRORED
