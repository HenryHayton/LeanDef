"""The SELF_DELEGATION admissibility gate.

**What it is for.** A candidate whose body invokes the very object it is supposed to define
(`def VTask.clog := Nat.clog`) is a tautology. It compiles, it has the pinned type, and it passes
every fact the real object passes -- so it scores like a perfect answer while demonstrating
nothing about whether the model can construct anything. 22 of the prelim's 116 survivors were
this shape.

**The line the gate draws**: using the library is legal, using the object under definition is not.
A `clog` candidate built out of `Nat.log` is an honest construction and must pass; the same
candidate built out of `Nat.clog` must not.

Split deliberately:

- **Matcher semantics** are unit-tested. They are claims about names, and `authoring.namematch`
  is already the single tested matcher for them -- these tests pin the four behaviours this gate
  depends on, so a future edit there cannot silently change what counts as self-delegation.
- **Closure extraction** is tested against real Mathlib, because the entire gate rests on a claim
  about what the Lean elaborator puts in a declaration's value. Faking the constant list would
  test only that this file agrees with itself.
"""

import pytest
from lean_interact import Command

from harness.admissibility import (
    AdmissibilityFailure,
    check_admissibility,
    parse_used_constants,
    parse_wrapper_expansions,
    self_delegating_constants,
    used_constants_command,
)
from harness.repl import run_checked
from harness.results import CheckStatus
from harness.scoring import splice_candidate_declaration
from harness.signature import PinnedSignature

CLOG = PinnedSignature(name="VTask.clog", type_sig="(b n : ℕ) -> ℕ")
MONOTONE = PinnedSignature(
    name="VTask.Monotone",
    type_sig="{α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> Prop",
)


# --- matcher semantics (no Lean needed) -------------------------------------------------------


def test_the_target_and_its_generated_companions_trip():
    """Lean auto-generates `Nat.clog.eq_1`, `.induct`, `.eq_def` beside a definition. Reaching the
    target through one of those is the same delegation by a different door."""
    consts = frozenset({"Nat.clog", "Nat.clog.eq_1", "Nat.clog.induct", "Nat.clog.eq_def"})
    assert self_delegating_constants(consts, "Nat.clog") == sorted(consts)


def test_using_a_different_library_definition_does_not_trip():
    """The whole point of the gate: `Nat.log` inside a `clog` candidate is honest construction."""
    consts = frozenset({"Nat.log", "Nat.rec", "HAdd.hAdd", "instAddNat", "ite", "Nat.decLe"})
    assert self_delegating_constants(consts, "Nat.clog") == []


def test_a_differently_named_declaration_does_not_trip():
    """`Nat.clog2` is a distinct declaration. This is the exact false-positive class
    `authoring.namematch` exists to kill -- an identifier-boundary match, not a substring one."""
    assert self_delegating_constants(frozenset({"Nat.clog2"}), "Nat.clog") == []
    assert self_delegating_constants(frozenset({"Equiv.ofLeftInverse'"}),
                                     "Equiv.ofLeftInverse") == []


def test_recursion_through_the_task_symbol_does_not_trip_an_unnamespaced_target():
    """The interaction that would otherwise break legitimate recursion.

    For a task mined from an UNNAMESPACED real name, the task symbol contains the real name:
    `VTask.Monotone` contains `Monotone`. A naive matcher flags the very symbol a recursive
    candidate is required to use. `exclude_task_symbol` is what prevents that, and this test is
    the reason the gate reuses `namematch` instead of rolling its own comparison.
    """
    assert self_delegating_constants(frozenset({"VTask.Monotone"}), "Monotone") == []
    assert self_delegating_constants(frozenset({"Monotone"}), "Monotone") == ["Monotone"]


def test_a_probe_that_produced_no_marker_is_distinguishable_from_no_constants():
    """Silence must not read as innocence -- the caller turns `None` into ERRORED, not admitted."""

    class _Raw:
        messages = []

    assert parse_used_constants(_Raw()) is None


def test_the_probe_command_names_the_pinned_symbol_as_its_root():
    cmd = used_constants_command(CLOG)
    assert "`VTask.clog" in cmd and "USEDCONSTS" in cmd


# --- closure extraction, against real Mathlib -------------------------------------------------


def _closure(server, env, signature):
    result = run_checked(server, Command(cmd=used_constants_command(signature), env=env),
                         timeout=60.0)
    assert result.status is CheckStatus.PASSED, result.detail
    consts = parse_used_constants(result.raw_response)
    assert consts is not None
    return consts


def _splice(server, env, signature, decl):
    outcome = splice_candidate_declaration(server, env, signature, decl)
    assert outcome.result.status is CheckStatus.PASSED, outcome.result.detail
    return outcome.result.env


@pytest.mark.parametrize(
    "label,decl,real_name,expect_trip",
    [
        # (a) the bare alias -- the 22-survivor shape
        ("alias", "def VTask.choose : (n k : ℕ) -> ℕ := Nat.choose", "Nat.choose", True),
        # (b) the wrapper -- boundary special-cased, target invoked for everything else
        ("wrapper",
         "def VTask.clog : (b n : ℕ) -> ℕ := fun b n => if b ≤ 1 then 0 else Nat.clog b n",
         "Nat.clog", True),
        # (c) the honest construction -- built from a DIFFERENT primitive
        ("honest",
         "def VTask.clog : (b n : ℕ) -> ℕ := fun b n => "
         "if b ≤ 1 ∨ n ≤ 1 then 0 else Nat.log b (n - 1) + 1",
         "Nat.clog", False),
    ],
)
def test_closure_gate_on_real_mathlib(mathlib_env, label, decl, real_name, expect_trip):
    server, env = mathlib_env
    sig = PinnedSignature(name=decl.split()[1], type_sig=decl.split(" : ", 1)[1].split(" := ")[0])
    candidate_env = _splice(server, env, sig, decl)
    verdict = check_admissibility(
        server, candidate_env, sig,
        splice_response=None, target_real_name=real_name, timeout=60.0,
    )
    tripped = verdict.failure is AdmissibilityFailure.SELF_DELEGATION
    assert tripped is expect_trip, f"{label}: {verdict.failure} {verdict.detail[:200]}"


def test_a_where_helper_smuggles_past_shadowing_but_not_past_the_closure(mathlib_env):
    """The case that justifies walking the closure rather than reading `declarations`.

    A `where` helper does NOT appear in the splice response's declaration list, so the
    NAME_SHADOWED gate never sees it -- confirmed live. The closure walk expands into it because
    its name is prefixed by the task symbol, and finds the target underneath.
    """
    server, env = mathlib_env
    decl = ("def VTask.clog : (b n : ℕ) -> ℕ := fun b n => go b n\n"
            "where go (b n : ℕ) : ℕ := Nat.clog b n")
    result = run_checked(server, Command(cmd=f"@[reducible] {decl}", env=env, declarations=True),
                         timeout=60.0)
    assert result.status is CheckStatus.PASSED, result.detail

    declared = {d.full_name or d.name for d in (result.raw_response.declarations or [])}
    assert declared == {"VTask.clog"}, f"the where-helper became visible: {declared}"

    consts = _closure(server, result.env, CLOG)
    assert "VTask.clog.go" in consts
    assert self_delegating_constants(consts, "Nat.clog") == ["Nat.clog"]


def test_legitimate_recursion_through_the_task_symbol_stays_admissible(mathlib_env):
    """(d) A structurally recursive candidate references `VTask.clog`, never `Nat.clog`."""
    server, env = mathlib_env
    decl = ("def VTask.clog : (b n : ℕ) -> ℕ := fun b n => "
            "match n with | 0 => 0 | Nat.succ k => VTask.clog b k")
    candidate_env = _splice(server, env, CLOG, decl)
    consts = _closure(server, candidate_env, CLOG)
    assert self_delegating_constants(consts, "Nat.clog") == []

    verdict = check_admissibility(server, candidate_env, CLOG, splice_response=None,
                                  target_real_name="Nat.clog", timeout=60.0)
    assert verdict.failure is not AdmissibilityFailure.SELF_DELEGATION


def test_root_qualification_does_not_manufacture_a_trip_for_an_innocent_body(mathlib_env):
    """The retry-path interaction the gate must not break.

    `_root_.` qualification rewrites bare occurrences of the task's BASE name. For an
    unnamespaced target (`Monotone`), that rewrite turns a self-reference into a real-name
    reference -- so the concern is whether the retry can convert an innocent candidate into a
    tripping one. It cannot: the rewrite only fires on the base name, so a body written out of
    other primitives is untouched by it and still passes.

    The converse is deliberate, not a defect: a body that IS `fun f => Monotone f` root-qualifies
    to `_root_.Monotone f`, which really does delegate to the target and really should trip. That
    half is asserted too, so the intent is on the record rather than inferred.
    """
    server, env = mathlib_env

    innocent = ("def VTask.Monotone {α : Type u} {β : Type v} [Preorder α] [Preorder β] "
                "(f : α → β) : Prop := ∀ a b, a ≤ b → f a ≤ f b")
    candidate_env = _splice(server, env, MONOTONE, innocent)
    verdict = check_admissibility(server, candidate_env, MONOTONE, splice_response=None,
                                  target_real_name="Monotone", timeout=60.0)
    assert verdict.failure is not AdmissibilityFailure.SELF_DELEGATION, verdict.detail

    aliasing = ("def VTask.Monotone {α : Type u} {β : Type v} [Preorder α] [Preorder β] "
                "(f : α → β) : Prop := Monotone f")
    outcome = splice_candidate_declaration(server, env, MONOTONE, aliasing)
    assert outcome.result.status is CheckStatus.PASSED, outcome.result.detail
    aliased_env = outcome.result.env
    verdict = check_admissibility(server, aliased_env, MONOTONE, splice_response=None,
                                  target_real_name="Monotone", timeout=60.0)
    assert verdict.failure is AdmissibilityFailure.SELF_DELEGATION, verdict.detail


def test_no_target_name_supplied_means_the_gate_is_skipped(mathlib_env):
    """Callers without mined provenance (authoring round-trips, synthetic tests) must not all
    become inadmissible. The gate is skipped, not failed closed."""
    server, env = mathlib_env
    decl = "def VTask.choose : (n k : ℕ) -> ℕ := Nat.choose"
    sig = PinnedSignature(name="VTask.choose", type_sig="(n k : ℕ) -> ℕ")
    candidate_env = _splice(server, env, sig, decl)
    verdict = check_admissibility(server, candidate_env, sig, splice_response=None, timeout=60.0)
    assert verdict.failure is not AdmissibilityFailure.SELF_DELEGATION


def test_a_thin_library_wrapper_around_the_target_is_still_delegation(mathlib_env):
    """The route the first version of this gate missed, found in live 32B output.

    `Finset.strongInductionOn` is literally `fun {α} {p} s H => Finset.strongInduction H s` -- an
    argument-swap wrapper. A candidate for `Finset.strongInduction` that calls it is defining the
    target by calling the target, one hop away, while naming a different constant. The original
    closure walk stopped at Mathlib constants and scored this ADMITTED.
    """
    server, env = mathlib_env
    sig = PinnedSignature(
        name="VTask.strongInduction",
        type_sig="{α : Type u_1} -> {p : Finset α → Sort u_4} -> "
                 "(H : (s : Finset α) → ((t : Finset α) → t ⊂ s → p t) → p s) → (s : Finset α) → p s",
    )
    decl = ("def VTask.strongInduction : {α : Type u_1} -> {p : Finset α → Sort u_4} -> "
            "(H : (s : Finset α) → ((t : Finset α) → t ⊂ s → p t) → p s) → (s : Finset α) → p s := "
            "fun {α} {p} H s => Finset.strongInductionOn s (fun s ih => H s (fun t ht => ih t ht))")
    candidate_env = _splice(server, env, sig, decl)

    # NOTE: for this particular splice Lean unfolds `strongInductionOn`, so the target already
    # appears in the DIRECT closure and the gate would catch it even without wrapper expansion.
    # Whether it unfolds is an elaboration detail that varies with how the candidate is written,
    # which is exactly why the wrapper level exists -- it removes the dependence on that luck.
    verdict = check_admissibility(server, candidate_env, sig, splice_response=None,
                                  target_real_name="Finset.strongInduction", timeout=60.0)
    assert verdict.failure is AdmissibilityFailure.SELF_DELEGATION, verdict.detail


def test_a_substantial_library_definition_is_not_expanded_as_a_wrapper(mathlib_env):
    """The bound that keeps this from becoming the unbounded Mathlib walk. An honest `clog`
    candidate built from `Nat.log` must stay admissible -- `Nat.log` does real work and is not a
    thin re-presentation of anything."""
    server, env = mathlib_env
    decl = ("def VTask.clog : (b n : ℕ) -> ℕ := fun b n => "
            "if b ≤ 1 ∨ n ≤ 1 then 0 else Nat.log b (n - 1) + 1")
    candidate_env = _splice(server, env, CLOG, decl)
    verdict = check_admissibility(server, candidate_env, CLOG, splice_response=None,
                                  target_real_name="Nat.clog", timeout=60.0)
    assert verdict.failure is not AdmissibilityFailure.SELF_DELEGATION, verdict.detail


def test_wrapper_expansions_parse_into_parent_child_sets():
    class _M:
        data = "WRAPPER Finset.strongInductionOn Finset.strongInduction Finset\nWRAPPER A B"

    class _Raw:
        messages = [_M()]

    got = parse_wrapper_expansions(_Raw())
    assert got["Finset.strongInductionOn"] == frozenset({"Finset.strongInduction", "Finset"})
    assert got["A"] == frozenset({"B"})
    assert parse_wrapper_expansions(type("R", (), {"messages": []})()) == {}
