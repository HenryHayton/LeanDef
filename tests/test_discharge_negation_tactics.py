"""Reject facts must be discharged with NEGATION tactics; non-reject facts unchanged.

§4 of the 13 Aug handoff: all 75 uncertified reject facts in the 200-task corpus are
proof-mechanism (decide rejects certify at 98%, proof rejects at 51%), because the discharge step
pointed the FORWARD tier-2 set at goals that are negations. `NEGATION_TACTICS` existed in this
module throughout and was never used by discharge.

The byte-identical regression on non-reject facts is the load-bearing test here: this change must
not alter which tactic wins on anything that already discharged.
"""

from dataclasses import dataclass

from authoring.fact_validation import (NEGATION_TACTICS, _is_reject_shaped,
                                       discharge_budgets_for)
from ladder.budgets import DEFAULT_LADDER_BUDGETS


@dataclass
class F:
    id: str = "f"
    mechanism: str = "proof"
    statement: str = "∀ n, P n"
    polarity: str | None = None
    anchors: tuple = ()


def test_non_reject_discharge_budgets_are_byte_identical():
    b = discharge_budgets_for(F(), DEFAULT_LADDER_BUDGETS)
    assert b is DEFAULT_LADDER_BUDGETS
    assert b.tier2_tactics == DEFAULT_LADDER_BUDGETS.tier2_tactics


def test_reject_fact_gets_negation_tactics_first():
    b = discharge_budgets_for(F(polarity="reject"), DEFAULT_LADDER_BUDGETS)
    assert b.tier2_tactics[:len(NEGATION_TACTICS)] == NEGATION_TACTICS, (
        "negation tactics must run BEFORE the forward set"
    )


def test_forward_set_is_preserved_after_the_negation_set():
    """Some rejects fall to simp + unfolding anyway; nothing that discharged may stop."""
    b = discharge_budgets_for(F(polarity="reject"), DEFAULT_LADDER_BUDGETS)
    assert b.tier2_tactics[len(NEGATION_TACTICS):] == tuple(DEFAULT_LADDER_BUDGETS.tier2_tactics)


def test_the_witness_grid_is_included():
    """The degenerate-value shapes that caught BOTH known-defective facts."""
    b = discharge_budgets_for(F(polarity="reject"), DEFAULT_LADDER_BUDGETS)
    tactics = [t.tactic for t in b.tier2_tactics]
    assert any("have := h 0 1" in t for t in tactics)
    assert any("push_neg" in t for t in tactics)


def test_reject_detected_from_statement_when_polarity_absent():
    """42 of the earlier corpus's 88 reject-shaped facts carried no polarity label."""
    for stmt in ("¬ VTask.P w", "3 ∉ VTask.S 4", "VTask.f 2 ≠ 5"):
        assert _is_reject_shaped(F(statement=stmt)), stmt
    assert not _is_reject_shaped(F(statement="∀ n, VTask.f n = n"))


def test_truth_unfolding_tactics_are_offered_to_reject_facts():
    """58 of the 113 residue facts are closed instances whose witness is already written; they
    failed only because discharge never unfolded the truth symbol. Measured on
    `¬ Antivary (fun i : Fin 3 => i.val) …`: `decide` FAILED, `simp only [_root_.Antivary] <;>
    decide` PASSED."""
    b = discharge_budgets_for(F(polarity="reject"), DEFAULT_LADDER_BUDGETS, truth_name="Antivary")
    tactics = [t.tactic for t in b.tier2_tactics]
    assert any("simp only [_root_.Antivary]" in t and "decide" in t for t in tactics)
    assert tactics[:len(NEGATION_TACTICS)] == [t.tactic for t in NEGATION_TACTICS]


def test_unfolding_is_absent_without_a_truth_name_and_for_non_rejects():
    assert discharge_budgets_for(F(), DEFAULT_LADDER_BUDGETS, truth_name="Antivary") is DEFAULT_LADDER_BUDGETS
    b = discharge_budgets_for(F(polarity="reject"), DEFAULT_LADDER_BUDGETS)
    assert not any("simp only [" in t.tactic for t in b.tier2_tactics)
