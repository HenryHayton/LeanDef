"""Unit tests for miner.scan's textual pre-filter, on small synthetic Lean-shaped inputs --
no real Mathlib files, no REPL. See tests/test_miner_harvest.py for the integration test
against a real module."""

from miner.scan import (
    _split_statement_at_top_level_assign,
    scan_text,
    scan_theorem_statements,
    scan_theorem_statements_with_namespace,
)


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


# --- _split_statement_at_top_level_assign (docs/theorem_mention_audit.md H2 fix) ---


def test_bracket_aware_split_ignores_named_argument_assign():
    """The audit's confirmed failing shape: a named-argument `(a := a)` inside the statement
    itself must not be mistaken for the statement/proof separator."""
    text = "lemma foo : Injective (bar (a := a)) := by simp"
    result = _split_statement_at_top_level_assign(text)
    assert result == "lemma foo : Injective (bar (a := a)) "
    assert "Injective" in result
    assert "by simp" not in result


def test_bracket_aware_split_still_finds_top_level_assign_with_no_brackets():
    text = "theorem a_eq (n : Nat) : dist n n = 0 := by simp [dist]"
    result = _split_statement_at_top_level_assign(text)
    assert result == "theorem a_eq (n : Nat) : dist n n = 0 "


def test_theorem_statement_not_truncated_by_named_argument_syntax():
    """End-to-end regression, via scan_theorem_statements: a mention appearing textually
    *after* a named-argument `:=` inside the statement must still be captured, not discarded
    by a premature split."""
    text = "lemma birkhoffFinset_injective : Injective (birkhoffFinset (α := α)) ∧ dist_comm := by simp\n"
    statements = scan_theorem_statements(text)
    assert len(statements) == 1
    assert "dist_comm" in statements[0]
    assert "by simp" not in statements[0]


# --- scan_theorem_statements_with_namespace (docs/theorem_mention_audit.md H1 fix) ---


def test_namespace_prefix_recorded_for_statement_inside_namespace():
    text = """\
namespace Finset

theorem pi_congr (s : Finset α) : True := trivial

end Finset
"""
    results = scan_theorem_statements_with_namespace(text)
    assert len(results) == 1
    statement, namespace_prefix = results[0]
    assert namespace_prefix == "Finset"
    assert "pi_congr" in statement


def test_namespace_prefix_empty_at_top_level():
    text = "theorem foo : True := trivial\n"
    results = scan_theorem_statements_with_namespace(text)
    assert len(results) == 1
    assert results[0][1] == ""


def test_nested_namespaces_join_with_dots():
    text = """\
namespace Finset
namespace Colex

theorem initSeg_something : True := trivial

end Colex
end Finset
"""
    results = scan_theorem_statements_with_namespace(text)
    assert len(results) == 1
    assert results[0][1] == "Finset.Colex"


def test_named_section_does_not_contribute_to_namespace_prefix():
    """A `section Foo` is scoping only -- Lean does not qualify declarations by it the way it
    does by `namespace Foo`. A statement inside `section Finset ... end` (no real namespace)
    must record an EMPTY prefix, not "Finset"."""
    text = """\
section Finset

theorem something : True := trivial

end
"""
    results = scan_theorem_statements_with_namespace(text)
    assert len(results) == 1
    assert results[0][1] == ""


def test_reopened_namespace_across_two_blocks_both_scoped_correctly():
    text = """\
namespace Finset

theorem a_thm : True := trivial

end Finset

namespace Finset

theorem b_thm : True := trivial

end Finset
"""
    results = scan_theorem_statements_with_namespace(text)
    assert len(results) == 2
    assert results[0][1] == "Finset"
    assert results[1][1] == "Finset"


def test_bare_pi_inside_finset_namespace_would_be_scoped_correctly_reproducing_the_audit_pattern():
    """Reproduces the qualitative pattern behind the audit's Finset.pi finding (0 -> ~63):
    several theorem statements inside `namespace Finset ... end Finset` mention `pi` bare,
    never qualified -- all must be recorded with namespace_prefix == "Finset" so
    miner.harvest.compute_theorem_mention_counts can count them toward `Finset.pi`."""
    text = """\
namespace Finset

theorem pi_nonempty (s : Finset α) (t : ∀ a, Finset (β a)) : (s.pi t).Nonempty ↔ True := trivial

theorem card_pi (s : Finset α) (t : ∀ a, Finset (β a)) : (s.pi t).card = 0 := trivial

theorem mem_pi (s : Finset α) (t : ∀ a, Finset (β a)) : True := trivial

end Finset
"""
    results = scan_theorem_statements_with_namespace(text)
    assert len(results) == 3
    assert all(ns == "Finset" for _, ns in results)
    assert all("pi" in statement for statement, _ in results)


def test_bare_pi_in_unrelated_namespace_must_not_be_scoped_to_finset():
    """Collision case: a bare `pi` mention inside an unrelated namespace (e.g. `Real`, where
    `pi` means the mathematical constant) must record that OTHER namespace, not `Finset` --
    this is what lets miner.harvest.compute_theorem_mention_counts avoid counting it toward
    `Finset.pi`, the collision risk the audit quantified at up to 98% noise for unscoped bare
    matching."""
    text = """\
namespace Real

theorem pi_pos : 0 < pi := trivial

end Real
"""
    results = scan_theorem_statements_with_namespace(text)
    assert len(results) == 1
    statement, namespace_prefix = results[0]
    assert namespace_prefix == "Real"
    assert namespace_prefix != "Finset"
    assert "pi" in statement
