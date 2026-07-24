"""Unit tests for miner.scan's textual pre-filter, on small synthetic Lean-shaped inputs --
no real Mathlib files, no REPL. See tests/test_miner_harvest.py for the integration test
against a real module."""

from miner.scan import (
    _find_module_doc_skip_lines,
    _qualify_name,
    _SECTION_RE,
    _split_statement_at_top_level_assign,
    _THEOREM_RE,
    scan_text,
    scan_theorem_declarations_with_namespace,
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


def test_scan_theorem_declarations_with_namespace_returns_qualified_name():
    text = """\
namespace Finset

theorem pi_congr (s : Finset α) : True := trivial

end Finset
"""
    results = scan_theorem_declarations_with_namespace(text)
    assert len(results) == 1
    name, statement, namespace_prefix = results[0]
    assert name == "Finset.pi_congr"
    assert namespace_prefix == "Finset"
    assert "pi_congr" in statement


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


# --- Bug A: `_root_.` namespace-escape prefix (bundled miner repairs task, batch-4 review §7(a)) --


def test_qualify_name_strips_root_escape_and_ignores_namespace_stack():
    assert _qualify_name("_root_.Foo.bar", ["Baz"]) == "Foo.bar"
    assert _qualify_name("_root_.Foo.bar", []) == "Foo.bar"
    assert _qualify_name("bar", ["Baz"]) == "Baz.bar"


def test_root_escape_def_inside_namespace_is_not_doubly_qualified():
    """Reproduces the exact real-corpus shape from the batch-4 review (§7(a)): `namespace
    Finset ... def _root_.Equiv.Finset.prod ... end Finset` declares `Equiv.Finset.prod`, not
    `Finset._root_.Equiv.Finset.prod` (the bug's old output) and not `Finset.Equiv.Finset.prod`
    (what a naive "just drop the marker but still prepend" fix would wrongly produce)."""
    text = """\
namespace Finset

/-- The product of `Finset.prod` reindexed through an equivalence. -/
def _root_.Equiv.Finset.prod (e : α ≃ β) (s : Finset α) (f : β → γ) : γ :=
  s.prod (f ∘ e)

end Finset
"""
    hits = scan_text(text, "Data/Finset/Prod.lean")
    assert len(hits) == 1
    assert hits[0].name == "Equiv.Finset.prod"


def test_root_escape_def_at_top_level_still_strips_marker():
    """Even with an empty namespace stack, the literal `_root_.` marker itself must be
    stripped -- it is not a valid part of the real declared name either way."""
    text = "def _root_.Foo.bar (n : Nat) : Nat := n\n"
    hits = scan_text(text, "Scratch.lean")
    assert len(hits) == 1
    assert hits[0].name == "Foo.bar"


def test_root_escape_nested_namespace_only_the_marker_is_special():
    text = """\
namespace Outer
namespace Inner

def _root_.Escaped.name (n : Nat) : Nat := n
def notEscaped (n : Nat) : Nat := n

end Inner
end Outer
"""
    hits = scan_text(text, "Scratch.lean")
    assert {h.name for h in hits} == {"Escaped.name", "Outer.Inner.notEscaped"}


def test_root_escape_theorem_name_qualification_shares_the_fix():
    """Piece 1 adds theorem-name qualification fresh (no prior implementation existed to have
    inherited the bug) -- built on the same `_qualify_name` helper `_capture_def` uses, so a
    `_root_.`-escaped theorem is named correctly too."""
    text = """\
namespace Finset

theorem _root_.Equiv.Finset.prod_congr (e : α ≃ β) : True := trivial

end Finset
"""
    results = scan_theorem_declarations_with_namespace(text)
    assert len(results) == 1
    name, _, namespace_prefix = results[0]
    assert name == "Equiv.Finset.prod_congr"
    assert namespace_prefix == "Finset"  # matching rule (namespace-scoped bare mentions) unaffected


# --- Bug B: `/-!` module-doc blocks scanned as code (batch-4 review §7(b)) ------------------


def test_module_doc_block_def_example_is_not_reported():
    """Acceptance test (task-specified shape): a `/-!` block containing an illustrative `def`
    must not be reported, and a real `def` after the block must be."""
    text = """\
/-!
# Some module

Illustrative example:
```
def phantom (n : Nat) : Nat := n
```
-/

def real (n : Nat) : Nat := n
"""
    hits = scan_text(text, "Scratch.lean")
    assert [h.name for h in hits] == ["real"]


def test_module_doc_block_reproduces_real_corpus_shape_nat_log():
    """Reproduces `Data/Nat/Log.lean`'s real shape (found while investigating this task): a
    `/-!` block, opened before `namespace Nat`, illustrates a tail-recursive `logTR` variant
    and an `#eval` example -- neither is real code."""
    text = """\
/-!
# Natural number logarithms

Note a tail-recursive version of `Nat.log` is also possible:
```
def logTR (b n : ℕ) : ℕ :=
  go b n
```
but performs worse for large numbers than `Nat.log`:
```
#eval Nat.logTR 2 (2 ^ 1000000)
```
-/

namespace Nat

def log (b n : ℕ) : ℕ := 0

end Nat
"""
    hits = scan_text(text, "Data/Nat/Log.lean")
    assert [h.name for h in hits] == ["Nat.log"]


def test_module_doc_block_single_line_is_skipped():
    """A `/-! ... -/` block fully on one line (real shape: `/-! ### Floor logarithm -/`) must
    still be recognized and skipped -- depth must return to 0 within the same line, not require
    a separate closing line."""
    text = """\
/-! ### Section header -/

def real (n : Nat) : Nat := n
"""
    hits = scan_text(text, "Scratch.lean")
    assert [h.name for h in hits] == ["real"]


def test_module_doc_block_nested_comment_does_not_close_early():
    """Lean block comments nest: a `/-!` block containing a genuinely nested `/- ... -/` must
    not have its OWN span end at the nested comment's `-/` -- the outer block continues until
    ITS matching close."""
    text = """\
/-!
Outer doc, with a nested aside: /- inner note -/ still inside.
def phantom (n : Nat) : Nat := n
-/

def real (n : Nat) : Nat := n
"""
    hits = scan_text(text, "Scratch.lean")
    assert [h.name for h in hits] == ["real"]


def test_module_doc_block_theorem_example_is_not_scanned_as_a_mention_source():
    """The same `/-!` skip applies to the theorem scanner: an illustrative `theorem`-shaped
    line inside a module-doc block must not be scanned as a real theorem statement (it would
    otherwise inflate `theorem_mention_count` for whatever candidate name it happens to
    illustrate)."""
    text = """\
/-!
Illustrative:
```
theorem phantom_thm : Foo.bar = Foo.bar := rfl
```
-/

theorem real_thm : True := trivial
"""
    results = scan_theorem_statements(text)
    assert len(results) == 1
    assert "real_thm" in results[0]


def test_find_module_doc_skip_lines_directly():
    text = "line0\n/-!\nline2\n-/\nline4\n"
    lines = text.split("\n")
    assert _find_module_doc_skip_lines(lines) == {1, 2, 3}


def test_find_module_doc_skip_lines_unterminated_block_skips_to_end_of_file():
    text = "line0\n/-!\nline2\nline3"
    lines = text.split("\n")
    assert _find_module_doc_skip_lines(lines) == {1, 2, 3}


def test_module_doc_block_does_not_affect_docstring_handling():
    """Regression guard: `/--` declaration docstrings (a completely different, already-handled
    mechanism) must keep working normally alongside the new `/-!` handling."""
    text = """\
/-!
Module overview.
-/

/-- Real docstring. -/
def real (n : Nat) : Nat := n
"""
    hits = scan_text(text, "Scratch.lean")
    assert len(hits) == 1
    assert hits[0].name == "real"
    assert hits[0].docstring == "Real docstring."


# --- Universe-annotation trailing dot (bundled miner repairs follow-up task) -----------------


def test_qualify_name_strips_spurious_trailing_dot():
    assert _qualify_name("bitCasesOn.", ["Int"]) == "Int.bitCasesOn"
    assert _qualify_name("Multiset.", []) == "Multiset"
    # composes correctly with the _root_. fix: strip the trailing dot first, THEN check escape.
    assert _qualify_name("_root_.Foo.bar.", ["Baz"]) == "Foo.bar"


def test_universe_annotated_def_int_bitcaseson():
    """Reproduces `Data/Int/Bitwise.lean`'s real shape: `def bitCasesOn.{u} {C : ...} ... :=
    by ...` inside `namespace Int` -- previously scanned as `Int.bitCasesOn.` (trailing dot,
    `Invalid field notation` at #check time)."""
    text = """\
namespace Int

/-- Defines a function from `ℤ` conditionally. -/
def bitCasesOn.{u} {C : ℤ → Sort u} (n) (h : ∀ b n, C (bit b n)) : C n := by
  rw [← bit_decomp n]
  apply h

end Int
"""
    hits = scan_text(text, "Data/Int/Bitwise.lean")
    assert len(hits) == 1
    assert hits[0].name == "Int.bitCasesOn"


def test_universe_annotated_def_equiv_optionequivsumpunit():
    """Reproduces `Logic/Equiv/Option.lean`'s real shape: two universe parameters."""
    text = """\
namespace Equiv

/-- `Option α` is equivalent to `α ⊕ PUnit` -/
def optionEquivSumPUnit.{v, w} (α : Type w) : Option α ≃ α ⊕ PUnit.{v + 1} :=
  ⟨fun o => o.elim (inr PUnit.unit) inl, fun s => s.elim some fun _ => none, id, id⟩

end Equiv
"""
    hits = scan_text(text, "Logic/Equiv/Option.lean")
    assert len(hits) == 1
    assert hits[0].name == "Equiv.optionEquivSumPUnit"


def test_universe_annotated_def_multiset_top_level():
    """Reproduces `Data/Multiset/Defs.lean`'s real shape: the universe-annotated def is at
    top level, declared BEFORE `namespace Multiset` opens -- no namespace to prepend at all."""
    text = """\
/-- `Multiset α` is the quotient of `List α` by list permutation. -/
def Multiset.{u} (α : Type u) : Type u :=
  Quotient (List.isSetoid α)

namespace Multiset

def ofList : List α → Multiset α := fun l => l

end Multiset
"""
    hits = scan_text(text, "Data/Multiset/Defs.lean")
    assert [h.name for h in hits] == ["Multiset", "Multiset.ofList"]


def test_universe_annotated_def_option_traverse():
    """Reproduces `Data/Option/Defs.lean`'s real shape."""
    text = """\
namespace Option

protected def traverse.{u, v} {F : Type u → Type v} [Applicative F] {α : Type u} {β : Type u}
    (f : α → F β) : Option α → F (Option β)
  | none => pure none
  | some x => some <$> f x

end Option
"""
    hits = scan_text(text, "Data/Option/Defs.lean")
    assert [h.name for h in hits] == ["Option.traverse"]


def test_theorem_name_capture_had_the_identical_trailing_dot_defect():
    """Verifies explicitly (per the follow-up task's instruction) that theorem-name capture
    shares the def-name capture's defect: `_THEOREM_RE` uses the same `_ID_REST` class, so its
    RAW captured group for a universe-annotated theorem also ends in a spurious `.` -- proven
    directly against the regex, independent of the `_qualify_name` fix that then strips it."""
    m = _THEOREM_RE.match("theorem foo.{u} {C : Sort u} (n : C) : C := n")
    assert m is not None
    assert m.group("name") == "foo."  # the raw defect, unfixed at the regex layer itself


def test_universe_annotated_theorem_name_is_qualified_correctly_end_to_end():
    """End-to-end: a universe-annotated theorem, scanned via `scan_theorem_declarations_with_namespace`
    (piece 1's naming path, which calls the shared, now-fixed `_qualify_name`), gets the
    correct name -- no trailing dot, whether or not `_root_.`-escaped."""
    text = "namespace Foo\n\ntheorem bar.{u} {C : Sort u} (n : C) : C := n\n\nend Foo\n"
    results = scan_theorem_declarations_with_namespace(text)
    assert len(results) == 1
    name, _, _ = results[0]
    assert name == "Foo.bar"


# --- `noncomputable section` / `public section` not matched by _SECTION_RE (bundled miner ----
# --- repairs follow-up task) ------------------------------------------------------------------


def test_noncomputable_section_reproduces_logic_function_basic_shape():
    """Reproduces `Logic/Function/Basic.lean`'s real, confirmed-live shape: `namespace Function
    ... noncomputable section Extend ... end Extend ...` -- before this fix, `noncomputable
    section Extend` was never pushed, so `end Extend` wrongly popped `namespace Function`
    instead, and every subsequent `def` (here, `afterExtend`) lost its `Function.` prefix."""
    text = """\
namespace Function

def beforeExtend (a : Nat) : Nat := a

noncomputable section Extend

def extendHelper (a : Nat) : Nat := a

end Extend

def afterExtend (a : Nat) : Nat := a

end Function
"""
    hits = scan_text(text, "Logic/Function/Basic.lean")
    assert [h.name for h in hits] == ["Function.beforeExtend", "Function.extendHelper", "Function.afterExtend"]


def test_public_section_reproduces_combinatorics_compactness_shape():
    """Reproduces `Combinatorics/Compactness.lean`'s real, confirmed-live shape: a bare
    `public section` (Lean's module-visibility marker, unrelated to `noncomputable`) later
    closed by a bare `end` -- same desync mechanism, different modifier word. Also covers the
    `@[expose] public section` form (the far more common real shape, e.g.
    `Data/Nat/Log.lean`) in the same test, both must be recognized."""
    text = """\
namespace Outer

public section

def inSection (a : Nat) : Nat := a

end

def afterSection (a : Nat) : Nat := a

end Outer
"""
    hits = scan_text(text, "Combinatorics/Compactness.lean")
    assert [h.name for h in hits] == ["Outer.inSection", "Outer.afterSection"]


def test_expose_attribute_prefixed_public_section_is_recognized():
    text = "@[expose] public section\n\ndef top (a : Nat) : Nat := a\n"
    hits = scan_text(text, "Scratch.lean")
    assert [h.name for h in hits] == ["top"]


def test_unattested_modifier_words_are_not_specially_handled():
    """`private section`/`protected section`/`scoped section` were checked against the whole
    Mathlib corpus and confirmed to never occur (0 matches each) -- not real Lean syntax. This
    test documents that `_SECTION_RE` deliberately does NOT special-case them (nothing to
    special-case): a line shaped like one is simply not recognized as a section opener, exactly
    as before this fix, since there is no live example to fix against. `meta section` (48
    corpus-wide occurrences, structurally identical risk) is real syntax but does not occur
    within `TARGET_MODULES` -- also not specially handled, for the same "no live example in
    scope" reason."""
    for unrecognized in ("private section", "protected section", "scoped section", "meta section"):
        assert _SECTION_RE.match(unrecognized) is None


def test_section_name_capture_still_works_with_modifier_prefix():
    """The optional section NAME (used for `end <name>` bookkeeping, though qualification
    itself only ever reads `namespace` entries) must still be captured correctly alongside a
    modifier prefix."""
    m = _SECTION_RE.match("noncomputable section Extend")
    assert m.group(1) == "Extend"
    m2 = _SECTION_RE.match("public section")
    assert m2.group(1) is None
