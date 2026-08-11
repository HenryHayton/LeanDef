"""Tier 4 must certify `candidate = truth` for RECURSIVE definitions.

Acceptance case from the 32B corpus: a `Nat.choose` candidate that is character-for-character
Mathlib's own definition, which tier 4 nevertheless failed to certify (rfl / simp / aesop all
FAIL on an equality of two recursively-defined functions; it needs `funext` + induction).

The stakes are whole-suite: equivalence certification transfers every fact. In the scored corpus
all 27 certified candidates had zero unknowns, and `Nat.choose` had 16 admissible candidates with
zero certifications carrying 128 unknowns between them.
"""

from harness.results import CheckStatus
from harness.scoring import splice_candidate_declaration
from ladder.budgets import DEFAULT_LADDER_BUDGETS, equivalence_induction_tactics
from ladder.tier4 import adjudicate_tier4_equivalence
from scoring.samples import load_task

MATHLIB_IDENTICAL_CHOOSE = (
    "def VTask.choose : ℕ → ℕ → ℕ\n"
    "  | _, 0 => 1\n"
    "  | 0, _ + 1 => 0\n"
    "  | n + 1, k + 1 => VTask.choose n k + VTask.choose n (k + 1)"
)


def test_templates_are_appended_after_the_pinned_set_not_substituted():
    """Cheap-first ordering must hold: an eta-expanded alias still closes on `rfl`."""
    tpl = equivalence_induction_tactics("VTask.f", "Real.g")
    assert tpl, "expected a non-empty template family"
    assert all("funext" in t.tactic for t in tpl)
    assert any("generalizing" in t.tactic for t in tpl), "the Pascal-shaped recursion needs it"
    assert all("VTask.f" in t.tactic and "Real.g" in t.tactic for t in tpl), (
        "both names must be unfolded -- naming only the task symbol can stop at the alias"
    )


def test_recursive_candidate_identical_to_mathlib_now_certifies(mathlib_env):
    server, base_env = mathlib_env
    t = load_task("Nat.choose")
    outcome = splice_candidate_declaration(server, base_env, t["signature"],
                                           MATHLIB_IDENTICAL_CHOOSE)
    assert outcome.result.status is CheckStatus.PASSED, outcome.result.detail

    result = adjudicate_tier4_equivalence(
        server, outcome.result.env, base_env, t["signature"].name, t["truth_real_name"],
        DEFAULT_LADDER_BUDGETS, fact_id="equiv_acceptance", imports=t.get("imports"),
    )
    assert result.winning is not None, (
        "a candidate identical to Mathlib's own definition must certify as equivalent; "
        f"attempts tried: {[a.tactic for a in result.attempts]}"
    )
    assert result.winning_script, "the winning tactic must be recorded"
