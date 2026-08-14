# Pilot corpus v1 — selection memo

**Date:** 13 August 2026. **Config:** `training/config/pilot_corpus_v1.json`.
**Seed:** 20260813. **Corpus hash:** `062ffd01b8fbf21c4ff6dc5bd39a1a03…`
**Drawn from:** the 172 shipped tasks in `prelim_testing/tasks_batch200/` (read-only; nothing
modified). Every selected task is pinned by a SHA-256 of its `task.json`, so any later mutation
by the authoring session's retry work is detectable at harvest time.

**Shape:** 42 training + 8 held-out (frozen) + 7 score-only annex.

---

## 1. Population, recomputed from the shipped files

The handoff's ladder was not trusted; membership was recomputed. It agrees exactly.

| population | tasks |
|---|---|
| **certified-reject** (≥1 kernel-CERTIFIED reject fact) — the main pool | **88** |
| uncertified-reject (has reject facts, none certified) — the annex pool | 38 |
| no reject fact at all — excluded entirely | 46 |
| total shipped | 172 |

All 50 main-corpus tasks come from the 88, so every training task has a demonstrably working
vacuity detector and the verified filter has certified teeth wherever it filters.

---

## 2. Strata: population share vs selected share

### Return shape — matched to within 1pp

| | population (88) | selected (50) |
|---|---|---|
| value | 54 (61%) | 30 (60%) |
| prop | 24 (27%) | 14 (28%) |
| bundled | 10 (11%) | 6 (12%) |

### Suite strength — deliberately biased upward, as instructed

| | population | selected |
|---|---|---|
| ≥8 facts | 63 (72%) | **47 (94%)** |
| <8 facts | 25 (28%) | 3 (6%) |

The three thin suites are all hard tasks kept for difficulty coverage (§4); the bias is
deliberate, since survivor-filtering quality depends on suite depth.

### Namespace spread

Cap of 5 per family, never exceeded: `Nat` 5, `Set` 5, `SimpleGraph` 5, `Equiv` 4, `Finset` 4,
`List` 4, `Function` 3, then 20 families with 1–2 each. **27 distinct families across 50 tasks**
(the certified population has 43).

### Definition style — the stratum that gave

| | population | selected |
|---|---|---|
| computable | **88 (100%)** | 50 (100%) |
| noncomputable | 0 | 0 |
| well-founded | 0 | 0 |

**This axis is degenerate and could not constrain the selection.** It is listed first in the
spec, so per the tie-break rule it "gave" and the remaining axes were satisfied in order. See §5
for why, and for the metadata problems behind it.

---

## 3. Held-out split (8, frozen)

Includes 2 hard tasks and spans all three return shapes.

| task | shape | facts | hard |
|---|---|---|---|
| AList.insertRec | value | 3 | ✅ |
| Equiv.sumPiEquivProdPi | bundled | 9 | ✅ |
| piFinTwoEquiv | bundled | 10 | ✅ |
| Function.update | value | 10 | |
| Int.land | value | 9 | |
| Set.codRestrict | value | 11 | |
| SuccChain | value | 9 | |
| SupPrime | prop | 13 | |

Frozen at creation, never sampled for training, seed and corpus hash recorded in the config.

---

## 4. Hard tasks (10) — one line each

Scored on construction shape, not arithmetic smoothness: body length, pattern-matching recursion,
bundled structures, anonymous-constructor bundles, hypothesis arguments, dependent/universe
polymorphism, richness.

| task | why it qualifies |
|---|---|
| `YoungDiagram.ofRowLens` | 498c body; **hypothesis argument** (`hw : w.SortedGE`); dependent; bundle construction |
| `Equiv.sumCompl` | 359c; bundled `Equiv`; anonymous-constructor; richness 6 |
| `SimpleGraph.sum` | 341c; **pattern-matching recursion**; richness 6 |
| `Composition.embedding` | 321c; bundled structure; richness 6 |
| `SimpleGraph.Walk.dropUntil` | 303c; pattern-matching recursion over walks; richness 6 |
| `AList.insertRec` | 300c; recursion + bundle + dependent motive `C : AList β → Sort*` |
| `Equiv.sumAssoc` | 273c; bundled `Equiv`; anonymous-constructor |
| `Equiv.sumProdDistrib` | 248c; bundled `Equiv`; anonymous-constructor |
| `Equiv.sumPiEquivProdPi` | 234c; bundled; dependent Π-types; richness 6 |
| `piFinTwoEquiv` | 206c; bundled; dependent family over `Fin 2` |

**Expected to produce few or no survivors.** That is the point: an all-easy 50 forecloses the
pilot's most valuable possible specimen (a survivor on a task the base model rarely solves), and
zero survivors here is itself a measurement that exercises the N-escalation path in round 2.

Note the hard tier is heavily `Equiv`-flavoured (4 of 10) because bundled equivalences are where
construction difficulty concentrates in this pool; the family cap held it at 4.

---

## 5. Findings and judgment calls — read this part

### 5.1 `definition_style` was specified but never ships

The schema-v1.2 work listed "definition-style label on the task (computable / noncomputable /
well-founded-recursion) for the scoring-time fairness reporting" as a deliverable. **It is not in
any shipped `task.json`.** Confirmed: neither `harness/task_schema.py` nor `authoring/emit.py`
mentions it. It was specified, agreed, and silently not implemented.

### 5.2 The obvious fallback is also broken — and would have lied

Deriving style from the miner manifest's `verified.source_text` returns **100% computable across
all 172**, which is false. The miner's scan captures the declaration starting at `def` or
`protected`, so a preceding `noncomputable` modifier is *structurally outside the captured text*.
Mathlib contains **5,825 `noncomputable def`** occurrences. Anyone stratifying on that field
would have got a confident, wrong answer.

Style was therefore derived from the **actual Mathlib source files**, matching the declaration
line only. An intermediate version that scanned two lines of context produced two false positives
— `PartialEquiv.pi` and `IsOrderRightAdjoint` matched "partial" from **docstring prose**, and
`Multiset.strongInductionOn` matched a `termination_by` belonging to a *later* declaration.

### 5.3 The result: the pool genuinely contains no noncomputable definitions

After correction: **171 computable, 1 well-founded (`Multiset.strongInductionOn`, not in the
certified population), 0 noncomputable.** 5 declarations could not be located in their module
files (name-resolution mismatches) and defaulted to computable — a small, flagged uncertainty.

The likely cause is upstream and worth knowing: the miner's **fact-supply gate** filters
noncomputable definitions out of the eligible pool, because they have no decidable facts. So the
computable/noncomputable fairness question the style label was meant to support **cannot be
studied on this corpus at all** — there is nothing to compare. That is a mining-side finding, not
a selection problem, and it will recur on any batch-4-derived corpus.

### 5.4 Quota overshoot required a deterministic trim

Filling shape quotas after the hard-first pass overshot to 51. Resolved by removing the *weakest
non-hard* task (fewest facts, then fewest certified rejects) so the hard tier can never be cut by
a rounding artefact. Deterministic and seeded.

---

## 6. Score-only annex (7) — the 85-vs-121 rider

Drawn from the 38 uncertified-reject tasks. **Harvested at reduced N, scored, never entering
training data.** Marked `annex: true` in the config.

**Purpose:** settle whether an uncertified reject fact produces any verdict against real
candidates — PASS on the negation, FAIL, or UNKNOWN-for-everyone. If they are inert, the corpus
headline is 85; if they fire, it is 121.

| task | negation shapes | reject facts | suite |
|---|---|---|---|
| `SimpleGraph.finsetWalkLength` | `¬` , `≠` , `∉` | 4 | 13 |
| `Hypergraph.EAdj` | `¬` , `∉` | 3 | 13 |
| `Antivary` | `¬` | 3 | 14 |
| `List.TFAE` | `¬` | 3 | 14 |
| `Relator.RightUnique` | `¬` | 3 | 14 |
| `Monovary` | `¬` | 2 | 13 |
| `MonovaryOn` | `¬` | 2 | 13 |

Shape coverage is honest but **uneven, and this is a limitation of the pool, not the pick**: `¬`
dominates the uncertified population, and `≠`/`∉` occur only alongside `¬` — no task in the 38 has
an uncertified reject fact of `≠` or `∉` shape *alone*. The two multi-shape tasks
(`finsetWalkLength`, `EAdj`) are included precisely so the non-`¬` shapes are represented at all.

**Prediction on record, so the rider can falsify it:** these will mostly return UNKNOWN. The
reasoning is mechanical — all 75 uncertified reject facts corpus-wide are proof-mechanism, and the
ladder's discharge step runs *forward* tactics (`rfl, omega, norm_num, positivity, simp, exact?,
aesop`) at a negation, with no `push_neg` and no witness search. If it cannot prove `¬P(w)`
against the truth, it likely cannot against a correct candidate either. If the annex instead shows
these firing, that inference is wrong and the corpus headline moves to 121.
