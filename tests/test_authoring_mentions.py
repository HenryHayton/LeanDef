"""Tests for `authoring.mentions` -- pure ranking/capping logic over synthetic `MentionRecord`s,
no REPL/Mathlib/Bedrock involved."""

from authoring.mentions import DEFAULT_MENTION_CAP, rank_mentions, render_mention_excerpt
from miner.harvest import MentionRecord


def _rec(name: str, statement: str, source: str = "Some/File.lean") -> MentionRecord:
    return MentionRecord(theorem_name=name, source_file=source, statement_text=statement)


def test_rank_prefers_more_fully_qualified_references():
    low = _rec("a.low", "theorem a : f x = 1")
    high = _rec("a.high", "theorem a : Nat.clog 2 x = Nat.log 2 x")
    ranked = rank_mentions([low, high])
    assert ranked[0] is high
    assert ranked[1] is low


def test_rank_prefers_shorter_statement_as_tiebreak():
    short = _rec("a.short", "Nat.clog 2 x = 1")
    long = _rec("a.long", "Nat.clog 2 x = 1 ∧ True ∧ True ∧ True ∧ True")
    ranked = rank_mentions([long, short])
    assert ranked[0] is short
    assert ranked[1] is long


def test_rank_dedupes_by_statement_text_keeping_highest_ranked_copy():
    same_text = "Nat.clog 2 x = 1"
    a = _rec("a.first", same_text, source="First.lean")
    b = _rec("a.second", same_text, source="Second.lean")
    ranked = rank_mentions([a, b])
    assert len(ranked) == 1
    assert ranked[0] in (a, b)


def test_rank_caps_to_the_configured_limit():
    records = [_rec(f"a.{i}", f"statement number {i}") for i in range(30)]
    ranked = rank_mentions(records, cap=5)
    assert len(ranked) == 5


def test_default_cap_is_15():
    assert DEFAULT_MENTION_CAP == 15
    records = [_rec(f"a.{i}", f"Nat.clog 2 {i} = statement {i}") for i in range(30)]
    ranked = rank_mentions(records)
    assert len(ranked) == 15


def test_render_excerpt_empty_list():
    assert "no mentioning theorems" in render_mention_excerpt([])


def test_render_excerpt_contains_name_statement_and_source():
    r = _rec("Nat.clog_pow", "Nat.clog b (b ^ n) = n", source="Data/Nat/Log.lean")
    text = render_mention_excerpt([r])
    assert "Nat.clog_pow" in text
    assert "Nat.clog b (b ^ n) = n" in text
    assert "Data/Nat/Log.lean" in text


def test_render_excerpt_respects_cap():
    records = [_rec(f"a.{i}", f"Nat.clog 2 {i} = statement {i}") for i in range(30)]
    text = render_mention_excerpt(records, cap=3)
    assert text.count("\n") == 2  # 3 lines, 2 newlines
