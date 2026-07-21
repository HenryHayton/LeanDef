"""Unit tests for miner.richness -- structural richness counting, on hand-computed examples
spanning zero-structure (a pure delegation) to condition-rich. No REPL, no real Mathlib data."""

from miner.richness import compute_richness
from miner.verify import BinderGroup, VerifiedDef


def _verified(source_text: str, binder_groups: list[BinderGroup]) -> VerifiedDef:
    return VerifiedDef(
        name="Test.foo",
        module_path="Test.lean",
        source_text=source_text,
        docstring=None,
        mention_count=0,
        included=True,
        elaborates=True,
        binder_groups=binder_groups,
        explicit_arg_types=[],
        return_type="",
        executable=None,
        exec_mechanism="none",
        output_decidable_eq=None,
        referenced_constants=[],
        axioms=[],
    )


def test_pure_delegation_scores_zero():
    """A one-line delegation has no structure of its own -- the direct fix for the
    dependency-count proxy the old score used (design doc §4.1)."""
    v = _verified(
        "def toFinset (l : List α) : Finset α := Multiset.toFinset l",
        [BinderGroup(kind="explicit", names=["l"], type_text="List α")],
    )
    r = compute_richness(v)
    assert r.total == 0
    assert (r.conjunctions, r.disjunctions, r.conditionals, r.quantifiers, r.comparisons, r.hypothesis_binders) == (
        0,
        0,
        0,
        0,
        0,
        0,
    )


def test_bare_equality_counts_as_a_comparison():
    v = _verified(
        "def Nat.ModEq (n a b : ℕ) := a % n = b % n",
        [BinderGroup(kind="explicit", names=["n", "a", "b"], type_text="ℕ")],
    )
    r = compute_richness(v)
    assert r.comparisons == 1
    assert r.total == 1


def test_definition_assignment_operator_is_not_counted_as_comparison():
    """`:=` must not be miscounted as a bare `=` comparison."""
    v = _verified(
        "def foo (n : ℕ) : ℕ := n",
        [BinderGroup(kind="explicit", names=["n"], type_text="ℕ")],
    )
    r = compute_richness(v)
    assert r.comparisons == 0


def test_pairwise_counts_quantifier_comparison_and_relation_hypothesis_binder():
    v = _verified(
        "def Pairwise (r : α → α → Prop) := ∀ ⦃i j⦄, i ≠ j → r i j",
        [BinderGroup(kind="explicit", names=["r"], type_text="α → α → Prop")],
    )
    r = compute_richness(v)
    assert r.quantifiers == 1  # ∀
    assert r.comparisons == 1  # ≠
    assert r.hypothesis_binders == 1  # r's Prop-valued relation type
    assert r.total == 3


def test_condition_rich_definition_counts_every_component():
    v = _verified(
        "def foo (h : a ≤ b) (P : Prop) : Prop := "
        "if a < b then (P ∧ ∃ x, x = a) else (P ∨ ∀ y, y ≠ b)",
        [
            BinderGroup(kind="explicit", names=["h"], type_text="a ≤ b"),
            BinderGroup(kind="explicit", names=["P"], type_text="Prop"),
        ],
    )
    r = compute_richness(v)
    assert r.conjunctions == 1
    assert r.disjunctions == 1
    assert r.conditionals == 1  # "if"
    assert r.quantifiers == 2  # ∃, ∀
    assert r.comparisons == 4  # ≤, <, =, ≠
    assert r.hypothesis_binders == 2  # h : a ≤ b, P : Prop
    assert r.total == 11


def test_match_arms_count_as_conditionals():
    v = _verified(
        "def choose : ℕ → ℕ → ℕ | _, 0 => 1 | 0, _ + 1 => 0 | n + 1, k + 1 => choose n k + choose n (k + 1)",
        [],
    )
    r = compute_richness(v)
    assert r.conditionals == 3  # three match arms, three "=>"


def test_bif_counts_as_conditional():
    v = _verified("def foo (b : Bool) (n : ℕ) : ℕ := bif b then n else 0", [])
    r = compute_richness(v)
    assert r.conditionals == 1


def test_plain_data_binder_is_not_a_hypothesis():
    v = _verified(
        "def foo (n : ℕ) (s : Finset ℕ) : ℕ := n",
        [
            BinderGroup(kind="explicit", names=["n"], type_text="ℕ"),
            BinderGroup(kind="explicit", names=["s"], type_text="Finset ℕ"),
        ],
    )
    r = compute_richness(v)
    assert r.hypothesis_binders == 0


def test_bare_lambda_arm_does_not_count_as_conditional_or_comparison():
    """Fixed 22 July 2026 (batch-2 §5 item 3): a bare `fun x => ...` lambda arm (no preceding
    `|`) must not count as a match arm, and the `=` inside its `=>` must not count as a
    comparison either -- the second was a compounding bug (`=>` contains `=`)."""
    v = _verified("def foo (n : ℕ) : ℕ := (fun x => x + 1) n", [])
    r = compute_richness(v)
    assert r.conditionals == 0
    assert r.comparisons == 0
    assert r.total == 0


def test_equiv_prodassoc_shaped_source_drops_to_zero_richness():
    """Acceptance case: an anonymous-constructor equivalence proof built entirely from bare
    lambda arms (no genuine match arms, no real comparisons) must score ~0 richness -- this
    was batch 2's clearest false-positive (`Equiv.prodAssoc` ranked #4 on pure lambda-arm
    noise)."""
    v = _verified(
        "def prodAssoc (α β γ) : (α × β) × γ ≃ α × β × γ :=\n"
        "  ⟨fun p => (p.1.1, p.1.2, p.2), fun p => ((p.1, p.2.1), p.2.2), fun ⟨⟨_, _⟩, _⟩ => rfl,\n"
        "    fun ⟨_, ⟨_, _⟩⟩ => rfl⟩",
        [],
    )
    r = compute_richness(v)
    assert r.total == 0


def test_genuine_match_arm_still_counts_after_the_fix():
    """The fix must not throw out real match arms -- only bare lambda arms."""
    v = _verified("def foo : ℕ → ℕ | 0 => 0 | n + 1 => foo n", [])
    r = compute_richness(v)
    assert r.conditionals == 2


def test_genuine_greater_than_comparison_still_counts_after_the_fix():
    """The `=>`-exclusion fix must not eat a real, standalone `>` comparison -- only the `>`
    that is itself part of an arrow `=>` is excluded."""
    v = _verified(
        "def foo (a b : ℕ) : Prop := a > b",
        [BinderGroup(kind="explicit", names=["a", "b"], type_text="ℕ")],
    )
    r = compute_richness(v)
    assert r.comparisons == 1


def test_nat_clog_shaped_source_stays_top_richness_after_the_fix():
    """Acceptance case: Nat.clog's genuine fuel-recursive match arms and real comparisons
    must survive the fix essentially intact (only the double-counted bare `=` from its `=>`
    tokens should drop out)."""
    v = _verified(
        "def clog (b n : ℕ) : ℕ :=\n"
        "  if 1 < b ∧ 1 < n then (go b n).2 + 1 else 0 where\n"
        "  go : ℕ → ℕ → ℕ × ℕ\n"
        "  | b, 0 => (b / n, 0)\n"
        "  | b, fuel + 1 =>\n"
        "    if n ≤ b then (b / n, 0)\n"
        "    else\n"
        "      let (q, e) := go (b * b) fuel\n"
        "      if q < b then (q, 2 * e + 1) else (q / b, 2 * e)",
        [BinderGroup(kind="explicit", names=["b", "n"], type_text="ℕ")],
    )
    r = compute_richness(v)
    assert r.conditionals == 5  # 3 "if"s + 2 genuine match arms
    assert r.total > 8  # still clearly the richest shape in the corpus


def test_implicit_and_instance_binders_are_not_counted_as_hypothesis_binders():
    """Only explicit binders count -- implicit type variables and instance arguments are
    plumbing, not side conditions, even when their type text happens to contain a Prop-like
    marker."""
    v = _verified(
        "def foo {α : Type*} [DecidableEq α] (a b : α) : Prop := a = b",
        [
            BinderGroup(kind="implicit", names=["α"], type_text="Type*"),
            BinderGroup(kind="instance", names=[], type_text="DecidableEq α"),
            BinderGroup(kind="explicit", names=["a", "b"], type_text="α"),
        ],
    )
    r = compute_richness(v)
    assert r.hypothesis_binders == 0
