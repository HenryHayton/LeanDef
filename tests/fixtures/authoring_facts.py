"""Hand-written fixture fact sets for `authoring.validate`, covering the two definitions from
the planned slice suggested by the task that introduced this validator: `Nat.clog` (computable,
boundary-rich -- casework- and global-fact-heavy) and `Monotone` (Prop-valued -- membership-
and global-fact-heavy; see that task's own request for an honest read on whether Monotone's
shape strains the casework/membership split, discussed in the summary this fixture set backs).

Each fixture set returns `(domain, pinned_name, facts, expected)`, where `expected` maps every
fact's `id` to the exact `(Verdict, reason_code)` pair `tests/test_authoring_validate.py`
asserts against -- not just "rejected", per the task's own instruction.

Domain choices, and why (see the summary's "judgment calls" list for the full discussion):

- `Nat.clog`'s constraint `1 < b ∧ b ≤ 12 ∧ 1 < n` is *not* purely dictated by the
  mathematics -- `Nat.clog`'s own definition (`Mathlib/Data/Nat/Log.lean`) case-splits on
  exactly `1 < b ∧ 1 < n`, with everything else (`b ≤ 1` or `n ≤ 1`) a junk value of `0`. That
  natural constraint plus its junk-value conventions exhaustively partitions `ℕ × ℕ` --
  meaning there is no way to construct a genuine OUT_OF_DOMAIN fact for `Nat.clog` without an
  extra, deliberately authoring-side restriction. The `b ≤ 12` clause is that restriction: a
  stand-in for "this task's fact suite only authors casework for small bases" (a realistic
  authoring-time scoping decision, not a mathematical one), added specifically so this fixture
  set can exercise OUT_OF_DOMAIN at all.
- `Monotone`'s constraint is the unrestricted `True` sentinel -- genuinely correct here, not a
  simplification: `Monotone f` is defined for every `f` between any two preorders, with no
  restricted region the way `Nat.clog` has junk values. Its OUT_OF_DOMAIN coverage is
  therefore carried entirely by the `Nat.clog` fixture set.
"""

from authoring.facts import ConventionPoint, DomainSpec, ProposedFact
from authoring.validate import ReasonCode, Verdict

# --- Nat.clog -----------------------------------------------------------------------------

CLOG_DOMAIN = DomainSpec(
    constraint="1 < b ∧ b ≤ 12 ∧ 1 < n",
    conventions=[
        ConventionPoint(
            point="b ≤ 1",
            statement="Nat.clog b n = 0 for b ≤ 1",
            note="Mathlib convention: a base of 0 or 1 has no valid logarithm; clog is defined as 0",
            predicate="b ≤ 1",
        ),
        ConventionPoint(
            point="n ≤ 1",
            statement="Nat.clog b n = 0 for n ≤ 1",
            note="Mathlib convention: the ceiling-log of 0 or 1 is trivially 0",
            predicate="n ≤ 1",
        ),
    ],
)
CLOG_NAME = "Nat.clog"


def clog_fixture_set() -> tuple[DomainSpec, str, list[ProposedFact], dict[str, tuple[Verdict, str]]]:
    facts = [
        # -- valid casework, inside the main constraint --
        ProposedFact(
            id="clog_2_37",
            type="casework",
            mechanism="decide",
            statement="example : Nat.clog 2 37 = 6 := by decide",
            domain_inputs={"b": "2", "n": "37"},
        ),
        ProposedFact(
            id="clog_2_64",
            type="casework",
            mechanism="decide",
            statement="example : Nat.clog 2 64 = 6 := by decide",
            domain_inputs={"b": "2", "n": "64"},
        ),
        ProposedFact(
            id="clog_3_10",
            type="casework",
            mechanism="decide",
            statement="example : Nat.clog 3 10 = 3 := by decide",
            domain_inputs={"b": "3", "n": "10"},
        ),
        # -- valid casework, in-domain via a stated convention point (not the main constraint) --
        ProposedFact(
            id="clog_junk_n_eq_1",
            type="casework",
            mechanism="decide",
            statement="example : Nat.clog 5 1 = 0 := by decide",
            domain_inputs={"b": "5", "n": "1"},
        ),
        ProposedFact(
            id="clog_junk_b_eq_0",
            type="casework",
            mechanism="decide",
            statement="example : Nat.clog 0 37 = 0 := by decide",
            domain_inputs={"b": "0", "n": "37"},
        ),
        # -- bad: false of the ground truth (clog 2 37 is 6, not 5) --
        ProposedFact(
            id="clog_false",
            type="casework",
            mechanism="decide",
            statement="example : Nat.clog 2 37 = 5 := by decide",
            domain_inputs={"b": "2", "n": "37"},
        ),
        # -- bad: out of domain (b = 100 exceeds this task's b <= 12 authoring scope, and
        # isn't covered by either convention point) --
        ProposedFact(
            id="clog_out_of_domain",
            type="casework",
            mechanism="decide",
            statement="example : Nat.clog 100 37 = 1 := by decide",
            domain_inputs={"b": "100", "n": "37"},
        ),
        # -- valid global fact, no quantifier over the domain's variables at all (a concrete
        # base) -- the clean provisionally-validated path --
        ProposedFact(
            id="clog_global_monotone",
            type="global",
            mechanism="proof",
            statement="Monotone (Nat.clog 2)",
            anchors=["Nat.clog_monotone"],
        ),
        # -- valid global fact, universally quantified but phrased over different variable
        # names (x, not n) than the domain constraint -- correctly flagged for human review by
        # the structural domain heuristic, not rejected; see the summary for why this is the
        # expected, intended outcome rather than a bug --
        ProposedFact(
            id="clog_global_pow",
            type="global",
            mechanism="proof",
            statement="∀ b x : ℕ, 1 < b → Nat.clog b (b ^ x) = x",
            anchors=["Nat.clog_pow"],
        ),
        # -- bad: cites a nonexistent anchor theorem --
        ProposedFact(
            id="clog_global_bad_anchor",
            type="global",
            mechanism="proof",
            statement="∀ b x : ℕ, 1 < b → Nat.clog b (b ^ x) = x",
            anchors=["Nat.clog_this_theorem_does_not_exist"],
        ),
        # -- bad: statement doesn't elaborate (genuine syntax error) --
        ProposedFact(
            id="clog_global_bad_syntax",
            type="global",
            mechanism="proof",
            statement="∀ n : ℕ, Nat.clog 2 n +++ 1 = n",
            anchors=["Nat.clog_pow"],
        ),
    ]

    expected = {
        "clog_2_37": (Verdict.ACCEPTED, ReasonCode.CERTIFIED_TRUE_OF_GROUND_TRUTH),
        "clog_2_64": (Verdict.ACCEPTED, ReasonCode.CERTIFIED_TRUE_OF_GROUND_TRUTH),
        "clog_3_10": (Verdict.ACCEPTED, ReasonCode.CERTIFIED_TRUE_OF_GROUND_TRUTH),
        "clog_junk_n_eq_1": (Verdict.ACCEPTED, ReasonCode.CERTIFIED_TRUE_OF_GROUND_TRUTH),
        "clog_junk_b_eq_0": (Verdict.ACCEPTED, ReasonCode.CERTIFIED_TRUE_OF_GROUND_TRUTH),
        "clog_false": (Verdict.REJECTED, ReasonCode.FALSE_OF_GROUND_TRUTH),
        "clog_out_of_domain": (Verdict.REJECTED, ReasonCode.OUT_OF_DOMAIN),
        "clog_global_monotone": (Verdict.PROVISIONALLY_VALIDATED, ReasonCode.STRUCTURAL_ONLY_NO_PROVER),
        "clog_global_pow": (Verdict.FLAGGED, ReasonCode.GLOBAL_DOMAIN_UNCHECKED),
        "clog_global_bad_anchor": (Verdict.REJECTED, ReasonCode.ANCHOR_NOT_FOUND),
        "clog_global_bad_syntax": (Verdict.REJECTED, ReasonCode.PROPOSITION_DOES_NOT_ELABORATE),
    }
    return CLOG_DOMAIN, CLOG_NAME, facts, expected


# --- Monotone -------------------------------------------------------------------------------

MONOTONE_DOMAIN = DomainSpec(constraint="True", conventions=[])
MONOTONE_NAME = "Monotone"

_DIP_INSTANCE = "(fun n : Fin 3 => if n = 0 then (2 : Fin 3) else n)"
_DIP_STATEMENT = f"example : ¬ Monotone {_DIP_INSTANCE} := by decide"


def monotone_fixture_set() -> tuple[DomainSpec, str, list[ProposedFact], dict[str, tuple[Verdict, str]]]:
    facts = [
        # -- valid, decidable membership over small finite carriers --
        ProposedFact(
            id="monotone_accept_fin3_id",
            type="membership",
            mechanism="decide",
            statement="example : Monotone (fun n : Fin 3 => n) := by decide",
            instance="(fun n : Fin 3 => n)",
            polarity="accept",
            expected_type="Fin 3 → Fin 3",
        ),
        ProposedFact(
            id="monotone_reject_fin3_dip",
            type="membership",
            mechanism="decide",
            statement=_DIP_STATEMENT,
            instance=_DIP_INSTANCE,
            polarity="reject",
            violated_property="a <= b -> f a <= f b fails at a=0, b=1: f 0 = 2 > f 1 = 1",
            expected_type="Fin 3 → Fin 3",
        ),
        ProposedFact(
            id="monotone_accept_fin5_const",
            type="membership",
            mechanism="decide",
            statement="example : Monotone (fun _ : Fin 5 => (2 : Fin 5)) := by decide",
            instance="(fun _ : Fin 5 => (2 : Fin 5))",
            polarity="accept",
            expected_type="Fin 5 → Fin 5",
        ),
        # -- bad: instance term doesn't elaborate --
        ProposedFact(
            id="monotone_bad_instance",
            type="membership",
            mechanism="decide",
            statement="example : Monotone (fun n : Fin 3 => n + garbage_token) := by decide",
            instance="(fun n : Fin 3 => n + garbage_token)",
            polarity="accept",
            expected_type="Fin 3 → Fin 3",
        ),
        # -- bad: reject-polarity instance missing violated_property --
        ProposedFact(
            id="monotone_bad_missing_violated_property",
            type="membership",
            mechanism="decide",
            statement=_DIP_STATEMENT,
            instance=_DIP_INSTANCE,
            polarity="reject",
            violated_property=None,
            expected_type="Fin 3 → Fin 3",
        ),
        # -- valid, proof-mechanism membership (infinite carrier -- no prover exists yet, so
        # this is structural-only, provisionally validated, never accepted) --
        ProposedFact(
            id="monotone_proof_id_nat",
            type="membership",
            mechanism="proof",
            statement="Monotone (fun n : ℕ => n)",
            instance="(fun n : ℕ => n)",
            polarity="accept",
            expected_type="ℕ → ℕ",
        ),
        # -- valid global fact: Monotone.comp, real anchor, unrestricted domain so the
        # structural domain heuristic never fires regardless of quantification --
        ProposedFact(
            id="monotone_global_comp",
            type="global",
            mechanism="proof",
            statement="∀ (f g : ℕ → ℕ), Monotone f → Monotone g → Monotone (f ∘ g)",
            anchors=["Monotone.comp"],
        ),
    ]

    expected = {
        "monotone_accept_fin3_id": (Verdict.ACCEPTED, ReasonCode.CERTIFIED_TRUE_OF_GROUND_TRUTH),
        "monotone_reject_fin3_dip": (Verdict.ACCEPTED, ReasonCode.CERTIFIED_TRUE_OF_GROUND_TRUTH),
        "monotone_accept_fin5_const": (Verdict.ACCEPTED, ReasonCode.CERTIFIED_TRUE_OF_GROUND_TRUTH),
        "monotone_bad_instance": (Verdict.REJECTED, ReasonCode.INSTANCE_DOES_NOT_ELABORATE),
        "monotone_bad_missing_violated_property": (
            Verdict.REJECTED,
            ReasonCode.MALFORMED_MISSING_VIOLATED_PROPERTY,
        ),
        "monotone_proof_id_nat": (Verdict.PROVISIONALLY_VALIDATED, ReasonCode.STRUCTURAL_ONLY_NO_PROVER),
        "monotone_global_comp": (Verdict.PROVISIONALLY_VALIDATED, ReasonCode.STRUCTURAL_ONLY_NO_PROVER),
    }
    return MONOTONE_DOMAIN, MONOTONE_NAME, facts, expected
