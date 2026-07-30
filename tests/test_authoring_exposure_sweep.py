"""Tests for `authoring.exposure_sweep`. `_scan_file`/`find_name_keyed_instances` are pure text
(a small fixture file, no real Mathlib needed); `build_instance_index` against the real Mathlib
tree is one real-corpus regression, confirming the known `Nat.ModEq` case is found."""

from authoring.exposure_sweep import (
    InstanceHit,
    _scan_file,
    find_name_keyed_instances,
    run_exposure_sweep,
)
from miner.config import MATHLIB_ROOT


def _write(tmp_path, name: str, text: str):
    path = tmp_path / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_scan_file_finds_a_same_line_decidable_instance(tmp_path):
    path = _write(
        tmp_path, "Data/Foo.lean",
        "namespace Nat\ndef ModEq (n a b : ℕ) := a % n = b % n\ninstance : Decidable (ModEq n a b) := inferInstanceAs _\nend Nat\n",
    )
    hits = _scan_file(path, tmp_path)
    assert len(hits) == 1
    assert hits[0] == InstanceHit("Decidable", "ModEq", "Data/Foo.lean", 3, "instance : Decidable (ModEq n a b) := inferInstanceAs _")


def test_scan_file_finds_a_wrapped_signature_within_the_window(tmp_path):
    path = _write(
        tmp_path, "Data/Bar.lean",
        "instance\n  Order.Preimage.decidable (f : α → β) :\n  DecidableRel (CompRel r) := fun _ _ => inferInstance\n",
    )
    hits = _scan_file(path, tmp_path)
    assert any(h.class_name == "DecidableRel" and h.target_head == "CompRel" for h in hits)


def test_scan_file_ignores_non_instance_lines(tmp_path):
    """A `def`/`theorem` merely mentioning `Decidable` in its type (e.g. a lemma ABOUT
    decidability, not an instance declaration) must not be picked up -- only lines under a
    literal `instance` keyword count."""
    path = _write(
        tmp_path, "Data/Qux.lean",
        "theorem decidable_of_iff (h : Decidable (ModEq n a b)) : True := trivial\n",
    )
    hits = _scan_file(path, tmp_path)
    assert hits == []


def test_scan_file_finds_decidable_eq_and_decidable_pred(tmp_path):
    path = _write(
        tmp_path, "Data/Baz.lean",
        "instance : DecidableEq (Lex α) := inferInstanceAs _\ninstance decPred : DecidablePred (SomePred) := fun _ => inferInstance\n",
    )
    hits = _scan_file(path, tmp_path)
    classes_targets = {(h.class_name, h.target_head) for h in hits}
    assert ("DecidableEq", "Lex") in classes_targets
    assert ("DecidablePred", "SomePred") in classes_targets


def test_find_name_keyed_instances_matches_full_name_repo_wide():
    index = [InstanceHit("Decidable", "Nat.ModEq", "Data/Elsewhere.lean", 1, "instance : Decidable (Nat.ModEq n a b) := ...")]
    hits = find_name_keyed_instances("Nat.ModEq", "Data/Nat/ModEq.lean", index)
    assert len(hits) == 1


def test_find_name_keyed_instances_base_name_match_requires_same_file():
    index = [InstanceHit("Decidable", "ModEq", "Data/Unrelated.lean", 1, "instance : Decidable (ModEq n a b) := ...")]
    hits = find_name_keyed_instances("Nat.ModEq", "Data/Nat/ModEq.lean", index)
    assert hits == []  # base-name match in a DIFFERENT file must not count


def test_find_name_keyed_instances_base_name_match_in_own_file_counts():
    index = [InstanceHit("Decidable", "ModEq", "Data/Nat/ModEq.lean", 74, "instance : Decidable (ModEq n a b) := ...")]
    hits = find_name_keyed_instances("Nat.ModEq", "Data/Nat/ModEq.lean", index)
    assert len(hits) == 1


def test_run_exposure_sweep_produces_jsonable_output():
    index = [InstanceHit("Decidable", "ModEq", "Data/Nat/ModEq.lean", 74, "instance : Decidable (ModEq n a b) := ...")]
    result = run_exposure_sweep({"Nat.ModEq": "Data/Nat/ModEq.lean", "Nat.clog": "Data/Nat/Log.lean"}, index=index)
    assert result["Nat.clog"] == []
    assert len(result["Nat.ModEq"]) == 1
    assert result["Nat.ModEq"][0]["class_name"] == "Decidable"


# --- real Mathlib regression (confirms the known case) --------------------------------------


def test_real_mathlib_finds_the_known_nat_modeq_instance():
    from authoring.exposure_sweep import build_instance_index

    index = build_instance_index(MATHLIB_ROOT)
    hits = find_name_keyed_instances("Nat.ModEq", "Data/Nat/ModEq.lean", index)
    assert any(h.class_name == "Decidable" and "ModEq" in h.line_text for h in hits)
