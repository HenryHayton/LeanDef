"""Unit tests for miner.proxies' supply-tier heuristics, on synthetic VerifiedDef instances
-- no REPL, no real Mathlib data."""

from miner.proxies import SupplyTier, compute_proxies
from miner.verify import VerifiedDef


def _verified(**overrides) -> VerifiedDef:
    defaults = dict(
        name="Test.foo",
        module_path="Test.lean",
        source_text="def foo (n : Nat) : Nat := n",
        docstring=None,
        mention_count=0,
        included=True,
        elaborates=True,
        explicit_arg_types=["ℕ"],
        return_type="ℕ",
        executable=True,
        output_decidable_eq=True,
        referenced_constants=[],
        axioms=[],
    )
    defaults.update(overrides)
    return VerifiedDef(**defaults)


# --- casework_tier ---


def test_casework_rich_for_executable_decidable_enumerable():
    v = _verified(explicit_arg_types=["ℕ"], return_type="ℕ", executable=True, output_decidable_eq=True)
    p = compute_proxies(v)
    assert p.casework_tier is SupplyTier.RICH


def test_casework_thin_for_nullary_constant():
    v = _verified(explicit_arg_types=[], return_type="ℕ", executable=True, output_decidable_eq=True)
    p = compute_proxies(v)
    assert p.casework_tier is SupplyTier.THIN


def test_casework_thin_for_non_enumerable_arg_type():
    v = _verified(explicit_arg_types=["MyWeirdType"], return_type="ℕ", executable=True, output_decidable_eq=True)
    p = compute_proxies(v)
    assert p.casework_tier is SupplyTier.THIN


def test_casework_none_when_not_executable():
    v = _verified(explicit_arg_types=["ℕ"], return_type="ℕ", executable=False, output_decidable_eq=True)
    p = compute_proxies(v)
    assert p.casework_tier is SupplyTier.NONE


def test_casework_none_when_output_not_decidable_eq():
    v = _verified(explicit_arg_types=["ℕ"], return_type="ℕ", executable=True, output_decidable_eq=False)
    p = compute_proxies(v)
    assert p.casework_tier is SupplyTier.NONE


def test_casework_none_when_excluded_at_verification():
    v = _verified(included=False, elaborates=False)
    p = compute_proxies(v)
    assert p.casework_tier is SupplyTier.NONE


# --- membership_tier ---


def test_membership_rich_for_decidable_predicate():
    v = _verified(explicit_arg_types=["ℕ"], return_type="Prop", executable=True, output_decidable_eq=True)
    p = compute_proxies(v)
    assert p.membership_tier is SupplyTier.RICH
    assert p.is_predicate_shaped


def test_membership_thin_for_undecidable_predicate():
    v = _verified(explicit_arg_types=["ℕ"], return_type="Prop", executable=False, output_decidable_eq=False)
    p = compute_proxies(v)
    assert p.membership_tier is SupplyTier.THIN


def test_membership_thin_for_structure_classifier_shape():
    v = _verified(explicit_arg_types=["Finset ℕ"], return_type="Bool", executable=False, output_decidable_eq=False)
    p = compute_proxies(v)
    assert p.classifies_structure
    assert p.membership_tier is not SupplyTier.NONE


def test_membership_none_for_plain_arithmetic():
    v = _verified(explicit_arg_types=["ℕ"], return_type="ℕ")
    p = compute_proxies(v)
    assert p.membership_tier is SupplyTier.NONE
    assert not p.is_predicate_shaped
    assert not p.classifies_structure


# --- global_tier ---


def test_global_none_for_zero_mentions():
    v = _verified(mention_count=0)
    p = compute_proxies(v)
    assert p.global_tier is SupplyTier.NONE


def test_global_thin_for_a_few_mentions():
    v = _verified(mention_count=3)
    p = compute_proxies(v)
    assert p.global_tier is SupplyTier.THIN


def test_global_rich_for_many_mentions():
    v = _verified(mention_count=20)
    p = compute_proxies(v)
    assert p.global_tier is SupplyTier.RICH


def test_global_uses_theorem_mention_count_when_supplied():
    v = _verified(mention_count=0)
    p = compute_proxies(v, theorem_mention_count=10)
    assert p.global_tier is SupplyTier.RICH
    assert p.theorem_mention_count == 10
