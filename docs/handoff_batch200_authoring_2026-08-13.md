# Handoff: the 200-task authoring run under the new fact-generation rules

**Date:** 13 August 2026. **Audience:** planning session with no prior context.
**Pins:** Lean v4.32.0, Mathlib `81a5d257c8e410db227a6665ed08f64fea08e997`.
**Artifacts:** `prelim_testing/tasks_batch200/` (172 task dirs + batch reviews),
`authoring/batches/batch200_{passing,preflight}.*`.

Every number below is measured from the shipped corpus. Where a claim is an inference rather than
a measurement, it says so.

---

# 1. What was run

The fact-generation overhaul from the previous handoff, applied to 200 fresh definitions.

**Selection.** Batch-4 eligible pool (721) in manifest rank order, minus the 29 July 50-name
selection, anything already authored, and the three exemplar burns. 677 available, first 200
taken (ranks 3–240), committed *before* authoring so it could not be fitted to results.

**Preflight.** 188 of 200 pass (94%). The 12 failures split 5 "printed type does not reparse",
5 "no derivable task symbol" (subscripts like `sumLift₂`), 2 stuck typeclass metavariables.
Worth feeding back to mining: **preflight-ability is not an eligibility gate**, so ~6% of the
eligible pool cannot be authored as-is.

**Roles.** Sonnet 4.6 authored everything; the kernel validated. DeepSeek was trialled as author
and rejected — see §7.

---

# 2. Outcome

| | |
|---|---|
| tasks attempted | 188 |
| **tasks shipped** | **172 (91.5%)** |
| rotated | 16 (all retryable) |
| facts shipped | **1,366** |
| cost | **$0.169/task**, ~$32 total |
| projection, full 721 | ~$122 |

All 172 are schema-valid.

## Fact composition

| | |
|---|---|
| mean / median suite | 7.9 / 8 (range 1–14) |
| by type | global 892 (65%) · membership 292 (21%) · casework 182 (13%) |
| by mechanism | proof 1,073 · **decide 293 (21%)** |
| **kernel-CERTIFIED against truth** | **1,040 (76%)** |
| PROVISIONALLY_VALIDATED | 326 |
| `self_restatement` set | 463 (34%), all on anchored proof facts |
| `anchors_resolved` populated | 892 / 892 anchored facts |

Two things improved materially against the old 41-task corpus: the decide share fell from
**41.6% → 21%**, and **76% of facts are now discharged against the real Mathlib object at
authoring time** where previously *none* were (validation was an LLM cross-check that never ran
the kernel, and shipped two facts that were provably false of their own ground truth).

---

# 3. How many "good" tasks — it depends entirely on the bar

This is the section to read. A single number is misleading; the ladder is the answer.

| tier | requirement | tasks | share |
|---|---|---|---|
| 1 | shipped, schema-valid | 172 | 100% |
| 2 | ≥1 kernel-certified fact | 170 | 98.8% |
| 3 | ≥1 certified **proof** fact | 163 | 94.8% |
| 4 | ≥1 **reject** fact — *a vacuity detector exists* | 126 | 73.3% |
| 5 | that reject fact is **certified** — *the detector demonstrably works* | 88 | 51.2% |
| 6 | suite floor ≥8 facts | 96 | 55.8% |
| 7 | reject floor ≥2 | 88 | 51.2% |

Composite definitions, given twice — counting any reject fact, and requiring it be certified:

| definition | any reject | certified reject |
|---|---|---|
| **USABLE** ≥1 reject + ≥1 certified proof | **121 (70%)** | 85 (49%) |
| **SOLID** ≥8 facts, ≥1 reject, ≥3 certified proof | **75 (44%)** | 52 (30%) |
| **STRICT** ≥8 facts, ≥2 rejects, decide cap respected | **57 (33%)** | 27 (16%) |

**Recommended headline: 121 usable tasks (70%)**, on the operator's decision that a reject fact
need not be decidable and that a floor of 1 is acceptable. 51 tasks have no reject fact at all.

Note 121 is only 5 below the 126 that have any reject fact — once uncertified rejects are
accepted, the certified-proof requirement costs almost nothing.

**The caveat attached to 121.** It is not established that an *uncertified* reject fact fires at
scoring time. Reasoning (not measurement): a reject fact yields PASS only if something can prove
`¬P(w)` in the candidate's environment; if the ladder cannot prove it against the TRUTH, where
it is definitely true, it probably cannot prove it against a correct candidate either — so it
returns UNKNOWN for correct and vacuous candidates alike, and UNKNOWN is excluded from
fidelity's denominator. **85 is the conservative count, 121 the optimistic one.** Settling this
costs one cheap experiment: run a sample of uncertified reject facts against a real candidate.

---

# 4. The 126 → 88 gap, explained

The sharpest drop in the ladder, and it has a single clean cause.

| reject facts | certified |
|---|---|
| decide-mechanism | **62 / 63 (98%)** |
| proof-mechanism | **121 / 237 (51%)** |

**All 75 uncertified reject facts in the 38 affected tasks are proof-mechanism. Not one is
decide-mechanism.**

Why: a reject fact is a NEGATION (`¬ VTask.Antivary f g`). Certifying it means proving that
negation about the real object. Decide-mechanism facts are computed by the kernel — instant. But
proof-mechanism facts go through the ladder's discharge step, which runs the **forward** tier-2
tactic set (`rfl, omega, norm_num, positivity, simp, exact?, aesop`, plus definition unfolding).
None of those is `push_neg`; none does witness search. They are tuned for proving things true.

This is the **third** appearance of the same underlying issue in this project:

1. the tier-5 truth-countercheck could not refute `Nat.divisors/divisors_mem_iff` until it reused
   the model's own witness script;
2. the validation ladder's negation check missed both known-defective facts until a degenerate-
   value grid (`intro h; have := h 0 1; simp at this`) was added;
3. now the discharge step, for the same reason.

**Proving negations needs different tactics from proving positives, and the discharge path never
got them.** `NEGATION_TACTICS` already exists in `authoring/fact_validation.py` — it simply is
not used on the discharge of reject facts. That is the highest-value outstanding fix: it would
move a large share of 38 tasks from "detector exists" to "detector works", i.e. much of the
121-vs-85 spread, without reclassifying anything as decidable.

---

# 5. Rule compliance — the recurring lesson

| rule | result | enforced? |
|---|---|---|
| decide cap ≤6 | 159/172 (**13 over**) | mechanically, but bypassed — see below |
| suite floor ≥8 | 96/172 | reported only |
| reject floor ≥2 | 88/172 | one re-ask, then reported |
| reject ≥1 | 126/172 | — |
| `near_miss_clause` set | **0 / 1,366** | requested only |

The pattern held all run: **what is enforced holds; what is requested does not.**

`near_miss_clause` at 0 of 1,366 is now conclusive rather than a small-sample impression. Sonnet
has never once set it, despite explicit instruction. The per-clause near-miss design needs
enforcement or different elicitation, not a prompt line.

## The reject top-up — the efficacy data

One focused re-ask when a suite lands under the floor; never discards the task. It fired **88
times**:

| outcome | count |
|---|---|
| success — floor reached (0→2, or 1→2) | **26** |
| partial — improved but short (0→1) | 9 |
| no usable gain | 53 |
| call failed | 2 |

**~30% conversion outright, ~10% partial.** Modest but real: 26 suites that would have shipped
below the floor, for one extra call each.

## The cap bypass — a live bug

All 13 over-cap suites are the same defect: the **reject top-up appends facts after composition
has already trimmed to the cap**. `Equiv.sumProdDistrib` is the clearest specimen — its last two
facts are `polarity=reject` decide facts taking it from 6 to 8. The top-up's additions never pass
through `enforce`.

This matters beyond the count: the operator is minded to raise the cap to 8 later, and an
unenforced cap will not behave predictably at any value. Fix: route top-up additions through
`composition.enforce` before appending.

---

# 6. Rotations — 109 across all passes

| stage | count |
|---|---|
| mechanical_validation | 37 |
| dossier_consistency | 25 |
| classification | 20 |
| emit | 10 |
| truth_splice | 7 |
| round_trip | 8 |
| fact_proposal / dossier | 2 |

## Why facts fail mechanical validation (131 fact-level drops)

| cause | count |
|---|---|
| `PROPOSITION_DOES_NOT_ELABORATE` | 31 |
| `ANCHOR_NOT_FOUND` (hallucinated theorem) | 21 |
| `GLOBAL_DOMAIN_UNCHECKED` | 20 |
| `INSTANCE_DOES_NOT_ELABORATE` | 19 |
| `FALSE_OF_GROUND_TRUTH` | 15 |
| `DOMAIN_UNDECIDED` | 13 |
| `DOES_NOT_MENTION_PINNED_NAME` | 12 |

Three distinct phenomena:

- **~50 elaboration failures** — dominated by "failed to synthesize instance of type class".
  These cluster hard on **definitions taking PROOF arguments or dependent type families**:
  `Walk.takeUntil (p : G.Walk v w) (u : V) : u ∈ p.support → G.Walk v u`, `Walk.ofSupport
  (hne : l ≠ []) (hchain : IsChain …)`, `Equiv.piFinsetUnion (h : Disjoint s t)`,
  `Finset.sigmaLift`, `List.TProd.mk`, `YoungDiagram.ofRowLens (hw : w.SortedGE)`. To state any
  fact about `takeUntil` you must construct a graph, a walk, a vertex AND a proof the vertex is
  in the walk's support. From a dossier alone, without the Lean source, the model cannot produce
  a well-typed inhabitant. This is a real capability limit, and it is exactly the contingency the
  fact prompt's own header anticipates ("if casework quality suffers without sight of the
  implementation, the definition body may be admitted into this call").
- **21 hallucinated anchors.**
- **~45 ordinary authoring errors** — including **15 facts outright false of ground truth**,
  which the new ladder now catches at authoring time rather than months later.

## No retry exists here — an unintentional asymmetry

Mechanical-validation drops get **no retry** (the batch review prints "(no retry)"), yet the same
pipeline retries parse/format rejections once, and retries round-trip compile failures with the
**compile error fed back to the model**. The errors here are specific and actionable
(`failed to synthesize instance of type class Preorder ι`, `anchor 'Foo.bar' does not resolve`).

Estimated retry-amenable share of the 131 drops: elaboration 50 (yes), anchors 21 (yes),
domain/pinned-name 32 (yes, purely mechanical), false-of-truth 15 (sometimes). Cost ≈ one extra
call per task with drops, ~$0.03–0.05/task.

**Agreed plan (not yet implemented):** add the retry, then re-run the 16 rotated tasks plus the
mechanical-validation losses. Deferred deliberately so the main run stayed on consistent settings.

---

# 7. DeepSeek as author — tried and rejected

When Sonnet hit its daily token quota mid-batch (the fourth such day), DeepSeek V3.2 was wired in
via a `BedrockClient`-shaped Converse adapter. Result on 3 tasks: 1 shipped (6 facts, 6 decide,
**0 reject**), 2 rotated because its dossiers lacked the required `Signature` section.

Consistent with everything else measured about it: DeepSeek is excellent at the **mechanical**
job (449 tier-5 proof goals at 24.7%, 100% parseable, zero truncation) and weak at multi-section
structured prose with compositional constraints. The original role split — Sonnet authors,
DeepSeek does mechanical work — is correct. The adapter remains in the tree, unused for authoring.

---

# 8. Outstanding work, in priority order

1. **Negation tactics on the discharge of reject facts** (§4). Highest value: converts "detector
   exists" into "detector works" and closes most of the 121-vs-85 spread. `NEGATION_TACTICS`
   already exists in the same module.
2. **Measure whether uncertified reject facts fire at scoring time** (§3 caveat). Cheap, and it
   decides whether the corpus headline is 85 or 121.
3. **Mechanical-validation retry with errors fed back** (§6), then re-run the 16 rotated tasks.
4. **Fix the cap bypass** (§5) — route top-up additions through `enforce`.
5. **`near_miss_clause` needs enforcement, not instruction** (§5).
6. **Dossier name-leaking** caused 25 rotations, the second-largest bucket. Out of scope for this
   package (dossier prompts were explicitly excluded) but now the biggest lever after the retry.
7. Re-mine the two quarantined facts (`Nat.log/log_lt_of_lt_pow`,
   `Nat.divisors/divisors_mem_iff`) with their `n ≠ 0` hypotheses restored.

---

# 9. Process note

Four bugs were shipped into live runs during this package and caught only by running:
a `repl_warmup` return-type error (rotated ~17 tasks *after* their Bedrock calls were paid for),
a `pinned_signature.imports` attribute error, an over-broad restatement gate that rejected every
casework fact, and an anchor probe with false negatives on ordinary theorems that collapsed suites
to 2.8 facts.

The most expensive mistake was not a bug: `render_batch_review` printed stage records only for
ROTATED tasks, so the reject top-up was invisible on every successful task. "The top-up never
fires" was diagnosed three times from absence of evidence and chased with a live run each time.
A per-stage census later proved there had been no attrition bug at all. Shipped tasks now print
their composition/validation records.

**Lesson worth carrying:** verify instrumentation before diagnosing from it, and smoke-test one
task end-to-end before committing a batch.
