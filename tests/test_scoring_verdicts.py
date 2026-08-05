"""Tests for `scoring.verdicts`, `scoring.dedup`, `scoring.store` -- the pure layer.

These decide what a stored number MEANS, so they are worth more than their runtime suggests: a
mapping bug here does not crash anything, it produces a plausible wrong score.
"""

import json

import pytest

from ladder.statuses import AdjudicationStatus
from scoring import dedup, store
from scoring.verdicts import (
    DECIDE,
    PROOF,
    RETRYABLE,
    Verdict,
    check_mechanism_invariant,
    fidelity,
    verdict_for,
)

# --- the ladder -> verdict mapping ---------------------------------------------------------------


@pytest.mark.parametrize(
    "status,expected",
    [
        (AdjudicationStatus.CERTIFIED, Verdict.PASS),
        (AdjudicationStatus.FAILED, Verdict.FAIL),
        (AdjudicationStatus.UNKNOWN, Verdict.UNKNOWN),
        (AdjudicationStatus.ENV_DEATH, Verdict.ERROR),
        (AdjudicationStatus.ERRORED, Verdict.ERROR),
    ],
)
def test_every_ladder_status_maps(status, expected):
    assert verdict_for(status) is expected


def test_every_ladder_status_is_covered():
    """A new `AdjudicationStatus` must not silently acquire a default -- especially not FAIL."""
    for status in AdjudicationStatus:
        assert verdict_for(status) in Verdict


def test_only_infrastructure_outcomes_are_retryable():
    """UNKNOWN is deliberately NOT retryable: exhausting the tactic budget a second time costs
    twice as much and tells us exactly the same thing."""
    assert RETRYABLE == {AdjudicationStatus.ENV_DEATH, AdjudicationStatus.ERRORED}
    assert AdjudicationStatus.UNKNOWN not in RETRYABLE
    assert AdjudicationStatus.FAILED not in RETRYABLE


# --- the mechanism invariant ------------------------------------------------------------------------


def test_a_proof_fact_may_never_be_recorded_as_a_refutation():
    """THE invariant. A tactic failing to close a goal is not evidence the goal is false; if a
    proof fact ever reaches FAIL, something has claimed exhaustion as a refutation."""
    with pytest.raises(ValueError, match="may not produce verdict 'fail'"):
        check_mechanism_invariant(PROOF, Verdict.FAIL)


@pytest.mark.parametrize("verdict", [Verdict.PASS, Verdict.UNKNOWN, Verdict.ERROR])
def test_proof_facts_allow_the_other_three(verdict):
    check_mechanism_invariant(PROOF, verdict)


@pytest.mark.parametrize("verdict", [Verdict.PASS, Verdict.FAIL, Verdict.ERROR, Verdict.UNKNOWN])
def test_decide_facts_allow_unknown_for_untestable_propositions(verdict):
    """Decide facts may be UNKNOWN since the 2026-08-05 tier-1 fix: a missing `Decidable`
    instance means untestable-through-this-splice, not refuted."""
    check_mechanism_invariant(DECIDE, verdict)


def test_unknown_mechanism_raises():
    with pytest.raises(ValueError, match="unknown fact mechanism"):
        check_mechanism_invariant("hammer", Verdict.PASS)


# --- fidelity -------------------------------------------------------------------------------------


def test_fidelity_excludes_unknown_and_error_from_the_denominator():
    verdicts = [Verdict.PASS, Verdict.PASS, Verdict.FAIL, Verdict.UNKNOWN, Verdict.ERROR]
    assert fidelity(verdicts) == pytest.approx(2 / 3)


def test_nothing_resolved_is_none_not_zero():
    """A candidate whose every fact came back UNKNOWN has not scored zero -- it has not been
    scored. Averaging those together downstream would be a category error."""
    assert fidelity([Verdict.UNKNOWN, Verdict.ERROR]) is None
    assert fidelity([]) is None


def test_all_pass_is_one():
    assert fidelity([Verdict.PASS, Verdict.PASS]) == 1.0


# --- dedup -------------------------------------------------------------------------------------------


def test_whitespace_only_differences_share_a_hash():
    a = "fun b n => Nat.log b n + 1"
    b = "fun b n =>\n    Nat.log b n + 1\n"
    assert dedup.candidate_hash(a) == dedup.candidate_hash(b)


def test_semantically_equal_but_textually_different_bodies_do_NOT_share_a_hash():
    """Deliberately conservative. Claiming `if h then a else b` equals a `match` would fan one
    candidate's verdicts onto a genuinely different definition. Semantic sameness is the
    kernel's job, via the tier-4 equivalence path, with a proof."""
    assert dedup.candidate_hash("fun n => if n = 0 then 0 else 1") != dedup.candidate_hash(
        "fun n => match n with | 0 => 0 | _ => 1"
    )


def test_group_by_hash_preserves_input_order_within_a_group():
    """Resume depends on this: a re-run must choose the same representative, or it would compute
    a second verdict where an inherited one already sits."""
    samples = [
        {"sample_index": 3, "extracted_code": "x"},
        {"sample_index": 1, "extracted_code": "x"},
        {"sample_index": 2, "extracted_code": "y"},
    ]
    groups = dedup.group_by_hash(samples)
    assert len(groups) == 2
    assert [s["sample_index"] for s in groups[dedup.candidate_hash("x")]] == [3, 1]


def test_samples_without_extracted_code_are_dropped():
    assert dedup.group_by_hash([{"sample_index": 0, "extracted_code": None}]) == {}


# --- store ------------------------------------------------------------------------------------------


def _record(idx=0, mechanisms=("decide", "proof")):
    return {
        "schema_version": 1, "model_slug": "m", "task_name": "T", "sample_index": idx,
        "fact_verdicts": [{"fact_id": "f", "verdict": "pass"}],
        "mechanisms_attempted": list(mechanisms),
    }


def test_write_then_read_roundtrips(tmp_path):
    path = store.write_verdict(_record(), scores_dir=tmp_path)
    assert path == tmp_path / "m" / "T" / "sample_00.json"
    assert store.read_verdict(path)["fact_verdicts"][0]["verdict"] == "pass"


def test_is_complete_requires_parseable_json_with_the_required_keys(tmp_path):
    assert not store.is_complete("m", "T", 0, scores_dir=tmp_path)
    store.write_verdict(_record(), scores_dir=tmp_path)
    assert store.is_complete("m", "T", 0, scores_dir=tmp_path)


# --- pass-aware completeness (Stage D writes decide, Stage E fills in proof) ---------------------


def test_a_decide_only_record_is_not_complete_for_the_proof_pass(tmp_path):
    """THE Stage D/E handover test. Without the mechanism clause a Stage D record satisfies every
    other test of doneness, so Stage E would skip exactly the candidates it exists to finish --
    silently, and looking indistinguishable from a successful resume."""
    store.write_verdict(_record(mechanisms=("decide",)), scores_dir=tmp_path)

    assert store.is_complete("m", "T", 0, scores_dir=tmp_path, require_mechanisms=("decide",))
    assert not store.is_complete("m", "T", 0, scores_dir=tmp_path, require_mechanisms=("decide", "proof"))


def test_a_decide_only_record_is_not_rescored_by_a_second_decide_pass(tmp_path):
    """The other half: re-running Stage D must recompute nothing."""
    store.write_verdict(_record(mechanisms=("decide",)), scores_dir=tmp_path)
    assert store.is_complete("m", "T", 0, scores_dir=tmp_path, require_mechanisms=("decide",))


def test_a_record_with_no_mechanism_field_is_never_complete(tmp_path):
    """Fails closed. A record predating the field is more safely rescored than wrongly skipped."""
    legacy = _record()
    del legacy["mechanisms_attempted"]
    store.write_verdict(legacy, scores_dir=tmp_path)
    assert not store.is_complete("m", "T", 0, scores_dir=tmp_path)


def test_a_truncated_file_is_not_complete(tmp_path):
    """File existence alone must never count as done -- the 2026-08-04 kill is why."""
    path = store.verdict_path("m", "T", 0, scores_dir=tmp_path)
    path.parent.mkdir(parents=True)
    path.write_text('{"schema_version": 1, "model_slug": "m", "task_nam')
    assert path.exists()
    assert not store.is_complete("m", "T", 0, scores_dir=tmp_path)


def test_a_parseable_file_missing_required_keys_is_not_complete(tmp_path):
    path = store.verdict_path("m", "T", 0, scores_dir=tmp_path)
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"schema_version": 1}))
    assert not store.is_complete("m", "T", 0, scores_dir=tmp_path)


def test_no_temp_files_survive_a_write(tmp_path):
    store.write_verdict(_record(), scores_dir=tmp_path)
    assert list((tmp_path / "m" / "T").glob(".*.tmp")) == []


def test_iter_verdicts_skips_unparseable_files_rather_than_raising(tmp_path):
    """A reader must never crash on a run that is mid-write."""
    store.write_verdict(_record(0), scores_dir=tmp_path)
    (tmp_path / "m" / "T" / "sample_09.json").write_text("{not json")
    assert len(list(store.iter_verdicts(scores_dir=tmp_path))) == 1


def test_iter_verdicts_on_a_missing_tree_is_empty(tmp_path):
    assert list(store.iter_verdicts(scores_dir=tmp_path / "nope")) == []


# --- NOT_ATTEMPTED is not UNKNOWN ------------------------------------------------------------------


def test_not_attempted_is_distinct_from_unknown():
    """UNKNOWN means we tried and could not tell; NOT_ATTEMPTED means we deliberately have not
    tried yet. Collapsing them would let a Stage D coverage figure read as a Stage E one."""
    assert Verdict.NOT_ATTEMPTED is not Verdict.UNKNOWN
    assert not Verdict.NOT_ATTEMPTED.is_resolved
    assert Verdict.UNKNOWN.is_resolved


def test_not_attempted_is_excluded_from_fidelity():
    assert fidelity([Verdict.PASS, Verdict.FAIL, Verdict.NOT_ATTEMPTED]) == pytest.approx(0.5)
    assert fidelity([Verdict.NOT_ATTEMPTED, Verdict.NOT_ATTEMPTED]) is None


@pytest.mark.parametrize("mechanism", [DECIDE, PROOF])
def test_not_attempted_is_legal_for_either_mechanism(mechanism):
    """It is a statement about the PASS, not about the fact, so the mechanism invariant must
    not reject it -- including for proof facts, which may otherwise never be FAIL."""
    check_mechanism_invariant(mechanism, Verdict.NOT_ATTEMPTED)


# --- Stage D -> Stage E merge (2026-08-07) ---------------------------------------------------------


def test_a_later_pass_does_not_erase_an_earlier_pass(tmp_path):
    """THE Stage D/E handover hazard. Without merging, Stage E overwrites the file and the decide
    verdicts revert to NOT_ATTEMPTED -- worse than losing them, because the record still looks
    complete and internally consistent."""
    from scoring.runner import _merge_with_existing

    store.write_verdict({
        "schema_version": 1, "model_slug": "m", "task_name": "T", "sample_index": 0,
        "mechanisms_attempted": ["decide"], "admissible": True, "splice_path": "plain",
        "fact_verdicts": [
            {"fact_id": "d1", "mechanism": "decide", "verdict": "pass"},
            {"fact_id": "p1", "mechanism": "proof", "verdict": "not_attempted_this_pass"},
        ],
    }, scores_dir=tmp_path)

    stage_e = {
        "mechanisms_attempted": ["proof"],
        "fact_verdicts": [
            {"fact_id": "d1", "mechanism": "decide", "verdict": "not_attempted_this_pass"},
            {"fact_id": "p1", "mechanism": "proof", "verdict": "pass"},
        ],
    }
    merged = _merge_with_existing(stage_e, "m", "T", 0, tmp_path)
    by_id = {fv["fact_id"]: fv["verdict"] for fv in merged["fact_verdicts"]}

    assert by_id["d1"] == "pass", "Stage D's decide verdict must survive Stage E"
    assert by_id["p1"] == "pass", "Stage E's proof verdict must land"
    assert merged["mechanisms_attempted"] == ["decide", "proof"]
    assert merged["fidelity"] == 1.0
    assert merged["admissible"] is True  # carried from the pass that actually spliced


def test_merging_into_nothing_is_a_no_op(tmp_path):
    from scoring.runner import _merge_with_existing

    payload = {"fact_verdicts": [{"fact_id": "x", "mechanism": "decide", "verdict": "pass"}]}
    assert _merge_with_existing(dict(payload), "m", "T", 0, tmp_path) == payload
