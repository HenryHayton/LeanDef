"""Unit tests for miner.shape -- return-shape classification (metadata only, no gate)."""

from miner.shape import classify_return_shape


def test_prop_return_type():
    assert classify_return_shape("Prop") == "prop"
    assert classify_return_shape("  Prop  ") == "prop"


def test_plain_value_return_types():
    assert classify_return_shape("ℕ") == "value"
    assert classify_return_shape("Finset α") == "value"
    assert classify_return_shape("List ℕ") == "value"
    assert classify_return_shape("ℕ × ℕ") == "value"


def test_bundled_equivalence_and_embedding():
    assert classify_return_shape("α ≃ β") == "bundled"
    assert classify_return_shape("Subtype p ↪ α") == "bundled"


def test_bundled_named_hom_and_iso_types():
    assert classify_return_shape("ℤ →+* α") == "value"  # no literal keyword match, arrow-hom notation
    assert classify_return_shape("RingHom ℤ α") == "bundled"
    assert classify_return_shape("OrderIso α β") == "bundled"
    assert classify_return_shape("Equiv.Perm α") == "bundled"


def test_bundled_type_former():
    assert classify_return_shape("Type") == "bundled"
    assert classify_return_shape("Type u_1") == "bundled"
    assert classify_return_shape("Type*") == "bundled"
    assert classify_return_shape("Sort u") == "bundled"
