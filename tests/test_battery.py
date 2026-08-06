"""Tests for the decode/exemplar battery: token ban, prefill, exemplar presentation modes.

Two of these are load-bearing rather than routine, and both guard against the same failure shape
-- an intervention that is *absent* rather than *ineffective*, which is invisible in the output
and would be read as "the intervention did not work":

- `test_a_ban_cell_refuses_to_run_without_resolved_variants` -- T1/T3 with an empty ban list are
  byte-identical to T0, and would silently report the null result as a finding.
- `test_prefill_reaches_the_wire_and_the_stored_completion` -- if the prefix never reaches the
  server, or reaches it but is not re-attached to the stored completion, T2/T3 measure a prompt
  they did not run or a declaration missing its head.
"""

import json

import pytest

from harness.signature import PinnedSignature, reducible_declaration
from prelim.extract import Extraction, extract_definition
from prelim.prompts import available_tasks, load_task
from prelim.stubserver import ScriptedResponse, StubEndpointServer, sse_stream
from pretuning import buckets as B
from pretuning.battery import A_CELLS, BATTERY_CELLS, CELL_BY_ID, T_CELLS, compose
from pretuning.cells import R0, S_A, Cell
from pretuning.decode import (
    BASE_WORDS,
    assemble_prefilled,
    ban_variants,
    bad_words_body,
    prefill_body,
    prefill_text,
)
from pretuning.driver import run_all
from pretuning.prompts import (
    ONE_REFRAMED,
    THREE_PLAIN,
    THREE_REFRAMED,
    ZERO,
    build_prompt,
    load_exemplars,
)

SIG = PinnedSignature(name="VTask.clog", type_sig="(b n : ℕ) -> ℕ")


@pytest.fixture(scope="module")
def tasks():
    t = available_tasks()
    if len(t) != 41:
        pytest.skip(f"expected the 41-task corpus, found {len(t)}")
    return t


# --- the design -----------------------------------------------------------------------------


def test_battery_is_seven_cells_plus_a_composition_built_later():
    assert len(BATTERY_CELLS) == 7
    assert [c.cell_id for c in T_CELLS] == ["T0", "T1", "T2", "T3"]
    assert [c.cell_id for c in A_CELLS] == ["A1", "A2", "A3"]
    assert len({c.cell_id for c in BATTERY_CELLS}) == 7


def test_every_battery_cell_holds_the_prompt_axis_at_the_measured_winner():
    """S-A_R0 was the eight-cell run's quality winner (40.5% adm|non-sorry) and R1 was worse on
    both metrics in every comparison. A cell that quietly varied the prompt too would confound
    the decode effect with a prompt effect."""
    for c in BATTERY_CELLS:
        assert (c.sorry_level, c.scaffold) == (S_A, R0)
        assert c.uses_prose_exemplars is False


def test_t_battery_varies_only_decode_and_a_battery_only_exemplars():
    assert {(c.ban, c.prefill) for c in T_CELLS} == {(False, False), (True, False),
                                                    (False, True), (True, True)}
    assert {c.exemplar_mode for c in T_CELLS} == {THREE_PLAIN}
    assert all(not c.ban and not c.prefill for c in A_CELLS)
    assert [c.exemplar_mode for c in A_CELLS] == [ZERO, THREE_REFRAMED, ONE_REFRAMED]


def test_compose_takes_decode_from_t_and_exemplars_from_a():
    c = compose("T3", "A3")
    assert (c.ban, c.prefill) == (True, True)
    assert c.exemplar_mode == ONE_REFRAMED and c.n_exemplars == 1
    with pytest.raises(ValueError):
        compose("A1", "T0")


# --- the token ban --------------------------------------------------------------------------


def test_ban_variants_cover_every_context_a_punt_can_appear_in():
    v = set(ban_variants())
    for word in BASE_WORDS:
        for spelling in (word, f" {word}", f"\n{word}", f":= {word}", f".{word}", f"by {word}"):
            assert spelling in v, spelling
    assert len(v) == len(ban_variants()), "variants must be de-duplicated"


def test_bad_words_go_on_the_wire_as_strings():
    """vLLM tokenizes them with the SERVED tokenizer. Sending ids we resolved separately would
    introduce a second tokenization that could disagree with the one actually applied."""
    body = bad_words_body([" sorry", "admit"])
    assert body == {"bad_words": [" sorry", "admit"]}
    assert all(isinstance(x, str) for x in body["bad_words"])


def test_tokenize_url_is_derived_from_the_chat_completions_url():
    from pretuning.decode import _tokenize_url

    urls = _tokenize_url("https://pod-8000.proxy.runpod.net/v1/chat/completions")
    assert "https://pod-8000.proxy.runpod.net/tokenize" in urls
    assert "https://pod-8000.proxy.runpod.net/v1/tokenize" in urls


# --- the prefill ----------------------------------------------------------------------------


def test_prefill_is_the_splice_header_verbatim_and_ends_at_the_assignment():
    p = prefill_text(SIG)
    assert p == "@[reducible] def VTask.clog : (b n : ℕ) -> ℕ :="
    assert p == SIG.splice("").rstrip(), "must come from the signature machinery, not a retype"
    assert not p.endswith(" "), "a trailing space forces a tokenization the model never saw"


def test_prefill_flags_are_the_pair_that_continues_rather_than_reopens_the_turn():
    assert prefill_body("x") == {"continue_final_message": True, "add_generation_prompt": False}


def test_assemble_reattaches_the_prefix_the_server_does_not_echo():
    assert assemble_prefilled("def f :=", " 3") == "def f := 3"
    assert assemble_prefilled("def f :=", "") == "def f :="


def test_reducible_declaration_is_idempotent():
    """Under T2/T3 EVERY candidate arrives already carrying `@[reducible]` -- it is in the prefix
    we handed the model. `@[reducible, reducible]` would be a new failure mode affecting 100% of
    two cells."""
    once = reducible_declaration("def VTask.clog : ℕ := 0")
    assert once.startswith("@[reducible] def")
    assert reducible_declaration(once) == once
    assert reducible_declaration("@[simp] def VTask.f : ℕ := 0") == "@[reducible, simp] def VTask.f : ℕ := 0"
    assert reducible_declaration("@[reducible, simp] def VTask.f : ℕ := 0") == \
        "@[reducible, simp] def VTask.f : ℕ := 0"


# --- extractor smoke on prefill-shaped output ------------------------------------------------
#
# A prefilled completion starts mid-declaration at character 0 with no fence and no think-block.
# Every shape below is prefix+continuation as `assemble_prefilled` produces it.

_PRE = "@[reducible] def VTask.clog : (b n : ℕ) -> ℕ :="

PREFILL_SHAPES = {
    "bare continuation": f"{_PRE}\n  if b ≤ 1 ∨ n ≤ 1 then 0 else Nat.log b n + 1",
    "continuation then closing fence": f"{_PRE}\n  if b ≤ 1 then 0 else Nat.log b n + 1\n```",
    "continuation then prose": f"{_PRE}\n  if b ≤ 1 then 0 else Nat.log b n + 1\n\n"
                               f"This handles the boundary case where b ≤ 1.",
    "single line": f"{_PRE} if b ≤ 1 then 0 else Nat.log b n + 1",
    "continuation then a second fenced restatement": (
        f"{_PRE}\n  if b ≤ 1 then 0 else Nat.log b n + 1\n\nFor clarity:\n\n"
        f"```lean4\ndef VTask.clog (b n : ℕ) : ℕ :=\n  if b ≤ 1 then 0 else Nat.log b n + 1\n```"
    ),
}


@pytest.mark.parametrize("label", sorted(PREFILL_SHAPES))
def test_extractor_survives_prefill_shaped_output(label):
    r = extract_definition("goedel-formalizer-v2-8b", PREFILL_SHAPES[label])
    assert isinstance(r, Extraction), f"{label}: {r}"
    assert r.declared_name == "VTask.clog"
    assert "Nat.log b n + 1" in r.code
    assert "This handles" not in r.code and "For clarity" not in r.code


def test_a_prefill_that_produced_nothing_is_an_unfinished_body_not_a_definition():
    """The one shape that must NOT be scored as an answer: the model emitted nothing after `:=`.
    Reading that as a definition would put an empty body through the kernel and record whatever
    error came back as if the model had attempted something."""
    r = extract_definition("goedel-formalizer-v2-8b", _PRE, finish_reason="length")
    assert not isinstance(r, Extraction)


# --- escape-route buckets --------------------------------------------------------------------


def _classify(decl, *, name="VTask.clog", finish="stop", extracted=True):
    return B.classify(extracted=extracted, declaration=decl, declared_name=name,
                      expected_name="VTask.clog",
                      exemplar_symbols=frozenset({"VTask.ceilRoot", "VTask.limsSup"}),
                      finish_reason=finish)


def test_every_bucket_is_reachable_and_precedence_is_total():
    assert _classify("def VTask.clog : ℕ := Nat.log 2 5 + 1") == B.REAL_CONSTRUCTION_ATTEMPT
    assert _classify("def VTask.clog : ℕ := by exact?") == B.TACTIC_JUNK_BODY
    assert _classify("def VTask.clog : ℕ := by aesop") == B.TACTIC_JUNK_BODY
    # The shape the ban ACTUALLY produces: a whole proof script as the definition body.
    assert _classify("def VTask.f : T := by use f use hf_nonempty use hf_inverse") == B.TACTIC_JUNK_BODY
    # Commentary explaining that the answer is absent is not a construction attempt.
    assert _classify("def VTask.f : T := by -- this would be a complex recursive definition\n"
                     "  -- the actual implementation is intricate") == B.DEGENERATE_BODY
    assert _classify("def VTask.f : T := by -- goes here\n  placeholder") == B.DEGENERATE_BODY
    assert _classify("def VTask.clog : ℕ :=") == B.DEGENERATE_BODY
    assert _classify("def VTask.clog : ℕ := _") == B.DEGENERATE_BODY
    assert _classify("def VTask.ceilRoot : ℕ := 3", name="VTask.ceilRoot") == B.EXEMPLAR_SUBSTITUTION
    assert _classify("def VTask.clog : ℕ := 3", finish="length") == B.TRUNCATION_AT_CAP
    assert _classify(None, extracted=False) == B.OTHER
    assert set(B.BUCKETS) == {
        B.REAL_CONSTRUCTION_ATTEMPT, B.TACTIC_JUNK_BODY, B.DEGENERATE_BODY,
        B.EXEMPLAR_SUBSTITUTION, B.TRUNCATION_AT_CAP, B.OTHER,
    }


def test_truncation_outranks_every_other_reading():
    """A generation cut off at the cap says nothing about what the model would have written, so
    reading its partial body as a punt (or as a construction) invents evidence either way."""
    assert _classify("def VTask.clog : ℕ := by exact?", finish="length") == B.TRUNCATION_AT_CAP
    assert _classify("def VTask.ceilRoot : ℕ := 3", name="VTask.ceilRoot",
                     finish="length") == B.TRUNCATION_AT_CAP


def test_a_leaked_ban_token_is_classified_as_a_punt_not_as_construction():
    assert _classify("def VTask.clog : ℕ := sorry") == B.DEGENERATE_BODY
    assert B.contains_banned_token("we could write sorry here")
    assert not B.contains_banned_token("def VTask.clog : ℕ := Nat.log 2 5")


def test_the_exemplar_bucket_fires_on_the_declared_name_not_on_the_body_text():
    """The measured contamination was 54 RE-DERIVED variants against 15 byte-identical copies --
    a body-text match would have missed 78% of it."""
    rederived = "def VTask.ceilRoot (n a : ℕ) : ℕ := Nat.ceilDiv 1 1  -- nothing like the original"
    assert _classify(rederived, name="VTask.ceilRoot") == B.EXEMPLAR_SUBSTITUTION


# --- exemplar presentation modes --------------------------------------------------------------


def test_three_plain_is_byte_identical_to_the_eight_cell_prompt(tasks):
    """T0 is only a paired control if its prompt is the prompt that produced last week's numbers."""
    d, sig = load_task(tasks[0])
    base = Cell(S_A, R0)
    assert build_prompt(base, d, sig, exemplar_mode=THREE_PLAIN) == build_prompt(base, d, sig)


def test_zero_mode_carries_no_exemplar_text_at_all(tasks):
    d, sig = load_task(tasks[0])
    p = build_prompt(Cell(S_A, R0), d, sig, exemplar_mode=ZERO)
    for e in load_exemplars():
        assert e["task_symbol"] not in p
        assert e["definition"].strip().splitlines()[0] not in p
    # Line-exact: dossiers carry their own `## Worked examples` section, so a substring test here
    # would fail on the task's own text rather than on a leftover exemplar block.
    assert "# Worked examples" not in p.splitlines()
    assert "# Your task" in p.splitlines()


def test_reframed_modes_separate_the_examples_from_the_task(tasks):
    d, sig = load_task(tasks[0])
    for mode, n in ((THREE_REFRAMED, 3), (ONE_REFRAMED, 1)):
        p = build_prompt(Cell(S_A, R0), d, sig, exemplar_mode=mode)
        assert "NOT YOUR TASK" in p
        assert "END OF WORKED EXAMPLES" in p
        assert "THE TASK -- ANSWER THIS" in p
        assert p.count("(not your task) ---") == n
        assert p.index("END OF WORKED EXAMPLES") < p.index("THE TASK -- ANSWER THIS")


def test_one_reframed_shows_only_the_first_exemplar(tasks):
    d, sig = load_task(tasks[0])
    p = build_prompt(Cell(S_A, R0), d, sig, exemplar_mode=ONE_REFRAMED)
    ex = load_exemplars()
    assert ex[0]["task_symbol"] in p
    for other in ex[1:]:
        assert other["task_symbol"] not in p


def test_unknown_exemplar_mode_is_refused(tasks):
    d, sig = load_task(tasks[0])
    with pytest.raises(ValueError):
        build_prompt(Cell(S_A, R0), d, sig, exemplar_mode="two_ish")


def test_no_task_real_name_leaks_in_any_battery_prompt(tasks):
    """41 tasks x 7 cells, exemplar text included -- the same guard the eight-cell run ran under,
    re-run because two of the three exemplar modes are new text."""
    from pathlib import Path

    from pretuning.prompts import check_prompt_leak

    reals = {p.parent.name: (json.loads(p.read_text()).get("provenance") or {}).get("mathlib_name")
             for p in Path("prelim_testing/tasks").glob("*/task.json")}
    offenders = []
    for t in tasks:
        d, sig = load_task(t)
        for c in BATTERY_CELLS:
            ok, detail = check_prompt_leak(
                build_prompt(c, d, sig, exemplar_mode=c.exemplar_mode), reals[t])
            if not ok:
                offenders.append((t, c.cell_id, detail))
    assert not offenders, f"leak in {len(offenders)} prompt(s): {offenders[:5]}"


# --- driver wiring ----------------------------------------------------------------------------


def test_a_ban_cell_refuses_to_run_without_resolved_variants(tmp_path, tasks):
    """A T1 with an empty ban list is byte-identical to T0. It would burn the cell and report the
    null result as a finding about token banning."""
    out = run_all(tasks[:1], endpoint_url="http://unused", samples_dir=tmp_path, model_name="m",
                  cells=[CELL_BY_ID["T1"]], samples_per_task=1, log=lambda *a, **k: None)
    assert out[0].status == "aborted"
    assert not list(tmp_path.rglob("sample_*.json")), "must not generate anything"


def test_ban_variants_reach_the_wire_for_ban_cells_only(tmp_path, tasks):
    body = "```lean4\ndef VTask.clog (b n : ℕ) : ℕ := Nat.log b n + 1\n```"
    for cell_id, expect_ban in (("T1", True), ("T0", False)):
        srv = StubEndpointServer([ScriptedResponse(200, sse_stream(body))])
        try:
            run_all(tasks[:1], endpoint_url=srv.url, samples_dir=tmp_path / cell_id,
                    model_name="m", cells=[CELL_BY_ID[cell_id]], samples_per_task=1,
                    ban_variants=[" sorry", "sorry"], log=lambda *a, **k: None)
            sent = srv.requests_received[0]
            assert ("bad_words" in sent) is expect_ban, cell_id
            if expect_ban:
                assert sent["bad_words"] == [" sorry", "sorry"]
        finally:
            srv.stop()


def test_prefill_reaches_the_wire_and_the_stored_completion(tmp_path, tasks):
    """Three things at once, because they fail independently: the prefix goes out as a trailing
    assistant message, the template flags that make it a continuation go with it, and the prefix
    is re-attached to the stored completion (the server returns only the continuation)."""
    srv = StubEndpointServer([ScriptedResponse(200, sse_stream(" Nat.log b n + 1"))])
    try:
        run_all(tasks[:1], endpoint_url=srv.url, samples_dir=tmp_path, model_name="m",
                cells=[CELL_BY_ID["T2"]], samples_per_task=1, log=lambda *a, **k: None)
        sent = srv.requests_received[0]
        assert sent["messages"][-1]["role"] == "assistant"
        assert sent["messages"][-1]["content"].startswith("@[reducible] def VTask.")
        assert sent["messages"][-1]["content"].endswith(":=")
        assert sent["continue_final_message"] is True
        assert sent["add_generation_prompt"] is False

        rec = json.loads(next(tmp_path.rglob("sample_*.json")).read_text())
        assert rec["completion"].startswith("@[reducible] def VTask.")
        assert rec["completion"].endswith("Nat.log b n + 1")
        assert rec["extra"]["prefill_applied"] is True
        assert rec["extra"]["raw_continuation"] == " Nat.log b n + 1"
        assert isinstance(extract_definition("goedel-formalizer-v2-8b", rec["completion"]), Extraction)
    finally:
        srv.stop()


def test_every_battery_sample_records_its_full_configuration(tmp_path, tasks):
    srv = StubEndpointServer([ScriptedResponse(200, sse_stream(
        "```lean\ndef VTask.clog : ℕ := 0\n```"))])
    try:
        run_all(tasks[:1], endpoint_url=srv.url, samples_dir=tmp_path, model_name="m",
                cells=[CELL_BY_ID["A2"]], samples_per_task=1, log=lambda *a, **k: None)
        rec = json.loads(next(tmp_path.rglob("sample_*.json")).read_text())
        assert rec["extra"]["exemplar_mode"] == THREE_REFRAMED
        assert rec["extra"]["ban_applied"] is False
        assert rec["extra"]["prefill_applied"] is False
        assert rec["extra"]["cell_id"] == "A2"
    finally:
        srv.stop()


def test_the_gate_reads_the_assembled_text_not_the_bare_continuation(tmp_path, tasks):
    """Under a prefill the `def ... :=` the gate looks for is in the prefix the server never
    echoes. Gating on the continuation alone would fail every prefill cell for the one reason
    that is not a defect."""
    srv = StubEndpointServer([ScriptedResponse(200, sse_stream(" Nat.log b n + 1"))])
    try:
        out = run_all(tasks[:1], endpoint_url=srv.url, samples_dir=tmp_path, model_name="m",
                      cells=[CELL_BY_ID["T2"]], samples_per_task=3, log=lambda *a, **k: None)
        assert out[0].status == "completed", out[0].gate_detail
    finally:
        srv.stop()
