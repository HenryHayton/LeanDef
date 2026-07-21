"""Unit tests for miner.scan's textual pre-filter, on small synthetic Lean-shaped inputs --
no real Mathlib files, no REPL. See tests/test_miner_harvest.py for the integration test
against a real module."""

from miner.scan import scan_text, scan_theorem_statements


def test_simple_def_with_docstring():
    text = """\
namespace Nat

/-- Distance between naturals. -/
def dist (n m : ℕ) :=
  n - m + (m - n)

theorem dist_comm (n m : ℕ) : dist n m = dist m n := by simp [dist, add_comm]

end Nat
"""
    hits = scan_text(text, "Data/Nat/Dist.lean")
    assert len(hits) == 1
    assert hits[0].name == "Nat.dist"
    assert hits[0].docstring == "Distance between naturals."
    assert hits[0].source_text == "def dist (n m : ℕ) :=\n  n - m + (m - n)"


def test_def_without_docstring():
    text = "def foo (n : Nat) : Nat := n + 1\n"
    hits = scan_text(text, "Scratch.lean")
    assert len(hits) == 1
    assert hits[0].name == "foo"
    assert hits[0].docstring is None


def test_private_def_is_skipped():
    text = "private def secretHelper (n : Nat) : Nat := n\n"
    hits = scan_text(text, "Scratch.lean")
    assert hits == []


def test_noncomputable_def_is_skipped():
    text = "noncomputable def choiceValue : Nat := Classical.choice ⟨0⟩\n"
    hits = scan_text(text, "Scratch.lean")
    assert hits == []


def test_deprecated_def_is_skipped():
    text = """\
@[deprecated (since := "2026-01-01")]
def oldName (n : Nat) : Nat := n
"""
    hits = scan_text(text, "Scratch.lean")
    assert hits == []


def test_protected_def_is_kept():
    text = "protected def foo (n : Nat) : Nat := n\n"
    hits = scan_text(text, "Scratch.lean")
    assert len(hits) == 1
    assert hits[0].name == "foo"


def test_theorem_instance_abbrev_structure_are_not_hits():
    text = """\
theorem foo_eq (n : Nat) : n = n := rfl

instance : Inhabited Nat := ⟨0⟩

abbrev NatAlias := Nat

structure Point where
  x : Nat
  y : Nat
"""
    hits = scan_text(text, "Scratch.lean")
    assert hits == []


def test_nested_namespace_qualifies_name():
    text = """\
namespace Outer
namespace Inner

def foo (n : Nat) : Nat := n

end Inner
end Outer
"""
    hits = scan_text(text, "Scratch.lean")
    assert len(hits) == 1
    assert hits[0].name == "Outer.Inner.foo"


def test_section_does_not_affect_qualified_name():
    text = """\
namespace Nat

section Helpers
variable (p : Nat -> Prop)

def foo (n : Nat) : Nat := n

end Helpers

end Nat
"""
    hits = scan_text(text, "Scratch.lean")
    assert len(hits) == 1
    assert hits[0].name == "Nat.foo"


def test_multiple_defs_are_separated_at_column_zero():
    text = """\
def first (n : Nat) : Nat :=
  n + 1

def second (n : Nat) : Nat := n + 2
"""
    hits = scan_text(text, "Scratch.lean")
    assert [h.name for h in hits] == ["first", "second"]
    assert hits[0].source_text == "def first (n : Nat) : Nat :=\n  n + 1"
    assert hits[1].source_text == "def second (n : Nat) : Nat := n + 2"


def test_attribute_and_docstring_both_present():
    text = """\
/-- Counts something. -/
@[simp]
def count (n : Nat) : Nat := n
"""
    hits = scan_text(text, "Scratch.lean")
    assert len(hits) == 1
    assert hits[0].docstring == "Counts something."
    assert hits[0].source_text == "def count (n : Nat) : Nat := n"


def test_multiline_docstring():
    text = """\
/-- First line.
Second line. -/
def foo (n : Nat) : Nat := n
"""
    hits = scan_text(text, "Scratch.lean")
    assert len(hits) == 1
    assert "First line." in hits[0].docstring
    assert "Second line." in hits[0].docstring


# --- scan_theorem_statements ---


def test_theorem_statement_excludes_proof_body():
    text = """\
theorem foo_pos (n : Nat) (h : 0 < n) : foo n > 0 := by
  unfold foo
  simp [h]
  exact absurd h (by omega)
"""
    statements = scan_theorem_statements(text)
    assert len(statements) == 1
    assert "foo_pos" in statements[0]
    assert "omega" not in statements[0]
    assert "unfold foo" not in statements[0]


def test_theorem_statement_multiple_theorems():
    text = """\
theorem a_eq (n : Nat) : dist n n = 0 := by simp [dist]

lemma b_eq (n m : Nat) : dist n m = dist m n := dist_comm n m
"""
    statements = scan_theorem_statements(text)
    assert len(statements) == 2
    assert "a_eq" in statements[0] and "dist n n = 0" in statements[0]
    assert "b_eq" in statements[1] and "dist n m = dist m n" in statements[1]
    # the proof term after `:=` on the second theorem must not leak into its statement
    assert "dist_comm" not in statements[1]


# --- Regression tests for the six real collisions found in the batch-1 review (harvest
# batch 1 review, "data-quality flag"): unicode subscript suffixes were silently dropped by
# the old identifier regex, causing e.g. `image₂` to be scanned as `image` and collide with
# the real `Finset.image`. Each of these must now resolve to its own, distinct, full name.


def test_image2_does_not_collide_with_image():
    text = "namespace Finset\ndef image (f : α → β) (s : Finset α) : Finset β := sorry\nend Finset\n"
    hits = scan_text(text, "Data/Finset/Image.lean")
    assert [h.name for h in hits] == ["Finset.image"]

    text2 = "namespace Finset\ndef image₂ (f : α → β → γ) (s : Finset α) (t : Finset β) : Finset γ := sorry\nend Finset\n"
    hits2 = scan_text(text2, "Data/Finset/NAry.lean")
    assert [h.name for h in hits2] == ["Finset.image₂"]


def test_semiconj2_does_not_collide_with_semiconj():
    text = "namespace Function\ndef Semiconj (f : α → β) (ga : α → α) (gb : β → β) : Prop := sorry\nend Function\n"
    hits = scan_text(text, "Logic/Function/Conjugate.lean")
    assert [h.name for h in hits] == ["Function.Semiconj"]

    text2 = "namespace Function\ndef Semiconj₂ (f : α → β) (ga : α → α → α) (gb : β → β → β) : Prop := sorry\nend Function\n"
    hits2 = scan_text(text2, "Logic/Function/Conjugate.lean")
    assert [h.name for h in hits2] == ["Function.Semiconj₂"]


def test_map2_variants_do_not_collide_with_map():
    variants = ["map₂Left'", "map₂Right'", "map₂Left", "map₂Right"]
    for variant in variants:
        text = f"namespace List\ndef {variant} (f : α → β → γ) : List γ := sorry\nend List\n"
        hits = scan_text(text, "Data/List/Defs.lean")
        assert [h.name for h in hits] == [f"List.{variant}"], f"failed for {variant}"


def test_subscript_digit_and_letter_are_id_rest_characters():
    """Direct check of the character-class fix itself (not just the specific collisions
    above): both the numeric-subscript range (₀-₉) and the subscript-letter range
    (e.g. ₐ, ᵢ, ⱼ) that Lean's own `isSubScriptAlnum` accepts must be captured."""
    text = "def foo₂ : Nat := 0\ndef barₐ : Nat := 0\ndef bazᵢ : Nat := 0\n"
    hits = scan_text(text, "Scratch.lean")
    assert [h.name for h in hits] == ["foo₂", "barₐ", "bazᵢ"]
