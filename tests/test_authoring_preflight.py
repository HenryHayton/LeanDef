"""Tests for `authoring.preflight` -- the promoted print-then-reparse signature-pinning check.
`check_output_to_pinned_type`/`_split_top_level_groups` are pure text; `run_preflight` needs a
real warm Mathlib environment (there's no ground truth to fake for "does this actually
re-elaborate")."""

import pytest

from authoring.preflight import (
    FAIL_INVALID_SYMBOL,
    FAIL_PP_ELISION,
    check_output_to_pinned_type,
    run_preflight,
    write_preflight_json,
    load_preflight_json,
)
from harness.repl import get_warm_environment
from harness.results import CheckStatus


@pytest.fixture(scope="module")
def mathlib_env():
    server, import_result = get_warm_environment()
    assert import_result.status is CheckStatus.PASSED, import_result.detail
    yield server, import_result.env
    server.kill()


# --- check_output_to_pinned_type (pure) --------------------------------------------------------


@pytest.mark.parametrize(
    "raw,name,expected",
    [
        ("Nat.clog (b n : ℕ) : ℕ", "Nat.clog", "(b n : ℕ) -> ℕ"),
        ("Nat.choose : ℕ → ℕ → ℕ", "Nat.choose", "ℕ → ℕ → ℕ"),
        (
            "Monotone.{u, v} {α : Type u} {β : Type v} [Preorder α] [Preorder β] (f : α → β) : Prop",
            "Monotone",
            "{α : Type u} -> {β : Type v} -> [Preorder α] -> [Preorder β] -> (f : α → β) -> Prop",
        ),
        (
            "Nat.findGreatest (P : ℕ → Prop) [DecidablePred P] : ℕ → ℕ",
            "Nat.findGreatest",
            "(P : ℕ → Prop) -> [DecidablePred P] -> ℕ → ℕ",
        ),
    ],
)
def test_check_output_to_pinned_type_matches_known_real_cases(raw, name, expected):
    """These four are exactly the real `#check` outputs and hand-validated pinned types from
    the 2026-07-28 batch-50 preflight session -- regression-pinned so a refactor of the
    bracket-depth scanner can't silently drift from real, previously-confirmed-correct output."""
    assert check_output_to_pinned_type(raw, name) == expected


def test_check_output_to_pinned_type_rejects_mismatched_name():
    with pytest.raises(ValueError):
        check_output_to_pinned_type("Other.name : ℕ", "Nat.clog")


# --- run_preflight (real REPL) ------------------------------------------------------------------


def test_run_preflight_passes_a_clean_definition(mathlib_env):
    server, env = mathlib_env
    results = run_preflight(["Nat.clog"], server, env)
    assert len(results) == 1
    r = results[0]
    assert r.status == "pass"
    assert r.pinned_type is not None
    assert r.task_symbol == "VTask.clog"


def test_run_preflight_categorizes_pp_elision(mathlib_env):
    """`Nat.leRec` -- one of the 6 real recursor-class pp-elision cases characterized
    2026-07-29 (`miner/output/excluded_recursor_class.json`)."""
    server, env = mathlib_env
    results = run_preflight(["Nat.leRec"], server, env)
    assert results[0].status == "fail"
    assert results[0].category == FAIL_PP_ELISION


def test_run_preflight_categorizes_invalid_symbol_without_any_repl_call(mathlib_env):
    """`Finset.sumLift₂`'s subscript makes `task_symbol_for` raise before any REPL round-trip
    -- confirmed by using a name that isn't even real Mathlib vocabulary; if this reached the
    REPL it would come back some other failure category, not `invalid_symbol`."""
    server, env = mathlib_env
    results = run_preflight(["NotReal.sumLift₂"], server, env)
    assert results[0].status == "fail"
    assert results[0].category == FAIL_INVALID_SYMBOL


def test_run_preflight_one_bad_name_does_not_stop_the_rest(mathlib_env):
    server, env = mathlib_env
    results = run_preflight(["Nat.leRec", "Nat.clog"], server, env)
    assert len(results) == 2
    by_name = {r.name: r for r in results}
    assert by_name["Nat.leRec"].status == "fail"
    assert by_name["Nat.clog"].status == "pass"


def test_write_and_load_preflight_json_round_trips(mathlib_env, tmp_path):
    server, env = mathlib_env
    results = run_preflight(["Nat.clog", "Nat.leRec"], server, env)
    path = tmp_path / "preflight.json"
    write_preflight_json(results, path)
    loaded = load_preflight_json(path)
    assert loaded["Nat.clog"].status == "pass"
    assert loaded["Nat.leRec"].status == "fail"
    assert loaded["Nat.leRec"].category == FAIL_PP_ELISION
