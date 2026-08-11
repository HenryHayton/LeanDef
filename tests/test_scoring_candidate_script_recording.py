"""Winning tactics must be recorded on PASS verdicts (11 Aug 2026).

`script` was empty for all 553 tier-2 wins in the 32B corpus, which made the self-citation
failure mode -- `exact?` closing a goal by finding the fact's own anchor theorem in Mathlib,
measured at 100% of certified facts in the tier-cascade study -- invisible at scoring time.
"""

from scoring.candidate import FactVerdict
from scoring.verdicts import Verdict


def test_script_is_serialised_on_pass():
    v = FactVerdict(fact_id="f", mechanism="proof", verdict=Verdict.PASS, tier=2,
                    certified_via="fact", elapsed_s=0.1, script="intros <;> simp [VTask.X]")
    assert v.to_dict()["script"] == "intros <;> simp [VTask.X]"


def test_script_key_always_present_even_when_unknown():
    """Absent-vs-null must be distinguishable by readers; the key is always emitted."""
    v = FactVerdict(fact_id="f", mechanism="proof", verdict=Verdict.UNKNOWN, tier=None,
                    certified_via="fact", elapsed_s=0.1)
    d = v.to_dict()
    assert "script" in d and d["script"] is None
