"""Candidate-side splice parity with the truth side (Stage A, 2026-08-04).

Two protections existed only on the truth-splice path (`splice_real_name`) and not on the
candidate path: `_root_.` qualification and the `noncomputable` retry. Both turn a CORRECT
candidate into a `COMPILE_ERROR` admissibility failure, and both do so differentially -- they
punish precisely the Lean-fluent output styles that reference real declarations by their bare
name or reach for classical constructions. Scoring the prelim candidates before fixing them
would have measured output style as much as faithfulness.

Split deliberately:

- **Ladder logic** (which path is taken, how many retries are consumed, what is preserved on
  total failure) is tested against a scripted fake server. These are pure decisions about error
  strings; a real Lean environment would make them slow without making them stronger.
- **The error shapes themselves** are tested against real Mathlib (`mathlib_env`), because the
  entire retry trigger is a claim about what Lean actually says. Faking those strings would
  test only that this file agrees with itself.
"""

import pytest
from lean_interact.interface import CommandResponse, Message, Pos

from harness.repl import run_checked
from harness.results import CheckStatus, SplicePath
from harness.scoring import (
    splice_candidate_body,
    splice_candidate_declaration,
    splice_real_name,
)
from harness.signature import PinnedSignature
from lean_interact import Command


# The two real Lean error strings the retries key on. `well-founded recursion` is asserted
# verbatim against live Mathlib in `test_bare_self_reference_really_does_fail_this_way`.
WELL_FOUNDED = (
    "fail to show termination for\n  VTask.Monotone\nwith errors\nstructural recursion cannot be used\n\n"
    "well-founded recursion cannot be used, 'VTask.Monotone' does not take any (non-instance) arguments"
)
NONCOMPUTABLE = (
    "failed to compile definition, consider marking it as 'noncomputable' because it depends on "
    "'Real.decidableLT', which is 'noncomputable'"
)
# Lean's SECOND noncomputable phrasing, from a different point in the compiler and matching none
# of the first's wording -- different verb ("marking definition" vs "marking it"), backticks
# rather than single quotes, no "failed to compile definition" preamble. Confirmed verbatim
# against live Lean v4.32.2 (2026-08-07). It fires only when the body names `Classical.choice`
# DIRECTLY; routing through `Classical.choose` produces the first phrasing instead, which is why
# this went unnoticed until the prefill work made the retry load-bearing.
NONCOMPUTABLE_DIRECT_CHOICE = (
    "`Classical.choice` not supported by code generator; consider marking definition as "
    "`noncomputable`"
)

MONOTONE = PinnedSignature(
    name="VTask.Monotone",
    type_sig="{α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> Prop",
)
CLOG = PinnedSignature(name="VTask.clog", type_sig="(b n : ℕ) -> ℕ")


def _err(data: str) -> Message:
    return Message(start_pos=Pos(line=1, column=1), end_pos=None, severity="error", data=data)


class _FakeServer:
    """Scripted responses in order, matching `tests/test_ladder_tier2.py`'s `_FakeServer`.
    `cmds` records every command text sent, which is what lets these tests assert on the
    REWRITTEN body rather than merely on the returned path."""

    def __init__(self, script):
        self.script = list(script)
        self.cmds: list[str] = []

    def run(self, request, timeout=None):
        self.cmds.append(request.cmd)
        if not self.script:
            raise AssertionError(f"fake server ran out of responses at: {request.cmd!r}")
        return self.script.pop(0)


def _ok(env=7):
    return CommandResponse(env=env, messages=[])


def _fail(data):
    return CommandResponse(env=1, messages=[_err(data)])


# --- the four enumerated paths --------------------------------------------------------------


def test_candidate_needing_nothing_takes_the_plain_path_with_zero_retries():
    server = _FakeServer([_ok()])
    outcome = splice_candidate_body(server, 0, CLOG, "fun b n => Nat.log b n + 1")

    assert outcome.succeeded
    assert outcome.path is SplicePath.PLAIN
    assert outcome.retries_consumed == 0
    assert len(server.cmds) == 1  # exactly one REPL round-trip on the common path


def test_shadowed_reference_candidate_is_rescued_by_root_qualification():
    """The Fix-1 case: a body for `VTask.Monotone` referencing the bare real `Monotone`."""
    server = _FakeServer([_fail(WELL_FOUNDED), _ok()])
    outcome = splice_candidate_body(server, 0, MONOTONE, "fun f => Monotone f")

    assert outcome.succeeded
    assert outcome.path is SplicePath.ROOT_QUALIFIED
    assert outcome.retries_consumed == 1
    assert "_root_.Monotone f" in server.cmds[1]
    assert "_root_._root_" not in server.cmds[1]  # qualified once, not compounded


def test_noncomputable_candidate_is_rescued_by_the_modifier_retry():
    """The Fix-2 case, mirroring `splice_real_name`'s existing truth-side behaviour."""
    server = _FakeServer([_fail(NONCOMPUTABLE), _ok()])
    outcome = splice_candidate_body(server, 0, CLOG, "fun b n => Classical.choice inferInstance")

    assert outcome.succeeded
    assert outcome.path is SplicePath.NONCOMPUTABLE
    assert outcome.retries_consumed == 1
    assert server.cmds[1].startswith("@[reducible] noncomputable def VTask.clog")


def test_both_of_leans_noncomputable_phrasings_trigger_the_retry():
    """Matching only the first phrasing recorded a correct classical candidate as COMPILE_ERROR.

    The declaration path is checked alongside the body path because the prefill intervention
    (`pretuning.decode`) sends declarations, and a prefilled candidate cannot write
    `noncomputable` for itself -- the prefix already consumed the modifier slot, so this retry is
    the only thing between a classical definition and a false compile error in T2/T3.
    """
    for splice, arg in ((splice_candidate_body, "fun _ _ => Classical.choice inferInstance"),
                        (splice_candidate_declaration,
                         "def VTask.clog : (b n : ℕ) -> ℕ := Classical.choice inferInstance")):
        server = _FakeServer([_fail(NONCOMPUTABLE_DIRECT_CHOICE), _ok()])
        outcome = splice(server, 0, CLOG, arg)
        assert outcome.succeeded, splice.__name__
        assert outcome.path is SplicePath.NONCOMPUTABLE, splice.__name__
        assert "noncomputable def VTask.clog" in server.cmds[1]


def test_candidate_needing_both_converges_on_the_combined_path():
    """Self-reference first, then noncomputable on the rewritten body -- the 1 -> 3 -> 4 chain."""
    server = _FakeServer([_fail(WELL_FOUNDED), _fail(NONCOMPUTABLE), _ok()])
    outcome = splice_candidate_body(server, 0, MONOTONE, "fun f => Monotone f")

    assert outcome.succeeded
    assert outcome.path is SplicePath.ROOT_QUALIFIED_NONCOMPUTABLE
    assert outcome.retries_consumed == 2
    assert server.cmds[2].startswith("@[reducible] noncomputable def VTask.Monotone")
    assert "_root_.Monotone" in server.cmds[2]


def test_the_other_arrival_order_reaches_the_same_combined_path():
    """Noncomputable first, then self-reference -- the 1 -> 2 -> 4 chain. Both orders must
    converge, and neither may revisit a state."""
    server = _FakeServer([_fail(NONCOMPUTABLE), _fail(WELL_FOUNDED), _ok()])
    outcome = splice_candidate_body(server, 0, MONOTONE, "fun f => Monotone f")

    assert outcome.succeeded
    assert outcome.path is SplicePath.ROOT_QUALIFIED_NONCOMPUTABLE
    assert len(server.cmds) == 3


# --- the guards: when the rewrite must NOT happen ---------------------------------------------


def test_genuinely_recursive_candidate_is_never_rewritten():
    """A body naming the task symbol IN FULL has declared its intent to recurse. It must fail
    on its own terms -- not be silently rewritten into a different definition."""
    body = "fun b n => if n <= 1 then 0 else VTask.clog b (n / b) + 1"
    server = _FakeServer([_fail(WELL_FOUNDED)])
    outcome = splice_candidate_body(server, 0, CLOG, body)

    assert not outcome.succeeded
    assert outcome.path is SplicePath.PLAIN
    assert outcome.retries_consumed == 0
    assert len(server.cmds) == 1  # no retry was even attempted
    assert "VTask.clog b (n / b)" in server.cmds[0]  # body sent through untouched


def test_recursive_candidate_that_compiles_is_left_alone():
    server = _FakeServer([_ok()])
    outcome = splice_candidate_body(server, 0, CLOG, "fun b n => VTask.clog b n")

    assert outcome.succeeded
    assert outcome.path is SplicePath.PLAIN
    assert server.cmds[0].endswith(":= fun b n => VTask.clog b n")


def test_termination_error_with_nothing_to_rewrite_does_not_retry():
    """A real termination failure in a body that never mentions the base name is a real
    termination failure. Retrying would re-send byte-identical text."""
    server = _FakeServer([_fail(WELL_FOUNDED)])
    outcome = splice_candidate_body(server, 0, CLOG, "fun b n => Nat.log b n")

    assert not outcome.succeeded
    assert len(server.cmds) == 1


def test_an_unrelated_compile_error_triggers_no_retry_at_all():
    server = _FakeServer([_fail("type mismatch: expected ℕ, got Prop")])
    outcome = splice_candidate_body(server, 0, MONOTONE, "fun f => Monotone f")

    assert not outcome.succeeded
    assert outcome.retries_consumed == 0
    assert len(server.cmds) == 1


def test_dotted_references_are_not_rewritten():
    """`Nat.clog` already resolves correctly; only the BARE base name mis-resolves."""
    rewritten, n = CLOG.root_qualified_body("fun b n => Nat.clog b n + clog2 b n")
    assert n == 0
    assert rewritten == "fun b n => Nat.clog b n + clog2 b n"


def test_primed_identifier_is_not_rewritten():
    """`LEAN_IDENT_CHAR` treats `'` as an identifier character -- the `Equiv.ofLeftInverse'`
    false-positive class `authoring.namematch` documents."""
    sig = PinnedSignature(name="VTask.ofLeftInverse", type_sig="Nat -> Nat")
    _, n = sig.root_qualified_body("fun x => ofLeftInverse' x")
    assert n == 0


# --- total failure preserves the primary diagnostic -------------------------------------------


def test_failure_on_every_path_reports_the_plain_error_as_primary():
    """The funnel must not be polluted by retry noise: `result` is the PLAIN attempt's, and the
    rescue errors are available separately."""
    server = _FakeServer([_fail(WELL_FOUNDED), _fail("rewritten body still broken")])
    outcome = splice_candidate_body(server, 0, MONOTONE, "fun f => Monotone f")

    assert not outcome.succeeded
    assert outcome.path is SplicePath.PLAIN
    assert "well-founded recursion" in outcome.result.detail  # primary = plain attempt
    assert outcome.retries_consumed == 1
    assert any("rewritten body still broken" in d for d in outcome.secondary_details)
    assert len(outcome.attempts) == 2  # every attempt kept


def test_errored_attempt_stops_the_ladder_immediately():
    """Infrastructure failure is not evidence about the candidate; retrying against a possibly
    dead server would only confuse the diagnosis."""
    class _DeadServer:
        def __init__(self):
            self.calls = 0

        def run(self, request, timeout=None):
            self.calls += 1
            raise TimeoutError("server wedged")

    server = _DeadServer()
    outcome = splice_candidate_body(server, 0, MONOTONE, "fun f => Monotone f")

    assert outcome.result.status is CheckStatus.ERRORED
    assert outcome.retries_consumed == 0
    assert len(outcome.attempts) == 1  # the ladder stopped; no variant was tried


# --- truth-side byte-identity regression ------------------------------------------------------


@pytest.mark.parametrize(
    "symbol,type_sig,real_name",
    [
        # a Prop-valued task -- the @[reducible] path that makes Decidable instances resolve
        ("VTask.Monotone", "{α : Type u} -> {β : Type v} -> (f : α → β) -> Prop", "Monotone"),
        ("VTask.ModEq", "(n a b : ℕ) -> Prop", "Nat.ModEq"),
        ("VTask.clog", "(b n : ℕ) -> ℕ", "Nat.clog"),
    ],
)
def test_truth_splice_text_is_byte_identical_after_the_refactor(symbol, type_sig, real_name):
    """`splice_real_name` now routes through the shared `root_qualify`; the emitted text must
    not have moved by a single byte."""
    sig = PinnedSignature(name=symbol, type_sig=type_sig)
    assert sig.splice_real_name(real_name) == f"@[reducible] def {symbol} : {type_sig} := _root_.{real_name}"
    assert (
        sig.splice_real_name(real_name, noncomputable=True)
        == f"@[reducible] noncomputable def {symbol} : {type_sig} := _root_.{real_name}"
    )


def test_plain_splice_is_unchanged_for_existing_single_argument_callers():
    """`splice(body)` gained a keyword-only `noncomputable` defaulting to False -- every
    existing call site must emit exactly what it emitted before."""
    assert CLOG.splice("fun b n => n") == "@[reducible] def VTask.clog : (b n : ℕ) -> ℕ := fun b n => n"


# --- real Lean: the error shapes the triggers depend on ---------------------------------------


def test_bare_self_reference_really_does_fail_this_way(mathlib_env):
    """Ground truth for the Fix-1 trigger: confirm live Mathlib still produces a
    `_SELF_REFERENCE_ERROR_MARKERS` string for the bare-name collision. If Lean ever rewords
    this, the retry silently stops firing -- so this test is the canary."""
    server, env = mathlib_env
    sig = PinnedSignature(
        name="VTask.Monotone",
        type_sig="{α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> Prop",
    )
    bare = run_checked(server, Command(cmd=sig.splice("Monotone"), env=env), timeout=30.0)

    assert bare.status is CheckStatus.FAILED
    from harness.scoring import _looks_like_self_reference

    assert _looks_like_self_reference(bare.detail), bare.detail


def test_candidate_ladder_rescues_the_real_self_reference_against_live_mathlib(mathlib_env):
    """End-to-end: the exact shape that fails today, rescued, against a real environment."""
    server, env = mathlib_env
    sig = PinnedSignature(
        name="VTask.Monotone",
        type_sig="{α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> Prop",
    )
    outcome = splice_candidate_body(server, env, sig, "Monotone", timeout=30.0)

    assert outcome.succeeded, outcome.result.detail
    assert outcome.path is SplicePath.ROOT_QUALIFIED
    assert outcome.retries_consumed == 1


def test_candidate_ladder_rescues_a_real_noncomputable_body(mathlib_env):
    """`Function.extend` is noncomputable at an alias site despite its own source line carrying
    no `noncomputable` keyword -- the real case that motivated the truth-side retry."""
    server, env = mathlib_env
    sig = PinnedSignature(
        name="VTask.extend",
        type_sig="{α : Sort u_1} -> {β : Sort u_2} -> {γ : Sort u_3} -> (f : α → β) -> (g : α → γ) -> (j : β → γ) -> β → γ",
    )
    outcome = splice_candidate_body(server, env, sig, "Function.extend", timeout=30.0)

    assert outcome.succeeded, outcome.result.detail
    assert outcome.path is SplicePath.NONCOMPUTABLE
    assert outcome.retries_consumed == 1


def test_truth_side_still_passes_on_the_same_real_cases(mathlib_env):
    """Truth-path regression against live Mathlib, not just string equality."""
    server, env = mathlib_env
    sig = PinnedSignature(
        name="VTask.extend",
        type_sig="{α : Sort u_1} -> {β : Sort u_2} -> {γ : Sort u_3} -> (f : α → β) -> (g : α → γ) -> (j : β → γ) -> β → γ",
    )
    result = splice_real_name(server, env, sig, "Function.extend", timeout=30.0)
    assert result.status is CheckStatus.PASSED, result.detail
