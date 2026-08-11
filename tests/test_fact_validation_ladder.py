"""The fact validation ladder (schema v1.2): what "validated" now means.

Motivating failures, both from the authored corpus:
  - `Nat.divisors/divisors_mem_iff` and `Nat.log/log_lt_of_lt_pow` are FALSE of their real
    Mathlib objects (each missing an `n ≠ 0` side condition) and both shipped as
    PROVISIONALLY_VALIDATED, "validated against ground truth".
  - `Relation.Map/map_apply_iff_global` is a definitional restatement (Mathlib proves the
    corresponding lemma by `Iff.rfl`), so it cannot discriminate between candidates at all.
"""

from authoring.fact_validation import (CERTIFIED, QUARANTINED_FALSE_OF_TRUTH,
                                       REJECTED_RESTATEMENT, UNVALIDATED, _bare_prop,
                                       truth_statement)


def test_decide_command_is_reduced_to_its_bare_prop():
    assert _bare_prop("example : VTask.clog 2 8 = 3 := by decide") == "VTask.clog 2 8 = 3"


def test_bare_prop_left_alone():
    assert _bare_prop("∀ n : ℕ, VTask.f n = n") == "∀ n : ℕ, VTask.f n = n"


def test_truth_substitution_targets_the_real_object():
    out = truth_statement("∀ n, VTask.divisors n = x", "VTask.divisors", "Nat.divisors")
    assert "VTask.divisors" not in out
    assert "Nat.divisors" in out


def test_shipping_statuses_are_exactly_certified_and_unvalidated():
    """Rejections and quarantines must NOT ship; UNVALIDATED must, so attrition stays visible
    rather than being silently dropped."""
    from authoring.fact_validation import FactValidation
    ships = {s for s in (CERTIFIED, UNVALIDATED, REJECTED_RESTATEMENT,
                         QUARANTINED_FALSE_OF_TRUTH)
             if FactValidation("f", s).ships}
    assert ships == {CERTIFIED, UNVALIDATED}
