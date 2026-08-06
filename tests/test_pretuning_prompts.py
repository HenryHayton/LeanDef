"""Tests for the pre-tuning prompt architecture.

The leak guard is the load-bearing test. Unlike the prelim's, it runs over the FULLY ASSEMBLED
prompt including exemplar text -- the exemplars are real Mathlib definitions carrying real
Mathlib names by construction, so "no leak in the task block" is not the property that matters.
"""

import json
from pathlib import Path

import pytest

from prelim.prompts import available_tasks, load_task
from pretuning.cells import CELL_IDS, CELLS, R0, R1, S0, S_A, S_B, S_C
from pretuning.glossary import glossary_for, render_glossary
from pretuning.prompts import CONFORMANCE, build_prompt, check_prompt_leak, load_exemplars


@pytest.fixture(scope="module")
def tasks():
    t = available_tasks()
    if len(t) != 41:
        pytest.skip(f"expected the 41-task corpus, found {len(t)}")
    return t


@pytest.fixture(scope="module")
def reals():
    return {p.parent.name: (json.loads(p.read_text()).get("provenance") or {}).get("mathlib_name")
            for p in Path("prelim_testing/tasks").glob("*/task.json")}


# --- the design -----------------------------------------------------------------------------


def test_eight_distinct_cells():
    assert len(CELLS) == 8
    assert len(set(CELL_IDS)) == 8


def test_run_order_puts_the_plain_prohibition_control_last():
    """S-A is the control: it says whether either theory (S-B, S-C) was needed at all. Running
    it last lets analysis of the theory-bearing cells start while it generates."""
    assert [c.sorry_level for c in CELLS[-2:]] == [S_A, S_A]
    assert {c.sorry_level for c in CELLS[:6]} == {S0, S_B, S_C}


def test_s0_carries_no_anti_sorry_text_and_r0_carries_no_scaffold_text():
    """R0 must be genuinely unconstrained -- no nudge at all on that axis, so whatever structure
    the model chooses is data about its native prior."""
    from pretuning.cells import Cell

    assert Cell(S0, R0).anti_sorry_text == ""
    assert Cell(S0, R0).scaffold_text == ""
    assert Cell(S_C, R0).scaffold_text == ""


def test_sb_and_sc_encode_different_theories():
    """They are not two phrasings of one idea: S-B changes the decision norm under uncertainty,
    S-C denies the existence of a downstream prover. If they separate, that is a finding."""
    from pretuning.cells import Cell

    b, c = Cell(S_B, R0).anti_sorry_text, Cell(S_C, R0).anti_sorry_text
    assert "unsure" in b and "score" in b
    assert "downstream prover" in c
    assert b != c


# --- exemplars ------------------------------------------------------------------------------


def test_exemplars_are_verified_before_they_can_be_shipped():
    """An unverified exemplar would teach the model a definition that does not compile, in every
    prompt of every run. `load_exemplars` refuses rather than warns."""
    ex = load_exemplars()
    assert len(ex) == 3
    for e in ex:
        assert e["verified_compiles"] and e["verified_admissible"] and e["verified_type_matches"]
    assert [e["slot"] for e in ex] == [1, 2, 3]


def test_r1_cells_show_prose_and_r0_cells_do_not(tasks):
    d, sig = load_task(tasks[0])
    from pretuning.cells import Cell

    r1 = build_prompt(Cell(S0, R1), d, sig)
    r0 = build_prompt(Cell(S0, R0), d, sig)
    assert "### Characterization" in r1
    assert "### Characterization" not in r0
    # same three definitions either way
    for e in load_exemplars():
        assert e["definition"].strip().splitlines()[0] in r0
        assert e["definition"].strip().splitlines()[0] in r1


def test_every_cell_carries_the_conformance_instruction(tasks):
    d, sig = load_task(tasks[0])
    for c in CELLS:
        assert CONFORMANCE in build_prompt(c, d, sig)


# --- THE leak guard -------------------------------------------------------------------------


def test_no_task_real_name_appears_in_any_assembled_prompt(tasks, reals):
    """41 tasks x 8 cells = 328 prompts, exemplar text included."""
    offenders = []
    for t in tasks:
        d, sig = load_task(t)
        for c in CELLS:
            ok, detail = check_prompt_leak(build_prompt(c, d, sig), reals[t])
            if not ok:
                offenders.append((t, c.cell_id, detail))
    assert not offenders, f"leak in {len(offenders)} prompt(s): {offenders[:5]}"


def test_the_leak_guard_would_catch_a_planted_leak(tasks):
    """Positive control -- a guard that never fires is not a guard."""
    d, sig = load_task(tasks[0])
    poisoned = build_prompt(CELLS[0], d, sig) + "\n(also known as Nat.clog)\n"
    ok, _ = check_prompt_leak(poisoned, "Nat.clog")
    assert not ok


def test_exemplar_source_names_are_burned_from_task_selection():
    """The three exemplars must never be drawable as tasks -- otherwise a future run measures
    recall of our own prompt."""
    import yaml

    cur = yaml.safe_load(Path("miner/curation.yaml").read_text())
    burned = {e["name"] for e in cur["entries"]
              if e.get("action") == "exclude" and "exemplar" in (e.get("reason") or "")}
    assert {e["source_name"] for e in load_exemplars()} <= burned


# --- glossary -------------------------------------------------------------------------------


def test_glossary_is_meaning_level_not_implementation_advice():
    """A glossary entry may say what notation MEANS; it must never say what to write. Naming a
    constructor would be answering the question rather than supporting the reading."""
    banned = ("use ", "write ", "you should", "construct with", ".mk", "prefer ")
    for line in sum((glossary_for(t) for t in ("⦃x⦄ → Prop", "α →o α", "↑s", "∀ᶠ n in f", "[Group α]")), []):
        low = line.lower()
        for b in banned:
            assert b not in low, f"implementation advice in glossary: {line!r}"


def test_glossary_only_covers_notation_actually_present():
    assert glossary_for("(b n : ℕ) -> ℕ") == []
    assert render_glossary("(b n : ℕ) -> ℕ") == ""
    assert any("strict implicit" in ln for ln in glossary_for("⦃x : α⦄ -> Prop"))
    assert not any("bundled monotone" in ln for ln in glossary_for("⦃x : α⦄ -> Prop"))


def test_determinism(tasks):
    """The store's prompt hash is only a useful key if assembly is byte-stable."""
    d, sig = load_task(tasks[0])
    for c in CELLS:
        assert build_prompt(c, d, sig) == build_prompt(c, d, sig)
