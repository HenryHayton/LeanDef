"""Schema v1.2 fields must survive authoring -> task.json -> scoring (11 Aug 2026).

The standing debt this closes: `self_restatement` was computed by the fact-proposal call and
documented as "authoring-time-only: never reaches a shipped task.json fact entry", so no scorer
could act on it. 13.1% of proof-mechanism facts in the authored corpus turned out to be
rfl-provable restatements of the definition, invisible downstream.
"""

from authoring.emit import _fact_to_dict
from harness.facts import Fact


def _round_trip(f: Fact) -> Fact:
    return Fact.from_dict(_fact_to_dict(f))


def test_self_restatement_reaches_the_shipped_fact():
    f = Fact(id="g", type="global", mechanism="proof", statement="∀ n, P n",
             self_restatement=True)
    assert _fact_to_dict(f)["self_restatement"] is True
    assert _round_trip(f).self_restatement is True


def test_polarity_ships_on_every_fact_not_just_membership():
    """42 of the corpus's 88 reject-shaped facts were unlabelled and could only be found by
    regex-sniffing, so the reject-fact floor had nothing to count."""
    g = Fact(id="g", type="global", mechanism="proof", statement="¬ VTask.P w",
             polarity="reject", violated_property="closure")
    d = _fact_to_dict(g)
    assert d["polarity"] == "reject"
    assert d["violated_property"] == "closure"


def test_near_miss_and_boundary_labels_round_trip():
    f = Fact(id="m", type="membership", mechanism="decide", statement="x", instance="w",
             polarity="reject", violated_property="assoc", near_miss_clause="assoc",
             boundary_vs_interior="boundary")
    back = _round_trip(f)
    assert back.near_miss_clause == "assoc"
    assert back.boundary_vs_interior == "boundary"


def test_resolved_anchors_round_trip():
    f = Fact(id="g", type="global", mechanism="proof", statement="∀ n, P n",
             anchors=["Nat.foo"], anchors_resolved=["Nat.foo_bar"])
    assert _round_trip(f).anchors_resolved == ["Nat.foo_bar"]


def test_pre_v12_task_json_still_loads():
    """Every existing task.json predates these keys; absence must default, never raise."""
    old = {"id": "f", "type": "global", "mechanism": "proof", "statement": "∀ n, P n",
           "domain_inputs": {}, "anchors": [], "validation_status": "CERTIFIED",
           "discharge": None, "cached_script": None, "axiom_closure": None, "provenance": None}
    f = Fact.from_dict(old)
    assert f.self_restatement is False and f.near_miss_clause is None
    assert f.anchors_resolved == []
