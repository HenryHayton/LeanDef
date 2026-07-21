"""Unit tests for miner.rank -- scoring and curation, on synthetic VerifiedDef instances (no
REPL, no real Mathlib data, no real curation.yaml on disk unless a test says so)."""

from miner.rank import CurationEntry, build_manifest, load_curation
from miner.verify import VerifiedDef


def _verified(name: str, **overrides) -> VerifiedDef:
    defaults = dict(
        name=name,
        module_path="Test.lean",
        source_text=f"def {name} (n : Nat) : Nat := n",
        docstring=None,
        mention_count=0,
        included=True,
        elaborates=True,
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


def _record_for(records, name):
    return next(r for r in records if r.name == name)


# --- curation: exclude ---


def test_exclude_removes_from_included_set_and_records_reason():
    verified = [_verified("Foo.a", mention_count=20), _verified("Foo.b", mention_count=1)]
    curation = [CurationEntry(name="Foo.a", action="exclude", reason="internal helper")]

    records = build_manifest(verified, top_n=10, curation=curation)

    excluded = _record_for(records, "Foo.a")
    assert excluded.included is False
    assert excluded.exclusion_reason == "internal helper"
    assert excluded.rank is None
    assert excluded.curation_applied == {"action": "exclude", "reason": "internal helper"}

    # the excluded candidate must not consume a rank slot from the remaining pool
    kept = _record_for(records, "Foo.b")
    assert kept.included is True
    assert kept.rank == 1


def test_excluded_record_still_carries_its_proxies_and_score():
    """Excluding shouldn't throw away the mechanical data -- just the inclusion decision --
    so a reviewer can still see why it scored the way it did."""
    verified = [_verified("Foo.a", mention_count=20)]
    curation = [CurationEntry(name="Foo.a", action="exclude", reason="internal helper")]

    records = build_manifest(verified, top_n=10, curation=curation)
    excluded = _record_for(records, "Foo.a")
    assert excluded.proxies is not None
    assert excluded.score is not None


# --- curation: demote ---


def test_demote_ranks_below_a_higher_scoring_undemoted_peer():
    # Both stay in the same (THIN) global tier -- mention_count 1 vs 4 -- so the pre-demote
    # score gap is small (just the log1p in-degree term), well within DEMOTE_PENALTY's reach.
    # A bigger gap (e.g. crossing into the RICH tier) would swamp the penalty and not test
    # what this case is meant to test.
    verified = [_verified("Foo.strong", mention_count=4), _verified("Foo.weak", mention_count=1)]
    curation = [CurationEntry(name="Foo.strong", action="demote", reason="near-duplicate")]

    records = build_manifest(verified, top_n=10, curation=curation)

    strong = _record_for(records, "Foo.strong")
    weak = _record_for(records, "Foo.weak")
    assert weak.rank < strong.rank
    assert strong.curation_applied == {"action": "demote", "reason": "near-duplicate"}


def test_demote_does_not_alter_the_recorded_score_total():
    """The penalty is sort-key-only -- the stored score must stay the true, unpenalized
    value so the manifest remains auditable (a demoted item's score should match what an
    identical undemoted item would get)."""
    demoted = [_verified("Foo.a", mention_count=5)]
    plain = [_verified("Foo.a", mention_count=5)]
    curation = [CurationEntry(name="Foo.a", action="demote", reason="reason")]

    demoted_records = build_manifest(demoted, top_n=10, curation=curation)
    plain_records = build_manifest(plain, top_n=10, curation=None)

    assert _record_for(demoted_records, "Foo.a").score.total == _record_for(plain_records, "Foo.a").score.total


def test_demote_can_still_survive_to_be_included_if_score_is_high_enough():
    verified = [_verified("Foo.only", mention_count=20)]
    curation = [CurationEntry(name="Foo.only", action="demote", reason="reason")]

    records = build_manifest(verified, top_n=10, curation=curation)
    assert _record_for(records, "Foo.only").included is True


# --- curation: note ---


def test_note_leaves_ranking_and_inclusion_untouched_but_records_reason():
    verified = [_verified("Foo.a", mention_count=20), _verified("Foo.b", mention_count=1)]
    plain_records = build_manifest(verified, top_n=10, curation=None)

    curation = [CurationEntry(name="Foo.a", action="note", reason="near-duplicate of Foo.b")]
    noted_records = build_manifest(verified, top_n=10, curation=curation)

    assert _record_for(noted_records, "Foo.a").rank == _record_for(plain_records, "Foo.a").rank
    assert _record_for(noted_records, "Foo.a").included == _record_for(plain_records, "Foo.a").included
    assert _record_for(noted_records, "Foo.a").curation_applied == {
        "action": "note",
        "reason": "near-duplicate of Foo.b",
    }


def test_uncurated_records_have_no_curation_applied():
    verified = [_verified("Foo.a", mention_count=20)]
    curation = [CurationEntry(name="Foo.other", action="note", reason="unrelated")]

    records = build_manifest(verified, top_n=10, curation=curation)
    assert _record_for(records, "Foo.a").curation_applied is None


def test_curation_applied_recorded_even_for_verification_failures():
    verified = [_verified("Foo.a", included=False, exclusion_reason="does not elaborate")]
    curation = [CurationEntry(name="Foo.a", action="note", reason="known issue")]

    records = build_manifest(verified, top_n=10, curation=curation)
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
