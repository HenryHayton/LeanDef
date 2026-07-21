"""Unit tests for miner.depindex -- the best-effort name -> defining-module index. Operates
on synthetic Mathlib-shaped file trees under tmp_path; no real Mathlib, no REPL."""

from miner.depindex import build_declaration_index


def test_indexes_bare_and_qualified_names_for_a_def(tmp_path):
    (tmp_path / "Data").mkdir()
    (tmp_path / "Data" / "Nat.lean").write_text(
        "namespace Nat\ndef succ (n : ℕ) : ℕ := n + 1\nend Nat\n", encoding="utf-8"
    )
    index = build_declaration_index(tmp_path)
    assert index["succ"] == "Data/Nat.lean"
    assert index["Nat.succ"] == "Data/Nat.lean"


def test_indexes_various_declaration_kinds(tmp_path):
    (tmp_path / "Foo.lean").write_text(
        "\n".join(
            [
                "theorem bar : True := trivial",
                "instance : Inhabited Nat := ⟨0⟩",
                "structure Baz where",
                "  x : Nat",
                "class Qux where",
                "  y : Nat",
                "abbrev Quux := Nat",
                "inductive Corge | a | b",
            ]
        ),
        encoding="utf-8",
    )
    index = build_declaration_index(tmp_path)
    assert index["bar"] == "Foo.lean"
    assert index["Baz"] == "Foo.lean"
    assert index["Qux"] == "Foo.lean"
    assert index["Quux"] == "Foo.lean"
    assert index["Corge"] == "Foo.lean"


def test_first_occurrence_wins_on_bare_name_collision(tmp_path):
    (tmp_path / "A.lean").write_text("def choose (n : ℕ) : ℕ := n\n", encoding="utf-8")
    (tmp_path / "B.lean").write_text("def choose (n : ℕ) : ℕ := n\n", encoding="utf-8")
    index = build_declaration_index(tmp_path)
    # sorted() path order -- A.lean sorts before B.lean
    assert index["choose"] == "A.lean"


def test_section_and_namespace_nesting_tracked(tmp_path):
    (tmp_path / "Nested.lean").write_text(
        "\n".join(
            [
                "namespace Outer",
                "namespace Inner",
                "def helper : ℕ := 0",
                "end Inner",
                "end Outer",
            ]
        ),
        encoding="utf-8",
    )
    index = build_declaration_index(tmp_path)
    assert index["Outer.Inner.helper"] == "Nested.lean"
    assert index["helper"] == "Nested.lean"


def test_private_and_protected_defs_are_indexed(tmp_path):
    (tmp_path / "P.lean").write_text(
        "private def hidden : ℕ := 0\nprotected def shown : ℕ := 0\n", encoding="utf-8"
    )
    index = build_declaration_index(tmp_path)
    assert index["hidden"] == "P.lean"
    assert index["shown"] == "P.lean"


def test_empty_tree_gives_empty_index(tmp_path):
    assert build_declaration_index(tmp_path) == {}
