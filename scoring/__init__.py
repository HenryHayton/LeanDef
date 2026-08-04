"""Stage B: scoring one candidate definition end-to-end.

`harness.scoring.run_facts` deliberately raises `NotImplementedError` on proof-mechanism facts
(58% of the 41-task corpus). This package is what closes that gap: it walks a candidate from
raw model completion to a persisted per-fact verdict record, dispatching decide facts to tier 1
and proof facts to the adjudication ladder.

Layering: `harness/` owns splice/admissibility primitives, `ladder/` owns adjudication, and this
package owns the orchestration and the persistence -- including the mapping between the two
status vocabularies, which stays at this boundary rather than leaking either way.
"""
