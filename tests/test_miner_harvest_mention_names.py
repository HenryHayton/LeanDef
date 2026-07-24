"""Unit tests for `miner.harvest.compute_theorem_mentions`/`write_mention_names` -- bundled
miner repairs task, piece 1 (persist mentioning-theorem fully-qualified names). Synthetic
`.lean` fixtures under tmp_path; no real Mathlib tree, no REPL. See
`tests/test_miner_harvest_mentions.py` for the sibling count-only tests this mirrors."""

import json

from miner.harvest import MentionRecord, compute_theorem_mention_counts, compute_theorem_mentions, write_mention_names
from miner.scan import ScanHit


def _hit(name: str, module_path: str = "Test.lean") -> ScanHit:
    return ScanHit(name=name, module_path=module_path, source_text="def stub := 0")


def test_qualified_mention_is_named_and_located(tmp_path):
    (tmp_path / "A.lean").write_text("theorem uses_it : Finset.pi = Finset.pi := rfl\n", encoding="utf-8")
    mentions = compute_theorem_mentions([_hit("Finset.pi")], tmp_path)
    assert mentions["Finset.pi"] == [
        MentionRecord(
            theorem_name="uses_it",
            source_file="A.lean",
            statement_text="theorem uses_it : Finset.pi = Finset.pi ",
        )
    ]


def test_bare_mention_inside_matching_namespace_is_named_with_its_own_qualification(tmp_path):
    (tmp_path / "Pi.lean").write_text(
        "\n".join(
            [
                "namespace Finset",
                "",
                "theorem pi_nonempty (s : Finset α) (t : ∀ a, Finset (β a)) : (s.pi t).Nonempty ↔ True := trivial",
                "",
                "end Finset",
                "",
            ]
        ),
        encoding="utf-8",
    )
    mentions = compute_theorem_mentions([_hit("Finset.pi")], tmp_path)
    assert len(mentions["Finset.pi"]) == 1
    record = mentions["Finset.pi"][0]
    assert record.theorem_name == "Finset.pi_nonempty"  # the MENTIONING theorem's own name
    assert record.source_file == "Pi.lean"
    assert "pi_nonempty" in record.statement_text


def test_len_mentions_agrees_with_compute_theorem_mention_counts(tmp_path):
    """The core agreement requirement the task calls for: `len(mentions) ==
    theorem_mention_count` for the same corpus and the same hit, since both walk the same
    matching rule over the same underlying scan."""
    (tmp_path / "Mixed.lean").write_text(
        "\n".join(
            [
                "theorem uses_qualified : Finset.empty = Finset.empty := rfl",
                "",
                "namespace Finset",
                "",
                "theorem empty_subset (s : Finset α) : (∅ : Finset α) ⊆ s := trivial",
                "theorem card_empty : (∅ : Finset α).card = 0 := trivial",
                "",
                "end Finset",
                "",
                "namespace List",
                "",
                "theorem unrelated_empty : ([] : List α).length = 0 := trivial",
                "",
                "end List",
                "",
            ]
        ),
        encoding="utf-8",
    )
    hits = [_hit("Finset.empty")]
    mentions = compute_theorem_mentions(hits, tmp_path)
    counts = compute_theorem_mention_counts(hits, tmp_path)
    assert len(mentions["Finset.empty"]) == counts["Finset.empty"]
    assert counts["Finset.empty"] == 3  # 1 qualified + 2 own-namespace bare (via each theorem's own name)


def test_no_mentions_for_a_hit_with_zero_supply(tmp_path):
    (tmp_path / "Empty.lean").write_text("theorem irrelevant : True := trivial\n", encoding="utf-8")
    mentions = compute_theorem_mentions([_hit("Finset.pi")], tmp_path)
    assert mentions["Finset.pi"] == []


def test_root_escaped_mentioning_theorem_is_named_correctly():
    """Piece 1 + Bug A interaction: a `_root_.`-escaped mentioning theorem must be named
    correctly (piece 1's naming is built on the same fixed `_qualify_name` `_capture_def`
    uses), not corrupted the way un-escaped `def` qualification used to be before the fix."""
    from miner.scan import scan_theorem_declarations_with_namespace

    text = "namespace Baz\n\ntheorem _root_.Foo.bar_mentions_pi : Finset.pi = Finset.pi := rfl\n\nend Baz\n"
    results = scan_theorem_declarations_with_namespace(text)
    assert len(results) == 1
    name, _, _ = results[0]
    assert name == "Foo.bar_mentions_pi"


def test_module_doc_block_illustrative_theorem_does_not_produce_a_phantom_mention(tmp_path):
    """Piece 1 + Bug B interaction: an illustrative `theorem`-shaped line inside a `/-!` block
    must not be counted as a real mentioning theorem."""
    (tmp_path / "Doc.lean").write_text(
        "\n".join(
            [
                "/-!",
                "Illustrative:",
                "```",
                "theorem phantom : Finset.pi = Finset.pi := rfl",
                "```",
                "-/",
                "",
                "theorem real_thm : Finset.pi = Finset.pi := rfl",
                "",
            ]
        ),
        encoding="utf-8",
    )
    mentions = compute_theorem_mentions([_hit("Finset.pi")], tmp_path)
    assert len(mentions["Finset.pi"]) == 1
    assert mentions["Finset.pi"][0].theorem_name == "real_thm"


def test_write_mention_names_round_trips_through_json(tmp_path):
    mentions = {
        "Finset.pi": [MentionRecord(theorem_name="Finset.pi_nonempty", source_file="Pi.lean", statement_text="...")],
        "Nat.dist": [],
    }
    output_path = tmp_path / "mention_names.jsonl"
    write_mention_names(mentions, output_path)

    lines = output_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    records = [json.loads(line) for line in lines]
    # sorted by name (deterministic output)
    assert [r["name"] for r in records] == ["Finset.pi", "Nat.dist"]
    assert records[0]["mentions"] == [
        {"theorem_name": "Finset.pi_nonempty", "source_file": "Pi.lean", "statement_text": "..."}
    ]
    assert records[1]["mentions"] == []
