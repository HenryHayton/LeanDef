"""Acceptance tests for the verification cache (batch 5): reuse + crash resume.

Written from the two failures that motivated it -- a re-verify-everything harvest, and a long
run with no on-disk checkpoint -- per the house rule that an observed failure becomes a test.
No REPL: `verify_all_with_recovery` is driven with a cache that already contains the answers,
so the "did it avoid the REPL" assertion is exactly that no server call happened.
"""

import json

import pytest

from miner.verified_cache import append_records, cache_key, load_cache
from miner.verify import BinderGroup, VerifiedDef, verify_all_with_recovery
from miner.scan import ScanHit


def _vd(name="Test.foo", module_path="Test.lean", source_text="def foo := 1"):
    return VerifiedDef(
        name=name, module_path=module_path, source_text=source_text, docstring="doc",
        mention_count=3, included=True, elaborates=True,
        binder_groups=[BinderGroup(kind="explicit", names=["n"], type_text="ℕ")],
        explicit_arg_types=["ℕ"], return_type="ℕ", executable=True, exec_mechanism="eval",
        output_decidable_eq=True, referenced_constants=["Nat.succ"], axioms=[],
    )


def _hit(v):
    return ScanHit(name=v.name, module_path=v.module_path, source_text=v.source_text)


class _ExplodingServer:
    """Any REPL access at all is a test failure -- the cache must make it unnecessary."""

    def __getattr__(self, item):
        raise AssertionError(f"cache miss reached the REPL (accessed {item!r})")


def test_roundtrip_restores_binder_groups_as_dataclasses(tmp_path):
    """asdict() flattens nested dataclasses; a dict here would fail far from the cause."""
    path = tmp_path / "cache.jsonl"
    append_records([_vd()], path)
    restored = load_cache(path)
    (only,) = restored.values()
    assert isinstance(only.binder_groups[0], BinderGroup)
    assert only.binder_groups[0].type_text == "ℕ"
    assert only.referenced_constants == ["Nat.succ"]


def test_cached_hit_is_reused_without_touching_the_repl(tmp_path):
    path = tmp_path / "cache.jsonl"
    v = _vd()
    append_records([v], path)
    out = verify_all_with_recovery(
        _ExplodingServer(), 0, [_hit(v)], cache=load_cache(path), cache_path=None)
    assert [r.name for r in out] == [v.name]


def test_changed_source_text_is_not_served_from_cache(tmp_path):
    """The key hashes the body: a definition whose text changed is a different definition, and
    reusing a stale record would silently gate the wrong text.

    A miss cannot be detected by expecting a raise: `harness.repl.run_checked` deliberately
    converts ANY unexpected exception into an ERRORED result so one bad call cannot stall a
    batch (its own docstring says so), which swallows the exploding server's AssertionError.
    So the miss is asserted on the OUTCOME -- the cached record has included=True, and a record
    that actually went to the (broken) REPL cannot.
    """
    path = tmp_path / "cache.jsonl"
    append_records([_vd(source_text="def foo := 1")], path)
    cache = load_cache(path)
    changed = _hit(_vd(source_text="def foo := 2"))
    (out,) = verify_all_with_recovery(_ExplodingServer(), 0, [changed], cache=cache)
    assert not out.included, "stale cache record was served for changed source text"
    assert out.source_text == "def foo := 2"


def test_torn_final_line_does_not_abort_loading(tmp_path):
    """A kill -9 mid-write must cost one record, not the whole cache."""
    path = tmp_path / "cache.jsonl"
    append_records([_vd(name="A.one"), _vd(name="B.two")], path)
    with path.open("a", encoding="utf-8") as fh:
        fh.write('{"name": "C.three", "module_pa')  # torn
    loaded = load_cache(path)
    assert {v.name for v in loaded.values()} == {"A.one", "B.two"}


def test_missing_cache_file_is_empty_not_an_error(tmp_path):
    assert load_cache(tmp_path / "nope.jsonl") == {}


def test_cache_key_is_stable_and_source_sensitive():
    a = cache_key("N.f", "M.lean", "def f := 1")
    assert a == cache_key("N.f", "M.lean", "def f := 1")
    assert a != cache_key("N.f", "M.lean", "def f := 2")
    assert a != cache_key("N.g", "M.lean", "def f := 1")
