"""Unit tests for miner.rank -- gates-then-preference-score selection and curation, on
synthetic VerifiedDef instances (no REPL, no real Mathlib data, no real curation.yaml on disk
unless a test says so). No top-N: the manifest is two populations, eligible (ranked, in full)
and excluded (with the gate(s) that fired) -- see the 22 July 2026 design-doc revision."""

from miner.gates import GateConfig
from miner.rank import CurationEntry, build_manifest, load_curation
from miner.verify import VerifiedDef

_ANTI_PLUMBING_PATTERNS = [
    r"(?i)aux\d*$",
    r"(?i)^aux",
    r"Impl$",
    r"(?:^|\.)go$",
    r"TR$",
    r"(?i)decEq$",
    r"(?i)beq$",
]


def _gate_config(**overrides) -> GateConfig:
    defaults = dict(
        theorem_mention_floor=2,
        length_min=40,
        length_max=500,
        docstring_min_length=20,
        vocabulary_modules=["Data/Nat", "Data/List", "Data/Finset", "Logic"],
        anti_plumbing_patterns=_ANTI_PLUMBING_PATTERNS,
        richness_floor=1,
    )
    defaults.update(overrides)
    return GateConfig(**defaults)


def _verified(name: str, **overrides) -> VerifiedDef:
    """Passes all seven gates by default: substantial docstring, body within the length band,
    an ordinary name, no exotic dependencies, a casework-rich supply tier (ℕ -> ℕ, executable,
    decidable-equal output), and a richness of 1 (one comparison, `≠`) -- above the richness
    floor without needing per-test overrides."""
    defaults = dict(
        name=name,
        module_path="Test.lean",
        source_text=f"def {name} (n : Nat) : Nat := n ≠ 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1",
        docstring="A perfectly ordinary docstring describing what this computes in full.",
        mention_count=30,
        included=True,
        elaborates=True,
        binder_groups=[],
        explicit_arg_types=["ℕ"],
        return_type="ℕ",
        executable=True,
        exec_mechanism="eval",
        output_decidable_eq=True,
        referenced_constants=[],
        axioms=[],
    )
    defaults.update(overrides)
    return VerifiedDef(**defaults)


def _build(verified, theorem_mention_counts=None, **kwargs):
    kwargs.setdefault("declaration_index", {})
    kwargs.setdefault("gate_config", _gate_config())
    if theorem_mention_counts is None:
        # Default: every candidate clears the theorem-mention floor, so tests that aren't
        # specifically exercising that gate don't need to think about it.
        theorem_mention_counts = {v.name: 10 for v in verified}
    return build_manifest(verified, theorem_mention_counts=theorem_mention_counts, **kwargs)


def _record_for(records, name):
    return next(r for r in records if r.name == name)


# --- gates, at the build_manifest integration level (see tests/test_miner_gates.py for the
# individual-gate unit tests) ---


def test_gate_failure_excludes_and_records_which_gates_fired():
    verified = [_verified("Foo.a")]
    records = _build(verified, theorem_mention_counts={"Foo.a": 0})  # fails the floor only
    record = _record_for(records, "Foo.a")
    assert record.eligible is False
    assert record.gates_failed == ["theorem_mention_floor"]
    assert "theorem_mention_floor" in record.exclusion_reason
    assert record.rank is None


def test_gate_survivor_is_ranked_normally():
    verified = [_verified("Foo.a")]
    records = _build(verified)
    record = _record_for(records, "Foo.a")
    assert record.eligible is True
    assert record.gates_failed == []
    assert record.rank == 1


def test_gate_excluded_candidate_does_not_consume_a_rank_slot():
    gated = _verified("Foo.gated")
    eligible = _verified("Foo.eligible")
    records = _build([gated, eligible], theorem_mention_counts={"Foo.gated": 0, "Foo.eligible": 10})
    assert _record_for(records, "Foo.gated").rank is None
    assert _record_for(records, "Foo.eligible").rank == 1


def test_gate_excluded_record_still_carries_richness_and_score_for_auditability():
    verified = [_verified("Foo.a")]
    records = _build(verified, theorem_mention_counts={"Foo.a": 0})
    record = _record_for(records, "Foo.a")
    assert record.richness is not None
    assert record.score is not None


def test_no_top_n_cutoff_every_eligible_candidate_is_ranked():
    """There is no top-N mechanism -- an arbitrarily large pool of gate-survivors must all end
    up eligible with a rank, none "outranked"."""
    verified = [_verified(f"Foo.item{i}") for i in range(250)]
    records = _build(verified)
    eligible = [r for r in records if r.eligible]
    assert len(eligible) == 250
    assert sorted(r.rank for r in eligible) == list(range(1, 251))


def test_return_shape_recorded_on_eligible_and_gate_excluded_records():
    prop_def = _verified("Foo.prop", return_type="Prop")
    gated = _verified("Foo.gated")
    records = _build([prop_def, gated], theorem_mention_counts={"Foo.prop": 10, "Foo.gated": 0})
    assert _record_for(records, "Foo.prop").return_shape == "prop"
    assert _record_for(records, "Foo.gated").return_shape == "value"


def test_return_shape_is_none_for_verification_failures():
    verified = [_verified("Foo.a", included=False, exclusion_reason="does not elaborate")]
    records = _build(verified)
    assert _record_for(records, "Foo.a").return_shape is None


# --- curation: exclude ---


def test_exclude_removes_from_eligible_set_and_records_reason():
    verified = [_verified("Foo.a"), _verified("Foo.b")]
    curation = [CurationEntry(name="Foo.a", action="exclude", reason="internal helper")]

    records = _build(verified, curation=curation)

    excluded = _record_for(records, "Foo.a")
    assert excluded.eligible is False
    assert excluded.exclusion_reason == "internal helper"
    assert excluded.rank is None
    assert excluded.curation_applied == {"action": "exclude", "reason": "internal helper"}

    # the excluded candidate must not consume a rank slot from the remaining pool
    kept = _record_for(records, "Foo.b")
    assert kept.eligible is True
    assert kept.rank == 1


def test_excluded_record_still_carries_its_proxies_and_score():
    """Excluding shouldn't throw away the mechanical data -- just the eligibility decision --
    so a reviewer can still see why it scored the way it did."""
    verified = [_verified("Foo.a")]
    curation = [CurationEntry(name="Foo.a", action="exclude", reason="internal helper")]

    records = _build(verified, curation=curation)
    excluded = _record_for(records, "Foo.a")
    assert excluded.proxies is not None
    assert excluded.richness is not None
    assert excluded.score is not None


# --- curation: demote ---


def test_demote_ranks_below_a_higher_scoring_undemoted_peer():
    # "strong" has one extra comparison operator over "weak" -- a richness gap of exactly
    # RICHNESS_WEIGHT (10), comfortably inside DEMOTE_PENALTY's reach (15). A bigger richness
    # gap would swamp the penalty and not test what this case is meant to test.
    strong = _verified("Foo.strong", source_text="def strong (n : Nat) : Nat := n + 1 + 1 + 1 + 1 + 1 ≠ 1 ≠ 1")
    weak = _verified("Foo.weak", source_text="def weak (n : Nat) : Nat := n ≠ 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1")
    curation = [CurationEntry(name="Foo.strong", action="demote", reason="near-duplicate")]

    records = _build([strong, weak], curation=curation)

    strong_record = _record_for(records, "Foo.strong")
    weak_record = _record_for(records, "Foo.weak")
    assert weak_record.rank < strong_record.rank
    assert strong_record.curation_applied == {"action": "demote", "reason": "near-duplicate"}


def test_demote_does_not_alter_the_recorded_score_total():
    """The penalty is sort-key-only -- the stored score must stay the true, unpenalized
    value so the manifest remains auditable (a demoted item's score should match what an
    identical undemoted item would get)."""
    demoted = [_verified("Foo.a")]
    plain = [_verified("Foo.a")]
    curation = [CurationEntry(name="Foo.a", action="demote", reason="reason")]

    demoted_records = _build(demoted, curation=curation)
    plain_records = _build(plain, curation=None)

    assert _record_for(demoted_records, "Foo.a").score.total == _record_for(plain_records, "Foo.a").score.total


def test_demote_can_still_survive_to_be_eligible_if_score_is_high_enough():
    verified = [_verified("Foo.only")]
    curation = [CurationEntry(name="Foo.only", action="demote", reason="reason")]

    records = _build(verified, curation=curation)
    assert _record_for(records, "Foo.only").eligible is True


# --- curation: note ---


def test_note_leaves_ranking_and_eligibility_untouched_but_records_reason():
    verified = [_verified("Foo.a"), _verified("Foo.b")]
    plain_records = _build(verified, curation=None)

    curation = [CurationEntry(name="Foo.a", action="note", reason="near-duplicate of Foo.b")]
    noted_records = _build(verified, curation=curation)

    assert _record_for(noted_records, "Foo.a").rank == _record_for(plain_records, "Foo.a").rank
    assert _record_for(noted_records, "Foo.a").eligible == _record_for(plain_records, "Foo.a").eligible
    assert _record_for(noted_records, "Foo.a").curation_applied == {
        "action": "note",
        "reason": "near-duplicate of Foo.b",
    }


def test_uncurated_records_have_no_curation_applied():
    verified = [_verified("Foo.a")]
    curation = [CurationEntry(name="Foo.other", action="note", reason="unrelated")]

    records = _build(verified, curation=curation)
    assert _record_for(records, "Foo.a").curation_applied is None


def test_curation_applied_recorded_even_for_verification_failures():
    verified = [_verified("Foo.a", included=False, exclusion_reason="does not elaborate")]
    curation = [CurationEntry(name="Foo.a", action="note", reason="known issue")]

    records = _build(verified, curation=curation)
    record = _record_for(records, "Foo.a")
    assert record.curation_applied == {"action": "note", "reason": "known issue"}
    assert record.exclusion_reason == "does not elaborate"  # note doesn't override the real reason


# --- load_curation ---


def test_load_curation_parses_the_real_seeded_file():
    """Regression test against the actual committed miner/curation.yaml -- confirms its
    schema keeps parsing as this module evolves."""
    entries = load_curation()
    by_name = {e.name: e for e in entries}
    assert by_name["Nat.digitsAux1"].action == "exclude"
    assert by_name["Pairwise"].action == "note"
    assert by_name["Set.Pairwise"].action == "note"


def test_load_curation_missing_file_returns_empty_list(tmp_path):
    assert load_curation(tmp_path / "does_not_exist.yaml") == []


def test_load_curation_rejects_unknown_action(tmp_path):
    bad = tmp_path / "curation.yaml"
    bad.write_text("entries:\n  - name: Foo\n    action: nonsense\n    reason: because\n")
    try:
        load_curation(bad)
        raise AssertionError("expected ValueError for an unknown action")
    except ValueError:
        pass
