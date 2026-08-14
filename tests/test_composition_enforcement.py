"""Suite-composition caps are ENFORCED, not merely requested.

From the 3-task calibration (11 Aug 2026): the prompt calls the decide cap "hard", and
`List.nextOr` still came back with 10 decide facts; `ArithmeticFunction.dirichletInverseFun`
came back with 6 facts against a floor of 8. A prompt only asks.
"""

from dataclasses import dataclass

from authoring.composition import DECIDE_CAP, enforce


@dataclass
class F:
    id: str
    mechanism: str = "proof"
    statement: str = "P x"
    polarity: str | None = None
    boundary_vs_interior: str | None = None


def _decides(n, *, boundary=0):
    return [F(id=f"d{i}", mechanism="decide",
              boundary_vs_interior="boundary" if i < boundary else "interior")
            for i in range(n)]


def test_decide_cap_is_applied():
    out = enforce(_decides(10) + [F(id="g")])
    assert sum(1 for f in out.kept if f.mechanism == "decide") == DECIDE_CAP
    assert out.trimmed_decide == 4


def test_trimming_drops_interior_before_boundary():
    """An interior spot-check survives every plausible misreading, so it is the weakest fact in
    the suite and must be the first to go."""
    out = enforce(_decides(9, boundary=6))
    kept = [f for f in out.kept if f.mechanism == "decide"]
    assert all(f.boundary_vs_interior == "boundary" for f in kept)
    assert all(f.boundary_vs_interior == "interior" for f in out.dropped)


def test_unlabelled_decide_facts_are_treated_as_interior():
    labelled = [F(id=f"b{i}", mechanism="decide", boundary_vs_interior="boundary") for i in range(6)]
    unlabelled = [F(id=f"u{i}", mechanism="decide") for i in range(3)]
    out = enforce(labelled + unlabelled)
    assert {f.id for f in out.dropped} == {"u0", "u1", "u2"}


def test_reject_floor_violation_is_reported():
    out = enforce([F(id=f"g{i}") for i in range(10)])
    assert any("reject_floor" in v for v in out.violations)


def test_reject_detected_from_statement_when_polarity_absent():
    """42 of the corpus's 88 reject-shaped facts carried no polarity label."""
    facts = [F(id="r1", statement="¬ VTask.P w"), F(id="r2", statement="3 ∉ VTask.S 4")]
    facts += [F(id=f"g{i}") for i in range(8)]
    out = enforce(facts)
    assert not any("reject_floor" in v for v in out.violations)


def test_suite_floor_reported_but_nothing_invented():
    out = enforce([F(id=f"g{i}") for i in range(6)] + [F(id="r", statement="¬ P"),
                                                       F(id="r2", statement="x ≠ y")])
    assert len(out.kept) == 8
    out2 = enforce([F(id="r", statement="¬ P"), F(id="r2", statement="x ≠ y")])
    assert any("suite_floor" in v for v in out2.violations)
    assert len(out2.kept) == 2, "enforcement must never invent facts to reach the floor"


class TestTopUpRespectsTheCap:
    """The reject top-up must not smuggle facts past the decide cap.

    Measured on the 200-task run: 13 suites shipped over-cap because top-up additions were
    appended AFTER composition had trimmed. `Equiv.sumProdDistrib` is the specimen -- its last
    two facts are reject-polarity decide facts taking it from 6 to 8. This matters beyond the
    count, since the cap is due to be raised to 8 and an unenforced cap is unpredictable at any
    value.
    """

    def test_topup_decide_facts_beyond_the_cap_are_trimmed(self):
        kept = [F(id=f"d{i}", mechanism="decide") for i in range(DECIDE_CAP)]
        kept += [F(id="g0"), F(id="g1")]
        topup = [F(id="r0", mechanism="decide", polarity="reject"),
                 F(id="r1", mechanism="decide", polarity="reject")]
        out = enforce(kept + topup)
        n_decide = sum(1 for f in out.kept if f.mechanism == "decide")
        assert n_decide == DECIDE_CAP, f"cap breached by top-up: {n_decide}"

    def test_proof_mechanism_topup_facts_are_never_trimmed_by_the_decide_cap(self):
        kept = [F(id=f"d{i}", mechanism="decide") for i in range(DECIDE_CAP)]
        topup = [F(id="r0", statement="¬ VTask.P w"), F(id="r1", statement="w ∉ VTask.S")]
        out = enforce(kept + topup)
        assert {f.id for f in topup} <= {f.id for f in out.kept}
