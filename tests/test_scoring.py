"""Tests for harness.scoring's mechanism dispatch: `decide` facts run as before, `proof`
facts have no adjudication path yet and must fail loudly rather than silently mis-score."""

import pytest

from harness import Fact, PinnedSignature, score_candidate
from harness.scoring import run_facts, splice_candidate

DOUBLE = PinnedSignature(name="double", type_sig="Nat → Nat")


def test_proof_mechanism_fact_raises_not_implemented(lean_server):
    """A `decide` fact splice succeeds; running a `proof`-mechanism fact against it must
    raise NotImplementedError, not silently score it as FAILED or ERRORED."""
    splice = splice_candidate(lean_server, None, DOUBLE.splice("fun n => 2 * n"), timeout=30.0)
    assert splice.status.name == "PASSED", splice.detail

    proof_fact = Fact(
        id="global_never_scored", type="global", mechanism="proof", statement="example : True := trivial"
    )
    with pytest.raises(NotImplementedError, match="prover scaffold"):
        run_facts(lean_server, splice.env, [proof_fact], decide_timeout=30.0)


def test_score_candidate_propagates_not_implemented_for_proof_facts(lean_server):
    """The same guarantee at the score_candidate level: a proof-mechanism fact in the suite
    must not be silently skipped or mis-scored."""
    facts = [
        Fact(id="d1", type="casework", mechanism="decide", statement="example : double 1 = 2 := by decide"),
        Fact(id="g1", type="global", mechanism="proof", statement="example : True := trivial"),
    ]
    with pytest.raises(NotImplementedError, match="prover scaffold"):
        score_candidate(
            lean_server, None, DOUBLE, "fun n => 2 * n", facts, label="mixed", baseline_axioms=frozenset()
        )
