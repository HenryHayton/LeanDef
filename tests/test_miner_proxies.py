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
        exec_mechanism="eval",
        output_decidable_eq=True,
        referenced_constants=[],
        axioms=[],
    )
    defaults.update(overrides)
    return VerifiedDef(**defaults)


# --- casework_tier ---


def test_casework_rich_for_executable_decidable_enumerable():
    v = _verified(explicit_arg_types=["ℕ"], return_type="ℕ", exec_mechanism="eval", output_decidable_eq=True)
    p = compute_proxies(v)
    assert p.casework_tier is SupplyTier.RICH


def test_casework_thin_for_nullary_constant():
    v = _verified(explicit_arg_types=[], return_type="ℕ", exec_mechanism="eval", output_decidable_eq=True)
    p = compute_proxies(v)
    assert p.casework_tier is SupplyTier.THIN


def test_casework_thin_for_non_enumerable_arg_type():
    v = _verified(
        explicit_arg_types=["MyWeirdType"], return_type="ℕ", exec_mechanism="eval", output_decidable_eq=True
    )
    p = compute_proxies(v)
    assert p.casework_tier is SupplyTier.THIN


def test_casework_none_when_not_executable():
    v = _verified(explicit_arg_types=["ℕ"], return_type="ℕ", exec_mechanism="none", output_decidable_eq=True)
    p = compute_proxies(v)
    assert p.casework_tier is SupplyTier.NONE


def test_casework_none_when_output_not_decidable_eq():
    v = _verified(explicit_arg_types=["ℕ"], return_type="ℕ", exec_mechanism="eval", output_decidable_eq=False)
    p = compute_proxies(v)
    assert p.casework_tier is SupplyTier.NONE


def test_casework_none_when_excluded_at_verification():
    v = _verified(included=False, elaborates=False)
    p = compute_proxies(v)
    assert p.casework_tier is SupplyTier.NONE


def test_casework_rich_for_decidable_prop_no_decidable_eq_needed():
    """The Nat.Prime case: Prop-valued, mechanism `decide`, `output_decidable_eq=None`
    (never computed -- see verify.py) -- must still come out casework-rich. This is the
    regression test for the harvest-batch-1 bug where `DecidableEq Prop` (always false, not
    a real instance) incorrectly gated every decidable predicate to `none`."""
    v = _verified(
        explicit_arg_types=["ℕ"],
        return_type="Prop",
        exec_mechanism="decide",
        executable=True,
        output_decidable_eq=None,
    )
    p = compute_proxies(v)
    assert p.casework_tier is SupplyTier.RICH


# --- membership_tier ---


def test_membership_rich_for_decidable_predicate():
    v = _verified(explicit_arg_types=["ℕ"], return_type="Prop", exec_mechanism="decide", output_decidable_eq=None)
    p = compute_proxies(v)
    assert p.membership_tier is SupplyTier.RICH
    assert p.is_predicate_shaped


def test_membership_thin_for_undecidable_predicate():
    v = _verified(explicit_arg_types=["ℕ"], return_type="Prop", exec_mechanism="none", output_decidable_eq=None)
    p = compute_proxies(v)
    assert p.membership_tier is SupplyTier.THIN


def test_membership_thin_for_structure_classifier_shape():
    v = _verified(
        explicit_arg_types=["Finset ℕ"], return_type="Bool", exec_mechanism="none", output_decidable_eq=None
    )
    p = compute_proxies(v)
    assert p.classifies_structure
    assert p.membership_tier is not SupplyTier.NONE


def test_membership_none_for_plain_arithmetic():
    v = _verified(explicit_arg_types=["ℕ"], return_type="ℕ")
    p = compute_proxies(v)
    assert p.membership_tier is SupplyTier.NONE
    assert not p.is_predicate_shaped
    assert not p.classifies_structure


def test_nat_prime_like_definition_is_both_casework_and_membership_rich():
    """Direct regression test matching the task's explicit acceptance criterion: a
    Nat.Prime-shaped definition (Prop-valued, one ℕ argument, decidable in practice) must
    come out rich in *both* tiers -- see proxies.py's module docstring on why this overlap
    is intentional, not a bug."""
    v = _verified(
        explicit_arg_types=["ℕ"],
        return_type="Prop",
        exec_mechanism="decide",
        executable=True,
        output_decidable_eq=None,
    )
    p = compute_proxies(v)
    assert p.casework_tier is SupplyTier.RICH
    assert p.membership_tier is SupplyTier.RICH


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
