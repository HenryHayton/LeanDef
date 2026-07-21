"""Unit tests for miner.verify's `#check`-output parsing, using synthetic (but verbatim-
observed) type strings -- no REPL involved.

Regression tests for the arity-parsing bug found reviewing harvest batch 1: universe-
polymorphic definitions (`Pairwise`, `Function.Bijective`, ...) were recorded with zero
explicit arguments because `#check`'s output attaches a `.{u_1}`-style universe annotation
directly to the name, which the old parser didn't know to skip. A second, related gap:
trailing *anonymous* explicit arguments (e.g. from an enclosing `variable` declaration not
written in the `def`'s own header) show up as a bare arrow chain rather than a named group,
and need counting via `_split_top_level_arrows`, not just named binder groups.
"""

from miner.verify import (
    _explicit_arg_types,
    _parse_binder_groups,
    _split_check_output,
    _split_top_level_arrows,
    _strip_universe_annotation,
)


def _arity_and_return(message: str, name: str) -> tuple[list[str], str]:
    """Mirrors the parsing steps inside verify_definition, for testing in isolation."""
    binders_text, raw_return_type = _split_check_output(message, name)
    groups = _parse_binder_groups(binders_text)
    arrow_segments = _split_top_level_arrows(raw_return_type)
    trailing_arg_types, return_type = arrow_segments[:-1], arrow_segments[-1]
    return _explicit_arg_types(groups) + trailing_arg_types, return_type


# --- _strip_universe_annotation ---


def test_strip_universe_annotation_single_param():
    assert _strip_universe_annotation(".{u_1} {α : Type u_1} : Prop") == " {α : Type u_1} : Prop"


def test_strip_universe_annotation_multiple_params():
    assert _strip_universe_annotation(".{u₁, u₂} (f : α → β) : Prop") == " (f : α → β) : Prop"


def test_strip_universe_annotation_absent_is_noop():
    assert _strip_universe_annotation(" (n : ℕ) : ℕ") == " (n : ℕ) : ℕ"


# --- _split_top_level_arrows ---


def test_split_top_level_arrows_simple():
    assert _split_top_level_arrows("List α → List α") == ["List α", "List α"]


def test_split_top_level_arrows_no_arrow():
    assert _split_top_level_arrows("Prop") == ["Prop"]


def test_split_top_level_arrows_nested_arrow_not_split():
    # the arrow inside the parens is not top-level and must not be split on
    assert _split_top_level_arrows("(Nat → Nat) → Nat") == ["(Nat → Nat)", "Nat"]


def test_split_top_level_arrows_three_segments():
    assert _split_top_level_arrows("ℕ → ℕ → ℕ") == ["ℕ", "ℕ", "ℕ"]


# --- End-to-end regression tests: exact #check output observed for the batch-1 zero-arity cases ---


def test_pairwise_arity_regression():
    msg = "Pairwise.{u_1} {α : Type u_1} (r : α → α → Prop) : Prop"
    arg_types, return_type = _arity_and_return(msg, "Pairwise")
    assert arg_types == ["α → α → Prop"]
    assert return_type == "Prop"


def test_function_bijective_arity_regression():
    msg = "Function.Bijective.{u₁, u₂} {α : Sort u₁} {β : Sort u₂} (f : α → β) : Prop"
    arg_types, return_type = _arity_and_return(msg, "Function.Bijective")
    assert arg_types == ["α → β"]
    assert return_type == "Prop"


def test_list_orderedinsert_arity_regression():
    """The trailing `List α → List α` is a bare arrow chain -- an anonymous explicit
    argument (the list) plus the true return type -- not itself a return type of function
    shape. True arity is 3: r, a, and the anonymous list argument."""
    msg = (
        "List.orderedInsert.{u_1} {α : Type u_1} (r : α → α → Prop) [DecidableRel r] "
        "(a : α) : List α → List α"
    )
    arg_types, return_type = _arity_and_return(msg, "List.orderedInsert")
    assert arg_types == ["α → α → Prop", "α", "List α"]
    assert return_type == "List α"


def test_list_kerase_arity_regression():
    msg = (
        "List.kerase.{u, v} {α : Type u} {β : α → Type v} [DecidableEq α] (a : α) : "
        "List (Sigma β) → List (Sigma β)"
    )
    arg_types, return_type = _arity_and_return(msg, "List.kerase")
    assert arg_types == ["α", "List (Sigma β)"]
    assert return_type == "List (Sigma β)"


def test_nat_prime_arity_unaffected_by_fix():
    """Nat.Prime has no universe polymorphism and no trailing anonymous argument -- confirms
    the fix doesn't disturb the simple, already-correct case."""
    msg = "Nat.Prime (p : ℕ) : Prop"
    arg_types, return_type = _arity_and_return(msg, "Nat.Prime")
    assert arg_types == ["ℕ"]
    assert return_type == "Prop"
