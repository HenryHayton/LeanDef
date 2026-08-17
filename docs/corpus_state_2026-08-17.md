# Corpus state — 17 August 2026

Everything on disk, counted from the shipped files rather than from earlier handoffs.

## 1. Headline

- **392 tasks**, **3,003 facts**, across three authoring generations.
- **392 distinct definitions — zero duplicates across corpora.** Verified by name set.
- **194 Mathlib namespaces**. Top: `Nat` 21, `Equiv` 18, `SimpleGraph` 18, `List` 15,
  `Function` 13, `Set` 13, `Filter` 10, `Finset` 10.
- **391/392 schema-valid.** The one exception is `SimpleGraph.boxProd` (below).
- Bedrock spend to date across all authoring: **14,792 calls, 11.3M in / 5.9M out ≈ $123.**

## 2. The three generations

| | July (29 Jul) | batch 200 (11 Aug) | batch 2500 (16 Aug, running) |
|---|---|---|---|
| tasks | 41 | 172 | 179 |
| facts | 471 | 1,366 | 1,166 |
| mean facts/task | 11.5 | 7.9 | 6.5 |
| suite ≥8 facts | 63% | 56% | 39% |
| ≥1 reject fact | 59% | 73% | 69% |
| ≥1 **certified** reject fact | 32% | 59% | 39% |
| decide share of facts | 42% | 21% | 13% |
| facts kernel-CERTIFIED | 42% | 79% | 73% |
| zero-fact tasks | 0 | 0 | 3 |

Reading the three columns left to right is the project's own history:

**July → batch 200** is the fact-generation overhaul working. Decide share fell 42%→21% and
certification rose 42%→79%. The July suites were long because they were padded with cheap
decidable casework; batch 200's are shorter but far better adjudicated, and the share of tasks
with a *working vacuity detector* (a certified reject fact) nearly doubled, 32%→59%.

**batch 200 → batch 2500** is a pool change, not a pipeline change — same code path, same
prompts. Batch 5 widened the mine to 24 Mathlib subtrees, and the new material is markedly less
decidable: decide share halved again to 13%. Since decide facts are what pushed suites over 8,
suite depth fell with it (56%→39%). Reject coverage held up (73%→69%).

## 3. Facts, in aggregate

- **2,363 proof-mechanism / 640 decide-mechanism.**
- **2,126 CERTIFIED / 877 PROVISIONALLY_VALIDATED** (71% / 29%).
- **634 reject-shaped facts, 397 of them certified (63%).**

The reject-shaped count is the number that matters for vacuity detection: a task without a
certified reject fact cannot demonstrably refute a `:= True` candidate. 397 certified reject
facts is the real teeth in the corpus.

## 4. Mining capacity — what's left

| | scanned | eligible |
|---|---|---|
| batch 4 manifest | 3,185 | 721 |
| batch 5 manifest (wide, 24 subtrees) | 15,387 | 2,609 |

Current batch-2500 pipeline state:

- pool after excluding everything already authored: **2,368**
- preflighted so far: **758** → **693 passing** (91%, matching batch 200's 94%)
- **1,610 names not yet preflighted** (preflight needs only the local REPL, no AWS)
- authored from the passing list: 179 → **514 passing names still queued**
- content-rotation ledger: 19 names that failed on their own content and are excluded

So there is roughly **2,190 definitions of headroom** before the batch-5 eligible pool is
exhausted, without any new mining.

## 5. Downstream artifacts

**Pilot corpus v1** (`training/config/pilot_corpus_v1.json`, seed 20260813): 42 training +
8 held-out (frozen) + 7 score-only annex, all drawn from batch 200's certified-reject
population, each pinned by task hash.

**Model scoring runs** — 6 arms, 1,889 candidate samples, 400 admissible:

| arm | samples | admissible | mean fidelity |
|---|---|---|---|
| qwen2-5-coder-7b-instruct | 410 | 49 | 0.993 |
| qwen3-32b | 406 | 115 | 1.000 |
| goedel-formalizer-v2-8b | 371 | 86 | 0.990 |
| goedel-prover-v2-32b | 349 | 84 | 1.000 |
| goedel-prover-v2-8b | 258 | 49 | 0.995 |
| stepfun-formalizer-32b | 95 | 17 | 1.000 |

**Fidelity ≈ 1.000 everywhere is a known measurement defect, not a result.** FAIL is nearly
unreachable on forward facts — they return PASS or UNKNOWN — and UNKNOWN is excluded from
fidelity's denominator, so a vacuous `:= True` definition scores 1.000. This is documented
against real specimens in `docs/batch_reports/vacuity_specimen_2026-08-11.md`. Separation
against mutant suites, not fidelity, is the signal that survived scrutiny.

**Tier-5 prover adjudication**: 226 forward facts checked, 9 certified; 731 negation facts
checked, 0 certified. The negation direction returning nothing is itself the finding — the
ladder runs forward tactics at a negation with no `push_neg` and no witness search.

## 6. Known defects, all of them

1. **`SimpleGraph.boxProd` is schema-invalid** (1 of 392). Its `domain.conventions` holds a
   real entry alongside a `NONE_DECLARED` sentinel asserting no conventions exist; the two
   contradict. Not in the pilot corpus, so it blocks nothing. Deferred to corpus-v1.1 because
   choosing which entry to drop is a content judgment, not a mechanical re-emission.
2. **3 zero-fact tasks in batch 2500** (~1.7%). Unusable as tasks; trivially filtered on
   `len(facts) == 0`. Concentrated in the exotic head of the batch-5 pool. Fixing it means
   changing ship criteria, which is a design change, so it is flagged rather than done.
3. **877 facts (29%) are PROVISIONALLY_VALIDATED**, not kernel-certified. They ship, but they
   are not evidence.
4. **Fidelity is near-vacuous** as above.
5. **The corpus contains no noncomputable definitions at all** — the miner's fact-supply gate
   filters them out, since they have no decidable facts. The computable/noncomputable fairness
   question cannot be studied on any batch-4- or batch-5-derived corpus.

## 7. Deferred work, recorded so it is not lost

- Mechanical-validation retry with kernel errors fed back to the model.
- Re-run the 16 tasks rotated during batch 200.
- Dossier name-leak fixes.
- Re-mine two quarantined facts (`Nat.log/log_lt_of_lt_pow`, `Nat.divisors/divisors_mem_iff`).
- Preflight the remaining 1,610 batch-2500 names.
