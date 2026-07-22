"""Unit tests for miner.harvest.compute_theorem_mention_counts -- the namespace-scoped,
union-of-qualified-and-bare mention counting fixed per docs/theorem_mention_audit.md (H1) and
docs/theorem_mention_audit.md (H2). Synthetic `.lean` fixtures under tmp_path, reproducing the
audit's confirmed patterns; no real Mathlib tree, no REPL."""

from miner.harvest import compute_theorem_mention_counts
from miner.scan import ScanHit


def _hit(name: str, module_path: str = "Test.lean") -> ScanHit:
    return ScanHit(name=name, module_path=module_path, source_text="def stub := 0")


def test_qualified_mention_counted_regardless_of_namespace(tmp_path):
    (tmp_path / "A.lean").write_text(
        "theorem uses_it : Finset.pi = Finset.pi := rfl\n", encoding="utf-8"
    )
    counts = compute_theorem_mention_counts([_hit("Finset.pi")], tmp_path)
    assert counts["Finset.pi"] == 1


def test_bare_mention_inside_matching_namespace_is_counted(tmp_path):
    """Reproduces the qualitative shape of the audit's Finset.pi finding: several theorem
    statements inside `namespace Finset ... end Finset` mention `pi` bare, never qualified."""
    (tmp_path / "Pi.lean").write_text(
        "\n".join(
            [
                "namespace Finset",
                "",
                "theorem pi_nonempty (s : Finset α) (t : ∀ a, Finset (β a)) : (s.pi t).Nonempty ↔ True := trivial",
                "",
                "theorem card_pi (s : Finset α) (t : ∀ a, Finset (β a)) : (s.pi t).card = 0 := trivial",
                "",
                "theorem mem_pi (s : Finset α) (t : ∀ a, Finset (β a)) : True := trivial",
                "",
                "end Finset",
                "",
            ]
        ),
        encoding="utf-8",
    )
    counts = compute_theorem_mention_counts([_hit("Finset.pi")], tmp_path)
    assert counts["Finset.pi"] == 3


def test_bare_mention_in_unrelated_namespace_is_not_counted_collision_case(tmp_path):
    """Explicit acceptance case: a bare `pi` inside an unrelated namespace (here `Real`, where
    `pi` means the mathematical constant) must NOT count toward `Finset.pi` -- the collision
    the audit quantified at up to 98% noise for unscoped bare matching."""
    (tmp_path / "RealPi.lean").write_text(
        "\n".join(
            [
                "namespace Real",
                "",
                "theorem pi_pos : 0 < pi := trivial",
                "theorem pi_gt_three : pi > 3 := trivial",
                "",
                "end Real",
                "",
            ]
        ),
        encoding="utf-8",
    )
    counts = compute_theorem_mention_counts([_hit("Finset.pi")], tmp_path)
    assert counts["Finset.pi"] == 0


def test_mixed_qualified_and_scoped_bare_and_collision_all_at_once(tmp_path):
    """One combined fixture: a qualified mention (counts), several own-namespace bare
    mentions (count), and unrelated-namespace bare mentions (must not count) -- reproducing
    the full pattern behind the audit's Finset.empty finding (0 -> ~95 on the real corpus)."""
    (tmp_path / "Empty.lean").write_text(
        "\n".join(
            [
                "theorem uses_qualified : Finset.empty = Finset.empty := rfl",
                "",
                "namespace Finset",
                "",
                "theorem empty_subset (s : Finset α) : (∅ : Finset α) ⊆ s := trivial",
                "theorem card_empty : (∅ : Finset α).card = 0 := trivial",
                "theorem not_mem_empty (a : α) : a ∉ (∅ : Finset α) := trivial",
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
    counts = compute_theorem_mention_counts([_hit("Finset.empty")], tmp_path)
    # 1 qualified + 3 own-namespace bare mentions ("∅" isn't the bare name "empty", so those
    # three lines only count because "empty" also appears in each theorem's own NAME, e.g.
    # `empty_subset`/`card_empty`/`not_mem_empty` -- a legitimate bare substring match, same
    # mechanism the audit's real-corpus recount relied on).
    assert counts["Finset.empty"] == 4


def test_top_level_unnamespaced_candidate_counts_correctly(tmp_path):
    """A candidate with no namespace (bare name == qualified name) must still work: the
    qualified branch alone already covers everything, no double counting via the bare branch."""
    (tmp_path / "TopLevel.lean").write_text(
        "theorem uses_max_default : maxDefault = maxDefault := rfl\n", encoding="utf-8"
    )
    counts = compute_theorem_mention_counts([_hit("maxDefault")], tmp_path)
    assert counts["maxDefault"] == 1


def test_no_double_counting_when_both_qualified_and_bare_would_match_same_statement(tmp_path):
    """A single statement that legitimately contains the qualified name inside its own
    namespace must be counted exactly once, not twice (qualified branch and bare branch must
    be mutually exclusive per statement)."""
    (tmp_path / "Dup.lean").write_text(
        "\n".join(
            [
                "namespace Finset",
                "",
                "theorem self_ref (s : Finset α) : Finset.pi = Finset.pi := rfl",
                "",
                "end Finset",
                "",
            ]
        ),
        encoding="utf-8",
    )
    counts = compute_theorem_mention_counts([_hit("Finset.pi")], tmp_path)
    assert counts["Finset.pi"] == 1


def test_named_argument_syntax_no_longer_truncates_mention_out_of_statement(tmp_path):
    """Regression for the H2 truncation fix: a mention appearing after a named-argument `:=`
    inside the statement (not the candidate's own name -- a different name used earlier in the
    same statement) must not cause the candidate's own later mention to be discarded."""
    (tmp_path / "Trunc.lean").write_text(
        "lemma foo : Injective (bar (a := a)) ∧ Finset.pi = Finset.pi := by simp\n",
        encoding="utf-8",
    )
    counts = compute_theorem_mention_counts([_hit("Finset.pi")], tmp_path)
    assert counts["Finset.pi"] == 1
